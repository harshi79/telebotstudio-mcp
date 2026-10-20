# Advanced Features
This section explores advanced capabilities and techniques in TeleBot Studio that enable you to build sophisticated, enterprise-grade Telegram bots. From complex workflow automation to external API integrations and multi-bot orchestration, these features unlock the full potential of the platform.
***
## Environment Variables
### Overview
**Environment Variables** provide a secure, centralized way to manage configuration settings, API keys, credentials, and other sensitive data for your bot. Variables set through the dashboard are **automatically available in your bot commands** as Python variables.
### Benefits
✅ **Security** - Keep sensitive data (API keys, tokens) out of your code
✅ **Easy Management** - Update values through dashboard without code changes
✅ **Automatic Access** - Variables are instantly available in your commands
✅ **Best Practice** - Industry-standard approach for credentials management
✅ **No Redeployment** - Change values without restarting your bot
### Managing Environment Variables
Navigate to **Bot Management → Env** tab to manage your environment variables:
**Add New Variable:**
1. Click "Add Variable"
2. Enter variable name (use UPPERCASE with underscores: `OPENAI_API_KEY`, `MERCHANT_ID`)
3. Enter value
4. Save
**Edit Variable:**
* Both variable name and value can be edited
* Click edit icon next to variable
* Update name or value
* Save changes
**Delete Variable:**
* Click delete icon next to variable
* Confirm deletion
**Naming Convention:**
* Use UPPERCASE letters
* Separate words with underscores
* Examples: `API_KEY`, `DATABASE_URL`, `MAIL_USERNAME`, `WEBHOOK_SECRET`
### Using Environment Variables in Code
Environment variables are **automatically available** in your bot commands - just use them like any Python variable:
```python
# Environment variable OPENAI_API_KEY is automatically available
ai_client = Lib.AI.client(provider="openai", apiKey=OPENAI_API_KEY)
Api.sendMessage("AI initialized successfully!")
# Use PORT variable with fallback
port = PORT if 'PORT' in dir() else "5000"
# Example with payment gateway
client = Lib.Oxapay.post(OXAPAY_MERCHANT_KEY)
# Use in API requests
response = Request.get(
f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=London"
)
```
### Scope and Behavior
**Variable Overriding:** If you define a variable with the same name in your command code, your local definition overrides the environment variable for that specific command:
```python
# Environment variable: API_KEY = "env_value_123"
# In command code:
API_KEY = "local_value_456" # This overrides the env variable
# Local definition takes precedence
Api.sendMessage(f"Using: {API_KEY}") # Outputs: "Using: local_value_456"
```
**On Bot Cloning:**
* ✅ **Both variable names AND values** are copied to the cloned bot
* ⚠️ **Review after cloning** - Update sensitive values like API keys, merchant IDs, or bot tokens if the cloned bot needs separate credentials
**On Bot Transfer:**
* ✅ **Variable names** are transferred
* ❌ **Variable values** are NOT transferred (for security)
* 📝 Recipient must configure their own values after transfer
* 🔒 Protects sensitive credentials during ownership transfers
### Common Use Cases
**API Keys:**
```python
# Set in Env tab:
# OPENAI_API_KEY = sk-abc123...
# GEMINI_API_KEY = AIza...
# SENDGRID_API_KEY = SG.xyz...
# Use directly in code:
ai_client = Lib.AI.client(provider="openai", apiKey=OPENAI_API_KEY)
```
**Payment Gateways:**
```python
# Set in Env tab:
# OXAPAY_MERCHANT_KEY = merchant_12345
# STRIPE_SECRET_KEY = sk_live_...
# Use directly in code:
oxapay = Lib.Oxapay.post(OXAPAY_MERCHANT_KEY)
```
**Configuration:**
```python
# Set in Env tab:
# BASE_URL = https://mybot.com
# DEBUG_MODE = false
# MAX_RETRIES = 3
# Use directly in code:
if DEBUG_MODE == "true":
Api.sendMessage("Debug mode enabled")
```
### Best Practices
1. **Never hardcode secrets in your code**
```python
# ❌ Bad
api_key = "sk-abc123xyz..."
# ✅ Good - Set in Env tab, use directly
ai_client = Lib.AI.client(provider="openai", apiKey=OPENAI_API_KEY)
```
2. **Use descriptive variable names**
```
# ✅ Good
OPENAI_API_KEY
PAYMENT_WEBHOOK_URL
DATABASE_CONNECTION_STRING
# ❌ Bad
KEY1, URL, DB
```
3. **Check if variable exists before using**
```python
# Check if environment variable is set
if 'OPENAI_API_KEY' not in dir():
Api.sendMessage("⚠️ Please configure OPENAI_API_KEY in Env settings")
return
# Now safe to use
ai_client = Lib.AI.client(provider="openai", apiKey=OPENAI_API_KEY)
```
4. **Use separate values for development and production**
```
# Development bot Env settings:
STRIPE_KEY = sk_test_...
DEBUG_MODE = true
# Production bot Env settings:
STRIPE_KEY = sk_live_...
DEBUG_MODE = false
```
***
## Advanced Scheduling Techniques
TeleBot Studio's scheduling system offers precise control over command execution timing with support for delays from 0.1 seconds to 1 year.
### Bot.scheduleCommand()
Schedule a command to execute after a specified delay.
**Syntax:**
```python
Bot.scheduleCommand(delay_seconds, command, user_id=None, chat_id=None, params=None, **options)
```
**Parameters:**
* `delay_seconds` (Required): Delay in seconds (0.1 to 31536000 - one year)
* `command` (Required): Name of the command to execute
* `user_id` (Optional): Target user ID
* `chat_id` (Optional): Target chat ID
* `params` (Optional): Parameters to pass to the command
* `**options` (Optional): Additional options passed to the command
**Returns:** None
**Rate Limiting:**
* For commands scheduled under 0.4 seconds: Maximum 5 executions within 5 seconds
* Maximum 100 scheduled commands per user
### Micro-Scheduling for Performance
Execute commands with minimal delay for time-sensitive operations:
```python
# Quick follow-up message (0.2 seconds)
Api.sendMessage("Processing your request...")
Bot.scheduleCommand(0.2, "send_result")
```
### Cascading Scheduled Tasks
Chain multiple scheduled commands for complex workflows:
```python
# Multi-stage notification system
Api.sendMessage("Order confirmed! We'll keep you updated.")
Bot.scheduleCommand(60, "order_preparing") # 1 minute
Bot.scheduleCommand(300, "order_shipping") # 5 minutes
Bot.scheduleCommand(1800, "order_delivered") # 30 minutes
```
**Order Preparing Command:**
```python
Api.sendMessage("👨‍🍳 Your order is being prepared!")
```
**Order Shipping Command:**
```python
Api.sendMessage("📦 Your order has been shipped!")
tracking_number = Bot.uniqueID()
User.storeData("tracking", tracking_number)
Api.sendMessage(f"Tracking: {tracking_number}")
```
**Order Delivered Command:**
```python
Api.sendMessage("✅ Your order has been delivered!")
Api.sendMessage("Please rate your experience: /rate")
```
### Conditional Scheduling
Schedule tasks based on user actions or conditions:
```python
reminder_enabled = User.fetchData("reminders_enabled")
if reminder_enabled:
Bot.scheduleCommand(86400, "daily_reminder") # 24 hours
Api.sendMessage("Daily reminder scheduled!")
```
***
## Complex Command Chaining Workflows
Build sophisticated multi-step processes that guide users through intricate operations.
### Bot.waitForInput()
Waits for the next user message and routes it to a specific command.
**Syntax:**
```python
Bot.waitForInput(command, **options)
```
**Parameters:**
* `command` (Required): Name of the command to execute when user sends next message
* `**options` (Optional): Dictionary of options passed to the command via `options` global variable
**Returns:** None
**Example:**
```python
Api.sendMessage("What's your name?")
Bot.waitForInput("process_name", greeting="Hello")
```
In the `process_name` command:
```python
name = msg
greeting = options.get('greeting', 'Hi')
Api.sendMessage(f"{greeting}, {name}!")
```
### Multi-Step Form with Validation
**Step 1 - Initiate Process:**
```python
# /register_business command
Api.sendMessage("🏢 Business Registration")
Api.sendMessage("Let's start with your business name:")
Bot.waitForInput("get_business_name")
```
**Step 2 - Validate Business Name:**
```python
# get_business_name command
business_name = msg
if len(business_name) < 3:
Api.sendMessage("Business name too short. Please enter at least 3 characters:")
Bot.waitForInput("get_business_name")
elif len(business_name) > 50:
Api.sendMessage("Business name too long. Maximum 50 characters:")
Bot.waitForInput("get_business_name")
else:
User.storeData("business_name", business_name)
Api.sendMessage(f"✅ Business name: {business_name}")
Api.sendMessage("What's your business type? (Retail/Service/Manufacturing/Other)")
Bot.waitForInput("get_business_type")
```
**Step 3 - Process Business Type:**
```python
# get_business_type command
business_type = msg.lower()
valid_types = ["retail", "service", "manufacturing", "other"]
if business_type not in valid_types:
Api.sendMessage("Invalid type. Choose: Retail, Service, Manufacturing, or Other")
Bot.waitForInput("get_business_type")
else:
User.storeData("business_type", business_type)
Api.sendMessage("How many employees? (Enter a number)")
Bot.waitForInput("get_employee_count")
```
**Step 4 - Validate Numeric Input:**
```python
# get_employee_count command
employee_input = msg
if not employee_input.isdigit():
Api.sendMessage("Please enter a valid number:")
Bot.waitForInput("get_employee_count")
else:
employee_count = int(employee_input)
User.storeData("employee_count", employee_count)
# Generate business profile
Api.sendMessage("📋 Business Profile Created:")
Api.sendMessage(f"Name: {User.fetchData('business_name')}")
Api.sendMessage(f"Type: {User.fetchData('business_type')}")
Api.sendMessage(f"Employees: {employee_count}")
# Assign business tier
tier = "Enterprise" if employee_count > 100 else "Business" if employee_count > 10 else "Startup"
User.storeData("business_tier", tier)
Api.sendMessage(f"Tier: {tier}")
# Award points based on tier
points = User.res("points")
bonus = 500 if tier == "Enterprise" else 200 if tier == "Business" else 100
points.add(bonus)
Api.sendMessage(f"Welcome bonus: {bonus} points!")
```
### Branching Workflows
Create dynamic paths based on user choices:
```python
# /support command
Api.sendMessage("What do you need help with?")
Api.sendMessage("1. Technical Issue")
Api.sendMessage("2. Billing Question")
Api.sendMessage("3. Feature Request")
Api.sendMessage("Reply with 1, 2, or 3")
Bot.waitForInput("support_router")
```
**Support Router:**
```python
# support_router command
choice = msg
if choice == "1":
Api.sendMessage("Describe your technical issue:")
Bot.waitForInput("handle_technical")
elif choice == "2":
Api.sendMessage("What's your billing question?")
Bot.waitForInput("handle_billing")
elif choice == "3":
Api.sendMessage("Tell us about your feature idea:")
Bot.waitForInput("handle_feature_request")
else:
Api.sendMessage("Invalid choice. Reply with 1, 2, or 3:")
Bot.waitForInput("support_router")
```
***
## Advanced API Integrations
Leverage external services to extend your bot's capabilities with real-time data and third-party functionality.
### HTTP Request Methods
TeleBot Studio provides comprehensive HTTP support through the `Request` module.
#### Request.get()
Performs an HTTP GET request.
**Syntax:**
```python
Request.get(url, **kwargs)
```
**Parameters:**
* `url` (Required): The URL to request
* `headers` (Optional): Dictionary of HTTP headers
* `params` (Optional): Dictionary of URL parameters
* `timeout` (Optional): Request timeout in seconds (default: 30)
* `**kwargs` (Optional): Additional requests library parameters
**Returns:** `TBS_HTTP_Response` object with attributes:
* `status_code` (int): HTTP status code
* `text` (str): Response body as text
* `content` (bytes): Response body as bytes
* `headers` (dict): Response headers
* `ok` (bool): True if status code is 200-299
* `url` (str): Final URL after redirects
* `json()` (method): Parse response as JSON
**Example:**
```python
response = Request.get("https://api.example.com/data")
if response.status_code == 200:
data = response.json()
Api.sendMessage(f"Result: {data['value']}")
else:
Api.sendMessage(f"Error: {response.status_code}")
```
#### Request.post()
Performs an HTTP POST request.
**Syntax:**
```python
Request.post(url, **kwargs)
```
**Parameters:**
* `url` (Required): The URL to request
* `json` (Optional): Dictionary to send as JSON body
* `data` (Optional): Dictionary or string to send as form data
* `headers` (Optional): Dictionary of HTTP headers
* `timeout` (Optional): Request timeout in seconds (default: 30)
* `**kwargs` (Optional): Additional requests library parameters
**Returns:** `TBS_HTTP_Response` object (same attributes as GET)
**Example:**
```python
payload = {
"username": User.fetchData("name"),
"email": User.fetchData("email"),
"action": "register"
}
response = Request.post(
"https://api.example.com/users",
json=payload,
headers={"Authorization": "Bearer YOUR_API_KEY"}
)
if response.ok:
Api.sendMessage("✅ Registration successful!")
result = response.json()
User.storeData("external_id", result['user_id'])
else:
Api.sendMessage(f"❌ Registration failed: {response.status_code}")
```
#### Request.put()
Performs an HTTP PUT request.
**Syntax:**
```python
Request.put(url, **kwargs)
```
**Parameters:** Same as `Request.post()`
**Returns:** `TBS_HTTP_Response` object
**Example:**
```python
update_data = {"status": "active", "last_seen": time.time()}
response = Request.put(
f"https://api.example.com/users/{u}",
json=update_data
)
```
#### Request.delete()
Performs an HTTP DELETE request.
**Syntax:**
```python
Request.delete(url, **kwargs)
```
**Parameters:** Same as `Request.get()`
**Returns:** `TBS_HTTP_Response` object
**Example:**
```python
response = Request.delete(f"https://api.example.com/users/{u}")
if response.status_code == 204:
Api.sendMessage("Account deleted successfully")
```
#### Request.patch()
Performs an HTTP PATCH request.
**Syntax:**
```python
Request.patch(url, **kwargs)
```
**Parameters:** Same as `Request.post()`
**Returns:** `TBS_HTTP_Response` object
### Weather API Integration
```python
# Get weather data
api_key = "YOUR_WEATHER_API_KEY"
city = User.fetchData("city") or "London"
response = Request.get(
f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
)
if response.ok:
weather = response.json()
Api.sendMessage(f"🌤 Weather in {city}:")
Api.sendMessage(f"Temperature: {weather['current']['temp_c']}°C")
Api.sendMessage(f"Condition: {weather['current']['condition']['text']}")
Api.sendMessage(f"Humidity: {weather['current']['humidity']}%")
else:
Api.sendMessage("Could not fetch weather data.")
```
### Cryptocurrency Price Tracking
```python
# Track crypto prices
response = Request.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
if response.ok:
prices = response.json()
Api.sendMessage("💰 Crypto Prices:")
Api.sendMessage(f"Bitcoin: ${prices['bitcoin']['usd']:,.2f}")
Api.sendMessage(f"Ethereum: ${prices['ethereum']['usd']:,.2f}")
```
### News API Integration
```python
# Fetch latest news
response = Request.get(
"https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
)
if response.ok:
news_data = response.json()
articles = news_data['articles'][:5] # Top 5 articles
Api.sendMessage("📰 Latest News:")
for idx, article in enumerate(articles, 1):
Api.sendMessage(f"{idx}. {article['title']}")
Api.sendMessage(f" {article['url']}")
```
***
## Advanced Webhook Integration
Create sophisticated webhook-based integrations for real-time event handling.
### Lib.Webhook.getUrlFor()
Generates a webhook URL for invoking a specific command.
**Syntax:**
```python
Lib.Webhook.getUrlFor(command, user_id=None, chat_id=None, bot_id=None, api_key=None, **options)
```
**Parameters:**
* `command` (Required): Name of the command to invoke
* `user_id` (Optional): Specific user ID for user-specific webhook
* `chat_id` (Optional): Specific chat ID for chat-specific webhook
* `bot_id` (Optional): Target another bot by ID
* `api_key` (Optional): API key for the target bot (required with bot\_id)
* `**options` (Optional): Additional data passed to the command via `options` variable
**Returns:** String containing the webhook URL
**Example:**
```python
# Generate personalized webhook
webhook_url = Lib.Webhook.getUrlFor("payment_received", user_id=u)
User.storeData("payment_webhook", webhook_url)
Api.sendMessage(f"Your payment webhook:\n{webhook_url}")
```
### Cross-Bot Communication
Enable multiple bots to work together:
```python
# Bot A triggers Bot B
bot_b_webhook = Lib.Webhook.getUrlFor(
"process_notification",
bot_id="bot_b_id",
api_key="bot_b_api_key",
user_id=u
)
# Trigger Bot B
response = Request.post(bot_b_webhook, json={"message": "Hello from Bot A"})
```
### Webhook Command Handler
```python
# process_notification command (in Bot B)
webhook_data = options
sender_bot = webhook_data.get('bot_id', 'Unknown')
message_content = webhook_data.get('message', '')
Api.sendMessage(f"Received from {sender_bot}: {message_content}")
# Process and respond
User.storeData("last_notification", message_content)
Api.sendMessage("Notification processed!")
```
### Payment Gateway Integration
```python
# Create payment webhook
payment_webhook = Lib.Webhook.getUrlFor("handle_payment", user_id=u)
# Send to payment provider
Api.sendMessage("Complete your payment:")
Api.sendMessage(payment_webhook)
```
**Handle Payment Command:**
```python
# handle_payment command
payment_data = options
amount = payment_data.get('amount', 0)
currency = payment_data.get('currency', 'USD')
status = payment_data.get('status', 'pending')
if status == 'completed':
# Award credits
credits = User.res("credits")
credits.add(int(amount))
Api.sendMessage(f"✅ Payment successful!")
Api.sendMessage(f"Added {amount} {currency} to your account")
Api.sendMessage(f"Current balance: {credits.value()} credits")
# Send receipt
receipt_data = f"Amount: {amount} {currency}\nStatus: {status}\nDate: {Lib.DateTime.utcnow()}"
User.storeData("last_receipt", receipt_data)
else:
Api.sendMessage(f"Payment status: {status}")
```
***
## Bot Transfer Functionality
### Bot.transfer()
Creates a copy of your bot and transfers it to another TeleBot Studio account. The original bot remains in your account.
**Syntax:**
```python
Bot.transfer(email, bot_id, bot_token=None, run_now=False)
```
**Parameters:**
* `email` (Required): Email address of the recipient's TeleBot Studio account
* `bot_id` (Required): The bot ID to transfer
* `bot_token` (Optional): Telegram bot token (required if run\_now is True)
* `run_now` (Optional): If True, starts the bot immediately in the new account
**Returns:** Dictionary with attributes:
* `ok` (bool): True if transfer successful
* `bot_id` (str): The bot ID that was transferred
* `new_owner` (str): Email of the new owner
* `error` (str): Error message if ok is False
**Example:**
```python
# Transfer bot copy to another account
try:
result = Bot.transfer(
email="recipient@example.com",
bot_id=bot_id,
bot_token="YOUR_BOT_TOKEN",
run_now=True
)
if result['ok']:
Api.sendMessage("✅ Bot copy transferred successfully!")
Api.sendMessage(f"Recipient: {result['new_owner']}")
Api.sendMessage(f"Bot ID: {result['bot_id']}")
Api.sendMessage("Note: Your original bot remains in your account.")
else:
Api.sendMessage(f"❌ Transfer failed: {result['error']}")
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"Transfer error {error_id}: {str(e)}")
```
### Batch Bot Transfer
Transfer copies of multiple bots:
```python
# Transfer multiple bot copies
bots_to_transfer = [
{"bot_id": "123456", "token": "TOKEN1"},
{"bot_id": "789012", "token": "TOKEN2"},
{"bot_id": "345678", "token": "TOKEN3"}
]
target_email = "recipient@example.com"
success_count = 0
failed_bots = []
for bot_data in bots_to_transfer:
try:
result = Bot.transfer(
email=target_email,
bot_id=bot_data['bot_id'],
bot_token=bot_data['token'],
run_now=False
)
if result['ok']:
success_count += 1
Api.sendMessage(f"✅ Bot {bot_data['bot_id']} copy transferred")
else:
failed_bots.append(bot_data['bot_id'])
except Exception as e:
failed_bots.append(bot_data['bot_id'])
Api.sendMessage(f"❌ {bot_data['bot_id']}: {str(e)}")
# Summary
Api.sendMessage(f"\n📊 Transfer Summary:")
Api.sendMessage(f"Successful: {success_count}")
Api.sendMessage(f"Failed: {len(failed_bots)}")
if failed_bots:
Api.sendMessage(f"Failed IDs: {', '.join(failed_bots)}")
```
### Bot Information Retrieval
#### Bot.getInfo()
Retrieves comprehensive information about a bot.
**Syntax:**
```python
Bot.getInfo(bot_id=None, api_key=None)
```
**Parameters:**
* `bot_id` (Optional): Bot ID to query (defaults to current bot)
* `api_key` (Optional): API key for accessing another bot
**Returns:** Dictionary with attributes:
* `token` (str): Bot token
* `bot_id` (str): Platform bot ID
* `owner_email` (str): Owner's email address
* `status` (str): "Working" or "Stopped"
* `username` (str): Bot's Telegram username
* `first_name` (str): Bot's display name
* `account_points` (int): Owner's remaining points
* `userstat` (int): Total number of bot users
**Example:**
```python
# Get comprehensive bot details
bot_details = Bot.getInfo()
Api.sendMessage("🤖 Bot Information:")
Api.sendMessage(f"Name: {bot_details['first_name']}")
Api.sendMessage(f"Username: @{bot_details['username']}")
Api.sendMessage(f"ID: {bot_details['bot_id']}")
Api.sendMessage(f"Status: {bot_details['status']}")
# Additional stats if available
if 'userstat' in bot_details:
Api.sendMessage(f"Total Users: {bot_details['userstat']}")
```
***
## Advanced Error Handling Strategies
### Comprehensive Error Management
```python
try:
# Critical operation
response = Request.post("https://api.example.com/critical", json=data)
response.raise_for_status()
result = response.json()
Api.sendMessage("✅ Operation successful!")
except ConnectionError as ce:
# Network issues
Api.sendMessage("🌐 Connection error. Retrying in 5 seconds...")
Bot.scheduleCommand(5, "retry_operation")
retry_count = User.fetchData("retry_count") or 0
User.storeData("retry_count", retry_count + 1)
except ValueError as ve:
# Data validation errors
Api.sendMessage(f"❌ Invalid data: {str(ve)}")
Api.sendMessage("Please check your input and try again.")
except Exception as e:
# Catch-all for unexpected errors
error_id = Bot.errorID()
error_details = {
"error_id": error_id,
"user_id": u,
"timestamp": time.time(),
"error_type": type(e).__name__,
"error_message": str(e),
"command": "current_command_name"
}
# Log error
Bot.storeData(f"error_{error_id}", error_details)
# Notify user
Api.sendMessage(f"❌ An error occurred.")
Api.sendMessage(f"Error ID: {error_id}")
Api.sendMessage("Our team has been notified.")
# Notify admin
Api.sendMessage(
f"🚨 Error {error_id}\nUser: {u}\nType: {type(e).__name__}\nMessage: {str(e)}",
chat_id="ADMIN_CHAT_ID"
)
```
### Retry Logic with Exponential Backoff
```python
# Initial attempt
retry_count = User.fetchData("operation_retry_count") or 0
max_retries = 3
if retry_count < max_retries:
try:
# Attempt operation
response = Request.get("https://api.example.com/data")
if response.ok:
# Success - reset retry counter
User.removeData("operation_retry_count")
Api.sendMessage("✅ Operation successful!")
else:
raise Exception(f"HTTP {response.status_code}")
except Exception as e:
retry_count += 1
User.storeData("operation_retry_count", retry_count)
# Exponential backoff: 2, 4, 8 seconds
delay = 2 ** retry_count
Api.sendMessage(f"Attempt {retry_count} failed. Retrying in {delay}s...")
Bot.scheduleCommand(delay, "retry_operation")
else:
# Max retries exceeded
User.removeData("operation_retry_count")
Api.sendMessage("❌ Operation failed after multiple attempts.")
Api.sendMessage("Please try again later or contact support.")
```
***
## Multi-Bot Orchestration
### Master-Slave Bot Architecture
**Master Bot - Distributes Tasks:**
```python
# Master bot receives task
task_type = msg
task_id = Bot.uniqueID()
# Determine which slave bot handles this task type
bot_mapping = {
"payment": {"bot_id": "payment_bot_id", "api_key": "payment_api_key"},
"notification": {"bot_id": "notif_bot_id", "api_key": "notif_api_key"},
"analytics": {"bot_id": "analytics_bot_id", "api_key": "analytics_api_key"}
}
if task_type in bot_mapping:
bot_config = bot_mapping[task_type]
webhook = Lib.Webhook.getUrlFor(
f"handle_{task_type}",
bot_id=bot_config['bot_id'],
api_key=bot_config['api_key'],
user_id=u
)
# Send task to slave bot
response = Request.post(webhook, json={"task_id": task_id, "user_id": u})
Api.sendMessage(f"Task {task_id} assigned to {task_type} bot")
else:
Api.sendMessage("Unknown task type")
```
**Slave Bot - Executes Task:**
```python
# handle_payment command (in payment bot)
task_data = options
task_id = task_data.get('task_id')
user_id = task_data.get('user_id')
Api.sendMessage(f"Processing payment task {task_id}", chat_id=user_id)
# Execute payment logic
Api.sendMessage("Payment processed successfully!", chat_id=user_id)
```
***
## CSV Data Management
### Lib.CSV.Table
Manages structured data efficiently with CSV operations.
**Syntax:**
```python
csv_handler = Lib.CSV.Table(filename)
```
#### Methods:
**create()** - Create CSV with headers
```python
csv_handler.create(["column1", "column2", "column3"])
```
**insert()** - Add row
```python
csv_handler.insert({"column1": "value1", "column2": "value2"})
```
**row()** - Get specific row by index
```python
row_data = csv_handler.row(0) # Returns dictionary
```
**update()** - Update row by index
```python
csv_handler.update(0, {"column1": "new_value"})
```
**delete()** - Delete row by index
```python
csv_handler.delete(1)
```
**toString()** - Export as string
```python
csv_string = csv_handler.toString()
```
**Example:**
```python
# Initialize CSV handler
csv_handler = Lib.CSV.Table("users_data.csv")
# Create CSV with headers
csv_handler.create(["user_id", "name", "email", "points"])
# Add rows
csv_handler.insert({"user_id": u, "name": "John", "email": "john@example.com", "points": 100})
csv_handler.insert({"user_id": u+1, "name": "Jane", "email": "jane@example.com", "points": 150})
Api.sendMessage("User data saved to CSV!")
# Query data
user_row = csv_handler.row(0)
Api.sendMessage(f"User: {user_row['name']}, Points: {user_row['points']}")
# Update row
csv_handler.update(0, {"points": 200})
# Export CSV
csv_string = csv_handler.toString()
Api.sendMessage(f"CSV Data:\n{csv_string}")
```
***
## Cryptocurrency and Blockchain Integration
### TON Blockchain Operations
#### Lib.TON.createWallet()
Generates a new TON wallet.
**Returns:** Dictionary with attributes:
* `address` (str): Wallet address
* `mnemonics` (str): 24-word recovery phrase
**Example:**
```python
wallet = Lib.TON.createWallet()
address = wallet['address']
mnemonics = wallet['mnemonics']
Api.sendMessage(f"New TON Wallet Created:")
Api.sendMessage(f"Address: {address}")
Api.sendMessage(f"Mnemonics: {mnemonics}")
# Store mnemonics securely
Lib.TON.storeKey(mnemonics)
```
#### Lib.TON.balance()
Checks wallet balance.
**Syntax:**
```python
Lib.TON.balance(address, api_key=None, endpoint=None)
```
**Parameters:**
* `address` (Required): TON wallet address
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
**Returns:** Float representing balance in TON
**Example:**
```python
address = "EQD..."
balance = Lib.TON.balance(address)
Api.sendMessage(f"Balance: {balance} TON")
```
#### Lib.TON.send()
Transfers TON to another address.
**Syntax:**
```python
Lib.TON.send(to_address, amount, comment=None, mnemonics=None, api_key=None, endpoint=None, is_testnet=False)
```
**Parameters:**
* `to_address` (Required): Recipient wallet address
* `amount` (Required): Amount to send in TON
* `comment` (Optional): Transaction comment
* `mnemonics` (Optional): Wallet mnemonics (uses stored if not provided)
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
* `is_testnet` (Optional): Use testnet if True
**Returns:** Dictionary with transaction details
**Example:**
```python
result = Lib.TON.send(
to_address="EQD...",
amount=0.5,
comment="Payment for service"
)
Api.sendMessage("TON sent successfully!")
```
### EVM Blockchain Operations
#### Lib.EVM.sendCoin()
Sends native cryptocurrency (ETH, BNB, MATIC, etc.).
**Syntax:**
```python
Lib.EVM.sendCoin(network, to, value, private_key=None, gas_limit=None, gas_price=None, proxy=None, estimate_gas=True, retry=False)
```
**Parameters:**
* `network` (Required): Network name (ethereum, bsc, polygon, etc.)
* `to` (Required): Recipient address
* `value` (Required): Amount to send
* `private_key` (Optional): Sender's private key (uses stored if not provided)
* `gas_limit` (Optional): Gas limit for transaction
* `gas_price` (Optional): Gas price in Gwei
* `proxy` (Optional): Proxy configuration
* `estimate_gas` (Optional): Auto-estimate gas (default True)
* `retry` (Optional): Retry once on failure (default False)
**Returns:** Transaction hash string
**Example:**
```python
# Store private key
Lib.EVM.storeKey("your_private_key")
# Send Ethereum
tx_hash = Lib.EVM.sendCoin(
network="ethereum",
to="0x...",
value=0.1
)
Api.sendMessage(f"Transaction: {tx_hash}")
```
#### Lib.EVM.sendToken()
Sends ERC-20 tokens.
**Syntax:**
```python
Lib.EVM.sendToken(network, to, value, contract_address, private_key=None, gas_limit=None, gas_price=None, proxy=None, estimate_gas=True, retry=False)
```
**Parameters:** Same as sendCoin() plus:
* `contract_address` (Required): Token contract address
**Returns:** Transaction hash string
**Example:**
```python
# Send USDT on Ethereum
tx_hash = Lib.EVM.sendToken(
network="ethereum",
to="0x...",
value=100,
contract_address="0xdac17f958d2ee523a2206206994597c13d831ec7" # USDT
)
Api.sendMessage(f"USDT sent: {tx_hash}")
```
#### Lib.EVM.networks()
Gets supported blockchain networks.
**Returns:** Dictionary of supported networks with their details
**Example:**
```python
networks = Lib.EVM.networks()
Api.sendMessage(f"Supported networks: {list(networks.keys())}")
```
***
## AI Integration
### Lib.AI.client()
Creates an AI client for OpenAI or Google Gemini.
**Syntax:**
```python
Lib.AI.client(provider='openai', apiKey=None, baseUrl=None, **kwargs)
```
**Parameters:**
* `provider` (Optional): 'openai' or 'gemini' (default: 'openai')
* `apiKey` (Required): API key for the provider
* `baseUrl` (Optional): Custom API base URL (OpenAI only)
* `**kwargs` (Optional): Additional provider-specific parameters
**Returns:** AI client object
### OpenAI Integration
**Simple Chat Completion:**
```python
# Create AI client
ai_client = Lib.AI.client(
provider="openai",
apiKey="YOUR_OPENAI_API_KEY"
)
# Generate response
response = ai_client.chat(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": msg}
]
)
Api.sendMessage(response['choices'][0]['message']['content'])
```
**Assistant with Memory:**
```python
# Create persistent assistant
assistant = Lib.AI.Assistant(
provider="openai",
apiKey="YOUR_API_KEY",
create_new=True,
name="Support Bot",
instructions="You are a technical support assistant.",
model="gpt-4"
)
# Start conversation
thread_id = assistant.start()
User.storeData("ai_thread", thread_id)
# Send message
response = assistant.send("How do I reset my password?")
Api.sendMessage(response['content'])
```
### Google Gemini Integration
```python
# Create Gemini client
gemini_client = Lib.AI.client(
provider="gemini",
apiKey="YOUR_GEMINI_API_KEY"
)
# Generate response
response = gemini_client.chat(
model="gemini-2.0-flash",
messages=[
{"role": "user", "content": msg}
]
)
Api.sendMessage(response['choices'][0]['message']['content'])
```
***
## Advanced Resource Management
### Cross-User Resource Operations
```python
# Award points to multiple users
winners = [12345, 67890, 54321]
for winner_id in winners:
winner_points = User.resOf("points", winner_id)
winner_points.add(100)
Api.sendMessage(f"Awarded 100 points to user {winner_id}")
```
### Resource Leaderboards
```python
# Get top performers
top_users = User.res("points").exportAllData(limit=10)
Api.sendMessage("🏆 Top 10 Leaderboard:")
for idx, entry in enumerate(top_users, 1):
medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
Api.sendMessage(f"{medal} User {entry['user_id']}: {entry['value']} points")
```
***
## Time-Based Operations
### Lib.DateTime Methods
#### utcnow()
Returns current UTC date and time.
**Returns:** String in format "YYYY-MM-DD HH:MM:SS"
#### now()
Returns current time in specified timezone.
**Syntax:**
```python
Lib.DateTime.now(timezone_str)
```
**Parameters:**
* `timezone_str` (Required): Timezone name (e.g., "Asia/Tokyo")
**Returns:** String with localized date and time
#### time()
Returns current UNIX timestamp.
**Returns:** Float representing seconds since epoch
**Example:**
```python
# Get current time
current_time = Lib.DateTime.utcnow()
Api.sendMessage(f"Current UTC time: {current_time}")
# Get timezone-specific time
tokyo_time = Lib.DateTime.now("Asia/Tokyo")
Api.sendMessage(f"Time in Tokyo: {tokyo_time}")
# Get timestamp
timestamp = Lib.DateTime.time()
User.storeData("last_action", timestamp)
```
### Sleep Functionality
```python
# Pause execution (max 10 seconds)
Api.sendMessage("Processing...")
time.sleep(3) # Wait 3 seconds
Api.sendMessage("Done!")
```
***
## Payment Integration
### Oxapay Integration
#### Lib.Oxapay.post()
Initializes Oxapay client.
**Syntax:**
```python
Lib.Oxapay.post(merchant_api_key)
```
**Parameters:**
* `merchant_api_key` (Required): Your Oxapay merchant API key
**Returns:** Oxapay client object
**Example:**
```python
# Initialize Oxapay
client = Lib.Oxapay.post("YOUR_MERCHANT_API_KEY")
# Create invoice
invoice = client.createInvoice({
"amount": 50,
"currency": "USD",
"description": "Service payment"
})
Api.sendMessage(f"Payment link: {invoice['url']}")
```
***
This comprehensive guide covers advanced features in TeleBot Studio. By mastering these techniques, you can build enterprise-grade bots with complex workflows, external integrations, and sophisticated data management capabilities.
