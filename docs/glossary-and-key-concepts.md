# Glossary and Key Concepts
This comprehensive glossary provides definitions and explanations of key terms and concepts in TeleBot Studio. Understanding these terms is essential for effectively building and managing bots on the platform.
***
## Introduction
TeleBot Studio uses specialized terminology to define its functionality and features. This glossary serves as a quick reference guide, ensuring you have a clear understanding of the platform's core elements, advanced features, and technical concepts.
***
## Core Concepts
### TeleBot Studio (TBS)
**Definition:** A comprehensive platform for building, hosting, and managing Telegram bots without server management. TeleBot Studio provides a complete development environment with built-in libraries, secure execution, and advanced features.
**Key Features:**
* Free hosting with no limits
* Python-like bot development language
* Built-in libraries for blockchain, AI, payments
* No server configuration required
***
### TeleBot Syntax (TBS)
**Definition:** The custom Python-like programming language designed specifically for TeleBot Studio. TBS simplifies bot development by offering built-in libraries, pre-defined variables, and a secure, sandboxed execution environment.
**Example:**
```python
Api.sendMessage("Welcome to my bot!")
User.storeData("name", "John")
points = User.res("points")
points.add(50)
```
**Key Characteristics:**
* Python-like syntax
* No import statements required
* Pre-loaded libraries and utilities
* Secure sandboxed execution
* Maximum execution time: 160 seconds
***
### Bot API Token
**Definition:** A unique authentication token provided by Telegram for managing and controlling a bot. This token is required to connect your bot to TeleBot Studio.
**How to Get:**
1. Message @BotFather on Telegram
2. Use `/newbot` command
3. Follow instructions to create bot
4. Copy the provided token
**Example Token Format:**
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
**Security Note:** Never share your bot token publicly as it grants full control over your bot.
***
## Commands
### Command
**Definition:** A trigger that executes specific logic when a user sends a corresponding message. Commands typically start with `/` (e.g., `/start`, `/help`) but can also be plain text.
**Types of Commands:**
* **Standard Commands:** `/start`, `/help`, `/settings`
* **Wildcard Command (`*`):** Catches unmatched messages
* **At Handler (`@`):** Executes before all other commands
* **Custom Commands:** Any user-defined command
**Example:**
```python
# /start command
Api.sendMessage("Welcome! Use /help for assistance.")
# /help command
Api.sendMessage("Available commands:\n/start - Start the bot\n/help - Show this help")
```
***
### Wildcard Command (`*`)
**Definition:** A special command that catches any message not matching other defined commands. Essential for handling unknown inputs or creating conversational fallbacks.
**Use Cases:**
* Default responses
* Error handling
* Logging unrecognized commands
* Natural language processing fallback
**Example:**
```python
Api.sendMessage("I didn't understand that. Type /help for available commands.")
```
***
### At Handler (`@`)
**Definition:** A special command that executes before any other command. Used for preprocessing, logging, authentication, or setting up global conditions.
**Use Cases:**
* Activity logging
* Authentication checks
* Rate limiting
* Message validation
**Example:**
```python
# Log all user activity
Bot.res("total_messages").add(1)
User.storeData("last_active", time.time())
# Execution continues to matched command
```
***
## Objects and Classes
### Api Object
**Definition:** The object used for all Telegram Bot API methods. Provides direct access to Telegram's messaging and bot management functionality.
**Common Methods:**
* `Api.sendMessage()` - Send text messages
* `Api.sendPhoto()` - Send images
* `Api.sendDocument()` - Send files
* `Api.sendPoll()` - Create polls
* `Api.editMessageText()` - Edit messages
**Example:**
```python
Api.sendMessage("Hello, world!")
Api.sendPhoto("https://example.com/image.jpg", caption="Check this out!")
```
***
### Bot Object
**Definition:** The object for TeleBot Studio platform-specific operations like data storage, scheduling, broadcasting, and bot management.
**Common Methods:**
* `Bot.storeData()` / `Bot.fetchData()` - Bot-level data storage
* `Bot.scheduleCommand()` - Schedule commands
* `Bot.sendBroadcast()` - Send broadcasts
* `Bot.getInfo()` - Get bot information
* `Bot.createCaptcha()` - Generate CAPTCHA
**Example:**
```python
Bot.storeData("total_users", 1000)
Bot.scheduleCommand(3600, "send_reminder")
Bot.sendBroadcast(function="sendMessage", text="Announcement!")
```
***
### User Object
**Definition:** Manages user-specific data and resources for individual users interacting with your bot.
**Common Methods:**
* `User.storeData()` / `User.fetchData()` - User data storage
* `User.res()` - User resource management
* `User.resOf()` - Access another user's resources
**Example:**
```python
User.storeData("language", "en")
points = User.res("points")
points.add(50)
```
***
### Account Object
**Definition:** Manages account-level data shared across all bots in your TeleBot Studio account.
**Common Methods:**
* `Account.storeData()` / `Account.fetchData()` - Account data
* `Account.res()` - Account resources
* Account management operations
**Example:**
```python
Account.storeData("api_key", "secret_key")
global_config = Account.fetchData("config")
```
***
## Data Management
### Data Storage
**Definition:** The system for persisting information across bot interactions at different scopes (user, bot, account).
**Storage Levels:**
**User-Level Storage:**
```python
User.storeData("name", "John")
User.storeData("email", "john@example.com")
name = User.fetchData("name")
User.removeData("temp_data")
```
**Bot-Level Storage:**
```python
Bot.storeData("total_users", 1000)
total = Bot.fetchData("total_users")
Bot.removeData("old_config")
```
**Account-Level Storage:**
```python
Account.storeData("api_key", "key_value")
key = Account.fetchData("api_key")
Account.removeData("temp")
```
**Storage Limits:**
* Maximum size per entry: 10MB
* No limit on number of entries
***
### Resources
**Definition:** Numeric values that can be tracked and modified per user or globally. Perfect for points, credits, currency, or any numeric tracking.
**Operations:**
* `add()` - Increment value
* `cut()` - Decrement value
* `set()` - Set specific value
* `reset()` - Reset to zero
* `value()` - Get current value
**User Resources:**
```python
points = User.res("points")
points.add(50) # Add 50 points
points.cut(10) # Subtract 10 points
points.set(100) # Set to 100
current = points.value() # Get current value
points.reset() # Reset to 0
```
**Bot Resources (Global):**
```python
total_sales = Bot.res("total_sales")
total_sales.add(1)
Api.sendMessage(f"Total sales: {total_sales.value()}")
```
**Another User's Resources:**
```python
target_points = User.resOf("points", target_user_id)
Api.sendMessage(f"User has {target_points.value()} points")
```
***
## Broadcasting
### Broadcast
**Definition:** A feature that sends messages or executes commands across multiple users simultaneously. Essential for announcements, notifications, and mass communications.
**Types:**
**Function-Based:**
```python
Bot.sendBroadcast(
function="sendMessage",
text="Important announcement!"
)
```
**Command-Based:**
```python
Bot.sendBroadcast(command="send_personalized_message")
```
**Code-Based:**
```python
Bot.sendBroadcast(code="Api.sendMessage('Hello everyone!')")
```
**Broadcast Limits:**
* Maximum 2 simultaneous broadcasts per bot
* Maximum 1000 simultaneous broadcasts globally
**Management:**
```python
# List broadcasts
broadcasts = Bot.listBroadcasts()
# Check status
status = Bot.broadcastStatus(broadcast_id="123")
# Pause broadcast
Bot.pauseBroadcast(broadcast_id="123")
# Cancel broadcast
Bot.cancelBroadcast(broadcast_id="123")
```
***
## Advanced Features
### Webhook
**Definition:** A URL endpoint that allows external systems to trigger bot commands in real-time. Webhooks enable integration with payment processors, notification services, and other bots.
**Generation:**
```python
# Basic webhook
webhook_url = Lib.Webhook.getUrlFor("process_data", user_id=u)
# Cross-bot webhook
webhook = Lib.Webhook.getUrlFor(
"notify_user",
bot_id="other_bot_id",
api_key="other_bot_api_key",
user_id=u
)
```
**Handling Webhook Data:**
```python
# In webhook command
webhook_data = options
event_type = webhook_data.get('type')
data = webhook_data.get('data')
Api.sendMessage(f"Received: {data}")
```
***
### Command Chaining
**Definition:** The process of linking multiple commands together to create multi-step workflows.
**Implementation:**
```python
# Step 1
Api.sendMessage("What's your name?")
Bot.waitForInput("get_name")
# Step 2 (get_name command)
name = msg
User.storeData("name", name)
Api.sendMessage("What's your email?")
Bot.waitForInput("get_email")
# Step 3 (get_email command)
email = msg
User.storeData("email", email)
Api.sendMessage("Registration complete!")
```
***
### Scheduled Commands
**Definition:** Commands that execute after a specified delay, enabling reminders, follow-ups, and timed operations.
**Syntax:**
```python
Bot.scheduleCommand(delay_seconds, command_name, **options)
```
**Constraints:**
* Minimum delay: 0.1 seconds
* Maximum delay: 31,536,000 seconds (1 year)
* Maximum 100 scheduled commands per user
* Rate limit: 5 executions per 5 seconds for ultra-fast commands (<0.4s)
**Examples:**
```python
# 1 hour reminder
Bot.scheduleCommand(3600, "send_reminder")
# Quick follow-up
Bot.scheduleCommand(0.5, "send_confirmation")
# Daily notification
Bot.scheduleCommand(86400, "daily_digest")
```
***
### Bot Transfer
**Definition:** The process of creating a copy of your bot and transferring it to another TeleBot Studio account. The original bot remains in your account.
**Syntax:**
```python
Bot.transfer(email, bot_id, bot_token=None, run_now=False)
```
**Example:**
```python
result = Bot.transfer(
email="recipient@example.com",
bot_id=bot_id,
bot_token="YOUR_BOT_TOKEN",
run_now=True
)
```
**Important:** This creates a copy of the bot, not transfers ownership. Your original bot remains functional.
***
## Libraries
### Lib.EVM
**Definition:** Library for Ethereum and EVM-compatible blockchain operations including transactions, token transfers, and wallet management.
**Supported Networks:** 31+ including Ethereum, BSC, Polygon, Avalanche, Arbitrum, Optimism, and more
**Example:**
```python
# Store private key
Lib.EVM.storeKey("private_key")
# Send native coin
tx = Lib.EVM.sendCoin(network="ethereum", to="0x...", value=0.1)
# Send ERC-20 token
tx = Lib.EVM.sendToken(
network="ethereum",
to="0x...",
value=100,
contract_address="0x..." # Token contract
)
```
***
### Lib.TON
**Definition:** Library for The Open Network (TON) blockchain integration including wallet creation, balance checking, transactions, and TON Connect.
**Example:**
```python
# Create wallet
wallet = Lib.TON.createWallet()
Api.sendMessage(f"Address: {wallet['address']}")
# Check balance
balance = Lib.TON.balance("EQD...")
# Send TON
Lib.TON.send(to_address="EQD...", amount=0.5, comment="Payment")
```
***
### Lib.AI
**Definition:** Unified AI library supporting OpenAI and Google Gemini for chat completions and AI assistants.
**Example:**
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
***
### Lib.DateTime
**Definition:** Library for date and time operations including current time, timezone conversions, and timestamps.
**Methods:**
```python
# Current UTC time
current = Lib.DateTime.utcnow()
# Timezone-specific time
tokyo_time = Lib.DateTime.now("Asia/Tokyo")
# UNIX timestamp
timestamp = Lib.DateTime.time()
```
***
### Lib.Random
**Definition:** Library for generating random numbers, strings, and values.
**Methods:**
```python
# Random integer
num = Lib.Random.integer(1, 100)
# Random string
text = Lib.Random.string(16)
# Random decimal
decimal = Lib.Random.decimal(0.0, 1.0)
# Random ASCII
ascii_str = Lib.Random.ascii(20)
```
***
### Lib.CSV
**Definition:** Library for creating, reading, and managing CSV files for structured data storage.
**Example:**
```python
csv = Lib.CSV.Table("data.csv")
csv.create(["name", "email", "points"])
csv.insert({"name": "John", "email": "john@example.com", "points": 100})
row = csv.row(0)
csv.update(0, {"points": 150})
csv.delete(1)
```
***
### Lib.Webhook
**Definition:** Library for generating webhook URLs for command invocation and external integrations.
**Syntax:**
```python
Lib.Webhook.getUrlFor(command, user_id=None, chat_id=None, bot_id=None, api_key=None, **options)
```
**Example:**
```python
webhook = Lib.Webhook.getUrlFor("process_payment", user_id=u)
```
***
### Lib.Oxapay
**Definition:** Payment processing library for cryptocurrency and fiat payments through Oxapay merchant services.
**Example:**
```python
client = Lib.Oxapay.post("MERCHANT_API_KEY")
invoice = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Premium subscription"
})
Api.sendMessage(f"Pay: {invoice['url']}")
```
***
### Lib.Crypto
**Definition:** Cryptocurrency utility library for price conversions and crypto operations.
**Example:**
```python
# Convert between cryptocurrencies
result = Lib.Crypto.convert(amount=1, from_currency="BTC", to_currency="USD")
# Get current price
price = Lib.Crypto.get_price("BTC", "USD")
```
***
### Request Module
**Definition:** HTTP client for making API requests to external services.
**Methods:**
* `Request.get()` - GET request
* `Request.post()` - POST request
* `Request.put()` - PUT request
* `Request.delete()` - DELETE request
* `Request.patch()` - PATCH request
**Example:**
```python
response = Request.get("https://api.example.com/data")
if response.ok:
data = response.json()
Api.sendMessage(f"Result: {data}")
```
***
## Global Variables
### msg
**Definition:** Contains the raw text content of the incoming message from the user.
**Example:**
```python
user_input = msg
Api.sendMessage(f"You said: {user_input}")
```
***
### message
**Definition:** Contains the complete message object with all metadata including sender info, chat details, and message content.
**Example:**
```python
first_name = message.from_user.first_name
chat_id = message.chat.id
Api.sendMessage(f"Hello {first_name}!")
```
***
### u
**Definition:** The user ID of the current user interacting with the bot.
**Example:**
```python
Api.sendMessage(f"Your user ID is: {u}")
User.storeData("user_id", u)
```
***
### params
**Definition:** Parameters passed to a command via deep links or command arguments.
**Example:**
```python
# User clicks: t.me/yourbot?start=referral_123
referrer_id = params # Contains: "referral_123"
Api.sendMessage(f"Referred by: {referrer_id}")
```
***
### options
**Definition:** Additional data passed to a command, typically from webhooks or scheduled commands.
**Example:**
```python
# In webhook command
webhook_data = options
amount = webhook_data.get('amount')
Api.sendMessage(f"Amount: {amount}")
```
***
### bot\_id
**Definition:** The unique identifier of the current bot.
**Example:**
```python
Api.sendMessage(f"Bot ID: {bot_id}")
```
***
### bot\_token
**Definition:** The Telegram Bot API token for the current bot.
**Note:** Handle with care - never expose publicly.
***
### update\_type
**Definition:** Indicates the type of the current Telegram update (e.g., "message", "callback\_query", "inline\_query").
**Example:**
```python
if update_type == "callback_query":
Api.answerCallbackQuery("Button clicked!")
```
***
## Security Concepts
### Sandboxed Environment
**Definition:** A secure, isolated execution environment where bot code runs. Prevents unauthorized access to system resources and ensures bot security.
**Restrictions:**
* No system module access (os, sys, subprocess)
* No file system access outside allowed APIs
* No network access except through provided APIs
* Restricted Python builtins
***
### CAPTCHA
**Definition:** Challenge-response test to verify human users and prevent bot abuse.
**Implementation:**
```python
# Create CAPTCHA
captcha = Bot.createCaptcha()
captcha_id = captcha['captcha_id']
# Send to user
Bot.sendCaptcha(captcha_id, caption="Verify you're human")
Bot.waitForInput("verify_captcha")
# Verify response
is_valid = Bot.verifyCaptcha(captcha_id, user_answer)
if is_valid:
Api.sendMessage("✅ Verified!")
```
***
### Membership Check
**Definition:** Verification that a user is a member of a specific channel or group.
**Syntax:**
```python
CheckMembership(user_id, channel_username)
```
**Example:**
```python
is_member = CheckMembership(u, "@your_channel")
if is_member:
Api.sendMessage("Access granted!")
else:
Api.sendMessage("Join @your_channel first")
```
***
## Platform Limits
### Execution Limits
* **Maximum execution time:** 160 seconds per command
* **Sleep function maximum:** 10 seconds
* **Rate limit:** 5 executions per 5 seconds for fast commands (<0.4s)
### Storage Limits
* **Data entry size:** 10MB maximum per entry
* **Number of entries:** Unlimited
### Broadcast Limits
* **Per bot:** 2 simultaneous broadcasts
* **Global:** 1000 simultaneous broadcasts
### Scheduling Limits
* **Delay range:** 0.1 seconds to 31,536,000 seconds (1 year)
* **Per user:** Maximum 100 scheduled commands
***
## Best Practices
### Error Handling
Always use try-except blocks:
```python
try:
operation()
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"Error {error_id}: {str(e)}")
```
### Input Validation
Validate all user input:
```python
if not email or "@" not in email:
Api.sendMessage("Invalid email")
Bot.waitForInput("get_email")
```
### Data Security
Hash sensitive data:
```python
hashed = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password_hash", hashed)
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
Bot.waitForInput("step_2")
```
***
## Summary
This glossary covers the essential terms, concepts, and features of TeleBot Studio. Understanding these definitions will help you:
* Build more effective bots
* Use platform features correctly
* Troubleshoot issues efficiently
* Write better, more maintainable code
* Leverage advanced capabilities
For more detailed information, refer to the complete documentation including Getting Started guides, Language Reference, Library Documentation, and Real-World Use Cases.
Happy building with TeleBot Studio! 🚀
