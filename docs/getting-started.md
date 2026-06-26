> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/getting-started.md).
# Getting Started with TeleBot Studio
This guide will walk you through everything you need to know to create and launch your first Telegram bot on TeleBot Studio.
\*\*\*
## Account Setup
### Creating Your Account
Getting started with TeleBot Studio is quick and straightforward:
1. \*\*Visit the Website\*\*: Navigate to [TeleBotStudio.com](https://TeleBotStudio.com)
2. \*\*Register\*\*: Click the \*\*"Sign Up"\*\* or \*\*"Register"\*\* button
3. \*\*Enter Your Details\*\*:
\* \*\*Email address\*\*: Use a valid email you have access to
\* \*\*Password\*\*: Choose a strong, secure password
4. \*\*Submit\*\*: Click the register button to create your account
5. \*\*Log In\*\*: Use your email and password to access your dashboard
That's it! No credit card required, no email verification needed, and no additional steps. You're ready to start building bots immediately.
\*\*\*
## Creating Your First Bot
### Obtaining a Telegram Bot Token
Before you can add a bot to TeleBot Studio, you need to get an API token from Telegram:
1. \*\*Open Telegram\*\*: Launch the Telegram app on any device
2. \*\*Find BotFather\*\*: Search for `@BotFather` (the official Telegram bot for creating bots)
3. \*\*Start a Chat\*\*: Send the `/newbot` command to BotFather
4. \*\*Name Your Bot\*\*:
\* BotFather will ask for a name (e.g., "My Awesome Bot")
\* This name will be displayed in chats and contacts
5. \*\*Choose a Username\*\*:
\* Pick a unique username that ends with "bot" (e.g., "MyAwesomeBot" or "my\\_awesome\\_bot")
\* This username will be used to mention and find your bot
6. \*\*Copy the Token\*\*: BotFather will provide an API token that looks like:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
```
\*\*Important\*\*: Keep this token secure! Anyone with this token can control your bot.
### Adding Your Bot to TeleBot Studio
Once you have your API token:
1. \*\*Access Dashboard\*\*: Log in to your TeleBot Studio account
2. \*\*Add New Bot\*\*: Click the \*\*"Add New Bot"\*\* button on your dashboard
3. \*\*Enter Token\*\*: Paste the API token you received from BotFather
4. \*\*Create Bot\*\*: Click \*\*"Create Bot"\*\* or \*\*"Add Bot"\*\*
5. \*\*Confirmation\*\*: Your bot will now appear on your dashboard with its details:
\* Bot username
\* Bot ID
\* Current status
Congratulations! Your bot is now registered on TeleBot Studio.
\*\*\*
## Dashboard Overview
The TeleBot Studio dashboard is your control center for managing bots. Here's what each section does:
### Main Dashboard
When you first log in, you'll see a list of all your bots with:
\* \*\*Bot Username\*\*: The Telegram username of each bot
\* \*\*Bot ID\*\*: The unique identifier for the bot
\* \*\*Status\*\*: Current state (Working, Stopped, etc.)
\* \*\*Quick Actions\*\*: Buttons to manage each bot
### Bot Management Menu
Click on any bot to access its management interface with these sections:
#### 1. Home / Status (Main Menu)
Shows your bot's current status and overview:
\* \*\*Working\*\*: Bot is active and processing user messages
\* \*\*Stopped\*\*: Bot is inactive and not responding to users
\* \*\*Created\*\*: Newly added bot that hasn't been started yet
This is where you can start or stop your bot.
#### 2. Commands Menu
The Commands section is where you'll spend most of your time developing your bot:
\* \*\*View All Commands\*\*: See a list of all commands you've created
\* \*\*Add Command\*\*: Create a new command with TBS code
\* \*\*Edit Command\*\*: Modify existing commands
\* \*\*Delete Command\*\*: Remove commands you no longer need
Each command consists of:
\* \*\*Command Name\*\*: The trigger (e.g., `/start`, `/help`, or `\*` for wildcard)
\* \*\*Code\*\*: The TBS code that runs when the command is triggered
#### 3. Errors Menu
Monitor and debug your bot's errors:
\* \*\*Error Logs\*\*: View detailed error messages
\* \*\*Error Types\*\*: See what kind of errors are occurring
\* \*\*Timestamps\*\*: Know when errors happened
\* \*\*Debug Info\*\*: Get context to help fix issues
#### 4. Settings Menu
Configure your bot's settings:
\* \*\*Bot Token\*\*: Update or change your bot's API token
\* \*\*Bot Information\*\*: View basic bot details
\* \*\*Advanced Options\*\*: Access additional configuration
\*\*\*
## Creating Your First Command
Commands are how your bot responds to users. Let's create a simple `/start` command:
### Step 1: Access Commands Menu
1. Click on your bot in the dashboard
2. Navigate to the \*\*Commands\*\* section (tool icon)
3. Click \*\*"Add Command"\*\*
### Step 2: Define the Command
1. \*\*Command Name\*\*: Enter `/start`
2. \*\*Code Editor\*\*: Write your TBS code:
```python
# Get user's first name
name = message.from\_user.first\_name
# Send welcome message
Api.sendMessage(f"Hello {name}! Welcome to my bot.")
Api.sendMessage("Use /help to see available commands.")
```
3. \*\*Save\*\*: Click the save or create button
### Step 3: Test Your Bot
1. Go to \*\*Home/Status\*\* menu
2. Click \*\*"Start Bot"\*\* to activate it
3. Open Telegram and find your bot by its username
4. Send `/start` to your bot
5. You should receive the welcome message!
\*\*\*
## Understanding Command Types
TeleBot Studio supports several types of commands:
### Regular Commands
Commands that start with `/` are triggered when users type them:
```python
# /start command
Api.sendMessage("Bot started!")
# /help command
Api.sendMessage("Available commands:\n/start - Start the bot\n/help - Show this message")
```
### Wildcard Command (`\*`)
The wildcard command catches any message that doesn't match other commands:
```python
# \* command
Api.sendMessage("Sorry, I didn't understand that. Type /help for available commands.")
```
### At Handler (`@`)
The `@` command runs before every other command. Use it for logging or preprocessing:
```python
# @ command
# Log user activity
user\_id = message.from\_user.id
Api.sendMessage(f"Processing your request...")
```
### Special Update Handlers
Handle specific Telegram update types:
\* `/handler\_photo` - Triggered when users send photos
\* `/handler\_document` - Triggered when users send documents
\* `/handler\_callback\_query` - Triggered by inline keyboard callbacks
```python
# /handler\_photo command
Api.sendMessage("Thanks for the photo!")
```
\*\*\*
## Basic Bot Examples
### Simple Echo Bot
Create a bot that repeats what users say:
```python
# \* command (wildcard)
user\_message = message.text
Api.sendMessage(f"You said: {user\_message}")
```
### Help Menu Bot
```python
# /help command
help\_text = """
📋 \*\*Available Commands:\*\*
/start - Start the bot
/help - Show this help menu
/about - Learn about this bot
/contact - Get contact information
"""
Api.sendMessage(help\_text, parse\_mode="Markdown")
```
### Interactive Bot with User Input
```python
# /ask command
Api.sendMessage("What's your name?")
Bot.waitForInput("save\_name")
```
```python
# save\_name command
user\_name = msg
User.storeData("name", user\_name)
Api.sendMessage(f"Nice to meet you, {user\_name}!")
```
\*\*\*
## Starting and Stopping Your Bot
### Starting Your Bot
1. Navigate to your bot's \*\*Home/Status\*\* menu
2. Click \*\*"Start Bot"\*\* button
3. Wait for confirmation that the bot is running
4. Status will change to \*\*"Working"\*\*
Your bot is now live and will respond to users!
### Stopping Your Bot
1. Go to \*\*Home/Status\*\* menu
2. Click \*\*"Stop Bot"\*\* button
3. Status will change to \*\*"Stopped"\*\*
\*\*When to stop your bot:\*\*
\* Making major changes to commands
\* Testing new features safely
\* Temporarily disabling the bot
\*\*Note\*\*: You can edit commands while the bot is running, but stopping it prevents users from triggering old code during updates.
\*\*\*
## Best Practices for Beginners
### 1. Start Simple
Begin with basic commands before adding complex features:
\* `/start` - Welcome message
\* `/help` - Command list
\* `/about` - Bot information
### 2. Test Frequently
After creating or editing commands:
\* Test immediately in Telegram
\* Try different inputs
\* Check error logs if something doesn't work
### 3. Use Descriptive Names
Give commands clear, obvious names:
\* ✅ `/subscribe` - Good, clear purpose
\* ❌ `/s` - Bad, unclear meaning
### 4. Handle Errors Gracefully
Use try-except blocks for potentially failing code:
```python
try:
# Risky operation
result = Request.get("https://api.example.com/data")
Api.sendMessage(f"Data: {result.json()}")
except Exception as e:
Api.sendMessage("Sorry, something went wrong. Please try again later.")
```
### 5. Store User Data Wisely
Use User.storeData() for user-specific information:
```python
# Store user preferences
User.storeData("language", "en")
User.storeData("notifications", True)
# Retrieve later
language = User.fetchData("language")
```
\*\*\*
## Common Issues and Solutions
### Bot Not Responding
\*\*Problem\*\*: Bot doesn't reply to messages
\*\*Solutions\*\*:
\* Check if bot status is "Working"
\* Verify the command name matches what users are typing
\* Check error logs for issues
\* Ensure your Telegram bot token is valid
### Commands Not Saving
\*\*Problem\*\*: Changes to commands don't take effect
\*\*Solutions\*\*:
\* Click save after editing
\* Refresh the dashboard
\* Check for syntax errors in your code
### Token Errors
\*\*Problem\*\*: Invalid token or authentication errors
\*\*Solutions\*\*:
\* Verify token is copied correctly (no extra spaces)
\* Get a new token from @BotFather if needed
\* Update token in Settings menu
\*\*\*
## Next Steps
Now that you have your first bot running, explore these topics:
1. \*\*Learn TBS Syntax\*\*: Master the TeleBot Syntax language for more complex bots
2. \*\*Use Libraries\*\*: Integrate payments, blockchain, and external APIs
3. \*\*Command Chaining\*\*: Create multi-step user interactions
4. \*\*Resource Management\*\*: Track points, scores, and user data
5. \*\*Advanced Features\*\*: Broadcasting, webhooks, and bot management
Check out the other documentation sections for detailed guides on these topics!
\*\*\*
## Getting Help
Need assistance?
\* \*\*Community\*\*: Join our help group at 
\* \*\*Documentation\*\*: Browse other guides for specific features
\* \*\*Error Logs\*\*: Check the Errors menu in your dashboard for debugging information
Welcome to the TeleBot Studio community! We're excited to see what you'll build.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/getting-started.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.