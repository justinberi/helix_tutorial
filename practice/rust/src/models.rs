// models.rs
// Domain types for the LazyVim practice project.
// Used in lessons for cross-file LSP navigation, text objects, and diagnostics.

use std::collections::HashMap;
use std::fmt;

// ── Traits ───────────────────────────────────────────────────────────────────

pub trait Describable {
    fn describe(&self) -> String;
    fn short_name(&self) -> &str;
}

pub trait Validatable {
    fn validate(&self) -> Result<(), ValidationError>;
    fn is_valid(&self) -> bool {
        self.validate().is_ok()
    }
}

pub trait Serializable {
    fn to_csv_row(&self) -> String;
    fn field_names() -> Vec<&'static str>;
}

// ── Errors ───────────────────────────────────────────────────────────────────

#[derive(Debug)]
pub enum ValidationError {
    EmptyField(String),
    InvalidFormat { field: String, reason: String },
    OutOfRange { field: String, min: f64, max: f64, got: f64 },
}

impl fmt::Display for ValidationError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ValidationError::EmptyField(field) => {
                write!(f, "field '{}' must not be empty", field)
            }
            ValidationError::InvalidFormat { field, reason } => {
                write!(f, "field '{}' has invalid format: {}", field, reason)
            }
            ValidationError::OutOfRange { field, min, max, got } => {
                write!(
                    f,
                    "field '{}' out of range [{}, {}], got {}",
                    field, min, max, got
                )
            }
        }
    }
}

// ── Status ───────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq)]
pub enum Status {
    Active,
    Inactive,
    Pending,
    Suspended(String),
}

impl fmt::Display for Status {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Status::Active => write!(f, "active"),
            Status::Inactive => write!(f, "inactive"),
            Status::Pending => write!(f, "pending"),
            Status::Suspended(reason) => write!(f, "suspended: {}", reason),
        }
    }
}

// ── User ─────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct User {
    pub id: u64,
    pub username: String,
    pub email: String,
    pub status: Status,
    pub tags: Vec<String>,
    pub metadata: HashMap<String, String>,
}

impl User {
    pub fn new(id: u64, username: &str, email: &str) -> Self {
        User {
            id,
            username: username.to_string(),
            email: email.to_string(),
            status: Status::Active,
            tags: Vec::new(),
            metadata: HashMap::new(),
        }
    }

    pub fn with_tag(mut self, tag: &str) -> Self {
        self.tags.push(tag.to_string());
        self
    }

    pub fn with_meta(mut self, key: &str, value: &str) -> Self {
        self.metadata.insert(key.to_string(), value.to_string());
        self
    }

    pub fn suspend(&mut self, reason: &str) {
        self.status = Status::Suspended(reason.to_string());
    }

    pub fn deactivate(&mut self) {
        self.status = Status::Inactive;
    }

    pub fn is_active(&self) -> bool {
        self.status == Status::Active
    }

    pub fn has_tag(&self, tag: &str) -> bool {
        self.tags.iter().any(|t| t == tag)
    }
}

impl Describable for User {
    fn describe(&self) -> String {
        format!(
            "User #{} — {} <{}> [{}]",
            self.id, self.username, self.email, self.status
        )
    }

    fn short_name(&self) -> &str {
        &self.username
    }
}

impl Validatable for User {
    fn validate(&self) -> Result<(), ValidationError> {
        if self.username.is_empty() {
            return Err(ValidationError::EmptyField("username".to_string()));
        }
        if !self.email.contains('@') || !self.email.contains('.') {
            return Err(ValidationError::InvalidFormat {
                field: "email".to_string(),
                reason: "must contain '@' and '.'".to_string(),
            });
        }
        Ok(())
    }
}

impl Serializable for User {
    fn to_csv_row(&self) -> String {
        format!(
            "{},{},{},{}",
            self.id, self.username, self.email, self.status
        )
    }

    fn field_names() -> Vec<&'static str> {
        vec!["id", "username", "email", "status"]
    }
}

// ── Product ──────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct Product {
    pub sku: String,
    pub name: String,
    pub price_cents: u64,
    pub stock: u32,
    pub category: String,
}

impl Product {
    pub fn new(sku: &str, name: &str, price_cents: u64, category: &str) -> Self {
        Product {
            sku: sku.to_string(),
            name: name.to_string(),
            price_cents,
            stock: 0,
            category: category.to_string(),
        }
    }

    pub fn price(&self) -> f64 {
        self.price_cents as f64 / 100.0
    }

    pub fn restock(&mut self, units: u32) {
        self.stock += units;
    }

    pub fn sell(&mut self, units: u32) -> Result<(), String> {
        if units > self.stock {
            return Err(format!(
                "insufficient stock: need {}, have {}",
                units, self.stock
            ));
        }
        self.stock -= units;
        Ok(())
    }

    pub fn in_stock(&self) -> bool {
        self.stock > 0
    }
}

impl Describable for Product {
    fn describe(&self) -> String {
        format!(
            "Product {} — {} @ ${:.2} ({} in stock)",
            self.sku,
            self.name,
            self.price(),
            self.stock
        )
    }

    fn short_name(&self) -> &str {
        &self.name
    }
}

impl Validatable for Product {
    fn validate(&self) -> Result<(), ValidationError> {
        if self.sku.is_empty() {
            return Err(ValidationError::EmptyField("sku".to_string()));
        }
        if self.name.is_empty() {
            return Err(ValidationError::EmptyField("name".to_string()));
        }
        if self.price_cents == 0 {
            return Err(ValidationError::OutOfRange {
                field: "price_cents".to_string(),
                min: 1.0,
                max: f64::MAX,
                got: 0.0,
            });
        }
        Ok(())
    }
}

// ── Order ────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct OrderLine {
    pub sku: String,
    pub quantity: u32,
    pub unit_price_cents: u64,
}

impl OrderLine {
    pub fn subtotal_cents(&self) -> u64 {
        self.quantity as u64 * self.unit_price_cents
    }
}

#[derive(Debug, Clone)]
pub struct Order {
    pub id: u64,
    pub user_id: u64,
    pub lines: Vec<OrderLine>,
    pub status: Status,
    pub notes: Option<String>,
}

impl Order {
    pub fn new(id: u64, user_id: u64) -> Self {
        Order {
            id,
            user_id,
            lines: Vec::new(),
            status: Status::Pending,
            notes: None,
        }
    }

    pub fn add_line(&mut self, sku: &str, quantity: u32, unit_price_cents: u64) {
        self.lines.push(OrderLine {
            sku: sku.to_string(),
            quantity,
            unit_price_cents,
        });
    }

    pub fn total_cents(&self) -> u64 {
        self.lines.iter().map(|l| l.subtotal_cents()).sum()
    }

    pub fn total(&self) -> f64 {
        self.total_cents() as f64 / 100.0
    }

    pub fn item_count(&self) -> u32 {
        self.lines.iter().map(|l| l.quantity).sum()
    }

    pub fn confirm(&mut self) {
        self.status = Status::Active;
    }

    pub fn cancel(&mut self, reason: &str) {
        self.status = Status::Suspended(reason.to_string());
    }

    pub fn with_note(mut self, note: &str) -> Self {
        self.notes = Some(note.to_string());
        self
    }
}

impl Describable for Order {
    fn describe(&self) -> String {
        format!(
            "Order #{} for user #{} — {} items, total ${:.2} [{}]",
            self.id,
            self.user_id,
            self.item_count(),
            self.total(),
            self.status
        )
    }

    fn short_name(&self) -> &str {
        "order"
    }
}
