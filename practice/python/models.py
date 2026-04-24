"""
models.py
Domain types for the LazyVim practice project.

Used in lessons for:
  - LSP navigation: gd (go to definition), gr (references), gI (implementation)
  - Text objects: ci", di(, yi', gsd, gsa, etc.
  - Diagnostic exercises: type annotations give pyright/pylsp something to check
  - Cross-file jumps: imported in pipeline.py and main.py
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Generic, Iterator, Optional, TypeVar


# ── Status ────────────────────────────────────────────────────────────────────


class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = auto()
    SUSPENDED = auto()


# ── Errors ────────────────────────────────────────────────────────────────────


class ValidationError(Exception):
    """Raised when a model fails its own validation rules."""

    def __init__(self, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(f"validation failed for '{field}': {reason}")


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: Any) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier!r}")


# ── Base classes ──────────────────────────────────────────────────────────────


class Describable(ABC):
    """Any model that can produce a human-readable description of itself."""

    @abstractmethod
    def describe(self) -> str: ...

    @abstractmethod
    def short_name(self) -> str: ...


class Validatable(ABC):
    """Any model that can validate its own fields."""

    @abstractmethod
    def validate(self) -> None:
        """Raise ValidationError if the model is not valid."""
        ...

    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValidationError:
            return False


class Serializable(ABC):
    """Any model that can serialise itself to a flat string format."""

    @abstractmethod
    def to_csv_row(self) -> str: ...

    @classmethod
    @abstractmethod
    def field_names(cls) -> list[str]: ...


# ── User ─────────────────────────────────────────────────────────────────────


@dataclass
class User(Describable, Validatable, Serializable):
    id: int
    username: str
    email: str
    status: Status = Status.ACTIVE
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ── Construction helpers ───────────────────────────────────────────────

    def with_tag(self, tag: str) -> "User":
        self.tags.append(tag)
        return self

    def with_meta(self, key: str, value: str) -> "User":
        self.metadata[key] = value
        return self

    # ── State transitions ──────────────────────────────────────────────────

    def activate(self) -> None:
        self.status = Status.ACTIVE

    def deactivate(self) -> None:
        self.status = Status.INACTIVE

    def suspend(self, reason: str = "no reason given") -> None:
        self.status = Status.SUSPENDED
        self.metadata["suspension_reason"] = reason

    # ── Queries ────────────────────────────────────────────────────────────

    def is_active(self) -> bool:
        return self.status == Status.ACTIVE

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def get_meta(self, key: str, default: str = "") -> str:
        return self.metadata.get(key, default)

    # ── Describable ────────────────────────────────────────────────────────

    def describe(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "no tags"
        return (
            f"User #{self.id} — {self.username} <{self.email}> "
            f"[{self.status.name.lower()}] ({tag_str})"
        )

    def short_name(self) -> str:
        return self.username

    # ── Validatable ────────────────────────────────────────────────────────

    def validate(self) -> None:
        if not self.username:
            raise ValidationError("username", "must not be empty")
        if len(self.username) < 3:
            raise ValidationError("username", "must be at least 3 characters")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", self.email):
            raise ValidationError("email", "must be a valid email address")

    # ── Serializable ───────────────────────────────────────────────────────

    def to_csv_row(self) -> str:
        return f"{self.id},{self.username},{self.email},{self.status.name}"

    @classmethod
    def field_names(cls) -> list[str]:
        return ["id", "username", "email", "status"]


# ── Product ───────────────────────────────────────────────────────────────────


@dataclass
class Product(Describable, Validatable):
    sku: str
    name: str
    price_cents: int
    category: str
    stock: int = 0
    tags: list[str] = field(default_factory=list)

    # ── Computed properties ────────────────────────────────────────────────

    @property
    def price(self) -> float:
        return self.price_cents / 100.0

    @property
    def in_stock(self) -> bool:
        return self.stock > 0

    # ── Mutations ──────────────────────────────────────────────────────────

    def restock(self, units: int) -> None:
        if units <= 0:
            raise ValueError(f"restock units must be positive, got {units}")
        self.stock += units

    def sell(self, units: int) -> None:
        if units <= 0:
            raise ValueError(f"sell units must be positive, got {units}")
        if units > self.stock:
            raise ValueError(
                f"insufficient stock for {self.sku!r}: "
                f"need {units}, have {self.stock}"
            )
        self.stock -= units

    def apply_discount(self, percent: float) -> int:
        """Return discounted price in cents (does not mutate)."""
        if not 0.0 <= percent <= 100.0:
            raise ValueError(f"discount percent must be in [0, 100], got {percent}")
        discounted = self.price_cents * (1.0 - percent / 100.0)
        return round(discounted)

    # ── Describable ────────────────────────────────────────────────────────

    def describe(self) -> str:
        stock_str = f"{self.stock} in stock" if self.in_stock else "out of stock"
        return f"Product {self.sku} — {self.name} @ ${self.price:.2f} ({stock_str})"

    def short_name(self) -> str:
        return self.name

    # ── Validatable ────────────────────────────────────────────────────────

    def validate(self) -> None:
        if not self.sku:
            raise ValidationError("sku", "must not be empty")
        if not self.name:
            raise ValidationError("name", "must not be empty")
        if self.price_cents <= 0:
            raise ValidationError("price_cents", "must be greater than zero")


# ── Order ─────────────────────────────────────────────────────────────────────


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price_cents: int

    @property
    def subtotal_cents(self) -> int:
        return self.quantity * self.unit_price_cents

    @property
    def subtotal(self) -> float:
        return self.subtotal_cents / 100.0


@dataclass
class Order(Describable, Validatable):
    id: int
    user_id: int
    lines: list[OrderLine] = field(default_factory=list)
    status: Status = Status.PENDING
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ── Mutations ──────────────────────────────────────────────────────────

    def add_line(self, sku: str, quantity: int, unit_price_cents: int) -> None:
        self.lines.append(OrderLine(sku, quantity, unit_price_cents))

    def confirm(self) -> None:
        self.status = Status.ACTIVE

    def cancel(self, reason: str = "cancelled by user") -> None:
        self.status = Status.SUSPENDED
        self.notes = reason

    # ── Computed ───────────────────────────────────────────────────────────

    @property
    def total_cents(self) -> int:
        return sum(line.subtotal_cents for line in self.lines)

    @property
    def total(self) -> float:
        return self.total_cents / 100.0

    @property
    def item_count(self) -> int:
        return sum(line.quantity for line in self.lines)

    def line_for(self, sku: str) -> Optional[OrderLine]:
        return next((l for l in self.lines if l.sku == sku), None)

    # ── Describable ────────────────────────────────────────────────────────

    def describe(self) -> str:
        return (
            f"Order #{self.id} for user #{self.user_id} — "
            f"{self.item_count} items, total ${self.total:.2f} "
            f"[{self.status.name.lower()}]"
        )

    def short_name(self) -> str:
        return f"order-{self.id}"

    # ── Validatable ────────────────────────────────────────────────────────

    def validate(self) -> None:
        if not self.lines:
            raise ValidationError("lines", "order must have at least one line")
        for line in self.lines:
            if line.quantity <= 0:
                raise ValidationError("quantity", f"must be positive for sku {line.sku!r}")

    # ── Iteration ──────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[OrderLine]:
        return iter(self.lines)


# ── Registry ──────────────────────────────────────────────────────────────────


T = TypeVar("T", bound="Describable")


class Registry(Generic[T]):
    """Generic in-memory registry for any Describable + Validatable type."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items: dict[Any, T] = {}

    def add(self, key: Any, item: T) -> None:
        item.validate()
        self._items[key] = item

    def get(self, key: Any) -> T:
        if key not in self._items:
            raise NotFoundError(self.name, key)
        return self._items[key]

    def all(self) -> list[T]:
        return list(self._items.values())

    def where(self, predicate: Any) -> list[T]:
        return [item for item in self._items.values() if predicate(item)]

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: Any) -> bool:
        return key in self._items
