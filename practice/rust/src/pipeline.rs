// pipeline.rs
// Data processing pipeline for the LazyVim practice project.
// Used in lessons for operator/text-object exercises, LSP jumps, and diagnostics.

use crate::models::{Describable, Validatable};

// ── Stage ─────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub enum StageError {
    InvalidInput(String),
    TransformFailed { stage: String, reason: String },
    DownstreamUnavailable(String),
}

impl std::fmt::Display for StageError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            StageError::InvalidInput(msg) => write!(f, "invalid input: {}", msg),
            StageError::TransformFailed { stage, reason } => {
                write!(f, "stage '{}' failed: {}", stage, reason)
            }
            StageError::DownstreamUnavailable(name) => {
                write!(f, "downstream '{}' unavailable", name)
            }
        }
    }
}

pub trait Stage {
    fn name(&self) -> &str;
    fn process(&self, input: &str) -> Result<String, StageError>;
}

// ── Built-in stages ───────────────────────────────────────────────────────────

pub struct NormaliseStage;

impl Stage for NormaliseStage {
    fn name(&self) -> &str {
        "normalise"
    }

    fn process(&self, input: &str) -> Result<String, StageError> {
        let trimmed = input.trim();
        if trimmed.is_empty() {
            return Err(StageError::InvalidInput("empty string after trim".to_string()));
        }
        Ok(trimmed.to_lowercase())
    }
}

pub struct EnrichStage {
    pub prefix: String,
    pub suffix: String,
}

impl EnrichStage {
    pub fn new(prefix: &str, suffix: &str) -> Self {
        EnrichStage {
            prefix: prefix.to_string(),
            suffix: suffix.to_string(),
        }
    }
}

impl Stage for EnrichStage {
    fn name(&self) -> &str {
        "enrich"
    }

    fn process(&self, input: &str) -> Result<String, StageError> {
        Ok(format!("{}{}{}", self.prefix, input, self.suffix))
    }
}

pub struct ValidateStage {
    pub min_length: usize,
    pub max_length: usize,
}

impl Stage for ValidateStage {
    fn name(&self) -> &str {
        "validate"
    }

    fn process(&self, input: &str) -> Result<String, StageError> {
        let len = input.len();
        if len < self.min_length {
            return Err(StageError::TransformFailed {
                stage: "validate".to_string(),
                reason: format!("too short: {} < {}", len, self.min_length),
            });
        }
        if len > self.max_length {
            return Err(StageError::TransformFailed {
                stage: "validate".to_string(),
                reason: format!("too long: {} > {}", len, self.max_length),
            });
        }
        Ok(input.to_string())
    }
}

// ── Pipeline ──────────────────────────────────────────────────────────────────

pub struct Pipeline {
    pub name: String,
    stages: Vec<Box<dyn Stage>>,
    pub processed: usize,
    pub errors: Vec<String>,
}

impl Pipeline {
    pub fn new(name: &str) -> Self {
        Pipeline {
            name: name.to_string(),
            stages: Vec::new(),
            processed: 0,
            errors: Vec::new(),
        }
    }

    pub fn add_stage(mut self, stage: impl Stage + 'static) -> Self {
        self.stages.push(Box::new(stage));
        self
    }

    pub fn run(&mut self, inputs: &[&str]) -> Vec<String> {
        let mut results = Vec::new();

        for &input in inputs {
            match self.run_one(input) {
                Ok(output) => {
                    results.push(output);
                    self.processed += 1;
                }
                Err(e) => {
                    self.errors.push(format!("[{}] {}", input, e));
                }
            }
        }

        results
    }

    fn run_one(&self, input: &str) -> Result<String, StageError> {
        let mut current = input.to_string();
        for stage in &self.stages {
            current = stage.process(&current)?;
        }
        Ok(current)
    }

    pub fn reset(&mut self) {
        self.processed = 0;
        self.errors.clear();
    }

    pub fn success_rate(&self) -> f64 {
        let total = self.processed + self.errors.len();
        if total == 0 {
            return 0.0;
        }
        self.processed as f64 / total as f64 * 100.0
    }

    pub fn report(&self) -> String {
        format!(
            "Pipeline '{}': {} ok, {} errors ({:.1}% success)",
            self.name,
            self.processed,
            self.errors.len(),
            self.success_rate()
        )
    }
}

// ── Batch runner ──────────────────────────────────────────────────────────────

pub fn run_batch<T: Describable + Validatable>(
    items: &[T],
    pipeline: &mut Pipeline,
    extract: impl Fn(&T) -> &str,
) -> (usize, usize) {
    let valid_inputs: Vec<&str> = items
        .iter()
        .filter(|item| item.is_valid())
        .map(|item| extract(item))
        .collect();

    let results = pipeline.run(&valid_inputs);
    let ok = results.len();
    let errs = pipeline.errors.len();
    (ok, errs)
}
