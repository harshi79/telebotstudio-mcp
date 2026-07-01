"""
TeleBot Studio Batch MCP Tools.

Registers 2 batch operation tools on the FastMCP server instance:
  - tbs_batch_create_commands
  - tbs_batch_delete_commands  (preview-supported)
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


def register_batch_tools(mcp: FastMCP) -> None:
    """Register all batch operation MCP tools on the FastMCP instance."""

    @mcp.tool
    def tbs_batch_create_commands(
        commands_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Create multiple commands on a bot in sequence.

        Each command is created independently. If one fails, the rest
        continue. A summary with per-command results is returned.

        Args:
            commands_json: JSON array of command definitions.
                           Format: [{"name": "start", "code": "Api.sendMessage(...)"}]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, batch results if confirm=True.
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
        plan = Planner.plan_batch_create_commands(bid, commands)

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
    def tbs_batch_delete_commands(
        command_names_json: str,
        bot_id: str = "",
        confirm: bool = False,
    ) -> str:
        """
        Delete multiple commands from a bot in sequence.

        This is a destructive operation. Each command is deleted independently.
        If one fails, the rest continue. A summary is returned.

        Args:
            command_names_json: JSON array of command names to delete.
                                Format: ["start", "help", "settings"]
            bot_id: Bot ID. Uses session bot_id if not provided.
            confirm: Set to True to execute. False returns a preview.

        Returns:
            Preview if confirm=False, batch results if confirm=True.
        """
        bid, err = _get_bot_id_or_error(bot_id or None)
        if err:
            return err

        # Parse command names
        try:
            names = json.loads(command_names_json)
            if not isinstance(names, list):
                raise ValueError("Expected a JSON array of strings")
        except (json.JSONDecodeError, ValueError) as e:
            return _error_response(
                "validation_error",
                f"Invalid command_names_json: {e}. "
                'Expected: ["start", "help", "settings"]',
            )

        # Plan
        plan = Planner.plan_batch_delete_commands(bid, names)

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
