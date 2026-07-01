"""
Agent Validator.

Validates execution plans before they are previewed or executed.
Checks:
  - Session credentials are present
  - Parameters are valid
  - Required dependencies between steps are met
"""

from __future__ import annotations

import logging

from api.auth import (
    validate_api_key,
    validate_bot_id,
    validate_bot_token,
    validate_command_name,
    validate_command_code,
)
from api.errors import ValidationError
from api.models import ExecutionPlan
from api.session import CredentialManager

logger = logging.getLogger("telebotstudio-mcp.agent.validator")


class Validator:
    """Validates execution plans against session state and parameter rules."""

    @staticmethod
    def validate_credentials() -> tuple[bool, str]:
        """
        Check that session credentials are present.

        Returns (is_valid, message).
        """
        if not CredentialManager.has_api_key():
            return (
                False,
                "API key not set. Use tbs_set_api_key to provide your "
                "TeleBot Studio API key. You can find it at "
                "telebotstudio.com → Account Settings → API.",
            )
        return True, "Credentials OK"

    @staticmethod
    def validate_bot_id_for_step(action: str, params: dict) -> tuple[bool, str]:
        """
        Check that a bot_id is available for bot-scoped operations.
        For create_bot, no bot_id is needed.
        For all other operations, bot_id must be in params or session.
        """
        if action == "create_bot":
            return True, "No bot_id needed for bot creation"

        # Check params first, then session
        bot_id = params.get("bot_id") or CredentialManager.get_bot_id()
        if not bot_id:
            return (
                False,
                "Bot ID not set. Use tbs_set_bot_id to specify which bot "
                "to operate on, or create a bot first with tbs_create_bot.",
            )

        # Validate format
        try:
            validate_bot_id(bot_id)
        except ValidationError as e:
            return False, str(e)

        return True, f"Bot ID: {bot_id}"

    @staticmethod
    def validate_plan(plan: ExecutionPlan) -> tuple[bool, list[str]]:
        """
        Validate an entire execution plan.

        Understands step dependencies: if a create_bot step is present,
        subsequent steps that need a bot_id are considered satisfied
        (the bot_id will be produced dynamically at execution time).

        Returns (is_valid, list_of_error_messages).
        """
        errors: list[str] = []

        # Check credentials
        cred_ok, cred_msg = Validator.validate_credentials()
        if not cred_ok:
            errors.append(cred_msg)

        # Track whether a create_bot step will produce a bot_id
        has_create_bot = any(s.action == "create_bot" for s in plan.steps)

        # Check each step
        for i, step in enumerate(plan.steps):
            # Check bot_id for bot-scoped operations
            # Skip bot_id check if create_bot precedes this step
            if step.action == "create_bot":
                pass  # No bot_id needed
            elif has_create_bot and i > 0:
                pass  # Bot_id will come from create_bot step
            else:
                bot_ok, bot_msg = Validator.validate_bot_id_for_step(
                    step.action, step.params
                )
                if not bot_ok:
                    errors.append(f"Step {i + 1} ({step.action}): {bot_msg}")

            # Validate specific parameters per action
            try:
                if step.action == "create_bot":
                    validate_bot_token(step.params.get("bot_token", ""))

                elif step.action == "create_command":
                    validate_command_name(step.params.get("command", ""))
                    validate_command_code(step.params.get("code", ""))

                elif step.action == "update_command":
                    validate_command_name(step.params.get("command_name", ""))
                    validate_command_code(step.params.get("code", ""))

                elif step.action == "delete_command":
                    validate_command_name(step.params.get("command_name", ""))

                elif step.action == "update_bot_token":
                    validate_bot_token(step.params.get("new_token", ""))

            except ValidationError as e:
                errors.append(f"Step {i + 1} ({step.action}): {e}")

        return len(errors) == 0, errors
