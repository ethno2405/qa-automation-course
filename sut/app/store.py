"""In-memory data store of the course shop. A restart or a reset loads the seed data again."""

import hashlib
import os
import secrets
import threading
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    salt: str
    email: str
    age: int
    member: bool
    is_admin: bool = False
    failed_logins: int = 0
    locked_until: float | None = None


@dataclass
class Product:
    id: int
    title: str
    author: str
    year: int
    price: Decimal
    stock: int


@dataclass
class OrderLine:
    product_id: int
    title: str
    unit_price: Decimal
    quantity: int


@dataclass
class Order:
    id: int
    user_id: int
    lines: list[OrderLine]
    subtotal: Decimal
    discount: Decimal
    discount_name: str | None
    shipping: Decimal
    total: Decimal
    coupon: str | None
    status: str
    history: list[dict[str, str]] = field(default_factory=list)


SEED_PRODUCTS: list[tuple[str, str, int, str, int]] = [
    ("The Boundary Hunter", "A. Lee", 2019, "12.50", 20),
    ("Partitions of Equivalence", "M. Novak", 2021, "25.00", 15),
    ("Decision Tables for Everyone", "R. Okafor", 2018, "10.00", 30),
    ("The State Machine Garden", "L. Petrova", 2022, "24.99", 12),
    ("Exploring Without a Map", "J. Santos", 2017, "5.00", 50),
    ("Flaky: A Mystery Novel", "K. Ito", 2023, "12.90", 8),
    ("The Pyramid and the Ice Cream Cone", "D. Weber", 2020, "49.99", 5),
    ("Regression Road", "S. Haddad", 2016, "7.45", 25),
    ("Shift Left, Shift Right", "P. Kowalski", 2024, "18.00", 10),
    ("Mocks and Stubs", "E. Dubois", 2015, "9.99", 40),
    ("The Linux Shell Diaries", "T. Andersen", 2021, "15.30", 18),
    ("Packets in the Night", "N. Rossi", 2019, "21.75", 9),
    ("The Handshake", "F. Moreau", 2014, "3.33", 60),
    ("Page Objects in Practice", "H. Schmidt", 2023, "33.00", 7),
    ("The Last Locator", "G. Costa", 2022, "8.80", 22),
    ("Pipelines and Gates", "V. Ivanova", 2024, "27.50", 14),
    ("Contract of the API", "B. Nakamura", 2020, "16.65", 11),
    ("The Seventh Principle", "O. Lindqvist", 2013, "11.11", 33),
    ("Testware", "C. Murphy", 2018, "19.95", 6),
    ("A Defect Named Sue", "W. Brown", 2025, "6.66", 2),
    ("Root Cause", "I. Kaya", 2019, "12.51", 16),
    ("The Oracle Problem", "Y. Cohen", 2021, "23.40", 13),
    ("Coverage Is Not Quality", "Z. Horvat", 2022, "29.99", 10),
    ("Out of Stock Stories", "U. Berg", 2020, "9.50", 0),
]


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class Store:
    """All shop data. Each public method must hold the lock."""

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.reset()

    def reset(self) -> None:
        with self.lock:
            self.users: dict[int, User] = {}
            self.products: dict[int, Product] = {}
            self.carts: dict[int, dict[int, int]] = {}
            self.orders: dict[int, Order] = {}
            self.tokens: dict[str, int] = {}
            self.client_tokens: dict[str, float] = {}
            self._next_user_id = 1
            self._next_order_id = 1001
            for number, (title, author, year, price, stock) in enumerate(SEED_PRODUCTS, start=1):
                self.products[number] = Product(number, title, author, year, Decimal(price), stock)
            admin_password = os.environ.get("SUT_ADMIN_PASSWORD", "Admin12345")
            self.add_user("admin", admin_password, "admin@shop.test", 40, member=False, is_admin=True)
            # The service user of the OAuth 2.0 API client (R8). Nobody knows its password.
            self.ship_bot = self.add_user("ship_bot", secrets.token_urlsafe(32), "ship-bot@shop.test", 40, member=False, is_admin=True)

    # Users

    def add_user(self, username: str, password: str, email: str, age: int, member: bool, is_admin: bool = False) -> User:
        with self.lock:
            salt = secrets.token_hex(16)
            user = User(self._next_user_id, username, hash_password(password, salt), salt, email, age, member, is_admin)
            self.users[user.id] = user
            self._next_user_id += 1
            return user

    def find_user(self, username: str) -> User | None:
        with self.lock:
            wanted = username.lower()
            return next((user for user in self.users.values() if user.username.lower() == wanted), None)

    def new_token(self, user: User) -> str:
        with self.lock:
            token = secrets.token_urlsafe(24)
            self.tokens[token] = user.id
            return token

    def user_for_token(self, token: str) -> User | None:
        with self.lock:
            user_id = self.tokens.get(token)
            return self.users.get(user_id) if user_id is not None else None

    def drop_token(self, token: str) -> None:
        with self.lock:
            self.tokens.pop(token, None)

    def new_client_token(self, lifetime_seconds: float) -> str:
        with self.lock:
            token = secrets.token_urlsafe(32)
            self.client_tokens[token] = time.time() + lifetime_seconds
            return token

    def client_token_state(self, token: str) -> str:
        """Return "valid", "expired", or "unknown" for an access token of the API client."""
        with self.lock:
            expires_at = self.client_tokens.get(token)
        if expires_at is None:
            return "unknown"
        return "valid" if time.time() < expires_at else "expired"

    # Orders

    def new_order_id(self) -> int:
        with self.lock:
            order_id = self._next_order_id
            self._next_order_id += 1
            return order_id

    def has_orders(self, user_id: int) -> bool:
        with self.lock:
            return any(order.user_id == user_id for order in self.orders.values())


def lock_seconds() -> float:
    return float(os.environ.get("SUT_LOCK_MINUTES", "15")) * 60


def is_locked(user: User) -> bool:
    if user.locked_until is None:
        return False
    if time.time() >= user.locked_until:
        user.locked_until = None
        user.failed_logins = 0
        return False
    return True


store = Store()
