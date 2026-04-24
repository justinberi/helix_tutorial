"""
pipeline.py
Data processing pipeline for the LazyVim practice project.

Used in lessons for:
  - Text objects on function arguments and decorator strings
  - LSP: follow Stage.process() to each implementation with gI
  - mini.surround: wrap/unwrap strings in stage configs
  - Diagnostics: missing return types surface in pyright
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, TypeVar

from models import Describable, Validatable, ValidationError
from utils import retry, logged

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ── Stage protocol ────────────────────────────────────────────────────────────


class StageError(Exception):
    """Raised when a pipeline stage cannot process its input."""

    def __init__(self, stage_name: str, reason: str) -> None:
        self.stage_name = stage_name
        self.reason = reason
        super().__init__(f"[{stage_name}] {reason}")


class Stage(ABC):
    """A single processing step in a Pipeline."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def process(self, value: str) -> str:
        """Transform value or raise StageError."""
        ...


# ── Built-in stages ───────────────────────────────────────────────────────────


class NormaliseStage(Stage):
    """Strip whitespace and lower-case the input."""

    @property
    def name(self) -> str:
        return "normalise"

    def process(self, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise StageError(self.name, "empty string after strip")
        return stripped.lower()


class EnrichStage(Stage):
    """Prepend a prefix and append a suffix to the input."""

    def __init__(self, prefix: str = "", suffix: str = "") -> None:
        self.prefix = prefix
        self.suffix = suffix

    @property
    def name(self) -> str:
        return "enrich"

    def process(self, value: str) -> str:
        return f"{self.prefix}{value}{self.suffix}"


class LengthGuardStage(Stage):
    """Reject inputs that are too short or too long."""

    def __init__(self, min_length: int = 1, max_length: int = 255) -> None:
        self.min_length = min_length
        self.max_length = max_length

    @property
    def name(self) -> str:
        return "length-guard"

    def process(self, value: str) -> str:
        length = len(value)
        if length < self.min_length:
            raise StageError(
                self.name,
                f"too short: {length} < {self.min_length}",
            )
        if length > self.max_length:
            raise StageError(
                self.name,
                f"too long: {length} > {self.max_length}",
            )
        return value


class TransformStage(Stage):
    """Apply an arbitrary callable to the input."""

    def __init__(self, name: str, fn: Callable[[str], str]) -> None:
        self._name = name
        self._fn = fn

    @property
    def name(self) -> str:
        return self._name

    def process(self, value: str) -> str:
        try:
            return self._fn(value)
        except Exception as exc:
            raise StageError(self.name, str(exc)) from exc


# ── Pipeline ──────────────────────────────────────────────────────────────────


@dataclass
class PipelineResult:
    input: str
    output: Optional[str]
    error: Optional[str]
    stages_run: int

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass
class Pipeline:
    """
    Run a sequence of Stage objects over a list of string inputs.

    Build a pipeline with add_stage(), then call run() to process inputs.
    Each stage receives the output of the previous stage.
    """

    name: str
    stages: list[Stage] = field(default_factory=list)
    _results: list[PipelineResult] = field(default_factory=list, repr=False)

    def add_stage(self, stage: Stage) -> "Pipeline":
        """Append a stage and return self for chaining."""
        self.stages.append(stage)
        return self

    def run(self, inputs: list[str]) -> list[PipelineResult]:
        """Process all inputs and return results (success or failure per item)."""
        self._results = []
        for raw in inputs:
            result = self._run_one(raw)
            self._results.append(result)
            if result.ok:
                logger.debug("ok: %r → %r", raw, result.output)
            else:
                logger.warning("error: %r — %s", raw, result.error)
        return self._results

    def _run_one(self, raw: str) -> PipelineResult:
        current = raw
        for i, stage in enumerate(self.stages):
            try:
                current = stage.process(current)
            except StageError as exc:
                return PipelineResult(
                    input=raw,
                    output=None,
                    error=str(exc),
                    stages_run=i,
                )
        return PipelineResult(
            input=raw,
            output=current,
            error=None,
            stages_run=len(self.stages),
        )

    # ── Reporting ──────────────────────────────────────────────────────────

    @property
    def successes(self) -> list[PipelineResult]:
        return [r for r in self._results if r.ok]

    @property
    def failures(self) -> list[PipelineResult]:
        return [r for r in self._results if not r.ok]

    @property
    def success_rate(self) -> float:
        total = len(self._results)
        if total == 0:
            return 0.0
        return len(self.successes) / total * 100.0

    def report(self) -> str:
        return (
            f"Pipeline '{self.name}': "
            f"{len(self.successes)} ok, "
            f"{len(self.failures)} errors "
            f"({self.success_rate:.1f}% success)"
        )

    def reset(self) -> None:
        self._results = []


# ── Remote pipeline runner (decorator practice target) ───────────────────────


@logged
@retry(times=3, exceptions=(StageError, RuntimeError))
def run_remote_pipeline(pipeline: "Pipeline", inputs: list[str]) -> list[PipelineResult]:
    """
    Run a pipeline as if calling a remote service.
    Decorated with @retry and @logged for text-object practice.
    """
    return pipeline.run(inputs)


# ── Model pipeline adapter ────────────────────────────────────────────────────


def pipeline_from_models(
    items: list[Describable],
    pipeline: Pipeline,
    extract: Callable[[Describable], str],
) -> tuple[list[str], list[str]]:
    """
    Run a pipeline over a list of models.

    Args:
        items:    Models to process. Only valid items are passed to the pipeline.
        pipeline: The pipeline to run.
        extract:  Function that extracts the string value to process from each model.

    Returns:
        A tuple of (successful outputs, error messages).
    """
    inputs = []
    for item in items:
        if isinstance(item, Validatable) and item.is_valid():
            inputs.append(extract(item))

    results = pipeline.run(inputs)
    outputs = [r.output for r in results if r.ok and r.output is not None]
    errors = [r.error for r in results if not r.ok and r.error is not None]
    return outputs, errors
