# Bot Features and Functionalities
This section explores the comprehensive features and functionalities available in TeleBot Studio, demonstrating how to apply them effectively in real-world scenarios. From handling user interactions to automating complex tasks and managing broadcasts, these features empower you to build sophisticated and versatile Telegram bots using TeleBot Syntax (TBS).
***
## Wildcard Master Command (`*`)
The `*` command serves as a **fallback handler** that triggers when a bot receives a message not matching any predefined command. This powerful feature is essential for creating intelligent default responses and handling unexpected user inputs gracefully.
**Common Use Cases:**
* Providing helpful default responses
* Guiding users back to available commands
* Logging unrecognized inputs for analysis
* Creating conversational fallback flows
**Example:**
```python
Api.sendMessage("I didn't quite catch that. Try /help to see available commands.")
```
**Advanced Example with Contextual Help:**
```python
unknown_input = msg
Api.sendMessage(f"'{unknown_input}' isn't a recognized command.")
Api.sendMessage("Here are some things you can do:")
Api.sendMessage("• /start - Begin your journey")
Api.sendMessage("• /help - Get assistance")
Api.sendMessage("• /settings - Configure your preferences")
```
***
## At Handler Command (`@`)
The `@` command executes **before any other command**, making it perfect for preprocessing, validation, logging, and setting up global conditions. This is your bot's entry point for every user interaction.
**Key Use Cases:**
* Message validation and sanitization
* User activity logging and analytics
* Authentication checks
* Rate limiting enforcement
* Context setup for downstream commands
**Example - Activity Logging:**
```python
# Log user activity
user_activity = User.res("activity")
count = user_activity.value() if user_activity.value() else 0
user_activity.set(count + 1)
Api.sendMessage("Processing your request...")
# Execution continues to the matched command
```
**Example - Rate Limiting:**
```python
last_request = User.fetchData("last_request_time")
current_time = time.time()
if last_request and (current_time - last_request) < 2:
Api.sendMessage("Please wait a moment before sending another request.")
else:
User.storeData("last_request_time", current_time)
# Continue to next command
```
***
## Broadcasting Messages
The broadcasting system allows you to communicate with multiple users simultaneously, enabling announcements, notifications, and targeted messaging campaigns.
**Core Functions:**
* **`Bot.sendBroadcast`**: Send messages or execute commands for groups of users
* **`Bot.cancelBroadcast`**: Stop an ongoing broadcast
* **`Bot.listBroadcasts`**: View all broadcast campaigns
* **`Bot.broadcastStatus`**: Check the status of a specific broadcast
* **`Bot.pauseBroadcast`**: Temporarily pause a broadcast
**Basic Broadcast with Code:**
```python
Bot.sendBroadcast(code="Api.sendMessage('🎉 Exciting news! New features launched!')")
```
**Command-Based Broadcast:**
```python
# Execute a command for all users
Bot.sendBroadcast(command="send_weekly_update")
```
**Function-Based Broadcast:**
```python
Bot.sendBroadcast(function="sendMessage", text="Hello everyone!")
```
**Managing Broadcast Status:**
```python
# List all broadcasts
broadcasts = Bot.listBroadcasts()
Api.sendMessage(f"Active broadcasts: {len(broadcasts)}")
# Check specific broadcast status
status = Bot.broadcastStatus(broadcast_id="broadcast_123")
Api.sendMessage(f"Status: {status['status']}")
# Pause if needed
if status['status'] == 'running':
Bot.pauseBroadcast(broadcast_id="broadcast_123")
```
***
## CAPTCHA Generation and Verification
Enhance your bot's security with built-in CAPTCHA support, perfect for preventing spam and validating human users.
**Key Functions:**
* **`Bot.createCaptcha`**: Generate a CAPTCHA challenge
* **`Bot.verifyCaptcha`**: Validate user responses
* **`Bot.sendCaptcha`**: Send CAPTCHA to users
**Automatic CAPTCHA Flow:**
```python
# Generate CAPTCHA
captcha_data = Bot.createCaptcha()
captcha_id = captcha_data['captcha_id']
# Send to user
Bot.sendCaptcha(captcha_id, caption="Please solve this CAPTCHA to continue")
# Wait for user response
Bot.waitForInput("verify_captcha")
User.storeData("pending_captcha_id", captcha_id)
```
**Verification Command:**
```python
# In verify_captcha command
user_answer = msg
captcha_id = User.fetchData("pending_captcha_id")
is_valid = Bot.verifyCaptcha(captcha_id, user_answer)
if is_valid:
Api.sendMessage("✅ Verification successful!")
User.removeData("pending_captcha_id")
# Continue with protected action
else:
Api.sendMessage("❌ Incorrect CAPTCHA. Please try again.")
Bot.waitForInput("verify_captcha")
```
***
## Error Handling and Debugging
TeleBot Studio provides comprehensive error handling tools to help you build reliable, production-ready bots.
**Built-in Features:**
* **Error Dashboard**: Access detailed logs in your bot's management panel
* **Exception Handling**: Use Python-style try-except blocks
* **Error IDs**: Generate unique identifiers for error tracking
**Basic Error Handling:**
```python
try:
Api.sendMessage("Executing critical operation...")
# Your code here
except ValueError as ve:
Api.sendMessage(f"Value error occurred: {str(ve)}")
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"An error occurred. Error ID: {error_id}")
Api.sendMessage(f"Details: {str(e)}")
```
**Advanced Error Management:**
```python
try:
# Risky operation
result = some_api_call()
except ConnectionError:
Api.sendMessage("Connection failed. Please try again later.")
Bot.scheduleCommand(300, "retry_operation") # Retry in 5 minutes
except Exception as e:
# Log error for debugging
error_info = {
"user": u,
"command": "operation_name",
"error": str(e),
"timestamp": time.time()
}
Bot.storeData("error_log", error_info)
# Notify admin
Api.sendMessage(f"Critical error: {e}", chat_id="ADMIN_ID")
```
***
## Persistent Data Storage
Manage bot-level and user-level data efficiently with TeleBot Studio's storage system.
**Bot-Level Storage:**
```python
# Store global bot data
Bot.storeData("total_users", 1000)
Bot.storeData("launch_date", "2025-01-01")
# Retrieve data
user_count = Bot.fetchData("total_users")
Api.sendMessage(f"Total users: {user_count}")
# Remove data
Bot.removeData("old_config")
```
**User-Level Storage:**
```python
# Save user preferences
User.storeData("language", "en")
User.storeData("notifications", True)
# Retrieve user data
language = User.fetchData("language")
Api.sendMessage(f"Your language is set to: {language}")
# Delete user data
User.removeData("temp_data")
```
**Data Export:**
```python
# Export specific bot data
data_file = Bot.exportData("user_stats")
Api.sendDocument(data_file)
# Export all bot data
all_data = Bot.exportAllData()
Api.sendDocument(all_data)
# Export user list
users_file = Bot.exportBotUsersFile()
Api.sendDocument(users_file)
```
***
## Resource Management System
Track and manage numeric resources like points, credits, or currency across users and globally.
**User Resources:**
```python
# Initialize user points
points = User.res("points")
# Add points
points.add(50)
Api.sendMessage(f"You earned 50 points! Total: {points.value()}")
# Deduct points
if points.value() >= 100:
points.cut(100)
Api.sendMessage("Purchase successful! 100 points deducted.")
else:
Api.sendMessage("Insufficient points.")
# Reset points
points.reset()
```
**Global Bot Resources:**
```python
# Track global statistics
total_messages = Bot.res("total_messages")
total_messages.add(1)
# Display leaderboard
leaderboard_data = User.res("points").exportAllData(limit=10)
Api.sendMessage("🏆 Top 10 Users:")
```
**Another User's Resources:**
```python
# Check another user's resources
target_user_id = 12345
target_points = User.resOf("points", target_user_id)
Api.sendMessage(f"User {target_user_id} has {target_points.value()} points")
```
***
## Command Chaining with Input Handling
Create multi-step workflows by chaining commands and waiting for user input.
**Basic Command Chain:**
```python
# Step 1: Start registration
Api.sendMessage("Welcome! Let's get you registered.")
Api.sendMessage("What's your name?")
Bot.waitForInput("collect_name")
```
**Collect Name Command:**
```python
# Step 2: Process name and ask for email
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email address?")
Bot.waitForInput("collect_email")
```
**Collect Email Command:**
```python
# Step 3: Finalize registration
email = msg
User.storeData("email", email)
# Validate email format
if "@" in email and "." in email:
Api.sendMessage("✅ Registration complete!")
Api.sendMessage(f"Name: {User.fetchData('name')}")
Api.sendMessage(f"Email: {email}")
else:
Api.sendMessage("Invalid email. Please try again.")
Bot.waitForInput("collect_email")
```
***
## Scheduled Commands
Schedule commands to execute after a delay or at specific times.
**Delayed Execution:**
```python
# Send a reminder after 30 seconds
Api.sendMessage("I'll remind you in 30 seconds.")
Bot.scheduleCommand(30, "send_reminder")
```
**Reminder Command:**
```python
Api.sendMessage("⏰ This is your reminder!")
```
**Multiple Scheduled Tasks:**
```python
Api.sendMessage("Setting up your daily tasks...")
# Schedule multiple commands
Bot.scheduleCommand(3600, "hourly_update") # 1 hour
Bot.scheduleCommand(86400, "daily_digest") # 24 hours
Bot.scheduleCommand(604800, "weekly_report") # 7 days
Api.sendMessage("All tasks scheduled successfully!")
```
**Quick Follow-up:**
```python
Api.sendMessage("Processing your request...")
Bot.scheduleCommand(0.2, "send_confirmation") # 0.2 seconds later
```
***
## Membership Verification
Verify if users are members of specific groups or channels before granting access.
**Basic Membership Check:**
```python
is_member = CheckMembership(u, "@your_channel")
if is_member:
Api.sendMessage("✅ Access granted! You're a member.")
# Proceed with protected content
else:
Api.sendMessage("❌ Please join our channel first:")
Api.sendMessage("https://t.me/your_channel")
```
**Multiple Channel Verification:**
```python
required_channels = ["@channel1", "@channel2", "@channel3"]
all_joined = True
for channel in required_channels:
if not CheckMembership(u, channel):
all_joined = False
Api.sendMessage(f"Please join: {channel}")
if all_joined:
Api.sendMessage("✅ All requirements met! Welcome!")
else:
Api.sendMessage("Join all channels to continue.")
```
***
## Webhook Integration
Create webhooks to enable external systems to trigger bot actions.
**Generate Webhook URL:**
```python
webhook_url = Lib.Webhook.getUrlFor("process_payment", user_id=u)
Api.sendMessage(f"Your webhook URL:\n{webhook_url}")
```
**Cross-Bot Communication:**
```python
# Trigger command in another bot
other_bot_webhook = Lib.Webhook.getUrlFor(
"notify_user",
bot_id="another_bot_id",
api_key="another_bot_api_key",
user_id=u
)
Api.sendMessage("Notification webhook created for Bot B.")
```
**Payment Webhook Example:**
```python
# In process_payment command
payment_data = options
Api.sendMessage("Payment received!")
Api.sendMessage(f"Amount: ${payment_data.get('amount')}")
# Award points
points = User.res("points")
points.add(int(payment_data.get('amount')) * 10)
```
***
## Bot Information and Control
Access comprehensive information about your bot and control its status.
**Get Bot Information:**
```python
bot_info = Bot.getInfo()
Api.sendMessage(f"Bot Name: {bot_info['first_name']}")
Api.sendMessage(f"Username: @{bot_info['username']}")
Api.sendMessage(f"Status: {bot_info['status']}")
```
**Bot Control:**
```python
# Start bot
start_result = Bot.start()
Api.sendMessage("Bot started successfully!")
# Stop bot
stop_result = Bot.stop()
Api.sendMessage("Bot stopped.")
# Check status
status = Bot.getStatus()
Api.sendMessage(f"Current status: {status}")
```
**Get Webhook and Payment URLs:**
```python
webhook = Bot.webhookURL()
Api.sendMessage(f"Webhook URL:\n{webhook}")
payment_url = Bot.paymentURL(amount=10.00, currency="USD")
Api.sendMessage(f"Payment URL:\n{payment_url}")
```
***
## Multi-Step Workflows
Combine features to create complex, interactive workflows.
**Complete Registration System:**
```python
# /register command
Api.sendMessage("📝 Let's set up your account!")
Api.sendMessage("First, what's your full name?")
Bot.waitForInput("reg_name")
```
**Step 2 - Name Collection:**
```python
# reg_name command
name = msg
if len(name) < 2:
Api.sendMessage("Name too short. Please enter your full name.")
Bot.waitForInput("reg_name")
else:
User.storeData("reg_name", name)
Api.sendMessage(f"Great, {name}! Now, what's your email?")
Bot.waitForInput("reg_email")
```
**Step 3 - Email Collection:**
```python
# reg_email command
email = msg
if "@" not in email or "." not in email:
Api.sendMessage("Invalid email format. Try again:")
Bot.waitForInput("reg_email")
else:
User.storeData("reg_email", email)
Api.sendMessage("Finally, set a password (min 8 characters):")
Bot.waitForInput("reg_password")
```
**Step 4 - Finalization:**
```python
# reg_password command
password = msg
if len(password) < 8:
Api.sendMessage("Password too short. Minimum 8 characters:")
Bot.waitForInput("reg_password")
else:
# Store securely (hash in production)
User.storeData("reg_password", hashlib.sha256(password.encode()).hexdigest())
# Complete registration
User.storeData("registered", True)
points = User.res("points")
points.set(100) # Welcome bonus
Api.sendMessage("✅ Registration complete!")
Api.sendMessage(f"Welcome, {User.fetchData('reg_name')}!")
Api.sendMessage("You've earned 100 welcome points!")
```
***
## Referral System Implementation
Build a complete referral tracking system with rewards.
**Generate Referral Link:**
```python
# /start command
referrer = params # Get referral ID from start parameter
if referrer and referrer != str(u):
# New user referred by someone
existing_user = User.fetchData("referred_by")
if not existing_user: # First time being referred
User.storeData("referred_by", referrer)
# Reward referrer
referrer_points = User.resOf("points", int(referrer))
referrer_points.add(50)
# Notify referrer
Api.sendMessage(
f"🎉 Someone joined using your link! +50 points",
chat_id=int(referrer)
)
Api.sendMessage("Welcome! You were referred by a friend. Enjoy your stay!")
# Show user their referral link
bot_username = Bot.getInfo()['username']
Api.sendMessage("📢 Invite friends and earn rewards!")
Api.sendMessage(f"Your referral link:\nt.me/{bot_username}?start={u}")
```
**View Referral Stats:**
```python
# /referrals command
referred_count = Bot.res(f"referral_count_{u}").value() or 0
total_earned = referred_count * 50
Api.sendMessage("📊 Your Referral Stats:")
Api.sendMessage(f"• Total referrals: {referred_count}")
Api.sendMessage(f"• Points earned: {total_earned}")
Api.sendMessage(f"• Current balance: {User.res('points').value()}")
```
***
## Dynamic Content Generation
Use resources and data to create personalized user experiences.
**Personalized Dashboard:**
```python
# /dashboard command
name = User.fetchData("name") or "User"
points = User.res("points").value() or 0
level = "Bronze" if points < 100 else "Silver" if points < 500 else "Gold"
last_active = User.fetchData("last_active") or "Never"
Api.sendMessage(f"👤 Dashboard for {name}")
Api.sendMessage(f"💰 Points: {points}")
Api.sendMessage(f"🏅 Level: {level}")
Api.sendMessage(f"🕒 Last active: {last_active}")
# Update last active
User.storeData("last_active", Lib.DateTime.utcnow())
```
***
## Bot Transfer Functionality
Transfer bot ownership between TeleBot Studio accounts.
**Transfer Bot:**
```python
result = Bot.transfer(
email="newowner@example.com",
bot_id=bot_id,
bot_token="YOUR_BOT_TOKEN",
run_now=True
)
if result['ok']:
Api.sendMessage(f"Bot transferred successfully!")
else:
Api.sendMessage(f"Transfer failed: {result['error']}")
```
***
## Unique ID Generation
Generate unique identifiers for various purposes.
**Random ID:**
```python
session_id = Bot.randomID()
User.storeData("session_id", session_id)
Api.sendMessage(f"Your session ID: {session_id}")
```
**Unique ID:**
```python
transaction_id = Bot.uniqueID()
Api.sendMessage(f"Transaction ID: {transaction_id}")
```
**Error Tracking:**
```python
try:
# Some operation
risky_operation()
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"Error {error_id}: {str(e)}")
```
***
## Running Commands Directly
Execute commands immediately within your code.
**Run Command:**
```python
Api.sendMessage("Redirecting you to the help menu...")
Bot.run("help")
```
**Run with Parameters:**
```python
Bot.run("process_data", params="user_report")
```
***
This comprehensive guide covers the core features and functionalities available in TeleBot Studio. By combining these building blocks, you can create sophisticated bots that handle complex workflows, manage user data efficiently, and provide engaging interactive experiences.
