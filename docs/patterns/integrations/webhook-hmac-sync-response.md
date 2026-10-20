---
title: Verified External Webhook Receiver & Async API Callback
category: integrations
difficulty: intermediate
keywords: webhook, verifyHMAC, signHMAC, Lib.Security, setWebhookResponse, fallback_command, Request.post, options.headers, options.ip, external API, payment webhook, idempotency, Bot.fetchData, Bot.storeData, User.res, StopExecution
commands: /webhook_payment, /trigger_report, /handle_report_result
callback_handlers: none
tags: integrations, webhook, hmac, security, sync-response, external-api, async-http, v1.1.0
verified: false
tested_with:
last_updated: 2026-10-20
---

# Verified External Webhook Receiver & Async API Callback

## Purpose

Receives external HTTP webhooks securely with `Lib.Security.verifyHMAC`, prevents duplicate event processing, returns a synchronous JSON payload via `Bot.setWebhookResponse`, and demonstrates long-running outbound API calls using `Request.post(..., fallback_command=...)`.

## When to Use

- External services (payment gateways, SaaS platforms, CI pipelines, custom backends) send webhooks to your TeleBot Studio bot
- You must cryptographically verify request authenticity using an HMAC header (`options.headers`) before crediting balances or triggering actions
- The external caller expects an immediate JSON response in the same HTTP request (`Bot.setWebhookResponse`)
- Your bot calls slow third-party APIs (AI pipelines, report generators, indexers) that exceed standard request timeouts and require `fallback_command`

Do NOT use this pattern for:
- Simple fast `GET` requests under a few seconds — call `Request.get(url)` directly
- Storing plain API keys inside command source code — store shared secrets in the bot's **Env** settings tab

## Features

- **Cryptographic HMAC verification**: Validates `X-Webhook-Signature` from `options.headers` using `Lib.Security.verifyHMAC`
- **Caller metadata logging**: Captures caller IP address via `options.ip` for audit trails
- **Idempotency protection**: Tracks processed `event_id` values in `Bot.storeData` so retried webhooks never double-credit users
- **Synchronous HTTP JSON response**: Returns `{"received": True, ...}` directly to the webhook sender via `Bot.setWebhookResponse`
- **User notification & credit grant**: Updates user balance in `Bot.storeData` and sends a Telegram confirmation message
- **Long-running outbound API pattern**: Dispatches slow external jobs via `Request.post(..., timeout=240, fallback_command="/handle_report_result")` without blocking the user

## Commands

| Command | Description |
|:---|:---|
| `/webhook_payment` | Webhook-triggered command that verifies HMAC signatures, credits user accounts once, and returns a sync JSON response |
| `/trigger_report` | User command that starts a long-running external API job asynchronously via `fallback_command` |
| `/handle_report_result` | Callback command invoked automatically when the long-running HTTP request finishes |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| None | This pattern processes external HTTP webhooks and async HTTP callbacks rather than inline button presses |

## Complete Working Code

### Command: /webhook_payment

```tbs
# Set WEBHOOK_SECRET in your bot's Env tab in TeleBot Studio
raw_body = options.body if hasattr(options, "body") else ""
headers = options.headers if hasattr(options, "headers") else {}
caller_ip = str(options.ip) if hasattr(options, "ip") else "unknown"

# Normalize header lookup (headers may arrive lowercase or mixed case)
signature = headers.get("x-webhook-signature") or headers.get("X-Webhook-Signature") or ""

# 1. Verify HMAC-SHA256 signature before trusting any field
if not signature or not Lib.Security.verifyHMAC(WEBHOOK_SECRET, str(raw_body), signature):
    Bot.setWebhookResponse({"accepted": False, "error": "invalid_signature", "ip": caller_ip})
    raise StopExecution()

# 2. Parse verified payload
payload = Lib.JSON.parse(raw_body) if isinstance(raw_body, str) else raw_body
event_id = str(payload.get("event_id", ""))
target_user_id = int(payload.get("telegram_user_id", 0))
credits_delta = int(payload.get("credits", 0))

if not event_id or not target_user_id or credits_delta <= 0:
    Bot.setWebhookResponse({"accepted": False, "error": "invalid_payload"})
    raise StopExecution()

# 3. Idempotency guard — ignore duplicate webhook deliveries safely
processed_events = Bot.fetchData("processed_webhook_events") or []
if event_id in processed_events:
    Bot.setWebhookResponse({"accepted": True, "duplicate": True, "event_id": event_id})
    raise StopExecution()

processed_events.append(event_id)
# Keep bounded history of the most recent 500 event IDs
if len(processed_events) > 500:
    processed_events = processed_events[-500:]
Bot.storeData("processed_webhook_events", processed_events)

# 4. Credit user balance in Bot-level storage and notify user
balance_key = f"credits_{target_user_id}"
new_balance = (Bot.fetchData(balance_key) or 0) + credits_delta
Bot.storeData(balance_key, new_balance)

try:
    Bot.sendMessage(
        chat_id=target_user_id,
        text=(
            "✅ <b>Payment Confirmed!</b>\n\n"
            f"Added: <b>+{credits_delta} credits</b>\n"
            f"New Balance: <b>{new_balance} credits</b>"
        ),
        parse_mode="HTML",
    )
except Exception:
    # Delivery failure on Telegram should not fail webhook acknowledgement
    pass

# 5. Return synchronous JSON result directly to the HTTP caller
Bot.setWebhookResponse({
    "accepted": True,
    "duplicate": False,
    "event_id": event_id,
    "new_balance": new_balance,
})
```

### Command: /trigger_report

```tbs
user_id = message.from_user.id
topic = params.strip() if params else "weekly-summary"

# Dispatch a long-running (>120s) external API request without blocking
job = Request.post(
    "https://api.example.com/v1/reports/generate",
    headers={"Authorization": f"Bearer {EXTERNAL_API_KEY}"},
    json={"user_id": user_id, "topic": topic},
    timeout=240,
    fallback_command="/handle_report_result",
)

Bot.sendMessage(
    "⏳ <b>Report queued!</b>\n\n"
    f"Topic: <code>{topic}</code>\n"
    "We will message you automatically as soon as generation completes.",
    parse_mode="HTML",
)
```

### Command: /handle_report_result

```tbs
# Triggered automatically when the long-running Request.post finishes
response_data = options.response if hasattr(options, "response") else {}
status_code = response_data.get("status_code", 0)

if status_code == 200:
    body = response_data.get("json", {})
    report_url = body.get("download_url", "Unavailable")
    Bot.sendMessage(
        "✅ <b>Your report is ready!</b>\n\n"
        f"🔗 Download: {report_url}",
        parse_mode="HTML",
    )
else:
    Bot.sendMessage(
        "⚠️ Report generation failed on the upstream service. Please try again shortly."
    )
```

## Execution Flow

```
Inbound Webhook (/webhook_payment):
1. External service POSTs JSON + X-Webhook-Signature header to TBS webhook URL
2. Command reads options.headers, options.ip, and raw payload
3. Lib.Security.verifyHMAC validates authenticity against WEBHOOK_SECRET
   - Invalid signature → Bot.setWebhookResponse({"accepted": False, ...}) → StopExecution
4. Checks event_id against bounded processed_webhook_events list in Bot.fetchData
   - Duplicate retry → Bot.setWebhookResponse({"accepted": True, "duplicate": True}) → StopExecution
5. Updates user balance in Bot.storeData and notifies user via Bot.sendMessage
6. Calls Bot.setWebhookResponse({"accepted": True, ...}) so caller receives immediate HTTP 200 JSON

Outbound Long-Running Request (/trigger_report -> /handle_report_result):
1. User sends /trigger_report sales-q4
2. Bot dispatches Request.post(..., timeout=240, fallback_command="/handle_report_result")
3. Request returns immediately with processing status; user gets instant confirmation
4. When external service completes, TBS invokes /handle_report_result with response details in options
5. Bot sends final report link (or clean error notice) to the user
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `Lib.Security.verifyHMAC` | Verify webhook HMAC-SHA256 signatures safely |
| `Bot.setWebhookResponse` | Return synchronous JSON data to the HTTP webhook caller |
| `Request.post` | Send outbound HTTP POST with `timeout` and `fallback_command` |
| `Bot.fetchData` / `Bot.storeData` | Persist processed webhook IDs and user balances across sessions |
| `Bot.sendMessage` | Notify Telegram users of payment receipt and async job completion |

## Best Practices

- Store `WEBHOOK_SECRET` and `EXTERNAL_API_KEY` in TeleBot Studio's **Env** tab rather than hardcoding them in command source
- Always verify signatures **before** trusting user IDs or amounts inside webhook payloads
- Make every webhook handler idempotent using a unique `event_id` — payment gateways retry webhooks whenever networks hiccup
- Bound your stored `processed_events` list (e.g., last 500 IDs) so bot storage stays compact
- Wrap `Bot.sendMessage` inside webhook commands in `try/except` so a user blocking the bot never causes webhook acknowledgment to fail

## Common Mistakes

- **Mistake**: Trusting webhook JSON without checking `options.headers` signature → **Fix**: Always validate with `Lib.Security.verifyHMAC` (or `Lib.Security.verifyPaymentGatewayWebhook`) first and `raise StopExecution()` on mismatch
- **Mistake**: Checking only exact casing `options.headers["X-Webhook-Signature"]` → **Fix**: Proxies normalize HTTP headers to lowercase; check lowercase first with fallback
- **Mistake**: Using `User.storeData` inside an external webhook to credit a target user → **Fix**: External webhooks execute outside the target user's interactive chat session; store cross-user balances in `Bot.storeData(f"credits_{user_id}", ...)`
- **Mistake**: Calling slow 3-minute external APIs synchronously without `fallback_command` → **Fix**: Pass `timeout=240, fallback_command="/handle_..."` so execution never blocks or times out

## Related Patterns

- [Referral & Reward System](../commerce/referral-reward-system.md) — cross-user balance storage with `Bot.storeData`
- [Admin Dashboard with Broadcast & Maintenance Mode](../admin/admin-dashboard-broadcast.md) — owner notifications and system state

## Search Keywords

webhook, payment webhook, HMAC verification, verifyHMAC, signHMAC, Lib.Security, setWebhookResponse, synchronous webhook response, options.headers, options.ip, fallback_command, long-running HTTP request, Request.post, idempotency, external API integration

## User Prompts This Pattern Solves

- "How do I receive and verify payment webhooks in TeleBot Studio?"
- "How do I return a JSON response directly from a webhook command?"
- "How do I check webhook HMAC signatures with Lib.Security?"
- "How do I call a slow external API that takes more than 2 minutes?"
- "How do I read HTTP headers and caller IP inside a webhook command?"
