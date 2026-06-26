> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/commands-in-tbs.md).
# Commands in TBS
Commands are the core building blocks of every bot on TeleBot Studio. They define how your bot responds to user inputs, processes data, and performs actions. This comprehensive guide explains everything you need to know about creating, managing, and optimizing commands using TeleBot Syntax (TBS).
\*\*\*
## What Are Commands?
A \*\*command\*\* is a trigger that executes specific code when a user sends a particular message to your bot. Commands can:
\* Respond to user messages with text, images, or files
\* Process and store user data
\* Interact with external APIs and services
\* Chain together to create complex workflows
\* Schedule future actions
\* Manage bot state and user sessions
\*\*Examples of common commands:\*\*
\* `/start` - Welcome new users
\* `/help` - Display available commands
\* `/subscribe` - Handle subscription requests
\* `\*` - Catch unrecognized inputs (wildcard)
\*\*\*
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
first\_name = message.from\_user.first\_name
# Get user ID
user\_id = message.from\_user.id
# Get chat ID
chat\_id = message.chat.id
# Send personalized message
Api.sendMessage(f"Hello {first\_name}! Your ID is {user\_id}.")
```
### Handling Command Parameters
Users can send parameters with commands (e.g., `/start 12345`). Access them using the `params` variable:
```python
# /start command
if params:
referrer\_id = params
Api.sendMessage(f"You were referred by user {referrer\_id}!")
User.storeData("referrer", referrer\_id)
else:
Api.sendMessage("Welcome! Use /help to get started.")
```
\*\*\*
## Managing User Interactions
TBS provides powerful methods for creating interactive bot experiences.
### 1. Bot.waitForInput()
Wait for the user's next message and route it to a specific command.
\*\*Syntax:\*\*
```python
Bot.waitForInput(command, \*\*options)
```
\*\*Parameters:\*\*
\* `command` (Required): Name of the command to execute next
\* `options` (Optional): Data to pass to the next command
\*\*Example - Collecting User Email:\*\*
```python
# /register command
Api.sendMessage("Please enter your email address:")
Bot.waitForInput("process\_email")
```
```python
# process\_email command
email = msg
User.storeData("email", email)
Api.sendMessage(f"Thank you! Your email {email} has been saved.")
```
\*\*Example - With Options:\*\*
```python
# /quiz command
Api.sendMessage("What is 2 + 2?")
Bot.waitForInput("check\_answer", correct\_answer=4, question\_id=1)
```
```python
# check\_answer command
user\_answer = int(msg)
correct = options.get("correct\_answer")
if user\_answer == correct:
Api.sendMessage("Correct! ✅")
else:
Api.sendMessage(f"Wrong! The answer was {correct}.")
```
### 2. Bot.run()
Execute another command immediately.
\*\*Syntax:\*\*
```python
Bot.run(command, \*\*options)
```
\*\*Parameters:\*\*
\* `command` (Required): Name of the command to run
\* `options` (Optional): Data to pass to the command
\*\*Example - Command Redirection:\*\*
```python
# /info command
Api.sendMessage("Redirecting you to the help menu...")
Bot.run("help")
```
\*\*Example - With Options:\*\*
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
\*\*Syntax:\*\*
```python
Bot.scheduleCommand(delay\_seconds, command, user\_id=None, chat\_id=None, params=None, \*\*options)
```
\*\*Parameters:\*\*
\* `delay\_seconds` (Required): Time in seconds before execution (0.1 to 31536000)
\* `command` (Required): Name of the command to run
\* `user\_id` (Optional): Target user ID
\* `chat\_id` (Optional): Target chat ID
\* `params` (Optional): Parameters to pass
\* `options` (Optional): Additional data to pass
\*\*Example - Reminder System:\*\*
```python
# /remind command
Api.sendMessage("I'll remind you in 10 seconds!")
Bot.scheduleCommand(10, "send\_reminder")
```
```python
# send\_reminder command
Api.sendMessage("⏰ This is your reminder!")
```
\*\*Example - Delayed Welcome:\*\*
```python
# /start command
Api.sendMessage("Welcome! Let me prepare something for you...")
Bot.scheduleCommand(3, "welcome\_bonus")
```
```python
# welcome\_bonus command
Api.sendMessage("🎁 Here's a welcome bonus!")
User.res("coins").add(100)
```
\*\*\*
## Command Types
### Regular Commands
Standard commands start with `/` and are triggered when users type them:
```python
# /start command
name = message.from\_user.first\_name
Api.sendMessage(f"Welcome to the bot, {name}!")
```
```python
# /help command
help\_message = """
\*\*Available Commands:\*\*
/start - Start the bot
/help - Show this help menu
/profile - View your profile
/settings - Configure bot settings
"""
Api.sendMessage(help\_message, parse\_mode="Markdown")
```
### Wildcard Command (`\*`)
The wildcard command catches any message that doesn't match defined commands. This is useful for:
\* Default responses to unknown commands
\* Natural language processing
\* Catching typos
```python
# \* command
user\_message = message.text
Api.sendMessage(f"I don't understand '{user\_message}'. Try /help for available commands.")
```
\*\*Advanced Wildcard Example:\*\*
```python
# \* command - AI Chatbot
user\_text = message.text
# Check for keywords
if "price" in user\_text.lower():
Api.sendMessage("Our pricing starts at $10/month. Type /pricing for details.")
elif "help" in user\_text.lower():
Bot.run("help")
else:
Api.sendMessage("I'm not sure what you mean. Type /help to see what I can do!")
```
### At Handler Command (`@`)
The `@` command executes \*\*before\*\* any other command. Use it for:
\* Logging user activity
\* Checking user permissions
\* Preprocessing messages
\* Analytics tracking
```python
# @ command
user\_id = message.from\_user.id
username = message.from\_user.username or "No username"
# Log activity
Bot.res("total\_messages").add(1)
# You can optionally send a message
# Api.sendMessage("Processing your request...")
```
\*\*Important\*\*: The `@` handler runs first, then the actual command runs.
### Special Update Handlers
Handle specific types of Telegram updates:
#### Photo Handler
```python
# /handler\_photo command
Api.sendMessage("Nice photo! Thanks for sharing.")
# Access photo info
photo = message.photo[-1] # Get largest photo
file\_id = photo.file\_id
Api.sendMessage(f"Photo file ID: {file\_id}")
```
#### Document Handler
```python
# /handler\_document command
doc = message.document
file\_name = doc.file\_name
file\_size = doc.file\_size
Api.sendMessage(f"Received document: {file\_name} ({file\_size} bytes)")
```
#### Callback Query Handler
```python
# /handler\_callback\_query command
callback\_data = message.data
Api.answerCallbackQuery("Button clicked!")
if callback\_data == "option\_1":
Api.sendMessage("You selected Option 1")
elif callback\_data == "option\_2":
Api.sendMessage("You selected Option 2")
```
\*\*\*
## Using Global Variables
TBS provides several pre-defined variables:
### Message Variables
```python
# Full message object
full\_message = message
# User information
user\_id = message.from\_user.id
username = message.from\_user.username
first\_name = message.from\_user.first\_name
last\_name = message.from\_user.last\_name
# Chat information
chat\_id = message.chat.id
chat\_type = message.chat.type # "private", "group", "supergroup", "channel"
# Message content
message\_text = message.text
message\_id = message.message\_id
```
### Shorthand Variables
```python
# msg - The message text or caption
user\_input = msg
# u - User ID (shorthand)
current\_user = u
# command - Current command name
current\_cmd = command
# params - Command parameters
command\_params = params
# options - Data passed from previous command
passed\_data = options
# update\_type - Type of update
update\_kind = update\_type # "message", "callback\_query", "photo", etc.
```
\*\*\*
## Command Chaining
Chain commands together to create multi-step workflows:
### Example: User Registration Flow
\*\*Step 1: Get Name\*\*
```python
# /register command
Api.sendMessage("Let's get you registered!")
Api.sendMessage("First, what's your name?")
Bot.waitForInput("get\_name")
```
\*\*Step 2: Get Email\*\*
```python
# get\_name command
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email address?")
Bot.waitForInput("get\_email")
```
\*\*Step 3: Get Age\*\*
```python
# get\_email command
email = msg
User.storeData("email", email)
Api.sendMessage("Great! How old are you?")
Bot.waitForInput("get\_age")
```
\*\*Step 4: Complete Registration\*\*
```python
# get\_age command
age = msg
User.storeData("age", age)
name = User.fetchData("name")
email = User.fetchData("email")
Api.sendMessage(f"""
✅ \*\*Registration Complete!\*\*
Name: {name}
Email: {email}
Age: {age}
Welcome to our community!
""", parse\_mode="Markdown")
```
\*\*\*
## Data Management in Commands
### Storing User Data
```python
# Store various data types
User.storeData("username", "john\_doe")
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
User.removeData("temp\_data")
# Or clear when user logs out
User.removeData("session\_token")
User.removeData("login\_time")
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
\*\*\*
## Advanced Command Techniques
### Conditional Logic
```python
# /profile command
user\_level = User.fetchData("level") or 1
if user\_level >= 10:
Api.sendMessage("🌟 You're a VIP user!")
elif user\_level >= 5:
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
message = "🏆 \*\*Leaderboard:\*\*\n\n"
for i, user in enumerate(users, 1):
message += f"{i}. {user['name']} - {user['score']} points\n"
Api.sendMessage(message, parse\_mode="Markdown")
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
\*\*\*
## Examples of Common Commands
### Subscription System
```python
# /subscribe command
Api.sendMessage("Choose your plan:", reply\_markup={
"inline\_keyboard": [[
{"text": "Basic - Free", "callback\_data": "plan\_basic"},
{"text": "Premium - $9.99", "callback\_data": "plan\_premium"}
]]
})
```
```python
# /handler\_callback\_query command
plan = message.data
if plan == "plan\_basic":
User.storeData("subscription", "basic")
Api.sendMessage("✅ Subscribed to Basic plan!")
elif plan == "plan\_premium":
User.storeData("subscription", "premium")
Api.sendMessage("✅ Subscribed to Premium plan!")
```
### Points System
```python
# /daily command
last\_claim = User.fetchData("last\_daily\_claim") or 0
current\_time = Lib.DateTime.now().timestamp()
# Check if 24 hours have passed
if current\_time - last\_claim >= 86400:
points = User.res("points")
points.add(100)
User.storeData("last\_daily\_claim", current\_time)
Api.sendMessage("🎁 You received 100 daily points!")
else:
remaining = 86400 - (current\_time - last\_claim)
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
User.storeData("quiz\_questions", questions)
User.storeData("quiz\_index", 0)
User.storeData("quiz\_score", 0)
Api.sendMessage(f"Question 1: {questions[0]['q']}")
Bot.waitForInput("quiz\_answer")
```
```python
# quiz\_answer command
answer = msg
questions = User.fetchData("quiz\_questions")
index = User.fetchData("quiz\_index")
score = User.fetchData("quiz\_score")
correct\_answer = questions[index]["a"]
if answer.lower() == correct\_answer.lower():
score += 1
User.storeData("quiz\_score", score)
Api.sendMessage("✅ Correct!")
else:
Api.sendMessage(f"❌ Wrong! The answer was: {correct\_answer}")
index += 1
User.storeData("quiz\_index", index)
if index < len(questions):
Api.sendMessage(f"Question {index + 1}: {questions[index]['q']}")
Bot.waitForInput("quiz\_answer")
else:
Api.sendMessage(f"🎉 Quiz complete! Your score: {score}/{len(questions)}")
```
\*\*\*
## Best Practices
### 1. Keep Commands Focused
Each command should do one thing well:
\*\*❌ Bad:\*\*
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
\*\*✅ Good:\*\*
```python
# /admin command
Api.sendMessage("Admin menu:", reply\_markup={
"inline\_keyboard": [[
{"text": "Users", "callback\_data": "admin\_users"},
{"text": "Stats", "callback\_data": "admin\_stats"}
]]
})
# Separate commands for each action
# /admin\_users, /admin\_stats, etc.
```
### 2. Validate User Input
Always check user input before processing:
```python
# /setage command
Api.sendMessage("Enter your age:")
Bot.waitForInput("save\_age")
```
```python
# save\_age command
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
Bot.storeData(f"error\_{Lib.DateTime.now().timestamp()}", str(e))
```
### 5. Use Descriptive Variable Names
Make your code readable:
\*\*❌ Bad:\*\*
```python
x = msg
y = User.fetchData("p")
z = y + x
```
\*\*✅ Good:\*\*
```python
user\_input = msg
current\_points = User.fetchData("points")
total\_points = current\_points + user\_input
```
\*\*\*
## Summary
Commands are the heart of your TeleBot Studio bot. By mastering command creation, user interaction methods, and data management, you can build sophisticated bots that provide great user experiences.
\*\*Key Takeaways:\*\*
\* Use `Api` object for Telegram API methods
\* Use `Bot` object for platform operations
\* Chain commands with `Bot.waitForInput()` for multi-step flows
\* Schedule delayed actions with `Bot.scheduleCommand()`
\* Store data with `User.storeData()` and retrieve with `User.fetchData()`
\* Handle different update types with special handlers
\* Always validate user input and handle errors
Start simple, test frequently, and gradually add more features as you become comfortable with TBS!
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/commands-in-tbs.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.