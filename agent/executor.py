"""
Agent Executor.

Executes validated ExecutionPlans step by step, with:
  - Sequential execution
  - Per-step error capture (does not abort on first failure)
  - Structured BatchResult reporting
  - Rate-limit awareness (pause between steps)
"""

from __future__ import annotations

import asyncio
import logging
import time

from api.bot_control import BotControlManager
from api.bots import BotManager
from api.client import TeleBotStudioClient
from api.commands import CommandManager
from api.errors import TeleBotStudioError
from api.models import (
    BatchResult,
    ExecutionPlan,
    PlanStep,
    StepResult,
)
from api.session import CredentialManager

logger = logging.getLogger("telebotstudio-mcp.agent.executor")

# Delay between batch steps to respect rate limits (60 req/min)
_STEP_DELAY = 1.0  # seconds


class Executor:
    """Executes validated execution plans."""

    @staticmethod
    def execute_plan(
        plan: ExecutionPlan,
        api_key: str | None = None,
    ) -> BatchResult:
        """
        Execute an entire ExecutionPlan sequentially.

        Each step is executed independently. If a step fails,
        execution continues with the next step (does not abort).
        All results are collected in a BatchResult.

        For deploy_bot plans, the bot_id from the create_bot step
        is automatically propagated to subsequent steps.
        """
        key = api_key or CredentialManager.get_api_key()
        if not key:
            return BatchResult(
                total=len(plan.steps),
                succeeded=0,
                failed=len(plan.steps),
                results=[
                    StepResult(
                        action=s.action,
                        success=False,
                        message="API key not set. Use tbs_set_api_key first.",
                    )
                    for s in plan.steps
                ],
            )

        results: list[StepResult] = []
        created_bot_id: str | None = CredentialManager.get_bot_id()

        with TeleBotStudioClient(api_key=key) as client:
            bot_mgr = BotManager(client)
            cmd_mgr = CommandManager(client)
            control_mgr = BotControlManager(client)

            for i, step in enumerate(plan.steps):
                step_result = Executor._execute_step(
                    step=step,
                    bot_mgr=bot_mgr,
                    cmd_mgr=cmd_mgr,
                    control_mgr=control_mgr,
                    bot_id=created_bot_id,
                )
                results.append(step_result)

                # If this was create_bot and it succeeded, capture the bot_id
                if step.action == "create_bot" and step_result.success:
                    created_bot_id = step_result.data
                    # Also store in session for subsequent operations
                    CredentialManager.set_bot_id(created_bot_id)

                # Rate-limit pause between steps (skip after last step)
                if i < len(plan.steps) - 1:
                    Executor._rate_limit_pause()

        succeeded = sum(1 for r in results if r.success)
        failed = sum(1 for r in results if not r.success)

        return BatchResult(
            total=len(plan.steps),
            succeeded=succeeded,
            failed=failed,
            results=results,
        )

    @staticmethod
    def _rate_limit_pause() -> None:
        """Pause between batch steps to respect rate limits.

        Uses the same async-aware sleep logic as TeleBotStudioClient
        so the event loop is not blocked under HTTP transport.
        """
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = loop.run_in_executor(pool, time.sleep, _STEP_DELAY)
                concurrent.futures.wait([future])
        except RuntimeError:
            time.sleep(_STEP_DELAY)

    @staticmethod
    def _execute_step(
        step: PlanStep,
        bot_mgr: BotManager,
        cmd_mgr: CommandManager,
        control_mgr: BotControlManager,
        bot_id: str | None,
    ) -> StepResult:
        """Execute a single plan step and return the result."""
        try:
            if step.action == "create_bot":
                info = bot_mgr.create(step.params["bot_token"])
                return StepResult(
                    action=step.action,
                    success=True,
                    message=f"Bot created: {info.bot_name} (ID: {info.botid})",
                    data=info.botid,
                )

            elif step.action == "delete_bot":
                bid = step.params.get("bot_id", bot_id)
                msg = bot_mgr.delete(bid)
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "update_bot_token":
                bid = step.params.get("bot_id", bot_id)
                msg = bot_mgr.update_token(
                    bid, step.params["new_token"]
                )
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "create_command":
                bid = step.params.get("bot_id", bot_id)
                msg = cmd_mgr.create(
                    bid, step.params["command"], step.params["code"]
                )
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "update_command":
                bid = step.params.get("bot_id", bot_id)
                msg = cmd_mgr.update(
                    bid, step.params["command_name"], step.params["code"]
                )
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "delete_command":
                bid = step.params.get("bot_id", bot_id)
                msg = cmd_mgr.delete(bid, step.params["command_name"])
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "start_bot":
                bid = step.params.get("bot_id", bot_id)
                msg = control_mgr.start(bid)
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "stop_bot":
                bid = step.params.get("bot_id", bot_id)
                msg = control_mgr.stop(bid)
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            elif step.action == "restart_bot":
                bid = step.params.get("bot_id", bot_id)
                msg = control_mgr.restart(bid)
                return StepResult(
                    action=step.action,
                    success=True,
                    message=msg,
                )

            else:
                return StepResult(
                    action=step.action,
                    success=False,
                    message=f"Unknown action: {step.action}",
                )

        except TeleBotStudioError as e:
            logger.error("Step '%s' failed: %s", step.action, e.message)
            return StepResult(
                action=step.action,
                success=False,
                message=f"{e.error_category}: {e.message}",
            )

        except ValueError as e:
            logger.error("Step '%s' validation error: %s", step.action, e)
            return StepResult(
                action=step.action,
                success=False,
                message=f"validation_error: {e}",
            )

        except Exception as e:
            logger.error(
                "Step '%s' unexpected error: %s", step.action, e, exc_info=True
            )
            return StepResult(
                action=step.action,
                success=False,
                message=f"unexpected_error: {e}",
            )
