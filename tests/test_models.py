"""Tests for data models (api/models.py)."""

from __future__ import annotations

from api.models import (
    ApiResponse,
    BatchResult,
    BotInfo,
    CommandDef,
    CommandInfo,
    ExecutionPlan,
    PlanStep,
    StepResult,
)
from api.utils import mask_value

# ---------------------------------------------------------------------------
# ApiResponse
# ---------------------------------------------------------------------------


class TestApiResponse:
    def test_creation(self):
        r = ApiResponse(ok=True, result="success")
        assert r.ok is True
        assert r.result == "success"
        assert r.status_code == 0

    def test_to_dict_basic(self):
        r = ApiResponse(ok=True, result="done", status_code=200)
        d = r.to_dict()
        assert d["ok"] is True
        assert d["result"] == "done"

    def test_to_dict_includes_rate_limit(self):
        r = ApiResponse(
            ok=True, result="ok", rate_limit_remaining=50, rate_limit_reset=100
        )
        d = r.to_dict()
        assert d["rate_limit_remaining"] == 50
        assert d["rate_limit_reset"] == 100

    def test_to_dict_omits_rate_limit_when_none(self):
        r = ApiResponse(ok=True, result="ok")
        d = r.to_dict()
        assert "rate_limit_remaining" not in d
        assert "rate_limit_reset" not in d


# ---------------------------------------------------------------------------
# BotInfo
# ---------------------------------------------------------------------------


class TestBotInfo:
    def test_creation(self):
        info = BotInfo(botid="123", bot_name="TestBot", bot_username="testbot")
        assert info.botid == "123"
        assert info.bot_name == "TestBot"

    def test_to_dict(self):
        info = BotInfo(botid="123", bot_name="TestBot", bot_username="testbot")
        d = info.to_dict()
        assert d == {"botid": "123", "bot_name": "TestBot", "bot_username": "testbot"}


# ---------------------------------------------------------------------------
# CommandInfo
# ---------------------------------------------------------------------------


class TestCommandInfo:
    def test_creation(self):
        ci = CommandInfo(command="start", code="print('hi')")
        assert ci.command == "start"
        assert ci.is_pinned is False

    def test_to_dict(self):
        ci = CommandInfo(command="start", code="code", is_pinned=True)
        d = ci.to_dict()
        assert d == {"command": "start", "code": "code", "is_pinned": True}


# ---------------------------------------------------------------------------
# CommandDef
# ---------------------------------------------------------------------------


class TestCommandDef:
    def test_creation(self):
        cd = CommandDef(name="start", code="bot.reply('Hi')")
        assert cd.name == "start"
        assert cd.code == "bot.reply('Hi')"

    def test_to_dict(self):
        cd = CommandDef(name="start", code="bot.reply('Hi')")
        d = cd.to_dict()
        assert d == {"name": "start", "code": "bot.reply('Hi')"}


# ---------------------------------------------------------------------------
# PlanStep
# ---------------------------------------------------------------------------


class TestPlanStep:
    def test_creation(self):
        step = PlanStep(action="create_bot", description="Create a bot")
        assert step.action == "create_bot"
        assert step.destructive is False
        assert step.params == {}

    def test_to_dict_masks_bot_token(self):
        step = PlanStep(
            action="create_bot",
            description="Create bot",
            params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
        )
        d = step.to_dict()
        # bot_token should be masked, not plaintext
        assert d["params"]["bot_token"] != "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"
        assert "..." in d["params"]["bot_token"]

    def test_to_dict_masks_new_token(self):
        step = PlanStep(
            action="update_bot_token",
            description="Update token",
            params={"new_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
        )
        d = step.to_dict()
        assert d["params"]["new_token"] != "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"
        assert "..." in d["params"]["new_token"]

    def test_to_dict_preserves_non_sensitive_params(self):
        step = PlanStep(
            action="create_command",
            description="Create cmd",
            params={"command": "start", "code": "print('hi')"},
        )
        d = step.to_dict()
        assert d["params"]["command"] == "start"
        assert d["params"]["code"] == "print('hi')"


# ---------------------------------------------------------------------------
# ExecutionPlan
# ---------------------------------------------------------------------------


class TestExecutionPlan:
    def test_creation(self):
        plan = ExecutionPlan()
        assert plan.steps == []
        assert plan.requires_confirmation is False

    def test_to_dict(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="create_bot", description="Create")],
            requires_confirmation=False,
        )
        d = plan.to_dict()
        assert d["total_steps"] == 1
        assert d["requires_confirmation"] is False
        assert len(d["steps"]) == 1


# ---------------------------------------------------------------------------
# StepResult
# ---------------------------------------------------------------------------


class TestStepResult:
    def test_creation(self):
        sr = StepResult(action="create_bot", success=True, message="Bot created")
        assert sr.data is None

    def test_to_dict_without_data(self):
        sr = StepResult(action="create_bot", success=True, message="Bot created")
        d = sr.to_dict()
        assert "data" not in d

    def test_to_dict_with_data(self):
        sr = StepResult(action="create_bot", success=True, message="OK", data="12345")
        d = sr.to_dict()
        assert d["data"] == "12345"


# ---------------------------------------------------------------------------
# BatchResult
# ---------------------------------------------------------------------------


class TestBatchResult:
    def test_creation(self):
        br = BatchResult(total=3, succeeded=2, failed=1)
        assert br.results == []

    def test_to_dict(self):
        br = BatchResult(
            total=2,
            succeeded=1,
            failed=1,
            results=[
                StepResult(action="create_bot", success=True, message="OK"),
                StepResult(action="start_bot", success=False, message="Fail"),
            ],
        )
        d = br.to_dict()
        assert d["total"] == 2
        assert d["succeeded"] == 1
        assert d["failed"] == 1
        assert len(d["results"]) == 2


# ---------------------------------------------------------------------------
# _mask_value helper
# ---------------------------------------------------------------------------


class TestMaskValue:
    def test_short_value_returns_stars(self):
        assert mask_value("short") == "***"

    def test_exactly_10_chars_returns_stars(self):
        assert mask_value("1234567890") == "***"

    def test_long_value_masks_middle(self):
        result = mask_value("abcdefghijklmnop")
        assert result == "abcde...lmnop"

    def test_non_string_returns_stars(self):
        assert mask_value(12345) == "***"
