"""Business rules of the course shop. See REQUIREMENTS.md."""

import re
from dataclasses import dataclass
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from app import defects

CENT = Decimal("0.01")
ZERO = Decimal("0.00")

USERNAME_MIN = 3
USERNAME_MAX = 20
PASSWORD_MIN = 8
PASSWORD_MAX = 64
AGE_MIN = 16
AGE_MAX = 120
QUANTITY_MIN = 1
QUANTITY_MAX = 10
MAX_FAILED_LOGINS = 3

MEMBER_RATE = Decimal("0.05")
WELCOME_RATE = Decimal("0.10")
BOOKS5_AMOUNT = Decimal("5.00")
BOOKS5_MIN_SUBTOTAL = Decimal("30.00")

SHIPPING_LOW_LIMIT = Decimal("25.00")
SHIPPING_FREE_LIMIT = Decimal("50.00")
SHIPPING_HIGH = Decimal("4.99")
SHIPPING_LOW = Decimal("2.99")

_USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RuleError(Exception):
    """A request breaks a business rule."""

    def __init__(self, status: int, message: str, details: list[dict[str, str]] | None = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.details = details or []


# Registration (R1)


def validate_registration(username: object, password: object, email: object, age: object) -> list[dict[str, str]]:
    """Return one error for each field that is not valid (R1.2 to R1.7)."""
    errors: list[dict[str, str]] = []

    username_max = USERNAME_MAX + 1 if defects.on("D02") else USERNAME_MAX
    if not isinstance(username, str) or not USERNAME_MIN <= len(username) <= username_max:
        errors.append({"field": "username", "message": f"The user name must have {USERNAME_MIN} to {USERNAME_MAX} characters."})
    elif not _USERNAME_PATTERN.match(username):
        errors.append({"field": "username", "message": "The user name must start with a letter and contain only letters, digits, and underscores."})

    if not isinstance(password, str) or not PASSWORD_MIN <= len(password) <= PASSWORD_MAX:
        errors.append({"field": "password", "message": f"The password must have {PASSWORD_MIN} to {PASSWORD_MAX} characters."})
    elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        errors.append({"field": "password", "message": "The password must contain at least one letter and one digit."})

    if not isinstance(email, str) or not _EMAIL_PATTERN.match(email):
        errors.append({"field": "email", "message": "The email address is not valid."})

    if isinstance(age, bool) or not isinstance(age, int) or not AGE_MIN <= age <= AGE_MAX:
        errors.append({"field": "age", "message": f"The age must be a whole number from {AGE_MIN} to {AGE_MAX}."})

    return errors


# Login (R2)


def failed_login_limit() -> int:
    """Return the number of failed logins that locks an account (R2.3)."""
    return MAX_FAILED_LOGINS + 1 if defects.on("D05") else MAX_FAILED_LOGINS


# Cart (R4)


def check_quantity(quantity: object) -> int:
    """Return the quantity if it is in the permitted range (R4.2, R4.5)."""
    quantity_min = 0 if defects.on("D06") else QUANTITY_MIN
    if isinstance(quantity, bool) or not isinstance(quantity, int) or not quantity_min <= quantity <= QUANTITY_MAX:
        raise RuleError(422, f"The quantity must be a whole number from {QUANTITY_MIN} to {QUANTITY_MAX}.")
    return quantity


# Prices (R5)


@dataclass(frozen=True)
class Quote:
    subtotal: Decimal
    discount: Decimal
    discount_name: str | None
    shipping: Decimal
    total: Decimal
    coupon: str | None
    coupon_error: str | None


def _round(amount: Decimal) -> Decimal:
    rounding = ROUND_DOWN if defects.on("D09") else ROUND_HALF_UP
    return amount.quantize(CENT, rounding=rounding)


def _coupon_discount(code: str, subtotal: Decimal, is_first_order: bool) -> Decimal:
    if code == "WELCOME10":
        if not is_first_order:
            raise RuleError(422, "The coupon WELCOME10 is valid only for the first order.")
        return _round(subtotal * WELCOME_RATE)
    if code == "BOOKS5":
        if subtotal < BOOKS5_MIN_SUBTOTAL:
            raise RuleError(422, "The coupon BOOKS5 is valid only for a subtotal of 30.00 EUR or more.")
        return BOOKS5_AMOUNT
    raise RuleError(422, "The coupon code is not known.")


def shipping_cost(order_value: Decimal) -> Decimal:
    """Return the shipping cost for an order value (R5.8)."""
    if order_value < SHIPPING_LOW_LIMIT:
        return SHIPPING_HIGH
    free = order_value > SHIPPING_FREE_LIMIT if defects.on("D01") else order_value >= SHIPPING_FREE_LIMIT
    return ZERO if free else SHIPPING_LOW


def quote(subtotal: Decimal, member: bool, coupon: str | None, is_first_order: bool) -> Quote:
    """Calculate the discount, the shipping cost, and the total (R5)."""
    coupon = coupon.strip() if coupon else None
    if subtotal == ZERO:
        return Quote(ZERO, ZERO, None, ZERO, ZERO, coupon, None)

    candidates: list[tuple[Decimal, str]] = []
    coupon_error = None
    if coupon:
        try:
            candidates.append((_coupon_discount(coupon, subtotal, is_first_order), coupon))
        except RuleError as error:
            coupon_error = error.message
    if member:
        candidates.append((_round(subtotal * MEMBER_RATE), "MEMBER"))

    discount = ZERO
    discount_name = None
    if candidates:
        if defects.on("D03"):
            discount = sum((amount for amount, _ in candidates), ZERO)
            discount_name = "+".join(name for _, name in candidates)
        else:
            # The coupon is first in the list, so it wins when the amounts are equal (R5.6).
            discount, discount_name = max(candidates, key=lambda candidate: candidate[0])

    shipping = shipping_cost(subtotal - discount)
    total = subtotal - discount + shipping
    return Quote(subtotal, discount, discount_name, shipping, total, coupon, coupon_error)


# Orders (R6)

STATUSES = ("NEW", "PAID", "SHIPPED", "DELIVERED", "CANCELLED")

_TRANSITIONS: dict[tuple[str, str], str] = {
    ("NEW", "pay"): "PAID",
    ("NEW", "cancel"): "CANCELLED",
    ("PAID", "cancel"): "CANCELLED",
    ("PAID", "ship"): "SHIPPED",
    ("SHIPPED", "deliver"): "DELIVERED",
}

ADMIN_ACTIONS = frozenset({"ship", "deliver"})


def next_status(status: str, action: str) -> str:
    """Return the new status, or raise a RuleError if the change is not possible (R6.5)."""
    if defects.on("D04") and (status, action) == ("SHIPPED", "cancel"):
        return "CANCELLED"
    new_status = _TRANSITIONS.get((status, action))
    if new_status is None:
        raise RuleError(409, f"The action '{action}' is not possible for an order with the status {status}.")
    return new_status
