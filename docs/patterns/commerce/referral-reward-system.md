---
title: Referral & Reward System
category: commerce
difficulty: intermediate
keywords: referral, invite, reward, points, balance, earn, refer to earn, invite link, start parameter, self-referral fraud, Bot.fetchData, Bot.storeData, User.fetchData, User.storeData, Bot.getInfo, Bot.sendMessage, Bot.editMessageText, Bot.run, params, update_type, callback_query
commands: /start, /referral, /handler_callback_query
callback_handlers: ref_refresh, ref_close
tags: referral, reward, points, invite, balance, earn, commerce, credits
verified: false
tested_with:
last_updated: 2025-07-01
---

# Referral & Reward System

## Purpose

A refer-to-earn system where users get a unique invite link, earn points for every new user who joins through their link, and can track their referral count and reward balance from a dashboard.

## When to Use

- You want users to earn points or credits for inviting friends
- You need per-user referral tracking with a unique invite link
- You want to display a referral dashboard with balance and invite count
- You need to prevent self-referral and spam /start farming

Do NOT use this pattern for:
- Affiliate tracking with revenue sharing — this uses flat points, not percentage-based rewards
- Multi-tier referral chains — this tracks direct referrals only
- Withdrawal or redemption — this only tracks the balance; add a separate redemption flow

## Features

- Unique invite link per user using `?start=ref_{user_id}` deep link parameter
- Automatic reward on new user registration (10 points per invite)
- Self-referral fraud prevention — users cannot refer themselves
- Duplicate registration check — users cannot farm points by spamming /start
- Real-time referral dashboard with invite count and reward balance
- Notification to the referrer when someone uses their link
- Edit-based refresh for the dashboard (no chat spam)
- Per-user stats stored in Bot-level data (accessible from any user's session)

## Commands

| Command | Description |
|:---|:---|
| `/start` | Registers the user, processes referral if `params` contains a `ref_` payload, sends welcome |
| `/referral` | Opens the referral dashboard with stats and invite link |
| `/handler_callback_query` | Handles `ref_refresh` and `ref_close` callbacks |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `ref_refresh` | Re-runs /referral to pull latest stats and edit the dashboard message |
| `ref_close` | Deletes the dashboard message |

## Complete Working Code

### Command: /start

```tbs
user_id = message.from_user.id

# 1. VERIFY IF USER IS NEW
# We check this so users cannot spam /start to farm points
is_registered = User.fetchData("is_registered")

if not is_registered:
    User.storeData("is_registered", True)

    # 2. CHECK FOR REFERRAL PAYLOAD
    if params and str(params).startswith("ref_"):
        referrer_id = str(params).replace("ref_", "")

        # 3. PREVENT SELF-REFERRAL FRAUD
        if referrer_id != str(user_id):

            # Fetch the referrer's current global stats
            ref_count_key = f"ref_count_{referrer_id}"
            balance_key = f"balance_{referrer_id}"

            current_refs = Bot.fetchData(ref_count_key) or 0
            current_balance = Bot.fetchData(balance_key) or 0

            # Reward amount: 10 points per successful invite
            reward_amount = 10

            # Update the referrer's global stats
            Bot.storeData(ref_count_key, current_refs + 1)
            Bot.storeData(balance_key, current_balance + reward_amount)

            # 4. NOTIFY THE REFERRER
            try:
                notification = (
                    "🎉 <b>New Referral!</b>\n\n"
                    f"A new user joined using your link. You earned <b>{reward_amount} points</b>!"
                )
                Bot.sendMessage(chat_id=int(referrer_id), text=notification, parse_mode="HTML")
            except Exception as e:
                # Pass silently if the referrer has blocked the bot
                pass

# 5. STANDARD WELCOME MESSAGE
welcome_text = (
    f"👋 <b>Hello {message.from_user.first_name}!</b>\n\n"
    "Welcome to the platform. Use the command below to access your dashboard and start earning rewards:\n\n"
    "👉 /referral - Open Dashboard"
)
Bot.sendMessage(welcome_text, parse_mode="HTML")
```

### Command: /referral

```tbs
user_id = message.from_user.id
bot_info = Bot.getInfo()
bot_username = bot_info["username"]

# Generate the unique invite link
invite_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

# Fetch the user's global stats (updated by other users when they join)
ref_count_key = f"ref_count_{user_id}"
balance_key = f"balance_{user_id}"

total_referrals = Bot.fetchData(ref_count_key) or 0
total_balance = Bot.fetchData(balance_key) or 0

# Construct the dashboard layout
dashboard_text = (
    "🚀 <b>Your Referral Dashboard</b>\n\n"
    f"👥 <b>Total Invites:</b> {total_referrals}\n"
    f"💰 <b>Reward Balance:</b> {total_balance} points\n\n"
    "🔗 <b>Your Unique Invite Link:</b>\n"
    f"<code>{invite_link}</code>\n\n"
    "<i>Share this link with your friends to earn 10 points for every new user who joins!</i>"
)

# Build the inline keyboard
markup = {
    "inline_keyboard": [
        [{"text": "🔄 Refresh Stats", "callback_data": "ref_refresh"}],
        [{"text": "❌ Close Dashboard", "callback_data": "ref_close"}]
    ]
}

# If triggered by a button, edit the message; otherwise, send a new one
if update_type == "callback_query":
    Bot.editMessageText(
        text=dashboard_text,
        message_id=message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )
else:
    Bot.sendMessage(
        text=dashboard_text,
        parse_mode="HTML",
        reply_markup=markup
    )
```

### Command: /handler_callback_query

```tbs
payload = str(call.data)
callback_id = call.id
msg_id = message.message_id
chat_id = message.chat.id

# Intercept only referral system callbacks
if payload.startswith("ref_"):

    # Acknowledge the callback immediately to stop the loading icon
    Bot.answerCallbackQuery(callback_id)

    if payload == "ref_refresh":
        # Re-run the /referral command to generate the latest stats and edit the UI
        Bot.run("/referral")

    elif payload == "ref_close":
        # Silently destroy the menu to keep the chat clean
        try:
            Bot.deleteMessage(chat_id, msg_id)
        except Exception as e:
            pass
```

## Execution Flow

```
/start (no referral):
1. Check is_registered → False (new user)
2. Store is_registered = True
3. No ref_ params → skip referral logic
4. Send welcome message

/start?start=ref_123456 (with referral):
1. Check is_registered → False (new user)
2. Store is_registered = True
3. params starts with "ref_" → extract referrer_id = "123456"
4. Check referrer_id != user_id → not self-referral
5. Fetch referrer's ref_count and balance from Bot-level data
6. Increment referrer's ref_count by 1
7. Add reward_amount (10) to referrer's balance
8. Send notification to referrer: "You earned 10 points!"
9. Send welcome message to the new user

/start (already registered):
1. Check is_registered → True
2. Skip referral logic entirely (prevents farming)
3. Send welcome message

/referral:
1. Get bot username via Bot.getInfo()
2. Build invite link: https://t.me/{bot_username}?start=ref_{user_id}
3. Fetch this user's ref_count and balance from Bot-level data
4. Render dashboard with stats and invite link
5. If update_type == "callback_query" → editMessageText (refresh)
6. If not → sendMessage (first open)

ref_refresh callback:
1. answerCallbackQuery to stop spinner
2. Bot.run("/referral") → re-executes the command with latest data
3. editMessageText updates the existing dashboard

ref_close callback:
1. answerCallbackQuery to stop spinner
2. deleteMessage removes the dashboard
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `User.fetchData` | Read per-user data (is_registered, admin_state) |
| `User.storeData` | Write per-user data (is_registered) |
| `Bot.fetchData` | Read bot-level data (ref_count, balance — must be accessible from any user's session) |
| `Bot.storeData` | Write bot-level data (ref_count, balance) |
| `Bot.getInfo` | Get the bot's username to build the invite link |
| `Bot.sendMessage` | Send welcome, referral notification, and dashboard |
| `Bot.editMessageText` | Refresh the dashboard without sending a new message |
| `Bot.deleteMessage` | Remove the dashboard on close |
| `Bot.answerCallbackQuery` | Acknowledge inline button presses |
| `Bot.run` | Re-execute /referral from a callback to pull fresh stats |

## Best Practices

- Store referral counts and balances in **Bot-level data** (`Bot.fetchData`/`Bot.storeData`), not User-level data — the referrer's stats must be updatable from any new user's session
- Check `is_registered` before processing referrals — this prevents users from spamming `/start` with their own referral link to farm points
- Always compare `referrer_id != str(user_id)` — self-referral is the most common exploit in referral systems
- Wrap `Bot.sendMessage` to the referrer in try/except — the referrer may have blocked the bot
- Use `Bot.editMessageText` for dashboard refresh instead of delete+send — it keeps the chat clean and avoids flickering
- Use `<code>` tags around the invite link so users can tap to copy it on mobile
- Use `params` in `/start` to receive the deep link payload — this is the standard Telegram mechanism for referral tracking

## Common Mistakes

- **Mistake**: Storing referrer stats in `User.storeData` instead of `Bot.storeData` → **Fix**: User-level data is scoped to the current user's session. The referrer's balance must be stored in Bot-level data so it can be updated when ANY new user joins
- **Mistake**: Not checking `is_registered` before processing referrals → **Fix**: Always check first — without this, a user can spam `/start?start=ref_THEIR_OWN_ID` to farm infinite points
- **Mistake**: Comparing `referrer_id` as integer instead of string → **Fix**: `params` returns a string; compare both as strings to avoid type mismatch bugs
- **Mistake**: Using `Api.sendMessage` to notify the referrer → **Fix**: Use `Bot.sendMessage` with `chat_id=int(referrer_id)` — you're sending to a different chat than the current user
- **Mistake**: Not handling the case where the referrer has blocked the bot → **Fix**: Wrap the notification in try/except — if the bot can't message the referrer, the referral should still succeed silently

## Related Patterns

- [Admin Dashboard with Broadcast & Maintenance Mode](../admin/admin-dashboard-broadcast.md) — uses the same Bot-level data pattern for cross-user data
- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — the inline keyboard and callback handler pattern
- [TEMPLATE.md](../TEMPLATE.md) — the standard pattern template

## Search Keywords

referral, invite, reward, points, balance, earn, refer to earn, invite link, deep link, start parameter, self-referral fraud, Bot.fetchData, Bot.storeData, User.fetchData, User.storeData, Bot.getInfo, Bot.editMessageText, Bot.run, params, update_type, callback_query, referral dashboard, reward system, credits, per-user stats, bot-level data

## User Prompts This Pattern Solves

- "How do I make a referral system in TeleBot Studio?"
- "How do I create a refer-to-earn bot?"
- "How do I give users points when they invite friends?"
- "How do I make a unique invite link for each user?"
- "How do I prevent self-referral fraud?"
- "How do I track referral counts and reward balances?"
- "How do I use the /start deep link parameter for referrals?"
- "How do I refresh a dashboard message without sending a new one?"
