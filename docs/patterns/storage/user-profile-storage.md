---
title: User Profile Storage with Edit & Delete
category: storage
difficulty: intermediate
keywords: user profile, profile setup, profile edit, profile delete, store profile, fetch profile, User.storeData, User.fetchData, Bot.sendMessage, Bot.editMessageText, Bot.deleteMessage, Bot.answerCallbackQuery, inline keyboard, state machine, wildcard, multi-step, setup wizard, edit profile, delete confirmation, StopExecution, params, callback_query
commands: /profile, /profile set, /profile clear, * (wildcard), /handler_callback_query
callback_handlers: setup_profile, edit_profile, edit_name, edit_age, edit_country, delete_profile, confirm_delete, back_to_profile
tags: profile, user data, storage, edit, delete, setup, state machine, wizard, inline keyboard, CRUD
verified: false
tested_with:
last_updated: 2025-07-02
---

# User Profile Storage with Edit & Delete

## Purpose

A complete user profile CRUD system — view, create, edit individual fields, and delete with confirmation — all managed through inline keyboard navigation and a state machine for multi-step input collection.

## When to Use

- You need to store per-user profile data (name, age, country, etc.)
- You want users to edit individual fields without re-entering everything
- You need a two-step delete confirmation to prevent accidental data loss
- You want conditional UI — different views for empty vs populated profiles
- You need a setup wizard for first-time profile creation

Do NOT use this pattern for:
- Bot-level data that must be accessible from any user's session — use `Bot.storeData`/`Bot.fetchData` instead
- Simple key-value storage without UI — just use `User.storeData`/`User.fetchData` directly
- Large datasets or lists — this pattern stores a flat profile, not collections

## Features

- **Conditional profile view**: Shows "Setup Profile" button when empty, "Edit/Delete" buttons when populated
- **3-step setup wizard**: name → age → country with step counter
- **Individual field editing**: Edit just one field without touching the others
- **Two-step delete confirmation**: "Are you sure?" prompt before permanent deletion
- **Inline keyboard navigation**: Back button returns to the main profile view
- **State machine**: `profile_state` tracks which field the user is currently entering
- **`/profile clear` shortcut**: Quick command to wipe all profile data
- **Safe message mutations**: All `editMessageText` and `deleteMessage` wrapped in try/except
- **Per-user storage**: All data scoped to the individual user via `User.storeData`/`User.fetchData`

## Commands

| Command | Description |
|:---|:---|
| `/profile` | View current profile (or setup prompt if empty) |
| `/profile set` | Start the 3-step profile setup wizard |
| `/profile clear` | Quick-delete all profile data without confirmation |
| `*` (wildcard) | Capture user input during setup and edit flows |
| `/handler_callback_query` | Handle all inline button callbacks |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `setup_profile` | Start the setup wizard from the empty profile view |
| `edit_profile` | Open the edit menu with field selection buttons |
| `edit_name` | Trigger name editing — sets state to `edit_name` |
| `edit_age` | Trigger age editing — sets state to `edit_age` |
| `edit_country` | Trigger country editing — sets state to `edit_country` |
| `delete_profile` | Show the "Are you sure?" confirmation prompt |
| `confirm_delete` | Permanently wipe all profile data and state |
| `back_to_profile` | Return to the main profile view from any sub-menu |

## Complete Working Code

### Command: /profile

```tbs
# 1. Check if user wants to clear their profile using /profile clear
if params == "clear":
    User.storeData("profile_name", None)
    User.storeData("profile_age", None)
    User.storeData("profile_country", None)
    Bot.sendMessage("🗑️ **Profile cleared.** All your data has been deleted.", parse_mode="Markdown")
    raise StopExecution()

# 2. Fetch the user's current profile data
name = User.fetchData("profile_name")
age = User.fetchData("profile_age")
country = User.fetchData("profile_country")

# 3. Display logic
if not name:
    # Profile is empty
    text = (
        "⚠️ **Profile not set.**\n\n"
        "You haven't set up your profile yet. Use the command `/profile set` or click the button below to start."
    )
    markup = {
        "inline_keyboard": [
            [{"text": "🛠️ Setup Profile", "callback_data": "setup_profile"}]
        ]
    }
    Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
else:
    # Profile exists
    text = (
        "👤 **Your Profile**\n\n"
        f"**Name:** {name}\n"
        f"**Age:** {age}\n"
        f"**Country:** {country}"
    )
    markup = {
        "inline_keyboard": [
            [{"text": "✏️ Edit Profile", "callback_data": "edit_profile"}],
            [{"text": "🗑️ Delete Profile", "callback_data": "delete_profile"}]
        ]
    }
    Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
```

### Command: /profile set

```tbs
# Set the state machine to start the flow
User.storeData("profile_state", "setup_name")

text = (
    "📝 **Profile Setup (Step 1 of 3)**\n\n"
    "Let's get your profile set up! First, what is your **Name**?"
)
Bot.sendMessage(text, parse_mode="Markdown")
```

### Command: /handler_callback_query

```tbs
payload = str(call.data)
cb_id = call.id
msg_id = message.message_id
chat_id = message.chat.id

# 1. Handle Setup Start from Empty Profile
if payload == "setup_profile":
    Bot.answerCallbackQuery(cb_id, text="Starting setup...")
    User.storeData("profile_state", "setup_name")

    try:
        Bot.deleteMessage(chat_id, msg_id)
    except:
        pass

    Bot.sendMessage("📝 **Profile Setup (Step 1 of 3)**\n\nFirst, what is your **Name**?", parse_mode="Markdown")
    raise StopExecution()

# 2. Main Edit Menu
elif payload == "edit_profile":
    Bot.answerCallbackQuery(cb_id)

    text = "✏️ **Edit Profile**\n\nWhich field would you like to update?"
    markup = {
        "inline_keyboard": [
            [{"text": "👤 Name", "callback_data": "edit_name"}, {"text": "🎂 Age", "callback_data": "edit_age"}],
            [{"text": "🌍 Country", "callback_data": "edit_country"}],
            [{"text": "⬅️ Back", "callback_data": "back_to_profile"}]
        ]
    }

    try:
        Bot.editMessageText(text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=markup)
    except:
        pass

    raise StopExecution()

# 3. Individual Edit Triggers
elif payload in ["edit_name", "edit_age", "edit_country"]:
    Bot.answerCallbackQuery(cb_id, text="Awaiting your input...")

    # Store the exact state needed for the wildcard command
    User.storeData("profile_state", payload)

    field_name = payload.replace("edit_", "").capitalize()

    try:
        Bot.deleteMessage(chat_id, msg_id)
    except:
        pass

    Bot.sendMessage(f"✏️ Please type your **new {field_name}** in the chat below:", parse_mode="Markdown")
    raise StopExecution()

# 4. Two-Step Deletion Flow
elif payload == "delete_profile":
    Bot.answerCallbackQuery(cb_id, text="Warning: This is permanent!", show_alert=True)

    text = "⚠️ **Delete Profile**\n\nAre you absolutely sure you want to permanently delete your profile? This cannot be undone."
    markup = {
        "inline_keyboard": [
            [{"text": "✅ Yes, Delete", "callback_data": "confirm_delete"}],
            [{"text": "❌ Cancel", "callback_data": "back_to_profile"}]
        ]
    }

    try:
        Bot.editMessageText(text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=markup)
    except:
        pass

    raise StopExecution()

elif payload == "confirm_delete":
    Bot.answerCallbackQuery(cb_id, text="Profile deleted.", show_alert=True)

    # Wipe all data
    User.storeData("profile_name", None)
    User.storeData("profile_age", None)
    User.storeData("profile_country", None)
    User.storeData("profile_state", None)

    try:
        Bot.editMessageText("🗑️ **Your profile has been permanently deleted.**\n\nYou can use `/profile set` to create a new one.", chat_id=chat_id, message_id=msg_id, parse_mode="Markdown")
    except:
        pass

    raise StopExecution()

# 5. Return to Main Profile View
elif payload == "back_to_profile":
    Bot.answerCallbackQuery(cb_id)

    name = User.fetchData("profile_name")
    age = User.fetchData("profile_age")
    country = User.fetchData("profile_country")

    text = (
        "👤 **Your Profile**\n\n"
        f"**Name:** {name}\n"
        f"**Age:** {age}\n"
        f"**Country:** {country}"
    )
    markup = {
        "inline_keyboard": [
            [{"text": "✏️ Edit Profile", "callback_data": "edit_profile"}],
            [{"text": "🗑️ Delete Profile", "callback_data": "delete_profile"}]
        ]
    }

    try:
        Bot.editMessageText(text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=markup)
    except:
        pass

    raise StopExecution()
```

### Command: * (Wildcard)

```tbs
state = User.fetchData("profile_state")
user_text = message.text

# Only intercept messages if the user is in an active profile state
if state:

    # --- FULL SETUP FLOW ---
    if state == "setup_name":
        User.storeData("profile_name", user_text)
        User.storeData("profile_state", "setup_age")
        Bot.sendMessage("📝 **Profile Setup (Step 2 of 3)**\n\nGreat! Now, what is your **Age**?", parse_mode="Markdown")
        raise StopExecution()

    elif state == "setup_age":
        User.storeData("profile_age", user_text)
        User.storeData("profile_state", "setup_country")
        Bot.sendMessage("📝 **Profile Setup (Step 3 of 3)**\n\nAlmost done! What is your **Country**?", parse_mode="Markdown")
        raise StopExecution()

    elif state == "setup_country":
        User.storeData("profile_country", user_text)
        User.storeData("profile_state", None) # Clear the state
        Bot.sendMessage("✅ **Profile Complete!**\n\nYour profile has been successfully saved. Type `/profile` to view it.", parse_mode="Markdown")
        raise StopExecution()

    # --- INDIVIDUAL EDIT CAPTURES ---
    elif state == "edit_name":
        User.storeData("profile_name", user_text)
        User.storeData("profile_state", None)
        Bot.sendMessage("✅ **Name updated successfully!** Type `/profile` to view changes.", parse_mode="Markdown")
        raise StopExecution()

    elif state == "edit_age":
        User.storeData("profile_age", user_text)
        User.storeData("profile_state", None)
        Bot.sendMessage("✅ **Age updated successfully!** Type `/profile` to view changes.", parse_mode="Markdown")
        raise StopExecution()

    elif state == "edit_country":
        User.storeData("profile_country", user_text)
        User.storeData("profile_state", None)
        Bot.sendMessage("✅ **Country updated successfully!** Type `/profile` to view changes.", parse_mode="Markdown")
        raise StopExecution()
```

## Execution Flow

```
/profile (empty profile):
1. Fetch profile_name → None
2. Send "Profile not set" with 🛠️ Setup Profile button
3. StopExecution

/profile (existing profile):
1. Fetch profile_name, profile_age, profile_country
2. Send "Your Profile" with ✏️ Edit and 🗑️ Delete buttons
3. StopExecution

/profile clear:
1. Store profile_name, profile_age, profile_country = None
2. Send "Profile cleared"
3. StopExecution

/profile set:
1. Store profile_state = "setup_name"
2. Send "Step 1 of 3: What is your Name?"
3. StopExecution

setup_profile callback (from empty profile view):
1. answerCallbackQuery → "Starting setup..."
2. Store profile_state = "setup_name"
3. Delete the empty profile message
4. Send "Step 1 of 3: What is your Name?"
5. StopExecution

Wildcard: user types name (state = setup_name):
1. Store profile_name = user_text
2. Store profile_state = "setup_age"
3. Send "Step 2 of 3: What is your Age?"
4. StopExecution

Wildcard: user types age (state = setup_age):
1. Store profile_age = user_text
2. Store profile_state = "setup_country"
3. Send "Step 3 of 3: What is your Country?"
4. StopExecution

Wildcard: user types country (state = setup_country):
1. Store profile_country = user_text
2. Store profile_state = None (clear state)
3. Send "Profile Complete! Type /profile to view it."
4. StopExecution

edit_profile callback:
1. answerCallbackQuery
2. editMessageText → Edit menu with Name/Age/Country + Back buttons
3. StopExecution

edit_name callback:
1. answerCallbackQuery → "Awaiting your input..."
2. Store profile_state = "edit_name"
3. Delete the edit menu message
4. Send "Please type your new Name"
5. StopExecution

Wildcard: user types new name (state = edit_name):
1. Store profile_name = user_text
2. Store profile_state = None
3. Send "Name updated successfully!"
4. StopExecution
(Same pattern for edit_age and edit_country)

delete_profile callback:
1. answerCallbackQuery → "Warning: This is permanent!" (show_alert)
2. editMessageText → "Are you sure?" with ✅ Yes, Delete / ❌ Cancel buttons
3. StopExecution

confirm_delete callback:
1. answerCallbackQuery → "Profile deleted." (show_alert)
2. Store profile_name, profile_age, profile_country, profile_state = None
3. editMessageText → "Your profile has been permanently deleted."
4. StopExecution

back_to_profile callback:
1. answerCallbackQuery
2. Fetch current profile data
3. editMessageText → Main profile view with Edit/Delete buttons
4. StopExecution
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `User.storeData` | Store profile fields (name, age, country) and state machine value |
| `User.fetchData` | Read profile fields and current state |
| `Bot.sendMessage` | Send setup prompts, confirmations, and profile views |
| `Bot.editMessageText` | Update existing messages (edit menu, delete confirmation, profile view) |
| `Bot.deleteMessage` | Remove the empty profile message when starting setup, remove edit menu when entering field edit |
| `Bot.answerCallbackQuery` | Acknowledge all inline button presses with optional text and show_alert |

## Best Practices

- Always check `if state:` before processing in the wildcard — without this guard, every user message gets intercepted as profile input
- Clear `profile_state` to `None` after every completed action — stale state causes the wildcard to capture normal chat messages as profile data
- Use `show_alert=True` for destructive actions like `confirm_delete` — the alert forces the user to acknowledge the action
- Wrap `editMessageText` and `deleteMessage` in try/except — messages may have been deleted by the user or another process, causing API errors
- Use `deleteMessage` for transitional UI (setup_profile, edit triggers) and `editMessageText` for in-place updates (edit menu, delete confirmation, back navigation) — this keeps the chat clean
- Store each profile field as a separate key (`profile_name`, `profile_age`, `profile_country`) instead of a dictionary — this makes individual field editing simpler since you only update one key
- Use `params` in `/profile` to handle sub-commands like `/profile clear` — this avoids needing separate command handlers for profile operations
- Re-fetch profile data in `back_to_profile` callback — the data may have changed since the original message was sent

## Common Mistakes

- **Mistake**: Not clearing `profile_state` after edit completion → **Fix**: Always set `profile_state = None` after storing the edited value — otherwise the wildcard keeps intercepting every message the user sends
- **Mistake**: Using `Bot.storeData` instead of `User.storeData` for profile data → **Fix**: Profile data is per-user and should use `User.storeData` — `Bot.storeData` is shared across all users and would mix up profiles
- **Mistake**: Not using `show_alert=True` on the delete confirmation callback → **Fix**: Use `show_alert=True` so the user sees a prominent alert before committing to deletion
- **Mistake**: Deleting the message instead of editing it in the delete confirmation flow → **Fix**: Use `editMessageText` to transform the "Are you sure?" message into "Profile deleted" — this preserves the message context and avoids chat clutter
- **Mistake**: Forgetting to clear `profile_state` in `confirm_delete` → **Fix**: Always clear the state key along with all data keys — a dangling state value will cause the wildcard to intercept future messages
- **Mistake**: Not handling the `back_to_profile` callback when profile is empty → **Fix**: If a user deletes their profile and then presses Back (which shouldn't happen but can in race conditions), check if `name` is None and show the empty profile view

## Related Patterns

- [Multi-Step Form Wizard](../ui/multi-step-form-wizard.md) — the simpler wizard-only pattern with confirm/cancel
- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — inline button and callback handler pattern
- [Referral & Reward System](../commerce/referral-reward-system.md) — uses Bot-level data for cross-user stats
- [Admin Dashboard with Broadcast & Maintenance Mode](../admin/admin-dashboard-broadcast.md) — similar inline menu navigation
- [Paginated List with Next/Prev Navigation](../ui/paginated-list.md) — another editMessageText-based UI pattern

## Search Keywords

user profile, profile setup, profile edit, profile delete, store profile, fetch profile, User.storeData, User.fetchData, Bot.editMessageText, Bot.deleteMessage, Bot.answerCallbackQuery, inline keyboard, state machine, wildcard, setup wizard, edit profile, delete confirmation, CRUD, profile CRUD, user data, per-user storage, multi-step, step by step, form input, profile management, user settings, data persistence, profile view

## User Prompts This Pattern Solves

- "How do I make a user profile system in TeleBot Studio?"
- "How do I store and display user profile data?"
- "How do I let users edit individual profile fields?"
- "How do I add a delete confirmation with inline buttons?"
- "How do I make a setup wizard for first-time users?"
- "How do I show different UI when the user has no data vs when they have data?"
- "How do I implement CRUD for user profile data?"
- "How do I use the wildcard command for multi-step input and editing?"
- "How do I add a back button to return to the main profile view?"
- "How do I handle /profile clear to quickly wipe all user data?"
