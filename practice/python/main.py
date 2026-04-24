"""
main.py
Entry point for the LazyVim Python practice project.

Exercises covered here:
  - LSP cross-file navigation: all imported names are defined in models.py / pipeline.py / utils.py
  - Diagnostics: run `pyright .` or `pylsp` to see type errors
  - Text objects: nested function calls, f-strings, list/dict literals
  - Search: <leader>sg "Pipeline" to find all usages across files
  - Rename: `<leader>cr` on `process_users` to rename across all call sites

Run with:   python main.py
Typecheck:  pyright .   (requires: pip install pyright)
"""

from __future__ import annotations

import logging
import sys
from typing import Optional

from models import (
    NotFoundError,
    Order,
    Product,
    Registry,
    Status,
    User,
    ValidationError,
)
from pipeline import (
    EnrichStage,
    LengthGuardStage,
    NormaliseStage,
    Pipeline,
    TransformStage,
)
from utils import (
    format_currency,
    format_date,
    group_by,
    mask_email,
    print_section,
    print_table,
    slugify,
    to_json,
    truncate,
)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")


# ── User workflow ─────────────────────────────────────────────────────────────


def build_user_registry() -> Registry[User]:
    registry: Registry[User] = Registry("users")

    users = [
        User(id=1, username="alice", email="alice@example.com")
        .with_tag("admin")
        .with_meta("timezone", "UTC")
        .with_meta("theme", "dark"),
        User(id=2, username="bob", email="bob@example.com")
        .with_tag("viewer")
        .with_meta("timezone", "EST"),
        User(id=3, username="charlie", email="charlie@example.com")
        .with_tag("editor")
        .with_tag("beta")
        .with_meta("timezone", "PST"),
        User(id=4, username="diana", email="diana@example.com")
        .with_tag("viewer")
        .with_meta("timezone", "CET"),
        User(id=5, username="eve", email="eve@example.com")
        .with_tag("admin")
        .with_tag("auditor"),
    ]

    users[1].deactivate()
    users[0].suspend("pending security review")

    for user in users:
        try:
            registry.add(user.id, user)
        except ValidationError as exc:
            print(f"Skipping invalid user: {exc}")

    return registry


def display_users(registry: Registry[User]) -> None:
    try:
        registry.get(99)
    except NotFoundError:
        print("user 99 not found")

    print_section("Users")

    all_users = registry.all()
    active = registry.where(lambda u: u.is_active())
    admins = registry.where(lambda u: u.has_tag("admin"))

    print(f"Total: {len(all_users)}  Active: {len(active)}  Admins: {len(admins)}")
    print()

    rows = [
        {
            "id": u.id,
            "username": u.username,
            "email": mask_email(u.email),
            "status": u.status.name,
            "tags": ", ".join(u.tags),
        }
        for u in all_users
    ]
    print_table(rows)

    by_status = group_by(all_users, lambda u: u.status.name)
    print(f"\nBy status: { {k: len(v) for k, v in by_status.items()} }")


# ── Product workflow ──────────────────────────────────────────────────────────


def build_product_catalogue() -> dict[str, Product]:
    catalogue: dict[str, Product] = {}

    products = [
        Product(
            sku="KB-01",
            name="Mechanical Keyboard",
            price_cents=14999,
            category="peripherals",
        ),
        Product(sku="MN-02", name="4K Monitor", price_cents=59999, category="displays"),
        Product(
            sku="CB-03", name="USB-C Cable", price_cents=999, category="accessories"
        ),
        Product(
            sku="WB-04", name="Webcam HD", price_cents=7999, category="peripherals"
        ),
        Product(
            sku="HS-05",
            name="Noise-Cancel Headset",
            price_cents=24999,
            category="audio",
        ),
    ]

    stock_levels = {
        "KB-01": 50,
        "MN-02": 12,
        "CB-03": 200,
        "WB-04": 30,
        "HS-05": 25,
    }

    for product in products:
        product.restock(stock_levels.get(product.sku, 0))
        catalogue[product.sku] = product

    catalogue["KB-01"].sell(3)
    catalogue["MN-02"].sell(1)
    catalogue["HS-05"].sell(5)

    return catalogue


def process_products(catalogue: dict[str, Product]) -> None:
    print_section("Products")

    rows = [
        {
            "sku": p.sku,
            "name": truncate(p.name, 25),
            "price": format_currency(p.price_cents),
            "stock": p.stock,
            "in_stock": "yes" if p.in_stock else "NO",
        }
        for p in catalogue.values()
    ]
    print_table(rows)

    total_value = sum(p.price_cents * p.stock for p in catalogue.values())
    print(f"\nTotal inventory value: {format_currency(total_value)}")

    low_stock = [p for p in catalogue.values() if p.stock < 10]
    if low_stock:
        print(f"\nLow stock alert ({len(low_stock)} products):")
        for p in low_stock:
            print(f"  {p.sku} — {p.name}: {p.stock} remaining")


# ── Order workflow ────────────────────────────────────────────────────────────


def build_orders(catalogue: dict[str, Product]) -> list[Order]:
    order_a = Order(id=1001, user_id=1)
    order_a.add_line("KB-01", 1, catalogue["KB-01"].price_cents)
    order_a.add_line("CB-03", 2, catalogue["CB-03"].price_cents)
    order_a.confirm()

    order_b = Order(id=1002, user_id=3)
    order_b.add_line("MN-02", 2, catalogue["MN-02"].price_cents)
    order_b.add_line("KB-01", 1, catalogue["KB-01"].price_cents)
    order_b.add_line("HS-05", 1, catalogue["HS-05"].price_cents)
    order_b.confirm()

    order_c = Order(id=1003, user_id=2)
    order_c.add_line("CB-03", 10, catalogue["CB-03"].price_cents)
    order_c.cancel("user account deactivated")

    return [order_a, order_b, order_c]


def process_orders(orders: list[Order], catalogue: dict[str, Product]) -> None:
    print_section("Orders")

    for order in orders:
        print(order.describe())
        for line in order:
            product_name = catalogue.get(
                line.sku, Product(sku=line.sku, name="?", price_cents=0, category="?")
            ).name
            print(
                f"  {line.quantity} × {product_name} @ {format_currency(line.unit_price_cents)}"
            )
        if order.notes:
            print(f"  Note: {order.notes}")
        print()

    confirmed = [o for o in orders if o.status == Status.ACTIVE]
    revenue = sum(o.total_cents for o in confirmed)
    print(f"Confirmed orders: {len(confirmed)}  Revenue: {format_currency(revenue)}")


# ── Pipeline workflow ─────────────────────────────────────────────────────────


def build_import_pipeline() -> Pipeline:
    pipeline = Pipeline(name="user-import")
    pipeline.add_stage(NormaliseStage())
    pipeline.add_stage(LengthGuardStage(min_length=3, max_length=60))
    pipeline.add_stage(EnrichStage(prefix="[imported] "))
    pipeline.add_stage(TransformStage("slug", slugify))
    return pipeline


def process_pipeline() -> None:
    print_section("Pipeline")

    pipeline = build_import_pipeline()

    raw_inputs = [
        "  Alice Johnson  ",
        "Bob",
        "Charlie Davis",
        "",
        "Diana Prince",
        "  Eve   ",
        "Frank Castle",
        "   ",
        "Grace Hopper",
        "H",
    ]

    results = pipeline.run(raw_inputs)

    for result in results:
        if result.ok:
            print(f"  ✓  {result.input!r:30}  →  {result.output!r}")
        else:
            print(f"  ✗  {result.input!r:30}  →  {result.error}")

    print(f"\n{pipeline.report()}")


# ── Export ────────────────────────────────────────────────────────────────────


def export_summary(
    users: Registry[User],
    catalogue: dict[str, Product],
    orders: list[Order],
) -> str:
    data = {
        "users": {
            "total": len(users),
            "active": len(users.where(lambda u: u.is_active())),
        },
        "products": {
            "total": len(catalogue),
            "in_stock": sum(1 for p in catalogue.values() if p.in_stock),
            "inventory_value": format_currency(
                sum(p.price_cents * p.stock for p in catalogue.values())
            ),
        },
        "orders": {
            "total": len(orders),
            "confirmed": sum(1 for o in orders if o.status == Status.ACTIVE),
            "revenue": format_currency(
                sum(o.total_cents for o in orders if o.status == Status.ACTIVE)
            ),
        },
    }
    return to_json(data)


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> int:
    users = build_user_registry()
    catalogue = build_product_catalogue()
    orders = build_orders(catalogue)

    display_users(users)
    process_products(catalogue)
    process_orders(orders, catalogue)
    process_pipeline()

    print_section("Summary")
    print(export_summary(users, catalogue, orders))

    return 0


if __name__ == "__main__":
    sys.exit(main())
