"""Tests for the Preview agent."""

from __future__ import annotations

import json

from agent.preview import Preview, _generate_summary
from api.models import ExecutionPlan, PlanStep
from api.utils import mask_value


class TestGenerate:
    def test_produces_valid_json(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="create_bot", description="Create bot")],
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        assert "steps" in parsed
        assert "total_steps" in parsed
        assert parsed["total_steps"] == 1

    def test_masks_bot_tokens(self):
        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_bot",
                    description="Create bot",
                    params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
                )
            ],
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        token_value = parsed["steps"][0]["bot_token"]
        assert "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456" not in token_value
        assert "..." in token_value

    def test_masks_new_token(self):
        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="update_bot_token",
                    description="Update token",
                    params={"new_token": "999999999:NewTokenValue1234567890abcdefghij"},
                )
            ],
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        token_value = parsed["steps"][0]["new_token"]
        assert "999999999:NewTokenValue1234567890abcdefghij" not in token_value

    def test_includes_code_length_for_create_command(self):
        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_command",
                    description="Create cmd",
                    params={"command": "start", "code": "print('hello world')"},
                )
            ],
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        assert "code_length" in parsed["steps"][0]
        assert parsed["steps"][0]["code_length"] == 20

    def test_requires_confirmation_false_shows_note(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="create_bot", description="Create")],
            requires_confirmation=False,
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        assert "note" in parsed
        assert "warning" not in parsed

    def test_requires_confirmation_true_shows_warning(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="delete_bot", description="Delete", destructive=True)],
            requires_confirmation=True,
        )
        result = Preview.generate(plan)
        parsed = json.loads(result)
        assert "warning" in parsed
        assert "note" not in parsed


class TestGenerateDestructivePreview:
    def test_produces_warning(self):
        result = Preview.generate_destructive_preview(
            action="delete_bot",
            description="Delete a bot",
            params={"bot_id": "12345"},
        )
        parsed = json.loads(result)
        assert parsed["preview"] is True
        assert "warning" in parsed
        assert "destructive" in parsed["warning"].lower()

    def test_includes_bot_id(self):
        result = Preview.generate_destructive_preview(
            action="delete_bot",
            description="Delete a bot",
            params={"bot_id": "12345"},
        )
        parsed = json.loads(result)
        assert parsed["bot_id"] == "12345"

    def test_includes_command_name(self):
        result = Preview.generate_destructive_preview(
            action="delete_command",
            description="Delete a command",
            params={"bot_id": "12345", "command_name": "start"},
        )
        parsed = json.loads(result)
        assert parsed["command_name"] == "start"


class TestGenerateSummary:
    def test_deploy_bot_summary(self):
        plan = ExecutionPlan(
            steps=[
                PlanStep(action="create_bot", description="Create"),
                PlanStep(action="create_command", description="Cmd"),
                PlanStep(action="start_bot", description="Start"),
            ]
        )
        summary = _generate_summary(plan)
        assert "Deploy new bot" in summary
        assert "1 command" in summary

    def test_batch_delete_commands_summary(self):
        plan = ExecutionPlan(
            steps=[
                PlanStep(action="delete_command", description="Del 1"),
                PlanStep(action="delete_command", description="Del 2"),
            ]
        )
        summary = _generate_summary(plan)
        assert "Delete 2 commands" in summary

    def test_delete_bot_summary(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="delete_bot", description="Del")]
        )
        summary = _generate_summary(plan)
        assert "Delete bot" in summary

    def test_update_bot_token_summary(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="update_bot_token", description="Update")]
        )
        summary = _generate_summary(plan)
        assert "Update bot token" in summary

    def test_generic_summary(self):
        plan = ExecutionPlan(
            steps=[PlanStep(action="start_bot", description="Start")]
        )
        summary = _generate_summary(plan)
        assert "Execute 1 operation" in summary


class TestMaskToken:
    def test_short_token(self):
        assert mask_value("short") == "***"

    def test_long_token(self):
        result = mask_value("1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh")
        assert result.startswith("12345")
        assert result.endswith("efgh")
        assert "..." in result

    def test_exactly_10_chars(self):
        assert mask_value("1234567890") == "***"
