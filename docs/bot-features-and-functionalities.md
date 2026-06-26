> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/bot-features-and-functionalities.md).
# Bot Features and Functionalities
This section explores the comprehensive features and functionalities available in TeleBot Studio, demonstrating how to apply them effectively in real-world scenarios. From handling user interactions to automating complex tasks and managing broadcasts, these features empower you to build sophisticated and versatile Telegram bots using TeleBot Syntax (TBS).
\*\*\*
## Wildcard Master Command (`\*`)
The `\*` command serves as a \*\*fallback handler\*\* that triggers when a bot receives a message not matching any predefined command. This powerful feature is essential for creating intelligent default responses and handling unexpected user inputs gracefully.
\*\*Common Use Cases:\*\*
\* Providing helpful default responses
\* Guiding users back to available commands
\* Logging unrecognized inputs for analysis
\* Creating conversational fallback flows
\*\*Example:\*\*
```python
Api.sendMessage("I didn't quite catch that. Try /help to see available commands.")
```
\*\*Advanced Example with Contextual Help:\*\*
```python
unknown\_input = msg
Api.sendMessage(f"'{unknown\_input}' isn't a recognized command.")
Api.sendMessage("Here are some things you can do:")
Api.sendMessage("• /start - Begin your journey")
Api.sendMessage("• /help - Get assistance")
Api.sendMessage("• /settings - Configure your preferences")
```
\*\*\*
## At Handler Command (`@`)
The `@` command executes \*\*before any other command\*\*, making it perfect for preprocessing, validation, logging, and setting up global conditions. This is your bot's entry point for every user interaction.
\*\*Key Use Cases:\*\*
\* Message validation and sanitization
\* User activity logging and analytics
\* Authentication checks
\* Rate limiting enforcement
\* Context setup for downstream commands
\*\*Example - Activity Logging:\*\*
```python
# Log user activity
user\_activity = User.res("activity")
count = user\_activity.value() if user\_activity.value() else 0
user\_activity.set(count + 1)
Api.sendMessage("Processing your request...")
# Execution continues to the matched command
```
\*\*Example - Rate Limiting:\*\*
```python
last\_request = User.fetchData("last\_request\_time")
current\_time = time.time()
if last\_request and (current\_time - last\_request) < 2:
Api.sendMessage("Please wait a moment before sending another request.")
else:
User.storeData("last\_request\_time", current\_time)
# Continue to next command
```
\*\*\*
## Broadcasting Messages
The broadcasting system allows you to communicate with multiple users simultaneously, enabling announcements, notifications, and targeted messaging campaigns.
\*\*Core Functions:\*\*
\* \*\*`Bot.sendBroadcast`\*\*: Send messages or execute commands for groups of users
\* \*\*`Bot.cancelBroadcast`\*\*: Stop an ongoing broadcast
\* \*\*`Bot.listBroadcasts`\*\*: View all broadcast campaigns
\* \*\*`Bot.broadcastStatus`\*\*: Check the status of a specific broadcast
\* \*\*`Bot.pauseBroadcast`\*\*: Temporarily pause a broadcast
\*\*Basic Broadcast with Code:\*\*
```python
Bot.sendBroadcast(code="Api.sendMessage('🎉 Exciting news! New features launched!')")
```
\*\*Command-Based Broadcast:\*\*
```python
# Execute a command for all users
Bot.sendBroadcast(command="send\_weekly\_update")
```
\*\*Function-Based Broadcast:\*\*
```python
Bot.sendBroadcast(function="sendMessage", text="Hello everyone!")
```
\*\*Managing Broadcast Status:\*\*
```python
# List all broadcasts
broadcasts = Bot.listBroadcasts()
Api.sendMessage(f"Active broadcasts: {len(broadcasts)}")
# Check specific broadcast status
status = Bot.broadcastStatus(broadcast\_id="broadcast\_123")
Api.sendMessage(f"Status: {status['status']}")
# Pause if needed
if status['status'] == 'running':
Bot.pauseBroadcast(broadcast\_id="broadcast\_123")
```
\*\*\*
## CAPTCHA Generation and Verification
Enhance your bot's security with built-in CAPTCHA support, perfect for preventing spam and validating human users.
\*\*Key Functions:\*\*
\* \*\*`Bot.createCaptcha`\*\*: Generate a CAPTCHA challenge
\* \*\*`Bot.verifyCaptcha`\*\*: Validate user responses
\* \*\*`Bot.sendCaptcha`\*\*: Send CAPTCHA to users
\*\*Automatic CAPTCHA Flow:\*\*
```python
# Generate CAPTCHA
captcha\_data = Bot.createCaptcha()
captcha\_id = captcha\_data['captcha\_id']
# Send to user
Bot.sendCaptcha(captcha\_id, caption="Please solve this CAPTCHA to continue")
# Wait for user response
Bot.waitForInput("verify\_captcha")
User.storeData("pending\_captcha\_id", captcha\_id)
```
\*\*Verification Command:\*\*
```python
# In verify\_captcha command
user\_answer = msg
captcha\_id = User.fetchData("pending\_captcha\_id")
is\_valid = Bot.verifyCaptcha(captcha\_id, user\_answer)
if is\_valid:
Api.sendMessage("✅ Verification successful!")
User.removeData("pending\_captcha\_id")
# Continue with protected action
else:
Api.sendMessage("❌ Incorrect CAPTCHA. Please try again.")
Bot.waitForInput("verify\_captcha")
```
\*\*\*
## Error Handling and Debugging
TeleBot Studio provides comprehensive error handling tools to help you build reliable, production-ready bots.
\*\*Built-in Features:\*\*
\* \*\*Error Dashboard\*\*: Access detailed logs in your bot's management panel
\* \*\*Exception Handling\*\*: Use Python-style try-except blocks
\* \*\*Error IDs\*\*: Generate unique identifiers for error tracking
\*\*Basic Error Handling:\*\*
```python
try:
Api.sendMessage("Executing critical operation...")
# Your code here
except ValueError as ve:
Api.sendMessage(f"Value error occurred: {str(ve)}")
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"An error occurred. Error ID: {error\_id}")
Api.sendMessage(f"Details: {str(e)}")
```
\*\*Advanced Error Management:\*\*
```python
try:
# Risky operation
result = some\_api\_call()
except ConnectionError:
Api.sendMessage("Connection failed. Please try again later.")
Bot.scheduleCommand(300, "retry\_operation") # Retry in 5 minutes
except Exception as e:
# Log error for debugging
error\_info = {
"user": u,
"command": "operation\_name",
"error": str(e),
"timestamp": time.time()
}
Bot.storeData("error\_log", error\_info)
# Notify admin
Api.sendMessage(f"Critical error: {e}", chat\_id="ADMIN\_ID")
```
\*\*\*
## Persistent Data Storage
Manage bot-level and user-level data efficiently with TeleBot Studio's storage system.
\*\*Bot-Level Storage:\*\*
```python
# Store global bot data
Bot.storeData("total\_users", 1000)
Bot.storeData("launch\_date", "2025-01-01")
# Retrieve data
user\_count = Bot.fetchData("total\_users")
Api.sendMessage(f"Total users: {user\_count}")
# Remove data
Bot.removeData("old\_config")
```
\*\*User-Level Storage:\*\*
```python
# Save user preferences
User.storeData("language", "en")
User.storeData("notifications", True)
# Retrieve user data
language = User.fetchData("language")
Api.sendMessage(f"Your language is set to: {language}")
# Delete user data
User.removeData("temp\_data")
```
\*\*Data Export:\*\*
```python
# Export specific bot data
data\_file = Bot.exportData("user\_stats")
Api.sendDocument(data\_file)
# Export all bot data
all\_data = Bot.exportAllData()
Api.sendDocument(all\_data)
# Export user list
users\_file = Bot.exportBotUsersFile()
Api.sendDocument(users\_file)
```
\*\*\*
## Resource Management System
Track and manage numeric resources like points, credits, or currency across users and globally.
\*\*User Resources:\*\*
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
\*\*Global Bot Resources:\*\*
```python
# Track global statistics
total\_messages = Bot.res("total\_messages")
total\_messages.add(1)
# Display leaderboard
leaderboard\_data = User.res("points").exportAllData(limit=10)
Api.sendMessage("🏆 Top 10 Users:")
```
\*\*Another User's Resources:\*\*
```python
# Check another user's resources
target\_user\_id = 12345
target\_points = User.resOf("points", target\_user\_id)
Api.sendMessage(f"User {target\_user\_id} has {target\_points.value()} points")
```
\*\*\*
## Command Chaining with Input Handling
Create multi-step workflows by chaining commands and waiting for user input.
\*\*Basic Command Chain:\*\*
```python
# Step 1: Start registration
Api.sendMessage("Welcome! Let's get you registered.")
Api.sendMessage("What's your name?")
Bot.waitForInput("collect\_name")
```
\*\*Collect Name Command:\*\*
```python
# Step 2: Process name and ask for email
name = msg
User.storeData("name", name)
Api.sendMessage(f"Nice to meet you, {name}!")
Api.sendMessage("What's your email address?")
Bot.waitForInput("collect\_email")
```
\*\*Collect Email Command:\*\*
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
Bot.waitForInput("collect\_email")
```
\*\*\*
## Scheduled Commands
Schedule commands to execute after a delay or at specific times.
\*\*Delayed Execution:\*\*
```python
# Send a reminder after 30 seconds
Api.sendMessage("I'll remind you in 30 seconds.")
Bot.scheduleCommand(30, "send\_reminder")
```
\*\*Reminder Command:\*\*
```python
Api.sendMessage("⏰ This is your reminder!")
```
\*\*Multiple Scheduled Tasks:\*\*
```python
Api.sendMessage("Setting up your daily tasks...")
# Schedule multiple commands
Bot.scheduleCommand(3600, "hourly\_update") # 1 hour
Bot.scheduleCommand(86400, "daily\_digest") # 24 hours
Bot.scheduleCommand(604800, "weekly\_report") # 7 days
Api.sendMessage("All tasks scheduled successfully!")
```
\*\*Quick Follow-up:\*\*
```python
Api.sendMessage("Processing your request...")
Bot.scheduleCommand(0.2, "send\_confirmation") # 0.2 seconds later
```
\*\*\*
## Membership Verification
Verify if users are members of specific groups or channels before granting access.
\*\*Basic Membership Check:\*\*
```python
is\_member = CheckMembership(u, "@your\_channel")
if is\_member:
Api.sendMessage("✅ Access granted! You're a member.")
# Proceed with protected content
else:
Api.sendMessage("❌ Please join our channel first:")
Api.sendMessage("https://t.me/your\_channel")
```
\*\*Multiple Channel Verification:\*\*
```python
required\_channels = ["@channel1", "@channel2", "@channel3"]
all\_joined = True
for channel in required\_channels:
if not CheckMembership(u, channel):
all\_joined = False
Api.sendMessage(f"Please join: {channel}")
if all\_joined:
Api.sendMessage("✅ All requirements met! Welcome!")
else:
Api.sendMessage("Join all channels to continue.")
```
\*\*\*
## Webhook Integration
Create webhooks to enable external systems to trigger bot actions.
\*\*Generate Webhook URL:\*\*
```python
webhook\_url = Lib.Webhook.getUrlFor("process\_payment", user\_id=u)
Api.sendMessage(f"Your webhook URL:\n{webhook\_url}")
```
\*\*Cross-Bot Communication:\*\*
```python
# Trigger command in another bot
other\_bot\_webhook = Lib.Webhook.getUrlFor(
"notify\_user",
bot\_id="another\_bot\_id",
api\_key="another\_bot\_api\_key",
user\_id=u
)
Api.sendMessage("Notification webhook created for Bot B.")
```
\*\*Payment Webhook Example:\*\*
```python
# In process\_payment command
payment\_data = options
Api.sendMessage("Payment received!")
Api.sendMessage(f"Amount: ${payment\_data.get('amount')}")
# Award points
points = User.res("points")
points.add(int(payment\_data.get('amount')) \* 10)
```
\*\*\*
## Bot Information and Control
Access comprehensive information about your bot and control its status.
\*\*Get Bot Information:\*\*
```python
bot\_info = Bot.getInfo()
Api.sendMessage(f"Bot Name: {bot\_info['first\_name']}")
Api.sendMessage(f"Username: @{bot\_info['username']}")
Api.sendMessage(f"Status: {bot\_info['status']}")
```
\*\*Bot Control:\*\*
```python
# Start bot
start\_result = Bot.start()
Api.sendMessage("Bot started successfully!")
# Stop bot
stop\_result = Bot.stop()
Api.sendMessage("Bot stopped.")
# Check status
status = Bot.getStatus()
Api.sendMessage(f"Current status: {status}")
```
\*\*Get Webhook and Payment URLs:\*\*
```python
webhook = Bot.webhookURL()
Api.sendMessage(f"Webhook URL:\n{webhook}")
payment\_url = Bot.paymentURL(amount=10.00, currency="USD")
Api.sendMessage(f"Payment URL:\n{payment\_url}")
```
\*\*\*
## Multi-Step Workflows
Combine features to create complex, interactive workflows.
\*\*Complete Registration System:\*\*
```python
# /register command
Api.sendMessage("📝 Let's set up your account!")
Api.sendMessage("First, what's your full name?")
Bot.waitForInput("reg\_name")
```
\*\*Step 2 - Name Collection:\*\*
```python
# reg\_name command
name = msg
if len(name) < 2:
Api.sendMessage("Name too short. Please enter your full name.")
Bot.waitForInput("reg\_name")
else:
User.storeData("reg\_name", name)
Api.sendMessage(f"Great, {name}! Now, what's your email?")
Bot.waitForInput("reg\_email")
```
\*\*Step 3 - Email Collection:\*\*
```python
# reg\_email command
email = msg
if "@" not in email or "." not in email:
Api.sendMessage("Invalid email format. Try again:")
Bot.waitForInput("reg\_email")
else:
User.storeData("reg\_email", email)
Api.sendMessage("Finally, set a password (min 8 characters):")
Bot.waitForInput("reg\_password")
```
\*\*Step 4 - Finalization:\*\*
```python
# reg\_password command
password = msg
if len(password) < 8:
Api.sendMessage("Password too short. Minimum 8 characters:")
Bot.waitForInput("reg\_password")
else:
# Store securely (hash in production)
User.storeData("reg\_password", hashlib.sha256(password.encode()).hexdigest())
# Complete registration
User.storeData("registered", True)
points = User.res("points")
points.set(100) # Welcome bonus
Api.sendMessage("✅ Registration complete!")
Api.sendMessage(f"Welcome, {User.fetchData('reg\_name')}!")
Api.sendMessage("You've earned 100 welcome points!")
```
\*\*\*
## Referral System Implementation
Build a complete referral tracking system with rewards.
\*\*Generate Referral Link:\*\*
```python
# /start command
referrer = params # Get referral ID from start parameter
if referrer and referrer != str(u):
# New user referred by someone
existing\_user = User.fetchData("referred\_by")
if not existing\_user: # First time being referred
User.storeData("referred\_by", referrer)
# Reward referrer
referrer\_points = User.resOf("points", int(referrer))
referrer\_points.add(50)
# Notify referrer
Api.sendMessage(
f"🎉 Someone joined using your link! +50 points",
chat\_id=int(referrer)
)
Api.sendMessage("Welcome! You were referred by a friend. Enjoy your stay!")
# Show user their referral link
bot\_username = Bot.getInfo()['username']
Api.sendMessage("📢 Invite friends and earn rewards!")
Api.sendMessage(f"Your referral link:\nt.me/{bot\_username}?start={u}")
```
\*\*View Referral Stats:\*\*
```python
# /referrals command
referred\_count = Bot.res(f"referral\_count\_{u}").value() or 0
total\_earned = referred\_count \* 50
Api.sendMessage("📊 Your Referral Stats:")
Api.sendMessage(f"• Total referrals: {referred\_count}")
Api.sendMessage(f"• Points earned: {total\_earned}")
Api.sendMessage(f"• Current balance: {User.res('points').value()}")
```
\*\*\*
## Dynamic Content Generation
Use resources and data to create personalized user experiences.
\*\*Personalized Dashboard:\*\*
```python
# /dashboard command
name = User.fetchData("name") or "User"
points = User.res("points").value() or 0
level = "Bronze" if points < 100 else "Silver" if points < 500 else "Gold"
last\_active = User.fetchData("last\_active") or "Never"
Api.sendMessage(f"👤 Dashboard for {name}")
Api.sendMessage(f"💰 Points: {points}")
Api.sendMessage(f"🏅 Level: {level}")
Api.sendMessage(f"🕒 Last active: {last\_active}")
# Update last active
User.storeData("last\_active", Lib.DateTime.utcnow())
```
\*\*\*
## Bot Transfer Functionality
Transfer bot ownership between TeleBot Studio accounts.
\*\*Transfer Bot:\*\*
```python
result = Bot.transfer(
email="newowner@example.com",
bot\_id=bot\_id,
bot\_token="YOUR\_BOT\_TOKEN",
run\_now=True
)
if result['ok']:
Api.sendMessage(f"Bot transferred successfully!")
else:
Api.sendMessage(f"Transfer failed: {result['error']}")
```
\*\*\*
## Unique ID Generation
Generate unique identifiers for various purposes.
\*\*Random ID:\*\*
```python
session\_id = Bot.randomID()
User.storeData("session\_id", session\_id)
Api.sendMessage(f"Your session ID: {session\_id}")
```
\*\*Unique ID:\*\*
```python
transaction\_id = Bot.uniqueID()
Api.sendMessage(f"Transaction ID: {transaction\_id}")
```
\*\*Error Tracking:\*\*
```python
try:
# Some operation
risky\_operation()
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"Error {error\_id}: {str(e)}")
```
\*\*\*
## Running Commands Directly
Execute commands immediately within your code.
\*\*Run Command:\*\*
```python
Api.sendMessage("Redirecting you to the help menu...")
Bot.run("help")
```
\*\*Run with Parameters:\*\*
```python
Bot.run("process\_data", params="user\_report")
```
\*\*\*
This comprehensive guide covers the core features and functionalities available in TeleBot Studio. By combining these building blocks, you can create sophisticated bots that handle complex workflows, manage user data efficiently, and provide engaging interactive experiences.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/bot-features-and-functionalities.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.