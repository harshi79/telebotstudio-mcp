> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/faq.md).
# Frequently Asked Questions (FAQ)
This section addresses common questions and concerns about using TeleBot Studio. Whether you're a beginner or an experienced developer, these FAQs provide quick answers to help you use the platform effectively.
\*\*\*
## General Questions
### 1. What is TeleBot Studio and how does it work?
TeleBot Studio is a comprehensive platform for building and hosting Telegram bots. It uses TeleBot Syntax (TBS), a Python-like language specifically designed for bot development, allowing you to create commands, integrate libraries, and host bots without managing your own servers.
### 2. How do I create my first bot?
To create your first bot:
1. Get a Bot API token from @BotFather on Telegram
2. Sign up at \*\*TeleBotStudio.com\*\* with email and password (no captcha or email verification required)
3. Click \*\*"Add New Bot"\*\* on the dashboard
4. Paste your Bot API token
5. Start adding commands and customizing your bot
### 3. Is TeleBot Studio free?
Yes! TeleBot Studio is completely free with no limitations. There are no point systems, usage limits, or premium tiers. You can create and run as many bots as you need without restrictions.
### 4. Do I need programming experience?
Basic programming knowledge is helpful but not required. TeleBot Syntax (TBS) is designed to be simple and intuitive, with comprehensive documentation and examples to help you get started.
### 5. Can I migrate my existing bot to TeleBot Studio?
Yes! Simply take your existing bot token from @BotFather and add it to TeleBot Studio. You can then recreate your bot's commands using TBS or use our documentation to convert your existing code.
### 6. What's the difference between TeleBot Studio and other bot platforms?
TeleBot Studio offers:
\* Completely free hosting with no limits
\* Python-like syntax that's easy to learn
\* Built-in libraries for blockchain, AI, payments, and more
\* No server management required
\* Advanced features like multi-bot communication and resource management
\*\*\*
## Commands and Features
### 1. How do I create a command?
Commands are added via the "Commands" menu in your bot dashboard:
1. Open the \*\*Commands\*\* menu
2. Click \*\*"Add Command"\*\*
3. Define the command name (e.g., `/start`)
4. Write your logic in TBS:
```python
Api.sendMessage("Welcome to my bot!")
```
### 2. What's the difference between `Bot.waitForInput()` and `Bot.run()`?
\* \*\*`Bot.waitForInput()`\*\*: Waits for the user's next message and routes it to a specific command
```python
Api.sendMessage("What's your name?")
Bot.waitForInput("save\_name")
```
\* \*\*`Bot.run()`\*\*: Executes another command immediately
```python
Api.sendMessage("Redirecting to help...")
Bot.run("help")
```
### 3. How do I handle user input in multiple steps?
Use command chaining with `Bot.waitForInput()`:
```python
# Step 1
Api.sendMessage("Enter your email:")
Bot.waitForInput("get\_email")
# Step 2 (in get\_email command)
email = msg
User.storeData("email", email)
Api.sendMessage("Enter your password:")
Bot.waitForInput("get\_password")
```
### 4. What is the wildcard command (`\*`)?
The `\*` command catches any message that doesn't match other commands:
```python
Api.sendMessage("I didn't understand that. Type /help for available commands.")
```
### 5. What is the at handler command (`@`)?
The `@` command runs before any other command, perfect for logging or preprocessing:
```python
# Log all user activity
Bot.res("total\_messages").add(1)
# Execution continues to matched command
```
### 6. How do I schedule commands to run later?
Use `Bot.scheduleCommand()`:
```python
# Run command after 60 seconds
Bot.scheduleCommand(60, "send\_reminder")
# Quick follow-up (0.5 seconds)
Bot.scheduleCommand(0.5, "send\_confirmation")
```
\*\*Limits:\*\*
\* Minimum: 0.1 seconds
\* Maximum: 31,536,000 seconds (1 year)
\* Max 100 scheduled commands per user
\*\*\*
## Data Storage
### 1. How do I save user data?
Use `User.storeData()` and `User.fetchData()`:
```python
# Save data
User.storeData("name", "John")
User.storeData("email", "john@example.com")
# Retrieve data
name = User.fetchData("name")
Api.sendMessage(f"Hello, {name}!")
# Delete data
User.removeData("temp\_data")
```
### 2. How do I save bot-level data?
Use `Bot.storeData()` and `Bot.fetchData()`:
```python
# Save global bot data
Bot.storeData("total\_users", 1000)
# Retrieve data
total = Bot.fetchData("total\_users")
Api.sendMessage(f"Total users: {total}")
```
### 3. What's the difference between User, Bot, and Account data?
\* \*\*User data\*\*: Specific to each user (e.g., preferences, progress)
\* \*\*Bot data\*\*: Global to the bot (e.g., statistics, configuration)
\* \*\*Account data\*\*: Shared across all your bots (e.g., API keys, templates)
### 4. How much data can I store?
Each data entry can be up to 10MB. There's no limit on the number of entries.
### 5. How do I export data?
```python
# Export user data
user\_data = User.exportData("preferences")
Api.sendDocument(user\_data)
# Export all bot data
all\_data = Bot.exportAllData()
Api.sendDocument(all\_data)
# Export user list
users = Bot.exportBotUsersFile()
Api.sendDocument(users)
```
\*\*\*
## Libraries and Integrations
### 1. What libraries are available?
TeleBot Studio includes:
\* \*\*Lib.EVM\*\*: Ethereum and EVM-compatible blockchain operations
\* \*\*Lib.TON\*\*: TON blockchain integration
\* \*\*Lib.AI\*\*: OpenAI and Google Gemini AI integration
\* \*\*Lib.DateTime\*\*: Date and time utilities
\* \*\*Lib.Random\*\*: Random number and string generation
\* \*\*Lib.CSV\*\*: CSV file management
\* \*\*Lib.Webhook\*\*: Webhook generation and management
\* \*\*Lib.Oxapay\*\*: Payment processing
\* \*\*Lib.Crypto\*\*: Cryptocurrency utilities
\* \*\*Request\*\*: HTTP client for API calls
### 2. How do I make HTTP requests?
Use the `Request` module:
```python
# GET request
response = Request.get("https://api.example.com/data")
if response.ok:
data = response.json()
Api.sendMessage(f"Result: {data}")
# POST request
response = Request.post(
"https://api.example.com/submit",
json={"name": "John", "email": "john@example.com"}
)
```
### 3. How do I integrate AI capabilities?
Use `Lib.AI`:
```python
# OpenAI
client = Lib.AI.client(provider="openai", apiKey="YOUR\_KEY")
response = client.chat(
model="gpt-4",
messages=[{"role": "user", "content": msg}]
)
Api.sendMessage(response['choices'][0]['message']['content'])
# Google Gemini
client = Lib.AI.client(provider="gemini", apiKey="YOUR\_KEY")
response = client.chat(
model="gemini-2.0-flash",
messages=[{"role": "user", "content": msg}]
)
Api.sendMessage(response['choices'][0]['message']['content'])
```
### 4. Can I use blockchain features?
Yes! TeleBot Studio supports:
\*\*TON Blockchain:\*\*
```python
# Create wallet
wallet = Lib.TON.createWallet()
Api.sendMessage(f"Address: {wallet['address']}")
# Send TON
Lib.TON.send(to\_address="EQD...", amount=0.5)
```
\*\*EVM Blockchains (Ethereum, BSC, Polygon, etc.):\*\*
```python
# Store private key
Lib.EVM.storeKey("your\_private\_key")
# Send ETH
tx = Lib.EVM.sendCoin(network="ethereum", to="0x...", value=0.1)
Api.sendMessage(f"Transaction: {tx}")
```
### 5. How do I handle payments?
Use `Lib.Oxapay`:
```python
client = Lib.Oxapay.post("YOUR\_MERCHANT\_API\_KEY")
invoice = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Premium subscription"
})
Api.sendMessage(f"Pay here: {invoice['url']}")
```
\*\*\*
## Broadcasting
### 1. How do I send messages to all users?
Use `Bot.sendBroadcast()`:
```python
# Simple broadcast
Bot.sendBroadcast(
function="sendMessage",
text="Important announcement!"
)
# Command-based broadcast
Bot.sendBroadcast(command="send\_personalized\_message")
# Code-based broadcast
Bot.sendBroadcast(code="Api.sendMessage('Hello everyone!')")
```
### 2. What are the broadcast limits?
\* Maximum 2 simultaneous broadcasts per bot
\* Maximum 1000 simultaneous broadcasts globally
### 3. How do I check broadcast status?
```python
# List all broadcasts
broadcasts = Bot.listBroadcasts()
Api.sendMessage(f"Active: {len(broadcasts)}")
# Check specific broadcast
status = Bot.broadcastStatus(broadcast\_id="123")
Api.sendMessage(f"Status: {status['status']}")
# Pause broadcast
Bot.pauseBroadcast(broadcast\_id="123")
# Cancel broadcast
Bot.cancelBroadcast(broadcast\_id="123")
```
### 4. Can I target specific users for broadcasts?
Broadcasts go to all bot users. For targeted messaging, use loops:
```python
target\_users = [12345, 67890, 54321]
for user\_id in target\_users:
Api.sendMessage("Special offer for you!", chat\_id=user\_id)
```
\*\*\*
## Webhooks
### 1. What is a webhook?
A webhook is a URL that allows external systems to trigger bot commands in real-time.
### 2. How do I create a webhook?
```python
webhook\_url = Lib.Webhook.getUrlFor("process\_payment", user\_id=u)
Api.sendMessage(f"Your webhook:\n{webhook\_url}")
```
### 3. How do I handle webhook data?
In your command, use the `options` variable:
```python
# process\_payment command
payment\_data = options
amount = payment\_data.get('amount')
status = payment\_data.get('status')
if status == 'completed':
Api.sendMessage(f"Payment of ${amount} received!")
```
### 4. Can webhooks trigger commands in other bots?
Yes! Use bot\\_id and api\\_key parameters:
```python
webhook = Lib.Webhook.getUrlFor(
"notify\_user",
bot\_id="other\_bot\_id",
api\_key="other\_bot\_api\_key",
user\_id=u
)
```
\*\*\*
## Resources
### 1. What are resources?
Resources are numeric values you can track per user or globally (like points, credits, currency):
```python
# User resources
points = User.res("points")
points.add(50)
points.cut(10)
points.set(100)
points.reset()
current = points.value()
# Bot resources (global)
total = Bot.res("total\_sales")
total.add(1)
```
### 2. How do I create a leaderboard?
```python
# Get top users by points
top\_users = User.res("points").exportAllData(limit=10)
Api.sendMessage("🏆 Leaderboard:")
for idx, user in enumerate(top\_users, 1):
Api.sendMessage(f"{idx}. User {user['user\_id']}: {user['value']} points")
```
### 3. Can I access another user's resources?
Yes, use `User.resOf()`:
```python
target\_user = 12345
target\_points = User.resOf("points", target\_user)
Api.sendMessage(f"User {target\_user} has {target\_points.value()} points")
```
\*\*\*
## Security and Privacy
### 1. How do I secure sensitive data?
Hash passwords and encrypt sensitive information:
```python
# Hash password
hashed = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password\_hash", hashed)
# Verify later
stored\_hash = User.fetchData("password\_hash")
input\_hash = hashlib.sha256(input\_password.encode()).hexdigest()
if stored\_hash == input\_hash:
Api.sendMessage("Login successful!")
```
### 2. How do I restrict admin commands?
```python
ADMIN\_USER\_ID = 123456789
if u == ADMIN\_USER\_ID:
# Admin operations
Api.sendMessage("Admin panel accessed")
else:
Api.sendMessage("⛔ Unauthorized")
```
### 3. Are user conversations private?
Yes. Each user's data is isolated and only accessible within your bot's context. Other bots cannot access your bot's data.
### 4. How do I validate user input?
Always validate before processing:
```python
# Validate email
if "@" not in email or "." not in email:
Api.sendMessage("Invalid email format")
Bot.waitForInput("get\_email")
# Validate number
if not amount.isdigit() or int(amount) < 1:
Api.sendMessage("Please enter a valid positive number")
Bot.waitForInput("get\_amount")
```
\*\*\*
## Bot Management
### 1. How do I start/stop my bot?
Use the dashboard controls or:
```python
# Start bot
Bot.start()
# Stop bot
Bot.stop()
# Check status
status = Bot.getStatus()
Api.sendMessage(f"Status: {status}")
```
### 2. How do I get bot information?
```python
info = Bot.getInfo()
Api.sendMessage(f"Bot: @{info['username']}")
Api.sendMessage(f"Status: {info['status']}")
Api.sendMessage(f"Users: {info['userstat']}")
```
### 3. Can I transfer my bot to another account?
Yes, `Bot.transfer()` creates a copy of your bot in another TeleBot Studio account:
```python
result = Bot.transfer(
email="recipient@example.com",
bot\_id=bot\_id,
bot\_token="YOUR\_BOT\_TOKEN",
run\_now=True
)
```
\*\*Note:\*\* This creates a copy - your original bot remains in your account.
### 4. Can I have multiple bots?
Yes! You can create and manage unlimited bots in your account.
### 5. How do I delete a bot?
Use the dashboard to delete bots. You can also use the Account class methods in code.
\*\*\*
## Troubleshooting
### 1. Why isn't my bot responding?
Check:
\* Bot is running (check dashboard status)
\* Command name is correct (case-sensitive)
\* Bot token is valid
\* Command exists in your bot
### 2. My scheduled command isn't running. Why?
Verify:
\* Delay is within valid range (0.1 to 31,536,000 seconds)
\* Command name is spelled correctly
\* You haven't exceeded 100 scheduled commands per user
### 3. Why is my broadcast failing?
Common causes:
\* Already running 2 broadcasts (bot limit)
\* Invalid function parameter
\* 1000 global broadcast limit reached
### 4. How do I debug errors?
Use try-except blocks and error logging:
```python
try:
# Your code
operation()
except Exception as e:
error\_id = Bot.errorID()
Bot.storeData(f"error\_{error\_id}", str(e))
Api.sendMessage(f"Error {error\_id}: {str(e)}")
```
Check error logs in your dashboard under the Errors menu.
### 5. My webhook isn't triggering. What should I do?
\* Verify the webhook URL is correct
\* Ensure the target command exists
\* Check that external service is sending requests properly
\* Test with a manual HTTP request
\*\*\*
## Advanced Features
### 1. How do I create multi-bot workflows?
Use webhooks for bot-to-bot communication:
```python
# Bot A triggers Bot B
webhook = Lib.Webhook.getUrlFor(
"process\_task",
bot\_id="bot\_b\_id",
api\_key="bot\_b\_api\_key"
)
Request.post(webhook, json={"task": "notification"})
```
### 2. Can I use external APIs?
Yes, use the Request module:
```python
response = Request.get("https://api.example.com/data")
if response.ok:
data = response.json()
# Process data
```
### 3. How do I implement rate limiting?
```python
last\_command = User.fetchData("last\_command\_time")
current\_time = time.time()
if last\_command and (current\_time - last\_command) < 3:
Api.sendMessage("Please wait 3 seconds between commands")
else:
User.storeData("last\_command\_time", current\_time)
# Process command
```
### 4. Can I create CAPTCHA verification?
Yes, use built-in CAPTCHA functions:
```python
# Create CAPTCHA
captcha = Bot.createCaptcha()
Bot.sendCaptcha(captcha['captcha\_id'])
Bot.waitForInput("verify\_captcha")
# Verify in next command
is\_valid = Bot.verifyCaptcha(captcha\_id, user\_answer)
if is\_valid:
Api.sendMessage("✅ Verified!")
```
### 5. How do I check user membership in channels?
```python
is\_member = CheckMembership(u, "@your\_channel")
if is\_member:
Api.sendMessage("Access granted!")
else:
Api.sendMessage("Please join @your\_channel first")
```
\*\*\*
## Platform Limits
### 1. Are there any execution limits?
\* Maximum execution time: 160 seconds per command
\* `time.sleep()` maximum: 10 seconds
\* Rate limit for fast commands (<0.4s): 5 executions per 5 seconds
### 2. Are there storage limits?
\* Each data entry: 10MB maximum
\* No limit on number of entries
### 3. Are there broadcast limits?
\* 2 simultaneous broadcasts per bot
\* 1000 simultaneous broadcasts globally
### 4. Can I use import statements?
No. TBS doesn't allow import statements. All libraries are pre-loaded and available through the `Lib` namespace.
\*\*\*
## Getting Help
### 1. Where can I find documentation?
Complete documentation is available at Help.TeleBotStudio.com including:
\* Getting Started guides
\* Language reference
\* Library documentation
\* Real-world examples
\* Best practices
### 2. How do I get support?
\* Check this FAQ first
\* Review documentation
\* Join our community forums
\* Contact support through the platform
### 3. Can I suggest new features?
Yes! We welcome feature suggestions. Submit them through:
\* Platform feedback form
\* Community discussions
\* Support channels
### 4. Is there a community?
Yes! Join other TeleBot Studio developers to:
\* Share bots and templates
\* Get help and advice
\* Showcase your projects
\* Stay updated on new features
\*\*\*
## Next Steps
Ready to build? Here's what to do:
1. \*\*Sign up\*\* at TeleBotStudio.com
2. \*\*Create your first bot\*\* with @BotFather
3. \*\*Add it\*\* to TeleBot Studio
4. \*\*Explore\*\* the documentation
5. \*\*Build\*\* something amazing!
Need inspiration? Check out our Real-World Use Cases documentation for complete bot examples including referral systems, payment bots, surveys, e-commerce, and more.
Happy building! 🚀
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/faq.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.