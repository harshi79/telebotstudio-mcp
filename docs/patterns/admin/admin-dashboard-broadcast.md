---
title: Admin Dashboard with Broadcast & Maintenance Mode
category: admin
difficulty: intermediate
keywords: admin panel, admin dashboard, broadcast, maintenance mode, user tracking, statistics, admin only, access control, forwardMessage, Bot.fetchData, Bot.storeData, User.fetchData, User.storeData, StopExecution, callback handler, inline keyboard
commands: /admin, /start, /handler_callback_query, * (wildcard)
callback_handlers: admin_stats, admin_broadcast, admin_maintenance, admin_settings, admin_back, admin_close
tags: admin, dashboard, broadcast, maintenance, stats, access-control, user-tracking
verified: false
tested_with:
last_updated: 2025-07-01
---

# Admin Dashboard with Broadcast & Maintenance Mode

## Purpose

A complete admin panel pattern with owner-only access control, broadcast messaging with forward support, real-time user statistics, maintenance mode toggle, and a wildcard command interceptor that handles broadcast input and maintenance blocking.

## When to Use

- Your bot needs an owner-only admin dashboard
- You want to broadcast messages to all registered users
- You need a maintenance mode that blocks non-admin users from all commands
- You want to track total registered users and use that data for stats and broadcasts
- You need a single callback handler that manages multiple admin sub-menus

Do NOT use this pattern for:
- Multi-admin or role-based access — this uses a single hardcoded admin ID
- Scheduled broadcasts — this only sends immediately
- Broadcast with custom text composition — this forwards whatever the admin sends

## Features

- Owner-only access control via hardcoded Telegram user ID
- Admin dashboard with inline keyboard navigation
- Broadcast system using `forwardMessage` (preserves photos, formatting, documents)
- Broadcast state machine: tap broadcast button → send any message → it forwards to all users
- `/cancel` abort during broadcast input
- Maintenance mode toggle that blocks all non-admin users across all commands
- User tracking via `/start` — registers every new user for stats and broadcast lists
- Wildcard `*` command that intercepts broadcast input and maintenance checks
- Delete-and-resend pattern for clean menu updates

## Commands

| Command | Description |
|:---|:---|
| `/admin` | Opens the admin dashboard (owner only) |
| `/start` | Registers the user and shows welcome message (respects maintenance mode) |
| `/handler_callback_query` | Handles all `admin_*` callback buttons |
| `*` (wildcard) | Intercepts broadcast input and maintenance mode for all other messages |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `admin_stats` | Shows total registered user count |
| `admin_broadcast` | Enters broadcast state — next message from admin gets forwarded to all users |
| `admin_maintenance` | Toggles maintenance mode on/off |
| `admin_settings` | Placeholder for system settings |
| `admin_back` | Returns to the main dashboard |
| `admin_close` | Deletes the dashboard message |

## Complete Working Code

### Command: /admin

```tbs
ADMIN_ID = 7728424218 # 🛠 REPLACE WITH YOUR TELEGRAM ID

# Secure Verification
if message.from_user.id != ADMIN_ID:
    Bot.sendMessage("⛔ <b>Access Denied:</b> You are not authorized to use this command.", parse_mode="HTML")
    raise StopExecution()

# Clear any lingering admin states
User.storeData("admin_state", None)

text = "👑 <b>Master Admin Dashboard</b>\n\nWelcome back! Select an operation below:"

markup = {
    "inline_keyboard": [
        [{"text": "📊 Statistics", "callback_data": "admin_stats"}, {"text": "📢 Broadcast", "callback_data": "admin_broadcast"}],
        [{"text": "🛠 Maintenance Mode", "callback_data": "admin_maintenance"}],
        [{"text": "⚙️ System Settings", "callback_data": "admin_settings"}],
        [{"text": "❌ Close Dashboard", "callback_data": "admin_close"}]
    ]
}

Bot.sendMessage(text, parse_mode="HTML", reply_markup=markup)
```

### Command: /start

```tbs
# 1. MAINTENANCE MODE CHECK
ADMIN_ID = 7728424218 # 🛠 REPLACE WITH YOUR TELEGRAM ID
is_maintenance = Bot.fetchData("maintenance_mode")

if is_maintenance and message.from_user.id != ADMIN_ID:
    Bot.sendMessage("🛠 <b>Maintenance Mode</b>\n\nThe bot is currently undergoing upgrades. Please check back later!", parse_mode="HTML")
    raise StopExecution()

# 2. USER TRACKING FOR ADMIN STATS & BROADCASTS
user_list = Bot.fetchData("all_users") or []
if message.from_user.id not in user_list:
    user_list.append(message.from_user.id)
    Bot.storeData("all_users", user_list)
    Bot.storeData("total_users", len(user_list))

# 3. NORMAL BOT WELCOME MESSAGE
welcome_text = f"👋 Hello {message.from_user.first_name}!\n\nWelcome to the bot."
Bot.sendMessage(welcome_text)
```

### Command: * (Wildcard)

```tbs
ADMIN_ID = 7728424218 # 🛠 REPLACE WITH YOUR TELEGRAM ID

# 1. MAINTENANCE INTERCEPTOR
is_maintenance = Bot.fetchData("maintenance_mode")
if is_maintenance and message.from_user.id != ADMIN_ID:
    Bot.sendMessage("🛠 The bot is currently in maintenance mode. Please check back later.")
    raise StopExecution()

# 2. BROADCAST LISTENER
admin_state = User.fetchData("admin_state")

if message.from_user.id == ADMIN_ID and admin_state == "wait_for_broadcast":
    # Allow the admin to abort
    if message.text == "/cancel":
        User.storeData("admin_state", None)
        Bot.sendMessage("❌ Broadcast aborted safely.")
        raise StopExecution()

    # Execute the broadcast loop
    user_list = Bot.fetchData("all_users") or []
    success_count = 0

    # Notify admin that processing has started
    status_msg = Bot.sendMessage(f"⏳ Broadcasting to {len(user_list)} users... Please wait.")

    for uid in user_list:
        try:
            Bot.forwardMessage(chat_id=uid, from_chat_id=message.chat.id, message_id=message.message_id)
            success_count += 1
        except Exception as e:
            pass

    # Clear the state and report completion
    User.storeData("admin_state", None)

    try:
        Bot.deleteMessage(message.chat.id, status_msg.message_id)
    except:
        pass

    Bot.sendMessage(f"✅ <b>Broadcast Complete!</b>\n\nSuccessfully delivered to {success_count} out of {len(user_list)} users.", parse_mode="HTML")
    raise StopExecution()

# (Put your normal fallback or general bot logic below this line)
```

### Command: /handler_callback_query

```tbs
ADMIN_ID = 7728424218 # 🛠 REPLACE WITH YOUR TELEGRAM ID

payload = str(call.data)
callback_id = call.id
msg_id = message.message_id
chat_id = message.chat.id

# ONLY process callbacks starting with "admin_"
if payload.startswith("admin_"):

    if chat_id != ADMIN_ID:
        Bot.answerCallbackQuery(callback_id, text="⛔ You do not have admin permissions.", show_alert=True)
        raise StopExecution()

    Bot.answerCallbackQuery(callback_id)

    if payload == "admin_stats":
        total_users = Bot.fetchData("total_users") or 0
        text = (
            "📊 <b>Platform Statistics</b>\n\n"
            f"👥 <b>Total Registered Users:</b> {total_users}\n\n"
            "<i>Metrics are updated in real-time.</i>"
        )
        markup = {"inline_keyboard": [[{"text": "⬅️ Back to Dashboard", "callback_data": "admin_back"}]]}

    elif payload == "admin_broadcast":
        User.storeData("admin_state", "wait_for_broadcast")
        text = (
            "📢 <b>Broadcast Wizard</b>\n\n"
            "Please send the message (text, photo, or document) you want to broadcast to all users right now.\n\n"
            "<i>To cancel, simply type <b>/cancel</b></i>"
        )
        markup = None

    elif payload == "admin_maintenance":
        current_state = Bot.fetchData("maintenance_mode")
        new_state = True if not current_state else False
        Bot.storeData("maintenance_mode", new_state)

        status = "ON 🔴 (Bot Locked)" if new_state else "OFF 🟢 (Bot Active)"
        text = f"🛠 <b>Maintenance Mode</b>\n\nCurrent Status: <b>{status}</b>\n\nWhen activated, standard users cannot interact with the bot commands."

        markup = {
            "inline_keyboard": [
                [{"text": "🔄 Toggle Maintenance", "callback_data": "admin_maintenance"}],
                [{"text": "⬅️ Back to Dashboard", "callback_data": "admin_back"}]
            ]
        }

    elif payload == "admin_settings":
        text = "⚙️ <b>System Settings</b>\n\n(Configure your platform-specific variables here)."
        markup = {"inline_keyboard": [[{"text": "⬅️ Back to Dashboard", "callback_data": "admin_back"}]]}

    elif payload == "admin_back":
        User.storeData("admin_state", None)
        text = "👑 <b>Master Admin Dashboard</b>\n\nWelcome back! Select an operation below:"
        markup = {
            "inline_keyboard": [
                [{"text": "📊 Statistics", "callback_data": "admin_stats"}, {"text": "📢 Broadcast", "callback_data": "admin_broadcast"}],
                [{"text": "🛠 Maintenance Mode", "callback_data": "admin_maintenance"}],
                [{"text": "⚙️ System Settings", "callback_data": "admin_settings"}],
                [{"text": "❌ Close Dashboard", "callback_data": "admin_close"}]
            ]
        }

    elif payload == "admin_close":
        User.storeData("admin_state", None)
        try:
            Bot.deleteMessage(chat_id, msg_id)
        except:
            pass
        raise StopExecution()

    # DELETE OLD & SEND NEW
    if payload != "admin_close":
        try:
            Bot.deleteMessage(chat_id, msg_id)
        except:
            pass

        Bot.sendMessage(
            text=text,
            parse_mode="HTML",
            reply_markup=markup
        )
```

## Execution Flow

```
/start:
1. Check maintenance mode — if ON and user is not admin, block with message
2. Register user in all_users list (if new)
3. Update total_users counter
4. Send welcome message

/admin:
1. Verify message.from_user.id == ADMIN_ID — if not, deny access
2. Clear any lingering admin_state
3. Render dashboard with inline keyboard (stats, broadcast, maintenance, settings, close)

Broadcast flow:
1. Admin taps 📢 Broadcast → callback sets admin_state = "wait_for_broadcast"
2. Dashboard shows "send your message" prompt
3. Admin sends any message (text, photo, document)
4. Wildcard * command detects admin_state == "wait_for_broadcast"
5. Bot sends "Broadcasting..." status message
6. Loop through all_users, forwardMessage to each
7. Delete the status message
8. Report success count vs total
9. Clear admin_state

Maintenance mode flow:
1. Admin taps 🛠 Maintenance Mode
2. Bot.fetchData("maintenance_mode") → toggle True/False
3. Bot.storeData("maintenance_mode", new_state)
4. /start and * commands check this flag and block non-admins

Dashboard navigation:
1. Admin taps any sub-menu → old message deleted, new one sent
2. Admin taps ⬅️ Back → returns to main dashboard
3. Admin taps ❌ Close → deletes the dashboard message entirely
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `Bot.sendMessage` | Send dashboard, stats, and status messages |
| `Bot.deleteMessage` | Remove old menu messages and status indicators |
| `Bot.forwardMessage` | Forward admin's message to all users during broadcast |
| `Bot.answerCallbackQuery` | Acknowledge inline button presses |
| `Bot.fetchData` | Read maintenance mode, user list, total users |
| `Bot.storeData` | Write maintenance mode, user list, total users |
| `User.fetchData` | Read admin state (broadcast waiting) |
| `User.storeData` | Write admin state and clear it after broadcast |

## Best Practices

- Always check `message.from_user.id` against your admin ID at the top of every admin command — never rely on callback data alone for authorization
- Use `Bot.forwardMessage` for broadcasts instead of copying text — it preserves photos, formatting, files, and any media the admin sends
- Track users in `/start` using `Bot.fetchData`/`Bot.storeData` — this gives you both a user list for broadcasts and a count for stats
- Clear `admin_state` when returning to the dashboard or closing — stale states cause unexpected behavior
- Use `try/except` around `Bot.deleteMessage` — the message may already be deleted by the user or Telegram
- Check maintenance mode in both `/start` and the `*` wildcard — this ensures every entry point is covered

## Common Mistakes

- **Mistake**: Using `call.from_user.id` for callback authorization instead of `chat_id` → **Fix**: Use `chat_id` (which is `message.chat.id`) — in group chats, `call.from_user.id` may differ from the chat where the button was pressed
- **Mistake**: Not clearing `admin_state` when the admin navigates away from broadcast → **Fix**: Always clear `admin_state` in `admin_back` and `admin_close` handlers
- **Mistake**: Only checking maintenance mode in `/start` → **Fix**: Also check in the `*` wildcard command — users can reach your bot through any command, not just `/start`
- **Mistake**: Using `Api.sendMessage` instead of `Bot.sendMessage` in callbacks → **Fix**: Use `Bot.sendMessage` inside `/handler_callback_query` for correct chat context
- **Mistake**: Not handling broadcast failures silently → **Fix**: Wrap `forwardMessage` in try/except — users who blocked the bot will throw errors, and that's expected

## Related Patterns

- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — the menu navigation pattern used by this dashboard
- [TEMPLATE.md](../TEMPLATE.md) — the standard pattern template

## Search Keywords

admin panel, admin dashboard, broadcast message, maintenance mode, user tracking, statistics, admin only, access control, forwardMessage, Bot.fetchData, Bot.storeData, User.storeData, admin_state, all_users, total_users, wildcard command, owner only, admin callback, broadcast wizard, toggle maintenance, close dashboard, admin statistics, user registration tracking

## User Prompts This Pattern Solves

- "How do I make an admin panel for my bot?"
- "How do I broadcast a message to all my bot users?"
- "Can I add maintenance mode to my bot?"
- "How do I track how many users my bot has?"
- "How do I restrict commands to the bot owner only?"
- "How do I forward a message to all users in TeleBot Studio?"
- "How do I make a broadcast system with cancel support?"
- "How do I block users from using the bot during maintenance?"
