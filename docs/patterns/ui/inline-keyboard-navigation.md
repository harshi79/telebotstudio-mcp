---
title: Inline Keyboard Navigation System
category: ui
difficulty: intermediate
keywords: inline keyboard, callback handler, navigation, menu, back button, callback_data, reply_markup, answerCallbackQuery, StopExecution
commands: /menu, /handler_callback_query
callback_handlers: nav_features, nav_settings, nav_stats, nav_support, nav_ai_hub, nav_crypto_hub, sys_home, sys_back, sys_refresh, act_toggle_alerts, act_run_gpt, act_run_gemini, act_pay_ton, act_pay_evm
tags: navigation, menu, inline, callback, multi-level, back-button
verified: false
tested_with:
last_updated: 2025-07-01
---

# Inline Keyboard Navigation System

## Purpose

A complete multi-level inline keyboard navigation framework with back button, home button, and action dispatching — the standard pattern for any bot with nested menus.

## When to Use

- Your bot needs a multi-level menu system (main → sub-menu → sub-sub-menu)
- Users need to navigate back and return home from any depth
- Different callback actions need different handling (navigation vs. system vs. user actions)
- You want to delete the old menu message and send a fresh one instead of editing in place

Do NOT use this pattern for:
- Single-level menus with no navigation — use a simple inline keyboard instead
- Edit-based menu updates — this pattern deletes and resends

## Features

- Multi-level nested navigation with unlimited depth
- Back button that walks up the navigation history
- Home button that resets to root instantly
- Three callback prefix types: `nav_`, `sys_`, `act_` for clean dispatch
- Dynamic data injection (e.g. live stats, toggle states)
- URL buttons (links to groups/channels)
- Menu message replacement (delete old → send new) to avoid chat spam
- `StopExecution` to halt when an action doesn't need a menu re-render

## Commands

| Command | Description |
|:---|:---|
| `/menu` | Initializes navigation state and renders the root menu |
| `/handler_callback_query` | Central dispatcher for all inline button callbacks |

## Callback Handlers

| Callback Pattern | Type | Description |
|:---|:---|:---|
| `nav_<menu_id>` | Navigation | Navigates to the specified sub-menu |
| `sys_home` | System | Resets to the main menu, clears history |
| `sys_back` | System | Pops history stack and returns to previous menu |
| `sys_refresh` | System | Re-renders the current menu (for dynamic data) |
| `act_<action_id>` | Action | Executes a feature action (e.g. toggle, launch) |

## Complete Working Code

### Command: /menu

```tbs
# Clear any previous navigation state to ensure a clean entry point
User.storeData("current_menu", "main")
User.storeData("menu_history", [])

# Define the root-level welcome layout text
welcome_text = (
    "🗂 <b>enterprise main menu</b>\n\n"
    "welcome to the optimized inline navigation framework.\n"
    "use the buttons below to browse nested categories."
)

# Build the initial root keyboard structure using standard TBS markup format
markup = {
    "inline_keyboard": [
        [
            {"text": "🚀 features", "callback_data": "nav_features"},
            {"text": "⚙️ settings", "callback_data": "nav_settings"}
        ],
        [
            {"text": "📊 statistics", "callback_data": "nav_stats"}
        ],
        [
            {"text": "ℹ️ help & support", "callback_data": "nav_support"}
        ]
    ]
}

# Distribute the message cleanly to the current interacting chat
Api.sendMessage(
    text=welcome_text,
    parse_mode="HTML",
    reply_markup=markup
)
```

### Command: /handler_callback_query

```tbs
# ------------------------------------------
# PART A: THE CENTRAL MENU REPOSITORY
# ------------------------------------------
menus = {
    "main": {
        "text": "🗂 <b>enterprise main menu</b>\n\nwelcome to the optimized inline navigation framework.\nuse the buttons below to browse nested categories.",
        "buttons": [
            [{"text": "🚀 features", "data": "nav_features"}, {"text": "⚙️ settings", "data": "nav_settings"}],
            [{"text": "📊 statistics", "data": "nav_stats"}],
            [{"text": "ℹ️ help & support", "data": "nav_support"}]
        ]
    },
    "features": {
        "text": "🚀 <b>features menu</b>\n\nexplore automated application interfaces engineered natively within telebot studio:",
        "buttons": [
            [{"text": "🧠 ai agent modules", "data": "nav_ai_hub"}],
            [{"text": "🪙 crypto settlement", "data": "nav_crypto_hub"}],
            [{"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    },
    "ai_hub": {
        "text": "🧠 <b>ai intelligence core</b>\n\nselect an integrated model interface to process context:",
        "buttons": [
            [{"text": "🤖 run gpt-4o", "data": "act_run_gpt"}, {"text": "🔮 run gemini flash", "data": "act_run_gemini"}],
            [{"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    },
    "crypto_hub": {
        "text": "🪙 <b>crypto settlement matrix</b>\n\ntribute or evaluate ledger allocations using our system infrastructure:",
        "buttons": [
            [{"text": "💎 request ton payment", "data": "act_pay_ton"}, {"text": "⛓ request evm transaction", "data": "act_pay_evm"}],
            [{"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    },
    "settings": {
        "text": "⚙️ <b>system configurations</b>\n\ntweak profile environment data values instantly:",
        "buttons": [
            [{"text": "🔔 toggle system alerts", "data": "act_toggle_alerts"}],
            [{"text": "🔄 refresh state", "data": "sys_refresh"}, {"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    },
    "stats": {
        "text": "📊 <b>live metric logs</b>\n\nthis menu queries dynamic operational data on each refresh:\n\n",
        "buttons": [
            [{"text": "🔄 pull live metrics", "data": "sys_refresh"}],
            [{"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    },
    "support": {
        "text": "ℹ️ <b>knowledge base & support</b>\n\naccess documentation portals or join our live community chat environment:",
        "buttons": [
            [{"text": "💬 global help group", "data": "url_https://t.me/TeleBotStudioChat"}],
            [{"text": "🏠 home", "data": "sys_home"}, {"text": "⬅️ back", "data": "sys_back"}]
        ]
    }
}

# ------------------------------------------
# PART B: REQUEST DECONSTRUCTION
# ------------------------------------------
payload = str(call.data)
callback_id = call.id
active_msg_id = message.message_id
active_chat_id = message.chat.id

current_view = User.fetchData("current_menu") or "main"
history_stack = User.fetchData("menu_history") or []

# ------------------------------------------
# PART C: DISPATCHER ROUTING ENGINE
# ------------------------------------------
if payload.startswith("nav_"):
    target_menu = payload.replace("nav_", "")

    if target_menu in menus:
        history_stack.append(current_view)
        User.storeData("menu_history", history_stack)
        User.storeData("current_menu", target_menu)
        current_view = target_menu
        Bot.answerCallbackQuery(callback_id)

elif payload.startswith("sys_"):
    action = payload.replace("sys_", "")

    if action == "home":
        User.storeData("menu_history", [])
        User.storeData("current_menu", "main")
        current_view = "main"
        Bot.answerCallbackQuery(callback_id)

    elif action == "back":
        if len(history_stack) > 0:
            previous_target = history_stack.pop()
            User.storeData("menu_history", history_stack)
            User.storeData("current_menu", previous_target)
            current_view = previous_target
            Bot.answerCallbackQuery(callback_id)
        else:
            Bot.answerCallbackQuery(callback_id, text="⚠️ already at main root menu", show_alert=True)
            raise StopExecution()

    elif action == "refresh":
        Bot.answerCallbackQuery(callback_id, text="🔄 view refreshed!")

elif payload.startswith("act_"):
    action_id = payload.replace("act_", "")

    if action_id == "toggle_alerts":
        alert_state = User.fetchData("alerts_enabled")
        new_state = True if not alert_state else False
        User.storeData("alerts_enabled", new_state)
        status_string = "enabled ✅" if new_state else "disabled ❌"
        Bot.answerCallbackQuery(callback_id, text=f"system alerts are now {status_string}", show_alert=True)

    elif action_id == "run_gpt":
        Bot.answerCallbackQuery(callback_id, text="🧠 initializing ai...", show_alert=True)
        raise StopExecution()

    elif action_id == "run_gemini":
        Bot.answerCallbackQuery(callback_id, text="🔮 compiling gemini...", show_alert=True)
        raise StopExecution()

    elif action_id == "pay_ton":
        Bot.answerCallbackQuery(callback_id, text="💎 generating checkout...", show_alert=True)
        raise StopExecution()

    elif action_id == "pay_evm":
        Bot.answerCallbackQuery(callback_id, text="⛓ generating evm invoice...", show_alert=True)
        raise StopExecution()

# ------------------------------------------
# PART D: ASSET COMPILATION & VIEW MUTATION
# ------------------------------------------
menu_config = menus.get(current_view, menus["main"])
menu_text = str(menu_config["text"])

# Dynamic data injection
if current_view == "stats":
    menu_text += "\n• 🕒 <b>last fetch timestamp:</b> updating...\n\n<i>click pull live metrics below to trigger refresh routines.</i>"

if current_view == "settings":
    is_enabled = User.fetchData("alerts_enabled")
    alert_status = "active status: [ enabled ✅ ]" if is_enabled else "active status: [ disabled ❌ ]"
    menu_text += f"\n👉 <b>alert tracker:</b> {alert_status}"

# Compile the keyboard dictionary
compiled_keyboard = []
for row in menu_config["buttons"]:
    compiled_row = []
    for btn in row:
        if str(btn.get("data", "")).startswith("url_"):
            clean_url = str(btn["data"]).replace("url_", "")
            compiled_row.append({"text": btn["text"], "url": clean_url})
        else:
            compiled_row.append({"text": btn["text"], "callback_data": btn["data"]})
    compiled_keyboard.append(compiled_row)

final_markup = {"inline_keyboard": compiled_keyboard}

# ==========================================
# DELETE OLD & SEND NEW
# ==========================================
try:
    Bot.deleteMessage(active_chat_id, active_msg_id)
except:
    pass

Bot.sendMessage(
    text=menu_text,
    parse_mode="HTML",
    reply_markup=final_markup
)
```

## Execution Flow

```
1. User sends /menu
2. Bot stores "current_menu" = "main" and "menu_history" = []
3. Bot renders the root menu with inline keyboard

4. User taps a nav_ button (e.g. "🚀 features")
5. Bot pushes current view ("main") onto history stack
6. Bot updates "current_menu" = "features"
7. Bot deletes old menu message
8. Bot sends the features menu with back/home buttons

9. User taps ⬅️ back
10. Bot pops "main" from history stack
11. Bot updates "current_menu" = "main"
12. Bot deletes old menu message
13. Bot sends the main menu again

14. User taps 🏠 home
15. Bot clears history stack entirely
16. Bot resets "current_menu" = "main"
17. Bot deletes old menu message
18. Bot sends the main menu

19. User taps an act_ button (e.g. "🔔 toggle alerts")
20. Bot executes the action logic
21. Bot does NOT raise StopExecution → menu re-renders with updated state

22. User taps an act_ button that raises StopExecution (e.g. "🤖 run gpt-4o")
23. Bot shows an alert popup
24. Execution stops — no menu re-render
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `Api.sendMessage` | Send the initial menu message |
| `Bot.answerCallbackQuery` | Acknowledge button press (with optional alert) |
| `Bot.deleteMessage` | Remove the old menu message before sending the new one |
| `Bot.sendMessage` | Send the updated menu (callback handler uses Bot, not Api) |
| `User.storeData` | Persist navigation state across interactions |
| `User.fetchData` | Retrieve navigation state from previous interactions |

## Best Practices

- Always call `Bot.answerCallbackQuery` for every callback — Telegram requires it within 30 seconds or the button shows a spinner
- Use a consistent callback prefix convention (`nav_`, `sys_`, `act_`) to keep the dispatcher readable
- Store menu history as a list so back navigation works at any depth
- Delete old menu messages instead of editing — this avoids "message not modified" errors when the content hasn't changed
- Wrap `Bot.deleteMessage` in try/except — the message may already be deleted by the user or Telegram

## Common Mistakes

- **Mistake**: Forgetting to call `Bot.answerCallbackQuery` → **Fix**: Always answer every callback, even if just `Bot.answerCallbackQuery(callback_id)` with no text
- **Mistake**: Using `Api.sendMessage` in the callback handler instead of `Bot.sendMessage` → **Fix**: Use `Bot.sendMessage` inside `/handler_callback_query` — the `Api` object may not have the correct chat context in callback mode
- **Mistake**: Editing the message instead of delete+send → **Fix**: Edit-based updates fail silently when content is identical; delete+send is more reliable
- **Mistake**: Not initializing `menu_history` as `[]` in the `/menu` command → **Fix**: Always reset both `current_menu` and `menu_history` when the user starts a fresh `/menu`

## Related Patterns

- [TEMPLATE.md](../TEMPLATE.md) — the standard pattern template

## Search Keywords

inline keyboard, callback handler, menu navigation, back button, nested menu, callback_data, answerCallbackQuery, StopExecution, reply_markup, deleteMessage, menu history

## User Prompts This Pattern Solves

- "How do I make an inline keyboard menu with sub-menus?"
- "I want a back button on my bot's inline keyboard"
- "How do I handle callback queries in TeleBot Studio?"
- "Can I build a multi-level navigation system with inline buttons?"
- "How do I delete old menu messages when the user taps a button?"
