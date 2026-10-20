# Tips, Best Practices, and Troubleshooting
This section provides essential guidance for optimizing bot performance, managing workflows effectively, ensuring security, and troubleshooting common issues in TeleBot Studio. By following these practices, you can create highly reliable, efficient, and secure bots.
***
## Tips for Optimizing Your Bot
### Efficient Command Structure
**1. Combine Actions into Single Commands**
Reduce redundant commands by combining related actions:
```python
# Instead of separate messages
Api.sendMessage("Welcome!")
Api.sendMessage("Use /help for instructions.")
# Combine into one
Api.sendMessage("Welcome! Use /help for instructions.")
```
**2. Use Command Chaining Wisely**
Structure multi-step workflows efficiently with `Bot.waitForInput()`:
```python
Api.sendMessage("Let's start registration. What's your name?")
Bot.waitForInput("collect_name")
```
**3. Schedule Tasks Appropriately**
Use `Bot.scheduleCommand()` for delayed or periodic tasks:
```python
# Send reminder after 1 hour
Bot.scheduleCommand(3600, "send_reminder")
# Quick follow-up (0.5 seconds)
Bot.scheduleCommand(0.5, "send_confirmation")
```
**Scheduling Best Practices:**
* Minimum delay: 0.1 seconds
* Maximum delay: 31,536,000 seconds (1 year)
* For ultra-fast commands (under 0.4 seconds): Maximum 5 executions within 5 seconds
* Maximum scheduled commands per user: 100
**4. Minimize Repeated API Calls**
Cache data that doesn't change frequently:
```python
# Cache bot info
bot_info = Bot.fetchData("cached_bot_info")
if not bot_info:
bot_info = Bot.getInfo()
Bot.storeData("cached_bot_info", bot_info)
Api.sendMessage(f"Bot: {bot_info['username']}")
```
### Enhancing Performance
**1. Handle Large User Bases**
Use efficient workflows for broadcasts and bulk operations:
```python
# Use broadcast for mass messaging
Bot.sendBroadcast(
function="sendMessage",
text="Important announcement for all users!"
)
```
**2. Optimize User Interactions**
Guide users through workflows smoothly:
```python
# Good: Clear, guided workflow
Api.sendMessage("Step 1: Enter your email")
Bot.waitForInput("validate_email")
# In validate_email command
email = msg
if "@" in email:
User.storeData("email", email)
Api.sendMessage("Step 2: Choose a password")
Bot.waitForInput("validate_password")
else:
Api.sendMessage("Invalid email. Try again:")
Bot.waitForInput("validate_email")
```
**3. Efficient Error Handling**
Log and analyze errors for better debugging:
```python
try:
Api.sendMessage("Attempting critical operation...")
# Your operation here
except ValueError as ve:
error_id = Bot.errorID()
Bot.storeData(f"error_{error_id}", {
"type": "ValueError",
"message": str(ve),
"user": u,
"time": time.time()
})
Api.sendMessage(f"Validation error. Error ID: {error_id}")
except Exception as e:
error_id = Bot.errorID()
Bot.storeData(f"error_{error_id}", str(e))
Api.sendMessage(f"Error occurred. ID: {error_id}")
```
### Code Execution Limits
**Important Constraints:**
1. **Execution Timeout**: 160 seconds maximum per command
2. **Sleep Function**: `time.sleep()` limited to 10 seconds maximum
3. **Rate Limiting**: Commands under 0.4 seconds are limited to 5 executions per 5 seconds
4. **No Import Statements**: Do not use `import` - all libraries are pre-loaded
**Example of Using Sleep:**
```python
Api.sendMessage("Processing your request...")
time.sleep(3) # Wait 3 seconds
Api.sendMessage("Processing complete!")
```
### Improving Security
**1. Secure Sensitive Data**
Hash or encrypt sensitive information before storing:
```python
# Hash passwords before storing
hashed_password = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password_hash", hashed_password)
```
**2. Validate User Input**
Always validate and sanitize user input:
```python
# Validate numeric input
if not msg.isdigit():
Api.sendMessage("Please enter a valid number")
Bot.waitForInput("get_number")
else:
amount = int(msg)
if amount < 1 or amount > 1000:
Api.sendMessage("Amount must be between 1 and 1000")
Bot.waitForInput("get_number")
else:
# Process valid amount
User.storeData("amount", amount)
```
**3. Secure Webhook Generation**
Use user-specific webhooks for sensitive operations:
```python
# Generate secure user-specific webhook
webhook_url = Lib.Webhook.getUrlFor("process_payment", user_id=u)
User.storeData("payment_webhook", webhook_url)
Api.sendMessage(f"Your secure payment webhook:\n{webhook_url}")
```
**4. Restrict Admin Commands**
Implement admin-only command checks:
```python
ADMIN_USER_ID = 123456789
if u != ADMIN_USER_ID:
Api.sendMessage("⛔ Unauthorized. Admin access required.")
else:
# Admin-only operations
Api.sendMessage("Admin panel accessed")
```
**5. Data Minimization**
Store only necessary data:
```python
# Store only essential user info
User.storeData("name", name)
User.storeData("email", email)
# Don't store: full addresses, SSN, etc. unless absolutely necessary
```
***
## Best Practices
### Developing Reliable Workflows
**1. Use Multi-Step Commands**
Break complex processes into manageable steps:
```python
# Step 1
Api.sendMessage("Let's create your profile!")
Api.sendMessage("What's your name?")
Bot.waitForInput("get_name")
# Step 2 (get_name command)
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email?")
Bot.waitForInput("get_email")
# Step 3 (get_email command)
email = msg
User.storeData("email", email)
Api.sendMessage("Profile created successfully!")
```
**2. Validate All Inputs**
Never trust user input without validation:
```python
# Email validation
if "@" not in email or "." not in email:
Api.sendMessage("Invalid email format")
Bot.waitForInput("get_email")
else:
User.storeData("email", email)
# Numeric validation
if not value.isdigit() or int(value) < 0:
Api.sendMessage("Please enter a positive number")
Bot.waitForInput("get_value")
```
**3. Provide Clear Feedback**
Always inform users about what's happening:
```python
Api.sendMessage("⏳ Processing your request...")
# Perform operation
Api.sendMessage("✅ Request completed successfully!")
# For errors
Api.sendMessage("❌ Operation failed. Please try again.")
```
### Optimizing Bot Features
**1. Leverage Built-In Libraries**
Use available libraries for common tasks:
```python
# CSV for data management
csv_handler = Lib.CSV.Table("users.csv")
csv_handler.create(["user_id", "name", "points"])
# DateTime for timestamps
current_time = Lib.DateTime.utcnow()
User.storeData("last_active", current_time)
# Random for unique IDs
unique_id = Lib.Random.string(16)
User.storeData("session_id", unique_id)
```
**2. Use Resource Management**
Track numeric values efficiently with resources:
```python
# User points
points = User.res("points")
points.add(50)
Api.sendMessage(f"You earned 50 points! Total: {points.value()}")
# Global counters
total_messages = Bot.res("total_messages")
total_messages.add(1)
```
**3. Test Workflows Thoroughly**
Test each step before deployment:
```python
# Add debug logging during development
Api.sendMessage(f"DEBUG: Current step = {User.fetchData('current_step')}")
Api.sendMessage(f"DEBUG: User data = {User.fetchData('user_data')}")
```
### Broadcast Best Practices
**1. Target Your Audience**
Use broadcasts efficiently:
```python
# Broadcast to all users
Bot.sendBroadcast(
function="sendMessage",
text="📢 Important announcement!"
)
# Command-based broadcast for personalization
Bot.sendBroadcast(command="send_personalized_message")
```
**2. Monitor Broadcast Limits**
Remember broadcast constraints:
* Maximum 2 simultaneous broadcasts per bot
* Maximum 1000 simultaneous broadcasts globally
**3. Handle Broadcast Status**
Monitor and manage broadcasts:
```python
# List active broadcasts
broadcasts = Bot.listBroadcasts()
Api.sendMessage(f"Active broadcasts: {len(broadcasts)}")
# Check specific broadcast
status = Bot.broadcastStatus(broadcast_id="broadcast_123")
Api.sendMessage(f"Status: {status['status']}")
# Pause if needed
if status['status'] == 'running':
Bot.pauseBroadcast(broadcast_id="broadcast_123")
```
***
## Troubleshooting Common Issues
### Command Errors
**Issue:** Bot doesn't respond to a command
**Common Causes:**
* Command name misspelled or case mismatch
* Command not created in dashboard
* Bot not running
**Solutions:**
```python
# Ensure command names are exact
# Wrong: /Start (capital S)
# Correct: /start (lowercase)
# Check bot status
status = Bot.getStatus()
Api.sendMessage(f"Bot status: {status}")
# Verify command exists in dashboard
```
**Issue:** Command executes but throws errors
**Solutions:**
```python
# Add comprehensive error handling
try:
# Your command logic
result = some_operation()
Api.sendMessage(f"Success: {result}")
except KeyError as ke:
Api.sendMessage(f"Missing data: {ke}")
except ValueError as ve:
Api.sendMessage(f"Invalid value: {ve}")
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"Error {error_id}: {str(e)}")
```
### Data Storage Issues
**Issue:** Data not persisting or retrieving incorrectly
**Solutions:**
```python
# Always check if data exists before using
user_name = User.fetchData("name")
if user_name:
Api.sendMessage(f"Welcome back, {user_name}!")
else:
Api.sendMessage("Please register first: /register")
# Store data correctly
User.storeData("preferences", {
"language": "en",
"notifications": True
})
# Verify storage
stored_prefs = User.fetchData("preferences")
Api.sendMessage(f"Stored preferences: {stored_prefs}")
```
### Broadcast Failures
**Issue:** Broadcast doesn't execute
**Common Causes:**
* Too many running broadcasts (limit: 2 per bot)
* Invalid function parameter
* Syntax errors in broadcast code
**Solutions:**
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
**Issue:** Webhook doesn't trigger command
**Common Causes:**
* Incorrect webhook URL
* Command doesn't exist
* Network/connectivity issues
**Solutions:**
```python
# Verify webhook URL generation
webhook_url = Lib.Webhook.getUrlFor("process_data", user_id=u)
Api.sendMessage(f"Generated webhook:\n{webhook_url}")
# Ensure target command exists
# Command name in webhook must match exactly
# Test webhook manually
# Copy URL and trigger it from external service
```
### Resource Management Issues
**Issue:** Resource values not updating correctly
**Solutions:**
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
**Issue:** External API calls failing
**Solutions:**
```python
try:
response = Request.get("https://api.example.com/data", timeout=10)
if response.status_code == 200:
data = response.json()
Api.sendMessage(f"Data: {data}")
else:
Api.sendMessage(f"API returned status {response.status_code}")
except ConnectionError:
Api.sendMessage("Network connection failed. Retrying in 5 seconds...")
Bot.scheduleCommand(5, "retry_api_call")
except Exception as e:
Api.sendMessage(f"API error: {str(e)}")
```
### Scheduling Issues
**Issue:** Scheduled commands not executing
**Common Causes:**
* Delay outside valid range (0.1 to 31,536,000 seconds)
* Command name incorrect
* User/chat ID invalid
**Solutions:**
```python
# Validate delay
delay = 3600 # 1 hour
if 0.1 <= delay <= 31536000:
Bot.scheduleCommand(delay, "reminder")
else:
Api.sendMessage("Invalid delay time")
# Verify command name
Bot.scheduleCommand(60, "send_followup") # Ensure "send_followup" command exists
# Check scheduled tasks (if available)
# Monitor command execution in dashboard
```
***
## Advanced Tips
### Monitor Bot Performance
Get comprehensive bot metrics:
```python
# Get bot information
bot_info = Bot.getInfo()
Api.sendMessage(f"📊 Bot Metrics:")
Api.sendMessage(f"Username: @{bot_info['username']}")
Api.sendMessage(f"Status: {bot_info['status']}")
Api.sendMessage(f"Total Users: {bot_info['userstat']}")
```
### Multi-Bot Communication
Enable bot-to-bot communication:
```python
# Bot A triggers Bot B
bot_b_webhook = Lib.Webhook.getUrlFor(
"process_task",
bot_id="bot_b_id",
api_key="bot_b_api_key",
user_id=u
)
# Send data to Bot B
response = Request.post(bot_b_webhook, json={
"task": "notification",
"data": "Important update"
})
```
### Efficient Data Export
Export data for analysis:
```python
# Export bot data
all_data = Bot.exportAllData()
Api.sendDocument(all_data)
# Export user list
users_file = Bot.exportBotUsersFile()
Api.sendDocument(users_file)
# Export specific data
data_file = Bot.exportData("user_stats")
Api.sendDocument(data_file)
```
### Implement Rate Limiting
Protect against spam:
```python
# Check last command time
last_command = User.fetchData("last_command_time")
current_time = time.time()
if last_command and (current_time - last_command) < 3:
Api.sendMessage("⏳ Please wait 3 seconds between commands")
else:
User.storeData("last_command_time", current_time)
# Execute command
```
### Create Admin Panel
Build administrative interfaces:
```python
ADMIN_ID = 123456789
if u == ADMIN_ID:
Api.sendMessage("🔧 Admin Panel")
Api.sendMessage("/stats - View statistics")
Api.sendMessage("/broadcast - Send broadcast")
Api.sendMessage("/users - List users")
Api.sendMessage("/logs - View error logs")
else:
Api.sendMessage("⛔ Admin access required")
```
***
## Real-World Optimization Scenarios
### Scenario 1: High-Traffic Bot
For bots with thousands of users:
```python
# Use efficient caching
cached_stats = Bot.fetchData("cached_stats")
cache_time = Bot.fetchData("cache_timestamp") or 0
if time.time() - cache_time > 300: # 5 minute cache
# Recalculate stats
total_users = Bot.res("total_users").value()
active_users = Bot.res("active_users").value()
stats = {
"total": total_users,
"active": active_users
}
Bot.storeData("cached_stats", stats)
Bot.storeData("cache_timestamp", time.time())
else:
stats = cached_stats
Api.sendMessage(f"Total: {stats['total']}, Active: {stats['active']}")
```
### Scenario 2: Complex Workflow Management
For multi-step registration or surveys:
```python
# Track workflow progress
current_step = User.fetchData("registration_step") or "start"
if current_step == "start":
Api.sendMessage("Welcome! Let's register you.")
Api.sendMessage("Enter your name:")
User.storeData("registration_step", "name")
Bot.waitForInput("registration_flow")
elif current_step == "name":
User.storeData("name", msg)
Api.sendMessage("Enter your email:")
User.storeData("registration_step", "email")
Bot.waitForInput("registration_flow")
elif current_step == "email":
User.storeData("email", msg)
Api.sendMessage("Registration complete!")
User.removeData("registration_step")
```
### Scenario 3: Payment Processing
Handle payments securely:
```python
# Store payment session securely
payment_id = Bot.uniqueID()
User.storeData(f"payment_{payment_id}", {
"amount": 10.00,
"status": "pending",
"timestamp": time.time()
})
# Generate secure payment webhook
webhook = Lib.Webhook.getUrlFor("process_payment", user_id=u)
# Create payment with Oxapay
client = Lib.Oxapay.post("YOUR_API_KEY")
invoice = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Premium subscription"
})
Api.sendMessage(f"Complete payment: {invoice['url']}")
```
***
## Debugging Checklist
When troubleshooting issues, check:
* [ ] Command names are correct and case-sensitive
* [ ] Bot is running (check dashboard)
* [ ] All required data is stored correctly
* [ ] Input validation is in place
* [ ] Error handling covers all cases
* [ ] Scheduled tasks have valid delays
* [ ] Webhook URLs are generated correctly
* [ ] API keys and credentials are valid
* [ ] Rate limits are not exceeded
* [ ] Data types match expected formats
***
By following these tips, best practices, and troubleshooting guidelines, you can build robust, efficient, and secure bots on TeleBot Studio. Remember to test thoroughly, handle errors gracefully, and optimize for your specific use case.
