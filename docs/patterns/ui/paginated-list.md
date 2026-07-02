---
title: Paginated List with Next/Prev Navigation
category: ui
difficulty: intermediate
keywords: pagination, paginated list, next prev, page navigation, editMessageText, inline keyboard, page indicator, per_page, callback_data, page_, ignore_page, User.storeData, User.fetchData, Bot.editMessageText, boundary check
commands: /list, /handler_callback_query
callback_handlers: page_{n}, ignore_page
tags: pagination, list, page, navigation, edit, inline keyboard, prev, next
verified: false
tested_with:
last_updated: 2025-07-01
---

# Paginated List with Next/Prev Navigation

## Purpose

A paginated list pattern that splits any dataset into pages with inline keyboard navigation — Previous, page indicator, and Next buttons. Uses `editMessageText` for smooth in-place updates without chat spam.

## When to Use

- You have a list of items (products, users, search results, orders) that exceeds 5–10 entries
- You want users to browse pages with ⬅️ Prev / ➡️ Next buttons
- You want the message to update in-place (edit) instead of deleting and resending
- You need a page indicator showing "2 / 5" in the keyboard

Do NOT use this pattern for:
- Short lists that fit in a single message — just send them directly
- Infinite scroll or load-more patterns — TBS doesn't support that natively
- Lists where each item needs its own callback action — combine with item buttons

## Features

- Configurable items per page
- Dynamic Prev/Next button visibility (hidden on first/last page)
- Page indicator button (e.g. "2 / 5") that is non-functional
- Boundary protection — page number clamped to valid range
- In-place message editing via `Bot.editMessageText` — no chat spam
- Graceful handling of "message not modified" errors on double-click
- Current page stored in `User.storeData` for state tracking

## Commands

| Command | Description |
|:---|:---|
| `/list` | Renders page 1 of the product list with navigation buttons |
| `/handler_callback_query` | Handles `page_` and `ignore_page` callbacks for navigation |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `page_{n}` | Navigate to page number `n` |
| `ignore_page` | Dummy callback for the page indicator button — shows a tooltip |

## Complete Working Code

### Command: /list

```tbs
# 1. Define your sample data (15 items)
products = [
    "1. 🍎 Apple", "2. 🍌 Banana", "3. 🍇 Grape", "4. 🍊 Orange", "5. 🍓 Strawberry",
    "6. 🍉 Watermelon", "7. 🍍 Pineapple", "8. 🥭 Mango", "9. 🍑 Peach", "10. 🍒 Cherry",
    "11. 🥝 Kiwi", "12. 🥥 Coconut", "13. 🍋 Lemon", "14. 🍈 Melon", "15. 🍐 Pear"
]

# 2. Pagination variables
per_page = 5
total_items = len(products)
total_pages = total_items // per_page
if total_items % per_page > 0:
    total_pages += 1

# Initialize state to page 1
current_page = 1
User.storeData("current_page", current_page)

# 3. Extract items for the current page
start_idx = (current_page - 1) * per_page
end_idx = start_idx + per_page
page_items = products[start_idx:end_idx]

# 4. Build the message text
text = f"📋 <b>Product Inventory (Page {current_page}/{total_pages})</b>\n\n"
for item in page_items:
    text += f"{item}\n"

# 5. Build the dynamic inline keyboard
nav_buttons = []

# Previous button (Only added if we are past page 1)
if current_page > 1:
    nav_buttons.append({"text": "⬅️ Prev", "callback_data": f"page_{current_page - 1}"})

# Page Indicator (Dummy callback)
nav_buttons.append({"text": f"{current_page} / {total_pages}", "callback_data": "ignore_page"})

# Next button (Only added if we haven't reached the last page)
if current_page < total_pages:
    nav_buttons.append({"text": "Next ➡️", "callback_data": f"page_{current_page + 1}"})

keyboard = {
    "inline_keyboard": [nav_buttons]
}

# 6. Send the initial message
Bot.sendMessage(text, parse_mode="HTML", reply_markup=keyboard)
```

### Command: /handler_callback_query

```tbs
payload = str(call.data)
callback_id = call.id
msg_id = message.message_id
chat_id = message.chat.id

# Catch the dummy page indicator button
if payload == "ignore_page":
    Bot.answerCallbackQuery(callback_id, text="You are viewing the current page number.")
    raise StopExecution()

# Handle Pagination Buttons
if payload.startswith("page_"):
    # Answer immediately to stop the loading icon
    Bot.answerCallbackQuery(callback_id)

    # 1. Parse the requested page number
    try:
        new_page = int(payload.replace("page_", ""))
    except Exception as e:
        raise StopExecution()

    # 2. Define the exact same data source
    products = [
        "1. 🍎 Apple", "2. 🍌 Banana", "3. 🍇 Grape", "4. 🍊 Orange", "5. 🍓 Strawberry",
        "6. 🍉 Watermelon", "7. 🍍 Pineapple", "8. 🥭 Mango", "9. 🍑 Peach", "10. 🍒 Cherry",
        "11. 🥝 Kiwi", "12. 🥥 Coconut", "13. 🍋 Lemon", "14. 🍈 Melon", "15. 🍐 Pear"
    ]

    per_page = 5
    total_items = len(products)
    total_pages = total_items // per_page
    if total_items % per_page > 0:
        total_pages += 1

    # Boundary constraints to prevent errors
    if new_page < 1:
        new_page = 1
    elif new_page > total_pages:
        new_page = total_pages

    # Save the updated state
    User.storeData("current_page", new_page)

    # 3. Extract items for the new requested page
    start_idx = (new_page - 1) * per_page
    end_idx = start_idx + per_page
    page_items = products[start_idx:end_idx]

    # 4. Build the updated text
    text = f"📋 <b>Product Inventory (Page {new_page}/{total_pages})</b>\n\n"
    for item in page_items:
        text += f"{item}\n"

    # 5. Build the updated inline keyboard
    nav_buttons = []

    if new_page > 1:
        nav_buttons.append({"text": "⬅️ Prev", "callback_data": f"page_{new_page - 1}"})

    nav_buttons.append({"text": f"{new_page} / {total_pages}", "callback_data": "ignore_page"})

    if new_page < total_pages:
        nav_buttons.append({"text": "Next ➡️", "callback_data": f"page_{new_page + 1}"})

    keyboard = {
        "inline_keyboard": [nav_buttons]
    }

    # 6. Smoothly edit the message
    try:
        Bot.editMessageText(
            text=text,
            message_id=msg_id,
            chat_id=chat_id,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        # Ignore Telegram's "Message is not modified" error if user double-clicks fast
        pass

    raise StopExecution()
```

## Execution Flow

```
/list:
1. Define the data source (products array)
2. Calculate total_pages = ceil(total_items / per_page)
3. Extract items for page 1 (index 0 to 4)
4. Build message text with item list
5. Build inline keyboard:
   - Page 1: no Prev, [1/3] indicator, Next
   - Page 2: Prev, [2/3] indicator, Next
   - Page 3: Prev, [3/3] indicator, no Next
6. Send message with keyboard

User taps Next ➡️:
1. callback_data = "page_2"
2. answerCallbackQuery stops the spinner
3. Parse new_page = 2
4. Clamp to valid range (1 to total_pages)
5. Store current_page = 2
6. Extract items for page 2 (index 5 to 9)
7. Build updated text and keyboard
8. editMessageText updates the message in place
9. StopExecution — done

User taps page indicator [2/3]:
1. callback_data = "ignore_page"
2. answerCallbackQuery shows tooltip "You are viewing the current page number."
3. StopExecution — no message update
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `Bot.sendMessage` | Send the initial paginated list |
| `Bot.editMessageText` | Update the message in-place when navigating pages |
| `Bot.answerCallbackQuery` | Acknowledge button presses (with tooltip for indicator) |
| `User.storeData` | Store the current page number |
| `User.fetchData` | Read the current page number (if needed across commands) |

## Best Practices

- Use `Bot.editMessageText` instead of delete+send for pagination — it keeps the chat clean and feels instant
- Always wrap `editMessageText` in try/except — Telegram throws "message is not modified" if the user double-clicks fast and the content hasn't changed
- Clamp the page number to valid bounds (`1` to `total_pages`) before slicing — prevents index errors
- Put the page indicator button in the middle of the row between Prev and Next — it's the standard Telegram UI pattern
- Hide Prev on the first page and Next on the last page — disabled buttons confuse users
- Define the data source in both `/list` and `/handler_callback_query` — TBS commands are stateless, so the array must be rebuilt on each callback

## Common Mistakes

- **Mistake**: Using `Api.editMessageText` instead of `Bot.editMessageText` in the callback handler → **Fix**: Use `Bot.editMessageText` inside `/handler_callback_query` — it requires `chat_id` and `message_id` parameters
- **Mistake**: Not wrapping `editMessageText` in try/except → **Fix**: Always wrap it — Telegram returns an error if the message content hasn't changed (double-click)
- **Mistake**: Forgetting to define the data source in the callback handler → **Fix**: TBS commands are independent — the products array must be defined in both `/list` and `/handler_callback_query`
- **Mistake**: Using `page_items = products[start_idx:end_idx]` without boundary checks → **Fix**: Always clamp `new_page` to the valid range before slicing
- **Mistake**: Making the page indicator button functional → **Fix**: Use a dummy `callback_data` like `"ignore_page"` and answer with a tooltip — it should not navigate anywhere

## Related Patterns

- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — multi-level menu navigation (not paginated)
- [Admin Dashboard with Broadcast & Maintenance Mode](../admin/admin-dashboard-broadcast.md) — uses delete+send pattern for menu updates
- [TEMPLATE.md](../TEMPLATE.md) — the standard pattern template

## Search Keywords

pagination, paginated list, next prev, page navigation, editMessageText, inline keyboard, page indicator, per_page, callback_data, page_, ignore_page, User.storeData, Bot.editMessageText, boundary check, product list, page number, prev next buttons, list display, smooth edit, message not modified

## User Prompts This Pattern Solves

- "How do I paginate a list in TeleBot Studio?"
- "How do I add next and previous buttons to a list?"
- "How do I show a page indicator like '2 / 5' in inline buttons?"
- "How do I edit a message in place instead of deleting and resending?"
- "How do I split a long list into pages with inline buttons?"
- "How do I handle the 'message is not modified' error in pagination?"
- "How do I make a product catalog with page navigation?"
