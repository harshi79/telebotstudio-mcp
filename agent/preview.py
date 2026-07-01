"""
Agent Preview.

Generates human-readable previews of execution plans, especially
for destructive operations.  Previews describe what WILL happen
without executing anything.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from api.models import ExecutionPlan

from api.utils import mask_value


class Preview:
    """Generates previews of execution plans before execution."""

    @staticmethod
    def generate(plan: ExecutionPlan) -> str:
        """
        Generate a human-readable preview of the execution plan.

        Sensitive parameters (bot tokens) are masked in the output.
        """
        steps_preview: list[dict[str, Any]] = []
        for i, step in enumerate(plan.steps, 1):
            step_info: dict[str, Any] = {
                "step": i,
                "action": step.action,
                "description": step.description,
            }

            # Add parameter details (mask sensitive values)
            if step.action == "create_bot":
                step_info["bot_token"] = mask_value(
                    step.params.get("bot_token", "")
                )
            elif step.action == "update_bot_token":
                step_info["new_token"] = mask_value(
                    step.params.get("new_token", "")
                )
            elif step.action in ("create_command", "update_command"):
                code = step.params.get("code", "")
                step_info["code_length"] = len(code)
                step_info["code_preview"] = (
                    code[:80] + "..." if len(code) > 80 else code
                )

            steps_preview.append(step_info)

        result = {
            "preview": True,
            "summary": _generate_summary(plan),
            "total_steps": len(plan.steps),
            "steps": steps_preview,
            "requires_confirmation": plan.requires_confirmation,
        }

        if plan.requires_confirmation:
            result["warning"] = (
                "This plan contains destructive operations. "
                "Set confirm=true to execute."
            )
        else:
            result["note"] = (
                "Set confirm=true to execute this plan."
            )

        return json.dumps(result, indent=2)

    @staticmethod
    def generate_destructive_preview(
        action: str,
        description: str,
        params: dict,
    ) -> str:
        """
        Generate a preview for a single destructive operation.

        Used by individual MCP tools that support confirm=False.
        """
        result = {
            "preview": True,
            "action": action,
            "description": description,
            "warning": (
                "This is a destructive operation. "
                "Set confirm=true to execute."
            ),
        }

        # Add relevant params (masked)
        if "bot_id" in params:
            result["bot_id"] = params["bot_id"]
        if "command_name" in params:
            result["command_name"] = params["command_name"]

        return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _generate_summary(plan: ExecutionPlan) -> str:
    """Generate a one-line summary of the plan."""
    actions = [s.action for s in plan.steps]

    if "create_bot" in actions and "start_bot" in actions:
        cmd_count = actions.count("create_command")
        return f"Deploy new bot with {cmd_count} command(s) and start it"

    if actions.count("delete_command") > 1:
        return f"Delete {actions.count('delete_command')} commands"

    if "delete_bot" in actions:
        return "Delete bot (soft delete — data preserved)"

    if "update_bot_token" in actions:
        return "Update bot token (bot will restart)"

    return f"Execute {len(plan.steps)} operation(s)"
