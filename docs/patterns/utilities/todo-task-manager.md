---
title: Todo Task Manager
category: utilities
difficulty: intermediate
keywords: todo, task manager, task list, checklist, to-do, add task, mark done, clear done, inline keyboard, dynamic buttons, User.storeData, User.fetchData, Bot.sendMessage, Bot.editMessageText, Bot.deleteMessage, Bot.answerCallbackQuery, wildcard, state machine, StopExecution, params, callback_query
commands: /todo, * (wildcard), /handler_callback_query
callback_handlers: todo_add, todo_view, todo_done_N, todo_clear_done
tags: todo, task, checklist, manager, utilities, inline keyboard, dynamic buttons, wildcard, state machine
verified: false
tested_with:
last_updated: 2025-07-02
---

# Todo Task Manager

## Purpose

A personal todo/task checklist where users add tasks via command or inline button, mark them done with a single tap, and clear completed items — all with a dynamic inline keyboard that rebuilds itself after every action.

## When to Use

- You need a personal task or checklist system for each user
- You want dynamic inline buttons that change based on data (pending tasks get ✅ buttons)
- You need to demonstrate the "re-render after action" pattern — edit the same message with updated content
- You want a quick-add via `/todo <task>` and a conversational add via the ➕ button

Do NOT use this pattern for:
- Shared/team task lists — this uses per-user `User.storeData`, not cross-user `Bot.storeData`
- Complex task management with due dates, priorities, or categories — extend the data model first
- Large task lists (50+) — this pattern shows only the first 5 tasks; for large lists, combine with pagination

## Features

- **Quick add**: `/todo buy milk` adds a task instantly without entering a flow
- **Conversational add**: Tap ➕ Add Task → type the task → saved
- **Dynamic ✅ buttons**: Only pending tasks get a "✅ N" button; done tasks show a checkmark in the text
- **Neat button rows**: Done buttons are arranged in rows of 3 for clean layout
- **Mark done with one tap**: Tap ✅ 1 → task 1 is marked complete, list re-renders
- **Clear completed**: 🗑️ Clear Done removes all done items from the list
- **Empty state handling**: Different UI when the list is empty vs populated
- **5-task display limit**: Shows first 5 tasks with "...and N more" overflow indicator
- **Re-render pattern**: All actions (done, clear, view) re-render the same message via `editMessageText`

## Commands

| Command | Description |
|:---|:---|
| `/todo` | View current task list (or empty state) |
| `/todo <task>` | Add a task instantly |
| `*` (wildcard) | Capture task text when user is in the "add task" flow |
| `/handler_callback_query` | Handle all inline button callbacks |

## Callback Handlers

| Callback Pattern | Description |
|:---|:---|
| `todo_add` | Enter the "awaiting task" state and prompt for input |
| `todo_view` | Re-render the task list (used after adding a task) |
| `todo_done_N` | Mark task N as done (1-based index) |
| `todo_clear_done` | Remove all completed tasks from the list |

## Complete Working Code

### Command: /todo

```tbs
todo_list = User.fetchData("todo_list") or []

# 1. No parameters provided -> Show the list
if not params:
    if not todo_list:
        text = "📋 Your todo list is empty. Use `/todo <task>` to add a task."
        markup = {
            "inline_keyboard": [
                [{"text": "➕ Add Task", "callback_data": "todo_add"}]
            ]
        }
        Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
        raise StopExecution()
    else:
        text = "📋 **Your Todo List:**\n\n"
        display_list = todo_list[:5] # Limit to first 5 tasks

        for i, item in enumerate(display_list):
            status_icon = "✅" if item.get("done") else "❌"
            status_text = "(done)" if item.get("done") else "(pending)"
            text += f"{i+1}. {status_icon} {item['task']} {status_text}\n"

        if len(todo_list) > 5:
            text += f"\n*...and {len(todo_list) - 5} more tasks.*"

        # Build inline keyboard dynamically for pending tasks
        markup = {"inline_keyboard": []}
        done_buttons = []

        for i, item in enumerate(display_list):
            if not item.get("done"):
                done_buttons.append({"text": f"✅ {i+1}", "callback_data": f"todo_done_{i+1}"})

        # Format buttons into neat rows of 3
        row = []
        for btn in done_buttons:
            row.append(btn)
            if len(row) == 3:
                markup["inline_keyboard"].append(row)
                row = []
        if row:
            markup["inline_keyboard"].append(row)

        # Add control buttons
        markup["inline_keyboard"].append([{"text": "🗑️ Clear Done", "callback_data": "todo_clear_done"}])

        if len(todo_list) > 5:
            markup["inline_keyboard"].append([{"text": "➡️ More", "callback_data": "todo_view"}])

        Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
        raise StopExecution()

# 2. Parameters provided -> Add the task instantly
else:
    todo_list.append({"task": params, "done": False})
    User.storeData("todo_list", todo_list)

    text = f"✅ Task added: **{params}**"
    markup = {
        "inline_keyboard": [
            [{"text": "📋 View List", "callback_data": "todo_view"}]
        ]
    }

    Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
    raise StopExecution()
```

### Command: /handler_callback_query

```tbs
payload = str(call.data)
cb_id = call.id
chat_id = message.chat.id
msg_id = message.message_id

# ------------------------------------------
# A. INITIATE ADD TASK FLOW
# ------------------------------------------
if payload == "todo_add":
    User.storeData("todo_add_state", "awaiting_task")

    try:
        Bot.answerCallbackQuery(cb_id, text="Type your task...")
    except:
        pass

    try:
        Bot.deleteMessage(chat_id, msg_id)
    except:
        pass

    Bot.sendMessage("📝 **Type your task below:**", parse_mode="Markdown")
    raise StopExecution()

# ------------------------------------------
# B. PROCESS LIST ACTIONS (View, Done, Clear)
# ------------------------------------------
elif payload == "todo_view" or payload.startswith("todo_done_") or payload == "todo_clear_done":

    todo_list = User.fetchData("todo_list") or []

    # Action: Mark item as Done
    if payload.startswith("todo_done_"):
        try:
            idx = int(payload.replace("todo_done_", "")) - 1
            if 0 <= idx < len(todo_list):
                todo_list[idx]["done"] = True
                User.storeData("todo_list", todo_list)

                try:
                    Bot.answerCallbackQuery(cb_id, text="Task completed! 🎉")
                except:
                    pass
        except:
            pass

    # Action: Clear Done items
    elif payload == "todo_clear_done":
        todo_list = [task for task in todo_list if not task.get("done")]
        User.storeData("todo_list", todo_list)

        try:
            Bot.answerCallbackQuery(cb_id, text="Cleared!")
        except:
            pass

    # Action: Simply View
    elif payload == "todo_view":
        try:
            Bot.answerCallbackQuery(cb_id)
        except:
            pass

    # --- RE-RENDER THE LIST UI ---
    if not todo_list:
        text = "📋 Your todo list is empty. Use `/todo <task>` to add a task."
        markup = {
            "inline_keyboard": [
                [{"text": "➕ Add Task", "callback_data": "todo_add"}]
            ]
        }
    else:
        text = "📋 **Your Todo List:**\n\n"
        display_list = todo_list[:5]

        for i, item in enumerate(display_list):
            status_icon = "✅" if item.get("done") else "❌"
            status_text = "(done)" if item.get("done") else "(pending)"
            text += f"{i+1}. {status_icon} {item['task']} {status_text}\n"

        if len(todo_list) > 5:
            text += f"\n*...and {len(todo_list) - 5} more tasks.*"

        markup = {"inline_keyboard": []}
        done_buttons = []

        for i, item in enumerate(display_list):
            if not item.get("done"):
                done_buttons.append({"text": f"✅ {i+1}", "callback_data": f"todo_done_{i+1}"})

        row = []
        for btn in done_buttons:
            row.append(btn)
            if len(row) == 3:
                markup["inline_keyboard"].append(row)
                row = []
        if row:
            markup["inline_keyboard"].append(row)

        markup["inline_keyboard"].append([{"text": "🗑️ Clear Done", "callback_data": "todo_clear_done"}])

        if len(todo_list) > 5:
            markup["inline_keyboard"].append([{"text": "➡️ More", "callback_data": "todo_view"}])

    # Safely update the active message
    try:
        Bot.editMessageText(text, chat_id=chat_id, message_id=msg_id, parse_mode="Markdown", reply_markup=markup)
    except:
        pass

    raise StopExecution()
```

### Command: * (Wildcard)

```tbs
add_state = User.fetchData("todo_add_state")
user_text = message.text

# Intercept only if the bot is actively waiting for a new task
if add_state == "awaiting_task" and user_text:

    todo_list = User.fetchData("todo_list") or []
    todo_list.append({"task": user_text, "done": False})

    # Save list and clear the conversational state
    User.storeData("todo_list", todo_list)
    User.storeData("todo_add_state", None)

    text = f"✅ Task added: **{user_text}**"
    markup = {
        "inline_keyboard": [
            [{"text": "📋 View List", "callback_data": "todo_view"}]
        ]
    }

    Bot.sendMessage(text, parse_mode="Markdown", reply_markup=markup)
    raise StopExecution()
```

## Execution Flow

```
/todo (empty list):
1. Fetch todo_list → []
2. Send empty state with ➕ Add Task button
3. StopExecution

/todo buy milk (quick add):
1. Fetch todo_list → []
2. Append {"task": "buy milk", "done": False}
3. User.storeData("todo_list", updated_list)
4. Send "✅ Task added: buy milk" with 📋 View List button
5. StopExecution

/todo (3 tasks, 1 done):
1. Fetch todo_list → [{"task": "buy milk", "done": True}, {"task": "homework", "done": False}, {"task": "call mom", "done": False}]
2. Render: "1. ✅ buy milk (done)" + "2. ❌ homework (pending)" + "3. ❌ call mom (pending)"
3. Build dynamic keyboard: ✅ 2 | ✅ 3 | 🗑️ Clear Done
4. Send message with inline keyboard
5. StopExecution

todo_add callback:
1. Store todo_add_state = "awaiting_task"
2. answerCallbackQuery "Type your task..."
3. Delete the old message
4. Send "📝 Type your task below:"
5. StopExecution

Wildcard: user types "call dentist" (state = awaiting_task):
1. Fetch todo_list, append {"task": "call dentist", "done": False}
2. User.storeData("todo_list", updated_list)
3. User.storeData("todo_add_state", None)
4. Send "✅ Task added: call dentist" with 📋 View List button
5. StopExecution

todo_done_2 callback:
1. Extract index N=2, convert to 0-based idx=1
2. Set todo_list[1]["done"] = True
3. User.storeData("todo_list", updated_list)
4. answerCallbackQuery "Task completed! 🎉"
5. Re-render the task list via editMessageText
6. StopExecution

todo_clear_done callback:
1. Filter out all tasks where done == True
2. User.storeData("todo_list", filtered_list)
3. answerCallbackQuery "Cleared!"
4. Re-render the task list (or empty state if no tasks remain)
5. StopExecution

todo_view callback:
1. answerCallbackQuery
2. Re-render the task list via editMessageText
3. StopExecution
```

## APIs Used

| API Method | Purpose |
|:---|:---|
| `User.storeData` | Store the todo list and the "add task" state |
| `User.fetchData` | Read the todo list and current state |
| `Bot.sendMessage` | Send the task list, add confirmation, and input prompt |
| `Bot.editMessageText` | Re-render the task list after done/clear/view actions |
| `Bot.deleteMessage` | Remove the empty-list message when entering add flow |
| `Bot.answerCallbackQuery` | Acknowledge all inline button presses with feedback text |

## Best Practices

- **Re-render pattern**: After every action (done, clear, view), rebuild the entire message and keyboard, then call `editMessageText` once — this keeps the UI consistent and avoids stale buttons
- **Dynamic keyboard**: Only generate ✅ buttons for pending tasks — done tasks don't need action buttons, which keeps the keyboard clean
- **Row of 3**: Arrange done buttons in rows of 3 for a neat, compact layout on mobile
- **Quick add vs conversational add**: Support both `/todo <task>` for speed and the ➕ button for users who prefer tapping — this covers both interaction styles
- **Guard the wildcard**: Always check `add_state == "awaiting_task"` before processing — without this, every user message gets captured as a task
- **Clear state after use**: Set `todo_add_state = None` after capturing the task — stale state causes the wildcard to eat normal messages
- **1-based indexing in buttons**: Use `todo_done_1`, `todo_done_2` (1-based) for user-facing buttons, but convert to 0-based when accessing the list — this is more intuitive for users
- **Wrap everything in try/except**: `editMessageText`, `deleteMessage`, and `answerCallbackQuery` can all fail if the message was deleted or the callback expired

## Common Mistakes

- **Mistake**: Not re-rendering the list after marking a task done → **Fix**: The "re-render pattern" rebuilds the text and keyboard from scratch after every action, then calls `editMessageText` — this ensures the UI always matches the data
- **Mistake**: Using `Bot.storeData` instead of `User.storeData` for the todo list → **Fix**: Todo lists are personal — use `User.storeData` so each user has their own list, not a shared one
- **Mistake**: Forgetting to clear `todo_add_state` after capturing the task → **Fix**: Always set `todo_add_state = None` — otherwise every subsequent message gets saved as a task
- **Mistake**: Not checking `if 0 <= idx < len(todo_list)` when processing `todo_done_N` → **Fix**: Always validate the index — a stale callback could reference a task that no longer exists after clearing
- **Mistake**: Adding ✅ buttons for done tasks → **Fix**: Only generate buttons for pending tasks (`if not item.get("done")`) — done tasks just show the ✅ icon in text, no button needed
- **Mistake**: Building a single row with all done buttons → **Fix**: Arrange buttons in rows of 3 — a single long row overflows on mobile and looks broken

## Related Patterns

- [Paginated List with Next/Prev Navigation](../ui/paginated-list.md) — pagination pattern for longer lists
- [User Profile Storage with Edit & Delete](../storage/user-profile-storage.md) — similar CRUD pattern with inline keyboard navigation
- [Multi-Step Form Wizard](../ui/multi-step-form-wizard.md) — the wildcard state machine pattern for collecting input
- [Inline Keyboard Navigation System](../ui/inline-keyboard-navigation.md) — inline button and callback handler fundamentals

## Search Keywords

todo, task manager, task list, checklist, to-do, add task, mark done, clear done, inline keyboard, dynamic buttons, User.storeData, User.fetchData, Bot.editMessageText, Bot.deleteMessage, Bot.answerCallbackQuery, wildcard, state machine, re-render pattern, quick add, conversational add, done button, pending task, task completion

## User Prompts This Pattern Solves

- "How do I make a todo list bot in TeleBot Studio?"
- "How do I add tasks and mark them as done with inline buttons?"
- "How do I build dynamic inline keyboards that change based on data?"
- "How do I use the re-render pattern to update a message after an action?"
- "How do I arrange inline buttons in neat rows of 3?"
- "How do I support both quick-add (/todo task) and conversational add (➕ button)?"
- "How do I clear completed items from a list?"
- "How do I handle indexed callbacks like todo_done_1, todo_done_2?"
