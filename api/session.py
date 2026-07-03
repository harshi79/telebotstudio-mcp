"""
Session-scoped Credential Manager.

Stores API key and Bot ID in memory only — never persisted to disk,
never logged in cleartext.  Credentials exist for the lifetime of the
MCP server process and are lost on restart (intentional).

Thread Safety:
    All shared state is protected by a threading.Lock.  The active
    session ID is stored in both thread-local storage and a
    contextvars.ContextVar so that concurrent HTTP requests and
    async handlers do not interfere with each other.

Session Isolation (HTTP transport):
    When set_session() is called with a unique session ID per
    client, credentials are fully isolated between sessions.

    The session ID is resolved via contextvars first (for async
    middleware support), falling back to thread-local storage, and
    finally to None (STDIO fallback).  Use set_context_session()
    from async middleware to set the contextvar without touching
    thread-local state.

For STDIO transport (single user), there is only one session.
"""

from __future__ import annotations

import contextvars
import logging
import threading
from typing import Any, ClassVar

from api.utils import mask_credential

logger = logging.getLogger("telebotstudio-mcp.session")


class CredentialManager:
    """In-memory, session-scoped credential storage.

    Supports per-session isolation for multi-user HTTP deployments.
    Falls back to a global default for single-user STDIO mode.

    Thread-safe: all access to shared state is protected by a lock.
    Uses both contextvars and thread-local storage for the active
    session ID so that concurrent requests in HTTP mode (including
    async handlers) cannot interfere with each other.  The contextvar
    is checked first, then thread-local storage, then None.
    """

    _lock: ClassVar[threading.Lock] = threading.Lock()

    # Per-session storage: session_id -> {"api_key": str, "bot_id": str}
    _sessions: ClassVar[dict[str, dict[str, str | None]]] = {}

    # Global fallback for STDIO mode (no session ID)
    _default_api_key: ClassVar[str | None] = None
    _default_bot_id: ClassVar[str | None] = None

    # Thread-local active session ID (replaces class-level _current_session_id)
    _tls: ClassVar[threading.local] = threading.local()

    # Contextvar for async-compatible session isolation
    _ctx_session_id: ClassVar[contextvars.ContextVar[str | None]] = (
        contextvars.ContextVar("_ctx_session_id", default=None)
    )

    # ---- Session Management ----

    @classmethod
    def set_session(cls, session_id: str | None) -> None:
        """Set the active session ID for the current request context.

        Sets both the contextvar and thread-local storage so that
        concurrent HTTP requests and async handlers do not overwrite
        each other's session.
        """
        cls._ctx_session_id.set(session_id)
        cls._tls.session_id = session_id

    @classmethod
    def get_session_id(cls) -> str | None:
        """Get the current active session ID.

        Checks the contextvar first (for async middleware support),
        then falls back to thread-local storage, then returns None.
        """
        ctx_val = cls._ctx_session_id.get()
        if ctx_val is not None:
            return ctx_val
        return getattr(cls._tls, "session_id", None)

    @classmethod
    def set_context_session(cls, session_id: str | None) -> None:
        """Set ONLY the contextvar session ID (for use in async middleware).

        This does not modify thread-local storage, making it safe to
        call from async request middleware that runs in a shared thread.
        """
        cls._ctx_session_id.set(session_id)

    @classmethod
    def get_context_session_id(cls) -> str | None:
        """Read ONLY the contextvar session ID.

        Returns None if no contextvar session has been set.
        """
        return cls._ctx_session_id.get()

    # ---- Internal Helpers ----

    @classmethod
    def _get_store(cls) -> dict[str, str | None]:
        """Get a snapshot of the credential store for the current session.

        Returns a COPY of the store dict so that callers don't
        hold references to internal mutable state across lock
        boundaries.  This prevents stale reads after concurrent
        writes.
        """
        sid = cls.get_session_id()
        if sid:
            with cls._lock:
                if sid not in cls._sessions:
                    cls._sessions[sid] = {"api_key": None, "bot_id": None}
                return dict(cls._sessions[sid])
        # Fallback: global defaults (STDIO mode)
        with cls._lock:
            return {"api_key": cls._default_api_key, "bot_id": cls._default_bot_id}

    @classmethod
    def _set_in_store(cls, key: str, value: str) -> None:
        """Set a value in the appropriate store."""
        sid = cls.get_session_id()
        if sid:
            with cls._lock:
                if sid not in cls._sessions:
                    cls._sessions[sid] = {"api_key": None, "bot_id": None}
                cls._sessions[sid][key] = value
        else:
            # Global fallback (STDIO mode — single thread)
            with cls._lock:
                if key == "api_key":
                    cls._default_api_key = value
                elif key == "bot_id":
                    cls._default_bot_id = value

    # ---- Setters ----

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """Store the API key for the current session."""
        cls._set_in_store("api_key", api_key.strip())
        logger.info("API key set for session (length=%d)", len(api_key.strip()))

    @classmethod
    def set_bot_id(cls, bot_id: str) -> None:
        """Store the active Bot ID for the current session."""
        cls._set_in_store("bot_id", bot_id.strip())
        logger.info("Bot ID set for session: %s", mask_credential(bot_id))

    # ---- Getters ----

    @classmethod
    def get_api_key(cls) -> str | None:
        """Return the session API key, or None if not set."""
        store = cls._get_store()
        key = store.get("api_key")
        return key if key else None

    @classmethod
    def get_bot_id(cls) -> str | None:
        """Return the session Bot ID, or None if not set."""
        store = cls._get_store()
        bid = store.get("bot_id")
        return bid if bid else None

    # ---- Status ----

    @classmethod
    def has_api_key(cls) -> bool:
        key = cls.get_api_key()
        return key is not None and len(key) > 0

    @classmethod
    def has_bot_id(cls) -> bool:
        bid = cls.get_bot_id()
        return bid is not None and len(bid) > 0

    @classmethod
    def status(cls) -> dict[str, Any]:
        """Return a status summary (key is masked)."""
        key = cls.get_api_key()
        bid = cls.get_bot_id()
        return {
            "api_key_set": cls.has_api_key(),
            "api_key_preview": mask_credential(key) if key else None,
            "bot_id_set": cls.has_bot_id(),
            "bot_id": bid if bid else None,
        }

    # ---- Cleanup ----

    @classmethod
    def clear(cls) -> None:
        """Clear credentials for the current session."""
        sid = cls.get_session_id()
        with cls._lock:
            if sid and sid in cls._sessions:
                cls._sessions[sid] = {"api_key": None, "bot_id": None}
            else:
                cls._default_api_key = None
                cls._default_bot_id = None
        logger.info("Session credentials cleared")

    @classmethod
    def clear_session(cls, session_id: str) -> None:
        """Clear credentials for a specific session (called on disconnect)."""
        with cls._lock:
            if session_id in cls._sessions:
                del cls._sessions[session_id]
                logger.info("Session %s cleared", mask_credential(session_id))

    @classmethod
    def active_session_count(cls) -> int:
        """Return the number of active sessions (for monitoring)."""
        with cls._lock:
            return len(cls._sessions)

    @classmethod
    def cleanup_all_sessions(cls) -> int:
        """Remove ALL sessions (for server shutdown / testing).

        Returns the number of sessions that were removed.
        """
        with cls._lock:
            count = len(cls._sessions)
            cls._sessions.clear()
            cls._default_api_key = None
            cls._default_bot_id = None
        logger.info("Cleaned up %d sessions", count)
        return count
