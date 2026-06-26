> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/glossary-and-key-concepts.md).
# Glossary and Key Concepts
This comprehensive glossary provides definitions and explanations of key terms and concepts in TeleBot Studio. Understanding these terms is essential for effectively building and managing bots on the platform.
\*\*\*
## Introduction
TeleBot Studio uses specialized terminology to define its functionality and features. This glossary serves as a quick reference guide, ensuring you have a clear understanding of the platform's core elements, advanced features, and technical concepts.
\*\*\*
## Core Concepts
### TeleBot Studio (TBS)
\*\*Definition:\*\* A comprehensive platform for building, hosting, and managing Telegram bots without server management. TeleBot Studio provides a complete development environment with built-in libraries, secure execution, and advanced features.
\*\*Key Features:\*\*
\* Free hosting with no limits
\* Python-like bot development language
\* Built-in libraries for blockchain, AI, payments
\* No server configuration required
\*\*\*
### TeleBot Syntax (TBS)
\*\*Definition:\*\* The custom Python-like programming language designed specifically for TeleBot Studio. TBS simplifies bot development by offering built-in libraries, pre-defined variables, and a secure, sandboxed execution environment.
\*\*Example:\*\*
```python
Api.sendMessage("Welcome to my bot!")
User.storeData("name", "John")
points = User.res("points")
points.add(50)
```
\*\*Key Characteristics:\*\*
\* Python-like syntax
\* No import statements required
\* Pre-loaded libraries and utilities
\* Secure sandboxed execution
\* Maximum execution time: 160 seconds
\*\*\*
### Bot API Token
\*\*Definition:\*\* A unique authentication token provided by Telegram for managing and controlling a bot. This token is required to connect your bot to TeleBot Studio.
\*\*How to Get:\*\*
1. Message @BotFather on Telegram
2. Use `/newbot` command
3. Follow instructions to create bot
4. Copy the provided token
\*\*Example Token Format:\*\*
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
\*\*Security Note:\*\* Never share your bot token publicly as it grants full control over your bot.
\*\*\*
## Commands
### Command
\*\*Definition:\*\* A trigger that executes specific logic when a user sends a corresponding message. Commands typically start with `/` (e.g., `/start`, `/help`) but can also be plain text.
\*\*Types of Commands:\*\*
\* \*\*Standard Commands:\*\* `/start`, `/help`, `/settings`
\* \*\*Wildcard Command (`\*`):\*\* Catches unmatched messages
\* \*\*At Handler (`@`):\*\* Executes before all other commands
\* \*\*Custom Commands:\*\* Any user-defined command
\*\*Example:\*\*
```python
# /start command
Api.sendMessage("Welcome! Use /help for assistance.")
# /help command
Api.sendMessage("Available commands:\n/start - Start the bot\n/help - Show this help")
```
\*\*\*
### Wildcard Command (`\*`)
\*\*Definition:\*\* A special command that catches any message not matching other defined commands. Essential for handling unknown inputs or creating conversational fallbacks.
\*\*Use Cases:\*\*
\* Default responses
\* Error handling
\* Logging unrecognized commands
\* Natural language processing fallback
\*\*Example:\*\*
```python
Api.sendMessage("I didn't understand that. Type /help for available commands.")
```
\*\*\*
### At Handler (`@`)
\*\*Definition:\*\* A special command that executes before any other command. Used for preprocessing, logging, authentication, or setting up global conditions.
\*\*Use Cases:\*\*
\* Activity logging
\* Authentication checks
\* Rate limiting
\* Message validation
\*\*Example:\*\*
```python
# Log all user activity
Bot.res("total\_messages").add(1)
User.storeData("last\_active", time.time())
# Execution continues to matched command
```
\*\*\*
## Objects and Classes
### Api Object
\*\*Definition:\*\* The object used for all Telegram Bot API methods. Provides direct access to Telegram's messaging and bot management functionality.
\*\*Common Methods:\*\*
\* `Api.sendMessage()` - Send text messages
\* `Api.sendPhoto()` - Send images
\* `Api.sendDocument()` - Send files
\* `Api.sendPoll()` - Create polls
\* `Api.editMessageText()` - Edit messages
\*\*Example:\*\*
```python
Api.sendMessage("Hello, world!")
Api.sendPhoto("https://example.com/image.jpg", caption="Check this out!")
```
\*\*\*
### Bot Object
\*\*Definition:\*\* The object for TeleBot Studio platform-specific operations like data storage, scheduling, broadcasting, and bot management.
\*\*Common Methods:\*\*
\* `Bot.storeData()` / `Bot.fetchData()` - Bot-level data storage
\* `Bot.scheduleCommand()` - Schedule commands
\* `Bot.sendBroadcast()` - Send broadcasts
\* `Bot.getInfo()` - Get bot information
\* `Bot.createCaptcha()` - Generate CAPTCHA
\*\*Example:\*\*
```python
Bot.storeData("total\_users", 1000)
Bot.scheduleCommand(3600, "send\_reminder")
Bot.sendBroadcast(function="sendMessage", text="Announcement!")
```
\*\*\*
### User Object
\*\*Definition:\*\* Manages user-specific data and resources for individual users interacting with your bot.
\*\*Common Methods:\*\*
\* `User.storeData()` / `User.fetchData()` - User data storage
\* `User.res()` - User resource management
\* `User.resOf()` - Access another user's resources
\*\*Example:\*\*
```python
User.storeData("language", "en")
points = User.res("points")
points.add(50)
```
\*\*\*
### Account Object
\*\*Definition:\*\* Manages account-level data shared across all bots in your TeleBot Studio account.
\*\*Common Methods:\*\*
\* `Account.storeData()` / `Account.fetchData()` - Account data
\* `Account.res()` - Account resources
\* Account management operations
\*\*Example:\*\*
```python
Account.storeData("api\_key", "secret\_key")
global\_config = Account.fetchData("config")
```
\*\*\*
## Data Management
### Data Storage
\*\*Definition:\*\* The system for persisting information across bot interactions at different scopes (user, bot, account).
\*\*Storage Levels:\*\*
\*\*User-Level Storage:\*\*
```python
User.storeData("name", "John")
User.storeData("email", "john@example.com")
name = User.fetchData("name")
User.removeData("temp\_data")
```
\*\*Bot-Level Storage:\*\*
```python
Bot.storeData("total\_users", 1000)
total = Bot.fetchData("total\_users")
Bot.removeData("old\_config")
```
\*\*Account-Level Storage:\*\*
```python
Account.storeData("api\_key", "key\_value")
key = Account.fetchData("api\_key")
Account.removeData("temp")
```
\*\*Storage Limits:\*\*
\* Maximum size per entry: 10MB
\* No limit on number of entries
\*\*\*
### Resources
\*\*Definition:\*\* Numeric values that can be tracked and modified per user or globally. Perfect for points, credits, currency, or any numeric tracking.
\*\*Operations:\*\*
\* `add()` - Increment value
\* `cut()` - Decrement value
\* `set()` - Set specific value
\* `reset()` - Reset to zero
\* `value()` - Get current value
\*\*User Resources:\*\*
```python
points = User.res("points")
points.add(50) # Add 50 points
points.cut(10) # Subtract 10 points
points.set(100) # Set to 100
current = points.value() # Get current value
points.reset() # Reset to 0
```
\*\*Bot Resources (Global):\*\*
```python
total\_sales = Bot.res("total\_sales")
total\_sales.add(1)
Api.sendMessage(f"Total sales: {total\_sales.value()}")
```
\*\*Another User's Resources:\*\*
```python
target\_points = User.resOf("points", target\_user\_id)
Api.sendMessage(f"User has {target\_points.value()} points")
```
\*\*\*
## Broadcasting
### Broadcast
\*\*Definition:\*\* A feature that sends messages or executes commands across multiple users simultaneously. Essential for announcements, notifications, and mass communications.
\*\*Types:\*\*
\*\*Function-Based:\*\*
```python
Bot.sendBroadcast(
function="sendMessage",
text="Important announcement!"
)
```
\*\*Command-Based:\*\*
```python
Bot.sendBroadcast(command="send\_personalized\_message")
```
\*\*Code-Based:\*\*
```python
Bot.sendBroadcast(code="Api.sendMessage('Hello everyone!')")
```
\*\*Broadcast Limits:\*\*
\* Maximum 2 simultaneous broadcasts per bot
\* Maximum 1000 simultaneous broadcasts globally
\*\*Management:\*\*
```python
# List broadcasts
broadcasts = Bot.listBroadcasts()
# Check status
status = Bot.broadcastStatus(broadcast\_id="123")
# Pause broadcast
Bot.pauseBroadcast(broadcast\_id="123")
# Cancel broadcast
Bot.cancelBroadcast(broadcast\_id="123")
```
\*\*\*
## Advanced Features
### Webhook
\*\*Definition:\*\* A URL endpoint that allows external systems to trigger bot commands in real-time. Webhooks enable integration with payment processors, notification services, and other bots.
\*\*Generation:\*\*
```python
# Basic webhook
webhook\_url = Lib.Webhook.getUrlFor("process\_data", user\_id=u)
# Cross-bot webhook
webhook = Lib.Webhook.getUrlFor(
"notify\_user",
bot\_id="other\_bot\_id",
api\_key="other\_bot\_api\_key",
user\_id=u
)
```
\*\*Handling Webhook Data:\*\*
```python
# In webhook command
webhook\_data = options
event\_type = webhook\_data.get('type')
data = webhook\_data.get('data')
Api.sendMessage(f"Received: {data}")
```
\*\*\*
### Command Chaining
\*\*Definition:\*\* The process of linking multiple commands together to create multi-step workflows.
\*\*Implementation:\*\*
```python
# Step 1
Api.sendMessage("What's your name?")
Bot.waitForInput("get\_name")
# Step 2 (get\_name command)
name = msg
User.storeData("name", name)
Api.sendMessage("What's your email?")
Bot.waitForInput("get\_email")
# Step 3 (get\_email command)
email = msg
User.storeData("email", email)
Api.sendMessage("Registration complete!")
```
\*\*\*
### Scheduled Commands
\*\*Definition:\*\* Commands that execute after a specified delay, enabling reminders, follow-ups, and timed operations.
\*\*Syntax:\*\*
```python
Bot.scheduleCommand(delay\_seconds, command\_name, \*\*options)
```
\*\*Constraints:\*\*
\* Minimum delay: 0.1 seconds
\* Maximum delay: 31,536,000 seconds (1 year)
\* Maximum 100 scheduled commands per user
\* Rate limit: 5 executions per 5 seconds for ultra-fast commands (<0.4s)
\*\*Examples:\*\*
```python
# 1 hour reminder
Bot.scheduleCommand(3600, "send\_reminder")
# Quick follow-up
Bot.scheduleCommand(0.5, "send\_confirmation")
# Daily notification
Bot.scheduleCommand(86400, "daily\_digest")
```
\*\*\*
### Bot Transfer
\*\*Definition:\*\* The process of creating a copy of your bot and transferring it to another TeleBot Studio account. The original bot remains in your account.
\*\*Syntax:\*\*
```python
Bot.transfer(email, bot\_id, bot\_token=None, run\_now=False)
```
\*\*Example:\*\*
```python
result = Bot.transfer(
email="recipient@example.com",
bot\_id=bot\_id,
bot\_token="YOUR\_BOT\_TOKEN",
run\_now=True
)
```
\*\*Important:\*\* This creates a copy of the bot, not transfers ownership. Your original bot remains functional.
\*\*\*
## Libraries
### Lib.EVM
\*\*Definition:\*\* Library for Ethereum and EVM-compatible blockchain operations including transactions, token transfers, and wallet management.
\*\*Supported Networks:\*\* 31+ including Ethereum, BSC, Polygon, Avalanche, Arbitrum, Optimism, and more
\*\*Example:\*\*
```python
# Store private key
Lib.EVM.storeKey("private\_key")
# Send native coin
tx = Lib.EVM.sendCoin(network="ethereum", to="0x...", value=0.1)
# Send ERC-20 token
tx = Lib.EVM.sendToken(
network="ethereum",
to="0x...",
value=100,
contract\_address="0x..." # Token contract
)
```
\*\*\*
### Lib.TON
\*\*Definition:\*\* Library for The Open Network (TON) blockchain integration including wallet creation, balance checking, transactions, and TON Connect.
\*\*Example:\*\*
```python
# Create wallet
wallet = Lib.TON.createWallet()
Api.sendMessage(f"Address: {wallet['address']}")
# Check balance
balance = Lib.TON.balance("EQD...")
# Send TON
Lib.TON.send(to\_address="EQD...", amount=0.5, comment="Payment")
```
\*\*\*
### Lib.AI
\*\*Definition:\*\* Unified AI library supporting OpenAI and Google Gemini for chat completions and AI assistants.
\*\*Example:\*\*
```python
# OpenAI
client = Lib.AI.client(provider="openai", apiKey="KEY")
response = client.chat(
model="gpt-4",
messages=[{"role": "user", "content": msg}]
)
# Gemini
client = Lib.AI.client(provider="gemini", apiKey="KEY")
response = client.chat(
model="gemini-2.0-flash",
messages=[{"role": "user", "content": msg}]
)
```
\*\*\*
### Lib.DateTime
\*\*Definition:\*\* Library for date and time operations including current time, timezone conversions, and timestamps.
\*\*Methods:\*\*
```python
# Current UTC time
current = Lib.DateTime.utcnow()
# Timezone-specific time
tokyo\_time = Lib.DateTime.now("Asia/Tokyo")
# UNIX timestamp
timestamp = Lib.DateTime.time()
```
\*\*\*
### Lib.Random
\*\*Definition:\*\* Library for generating random numbers, strings, and values.
\*\*Methods:\*\*
```python
# Random integer
num = Lib.Random.integer(1, 100)
# Random string
text = Lib.Random.string(16)
# Random decimal
decimal = Lib.Random.decimal(0.0, 1.0)
# Random ASCII
ascii\_str = Lib.Random.ascii(20)
```
\*\*\*
### Lib.CSV
\*\*Definition:\*\* Library for creating, reading, and managing CSV files for structured data storage.
\*\*Example:\*\*
```python
csv = Lib.CSV.Table("data.csv")
csv.create(["name", "email", "points"])
csv.insert({"name": "John", "email": "john@example.com", "points": 100})
row = csv.row(0)
csv.update(0, {"points": 150})
csv.delete(1)
```
\*\*\*
### Lib.Webhook
\*\*Definition:\*\* Library for generating webhook URLs for command invocation and external integrations.
\*\*Syntax:\*\*
```python
Lib.Webhook.getUrlFor(command, user\_id=None, chat\_id=None, bot\_id=None, api\_key=None, \*\*options)
```
\*\*Example:\*\*
```python
webhook = Lib.Webhook.getUrlFor("process\_payment", user\_id=u)
```
\*\*\*
### Lib.Oxapay
\*\*Definition:\*\* Payment processing library for cryptocurrency and fiat payments through Oxapay merchant services.
\*\*Example:\*\*
```python
client = Lib.Oxapay.post("MERCHANT\_API\_KEY")
invoice = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Premium subscription"
})
Api.sendMessage(f"Pay: {invoice['url']}")
```
\*\*\*
### Lib.Crypto
\*\*Definition:\*\* Cryptocurrency utility library for price conversions and crypto operations.
\*\*Example:\*\*
```python
# Convert between cryptocurrencies
result = Lib.Crypto.convert(amount=1, from\_currency="BTC", to\_currency="USD")
# Get current price
price = Lib.Crypto.get\_price("BTC", "USD")
```
\*\*\*
### Request Module
\*\*Definition:\*\* HTTP client for making API requests to external services.
\*\*Methods:\*\*
\* `Request.get()` - GET request
\* `Request.post()` - POST request
\* `Request.put()` - PUT request
\* `Request.delete()` - DELETE request
\* `Request.patch()` - PATCH request
\*\*Example:\*\*
```python
response = Request.get("https://api.example.com/data")
if response.ok:
data = response.json()
Api.sendMessage(f"Result: {data}")
```
\*\*\*
## Global Variables
### msg
\*\*Definition:\*\* Contains the raw text content of the incoming message from the user.
\*\*Example:\*\*
```python
user\_input = msg
Api.sendMessage(f"You said: {user\_input}")
```
\*\*\*
### message
\*\*Definition:\*\* Contains the complete message object with all metadata including sender info, chat details, and message content.
\*\*Example:\*\*
```python
first\_name = message.from\_user.first\_name
chat\_id = message.chat.id
Api.sendMessage(f"Hello {first\_name}!")
```
\*\*\*
### u
\*\*Definition:\*\* The user ID of the current user interacting with the bot.
\*\*Example:\*\*
```python
Api.sendMessage(f"Your user ID is: {u}")
User.storeData("user\_id", u)
```
\*\*\*
### params
\*\*Definition:\*\* Parameters passed to a command via deep links or command arguments.
\*\*Example:\*\*
```python
# User clicks: t.me/yourbot?start=referral\_123
referrer\_id = params # Contains: "referral\_123"
Api.sendMessage(f"Referred by: {referrer\_id}")
```
\*\*\*
### options
\*\*Definition:\*\* Additional data passed to a command, typically from webhooks or scheduled commands.
\*\*Example:\*\*
```python
# In webhook command
webhook\_data = options
amount = webhook\_data.get('amount')
Api.sendMessage(f"Amount: {amount}")
```
\*\*\*
### bot\\_id
\*\*Definition:\*\* The unique identifier of the current bot.
\*\*Example:\*\*
```python
Api.sendMessage(f"Bot ID: {bot\_id}")
```
\*\*\*
### bot\\_token
\*\*Definition:\*\* The Telegram Bot API token for the current bot.
\*\*Note:\*\* Handle with care - never expose publicly.
\*\*\*
### update\\_type
\*\*Definition:\*\* Indicates the type of the current Telegram update (e.g., "message", "callback\\_query", "inline\\_query").
\*\*Example:\*\*
```python
if update\_type == "callback\_query":
Api.answerCallbackQuery("Button clicked!")
```
\*\*\*
## Security Concepts
### Sandboxed Environment
\*\*Definition:\*\* A secure, isolated execution environment where bot code runs. Prevents unauthorized access to system resources and ensures bot security.
\*\*Restrictions:\*\*
\* No system module access (os, sys, subprocess)
\* No file system access outside allowed APIs
\* No network access except through provided APIs
\* Restricted Python builtins
\*\*\*
### CAPTCHA
\*\*Definition:\*\* Challenge-response test to verify human users and prevent bot abuse.
\*\*Implementation:\*\*
```python
# Create CAPTCHA
captcha = Bot.createCaptcha()
captcha\_id = captcha['captcha\_id']
# Send to user
Bot.sendCaptcha(captcha\_id, caption="Verify you're human")
Bot.waitForInput("verify\_captcha")
# Verify response
is\_valid = Bot.verifyCaptcha(captcha\_id, user\_answer)
if is\_valid:
Api.sendMessage("✅ Verified!")
```
\*\*\*
### Membership Check
\*\*Definition:\*\* Verification that a user is a member of a specific channel or group.
\*\*Syntax:\*\*
```python
CheckMembership(user\_id, channel\_username)
```
\*\*Example:\*\*
```python
is\_member = CheckMembership(u, "@your\_channel")
if is\_member:
Api.sendMessage("Access granted!")
else:
Api.sendMessage("Join @your\_channel first")
```
\*\*\*
## Platform Limits
### Execution Limits
\* \*\*Maximum execution time:\*\* 160 seconds per command
\* \*\*Sleep function maximum:\*\* 10 seconds
\* \*\*Rate limit:\*\* 5 executions per 5 seconds for fast commands (<0.4s)
### Storage Limits
\* \*\*Data entry size:\*\* 10MB maximum per entry
\* \*\*Number of entries:\*\* Unlimited
### Broadcast Limits
\* \*\*Per bot:\*\* 2 simultaneous broadcasts
\* \*\*Global:\*\* 1000 simultaneous broadcasts
### Scheduling Limits
\* \*\*Delay range:\*\* 0.1 seconds to 31,536,000 seconds (1 year)
\* \*\*Per user:\*\* Maximum 100 scheduled commands
\*\*\*
## Best Practices
### Error Handling
Always use try-except blocks:
```python
try:
operation()
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"Error {error\_id}: {str(e)}")
```
### Input Validation
Validate all user input:
```python
if not email or "@" not in email:
Api.sendMessage("Invalid email")
Bot.waitForInput("get\_email")
```
### Data Security
Hash sensitive data:
```python
hashed = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password\_hash", hashed)
```
### Resource Management
Use resources for numeric tracking:
```python
points = User.res("points")
points.add(50)
```
### Code Organization
Break complex workflows into steps:
```python
Api.sendMessage("Step 1: Enter name")
Bot.waitForInput("step\_2")
```
\*\*\*
## Summary
This glossary covers the essential terms, concepts, and features of TeleBot Studio. Understanding these definitions will help you:
\* Build more effective bots
\* Use platform features correctly
\* Troubleshoot issues efficiently
\* Write better, more maintainable code
\* Leverage advanced capabilities
For more detailed information, refer to the complete documentation including Getting Started guides, Language Reference, Library Documentation, and Real-World Use Cases.
Happy building with TeleBot Studio! 🚀
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/glossary-and-key-concepts.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.