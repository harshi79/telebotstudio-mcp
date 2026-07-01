"""
Shared utility functions for the TeleBot Studio API layer.

Centralises patterns used across multiple modules so they are
defined in exactly one place.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import time

# ---------------------------------------------------------------------------
# Credential / Token Masking
# ---------------------------------------------------------------------------

# Two masking policies are provided because different display contexts
# require different trade-offs between readability and security:
#
#   mask_value   - first/last 5 chars visible; used for long bot tokens
#                  that users may need to visually identify.
#   mask_credential - first/last 4 chars visible; used for API keys and
#                  other credentials where less exposure is preferred.
#
# Both functions return "***" when the input is too short to mask safely.


def mask_value(value: str) -> str:
    """Mask a sensitive value for safe display (5 + 5 chars visible).

    Used primarily for bot tokens where the user may need to visually
    confirm which token is in use.  Returns ``***`` for values shorter
    than or equal to 10 characters.

    Args:
        value: The secret string to mask.

    Returns:
        A masked representation like ``abcde...vwxyz``.
    """
    if not isinstance(value, str) or len(value) <= 10:
        return "***"
    return f"{value[:5]}...{value[-5:]}"


def mask_credential(value: str) -> str:
    """Mask a credential for safe display (4 + 4 chars visible).

    A slightly more conservative mask than :func:`mask_value`, showing
    fewer characters.  Used for API keys and session identifiers where
    less exposure is preferred.

    Returns ``***`` for values shorter than or equal to 8 characters.

    Args:
        value: The secret string to mask.

    Returns:
        A masked representation like ``tbs_...3456``.
    """
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


# ---------------------------------------------------------------------------
# Async-aware Sleep
# ---------------------------------------------------------------------------


def async_sleep(seconds: float) -> None:
    """Sleep that works in both sync and async contexts.

    When called from within a running event loop (e.g. HTTP transport),
    uses ``run_in_executor`` + ``concurrent.futures.wait`` to block the
    calling thread without blocking the event loop.  When no event loop
    is running (STDIO transport), falls back to plain ``time.sleep``.

    **Limitation:** In the async path, ``concurrent.futures.wait`` blocks
    the calling *sync* thread until the sleep completes while the event
    loop remains free to process other coroutines.  However, if the event
    loop is in a state where it cannot schedule the executor callback
    (for example, the loop is shutting down or the calling thread is the
    same thread the loop uses for I/O callbacks), this can deadlock.
    This should not occur in practice because FastMCP's sync tool handlers
    run in a thread pool, but callers should be aware of the edge case.

    Args:
        seconds: Number of seconds to sleep.
    """
    try:
        loop = asyncio.get_running_loop()
        # We're inside an async context but our code is sync.
        # Use run_in_executor and block until the sleep completes.
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = loop.run_in_executor(pool, time.sleep, seconds)
            # Block the calling sync thread until the sleep completes,
            # but the event loop remains free to process other coroutines.
            # asyncio.Future is not a subtype of concurrent.futures.Future,
            # but wait() works at runtime because they share the same interface.
            concurrent.futures.wait([future])  # type: ignore[arg-type]
    except RuntimeError:
        # No running event loop — safe to use time.sleep
        time.sleep(seconds)
