# Security Policy

## Reporting Vulnerabilities

Report security vulnerabilities privately to **security@telebotstudio.com**.

Do **not** open public GitHub Issues or Pull Requests for suspected security vulnerabilities.

## Scope

The following qualify as security vulnerabilities:

- Authentication bypass or cross-session credential leakage
- Exposure of unmasked API keys or Telegram bot tokens in logs, previews, or error responses
- Path traversal or file read outside the configured `docs/` directory via MCP tools
- Denial-of-service vectors via crafted tool inputs or unbounded memory growth
- Any flaw that compromises credential confidentiality or execution integrity

The following are **not** security vulnerabilities (file a standard GitHub Issue instead):

- Functional bugs in search ranking or command formatting
- Feature requests or documentation typos
- Upstream TeleBot Studio API quota or rate-limit responses (`HTTP 429`)

## Response Timeline

| Stage | Target |
|---|---|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 5 business days |
| Status updates | Every 5 business days until resolved |

## Supported Versions

| Version | Supported |
|---|---|
| `2.2.x` (latest) | Yes |
| `< 2.2.0` | No — upgrade to latest `main` / release |

## Credential & Session Security Architecture

- **Memory-only storage (`CredentialManager`)**: API keys and Bot IDs live strictly in process memory (`api/session.py`). Nothing is written to disk, databases, environment files, or logs, and all credentials disappear immediately on process exit.
- **Transport isolation modes**:
  - **STDIO mode (local single-user)**: Uses a lock-protected in-memory default store scoped to the local MCP server subprocess.
  - **HTTP mode (`--transport http`)**: `_SessionMiddleware` in `server.py` extracts the `X-Session-ID` HTTP request header and binds it to both `contextvars.ContextVar` (async task isolation) and `threading.local` (worker thread fallback), resetting context after each request.
  - **Deployment note for multi-user HTTP hosting**: Requests without an `X-Session-ID` header fall back to the shared default store. In multi-tenant deployments behind a gateway or reverse proxy, ensure your gateway injects a distinct, unpredictable `X-Session-ID` per authenticated user session.
- **Hashed connection pooling (`ConnectionPool`)**: Persistent `httpx.Client` instances are keyed by `SHA-256(api_key)`, bounded at 100 active tenants (LRU eviction), and automatically evicted after 300 seconds of inactivity.
- **Secret masking (`api/utils.py`)**:
  - `mask_credential()` masks API keys and session IDs to `first4...last4` (`***` if `<= 8` chars).
  - `mask_value()` masks bot tokens in execution previews to `first5...last5` (`***` if `<= 10` chars).
- **Destructive operation guardrails**: `tbs_delete_bot`, `tbs_update_bot_token`, `tbs_update_command`, `tbs_delete_command`, and `tbs_batch_delete_commands` default to `confirm=False` and return non-mutating previews until explicitly invoked with `confirm=True`.
- **Path traversal prevention**: `get_page()` strips all path separators and rejects `..` sequences through a strict character allowlist (`[A-Za-z0-9-_. ]`) before matching indexed corpus entries in memory.

If you suspect an API key or Telegram bot token was exposed, rotate it immediately in **TeleBot Studio → Settings → API Access** (or via `@BotFather` / `tbs_update_bot_token`).
