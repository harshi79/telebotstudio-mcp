---
title: Conversation State Machine with TTL & Rate Guard
category: systems
difficulty: intermediate
keywords: state machine, session timeout, TTL, rate limit, cooldown, throttle, middleware guard, error handler, Bot.errorID, User.storeData, User.fetchData, Lib.DateTime, wildcard, cancel, StopExecution
commands: /ticket, /cancel, * (wildcard)
callback_handlers: ticket_priority_low, ticket_priority_high
tags: systems, state-machine, ttl, session, rate-limit, cooldown, error-handling, middleware
verified: false
tested_with:
last_updated: 2026-10-20
---

# Conversation State Machine with TTL & Rate Guard

## Purpose

Provides reusable infrastructure guards for multi-turn bots: a conversation state machine that automatically expires stale sessions after a configurable TTL, per-user rate throttling to prevent command spam, global slash-command escape handling, and structured exception logging with `Bot.errorID()`.

## When to Use

- Your bot uses `*` (wildcard) handlers and users sometimes abandon flows halfway through and come back hours later expecting normal chat behavior
- You need per-user cooldown protection to stop rapid command spamming
- Multiple commands share a clean state envelope (`step`, `data`, `updated_at`) instead of scattered ad-hoc keys
- You want unexpected runtime errors caught cleanly with reference IDs rather than silent failures

Do NOT use this pattern for:
- Stateless single-command bots with no multi-step input or rate-sensitive endpoints
- Cross-user global rate limits across all users simultaneously — store global counters in `Bot.storeData` instead of `User.storeData`

## Features

- **Structured session envelope**: Stores `step`, `payload`, and `updated_at` timestamp together under `session_state`
- **Automatic TTL expiration**: Expired sessions (default 10 minutes) clear themselves transparently instead of trapping users in stale states
- **Per-user rate throttle**: Rejects bursts faster than `COOLDOWN_SECONDS` before running heavy logic
- **Slash-command escape hatch**: Typing `/cancel` aborts cleanly, and typing another `/command` clears stale wizard state instead of capturing the slash command as text input
- **Structured error boundary**: Catches unexpected errors and surfaces `Bot.errorID()` so operators can correlate user reports with logs

## Commands

| Command | Description |
|:---|:---|
| `/ticket` | Rate-guarded entry command that initializes a TTL-tracked support ticket session |
| `/cancel` | Clears any active conversation session immediately |
| `*` (wildcard) | Central state router with TTL check, slash-command escape, and error boundary |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `ticket_priority_low` | Finalizes ticket with Low priority and clears session state |
| `ticket_priority_high` | Finalizes ticket with High priority and clears session state |

## Complete Working Code

### Command: /ticket

```tbs
import time

COOLDOWN_SECONDS = 5
now_ts = int(time.time())

# 1. Per-user rate limit guard
last_action_ts = User.fetchData("last_ticket_cmd_ts") or 0
if now_ts - last_action_ts < COOLDOWN_SECONDS:
    wait_left = COOLDOWN_SECONDS - (now_ts - last_action_ts)
    Bot.sendMessage(f"⏳ Slow down! Please wait {wait_left}s before opening another ticket.")
    raise StopExecution()

User.storeData("last_ticket_cmd_ts", now_ts)

# 2. Initialize structured session state with timestamp for TTL checks
session = {
    "flow": "support_ticket",
    "step": "awaiting_subject",
    "payload": {},
    "updated_at": now_ts,
}
User.storeData("session_state", session)

Bot.sendMessage(
    "🎫 <b>New Support Ticket</b>\n\n"
    "<b>Step 1/2:</b> Briefly describe your issue subject.\n"
    "<i>Session expires automatically after 10 minutes of inactivity. Send /cancel anytime.</i>",
    parse_mode="HTML",
)
```

### Command: /cancel

```tbs
session = User.fetchData("session_state")
if session:
    User.storeData("session_state", None)
    Bot.sendMessage("❌ Active session canceled. How can I help you next?")
else:
    Bot.sendMessage("ℹ️ You have no active operation in progress.")
```

### Command: * (Wildcard)

```tbs
import time

SESSION_TTL_SECONDS = 600  # 10 minutes
now_ts = int(time.time())
session = User.fetchData("session_state")

if session:
    try:
        user_text = (message.text or "").strip()

        # 1. TTL Expiration Guard — never trap returning users in stale flows
        updated_at = int(session.get("updated_at", 0))
        if now_ts - updated_at > SESSION_TTL_SECONDS:
            User.storeData("session_state", None)
            Bot.sendMessage(
                "⌛ Your previous session expired due to inactivity. Please run /ticket to start again."
            )
            raise StopExecution()

        # 2. Explicit Cancel or Slash Command Escape Guard
        if user_text == "/cancel":
            User.storeData("session_state", None)
            Bot.sendMessage("❌ Session canceled.")
            raise StopExecution()

        if user_text.startswith("/"):
            # Do not swallow unrelated slash commands as form text
            User.storeData("session_state", None)
            raise StopExecution()

        if not user_text:
            Bot.sendMessage("⚠️ Please send a text message or type /cancel to exit.")
            raise StopExecution()

        # 3. State Transition Table (before_state -> validation -> after_state)
        step = session.get("step")
        payload = session.get("payload", {})

        if step == "awaiting_subject":
            if len(user_text) < 5:
                Bot.sendMessage("⚠️ Subject must be at least 5 characters. Try again:")
                raise StopExecution()

            payload["subject"] = user_text
            session["payload"] = payload
            session["step"] = "awaiting_priority"
            session["updated_at"] = now_ts
            User.storeData("session_state", session)

            markup = {
                "inline_keyboard": [
                    [
                        {"text": "🟢 Normal Priority", "callback_data": "ticket_priority_low"},
                        {"text": "🔴 Urgent Priority", "callback_data": "ticket_priority_high"},
                    ]
                ]
            }
            Bot.sendMessage(
                "<b>Step 2/2:</b> Select ticket priority below:",
                parse_mode="HTML",
                reply_markup=markup,
            )
            raise StopExecution()

        elif step == "awaiting_priority":
            Bot.sendMessage("⚠️ Please select a priority button above, or send /cancel.")
            raise StopExecution()

    except StopExecution:
        raise
    except Exception as e:
        err_id = Bot.errorID()
        User.storeData("session_state", None)
        Bot.sendMessage(
            f"⚠️ Something went wrong (Ref: <code>{err_id}</code>). Your session was reset safely.",
            parse_mode="HTML",
        )
        raise StopExecution()
```

### Command: /handler_callback_query

```tbs
payload_cb = str(call.data)

if payload_cb in ("ticket_priority_low", "ticket_priority_high"):
    Bot.answerCallbackQuery(call.id)
    session = User.fetchData("session_state")

    if not session or session.get("step") != "awaiting_priority":
        Bot.editMessageText(
            "⌛ This ticket session is no longer active. Run /ticket to open a new one.",
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
        raise StopExecution()

    priority = "URGENT" if payload_cb.endswith("high") else "NORMAL"
    subject = session["payload"]["subject"]

    # Commit ticket and clear session atomically
    tickets = Bot.fetchData("open_tickets") or []
    ticket_id = len(tickets) + 1001
    tickets.append({
        "id": ticket_id,
        "user_id": call.from_user.id,
        "subject": subject,
        "priority": priority,
    })
    Bot.storeData("open_tickets", tickets)
    User.storeData("session_state", None)

    Bot.editMessageText(
        f"✅ <b>Ticket #{ticket_id} Created</b>\n\n"
        f"• <b>Priority:</b> {priority}\n"
        f"• <b>Subject:</b> {subject}",
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode="HTML",
    )
    raise StopExecution()
```

## Execution Flow

```
State Transitions:
  None ──(/ticket, cooldown OK)──▶ awaiting_subject (updated_at = now)
  awaiting_subject ──(text >= 5 chars)──▶ awaiting_priority (updated_at = now)
  awaiting_priority ──(priority callback)──▶ None (ticket saved to Bot.storeData)
  ANY active state ──(inactivity > 600s | /cancel | unhandled Exception)──▶ None

Error & Edge Paths:
1. Burst spam (/ticket twice within 5s) → blocked immediately with remaining cooldown seconds
2. Abandoned flow (user returns 2 hours later) → wildcard sees now - updated_at > 600 → clears state gracefully
3. Non-text message (sticker/photo during text prompt) → guarded via (message.text or "").strip()
4. Stale inline button clicked after session reset → callback verifies session.step == "awaiting_priority"
5. Unexpected exception → re-raises StopExecution directly, otherwise logs Bot.errorID() and resets session_state
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `User.fetchData` / `User.storeData` | Read/write per-user session state and rate-limit timestamps |
| `Bot.fetchData` / `Bot.storeData` | Persist created support tickets globally |
| `Bot.errorID` | Generate correlation ID when unexpected exceptions occur |
| `Bot.sendMessage` / `Bot.editMessageText` | Prompt user and update confirmation messages cleanly |
| `Bot.answerCallbackQuery` | Acknowledge inline priority button presses |

## Best Practices

- Always re-raise `StopExecution` explicitly (`except StopExecution: raise`) before any broad `except Exception:` block — otherwise your error handler catches intentional flow exits!
- Refresh `session["updated_at"]` on every valid step transition so active users never time out mid-flow
- Verify `session` state inside `/handler_callback_query` before committing data — users can click old inline buttons days later
- Guard `message.text` with `(message.text or "")` because stickers, photos, and voice notes have `message.text == None`

## Common Mistakes

- **Mistake**: Wrapping command code in `try ... except Exception:` without `except StopExecution: raise` first → **Fix**: `StopExecution` inherits from `Exception`; catching it triggers false error messages unless re-raised first
- **Mistake**: Storing multi-step wizard fields without an expiration timestamp → **Fix**: Store `updated_at` in a single `session_state` dict and expire stale sessions in `*`
- **Mistake**: Letting wildcard `*` treat `/help` or `/menu` as text input for the current step → **Fix**: Check `if user_text.startswith("/"):` in your wildcard guard

## Related Patterns

- [Multi-Step Form Wizard](../ui/multi-step-form-wizard.md) — UI-focused multi-step form collection
- [User Profile Storage with Edit & Delete](../storage/user-profile-storage.md) — per-user profile state transitions

## Search Keywords

state machine, session state, TTL expiration, session timeout, cooldown, rate limiting, throttle, StopExecution, Bot.errorID, error boundary, middleware guard, wildcard routing, stale callback protection

## User Prompts This Pattern Solves

- "How do I prevent users from getting stuck in a wizard state forever?"
- "How do I add a timeout or TTL to conversation state in TeleBot Studio?"
- "How do I rate-limit or add a cooldown to a command per user?"
- "Why does try/except catch StopExecution in my command?"
- "How do I build a clean state machine with error handling in TBS?"
