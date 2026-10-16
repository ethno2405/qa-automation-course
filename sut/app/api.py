"""REST API of the course shop. The interactive description is at /docs."""

import asyncio
import base64
import binascii
import os
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Query, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StrictBool, StrictInt

from app import defects, services
from app.events import hub
from app.logs import log_event
from app.rules import RuleError
from app.store import User, store

router = APIRouter(prefix="/api")


# Request and response models


class RegisterIn(BaseModel):
    username: str
    password: str
    email: str
    age: StrictInt
    member: StrictBool = False


class LoginIn(BaseModel):
    username: str
    password: str


class CartItemIn(BaseModel):
    product_id: StrictInt
    quantity: StrictInt


class QuantityIn(BaseModel):
    quantity: StrictInt


class OrderIn(BaseModel):
    coupon: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    age: int
    member: bool
    is_admin: bool


class TokenOut(BaseModel):
    token: str
    username: str


class ProductOut(BaseModel):
    id: int
    title: str
    author: str
    year: int
    price: str
    stock: int


class ProductPage(BaseModel):
    items: list[ProductOut]
    page: int
    page_size: int
    total: int


class CartLineOut(BaseModel):
    product_id: int
    title: str
    unit_price: str
    quantity: int
    line_price: str


class CartOut(BaseModel):
    items: list[CartLineOut]
    count: int
    subtotal: str
    discount: str
    discount_name: str | None
    shipping: str
    total: str
    coupon: str | None
    coupon_error: str | None


class OrderLineOut(BaseModel):
    product_id: int
    title: str
    unit_price: str
    quantity: int


class HistoryOut(BaseModel):
    status: str
    at: str


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    items: list[OrderLineOut]
    subtotal: str
    discount: str
    discount_name: str | None
    shipping: str
    total: str
    coupon: str | None
    history: list[HistoryOut]


class HealthOut(BaseModel):
    status: str
    version: str
    defects: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str


class OAuthError(BaseModel):
    error: str
    error_description: str


# Authentication: a bearer token, or the session cookie of the web UI


def _token(request: Request) -> str | None:
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header.removeprefix("Bearer ").strip()
    return request.cookies.get("session")


def user_for_any_token(token: str | None) -> User | None:
    """Return the user of a login token, or the service user of a valid API client token (R8)."""
    if not token:
        return None
    user = store.user_for_token(token)
    if user is not None:
        return user
    state = store.client_token_state(token)
    if state == "expired":
        raise RuleError(401, "The access token has expired. Get a new token.")
    return store.ship_bot if state == "valid" else None


def current_user(request: Request) -> User:
    user = user_for_any_token(_token(request))
    if user is None:
        raise RuleError(401, "Log in first. Send the header 'Authorization: Bearer <token>'.")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


# Endpoints


@router.get("/health", response_model=HealthOut, tags=["system"])
def health(request: Request) -> dict[str, str]:
    return {"status": "ok", "version": request.app.state.version, "defects": defects.mode()}


@router.post("/admin/reset", status_code=204, tags=["system"])
def reset() -> Response:
    """Load the seed data again. Available only when SUT_TEST_MODE is 1."""
    if os.environ.get("SUT_TEST_MODE", "1") != "1":
        raise RuleError(404, "Not found.")
    store.reset()
    return Response(status_code=204)


# OAuth 2.0 client credentials grant for API clients (R8)

OAUTH_SCOPE = "orders:ship"


def _oauth_error(status: int, error: str, description: str) -> JSONResponse:
    headers = {"Cache-Control": "no-store"}
    if status == 401:
        headers["WWW-Authenticate"] = 'Basic realm="course-shop"'
    return JSONResponse({"error": error, "error_description": description}, status_code=status, headers=headers)


def _client_credentials(request: Request, client_id: str, client_secret: str) -> tuple[str, str]:
    header = request.headers.get("Authorization", "")
    if header.startswith("Basic "):
        try:
            decoded = base64.b64decode(header.removeprefix("Basic ").strip(), validate=True).decode()
        except (binascii.Error, UnicodeDecodeError):
            return "", ""
        name, _, secret = decoded.partition(":")
        return name, secret
    return client_id, client_secret


@router.post(
    "/oauth/token",
    response_model=TokenResponse,
    responses={400: {"model": OAuthError}, 401: {"model": OAuthError}},
    tags=["oauth"],
)
def oauth_token(
    request: Request,
    grant_type: Annotated[str, Form()] = "",
    scope: Annotated[str, Form()] = "",
    client_id: Annotated[str, Form()] = "",
    client_secret: Annotated[str, Form()] = "",
) -> JSONResponse:
    """Get an access token with the client credentials grant (RFC 6749, section 4.4)."""
    if not grant_type:
        return _oauth_error(400, "invalid_request", "The parameter grant_type is missing.")
    name, secret = _client_credentials(request, client_id, client_secret)
    expected_name = os.environ.get("SUT_OAUTH_CLIENT_ID", "ship-bot")
    expected_secret = os.environ.get("SUT_OAUTH_CLIENT_SECRET", "ShipBot-Secret-1")
    if not (secrets.compare_digest(name, expected_name) and secrets.compare_digest(secret, expected_secret)):
        log_event("oauth_client_rejected")
        return _oauth_error(401, "invalid_client", "The client authentication failed.")
    if grant_type != "client_credentials":
        return _oauth_error(400, "unsupported_grant_type", "Only the grant type client_credentials is supported.")
    if scope not in ("", OAUTH_SCOPE):
        return _oauth_error(400, "invalid_scope", f"The only scope is {OAUTH_SCOPE}.")
    lifetime = int(os.environ.get("SUT_OAUTH_TOKEN_SECONDS", "300"))
    token = store.new_client_token(lifetime)
    log_event("oauth_token_issued", client_id=name)
    body = {"access_token": token, "token_type": "Bearer", "expires_in": lifetime, "scope": OAUTH_SCOPE}
    return JSONResponse(body, headers={"Cache-Control": "no-store"})


# Order events over a WebSocket (R9)


@router.websocket("/ws/orders")
async def order_events(websocket: WebSocket, token: str | None = None) -> None:
    try:
        user = user_for_any_token(token or websocket.cookies.get("session"))
    except RuleError:
        user = None
    if user is None:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    subscriber = hub.subscribe(user)
    log_event("websocket_connected", user_id=user.id)

    async def forward() -> None:
        while True:
            await websocket.send_json(await subscriber.queue.get())

    sender: asyncio.Task[None] | None = None
    try:
        await websocket.send_json({"event": "subscribed", "username": user.username})
        sender = asyncio.create_task(forward())
        while True:
            await websocket.receive_text()  # The client sends nothing. This call detects the close.
    except WebSocketDisconnect:
        pass
    finally:
        if sender is not None:
            sender.cancel()
        hub.unsubscribe(subscriber)
        log_event("websocket_closed", user_id=user.id)


@router.post("/users", status_code=201, response_model=UserOut, tags=["users"])
def register(data: RegisterIn) -> dict[str, object]:
    user = services.register(data.username, data.password, data.email, data.age, data.member)
    return services.user_json(user)


@router.get("/users/me", response_model=UserOut, tags=["users"])
def me(user: CurrentUser) -> dict[str, object]:
    return services.user_json(user)


@router.post("/auth/login", response_model=TokenOut, tags=["users"])
def login(data: LoginIn) -> dict[str, str]:
    token = services.login(data.username, data.password)
    user = store.user_for_token(token)
    assert user is not None
    return {"token": token, "username": user.username}


@router.post("/auth/logout", status_code=204, tags=["users"])
def logout(request: Request, user: CurrentUser) -> Response:
    token = _token(request)
    if token:
        store.drop_token(token)
    return Response(status_code=204)


@router.get("/products", response_model=ProductPage, tags=["catalog"])
def products(
    q: str = "",
    page: Annotated[int, Query()] = 1,
    page_size: Annotated[int, Query()] = 10,
) -> dict[str, object]:
    return services.search_products(q, page, page_size)


@router.get("/products/{product_id}", response_model=ProductOut, tags=["catalog"])
def product(product_id: int) -> dict[str, object]:
    return services.product_json(services.get_product(product_id))


@router.get("/cart", response_model=CartOut, tags=["cart"])
def cart(user: CurrentUser, coupon: str | None = None) -> dict[str, object]:
    return services.cart_json(user, coupon)


@router.post("/cart/items", status_code=201, response_model=CartOut, tags=["cart"])
def add_item(data: CartItemIn, user: CurrentUser) -> dict[str, object]:
    services.add_to_cart(user, data.product_id, data.quantity)
    return services.cart_json(user)


@router.put("/cart/items/{product_id}", response_model=CartOut, tags=["cart"])
def change_item(product_id: int, data: QuantityIn, user: CurrentUser) -> dict[str, object]:
    services.set_cart_quantity(user, product_id, data.quantity)
    return services.cart_json(user)


@router.delete("/cart/items/{product_id}", response_model=CartOut, tags=["cart"])
def remove_item(product_id: int, user: CurrentUser) -> dict[str, object]:
    services.remove_from_cart(user, product_id)
    return services.cart_json(user)


@router.post("/orders", status_code=201, response_model=OrderOut, tags=["orders"])
def place_order(user: CurrentUser, data: OrderIn | None = None) -> dict[str, object]:
    order = services.place_order(user, data.coupon if data else None)
    return services.order_json(order)


@router.get("/orders", response_model=list[OrderOut], tags=["orders"])
def orders(user: CurrentUser) -> list[dict[str, object]]:
    return [services.order_json(order) for order in services.list_orders(user)]


@router.get("/orders/{order_id}", response_model=OrderOut, tags=["orders"])
def order(order_id: int, user: CurrentUser) -> dict[str, object]:
    return services.order_json(services.get_order(user, order_id))


@router.post("/orders/{order_id}/{action}", response_model=OrderOut, tags=["orders"])
def order_action(order_id: int, action: str, user: CurrentUser) -> dict[str, object]:
    """Change the status of an order. Actions: pay, cancel (owner), ship, deliver (administrator)."""
    if action not in ("pay", "cancel", "ship", "deliver"):
        raise RuleError(404, "The action is not known.")
    return services.order_json(services.change_order(user, order_id, action))
