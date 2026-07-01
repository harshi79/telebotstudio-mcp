"""Tests for CredentialManager (session.py)."""

from __future__ import annotations

from api.utils import mask_credential


class TestSetGetApiKey:
    def test_set_and_get_api_key(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("tbs_testkey12345")
        assert fresh_credential_manager.get_api_key() == "tbs_testkey12345"

    def test_get_api_key_returns_none_when_not_set(self, fresh_credential_manager):
        assert fresh_credential_manager.get_api_key() is None

    def test_api_key_stripped(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("  tbs_testkey12345  ")
        assert fresh_credential_manager.get_api_key() == "tbs_testkey12345"


class TestSetGetBotId:
    def test_set_and_get_bot_id(self, fresh_credential_manager):
        fresh_credential_manager.set_bot_id("12345")
        assert fresh_credential_manager.get_bot_id() == "12345"

    def test_get_bot_id_returns_none_when_not_set(self, fresh_credential_manager):
        assert fresh_credential_manager.get_bot_id() is None

    def test_bot_id_stripped(self, fresh_credential_manager):
        fresh_credential_manager.set_bot_id("  12345  ")
        assert fresh_credential_manager.get_bot_id() == "12345"


class TestStatus:
    def test_status_masks_api_key(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("tbs_longsecretkey123456")
        status = fresh_credential_manager.status()
        assert status["api_key_set"] is True
        # The key preview should be masked
        preview = status["api_key_preview"]
        assert "tbs_longsecretkey123456" not in preview
        assert "..." in preview

    def test_status_shows_bot_id(self, fresh_credential_manager):
        fresh_credential_manager.set_bot_id("12345")
        status = fresh_credential_manager.status()
        assert status["bot_id_set"] is True
        assert status["bot_id"] == "12345"

    def test_status_when_empty(self, fresh_credential_manager):
        status = fresh_credential_manager.status()
        assert status["api_key_set"] is False
        assert status["api_key_preview"] is None
        assert status["bot_id_set"] is False
        assert status["bot_id"] is None


class TestClear:
    def test_clear_resets_credentials(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("tbs_testkey12345")
        fresh_credential_manager.set_bot_id("12345")
        fresh_credential_manager.clear()
        assert fresh_credential_manager.get_api_key() is None
        assert fresh_credential_manager.get_bot_id() is None


class TestSessionIsolation:
    def test_sessions_are_isolated(self, fresh_credential_manager):
        """Different session IDs should have independent credentials."""
        # Session A
        fresh_credential_manager.set_session("session-a")
        fresh_credential_manager.set_api_key("key_for_a")
        fresh_credential_manager.set_bot_id("111")

        # Session B
        fresh_credential_manager.set_session("session-b")
        fresh_credential_manager.set_api_key("key_for_b")
        fresh_credential_manager.set_bot_id("222")

        # Verify session A's data
        fresh_credential_manager.set_session("session-a")
        assert fresh_credential_manager.get_api_key() == "key_for_a"
        assert fresh_credential_manager.get_bot_id() == "111"

        # Verify session B's data
        fresh_credential_manager.set_session("session-b")
        assert fresh_credential_manager.get_api_key() == "key_for_b"
        assert fresh_credential_manager.get_bot_id() == "222"


class TestCleanupAllSessions:
    def test_cleanup_removes_all_sessions(self, fresh_credential_manager):
        fresh_credential_manager.set_session("s1")
        fresh_credential_manager.set_api_key("key1")

        fresh_credential_manager.set_session("s2")
        fresh_credential_manager.set_api_key("key2")

        count = fresh_credential_manager.cleanup_all_sessions()
        assert count == 2

        # Both sessions should be gone
        fresh_credential_manager.set_session("s1")
        assert fresh_credential_manager.get_api_key() is None

    def test_cleanup_clears_global_defaults(self, fresh_credential_manager):
        fresh_credential_manager.set_session(None)
        fresh_credential_manager.set_api_key("global_key")
        fresh_credential_manager.cleanup_all_sessions()
        assert fresh_credential_manager.get_api_key() is None


class TestMaskHelper:
    def test_short_value(self):
        assert mask_credential("short") == "***"

    def test_long_value(self):
        result = mask_credential("tbs_longsecretkey123456")
        assert result.startswith("tbs_")
        assert result.endswith("3456")
        assert "..." in result

    def test_exactly_8_chars(self):
        assert mask_credential("12345678") == "***"

    def test_9_chars(self):
        # 9 chars > 8, so should show first 4 ... last 4
        result = mask_credential("123456789")
        assert result == "1234...6789"


class TestHasApiKey:
    def test_has_api_key_true(self, fresh_credential_manager):
        fresh_credential_manager.set_api_key("tbs_testkey12345")
        assert fresh_credential_manager.has_api_key() is True

    def test_has_api_key_false(self, fresh_credential_manager):
        assert fresh_credential_manager.has_api_key() is False


class TestHasBotId:
    def test_has_bot_id_true(self, fresh_credential_manager):
        fresh_credential_manager.set_bot_id("12345")
        assert fresh_credential_manager.has_bot_id() is True

    def test_has_bot_id_false(self, fresh_credential_manager):
        assert fresh_credential_manager.has_bot_id() is False
