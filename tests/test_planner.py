"""Tests for the Planner agent."""

from __future__ import annotations

from agent.planner import Planner
from api.models import CommandDef


class TestPlanDeployBot:
    def test_creates_correct_step_sequence(self):
        """Deploy bot should create: create_bot → create_command(s) → start_bot."""
        commands = [CommandDef(name="start", code="bot.reply('Hi')")]
        plan = Planner.plan_deploy_bot("123456:ABCdef", commands)

        actions = [s.action for s in plan.steps]
        assert actions == ["create_bot", "create_command", "start_bot"]

    def test_create_bot_step_has_token(self):
        commands = [CommandDef(name="start", code="code")]
        plan = Planner.plan_deploy_bot("123456:ABCdef", commands)

        create_step = plan.steps[0]
        assert create_step.params["bot_token"] == "123456:ABCdef"
        assert create_step.destructive is False

    def test_command_steps_created(self):
        commands = [
            CommandDef(name="start", code="code1"),
            CommandDef(name="help", code="code2"),
        ]
        plan = Planner.plan_deploy_bot("123456:ABCdef", commands)

        cmd_steps = [s for s in plan.steps if s.action == "create_command"]
        assert len(cmd_steps) == 2
        assert cmd_steps[0].params["command"] == "start"
        assert cmd_steps[1].params["command"] == "help"

    def test_start_bot_step_present(self):
        plan = Planner.plan_deploy_bot("123456:ABCdef", [])
        assert plan.steps[-1].action == "start_bot"

    def test_no_commands_still_creates_start_step(self):
        plan = Planner.plan_deploy_bot("123456:ABCdef", [])
        actions = [s.action for s in plan.steps]
        assert "create_bot" in actions
        assert "start_bot" in actions

    def test_not_destructive(self):
        plan = Planner.plan_deploy_bot("123456:ABCdef", [])
        assert plan.requires_confirmation is False


class TestPlanSetupCommands:
    def test_creates_correct_steps(self):
        commands = [
            CommandDef(name="start", code="code1"),
            CommandDef(name="help", code="code2"),
        ]
        plan = Planner.plan_setup_commands("99999", commands)

        assert len(plan.steps) == 2
        assert all(s.action == "create_command" for s in plan.steps)

    def test_steps_include_bot_id(self):
        commands = [CommandDef(name="start", code="code")]
        plan = Planner.plan_setup_commands("99999", commands)

        assert plan.steps[0].params["bot_id"] == "99999"
        assert plan.steps[0].params["command"] == "start"

    def test_not_destructive(self):
        plan = Planner.plan_setup_commands("99999", [CommandDef(name="x", code="y")])
        assert plan.requires_confirmation is False


class TestPlanBatchCreateCommands:
    def test_delegates_to_setup_commands(self):
        """plan_batch_create_commands should produce the same plan as setup_commands."""
        commands = [CommandDef(name="test", code="code")]
        plan = Planner.plan_batch_create_commands("12345", commands)

        assert len(plan.steps) == 1
        assert plan.steps[0].action == "create_command"


class TestPlanBatchDeleteCommands:
    def test_marks_destructive(self):
        plan = Planner.plan_batch_delete_commands("12345", ["start", "help"])
        assert plan.requires_confirmation is True

    def test_creates_delete_steps(self):
        plan = Planner.plan_batch_delete_commands("12345", ["start", "help"])
        assert len(plan.steps) == 2
        assert all(s.action == "delete_command" for s in plan.steps)
        assert all(s.destructive is True for s in plan.steps)

    def test_steps_include_command_names(self):
        plan = Planner.plan_batch_delete_commands("12345", ["start", "help"])
        assert plan.steps[0].params["command_name"] == "start"
        assert plan.steps[1].params["command_name"] == "help"


class TestPlanDeleteBot:
    def test_marks_destructive(self):
        plan = Planner.plan_delete_bot("12345")
        assert plan.requires_confirmation is True

    def test_single_step(self):
        plan = Planner.plan_delete_bot("12345")
        assert len(plan.steps) == 1
        assert plan.steps[0].action == "delete_bot"
        assert plan.steps[0].destructive is True

    def test_includes_bot_id(self):
        plan = Planner.plan_delete_bot("12345")
        assert plan.steps[0].params["bot_id"] == "12345"


class TestPlanUpdateBotToken:
    def test_marks_destructive(self):
        plan = Planner.plan_update_bot_token("12345", "999:newtoken1234567890abcdef")
        assert plan.requires_confirmation is True

    def test_single_step(self):
        plan = Planner.plan_update_bot_token("12345", "999:newtoken1234567890abcdef")
        assert len(plan.steps) == 1
        assert plan.steps[0].action == "update_bot_token"
        assert plan.steps[0].destructive is True

    def test_includes_params(self):
        plan = Planner.plan_update_bot_token("12345", "999:newtoken1234567890abcdef")
        assert plan.steps[0].params["bot_id"] == "12345"
        assert plan.steps[0].params["new_token"] == "999:newtoken1234567890abcdef"
