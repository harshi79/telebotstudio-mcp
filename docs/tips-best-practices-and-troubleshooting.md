> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/tips-best-practices-and-troubleshooting.md).
# Tips, Best Practices, and Troubleshooting
This section provides essential guidance for optimizing bot performance, managing workflows effectively, ensuring security, and troubleshooting common issues in TeleBot Studio. By following these practices, you can create highly reliable, efficient, and secure bots.
\*\*\*
## Tips for Optimizing Your Bot
### Efficient Command Structure
\*\*1. Combine Actions into Single Commands\*\*
Reduce redundant commands by combining related actions:
```python
# Instead of separate messages
Api.sendMessage("Welcome!")
Api.sendMessage("Use /help for instructions.")
# Combine into one
Api.sendMessage("Welcome! Use /help for instructions.")
```
\*\*2. Use Command Chaining Wisely\*\*
Structure multi-step workflows efficiently with `Bot.waitForInput()`:
```python
Api.sendMessage("Let's start registration. What's your name?")
Bot.waitForInput("collect\_name")
```
\*\*3. Schedule Tasks Appropriately\*\*
Use `Bot.scheduleCommand()` for delayed or periodic tasks:
```python
# Send reminder after 1 hour
Bot.scheduleCommand(3600, "send\_reminder")
# Quick follow-up (0.5 seconds)
Bot.scheduleCommand(0.5, "send\_confirmation")
```
\*\*Scheduling Best Practices:\*\*
\* Minimum delay: 0.1 seconds
\* Maximum delay: 31,536,000 seconds (1 year)
\* For ultra-fast commands (under 0.4 seconds): Maximum 5 executions within 5 seconds
\* Maximum scheduled commands per user: 100
\*\*4. Minimize Repeated API Calls\*\*
Cache data that doesn't change frequently:
```python
# Cache bot info
bot\_info = Bot.fetchData("cached\_bot\_info")
if not bot\_info:
bot\_info = Bot.getInfo()
Bot.storeData("cached\_bot\_info", bot\_info)
Api.sendMessage(f"Bot: {bot\_info['username']}")
```
### Enhancing Performance
\*\*1. Handle Large User Bases\*\*
Use efficient workflows for broadcasts and bulk operations:
```python
# Use broadcast for mass messaging
Bot.sendBroadcast(
function="sendMessage",
text="Important announcement for all users!"
)
```
\*\*2. Optimize User Interactions\*\*
Guide users through workflows smoothly:
```python
# Good: Clear, guided workflow
Api.sendMessage("Step 1: Enter your email")
Bot.waitForInput("validate\_email")
# In validate\_email command
email = msg
if "@" in email:
User.storeData("email", email)
Api.sendMessage("Step 2: Choose a password")
Bot.waitForInput("validate\_password")
else:
Api.sendMessage("Invalid email. Try again:")
Bot.waitForInput("validate\_email")
```
\*\*3. Efficient Error Handling\*\*
Log and analyze errors for better debugging:
```python
try:
Api.sendMessage("Attempting critical operation...")
# Your operation here
except ValueError as ve:
error\_id = Bot.errorID()
Bot.storeData(f"error\_{error\_id}", {
"type": "ValueError",
"message": str(ve),
"user": u,
"time": time.time()
})
Api.sendMessage(f"Validation error. Error ID: {error\_id}")
except Exception as e:
error\_id = Bot.errorID()
Bot.storeData(f"error\_{error\_id}", str(e))
Api.sendMessage(f"Error occurred. ID: {error\_id}")
```
### Code Execution Limits
\*\*Important Constraints:\*\*
1. \*\*Execution Timeout\*\*: 160 seconds maximum per command
2. \*\*Sleep Function\*\*: `time.sleep()` limited to 10 seconds maximum
3. \*\*Rate Limiting\*\*: Commands under 0.4 seconds are limited to 5 executions per 5 seconds
4. \*\*No Import Statements\*\*: Do not use `import` - all libraries are pre-loaded
\*\*Example of Using Sleep:\*\*
```python
Api.sendMessage("Processing your request...")
time.sleep(3) # Wait 3 seconds
Api.sendMessage("Processing complete!")
```
### Improving Security
\*\*1. Secure Sensitive Data\*\*
Hash or encrypt sensitive information before storing:
```python
# Hash passwords before storing
hashed\_password = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password\_hash", hashed\_password)
```
\*\*2. Validate User Input\*\*
Always validate and sanitize user input:
```python
# Validate numeric input
if not msg.isdigit():
Api.sendMessage("Please enter a valid number")
Bot.waitForInput("get\_number")
else:
amount = int(msg)
if amount < 1 or amount > 1000:
Api.sendMessage("Amount must be between 1 and 1000")
Bot.waitForInput("get\_number")
else:
# Process valid amount
User.storeData("amount", amount)
```
\*\*3. Secure Webhook Generation\*\*
Use user-specific webhooks for sensitive operations:
```python
# Generate secure user-specific webhook
webhook\_url = Lib.Webhook.getUrlFor("process\_payment", user\_id=u)
User.storeData("payment\_webhook", webhook\_url)
Api.sendMessage(f"Your secure payment webhook:\n{webhook\_url}")
```
\*\*4. Restrict Admin Commands\*\*
Implement admin-only command checks:
```python
ADMIN\_USER\_ID = 123456789
if u != ADMIN\_USER\_ID:
Api.sendMessage("⛔ Unauthorized. Admin access required.")
else:
# Admin-only operations
Api.sendMessage("Admin panel accessed")
```
\*\*5. Data Minimization\*\*
Store only necessary data:
```python
# Store only essential user info
User.storeData("name", name)
User.storeData("email", email)
# Don't store: full addresses, SSN, etc. unless absolutely necessary
```
\*\*\*
## Best Practices
### Developing Reliable Workflows
\*\*1. Use Multi-Step Commands\*\*
Break complex processes into manageable steps:
```python
# Step 1
Api.sendMessage("Let's create your profile!")
Api.sendMessage("What's your name?")
Bot.waitForInput("get\_name")
# Step 2 (get\_name command)
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email?")
Bot.waitForInput("get\_email")
# Step 3 (get\_email command)
email = msg
User.storeData("email", email)
Api.sendMessage("Profile created successfully!")
```
\*\*2. Validate All Inputs\*\*
Never trust user input without validation:
```python
# Email validation
if "@" not in email or "." not in email:
Api.sendMessage("Invalid email format")
Bot.waitForInput("get\_email")
else:
User.storeData("email", email)
# Numeric validation
if not value.isdigit() or int(value) < 0:
Api.sendMessage("Please enter a positive number")
Bot.waitForInput("get\_value")
```
\*\*3. Provide Clear Feedback\*\*
Always inform users about what's happening:
```python
Api.sendMessage("⏳ Processing your request...")
# Perform operation
Api.sendMessage("✅ Request completed successfully!")
# For errors
Api.sendMessage("❌ Operation failed. Please try again.")
```
### Optimizing Bot Features
\*\*1. Leverage Built-In Libraries\*\*
Use available libraries for common tasks:
```python
# CSV for data management
csv\_handler = Lib.CSV.Table("users.csv")
csv\_handler.create(["user\_id", "name", "points"])
# DateTime for timestamps
current\_time = Lib.DateTime.utcnow()
User.storeData("last\_active", current\_time)
# Random for unique IDs
unique\_id = Lib.Random.string(16)
User.storeData("session\_id", unique\_id)
```
\*\*2. Use Resource Management\*\*
Track numeric values efficiently with resources:
```python
# User points
points = User.res("points")
points.add(50)
Api.sendMessage(f"You earned 50 points! Total: {points.value()}")
# Global counters
total\_messages = Bot.res("total\_messages")
total\_messages.add(1)
```
\*\*3. Test Workflows Thoroughly\*\*
Test each step before deployment:
```python
# Add debug logging during development
Api.sendMessage(f"DEBUG: Current step = {User.fetchData('current\_step')}")
Api.sendMessage(f"DEBUG: User data = {User.fetchData('user\_data')}")
```
### Broadcast Best Practices
\*\*1. Target Your Audience\*\*
Use broadcasts efficiently:
```python
# Broadcast to all users
Bot.sendBroadcast(
function="sendMessage",
text="📢 Important announcement!"
)
# Command-based broadcast for personalization
Bot.sendBroadcast(command="send\_personalized\_message")
```
\*\*2. Monitor Broadcast Limits\*\*
Remember broadcast constraints:
\* Maximum 2 simultaneous broadcasts per bot
\* Maximum 1000 simultaneous broadcasts globally
\*\*3. Handle Broadcast Status\*\*
Monitor and manage broadcasts:
```python
# List active broadcasts
broadcasts = Bot.listBroadcasts()
Api.sendMessage(f"Active broadcasts: {len(broadcasts)}")
# Check specific broadcast
status = Bot.broadcastStatus(broadcast\_id="broadcast\_123")
Api.sendMessage(f"Status: {status['status']}")
# Pause if needed
if status['status'] == 'running':
Bot.pauseBroadcast(broadcast\_id="broadcast\_123")
```
\*\*\*
## Troubleshooting Common Issues
### Command Errors
\*\*Issue:\*\* Bot doesn't respond to a command
\*\*Common Causes:\*\*
\* Command name misspelled or case mismatch
\* Command not created in dashboard
\* Bot not running
\*\*Solutions:\*\*
```python
# Ensure command names are exact
# Wrong: /Start (capital S)
# Correct: /start (lowercase)
# Check bot status
status = Bot.getStatus()
Api.sendMessage(f"Bot status: {status}")
# Verify command exists in dashboard
```
\*\*Issue:\*\* Command executes but throws errors
\*\*Solutions:\*\*
```python
# Add comprehensive error handling
try:
# Your command logic
result = some\_operation()
Api.sendMessage(f"Success: {result}")
except KeyError as ke:
Api.sendMessage(f"Missing data: {ke}")
except ValueError as ve:
Api.sendMessage(f"Invalid value: {ve}")
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"Error {error\_id}: {str(e)}")
```
### Data Storage Issues
\*\*Issue:\*\* Data not persisting or retrieving incorrectly
\*\*Solutions:\*\*
```python
# Always check if data exists before using
user\_name = User.fetchData("name")
if user\_name:
Api.sendMessage(f"Welcome back, {user\_name}!")
else:
Api.sendMessage("Please register first: /register")
# Store data correctly
User.storeData("preferences", {
"language": "en",
"notifications": True
})
# Verify storage
stored\_prefs = User.fetchData("preferences")
Api.sendMessage(f"Stored preferences: {stored\_prefs}")
```
### Broadcast Failures
\*\*Issue:\*\* Broadcast doesn't execute
\*\*Common Causes:\*\*
\* Too many running broadcasts (limit: 2 per bot)
\* Invalid function parameter
\* Syntax errors in broadcast code
\*\*Solutions:\*\*
```python
# Check active broadcasts first
broadcasts = Bot.listBroadcasts()
if len(broadcasts) >= 2:
Api.sendMessage("Maximum broadcasts running. Please wait.")
else:
# Start new broadcast
Bot.sendBroadcast(
function="sendMessage",
text="Broadcast message"
)
# Use valid functions only
# Valid: sendMessage, sendPhoto, sendDocument, etc.
# Invalid: custom function names
```
### Webhook Issues
\*\*Issue:\*\* Webhook doesn't trigger command
\*\*Common Causes:\*\*
\* Incorrect webhook URL
\* Command doesn't exist
\* Network/connectivity issues
\*\*Solutions:\*\*
```python
# Verify webhook URL generation
webhook\_url = Lib.Webhook.getUrlFor("process\_data", user\_id=u)
Api.sendMessage(f"Generated webhook:\n{webhook\_url}")
# Ensure target command exists
# Command name in webhook must match exactly
# Test webhook manually
# Copy URL and trigger it from external service
```
### Resource Management Issues
\*\*Issue:\*\* Resource values not updating correctly
\*\*Solutions:\*\*
```python
# Always check current value first
points = User.res("points")
current = points.value() or 0 # Handle None case
Api.sendMessage(f"Current points: {current}")
# Use correct methods
points.add(10) # Add
points.cut(5) # Subtract
points.set(100) # Set to specific value
points.reset() # Reset to 0
# Verify after operation
Api.sendMessage(f"Updated points: {points.value()}")
```
### API Integration Errors
\*\*Issue:\*\* External API calls failing
\*\*Solutions:\*\*
```python
try:
response = Request.get("https://api.example.com/data", timeout=10)
if response.status\_code == 200:
data = response.json()
Api.sendMessage(f"Data: {data}")
else:
Api.sendMessage(f"API returned status {response.status\_code}")
except ConnectionError:
Api.sendMessage("Network connection failed. Retrying in 5 seconds...")
Bot.scheduleCommand(5, "retry\_api\_call")
except Exception as e:
Api.sendMessage(f"API error: {str(e)}")
```
### Scheduling Issues
\*\*Issue:\*\* Scheduled commands not executing
\*\*Common Causes:\*\*
\* Delay outside valid range (0.1 to 31,536,000 seconds)
\* Command name incorrect
\* User/chat ID invalid
\*\*Solutions:\*\*
```python
# Validate delay
delay = 3600 # 1 hour
if 0.1 <= delay <= 31536000:
Bot.scheduleCommand(delay, "reminder")
else:
Api.sendMessage("Invalid delay time")
# Verify command name
Bot.scheduleCommand(60, "send\_followup") # Ensure "send\_followup" command exists
# Check scheduled tasks (if available)
# Monitor command execution in dashboard
```
\*\*\*
## Advanced Tips
### Monitor Bot Performance
Get comprehensive bot metrics:
```python
# Get bot information
bot\_info = Bot.getInfo()
Api.sendMessage(f"📊 Bot Metrics:")
Api.sendMessage(f"Username: @{bot\_info['username']}")
Api.sendMessage(f"Status: {bot\_info['status']}")
Api.sendMessage(f"Total Users: {bot\_info['userstat']}")
```
### Multi-Bot Communication
Enable bot-to-bot communication:
```python
# Bot A triggers Bot B
bot\_b\_webhook = Lib.Webhook.getUrlFor(
"process\_task",
bot\_id="bot\_b\_id",
api\_key="bot\_b\_api\_key",
user\_id=u
)
# Send data to Bot B
response = Request.post(bot\_b\_webhook, json={
"task": "notification",
"data": "Important update"
})
```
### Efficient Data Export
Export data for analysis:
```python
# Export bot data
all\_data = Bot.exportAllData()
Api.sendDocument(all\_data)
# Export user list
users\_file = Bot.exportBotUsersFile()
Api.sendDocument(users\_file)
# Export specific data
data\_file = Bot.exportData("user\_stats")
Api.sendDocument(data\_file)
```
### Implement Rate Limiting
Protect against spam:
```python
# Check last command time
last\_command = User.fetchData("last\_command\_time")
current\_time = time.time()
if last\_command and (current\_time - last\_command) < 3:
Api.sendMessage("⏳ Please wait 3 seconds between commands")
else:
User.storeData("last\_command\_time", current\_time)
# Execute command
```
### Create Admin Panel
Build administrative interfaces:
```python
ADMIN\_ID = 123456789
if u == ADMIN\_ID:
Api.sendMessage("🔧 Admin Panel")
Api.sendMessage("/stats - View statistics")
Api.sendMessage("/broadcast - Send broadcast")
Api.sendMessage("/users - List users")
Api.sendMessage("/logs - View error logs")
else:
Api.sendMessage("⛔ Admin access required")
```
\*\*\*
## Real-World Optimization Scenarios
### Scenario 1: High-Traffic Bot
For bots with thousands of users:
```python
# Use efficient caching
cached\_stats = Bot.fetchData("cached\_stats")
cache\_time = Bot.fetchData("cache\_timestamp") or 0
if time.time() - cache\_time > 300: # 5 minute cache
# Recalculate stats
total\_users = Bot.res("total\_users").value()
active\_users = Bot.res("active\_users").value()
stats = {
"total": total\_users,
"active": active\_users
}
Bot.storeData("cached\_stats", stats)
Bot.storeData("cache\_timestamp", time.time())
else:
stats = cached\_stats
Api.sendMessage(f"Total: {stats['total']}, Active: {stats['active']}")
```
### Scenario 2: Complex Workflow Management
For multi-step registration or surveys:
```python
# Track workflow progress
current\_step = User.fetchData("registration\_step") or "start"
if current\_step == "start":
Api.sendMessage("Welcome! Let's register you.")
Api.sendMessage("Enter your name:")
User.storeData("registration\_step", "name")
Bot.waitForInput("registration\_flow")
elif current\_step == "name":
User.storeData("name", msg)
Api.sendMessage("Enter your email:")
User.storeData("registration\_step", "email")
Bot.waitForInput("registration\_flow")
elif current\_step == "email":
User.storeData("email", msg)
Api.sendMessage("Registration complete!")
User.removeData("registration\_step")
```
### Scenario 3: Payment Processing
Handle payments securely:
```python
# Store payment session securely
payment\_id = Bot.uniqueID()
User.storeData(f"payment\_{payment\_id}", {
"amount": 10.00,
"status": "pending",
"timestamp": time.time()
})
# Generate secure payment webhook
webhook = Lib.Webhook.getUrlFor("process\_payment", user\_id=u)
# Create payment with Oxapay
client = Lib.Oxapay.post("YOUR\_API\_KEY")
invoice = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Premium subscription"
})
Api.sendMessage(f"Complete payment: {invoice['url']}")
```
\*\*\*
## Debugging Checklist
When troubleshooting issues, check:
\* [ ] Command names are correct and case-sensitive
\* [ ] Bot is running (check dashboard)
\* [ ] All required data is stored correctly
\* [ ] Input validation is in place
\* [ ] Error handling covers all cases
\* [ ] Scheduled tasks have valid delays
\* [ ] Webhook URLs are generated correctly
\* [ ] API keys and credentials are valid
\* [ ] Rate limits are not exceeded
\* [ ] Data types match expected formats
\*\*\*
By following these tips, best practices, and troubleshooting guidelines, you can build robust, efficient, and secure bots on TeleBot Studio. Remember to test thoroughly, handle errors gracefully, and optimize for your specific use case.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/tips-best-practices-and-troubleshooting.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.