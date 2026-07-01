"""Tests for the Validator agent."""

from __future__ import annotations

from agent.validator import Validator
from api.models import ExecutionPlan, PlanStep


class TestValidateCredentials:
    def test_with_api_key(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("tbs_validkey123")
        ok, _msg = Validator.validate_credentials()
        assert ok is True

    def test_without_api_key(self, fresh_credential_manager):
        ok, msg = Validator.validate_credentials()
        assert ok is False
        assert "API key not set" in msg


class TestValidateBotIdForStep:
    def test_create_bot_needs_no_bot_id(self, fresh_credential_manager):
        ok, _msg = Validator.validate_bot_id_for_step("create_bot", {})
        assert ok is True

    def test_other_action_needs_bot_id_in_params(self, fresh_credential_manager):
        ok, _msg = Validator.validate_bot_id_for_step("delete_bot", {"bot_id": "12345"})
        assert ok is True

    def test_other_action_needs_bot_id_in_session(self, fresh_credential_manager):
        fresh_credential_manager.set_bot_id("12345")
        ok, _msg = Validator.validate_bot_id_for_step("start_bot", {})
        assert ok is True

    def test_other_action_fails_without_bot_id(self, fresh_credential_manager):
        ok, msg = Validator.validate_bot_id_for_step("start_bot", {})
        assert ok is False
        assert "Bot ID not set" in msg

    def test_invalid_bot_id_format(self, fresh_credential_manager):
        ok, _msg = Validator.validate_bot_id_for_step("start_bot", {"bot_id": "abc"})
        assert ok is False


class TestValidatePlan:
    def test_valid_plan_with_credentials(self, fresh_credential_manager):
        """A valid plan with credentials set should pass validation."""
        fresh_credential_manager.set_api_key("tbs_validkey123")
        fresh_credential_manager.set_bot_id("12345")

        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_command",
                    description="Create cmd",
                    params={"command": "start", "code": "print('hi')"},
                )
            ]
        )
        ok, errors = Validator.validate_plan(plan)
        assert ok is True
        assert errors == []

    def test_missing_credentials(self, fresh_credential_manager):
        """Plan validation should fail without credentials."""
        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_command",
                    description="Create cmd",
                    params={"command": "start", "code": "print('hi')"},
                )
            ]
        )
        ok, errors = Validator.validate_plan(plan)
        assert ok is False
        assert any("API key not set" in e for e in errors)

    def test_create_bot_dependency_resolution(self, fresh_credential_manager):
        """When create_bot is present, subsequent steps don't need bot_id."""
        fresh_credential_manager.set_api_key("tbs_validkey123")

        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_bot",
                    description="Create bot",
                    params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
                ),
                PlanStep(
                    action="create_command",
                    description="Create cmd",
                    params={"command": "start", "code": "print('hi')"},
                ),
                PlanStep(
                    action="start_bot",
                    description="Start",
                    params={},
                ),
            ]
        )
        ok, errors = Validator.validate_plan(plan)
        assert ok is True, f"Errors: {errors}"

    def test_invalid_command_name_in_plan(self, fresh_credential_manager):
        """Steps with invalid params should produce validation errors."""
        fresh_credential_manager.set_api_key("tbs_validkey123")
        fresh_credential_manager.set_bot_id("12345")

        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_command",
                    description="Bad cmd",
                    params={"command": "", "code": "print('hi')"},
                )
            ]
        )
        ok, errors = Validator.validate_plan(plan)
        assert ok is False
        assert len(errors) > 0

    def test_invalid_bot_token_in_create_bot(self, fresh_credential_manager):
        """create_bot with invalid token should produce validation error."""
        fresh_credential_manager.set_api_key("tbs_validkey123")

        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_bot",
                    description="Create",
                    params={"bot_token": "bad_token"},
                )
            ]
        )
        ok, _errors = Validator.validate_plan(plan)
        assert ok is False
