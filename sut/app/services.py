"""Shop operations. The API and the web UI both use these functions."""

import time
from decimal import Decimal
from typing import Any

from app import defects, rules
from app.events import hub
from app.logs import log_event
from app.rules import RuleError
from app.store import Order, OrderLine, Product, User, hash_password, is_locked, lock_seconds, now_iso, store

# Users and login


def register(username: Any, password: Any, email: Any, age: Any, member: Any) -> User:
    errors = rules.validate_registration(username, password, email, age)
    if errors:
        raise RuleError(422, "The registration data is not valid.", errors)
    with store.lock:
        if store.find_user(username) is not None:
            raise RuleError(409, "The user name is already in use.", [{"field": "username", "message": "The user name is already in use."}])
        user = store.add_user(username, password, email, age, member=bool(member))
    log_event("user_registered", user_id=user.id)
    return user


def login(username: Any, password: Any) -> str:
    if not isinstance(username, str) or not isinstance(password, str):
        raise RuleError(401, "The user name or the password is wrong.")
    with store.lock:
        user = store.find_user(username)
        if user is None:
            log_event("login_failed", reason="unknown_user")
            raise RuleError(401, "The user name or the password is wrong.")
        if is_locked(user):
            log_event("login_rejected", user_id=user.id, reason="locked")
            raise RuleError(423, "The account is locked. Try again later.")
        if hash_password(password, user.salt) != user.password_hash:
            user.failed_logins += 1
            log_event("login_failed", user_id=user.id, failed_logins=user.failed_logins)
            if user.failed_logins >= rules.failed_login_limit():
                user.locked_until = time.time() + lock_seconds()
                log_event("account_locked", user_id=user.id)
            raise RuleError(401, "The user name or the password is wrong.")
        user.failed_logins = 0
        token = store.new_token(user)
    log_event("login_ok", user_id=user.id)
    return token


def user_json(user: User) -> dict[str, Any]:
    return {"id": user.id, "username": user.username, "email": user.email, "age": user.age, "member": user.member, "is_admin": user.is_admin}


# Catalog


def product_json(product: Product) -> dict[str, Any]:
    return {"id": product.id, "title": product.title, "author": product.author, "year": product.year, "price": str(product.price), "stock": product.stock}


def search_products(text: str, page: Any, page_size: Any) -> dict[str, Any]:
    if isinstance(page, bool) or not isinstance(page, int) or page < 1:
        raise RuleError(422, "The page number must be 1 or more.")
    if isinstance(page_size, bool) or not isinstance(page_size, int) or not 1 <= page_size <= 50:
        raise RuleError(422, "The page size must be from 1 to 50.")
    with store.lock:
        products = list(store.products.values())
    text = text.strip()
    if text:
        if defects.on("D07"):
            products = [p for p in products if text in p.title or text in p.author]
        else:
            wanted = text.lower()
            products = [p for p in products if wanted in p.title.lower() or wanted in p.author.lower()]
    start = (page - 1) * page_size
    return {
        "items": [product_json(p) for p in products[start : start + page_size]],
        "page": page,
        "page_size": page_size,
        "total": len(products),
    }


def get_product(product_id: int) -> Product:
    with store.lock:
        if defects.on("D08"):
            return store.products[product_id]
        product = store.products.get(product_id)
    if product is None:
        raise RuleError(404, "The book was not found.")
    return product


# Cart


def _cart_lines(user: User) -> list[tuple[Product, int]]:
    cart = store.carts.get(user.id, {})
    return [(store.products[product_id], quantity) for product_id, quantity in cart.items()]


def cart_json(user: User, coupon: str | None = None) -> dict[str, Any]:
    with store.lock:
        lines = _cart_lines(user)
        subtotal = sum((product.price * quantity for product, quantity in lines), Decimal("0.00"))
        result = rules.quote(subtotal, user.member, coupon, not store.has_orders(user.id))
    return {
        "items": [
            {"product_id": p.id, "title": p.title, "unit_price": str(p.price), "quantity": q, "line_price": str(p.price * q)}
            for p, q in lines
        ],
        "count": sum(q for _, q in lines),
        "subtotal": str(result.subtotal),
        "discount": str(result.discount),
        "discount_name": result.discount_name,
        "shipping": str(result.shipping),
        "total": str(result.total),
        "coupon": result.coupon,
        "coupon_error": result.coupon_error,
    }


def add_to_cart(user: User, product_id: Any, quantity: Any) -> None:
    quantity = rules.check_quantity(quantity)
    if isinstance(product_id, bool) or not isinstance(product_id, int):
        raise RuleError(422, "The product_id must be a whole number.")
    with store.lock:
        product = store.products.get(product_id)
        if product is None:
            raise RuleError(404, "The book was not found.")
        cart = store.carts.setdefault(user.id, {})
        new_quantity = cart.get(product_id, 0) + quantity
        if new_quantity > rules.QUANTITY_MAX:
            raise RuleError(422, f"The cart can contain not more than {rules.QUANTITY_MAX} copies of one book.")
        if new_quantity > product.stock:
            raise RuleError(422, "There is not enough stock for this quantity.")
        cart[product_id] = new_quantity


def set_cart_quantity(user: User, product_id: int, quantity: Any) -> None:
    quantity = rules.check_quantity(quantity)
    with store.lock:
        cart = store.carts.setdefault(user.id, {})
        if product_id not in cart:
            raise RuleError(404, "The book is not in the cart.")
        if quantity > store.products[product_id].stock:
            raise RuleError(422, "There is not enough stock for this quantity.")
        cart[product_id] = quantity


def remove_from_cart(user: User, product_id: int) -> None:
    with store.lock:
        cart = store.carts.setdefault(user.id, {})
        if product_id not in cart:
            raise RuleError(404, "The book is not in the cart.")
        del cart[product_id]


# Orders


def order_json(order: Order) -> dict[str, Any]:
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "items": [
            {"product_id": line.product_id, "title": line.title, "unit_price": str(line.unit_price), "quantity": line.quantity}
            for line in order.lines
        ],
        "subtotal": str(order.subtotal),
        "discount": str(order.discount),
        "discount_name": order.discount_name,
        "shipping": str(order.shipping),
        "total": str(order.total),
        "coupon": order.coupon,
        "history": order.history,
    }


def place_order(user: User, coupon: Any) -> Order:
    if coupon is not None and not isinstance(coupon, str):
        raise RuleError(422, "The coupon must be a text.")
    with store.lock:
        lines = _cart_lines(user)
        if not lines:
            raise RuleError(409, "The cart is empty.")
        for product, quantity in lines:
            if quantity > product.stock:
                raise RuleError(422, f"There is not enough stock for '{product.title}'.")
        subtotal = sum((product.price * quantity for product, quantity in lines), Decimal("0.00"))
        result = rules.quote(subtotal, user.member, coupon or None, not store.has_orders(user.id))
        if result.coupon_error:
            raise RuleError(422, result.coupon_error, [{"field": "coupon", "message": result.coupon_error}])
        for product, quantity in lines:
            product.stock -= quantity
        order = Order(
            id=store.new_order_id(),
            user_id=user.id,
            lines=[OrderLine(p.id, p.title, p.price, q) for p, q in lines],
            subtotal=result.subtotal,
            discount=result.discount,
            discount_name=result.discount_name,
            shipping=result.shipping,
            total=result.total,
            coupon=result.coupon,
            status="NEW",
            history=[{"status": "NEW", "at": now_iso()}],
        )
        store.orders[order.id] = order
        store.carts[user.id] = {}
    log_event("order_placed", order_id=order.id, user_id=user.id, total=str(order.total))
    hub.publish({"event": "order_placed", "order_id": order.id, "status": "NEW", "at": order.history[0]["at"]}, user.id)
    return order


def list_orders(user: User) -> list[Order]:
    with store.lock:
        return [order for order in store.orders.values() if user.is_admin or order.user_id == user.id]


def get_order(user: User, order_id: int) -> Order:
    with store.lock:
        order = store.orders.get(order_id)
    if order is None or (order.user_id != user.id and not user.is_admin):
        raise RuleError(404, "The order was not found.")
    return order


def change_order(user: User, order_id: int, action: str) -> Order:
    order = get_order(user, order_id)
    if action in rules.ADMIN_ACTIONS and not user.is_admin:
        raise RuleError(403, "Only an administrator can do this action.")
    if action not in rules.ADMIN_ACTIONS and order.user_id != user.id:
        raise RuleError(403, "Only the owner of the order can do this action.")
    with store.lock:
        new_status = rules.next_status(order.status, action)
        if new_status == "CANCELLED":
            for line in order.lines:
                store.products[line.product_id].stock += line.quantity
        old_status = order.status
        order.status = new_status
        order.history.append({"status": new_status, "at": now_iso()})
    log_event("order_status_changed", order_id=order.id, old=old_status, new=new_status)
    event = {"event": "order_status_changed", "order_id": order.id, "old": old_status, "new": new_status, "at": order.history[-1]["at"]}
    hub.publish(event, order.user_id)
    return order
