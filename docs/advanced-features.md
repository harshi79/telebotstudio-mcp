> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/advanced-features.md).
# Advanced Features
This section explores advanced capabilities and techniques in TeleBot Studio that enable you to build sophisticated, enterprise-grade Telegram bots. From complex workflow automation to external API integrations and multi-bot orchestration, these features unlock the full potential of the platform.
\*\*\*
## Environment Variables
### Overview
\*\*Environment Variables\*\* provide a secure, centralized way to manage configuration settings, API keys, credentials, and other sensitive data for your bot. Variables set through the dashboard are \*\*automatically available in your bot commands\*\* as Python variables.
### Benefits
✅ \*\*Security\*\* - Keep sensitive data (API keys, tokens) out of your code\
✅ \*\*Easy Management\*\* - Update values through dashboard without code changes\
✅ \*\*Automatic Access\*\* - Variables are instantly available in your commands\
✅ \*\*Best Practice\*\* - Industry-standard approach for credentials management\
✅ \*\*No Redeployment\*\* - Change values without restarting your bot
### Managing Environment Variables
Navigate to \*\*Bot Management → Env\*\* tab to manage your environment variables:
\*\*Add New Variable:\*\*
1. Click "Add Variable"
2. Enter variable name (use UPPERCASE with underscores: `OPENAI\_API\_KEY`, `MERCHANT\_ID`)
3. Enter value
4. Save
\*\*Edit Variable:\*\*
\* Both variable name and value can be edited
\* Click edit icon next to variable
\* Update name or value
\* Save changes
\*\*Delete Variable:\*\*
\* Click delete icon next to variable
\* Confirm deletion
\*\*Naming Convention:\*\*
\* Use UPPERCASE letters
\* Separate words with underscores
\* Examples: `API\_KEY`, `DATABASE\_URL`, `MAIL\_USERNAME`, `WEBHOOK\_SECRET`
### Using Environment Variables in Code
Environment variables are \*\*automatically available\*\* in your bot commands - just use them like any Python variable:
```python
# Environment variable OPENAI\_API\_KEY is automatically available
ai\_client = Lib.AI.client(provider="openai", apiKey=OPENAI\_API\_KEY)
Api.sendMessage("AI initialized successfully!")
# Use PORT variable with fallback
port = PORT if 'PORT' in dir() else "5000"
# Example with payment gateway
client = Lib.Oxapay.post(OXAPAY\_MERCHANT\_KEY)
# Use in API requests
response = Request.get(
f"https://api.weatherapi.com/v1/current.json?key={WEATHER\_API\_KEY}&q=London"
)
```
### Scope and Behavior
\*\*Variable Overriding:\*\* If you define a variable with the same name in your command code, your local definition overrides the environment variable for that specific command:
```python
# Environment variable: API\_KEY = "env\_value\_123"
# In command code:
API\_KEY = "local\_value\_456" # This overrides the env variable
# Local definition takes precedence
Api.sendMessage(f"Using: {API\_KEY}") # Outputs: "Using: local\_value\_456"
```
\*\*On Bot Cloning:\*\*
\* ✅ \*\*Both variable names AND values\*\* are copied to the cloned bot
\* ⚠️ \*\*Review after cloning\*\* - Update sensitive values like API keys, merchant IDs, or bot tokens if the cloned bot needs separate credentials
\*\*On Bot Transfer:\*\*
\* ✅ \*\*Variable names\*\* are transferred
\* ❌ \*\*Variable values\*\* are NOT transferred (for security)
\* 📝 Recipient must configure their own values after transfer
\* 🔒 Protects sensitive credentials during ownership transfers
### Common Use Cases
\*\*API Keys:\*\*
```python
# Set in Env tab:
# OPENAI\_API\_KEY = sk-abc123...
# GEMINI\_API\_KEY = AIza...
# SENDGRID\_API\_KEY = SG.xyz...
# Use directly in code:
ai\_client = Lib.AI.client(provider="openai", apiKey=OPENAI\_API\_KEY)
```
\*\*Payment Gateways:\*\*
```python
# Set in Env tab:
# OXAPAY\_MERCHANT\_KEY = merchant\_12345
# STRIPE\_SECRET\_KEY = sk\_live\_...
# Use directly in code:
oxapay = Lib.Oxapay.post(OXAPAY\_MERCHANT\_KEY)
```
\*\*Configuration:\*\*
```python
# Set in Env tab:
# BASE\_URL = https://mybot.com
# DEBUG\_MODE = false
# MAX\_RETRIES = 3
# Use directly in code:
if DEBUG\_MODE == "true":
Api.sendMessage("Debug mode enabled")
```
### Best Practices
1. \*\*Never hardcode secrets in your code\*\*
```python
# ❌ Bad
api\_key = "sk-abc123xyz..."
# ✅ Good - Set in Env tab, use directly
ai\_client = Lib.AI.client(provider="openai", apiKey=OPENAI\_API\_KEY)
```
2. \*\*Use descriptive variable names\*\*
```
# ✅ Good
OPENAI\_API\_KEY
PAYMENT\_WEBHOOK\_URL
DATABASE\_CONNECTION\_STRING
# ❌ Bad
KEY1, URL, DB
```
3. \*\*Check if variable exists before using\*\*
```python
# Check if environment variable is set
if 'OPENAI\_API\_KEY' not in dir():
Api.sendMessage("⚠️ Please configure OPENAI\_API\_KEY in Env settings")
return
# Now safe to use
ai\_client = Lib.AI.client(provider="openai", apiKey=OPENAI\_API\_KEY)
```
4. \*\*Use separate values for development and production\*\*
```
# Development bot Env settings:
STRIPE\_KEY = sk\_test\_...
DEBUG\_MODE = true
# Production bot Env settings:
STRIPE\_KEY = sk\_live\_...
DEBUG\_MODE = false
```
\*\*\*
## Advanced Scheduling Techniques
TeleBot Studio's scheduling system offers precise control over command execution timing with support for delays from 0.1 seconds to 1 year.
### Bot.scheduleCommand()
Schedule a command to execute after a specified delay.
\*\*Syntax:\*\*
```python
Bot.scheduleCommand(delay\_seconds, command, user\_id=None, chat\_id=None, params=None, \*\*options)
```
\*\*Parameters:\*\*
\* `delay\_seconds` (Required): Delay in seconds (0.1 to 31536000 - one year)
\* `command` (Required): Name of the command to execute
\* `user\_id` (Optional): Target user ID
\* `chat\_id` (Optional): Target chat ID
\* `params` (Optional): Parameters to pass to the command
\* `\*\*options` (Optional): Additional options passed to the command
\*\*Returns:\*\* None
\*\*Rate Limiting:\*\*
\* For commands scheduled under 0.4 seconds: Maximum 5 executions within 5 seconds
\* Maximum 100 scheduled commands per user
### Micro-Scheduling for Performance
Execute commands with minimal delay for time-sensitive operations:
```python
# Quick follow-up message (0.2 seconds)
Api.sendMessage("Processing your request...")
Bot.scheduleCommand(0.2, "send\_result")
```
### Cascading Scheduled Tasks
Chain multiple scheduled commands for complex workflows:
```python
# Multi-stage notification system
Api.sendMessage("Order confirmed! We'll keep you updated.")
Bot.scheduleCommand(60, "order\_preparing") # 1 minute
Bot.scheduleCommand(300, "order\_shipping") # 5 minutes
Bot.scheduleCommand(1800, "order\_delivered") # 30 minutes
```
\*\*Order Preparing Command:\*\*
```python
Api.sendMessage("👨‍🍳 Your order is being prepared!")
```
\*\*Order Shipping Command:\*\*
```python
Api.sendMessage("📦 Your order has been shipped!")
tracking\_number = Bot.uniqueID()
User.storeData("tracking", tracking\_number)
Api.sendMessage(f"Tracking: {tracking\_number}")
```
\*\*Order Delivered Command:\*\*
```python
Api.sendMessage("✅ Your order has been delivered!")
Api.sendMessage("Please rate your experience: /rate")
```
### Conditional Scheduling
Schedule tasks based on user actions or conditions:
```python
reminder\_enabled = User.fetchData("reminders\_enabled")
if reminder\_enabled:
Bot.scheduleCommand(86400, "daily\_reminder") # 24 hours
Api.sendMessage("Daily reminder scheduled!")
```
\*\*\*
## Complex Command Chaining Workflows
Build sophisticated multi-step processes that guide users through intricate operations.
### Bot.waitForInput()
Waits for the next user message and routes it to a specific command.
\*\*Syntax:\*\*
```python
Bot.waitForInput(command, \*\*options)
```
\*\*Parameters:\*\*
\* `command` (Required): Name of the command to execute when user sends next message
\* `\*\*options` (Optional): Dictionary of options passed to the command via `options` global variable
\*\*Returns:\*\* None
\*\*Example:\*\*
```python
Api.sendMessage("What's your name?")
Bot.waitForInput("process\_name", greeting="Hello")
```
In the `process\_name` command:
```python
name = msg
greeting = options.get('greeting', 'Hi')
Api.sendMessage(f"{greeting}, {name}!")
```
### Multi-Step Form with Validation
\*\*Step 1 - Initiate Process:\*\*
```python
# /register\_business command
Api.sendMessage("🏢 Business Registration")
Api.sendMessage("Let's start with your business name:")
Bot.waitForInput("get\_business\_name")
```
\*\*Step 2 - Validate Business Name:\*\*
```python
# get\_business\_name command
business\_name = msg
if len(business\_name) < 3:
Api.sendMessage("Business name too short. Please enter at least 3 characters:")
Bot.waitForInput("get\_business\_name")
elif len(business\_name) > 50:
Api.sendMessage("Business name too long. Maximum 50 characters:")
Bot.waitForInput("get\_business\_name")
else:
User.storeData("business\_name", business\_name)
Api.sendMessage(f"✅ Business name: {business\_name}")
Api.sendMessage("What's your business type? (Retail/Service/Manufacturing/Other)")
Bot.waitForInput("get\_business\_type")
```
\*\*Step 3 - Process Business Type:\*\*
```python
# get\_business\_type command
business\_type = msg.lower()
valid\_types = ["retail", "service", "manufacturing", "other"]
if business\_type not in valid\_types:
Api.sendMessage("Invalid type. Choose: Retail, Service, Manufacturing, or Other")
Bot.waitForInput("get\_business\_type")
else:
User.storeData("business\_type", business\_type)
Api.sendMessage("How many employees? (Enter a number)")
Bot.waitForInput("get\_employee\_count")
```
\*\*Step 4 - Validate Numeric Input:\*\*
```python
# get\_employee\_count command
employee\_input = msg
if not employee\_input.isdigit():
Api.sendMessage("Please enter a valid number:")
Bot.waitForInput("get\_employee\_count")
else:
employee\_count = int(employee\_input)
User.storeData("employee\_count", employee\_count)
# Generate business profile
Api.sendMessage("📋 Business Profile Created:")
Api.sendMessage(f"Name: {User.fetchData('business\_name')}")
Api.sendMessage(f"Type: {User.fetchData('business\_type')}")
Api.sendMessage(f"Employees: {employee\_count}")
# Assign business tier
tier = "Enterprise" if employee\_count > 100 else "Business" if employee\_count > 10 else "Startup"
User.storeData("business\_tier", tier)
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
Bot.waitForInput("support\_router")
```
\*\*Support Router:\*\*
```python
# support\_router command
choice = msg
if choice == "1":
Api.sendMessage("Describe your technical issue:")
Bot.waitForInput("handle\_technical")
elif choice == "2":
Api.sendMessage("What's your billing question?")
Bot.waitForInput("handle\_billing")
elif choice == "3":
Api.sendMessage("Tell us about your feature idea:")
Bot.waitForInput("handle\_feature\_request")
else:
Api.sendMessage("Invalid choice. Reply with 1, 2, or 3:")
Bot.waitForInput("support\_router")
```
\*\*\*
## Advanced API Integrations
Leverage external services to extend your bot's capabilities with real-time data and third-party functionality.
### HTTP Request Methods
TeleBot Studio provides comprehensive HTTP support through the `Request` module.
#### Request.get()
Performs an HTTP GET request.
\*\*Syntax:\*\*
```python
Request.get(url, \*\*kwargs)
```
\*\*Parameters:\*\*
\* `url` (Required): The URL to request
\* `headers` (Optional): Dictionary of HTTP headers
\* `params` (Optional): Dictionary of URL parameters
\* `timeout` (Optional): Request timeout in seconds (default: 30)
\* `\*\*kwargs` (Optional): Additional requests library parameters
\*\*Returns:\*\* `TBS\_HTTP\_Response` object with attributes:
\* `status\_code` (int): HTTP status code
\* `text` (str): Response body as text
\* `content` (bytes): Response body as bytes
\* `headers` (dict): Response headers
\* `ok` (bool): True if status code is 200-299
\* `url` (str): Final URL after redirects
\* `json()` (method): Parse response as JSON
\*\*Example:\*\*
```python
response = Request.get("https://api.example.com/data")
if response.status\_code == 200:
data = response.json()
Api.sendMessage(f"Result: {data['value']}")
else:
Api.sendMessage(f"Error: {response.status\_code}")
```
#### Request.post()
Performs an HTTP POST request.
\*\*Syntax:\*\*
```python
Request.post(url, \*\*kwargs)
```
\*\*Parameters:\*\*
\* `url` (Required): The URL to request
\* `json` (Optional): Dictionary to send as JSON body
\* `data` (Optional): Dictionary or string to send as form data
\* `headers` (Optional): Dictionary of HTTP headers
\* `timeout` (Optional): Request timeout in seconds (default: 30)
\* `\*\*kwargs` (Optional): Additional requests library parameters
\*\*Returns:\*\* `TBS\_HTTP\_Response` object (same attributes as GET)
\*\*Example:\*\*
```python
payload = {
"username": User.fetchData("name"),
"email": User.fetchData("email"),
"action": "register"
}
response = Request.post(
"https://api.example.com/users",
json=payload,
headers={"Authorization": "Bearer YOUR\_API\_KEY"}
)
if response.ok:
Api.sendMessage("✅ Registration successful!")
result = response.json()
User.storeData("external\_id", result['user\_id'])
else:
Api.sendMessage(f"❌ Registration failed: {response.status\_code}")
```
#### Request.put()
Performs an HTTP PUT request.
\*\*Syntax:\*\*
```python
Request.put(url, \*\*kwargs)
```
\*\*Parameters:\*\* Same as `Request.post()`
\*\*Returns:\*\* `TBS\_HTTP\_Response` object
\*\*Example:\*\*
```python
update\_data = {"status": "active", "last\_seen": time.time()}
response = Request.put(
f"https://api.example.com/users/{u}",
json=update\_data
)
```
#### Request.delete()
Performs an HTTP DELETE request.
\*\*Syntax:\*\*
```python
Request.delete(url, \*\*kwargs)
```
\*\*Parameters:\*\* Same as `Request.get()`
\*\*Returns:\*\* `TBS\_HTTP\_Response` object
\*\*Example:\*\*
```python
response = Request.delete(f"https://api.example.com/users/{u}")
if response.status\_code == 204:
Api.sendMessage("Account deleted successfully")
```
#### Request.patch()
Performs an HTTP PATCH request.
\*\*Syntax:\*\*
```python
Request.patch(url, \*\*kwargs)
```
\*\*Parameters:\*\* Same as `Request.post()`
\*\*Returns:\*\* `TBS\_HTTP\_Response` object
### Weather API Integration
```python
# Get weather data
api\_key = "YOUR\_WEATHER\_API\_KEY"
city = User.fetchData("city") or "London"
response = Request.get(
f"https://api.weatherapi.com/v1/current.json?key={api\_key}&q={city}"
)
if response.ok:
weather = response.json()
Api.sendMessage(f"🌤 Weather in {city}:")
Api.sendMessage(f"Temperature: {weather['current']['temp\_c']}°C")
Api.sendMessage(f"Condition: {weather['current']['condition']['text']}")
Api.sendMessage(f"Humidity: {weather['current']['humidity']}%")
else:
Api.sendMessage("Could not fetch weather data.")
```
### Cryptocurrency Price Tracking
```python
# Track crypto prices
response = Request.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs\_currencies=usd")
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
"https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR\_API\_KEY"
)
if response.ok:
news\_data = response.json()
articles = news\_data['articles'][:5] # Top 5 articles
Api.sendMessage("📰 Latest News:")
for idx, article in enumerate(articles, 1):
Api.sendMessage(f"{idx}. {article['title']}")
Api.sendMessage(f" {article['url']}")
```
\*\*\*
## Advanced Webhook Integration
Create sophisticated webhook-based integrations for real-time event handling.
### Lib.Webhook.getUrlFor()
Generates a webhook URL for invoking a specific command.
\*\*Syntax:\*\*
```python
Lib.Webhook.getUrlFor(command, user\_id=None, chat\_id=None, bot\_id=None, api\_key=None, \*\*options)
```
\*\*Parameters:\*\*
\* `command` (Required): Name of the command to invoke
\* `user\_id` (Optional): Specific user ID for user-specific webhook
\* `chat\_id` (Optional): Specific chat ID for chat-specific webhook
\* `bot\_id` (Optional): Target another bot by ID
\* `api\_key` (Optional): API key for the target bot (required with bot\\_id)
\* `\*\*options` (Optional): Additional data passed to the command via `options` variable
\*\*Returns:\*\* String containing the webhook URL
\*\*Example:\*\*
```python
# Generate personalized webhook
webhook\_url = Lib.Webhook.getUrlFor("payment\_received", user\_id=u)
User.storeData("payment\_webhook", webhook\_url)
Api.sendMessage(f"Your payment webhook:\n{webhook\_url}")
```
### Cross-Bot Communication
Enable multiple bots to work together:
```python
# Bot A triggers Bot B
bot\_b\_webhook = Lib.Webhook.getUrlFor(
"process\_notification",
bot\_id="bot\_b\_id",
api\_key="bot\_b\_api\_key",
user\_id=u
)
# Trigger Bot B
response = Request.post(bot\_b\_webhook, json={"message": "Hello from Bot A"})
```
### Webhook Command Handler
```python
# process\_notification command (in Bot B)
webhook\_data = options
sender\_bot = webhook\_data.get('bot\_id', 'Unknown')
message\_content = webhook\_data.get('message', '')
Api.sendMessage(f"Received from {sender\_bot}: {message\_content}")
# Process and respond
User.storeData("last\_notification", message\_content)
Api.sendMessage("Notification processed!")
```
### Payment Gateway Integration
```python
# Create payment webhook
payment\_webhook = Lib.Webhook.getUrlFor("handle\_payment", user\_id=u)
# Send to payment provider
Api.sendMessage("Complete your payment:")
Api.sendMessage(payment\_webhook)
```
\*\*Handle Payment Command:\*\*
```python
# handle\_payment command
payment\_data = options
amount = payment\_data.get('amount', 0)
currency = payment\_data.get('currency', 'USD')
status = payment\_data.get('status', 'pending')
if status == 'completed':
# Award credits
credits = User.res("credits")
credits.add(int(amount))
Api.sendMessage(f"✅ Payment successful!")
Api.sendMessage(f"Added {amount} {currency} to your account")
Api.sendMessage(f"Current balance: {credits.value()} credits")
# Send receipt
receipt\_data = f"Amount: {amount} {currency}\nStatus: {status}\nDate: {Lib.DateTime.utcnow()}"
User.storeData("last\_receipt", receipt\_data)
else:
Api.sendMessage(f"Payment status: {status}")
```
\*\*\*
## Bot Transfer Functionality
### Bot.transfer()
Creates a copy of your bot and transfers it to another TeleBot Studio account. The original bot remains in your account.
\*\*Syntax:\*\*
```python
Bot.transfer(email, bot\_id, bot\_token=None, run\_now=False)
```
\*\*Parameters:\*\*
\* `email` (Required): Email address of the recipient's TeleBot Studio account
\* `bot\_id` (Required): The bot ID to transfer
\* `bot\_token` (Optional): Telegram bot token (required if run\\_now is True)
\* `run\_now` (Optional): If True, starts the bot immediately in the new account
\*\*Returns:\*\* Dictionary with attributes:
\* `ok` (bool): True if transfer successful
\* `bot\_id` (str): The bot ID that was transferred
\* `new\_owner` (str): Email of the new owner
\* `error` (str): Error message if ok is False
\*\*Example:\*\*
```python
# Transfer bot copy to another account
try:
result = Bot.transfer(
email="recipient@example.com",
bot\_id=bot\_id,
bot\_token="YOUR\_BOT\_TOKEN",
run\_now=True
)
if result['ok']:
Api.sendMessage("✅ Bot copy transferred successfully!")
Api.sendMessage(f"Recipient: {result['new\_owner']}")
Api.sendMessage(f"Bot ID: {result['bot\_id']}")
Api.sendMessage("Note: Your original bot remains in your account.")
else:
Api.sendMessage(f"❌ Transfer failed: {result['error']}")
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"Transfer error {error\_id}: {str(e)}")
```
### Batch Bot Transfer
Transfer copies of multiple bots:
```python
# Transfer multiple bot copies
bots\_to\_transfer = [
{"bot\_id": "123456", "token": "TOKEN1"},
{"bot\_id": "789012", "token": "TOKEN2"},
{"bot\_id": "345678", "token": "TOKEN3"}
]
target\_email = "recipient@example.com"
success\_count = 0
failed\_bots = []
for bot\_data in bots\_to\_transfer:
try:
result = Bot.transfer(
email=target\_email,
bot\_id=bot\_data['bot\_id'],
bot\_token=bot\_data['token'],
run\_now=False
)
if result['ok']:
success\_count += 1
Api.sendMessage(f"✅ Bot {bot\_data['bot\_id']} copy transferred")
else:
failed\_bots.append(bot\_data['bot\_id'])
except Exception as e:
failed\_bots.append(bot\_data['bot\_id'])
Api.sendMessage(f"❌ {bot\_data['bot\_id']}: {str(e)}")
# Summary
Api.sendMessage(f"\n📊 Transfer Summary:")
Api.sendMessage(f"Successful: {success\_count}")
Api.sendMessage(f"Failed: {len(failed\_bots)}")
if failed\_bots:
Api.sendMessage(f"Failed IDs: {', '.join(failed\_bots)}")
```
### Bot Information Retrieval
#### Bot.getInfo()
Retrieves comprehensive information about a bot.
\*\*Syntax:\*\*
```python
Bot.getInfo(bot\_id=None, api\_key=None)
```
\*\*Parameters:\*\*
\* `bot\_id` (Optional): Bot ID to query (defaults to current bot)
\* `api\_key` (Optional): API key for accessing another bot
\*\*Returns:\*\* Dictionary with attributes:
\* `token` (str): Bot token
\* `bot\_id` (str): Platform bot ID
\* `owner\_email` (str): Owner's email address
\* `status` (str): "Working" or "Stopped"
\* `username` (str): Bot's Telegram username
\* `first\_name` (str): Bot's display name
\* `account\_points` (int): Owner's remaining points
\* `userstat` (int): Total number of bot users
\*\*Example:\*\*
```python
# Get comprehensive bot details
bot\_details = Bot.getInfo()
Api.sendMessage("🤖 Bot Information:")
Api.sendMessage(f"Name: {bot\_details['first\_name']}")
Api.sendMessage(f"Username: @{bot\_details['username']}")
Api.sendMessage(f"ID: {bot\_details['bot\_id']}")
Api.sendMessage(f"Status: {bot\_details['status']}")
# Additional stats if available
if 'userstat' in bot\_details:
Api.sendMessage(f"Total Users: {bot\_details['userstat']}")
```
\*\*\*
## Advanced Error Handling Strategies
### Comprehensive Error Management
```python
try:
# Critical operation
response = Request.post("https://api.example.com/critical", json=data)
response.raise\_for\_status()
result = response.json()
Api.sendMessage("✅ Operation successful!")
except ConnectionError as ce:
# Network issues
Api.sendMessage("🌐 Connection error. Retrying in 5 seconds...")
Bot.scheduleCommand(5, "retry\_operation")
retry\_count = User.fetchData("retry\_count") or 0
User.storeData("retry\_count", retry\_count + 1)
except ValueError as ve:
# Data validation errors
Api.sendMessage(f"❌ Invalid data: {str(ve)}")
Api.sendMessage("Please check your input and try again.")
except Exception as e:
# Catch-all for unexpected errors
error\_id = Bot.errorID()
error\_details = {
"error\_id": error\_id,
"user\_id": u,
"timestamp": time.time(),
"error\_type": type(e).\_\_name\_\_,
"error\_message": str(e),
"command": "current\_command\_name"
}
# Log error
Bot.storeData(f"error\_{error\_id}", error\_details)
# Notify user
Api.sendMessage(f"❌ An error occurred.")
Api.sendMessage(f"Error ID: {error\_id}")
Api.sendMessage("Our team has been notified.")
# Notify admin
Api.sendMessage(
f"🚨 Error {error\_id}\nUser: {u}\nType: {type(e).\_\_name\_\_}\nMessage: {str(e)}",
chat\_id="ADMIN\_CHAT\_ID"
)
```
### Retry Logic with Exponential Backoff
```python
# Initial attempt
retry\_count = User.fetchData("operation\_retry\_count") or 0
max\_retries = 3
if retry\_count < max\_retries:
try:
# Attempt operation
response = Request.get("https://api.example.com/data")
if response.ok:
# Success - reset retry counter
User.removeData("operation\_retry\_count")
Api.sendMessage("✅ Operation successful!")
else:
raise Exception(f"HTTP {response.status\_code}")
except Exception as e:
retry\_count += 1
User.storeData("operation\_retry\_count", retry\_count)
# Exponential backoff: 2, 4, 8 seconds
delay = 2 \*\* retry\_count
Api.sendMessage(f"Attempt {retry\_count} failed. Retrying in {delay}s...")
Bot.scheduleCommand(delay, "retry\_operation")
else:
# Max retries exceeded
User.removeData("operation\_retry\_count")
Api.sendMessage("❌ Operation failed after multiple attempts.")
Api.sendMessage("Please try again later or contact support.")
```
\*\*\*
## Multi-Bot Orchestration
### Master-Slave Bot Architecture
\*\*Master Bot - Distributes Tasks:\*\*
```python
# Master bot receives task
task\_type = msg
task\_id = Bot.uniqueID()
# Determine which slave bot handles this task type
bot\_mapping = {
"payment": {"bot\_id": "payment\_bot\_id", "api\_key": "payment\_api\_key"},
"notification": {"bot\_id": "notif\_bot\_id", "api\_key": "notif\_api\_key"},
"analytics": {"bot\_id": "analytics\_bot\_id", "api\_key": "analytics\_api\_key"}
}
if task\_type in bot\_mapping:
bot\_config = bot\_mapping[task\_type]
webhook = Lib.Webhook.getUrlFor(
f"handle\_{task\_type}",
bot\_id=bot\_config['bot\_id'],
api\_key=bot\_config['api\_key'],
user\_id=u
)
# Send task to slave bot
response = Request.post(webhook, json={"task\_id": task\_id, "user\_id": u})
Api.sendMessage(f"Task {task\_id} assigned to {task\_type} bot")
else:
Api.sendMessage("Unknown task type")
```
\*\*Slave Bot - Executes Task:\*\*
```python
# handle\_payment command (in payment bot)
task\_data = options
task\_id = task\_data.get('task\_id')
user\_id = task\_data.get('user\_id')
Api.sendMessage(f"Processing payment task {task\_id}", chat\_id=user\_id)
# Execute payment logic
Api.sendMessage("Payment processed successfully!", chat\_id=user\_id)
```
\*\*\*
## CSV Data Management
### Lib.CSV.Table
Manages structured data efficiently with CSV operations.
\*\*Syntax:\*\*
```python
csv\_handler = Lib.CSV.Table(filename)
```
#### Methods:
\*\*create()\*\* - Create CSV with headers
```python
csv\_handler.create(["column1", "column2", "column3"])
```
\*\*insert()\*\* - Add row
```python
csv\_handler.insert({"column1": "value1", "column2": "value2"})
```
\*\*row()\*\* - Get specific row by index
```python
row\_data = csv\_handler.row(0) # Returns dictionary
```
\*\*update()\*\* - Update row by index
```python
csv\_handler.update(0, {"column1": "new\_value"})
```
\*\*delete()\*\* - Delete row by index
```python
csv\_handler.delete(1)
```
\*\*toString()\*\* - Export as string
```python
csv\_string = csv\_handler.toString()
```
\*\*Example:\*\*
```python
# Initialize CSV handler
csv\_handler = Lib.CSV.Table("users\_data.csv")
# Create CSV with headers
csv\_handler.create(["user\_id", "name", "email", "points"])
# Add rows
csv\_handler.insert({"user\_id": u, "name": "John", "email": "john@example.com", "points": 100})
csv\_handler.insert({"user\_id": u+1, "name": "Jane", "email": "jane@example.com", "points": 150})
Api.sendMessage("User data saved to CSV!")
# Query data
user\_row = csv\_handler.row(0)
Api.sendMessage(f"User: {user\_row['name']}, Points: {user\_row['points']}")
# Update row
csv\_handler.update(0, {"points": 200})
# Export CSV
csv\_string = csv\_handler.toString()
Api.sendMessage(f"CSV Data:\n{csv\_string}")
```
\*\*\*
## Cryptocurrency and Blockchain Integration
### TON Blockchain Operations
#### Lib.TON.createWallet()
Generates a new TON wallet.
\*\*Returns:\*\* Dictionary with attributes:
\* `address` (str): Wallet address
\* `mnemonics` (str): 24-word recovery phrase
\*\*Example:\*\*
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
\*\*Syntax:\*\*
```python
Lib.TON.balance(address, api\_key=None, endpoint=None)
```
\*\*Parameters:\*\*
\* `address` (Required): TON wallet address
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\*\*Returns:\*\* Float representing balance in TON
\*\*Example:\*\*
```python
address = "EQD..."
balance = Lib.TON.balance(address)
Api.sendMessage(f"Balance: {balance} TON")
```
#### Lib.TON.send()
Transfers TON to another address.
\*\*Syntax:\*\*
```python
Lib.TON.send(to\_address, amount, comment=None, mnemonics=None, api\_key=None, endpoint=None, is\_testnet=False)
```
\*\*Parameters:\*\*
\* `to\_address` (Required): Recipient wallet address
\* `amount` (Required): Amount to send in TON
\* `comment` (Optional): Transaction comment
\* `mnemonics` (Optional): Wallet mnemonics (uses stored if not provided)
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\* `is\_testnet` (Optional): Use testnet if True
\*\*Returns:\*\* Dictionary with transaction details
\*\*Example:\*\*
```python
result = Lib.TON.send(
to\_address="EQD...",
amount=0.5,
comment="Payment for service"
)
Api.sendMessage("TON sent successfully!")
```
### EVM Blockchain Operations
#### Lib.EVM.sendCoin()
Sends native cryptocurrency (ETH, BNB, MATIC, etc.).
\*\*Syntax:\*\*
```python
Lib.EVM.sendCoin(network, to, value, private\_key=None, gas\_limit=None, gas\_price=None, proxy=None, estimate\_gas=True, retry=False)
```
\*\*Parameters:\*\*
\* `network` (Required): Network name (ethereum, bsc, polygon, etc.)
\* `to` (Required): Recipient address
\* `value` (Required): Amount to send
\* `private\_key` (Optional): Sender's private key (uses stored if not provided)
\* `gas\_limit` (Optional): Gas limit for transaction
\* `gas\_price` (Optional): Gas price in Gwei
\* `proxy` (Optional): Proxy configuration
\* `estimate\_gas` (Optional): Auto-estimate gas (default True)
\* `retry` (Optional): Retry once on failure (default False)
\*\*Returns:\*\* Transaction hash string
\*\*Example:\*\*
```python
# Store private key
Lib.EVM.storeKey("your\_private\_key")
# Send Ethereum
tx\_hash = Lib.EVM.sendCoin(
network="ethereum",
to="0x...",
value=0.1
)
Api.sendMessage(f"Transaction: {tx\_hash}")
```
#### Lib.EVM.sendToken()
Sends ERC-20 tokens.
\*\*Syntax:\*\*
```python
Lib.EVM.sendToken(network, to, value, contract\_address, private\_key=None, gas\_limit=None, gas\_price=None, proxy=None, estimate\_gas=True, retry=False)
```
\*\*Parameters:\*\* Same as sendCoin() plus:
\* `contract\_address` (Required): Token contract address
\*\*Returns:\*\* Transaction hash string
\*\*Example:\*\*
```python
# Send USDT on Ethereum
tx\_hash = Lib.EVM.sendToken(
network="ethereum",
to="0x...",
value=100,
contract\_address="0xdac17f958d2ee523a2206206994597c13d831ec7" # USDT
)
Api.sendMessage(f"USDT sent: {tx\_hash}")
```
#### Lib.EVM.networks()
Gets supported blockchain networks.
\*\*Returns:\*\* Dictionary of supported networks with their details
\*\*Example:\*\*
```python
networks = Lib.EVM.networks()
Api.sendMessage(f"Supported networks: {list(networks.keys())}")
```
\*\*\*
## AI Integration
### Lib.AI.client()
Creates an AI client for OpenAI or Google Gemini.
\*\*Syntax:\*\*
```python
Lib.AI.client(provider='openai', apiKey=None, baseUrl=None, \*\*kwargs)
```
\*\*Parameters:\*\*
\* `provider` (Optional): 'openai' or 'gemini' (default: 'openai')
\* `apiKey` (Required): API key for the provider
\* `baseUrl` (Optional): Custom API base URL (OpenAI only)
\* `\*\*kwargs` (Optional): Additional provider-specific parameters
\*\*Returns:\*\* AI client object
### OpenAI Integration
\*\*Simple Chat Completion:\*\*
```python
# Create AI client
ai\_client = Lib.AI.client(
provider="openai",
apiKey="YOUR\_OPENAI\_API\_KEY"
)
# Generate response
response = ai\_client.chat(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": msg}
]
)
Api.sendMessage(response['choices'][0]['message']['content'])
```
\*\*Assistant with Memory:\*\*
```python
# Create persistent assistant
assistant = Lib.AI.Assistant(
provider="openai",
apiKey="YOUR\_API\_KEY",
create\_new=True,
name="Support Bot",
instructions="You are a technical support assistant.",
model="gpt-4"
)
# Start conversation
thread\_id = assistant.start()
User.storeData("ai\_thread", thread\_id)
# Send message
response = assistant.send("How do I reset my password?")
Api.sendMessage(response['content'])
```
### Google Gemini Integration
```python
# Create Gemini client
gemini\_client = Lib.AI.client(
provider="gemini",
apiKey="YOUR\_GEMINI\_API\_KEY"
)
# Generate response
response = gemini\_client.chat(
model="gemini-2.0-flash",
messages=[
{"role": "user", "content": msg}
]
)
Api.sendMessage(response['choices'][0]['message']['content'])
```
\*\*\*
## Advanced Resource Management
### Cross-User Resource Operations
```python
# Award points to multiple users
winners = [12345, 67890, 54321]
for winner\_id in winners:
winner\_points = User.resOf("points", winner\_id)
winner\_points.add(100)
Api.sendMessage(f"Awarded 100 points to user {winner\_id}")
```
### Resource Leaderboards
```python
# Get top performers
top\_users = User.res("points").exportAllData(limit=10)
Api.sendMessage("🏆 Top 10 Leaderboard:")
for idx, entry in enumerate(top\_users, 1):
medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
Api.sendMessage(f"{medal} User {entry['user\_id']}: {entry['value']} points")
```
\*\*\*
## Time-Based Operations
### Lib.DateTime Methods
#### utcnow()
Returns current UTC date and time.
\*\*Returns:\*\* String in format "YYYY-MM-DD HH:MM:SS"
#### now()
Returns current time in specified timezone.
\*\*Syntax:\*\*
```python
Lib.DateTime.now(timezone\_str)
```
\*\*Parameters:\*\*
\* `timezone\_str` (Required): Timezone name (e.g., "Asia/Tokyo")
\*\*Returns:\*\* String with localized date and time
#### time()
Returns current UNIX timestamp.
\*\*Returns:\*\* Float representing seconds since epoch
\*\*Example:\*\*
```python
# Get current time
current\_time = Lib.DateTime.utcnow()
Api.sendMessage(f"Current UTC time: {current\_time}")
# Get timezone-specific time
tokyo\_time = Lib.DateTime.now("Asia/Tokyo")
Api.sendMessage(f"Time in Tokyo: {tokyo\_time}")
# Get timestamp
timestamp = Lib.DateTime.time()
User.storeData("last\_action", timestamp)
```
### Sleep Functionality
```python
# Pause execution (max 10 seconds)
Api.sendMessage("Processing...")
time.sleep(3) # Wait 3 seconds
Api.sendMessage("Done!")
```
\*\*\*
## Payment Integration
### Oxapay Integration
#### Lib.Oxapay.post()
Initializes Oxapay client.
\*\*Syntax:\*\*
```python
Lib.Oxapay.post(merchant\_api\_key)
```
\*\*Parameters:\*\*
\* `merchant\_api\_key` (Required): Your Oxapay merchant API key
\*\*Returns:\*\* Oxapay client object
\*\*Example:\*\*
```python
# Initialize Oxapay
client = Lib.Oxapay.post("YOUR\_MERCHANT\_API\_KEY")
# Create invoice
invoice = client.createInvoice({
"amount": 50,
"currency": "USD",
"description": "Service payment"
})
Api.sendMessage(f"Payment link: {invoice['url']}")
```
\*\*\*
This comprehensive guide covers advanced features in TeleBot Studio. By mastering these techniques, you can build enterprise-grade bots with complex workflows, external integrations, and sophisticated data management capabilities.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/advanced-features.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.