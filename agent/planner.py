"""
Agent Planner.

Decomposes high-level user goals into ordered ExecutionPlans
composed of discrete PlanSteps.

Each step has:
  - action: the API operation to perform
  - description: human-readable summary
  - params: parameters for the operation
  - destructive: whether the operation is irreversible

The planner is a pure function — no side effects, no API calls.
"""

from __future__ import annotations

from api.models import CommandDef, ExecutionPlan, PlanStep


class Planner:
    """Decomposes high-level goals into execution plans."""

    @staticmethod
    def plan_deploy_bot(
        bot_token: str,
        commands: list[CommandDef],
    ) -> ExecutionPlan:
        """
        Plan a complete bot deployment:
        1. Create bot
        2. Create each command
        3. Start bot
        """
        steps: list[PlanStep] = []

        # Step 1: Create bot
        steps.append(
            PlanStep(
                action="create_bot",
                description="Create a new Telegram bot",
                params={"bot_token": bot_token},
                destructive=False,
            )
        )

        # Step 2: Create each command
        for cmd in commands:
            steps.append(
                PlanStep(
                    action="create_command",
                    description=f"Create command '/{cmd.name}'",
                    params={"command": cmd.name, "code": cmd.code},
                    destructive=False,
                )
            )

        # Step 3: Start bot
        steps.append(
            PlanStep(
                action="start_bot",
                description="Start the bot (set webhook)",
                params={},
                destructive=False,
            )
        )

        return ExecutionPlan(
            steps=steps,
            requires_confirmation=any(s.destructive for s in steps),
        )

    @staticmethod
    def plan_setup_commands(
        bot_id: str,
        commands: list[CommandDef],
    ) -> ExecutionPlan:
        """
        Plan bulk command creation on an existing bot.
        """
        steps: list[PlanStep] = []

        for cmd in commands:
            steps.append(
                PlanStep(
                    action="create_command",
                    description=f"Create command '/{cmd.name}' on bot {bot_id}",
                    params={
                        "bot_id": bot_id,
                        "command": cmd.name,
                        "code": cmd.code,
                    },
                    destructive=False,
                )
            )

        return ExecutionPlan(
            steps=steps,
            requires_confirmation=False,
        )

    @staticmethod
    def plan_batch_create_commands(
        bot_id: str,
        commands: list[CommandDef],
    ) -> ExecutionPlan:
        """
        Plan batch command creation (same as setup_commands but explicit).
        """
        return Planner.plan_setup_commands(bot_id, commands)

    @staticmethod
    def plan_batch_delete_commands(
        bot_id: str,
        command_names: list[str],
    ) -> ExecutionPlan:
        """
        Plan batch command deletion.
        Destructive — requires confirmation.
        """
        steps: list[PlanStep] = []

        for name in command_names:
            steps.append(
                PlanStep(
                    action="delete_command",
                    description=f"Delete command '/{name}' from bot {bot_id}",
                    params={"bot_id": bot_id, "command_name": name},
                    destructive=True,
                )
            )

        return ExecutionPlan(
            steps=steps,
            requires_confirmation=True,
        )

    @staticmethod
    def plan_delete_bot(bot_id: str) -> ExecutionPlan:
        """
        Plan bot deletion.
        Destructive — requires confirmation.
        """
        return ExecutionPlan(
            steps=[
                PlanStep(
                    action="delete_bot",
                    description=f"Delete bot {bot_id} (soft delete — data preserved)",
                    params={"bot_id": bot_id},
                    destructive=True,
                )
            ],
            requires_confirmation=True,
        )

    @staticmethod
    def plan_update_bot_token(bot_id: str, new_token: str) -> ExecutionPlan:
        """
        Plan bot token update.
        Destructive — bot restarts automatically.
        """
        return ExecutionPlan(
            steps=[
                PlanStep(
                    action="update_bot_token",
                    description=f"Update token for bot {bot_id} (bot will restart automatically)",
                    params={"bot_id": bot_id, "new_token": new_token},
                    destructive=True,
                )
            ],
            requires_confirmation=True,
        )
