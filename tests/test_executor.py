"""Tests for the Executor agent."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agent.executor import Executor
from api.errors import AuthenticationError
from api.models import BotInfo, ExecutionPlan, PlanStep


class TestExecutePlanNoApiKey:
    def test_returns_all_failures_without_api_key(self, fresh_credential_manager):
        """If no API key is set, all steps should fail."""
        plan = ExecutionPlan(
            steps=[
                PlanStep(action="create_bot", description="Create"),
                PlanStep(action="start_bot", description="Start"),
            ]
        )
        result = Executor.execute_plan(plan, api_key=None)
        assert result.total == 2
        assert result.succeeded == 0
        assert result.failed == 2
        for sr in result.results:
            assert "API key not set" in sr.message


class TestExecuteStep:
    """Test _execute_step with mocked managers."""

    @pytest.fixture
    def mock_managers(self):
        bot_mgr = MagicMock()
        cmd_mgr = MagicMock()
        control_mgr = MagicMock()
        return bot_mgr, cmd_mgr, control_mgr

    def test_create_bot_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        bot_mgr.create.return_value = BotInfo(
            botid="99999", bot_name="TestBot", bot_username="testbot"
        )
        step = PlanStep(
            action="create_bot",
            description="Create bot",
            params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True
        assert result.data == "99999"
        assert "TestBot" in result.message

    def test_delete_bot_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        bot_mgr.delete.return_value = "Bot deleted"
        step = PlanStep(
            action="delete_bot",
            description="Delete",
            params={"bot_id": "12345"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True
        assert "Bot deleted" in result.message

    def test_create_command_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        cmd_mgr.create.return_value = "Command created"
        step = PlanStep(
            action="create_command",
            description="Create cmd",
            params={"bot_id": "12345", "command": "start", "code": "print('hi')"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_update_command_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        cmd_mgr.update.return_value = "Command updated"
        step = PlanStep(
            action="update_command",
            description="Update cmd",
            params={"bot_id": "12345", "command_name": "start", "code": "new code"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_delete_command_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        cmd_mgr.delete.return_value = "Command deleted"
        step = PlanStep(
            action="delete_command",
            description="Delete cmd",
            params={"bot_id": "12345", "command_name": "start"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_start_bot_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        control_mgr.start.return_value = "Bot started"
        step = PlanStep(
            action="start_bot",
            description="Start",
            params={"bot_id": "12345"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_stop_bot_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        control_mgr.stop.return_value = "Bot stopped"
        step = PlanStep(
            action="stop_bot",
            description="Stop",
            params={"bot_id": "12345"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_restart_bot_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        control_mgr.restart.return_value = "Bot restarted"
        step = PlanStep(
            action="restart_bot",
            description="Restart",
            params={"bot_id": "12345"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True

    def test_update_bot_token_success(self, mock_managers):
        bot_mgr, cmd_mgr, control_mgr = mock_managers
        bot_mgr.update_token.return_value = "Token updated"
        step = PlanStep(
            action="update_bot_token",
            description="Update token",
            params={"bot_id": "12345", "new_token": "999:newtoken1234567890abc"},
        )
        result = Executor._execute_step(step, bot_mgr, cmd_mgr, control_mgr, bot_id=None)
        assert result.success is True


class TestExecuteStepErrors:
    def test_unknown_action_returns_failure(self):
        """An unknown action should return a failure StepResult."""
        step = PlanStep(action="fly_to_moon", description="Impossible", params={})
        result = Executor._execute_step(step, MagicMock(), MagicMock(), MagicMock(), bot_id=None)
        assert result.success is False
        assert "Unknown action" in result.message

    def test_telebot_studio_error_captured(self):
        """TeleBotStudioError should be captured as a step failure."""
        bot_mgr = MagicMock()
        bot_mgr.create.side_effect = AuthenticationError("Bad key", status_code=401)

        step = PlanStep(
            action="create_bot",
            description="Create",
            params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
        )
        result = Executor._execute_step(step, bot_mgr, MagicMock(), MagicMock(), bot_id=None)
        assert result.success is False
        assert "authentication_error" in result.message

    def test_bot_id_falls_back_to_parameter(self):
        """If bot_id param is missing, it falls back to the passed bot_id."""
        control_mgr = MagicMock()
        control_mgr.start.return_value = "Started"

        step = PlanStep(
            action="start_bot",
            description="Start",
            params={},  # No bot_id in params
        )
        result = Executor._execute_step(
            step, MagicMock(), MagicMock(), control_mgr, bot_id="fallback_id"
        )
        control_mgr.start.assert_called_once_with("fallback_id")
        assert result.success is True


class TestCreateBotResultPropagation:
    def test_create_bot_propagates_bot_id(self, fresh_credential_manager):
        """After create_bot, the bot_id should be stored in session for subsequent steps."""
        fresh_credential_manager.set_api_key("tbs_testkey12345")

        plan = ExecutionPlan(
            steps=[
                PlanStep(
                    action="create_bot",
                    description="Create",
                    params={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz123456"},
                ),
            ]
        )

        with patch("agent.executor.TeleBotStudioClient") as MockClient:
            mock_client_instance = MagicMock()
            MockClient.return_value.__enter__ = MagicMock(return_value=mock_client_instance)
            MockClient.return_value.__exit__ = MagicMock(return_value=False)

            with patch("agent.executor.BotManager") as MockBotMgr, \
                 patch("agent.executor.CommandManager"), \
                 patch("agent.executor.BotControlManager"):

                mock_bot_mgr = MagicMock()
                MockBotMgr.return_value = mock_bot_mgr
                mock_bot_mgr.create.return_value = BotInfo(
                    botid="77777", bot_name="TestBot", bot_username="testbot"
                )

                result = Executor.execute_plan(plan)
                assert result.succeeded == 1
                # bot_id should have been stored in session
                assert fresh_credential_manager.get_bot_id() == "77777"
