// main.rs
// Entry point for the LazyVim practice project.
//
// This file exercises:
//   - LSP navigation: gd (go to definition), gr (references), gI (implementation)
//   - Text objects: ci", di(, ya{, daf, cia, etc.
//   - Diagnostics: intentional TODO markers and clippy hints
//   - Cross-file jumps: types and traits are defined in models.rs / pipeline.rs
//
// Run with: cargo run
// Check with: cargo clippy

mod models;
mod pipeline;

use models::{Describable, Order, Product, User, Validatable};
use pipeline::{EnrichStage, NormaliseStage, Pipeline, ValidateStage};
use std::collections::HashMap;

// ── Helpers ───────────────────────────────────────────────────────────────────

fn format_currency(cents: u64) -> String {
    format!("${:.2}", cents as f64 / 100.0)
}

fn print_header(title: &str) {
    let bar = "─".repeat(title.len() + 4);
    println!("┌{}┐", bar);
    println!("│  {}  │", title);
    println!("└{}┘", bar);
}

fn active_users(users: &[User]) -> Vec<&User> {
    users.iter().filter(|u| u.is_active()).collect()
}

fn find_user<'a>(users: &'a [User], username: &str) -> Option<&'a User> {
    users.iter().find(|u| u.username == username)
}

fn describe_all(items: &[impl Describable]) -> Vec<String> {
    items.iter().map(|item| item.describe()).collect()
}

fn validate_all<T: Validatable>(items: &[T]) -> Vec<String> {
    items
        .iter()
        .filter_map(|item| item.validate().err())
        .map(|e| e.to_string())
        .collect()
}

fn summarise_order(order: &Order, products: &HashMap<String, Product>) -> String {
    let lines: Vec<String> = order
        .lines
        .iter()
        .map(|line| {
            let name = products
                .get(&line.sku)
                .map(|p| p.name.as_str())
                .unwrap_or("unknown");
            format!(
                "  {} × {} @ {}",
                line.quantity,
                name,
                format_currency(line.unit_price_cents)
            )
        })
        .collect();

    format!(
        "{}\n{}\n  Total: {}",
        order.describe(),
        lines.join("\n"),
        format_currency(order.total_cents())
    )
}

// ── Main ──────────────────────────────────────────────────────────────────────

fn main() {
    // ── Users ──────────────────────────────────────────────────────────────

    print_header("Users");
    let mut alice = User::new(1, "alice", "alice@example.com")
        .with_tag("admin")
        .with_meta("timezone", "UTC");

    let mut bob = User::new(2, "bob", "bob@example.com")
        .with_tag("viewer")
        .with_meta("timezone", "EST");

    let charlie = User::new(3, "charlie", "charlie@example.com")
        .with_tag("editor")
        .with_meta("timezone", "PST");

    bob.deactivate();
    alice.suspend("pending review");

    let users = vec![alice, bob, charlie];

    for line in describe_all(&users) {
        println!("{}", line);
    }

    let active = active_users(&users);
    println!("\nActive users: {}", active.len());

    if let Some(user) = find_user(&users, "charlie") {
        println!("Found: {}", user.describe());
    }

    let errors = validate_all(&users);
    if errors.is_empty() {
        println!("All users valid.");
    } else {
        for e in &errors {
            println!("Validation error: {}", e);
        }
    }

    // ── Products ───────────────────────────────────────────────────────────

    print_header("Products");

    let mut catalogue: HashMap<String, Product> = HashMap::new();

    let mut keyboard = Product::new("KB-01", "Mechanical Keyboard", 14999, "peripherals");
    keyboard.restock(50);

    let mut monitor = Product::new("MN-02", "4K Monitor", 59999, "displays");
    monitor.restock(12);

    let mut cable = Product::new("CB-03", "USB-C Cable", 999, "accessories");
    cable.restock(200);

    keyboard.sell(3).expect("sell keyboard");
    monitor.sell(1).expect("sell monitor");

    for product in [&keyboard, &monitor, &cable] {
        println!("{}", product.describe());
        catalogue.insert(product.sku.clone(), product.clone());
    }

    // ── Orders ────────────────────────────────────────────────────────────

    print_header("Orders");

    let mut order_a = Order::new(1001, 1).with_note("gift — please wrap");
    order_a.add_line("KB-01", 1, 14999);
    order_a.add_line("CB-03", 2, 999);
    order_a.confirm();

    let mut order_b = Order::new(1002, 3);
    order_b.add_line("MN-02", 2, 59999);
    order_b.add_line("KB-01", 1, 14999);
    order_b.add_line("CB-03", 5, 999);
    order_b.confirm();

    let mut order_c = Order::new(1003, 2);
    order_c.add_line("CB-03", 10, 999);
    order_c.cancel("user account inactive");

    let orders = vec![order_a, order_b, order_c];
    for order in &orders {
        println!("{}", summarise_order(order, &catalogue));
        println!();
    }

    // ── Pipeline ──────────────────────────────────────────────────────────

    print_header("Pipeline");

    let mut pipeline = Pipeline::new("user-import")
        .add_stage(NormaliseStage)
        .add_stage(EnrichStage::new("[imported] ", ""))
        .add_stage(ValidateStage {
            min_length: 5,
            max_length: 80,
        });

    let inputs = [
        "  Alice Johnson  ",
        "Bob",
        "Charlie Davis",
        "",
        "Diana Prince",
        "Eve",
        "  Frank Castle  ",
    ];

    let results = pipeline.run(&inputs);

    for result in &results {
        println!("{}", result);
    }

    println!("\n{}", pipeline.report());

    if !pipeline.errors.is_empty() {
        println!("\nErrors:");
        for e in &pipeline.errors {
            println!("  {}", e);
        }
    }

    // ── Lesson 4.3 macro practice ─────────────────────────────────────────────
    // These five bindings are intentionally declared without `mut`.
    // In Lesson 4.3 you will record a macro that inserts `mut` after `let`
    // on one line, then replay it across all five.
    let item_a = "alpha";
    let item_b = "beta";
    let item_c = "gamma";
    let item_d = "delta";
    let item_e = "epsilon";
    println!("{item_a} {item_b} {item_c} {item_d} {item_e}");
}
