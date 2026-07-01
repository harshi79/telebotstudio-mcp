"""
Typed request/response models for the TeleBot Studio REST API v2.

All dataclasses are plain Python objects — no external serialization
framework required.  They serve as documentation, validation targets,
and structured return types for the API wrapper layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------


@dataclass
class ApiResponse:
    """Wraps every API call result with metadata."""

    ok: bool
    result: Any  # str or dict, depending on endpoint
    status_code: int = 0
    rate_limit_remaining: int | None = None
    rate_limit_reset: int | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"ok": self.ok, "result": self.result}
        if self.rate_limit_remaining is not None:
            d["rate_limit_remaining"] = self.rate_limit_remaining
        if self.rate_limit_reset is not None:
            d["rate_limit_reset"] = self.rate_limit_reset
        return d


@dataclass
class BotInfo:
    """Bot metadata returned by create-bot."""

    botid: str
    bot_name: str
    bot_username: str

    def to_dict(self) -> dict[str, str]:
        return {
            "botid": self.botid,
            "bot_name": self.bot_name,
            "bot_username": self.bot_username,
        }


@dataclass
class CommandInfo:
    """Command metadata returned by get/list commands."""

    command: str
    code: str
    is_pinned: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "code": self.code,
            "is_pinned": self.is_pinned,
        }


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------


@dataclass
class CreateBotRequest:
    bot_token: str


@dataclass
class UpdateBotTokenRequest:
    token: str


@dataclass
class CreateCommandRequest:
    command: str
    code: str


@dataclass
class UpdateCommandRequest:
    command_name: str
    code: str


@dataclass
class DeleteCommandRequest:
    command_name: str


# ---------------------------------------------------------------------------
# Agent / Batch Models
# ---------------------------------------------------------------------------


@dataclass
class CommandDef:
    """A command name + code pair, used in batch and agent operations."""

    name: str
    code: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "code": self.code}


@dataclass
class PlanStep:
    """A single step in an execution plan."""

    action: str  # e.g. "create_bot", "create_command", "start_bot"
    description: str  # Human-readable description
    params: dict[str, Any] = field(default_factory=dict)
    destructive: bool = False

    def to_dict(self) -> dict[str, Any]:
        # Build a safe copy of params — mask sensitive values
        safe_params = dict(self.params)
        if "bot_token" in safe_params:
            safe_params["bot_token"] = _mask_value(safe_params["bot_token"])
        if "new_token" in safe_params:
            safe_params["new_token"] = _mask_value(safe_params["new_token"])
        return {
            "action": self.action,
            "description": self.description,
            "params": safe_params,
            "destructive": self.destructive,
        }


@dataclass
class ExecutionPlan:
    """An ordered list of steps to execute."""

    steps: list[PlanStep] = field(default_factory=list)
    requires_confirmation: bool = False  # True if any step is destructive

    def to_dict(self) -> dict[str, Any]:
        return {
            "steps": [s.to_dict() for s in self.steps],
            "requires_confirmation": self.requires_confirmation,
            "total_steps": len(self.steps),
        }


@dataclass
class StepResult:
    """Outcome of executing a single plan step."""

    action: str
    success: bool
    message: str
    data: Any = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "action": self.action,
            "success": self.success,
            "message": self.message,
        }
        if self.data is not None:
            d["data"] = self.data
        return d


@dataclass
class BatchResult:
    """Outcome of a batch or agent execution."""

    total: int
    succeeded: int
    failed: int
    results: list[StepResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "results": [r.to_dict() for r in self.results],
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mask_value(value: str) -> str:
    """Mask a sensitive value for safe display."""
    if not isinstance(value, str) or len(value) <= 10:
        return "***"
    return f"{value[:5]}...{value[-5:]}"
