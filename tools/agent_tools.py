"""
TeleBot Studio Agent MCP Tools.

Registers 2 agent-level tools on the FastMCP server instance:
  - tbs_deploy_bot
  - tbs_setup_commands
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from agent.executor import Executor
from agent.planner import Planner
from agent.preview import Preview
from agent.validator import Validator
from api.models import CommandDef
from tools.helpers import _error_response, _get_bot_id_or_error

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_agent_tools(mcp: FastMCP) -> None:
    """Register all agent-level MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_deploy_bot(
        bot_token: str,
        commands_json: str,
        confirm: bool = False,
    ) -> str:
        """
        Complete bot deployment: create bot, add commands, and start it.

        This is an agent-level tool that orchestrates multiple API calls
        in sequence. The AI uses this to fulfill high-level requests like
        "build me a bot" or "deploy a premium system."

        The bot ID from creation is automatically used for subsequent steps.

        Args:
            bot_token: Telegram bot token from @BotFather.
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, execution results if confirm=True.
        """
        # Parse commands
        try:
            cmds_data = json.loads(commands_json)
            commands = [
                CommandDef(name=c["name"], code=c["code"]) for c in cmds_data
            ]
        except (json.JSONDecodeError, KeyError) as e:
            return _error_response(
                "validation_error",
                f"Invalid commands_json format: {e}. "
                'Expected: [{{"name": "start", "code": "Api.sendMessage(...)"}}]',
            )

        # Plan
        plan = Planner.plan_deploy_bot(bot_token, commands)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)

    @mcp.tool
    def tbs_setup_commands(
        commands_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Bulk create commands on an existing bot.

        This is an agent-level tool for setting up multiple commands at once.

        Args:
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, execution results if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        # Parse commands
        try:
            cmds_data = json.loads(commands_json)
            commands = [
                CommandDef(name=c["name"], code=c["code"]) for c in cmds_data
            ]
        except (json.JSONDecodeError, KeyError) as e:
            return _error_response(
                "validation_error",
                f"Invalid commands_json format: {e}. "
                'Expected: [{{"name": "start", "code": "Api.sendMessage(...)"}}]',
            )

        # Plan
        plan = Planner.plan_setup_commands(bid, commands)

        # Validate
        valid, errors = Validator.validate_plan(plan)
        if not valid:
            return _error_response(
                "validation_error",
                "Plan validation failed",
                errors=errors,
            )

        # Preview
        if not confirm:
            return Preview.generate(plan)

        # Execute
        result = Executor.execute_plan(plan)
        return json.dumps(result.to_dict(), indent=2)
