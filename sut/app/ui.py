"""Web UI of the course shop. Server-rendered pages with a small script for the cart."""

import os
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app import defects, services
from app.rules import RuleError
from app.store import User, store

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

SLOW_UI = os.environ.get("SUT_SLOW_UI", "0") == "1"


def _user(request: Request) -> User | None:
    token = request.cookies.get("session")
    return store.user_for_token(token) if token else None


def _page(request: Request, name: str, user: User | None, status: int = 200, **context: Any) -> HTMLResponse:
    count = services.cart_json(user)["count"] if user else 0
    return templates.TemplateResponse(
        request,
        name,
        {"user": user, "cart_count": count, "slow_ui": SLOW_UI, "legacy_cart": defects.on("D10"), **context},
        status_code=status,
    )


def _to_login(request: Request) -> RedirectResponse:
    return RedirectResponse(f"/login?next={quote(request.url.path)}", status_code=303)


@router.get("/")
def home() -> RedirectResponse:
    return RedirectResponse("/products", status_code=303)


@router.get("/products")
def products(request: Request, q: str = "", page: int = 1) -> HTMLResponse:
    try:
        result = services.search_products(q, page, 10)
    except RuleError as error:
        return _page(request, "products.html", _user(request), status=error.status, q=q, result=None, error=error.message)
    pages = max(1, -(-result["total"] // 10))
    return _page(request, "products.html", _user(request), q=q, result=result, pages=pages, error=None)


@router.get("/products/{product_id}")
def product(request: Request, product_id: int) -> HTMLResponse:
    try:
        item = services.get_product(product_id)
    except RuleError as error:
        return _page(request, "error.html", _user(request), status=error.status, message=error.message)
    return _page(request, "product.html", _user(request), product=item)


@router.get("/login")
def login_form(request: Request, next: str = "/products", registered: int = 0) -> HTMLResponse:
    return _page(request, "login.html", _user(request), next=next, error=None, registered=registered == 1, username="")


@router.post("/login")
def login(request: Request, username: str = Form(""), password: str = Form(""), next: str = Form("/products")) -> Response:
    try:
        token = services.login(username, password)
    except RuleError as error:
        return _page(request, "login.html", None, status=error.status, next=next, error=error.message, registered=False, username=username)
    target = next if next.startswith("/") and not next.startswith("//") else "/products"
    response = RedirectResponse(target, status_code=303)
    response.set_cookie("session", token, httponly=True, samesite="lax")
    return response


@router.post("/logout")
def logout(request: Request) -> RedirectResponse:
    token = request.cookies.get("session")
    if token:
        store.drop_token(token)
    response = RedirectResponse("/products", status_code=303)
    response.delete_cookie("session")
    return response


@router.get("/register")
def register_form(request: Request) -> HTMLResponse:
    return _page(request, "register.html", _user(request), errors={}, error=None, form={})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    email: str = Form(""),
    age: str = Form(""),
    member: str = Form(""),
) -> Response:
    form = {"username": username, "email": email, "age": age, "member": member == "on"}
    age_value: object = int(age) if age.strip().lstrip("-").isdigit() else age
    try:
        services.register(username, password, email, age_value, member == "on")
    except RuleError as error:
        errors = {item["field"]: item["message"] for item in error.details}
        return _page(request, "register.html", None, status=error.status, errors=errors, error=error.message, form=form)
    return RedirectResponse("/login?registered=1", status_code=303)


@router.get("/cart")
def cart(request: Request, coupon: str = "") -> Response:
    user = _user(request)
    if user is None:
        return _to_login(request)
    return _page(request, "cart.html", user, cart=services.cart_json(user, coupon or None), error=None)


@router.post("/checkout")
def checkout(request: Request, coupon: str = Form("")) -> Response:
    user = _user(request)
    if user is None:
        return _to_login(request)
    try:
        order = services.place_order(user, coupon or None)
    except RuleError as error:
        return _page(request, "cart.html", user, status=error.status, cart=services.cart_json(user, coupon or None), error=error.message)
    return RedirectResponse(f"/orders/{order.id}", status_code=303)


@router.get("/orders")
def orders(request: Request) -> Response:
    user = _user(request)
    if user is None:
        return _to_login(request)
    return _page(request, "orders.html", user, orders=services.list_orders(user))


@router.get("/orders/{order_id}")
def order(request: Request, order_id: int, message: str = "") -> Response:
    user = _user(request)
    if user is None:
        return _to_login(request)
    try:
        item = services.get_order(user, order_id)
    except RuleError as error:
        return _page(request, "error.html", user, status=error.status, message=error.message)
    return _page(request, "order.html", user, order=item, message=message, error=None)


@router.post("/orders/{order_id}/{action}")
def order_action(request: Request, order_id: int, action: str) -> Response:
    user = _user(request)
    if user is None:
        return _to_login(request)
    if action not in ("pay", "cancel", "ship", "deliver"):
        return _page(request, "error.html", user, status=404, message="The action is not known.")
    try:
        services.change_order(user, order_id, action)
    except RuleError as error:
        try:
            item = services.get_order(user, order_id)
        except RuleError:
            return _page(request, "error.html", user, status=error.status, message=error.message)
        return _page(request, "order.html", user, status=error.status, order=item, message="", error=error.message)
    return RedirectResponse(f"/orders/{order_id}?message={quote('The order is updated.')}", status_code=303)
