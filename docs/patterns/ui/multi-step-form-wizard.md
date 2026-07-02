---
title: Multi-Step Form Wizard
category: ui
difficulty: intermediate
keywords: form wizard, multi-step, step by step, wizard, collect input, user data, form, confirm, cancel, wizard_step, wizard_data, StopExecution, User.storeData, User.fetchData, Bot.editMessageText, callback handler, wildcard, state machine
commands: /form, * (wildcard), /handler_callback_query
callback_handlers: wizard_confirm, wizard_cancel
tags: form, wizard, multi-step, input, collect, confirm, cancel, state machine
verified: false
tested_with:
last_updated: 2025-07-01
---

# Multi-Step Form Wizard

## Purpose

A step-by-step form that collects user information across multiple messages — name, email, phone — then shows a summary with Confirm/Cancel inline buttons. Uses a state machine pattern to track which step the user is on.

## When to Use

- You need to collect multiple pieces of information from a user one at a time
- You want a step-by-step wizard instead of asking everything in one message
- You need a confirmation step before saving data
- You want users to be able to cancel mid-form with /cancel

Do NOT use this pattern for:
- Single-field input — just ask directly, no wizard needed
- Long forms with 10+ fields — consider breaking into sections or using a paginated approach
- Forms where fields depend on previous answers — this pattern uses a fixed step sequence

## Features

- Three-step wizard: name → email → phone → confirm
- State machine tracking via `wizard_step` (name, email, phone, confirm)
- Intermediate data stored in `wizard_data` dictionary
- `/cancel` abort at any step — clears all state
- Summary review with inline Confirm/Cancel buttons before saving
- Lockout at confirm step — user must use buttons, not type text
- On confirm: saves to `final_profile` and clears wizard state
- On cancel: discards all data and clears wizard state
- Edit-based UI mutation on confirm/cancel — no chat spam

## Commands

| Command | Description |
|:---|:---|
| `/form` | Starts the wizard at step 1 (name) |
| `*` (wildcard) | Captures user input at each step and advances the wizard |
| `/handler_callback_query` | Handles Confirm and Cancel inline buttons |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `wizard_confirm` | Saves the collected data and clears wizard state |
| `wizard_cancel` | Discards all data and clears wizard state |

## Complete Working Code

### Command: /form

```tbs
# 1. Initialize the wizard state and empty data dictionary
User.storeData("wizard_step", "name")
User.storeData("wizard_data", {})

# 2. Build the welcome message
welcome_text = (
    "📝 **Form Wizard Started**\n\n"
    "Let's collect your information step by step.\n"
    "*(You can type /cancel at any time to abort the process)*\n\n"
    "**Step 1/3:** What is your **Full Name**?"
)

# 3. Send the prompt
Bot.sendMessage(welcome_text, parse_mode="Markdown")
```

### Command: * (Wildcard)

```tbs
# 1. Fetch current wizard step
current_step = User.fetchData("wizard_step")
user_text = message.text

# 2. Intercept messages ONLY if the user is in the wizard
if current_step:

    # Handle global cancel command
    if user_text == "/cancel":
        User.storeData("wizard_step", None)
        User.storeData("wizard_data", None)
        Bot.sendMessage("❌ **Wizard canceled.** All data has been discarded.", parse_mode="Markdown")
        raise StopExecution()

    # Fetch the ongoing data payload
    wizard_data = User.fetchData("wizard_data") or {}

    # STEP 1: Process Name -> Ask for Email
    if current_step == "name":
        wizard_data["name"] = user_text
        User.storeData("wizard_data", wizard_data)
        User.storeData("wizard_step", "email")

        text = "**Step 2/3:** Great! Now, what is your **Email Address**?"
        Bot.sendMessage(text, parse_mode="Markdown")
        raise StopExecution()

    # STEP 2: Process Email -> Ask for Phone
    elif current_step == "email":
        wizard_data["email"] = user_text
        User.storeData("wizard_data", wizard_data)
        User.storeData("wizard_step", "phone")

        text = "**Step 3/3:** Almost done. What is your **Phone Number**?"
        Bot.sendMessage(text, parse_mode="Markdown")
        raise StopExecution()

    # STEP 3: Process Phone -> Show Summary & Wait for Confirmation
    elif current_step == "phone":
        wizard_data["phone"] = user_text
        User.storeData("wizard_data", wizard_data)
        User.storeData("wizard_step", "confirm")

        summary_text = (
            "📋 **Please review your information:**\n\n"
            f"👤 **Name:** {wizard_data.get('name')}\n"
            f"📧 **Email:** {wizard_data.get('email')}\n"
            f"📱 **Phone:** {wizard_data.get('phone')}\n\n"
            "Is this information correct?"
        )

        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Confirm", "callback_data": "wizard_confirm"},
                    {"text": "❌ Cancel", "callback_data": "wizard_cancel"}
                ]
            ]
        }

        Bot.sendMessage(summary_text, parse_mode="Markdown", reply_markup=keyboard)
        raise StopExecution()

    # STEP 4: Prevent stray text inputs while waiting for the inline button click
    elif current_step == "confirm":
        Bot.sendMessage("⚠️ Please use the buttons above to **Confirm** or **Cancel**, or type `/cancel` to abort.", parse_mode="Markdown")
        raise StopExecution()
```

### Command: /handler_callback_query

```tbs
payload = call.data
msg_id = message.message_id
chat_id = message.chat.id

# Process Confirm Action
if payload == "wizard_confirm":
    # 1. Acknowledge button click
    Bot.answerCallbackQuery(call.id, text="Data saved successfully!")

    # 2. Finalize data
    wizard_data = User.fetchData("wizard_data")
    User.storeData("final_profile", wizard_data)

    # 3. Clear temporary wizard state
    User.storeData("wizard_step", None)
    User.storeData("wizard_data", None)

    # 4. Mutate the UI
    success_text = "✅ **Success!** Your information has been saved.\nThank you for completing the form!"

    try:
        Bot.editMessageText(success_text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown")
    except:
        pass

    raise StopExecution()

# Process Cancel Action
elif payload == "wizard_cancel":
    # 1. Acknowledge button click
    Bot.answerCallbackQuery(call.id, text="Wizard canceled.")

    # 2. Wipe temporary wizard state
    User.storeData("wizard_step", None)
    User.storeData("wizard_data", None)

    # 3. Mutate the UI
    cancel_text = "❌ **Canceled.** Your information was discarded."

    try:
        Bot.editMessageText(cancel_text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown")
    except:
        pass

    raise StopExecution()
```

## Execution Flow

```
/form:
1. Store wizard_step = "name", wizard_data = {}
2. Send "Step 1/3: What is your Full Name?"

User types "John":
1. Wildcard * detects wizard_step = "name"
2. Store wizard_data["name"] = "John"
3. Store wizard_step = "email"
4. Send "Step 2/3: What is your Email Address?"
5. StopExecution

User types "john@mail.com":
1. Wildcard * detects wizard_step = "email"
2. Store wizard_data["email"] = "john@mail.com"
3. Store wizard_step = "phone"
4. Send "Step 3/3: What is your Phone Number?"
5. StopExecution

User types "+1234567890":
1. Wildcard * detects wizard_step = "phone"
2. Store wizard_data["phone"] = "+1234567890"
3. Store wizard_step = "confirm"
4. Send summary with ✅ Confirm / ❌ Cancel keyboard
5. StopExecution

User types random text at confirm step:
1. Wildcard * detects wizard_step = "confirm"
2. Send "Please use the buttons above to Confirm or Cancel"
3. StopExecution (forces them to use buttons)

User taps ✅ Confirm:
1. Fetch wizard_data
2. Store final_profile = wizard_data
3. Clear wizard_step and wizard_data
4. Edit the summary message → "Success! Your information has been saved."
5. StopExecution

User taps ❌ Cancel (or types /cancel at any step):
1. Clear wizard_step and wizard_data
2. Edit/send → "Canceled. Your information was discarded."
3. StopExecution
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `User.storeData` | Store wizard step, collected data, and final profile |
| `User.fetchData` | Read current step and collected data |
| `Bot.sendMessage` | Send step prompts and summary |
| `Bot.editMessageText` | Update the summary message on confirm/cancel |
| `Bot.answerCallbackQuery` | Acknowledge Confirm and Cancel button presses |

## Best Practices

- Always check `wizard_step` before processing — the wildcard `*` runs on every message, so you must guard against processing normal chat
- Clear both `wizard_step` and `wizard_data` when the wizard ends — stale state causes unexpected behavior if the user starts another wizard
- Use a `confirm` step that blocks text input — this forces the user to make an explicit choice via the inline buttons
- Save the final data to a separate key (`final_profile`) distinct from the working data (`wizard_data`) — this separates draft from committed state
- Use `StopExecution` after every step — this prevents the wildcard from falling through to other logic below it

## Common Mistakes

- **Mistake**: Not checking `if current_step:` before processing in the wildcard → **Fix**: Always guard with the step check — otherwise every message a user sends gets processed as form input
- **Mistake**: Not clearing `wizard_step` after the wizard completes → **Fix**: Set `wizard_step = None` on confirm, cancel, and /cancel — stale state will intercept future messages
- **Mistake**: Using `message.text` without checking if it exists → **Fix**: Some messages (photos, stickers) don't have text — guard with `user_text = message.text` and check for None if your bot receives media
- **Mistake**: Letting users type "yes" or "no" at the confirm step → **Fix**: The `confirm` step handler sends a warning and raises `StopExecution` — this forces them to use the inline buttons
- **Mistake**: Storing `wizard_data` as individual keys instead of a dictionary → **Fix**: Use a dictionary so you can pass the entire payload to `final_profile` in one call

## Related Patterns

- [Paginated List with Next/Prev Navigation](../ui/paginated-list.md) — another UI pattern using editMessageText
- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — inline button and callback handler pattern
- [Referral & Reward System](../commerce/referral-reward-system.md) — uses similar state tracking with User.storeData
- [TEMPLATE.md](../TEMPLATE.md) — the standard pattern template

## Search Keywords

form wizard, multi-step form, step by step, collect input, user data, confirm cancel, wizard_step, wizard_data, StopExecution, User.storeData, User.fetchData, Bot.editMessageText, callback handler, wildcard, state machine, form input, registration form, data collection, review summary

## User Prompts This Pattern Solves

- "How do I make a multi-step form in TeleBot Studio?"
- "How do I collect user information step by step?"
- "How do I build a registration wizard with confirm and cancel?"
- "How do I use the wildcard command to handle form input?"
- "How do I show a summary before saving user data?"
- "How do I let users cancel a form at any step?"
- "How do I track which step a user is on in a wizard?"
