# Commands in TBS
Commands are the core building blocks of every bot on TeleBot Studio. They define how your bot responds to user inputs, processes data, and performs actions. This comprehensive guide explains everything you need to know about creating, managing, and optimizing commands using TeleBot Syntax (TBS).
***
## What Are Commands?
A **command** is a trigger that executes specific code when a user sends a particular message to your bot. Commands can:
* Respond to user messages with text, images, or files
* Process and store user data
* Interact with external APIs and services
* Chain together to create complex workflows
* Schedule future actions
* Manage bot state and user sessions
**Examples of common commands:**
* `/start` - Welcome new users
* `/help` - Display available commands
* `/subscribe` - Handle subscription requests
* `*` - Catch unrecognized inputs (wildcard)
***
## Writing Commands in TBS
TeleBot Syntax (TBS) is a Python-based language designed specifically for bot development. It provides built-in objects, methods, and libraries without requiring any imports.
### Basic Command Structure
Here's a simple command that sends a message:
```python
Api.sendMessage("Hello! This is my bot.")
```
### Using Variables
Access user information and message data:
```python
# Get user's first name
first_name = message.from_user.first_name
# Get user ID
user_id = message.from_user.id
# Get chat ID
chat_id = message.chat.id
# Send personalized message
Api.sendMessage(f"Hello {first_name}! Your ID is {user_id}.")
```
### Handling Command Parameters
Users can send parameters with commands (e.g., `/start 12345`). Access them using the `params` variable:
```python
# /start command
if params:
referrer_id = params
Api.sendMessage(f"You were referred by user {referrer_id}!")
User.storeData("referrer", referrer_id)
else:
Api.sendMessage("Welcome! Use /help to get started.")
```
***
## Managing User Interactions
TBS provides powerful methods for creating interactive bot experiences.
### 1. Bot.waitForInput()
Wait for the user's next message and route it to a specific command.
**Syntax:**
```python
Bot.waitForInput(command, **options)
```
**Parameters:**
* `command` (Required): Name of the command to execute next
* `options` (Optional): Data to pass to the next command
**Example - Collecting User Email:**
```python
# /register command
Api.sendMessage("Please enter your email address:")
Bot.waitForInput("process_email")
```
```python
# process_email command
email = msg
User.storeData("email", email)
Api.sendMessage(f"Thank you! Your email {email} has been saved.")
```
**Example - With Options:**
```python
# /quiz command
Api.sendMessage("What is 2 + 2?")
Bot.waitForInput("check_answer", correct_answer=4, question_id=1)
```
```python
# check_answer command
user_answer = int(msg)
correct = options.get("correct_answer")
if user_answer == correct:
Api.sendMessage("Correct! ✅")
else:
Api.sendMessage(f"Wrong! The answer was {correct}.")
```
### 2. Bot.run()
Execute another command immediately.
**Syntax:**
```python
Bot.run(command, **options)
```
**Parameters:**
* `command` (Required): Name of the command to run
* `options` (Optional): Data to pass to the command
**Example - Command Redirection:**
```python
# /info command
Api.sendMessage("Redirecting you to the help menu...")
Bot.run("help")
```
**Example - With Options:**
```python
# /premium command
Bot.run("subscribe", plan="premium", duration=30)
```
```python
# subscribe command
plan = options.get("plan", "basic")
duration = options.get("duration", 7)
Api.sendMessage(f"Subscribing to {plan} plan for {duration} days...")
```
### 3. Bot.scheduleCommand()
Schedule a command to execute after a specified delay.
**Syntax:**
```python
Bot.scheduleCommand(delay_seconds, command, user_id=None, chat_id=None, params=None, **options)
```
**Parameters:**
* `delay_seconds` (Required): Time in seconds before execution (0.1 to 31536000)
* `command` (Required): Name of the command to run
* `user_id` (Optional): Target user ID
* `chat_id` (Optional): Target chat ID
* `params` (Optional): Parameters to pass
* `options` (Optional): Additional data to pass
**Example - Reminder System:**
```python
# /remind command
Api.sendMessage("I'll remind you in 10 seconds!")
Bot.scheduleCommand(10, "send_reminder")
```
```python
# send_reminder command
Api.sendMessage("⏰ This is your reminder!")
```
**Example - Delayed Welcome:**
```python
# /start command
Api.sendMessage("Welcome! Let me prepare something for you...")
Bot.scheduleCommand(3, "welcome_bonus")
```
```python
# welcome_bonus command
Api.sendMessage("🎁 Here's a welcome bonus!")
User.res("coins").add(100)
```
***
## Command Types
### Regular Commands
Standard commands start with `/` and are triggered when users type them:
```python
# /start command
name = message.from_user.first_name
Api.sendMessage(f"Welcome to the bot, {name}!")
```
```python
# /help command
help_message = """
**Available Commands:**
/start - Start the bot
/help - Show this help menu
/profile - View your profile
/settings - Configure bot settings
"""
Api.sendMessage(help_message, parse_mode="Markdown")
```
### Wildcard Command (`*`)
The wildcard command catches any message that doesn't match defined commands. This is useful for:
* Default responses to unknown commands
* Natural language processing
* Catching typos
```python
# * command
user_message = message.text
Api.sendMessage(f"I don't understand '{user_message}'. Try /help for available commands.")
```
**Advanced Wildcard Example:**
```python
# * command - AI Chatbot
user_text = message.text
# Check for keywords
if "price" in user_text.lower():
Api.sendMessage("Our pricing starts at $10/month. Type /pricing for details.")
elif "help" in user_text.lower():
Bot.run("help")
else:
Api.sendMessage("I'm not sure what you mean. Type /help to see what I can do!")
```
### At Handler Command (`@`)
The `@` command executes **before** any other command. Use it for:
* Logging user activity
* Checking user permissions
* Preprocessing messages
* Analytics tracking
```python
# @ command
user_id = message.from_user.id
username = message.from_user.username or "No username"
# Log activity
Bot.res("total_messages").add(1)
# You can optionally send a message
# Api.sendMessage("Processing your request...")
```
**Important**: The `@` handler runs first, then the actual command runs.
### Special Update Handlers
Handle specific types of Telegram updates:
#### Photo Handler
```python
# /handler_photo command
Api.sendMessage("Nice photo! Thanks for sharing.")
# Access photo info
photo = message.photo[-1] # Get largest photo
file_id = photo.file_id
Api.sendMessage(f"Photo file ID: {file_id}")
```
#### Document Handler
```python
# /handler_document command
doc = message.document
file_name = doc.file_name
file_size = doc.file_size
Api.sendMessage(f"Received document: {file_name} ({file_size} bytes)")
```
#### Callback Query Handler
```python
# /handler_callback_query command
callback_data = message.data
Api.answerCallbackQuery("Button clicked!")
if callback_data == "option_1":
Api.sendMessage("You selected Option 1")
elif callback_data == "option_2":
Api.sendMessage("You selected Option 2")
```
***
## Using Global Variables
TBS provides several pre-defined variables:
### Message Variables
```python
# Full message object
full_message = message
# User information
user_id = message.from_user.id
username = message.from_user.username
first_name = message.from_user.first_name
last_name = message.from_user.last_name
# Chat information
chat_id = message.chat.id
chat_type = message.chat.type # "private", "group", "supergroup", "channel"
# Message content
message_text = message.text
message_id = message.message_id
```
### Shorthand Variables
```python
# msg - The message text or caption
user_input = msg
# u - User ID (shorthand)
current_user = u
# command - Current command name
current_cmd = command
# params - Command parameters
command_params = params
# options - Data passed from previous command
passed_data = options
# update_type - Type of update
update_kind = update_type # "message", "callback_query", "photo", etc.
```
***
## Command Chaining
Chain commands together to create multi-step workflows:
### Example: User Registration Flow
**Step 1: Get Name**
```python
# /register command
Api.sendMessage("Let's get you registered!")
Api.sendMessage("First, what's your name?")
Bot.waitForInput("get_name")
```
**Step 2: Get Email**
```python
# get_name command
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email address?")
Bot.waitForInput("get_email")
```
**Step 3: Get Age**
```python
# get_email command
email = msg
User.storeData("email", email)
Api.sendMessage("Great! How old are you?")
Bot.waitForInput("get_age")
```
**Step 4: Complete Registration**
```python
# get_age command
age = msg
User.storeData("age", age)
name = User.fetchData("name")
email = User.fetchData("email")
Api.sendMessage(f"""
✅ **Registration Complete!**
Name: {name}
Email: {email}
Age: {age}
Welcome to our community!
""", parse_mode="Markdown")
```
***
## Data Management in Commands
### Storing User Data
```python
# Store various data types
User.storeData("username", "john_doe")
User.storeData("score", 150)
User.storeData("premium", True)
User.storeData("settings", {"theme": "dark", "notifications": True})
```
### Retrieving User Data
```python
# Fetch stored data
username = User.fetchData("username")
score = User.fetchData("score")
settings = User.fetchData("settings")
# Check if data exists
if username:
Api.sendMessage(f"Welcome back, {username}!")
else:
Api.sendMessage("Please set your username with /setusername")
```
### Removing User Data
```python
# Delete specific data
User.removeData("temp_data")
# Or clear when user logs out
User.removeData("session_token")
User.removeData("login_time")
```
### Working with Resources
Resources are numeric values perfect for points, coins, scores:
```python
# Add points
points = User.res("points")
points.add(50)
Api.sendMessage(f"You earned 50 points! Total: {points.value()}")
# Deduct points
coins = User.res("coins")
cost = 20
if coins.value() >= cost:
coins.cut(cost)
Api.sendMessage("Purchase successful!")
else:
Api.sendMessage("Insufficient coins!")
```
***
## Advanced Command Techniques
### Conditional Logic
```python
# /profile command
user_level = User.fetchData("level") or 1
if user_level >= 10:
Api.sendMessage("🌟 You're a VIP user!")
elif user_level >= 5:
Api.sendMessage("⭐ You're an experienced user!")
else:
Api.sendMessage("👤 You're a new user. Keep exploring!")
```
### Loops and Iteration
```python
# /leaderboard command
users = [
{"name": "Alice", "score": 150},
{"name": "Bob", "score": 120},
{"name": "Charlie", "score": 100}
]
message = "🏆 **Leaderboard:**\n\n"
for i, user in enumerate(users, 1):
message += f"{i}. {user['name']} - {user['score']} points\n"
Api.sendMessage(message, parse_mode="Markdown")
```
### Error Handling
```python
# /divide command
try:
numbers = msg.split()
a = float(numbers[0])
b = float(numbers[1])
result = a / b
Api.sendMessage(f"Result: {result}")
except ZeroDivisionError:
Api.sendMessage("Error: Cannot divide by zero!")
except (ValueError, IndexError):
Api.sendMessage("Please send two numbers: /divide 10 2")
except Exception as e:
Api.sendMessage(f"An error occurred: {str(e)}")
```
***
## Examples of Common Commands
### Subscription System
```python
# /subscribe command
Api.sendMessage("Choose your plan:", reply_markup={
"inline_keyboard": [[
{"text": "Basic - Free", "callback_data": "plan_basic"},
{"text": "Premium - $9.99", "callback_data": "plan_premium"}
]]
})
```
```python
# /handler_callback_query command
plan = message.data
if plan == "plan_basic":
User.storeData("subscription", "basic")
Api.sendMessage("✅ Subscribed to Basic plan!")
elif plan == "plan_premium":
User.storeData("subscription", "premium")
Api.sendMessage("✅ Subscribed to Premium plan!")
```
### Points System
```python
# /daily command
last_claim = User.fetchData("last_daily_claim") or 0
current_time = Lib.DateTime.now().timestamp()
# Check if 24 hours have passed
if current_time - last_claim >= 86400:
points = User.res("points")
points.add(100)
User.storeData("last_daily_claim", current_time)
Api.sendMessage("🎁 You received 100 daily points!")
else:
remaining = 86400 - (current_time - last_claim)
hours = int(remaining / 3600)
Api.sendMessage(f"Come back in {hours} hours for your daily reward!")
```
### Quiz System
```python
# /quiz command
questions = [
{"q": "What is 5 + 3?", "a": "8"},
{"q": "Capital of France?", "a": "Paris"},
{"q": "2 × 6 = ?", "a": "12"}
]
User.storeData("quiz_questions", questions)
User.storeData("quiz_index", 0)
User.storeData("quiz_score", 0)
Api.sendMessage(f"Question 1: {questions[0]['q']}")
Bot.waitForInput("quiz_answer")
```
```python
# quiz_answer command
answer = msg
questions = User.fetchData("quiz_questions")
index = User.fetchData("quiz_index")
score = User.fetchData("quiz_score")
correct_answer = questions[index]["a"]
if answer.lower() == correct_answer.lower():
score += 1
User.storeData("quiz_score", score)
Api.sendMessage("✅ Correct!")
else:
Api.sendMessage(f"❌ Wrong! The answer was: {correct_answer}")
index += 1
User.storeData("quiz_index", index)
if index < len(questions):
Api.sendMessage(f"Question {index + 1}: {questions[index]['q']}")
Bot.waitForInput("quiz_answer")
else:
Api.sendMessage(f"🎉 Quiz complete! Your score: {score}/{len(questions)}")
```
***
## Best Practices
### 1. Keep Commands Focused
Each command should do one thing well:
**❌ Bad:**
```python
# /admin command that does everything
if msg == "users":
# Show users...
elif msg == "stats":
# Show stats...
elif msg == "ban":
# Ban user...
# (100+ lines of code)
```
**✅ Good:**
```python
# /admin command
Api.sendMessage("Admin menu:", reply_markup={
"inline_keyboard": [[
{"text": "Users", "callback_data": "admin_users"},
{"text": "Stats", "callback_data": "admin_stats"}
]]
})
# Separate commands for each action
# /admin_users, /admin_stats, etc.
```
### 2. Validate User Input
Always check user input before processing:
```python
# /setage command
Api.sendMessage("Enter your age:")
Bot.waitForInput("save_age")
```
```python
# save_age command
try:
age = int(msg)
if 1 <= age <= 120:
User.storeData("age", age)
Api.sendMessage(f"Age set to {age}")
else:
Api.sendMessage("Please enter a valid age (1-120)")
except ValueError:
Api.sendMessage("Please enter a number")
```
### 3. Provide Clear Feedback
Always let users know what's happening:
```python
# /process command
Api.sendMessage("Processing your request... ⏳")
# Do some work
result = Request.get("https://api.example.com/data")
Api.sendMessage("✅ Done! Here's your data:")
Api.sendMessage(result.text)
```
### 4. Handle Errors Gracefully
Don't let errors crash your bot:
```python
try:
# Risky operation
data = Request.get("https://api.example.com/data").json()
Api.sendMessage(f"Result: {data['value']}")
except Exception as e:
Api.sendMessage("Sorry, something went wrong. Please try again later.")
# Optionally log the error for debugging
Bot.storeData(f"error_{Lib.DateTime.now().timestamp()}", str(e))
```
### 5. Use Descriptive Variable Names
Make your code readable:
**❌ Bad:**
```python
x = msg
y = User.fetchData("p")
z = y + x
```
**✅ Good:**
```python
user_input = msg
current_points = User.fetchData("points")
total_points = current_points + user_input
```
***
## Summary
Commands are the heart of your TeleBot Studio bot. By mastering command creation, user interaction methods, and data management, you can build sophisticated bots that provide great user experiences.
**Key Takeaways:**
* Use `Api` object for Telegram API methods
* Use `Bot` object for platform operations
* Chain commands with `Bot.waitForInput()` for multi-step flows
* Schedule delayed actions with `Bot.scheduleCommand()`
* Store data with `User.storeData()` and retrieve with `User.fetchData()`
* Handle different update types with special handlers
* Always validate user input and handle errors
Start simple, test frequently, and gradually add more features as you become comfortable with TBS!
