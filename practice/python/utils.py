"""
utils.py
Utility functions for the LazyVim practice project.

Used in lessons for:
  - Searching with <leader>sw (word search hits these short function names)
  - Text objects: various bracket and string styles across function signatures
  - mini.surround: f-strings and template strings are good surround targets
  - Decorators: good targets for gsa / gsd exercises
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import textwrap
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


# ── Decorators ────────────────────────────────────────────────────────────────


def logged(fn: F) -> F:
    """Log entry and exit of any function."""
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"→ {fn.__name__}({args!r}, {kwargs!r})")
        result = fn(*args, **kwargs)
        print(f"← {fn.__name__} = {result!r}")
        return result
    return wrapper  # type: ignore[return-value]


def retry(times: int = 3, exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable[[F], F]:
    """Retry a function up to `times` times on the given exceptions."""
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Optional[Exception] = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(f"attempt {attempt}/{times} failed: {exc}")
            raise RuntimeError(f"{fn.__name__} failed after {times} attempts") from last_exc
        return wrapper  # type: ignore[return-value]
    return decorator  # type: ignore[return-value]


def deprecated(message: str) -> Callable[[F], F]:
    """Mark a function as deprecated with a custom message."""
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"DeprecationWarning: {fn.__name__} is deprecated. {message}")
            return fn(*args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator  # type: ignore[return-value]


# ── String utilities ──────────────────────────────────────────────────────────


def slugify(text: str, separator: str = "-") -> str:
    """Convert a string to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", separator, text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def truncate(text: str, max_length: int = 80, ellipsis: str = "…") -> str:
    """Truncate text to max_length, appending ellipsis if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(ellipsis)] + ellipsis


def wrap_text(text: str, width: int = 72, indent: str = "") -> str:
    """Word-wrap text to the given width with optional indent."""
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to CamelCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def mask_email(email: str) -> str:
    """Partially mask an email address for safe display."""
    if "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    visible = local[:2] if len(local) >= 2 else local[:1]
    return f"{visible}***@{domain}"


def format_currency(cents: int, symbol: str = "$") -> str:
    """Format an integer number of cents as a currency string."""
    return f"{symbol}{cents / 100:.2f}"


def parse_currency(value: str) -> int:
    """Parse a currency string like '$12.99' into cents (1299)."""
    cleaned = re.sub(r"[^\d.]", "", value)
    if not cleaned:
        raise ValueError(f"cannot parse currency from {value!r}")
    return round(float(cleaned) * 100)


# ── Collection utilities ──────────────────────────────────────────────────────


def chunk(items: list[Any], size: int) -> list[list[Any]]:
    """Split a list into chunks of at most `size` elements."""
    if size <= 0:
        raise ValueError(f"chunk size must be positive, got {size}")
    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten(nested: list[list[Any]]) -> list[Any]:
    """Flatten one level of nesting from a list of lists."""
    return [item for sublist in nested for item in sublist]


def group_by(items: list[Any], key: Callable[[Any], Any]) -> dict[Any, list[Any]]:
    """Group a list of items by the result of a key function."""
    result: dict[Any, list[Any]] = {}
    for item in items:
        k = key(item)
        result.setdefault(k, []).append(item)
    return result


def deduplicate(items: list[Any], key: Optional[Callable[[Any], Any]] = None) -> list[Any]:
    """Return a list with duplicates removed, preserving order."""
    seen: set[Any] = set()
    result = []
    for item in items:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


# ── I/O utilities ─────────────────────────────────────────────────────────────


def to_csv(rows: list[dict[str, Any]], fieldnames: Optional[list[str]] = None) -> str:
    """Serialise a list of dicts to a CSV string."""
    if not rows:
        return ""
    fieldnames = fieldnames or list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def to_json(obj: Any, indent: int = 2) -> str:
    """Serialise an object to a formatted JSON string."""
    return json.dumps(obj, indent=indent, default=str)


def read_env(key: str, default: str = "") -> str:
    """Read an environment variable, returning default if not set."""
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    """Read a required environment variable or raise an error."""
    value = os.environ.get(key)
    if value is None:
        raise EnvironmentError(f"required environment variable {key!r} is not set")
    return value


# ── Date utilities ────────────────────────────────────────────────────────────


def now_utc() -> datetime:
    """Return the current UTC datetime."""
    return datetime.utcnow()


def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """Format a datetime as a string."""
    return dt.strftime(fmt)


def parse_date(value: str, fmt: str = "%Y-%m-%d") -> datetime:
    """Parse a date string into a datetime object."""
    return datetime.strptime(value, fmt)


def days_since(dt: datetime) -> int:
    """Return the number of whole days since the given datetime."""
    delta = now_utc() - dt.replace(tzinfo=None)
    return delta.days


# ── Formatting ────────────────────────────────────────────────────────────────


def print_table(rows: list[dict[str, Any]], max_col_width: int = 30) -> None:
    """Print a list of dicts as a formatted table."""
    if not rows:
        print("(empty)")
        return

    headers = list(rows[0].keys())
    col_widths = {
        h: min(max_col_width, max(len(h), max(len(str(row.get(h, ""))) for row in rows)))
        for h in headers
    }

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths.values()) + "+"
    header_row = "|" + "|".join(f" {h:<{col_widths[h]}} " for h in headers) + "|"

    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        cells = "|".join(
            f" {truncate(str(row.get(h, '')), max_col_width):<{col_widths[h]}} "
            for h in headers
        )
        print(f"|{cells}|")
    print(sep)


def print_section(title: str, width: int = 60) -> None:
    """Print a section header."""
    pad = max(0, width - len(title) - 4)
    left = pad // 2
    right = pad - left
    print(f"\n{'─' * left}  {title}  {'─' * right}")
