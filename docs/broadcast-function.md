> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/broadcast-function.md).
# Broadcast Function
The broadcast system in TeleBot Studio enables you to send messages or execute commands for multiple users simultaneously. This powerful feature is essential for announcements, notifications, promotional campaigns, and mass communications.
\*\*\*
## Overview
Broadcasting in TeleBot Studio allows you to:
\* Send messages to all bot users at once
\* Execute commands across your entire user base
\* Run custom code for personalized broadcasts
\* Trigger external callbacks after broadcast completion
\* Control and monitor broadcast status in real-time
\*\*\*
## Core Broadcast Function
### Bot.sendBroadcast()
Sends a message or executes a command for all users of your bot.
\*\*Syntax:\*\*
```python
Bot.sendBroadcast(
code=None,
command=None,
function=None,
callback\_url=None,
bot\_id=None,
api\_key=None,
\*\*kwargs
)
```
\*\*Parameters:\*\*
\* `code` (Optional): Custom TBS code to execute for the broadcast
\* `command` (Optional): Name of a pre-defined command to execute
\* `function` (Optional): Telegram Bot API function name (e.g., "sendMessage")
\* `callback\_url` (Optional): URL to call after broadcast execution
\* `bot\_id` (Optional): Target another bot by ID (requires api\\_key)
\* `api\_key` (Optional): API key for accessing another bot
\* `\*\*kwargs` (Optional): Additional parameters for the function
\*\*Important:\*\* You must specify exactly ONE of: `code`, `command`, or `function`.
\*\*Returns:\*\* Dictionary with broadcast details:
\* `ok` (bool): Success status
\* `broadcast\_id` (str): Unique broadcast identifier
\* `status` (str): "running" or "queued"
\* `estimated\_users` (int): Number of users to receive broadcast
\*\*\*
## Broadcast Limits and Constraints
### Per-Bot Limits
\* \*\*Maximum simultaneous broadcasts per bot:\*\* 2
\* \*\*Users:\*\* All bot users receive the broadcast
### Global Limits
\* \*\*Maximum simultaneous broadcasts globally:\*\* 1000
### Validation
\* Command must exist in the bot
\* Function must be from allowed list
\* Bot must be running
\* Valid API key required for cross-bot broadcasts
\*\*\*
## Broadcast Methods
### 1. Function-Based Broadcasting
Use Telegram Bot API functions directly.
\*\*Allowed Functions:\*\*
\* `sendMessage` - Send text messages
\* `sendPhoto` - Send images
\* `sendVideo` - Send videos
\* `sendAnimation` - Send GIFs/animations
\* `sendAudio` - Send audio files
\* `sendDocument` - Send documents
\* `sendSticker` - Send stickers
\* `sendPoll` - Send polls
\* `sendLocation` - Send locations
\* `sendVenue` - Send venues
\* `sendContact` - Send contacts
\* `sendDice` - Send dice animations
\* `forwardMessage` - Forward messages
\*\*Example - Simple Text Broadcast:\*\*
```python
Bot.sendBroadcast(
function="sendMessage",
text="🎉 Exciting news! New features are now available!"
)
```
\*\*Example - Photo Broadcast:\*\*
```python
Bot.sendBroadcast(
function="sendPhoto",
photo="https://example.com/promo.jpg",
caption="Check out our latest product!"
)
```
\*\*Example - Poll Broadcast:\*\*
```python
Bot.sendBroadcast(
function="sendPoll",
question="What feature would you like next?",
options=["Dark Mode", "Voice Messages", "File Sharing", "Video Calls"],
is\_anonymous=True
)
```
\*\*\*
### 2. Command-Based Broadcasting
Execute a pre-defined command for all users.
\*\*Example:\*\*
```python
# Execute "weekly\_update" command for all users
Bot.sendBroadcast(command="weekly\_update")
```
\*\*In the weekly\\_update command:\*\*
```python
# This command executes individually for each user
name = User.fetchData("name") or "there"
points = User.res("points").value() or 0
Api.sendMessage(f"Hello {name}! 👋")
Api.sendMessage(f"Your weekly summary:")
Api.sendMessage(f"• Points: {points}")
Api.sendMessage(f"• Rank: #{calculate\_rank()}")
Api.sendMessage(f"Keep up the great work!")
```
\*\*Benefits:\*\*
\* Personalized messages per user
\* Access to user-specific data
\* Complex logic execution
\* Dynamic content generation
\*\*\*
### 3. Code-Based Broadcasting
Execute custom TBS code dynamically.
\*\*Example - Personalized Greeting:\*\*
```python
Bot.sendBroadcast(
code='''
first\_name = message.from\_user.first\_name
Api.sendMessage(f"Hello {first\_name}! Don't miss our latest updates!")
'''
)
```
\*\*Example - Conditional Messaging:\*\*
```python
Bot.sendBroadcast(
code='''
points = User.res("points").value() or 0
if points >= 1000:
Api.sendMessage("🌟 VIP user! You have exclusive access to premium features.")
elif points >= 500:
Api.sendMessage("⭐ Premium user! Unlock more rewards soon.")
else:
Api.sendMessage("📢 Earn more points to unlock exclusive features!")
'''
)
```
\*\*Example - Complex Logic:\*\*
```python
Bot.sendBroadcast(
code='''
# Check last activity
last\_active = User.fetchData("last\_active") or 0
current\_time = time.time()
days\_inactive = (current\_time - last\_active) / 86400
if days\_inactive > 30:
Api.sendMessage("We miss you! Come back for a special welcome bonus!")
points = User.res("points")
points.add(100)
elif days\_inactive > 7:
Api.sendMessage("Haven't seen you in a while! Check out what's new!")
else:
Api.sendMessage("Thanks for being an active member!")
'''
)
```
\*\*\*
## Cross-Bot Broadcasting
Send broadcasts from one bot to another's users.
\*\*Syntax:\*\*
```python
Bot.sendBroadcast(
bot\_id="target\_bot\_id",
api\_key="target\_bot\_api\_key",
function="sendMessage",
text="Cross-bot notification"
)
```
\*\*Example - Master Bot Coordinating Slave Bots:\*\*
```python
# Master bot sends notification via Bot A
Bot.sendBroadcast(
bot\_id="bot\_a\_id",
api\_key="bot\_a\_api\_key",
function="sendMessage",
text="Important announcement from Bot A!"
)
# Master bot sends notification via Bot B
Bot.sendBroadcast(
bot\_id="bot\_b\_id",
api\_key="bot\_b\_api\_key",
function="sendMessage",
text="Important announcement from Bot B!"
)
```
\*\*Security Note:\*\* Never expose API keys in public code or logs.
\*\*\*
## Callback URLs
Receive notifications after broadcast execution.
\*\*Example:\*\*
```python
Bot.sendBroadcast(
function="sendMessage",
text="Thank you for being with us!",
callback\_url="https://example.com/broadcast-callback"
)
```
\*\*Callback Payload:\*\*
```json
{
"ok": true,
"bot\_id": "123456789",
"success": true,
"total\_success": 450,
"total\_errors": 2,
"total": 452,
"status": "completed"
}
```
\*\*Handling Callbacks:\*\*
```python
# In your webhook endpoint
callback\_data = options
success\_rate = callback\_data.get('total\_success') / callback\_data.get('total')
if success\_rate > 0.95:
Api.sendMessage("Broadcast highly successful!", chat\_id=ADMIN\_ID)
else:
Api.sendMessage(f"Broadcast completed with {success\_rate\*100:.1f}% success", chat\_id=ADMIN\_ID)
```
\*\*\*
## Managing Broadcasts
### Bot.listBroadcasts()
Lists all broadcasts for the bot.
\*\*Syntax:\*\*
```python
Bot.listBroadcasts()
```
\*\*Returns:\*\* List of broadcast dictionaries:
\* `id` (int): Broadcast ID
\* `status` (str): "running", "completed", or "failed"
\* `created\_at` (str): Creation timestamp
\* `completed\_at` (str): Completion timestamp (if finished)
\*\*Example:\*\*
```python
broadcasts = Bot.listBroadcasts()
Api.sendMessage("📊 Broadcast Status:")
for broadcast in broadcasts:
Api.sendMessage(f"ID: {broadcast['id']}")
Api.sendMessage(f"Status: {broadcast['status']}")
Api.sendMessage(f"Created: {broadcast['created\_at']}")
Api.sendMessage("---")
```
\*\*\*
### Bot.broadcastStatus()
Checks the status of a specific broadcast.
\*\*Syntax:\*\*
```python
Bot.broadcastStatus(broadcast\_id)
```
\*\*Parameters:\*\*
\* `broadcast\_id` (Required): The broadcast ID to check
\*\*Returns:\*\* Dictionary with:
\* `ok` (bool): Success status
\* `id` (int): Broadcast ID
\* `status` (str): Current status
\* `error` (str): Error message if failed
\*\*Example:\*\*
```python
status = Bot.broadcastStatus(broadcast\_id="123")
if status['ok']:
Api.sendMessage(f"Broadcast {status['id']}: {status['status']}")
else:
Api.sendMessage(f"Error: {status['error']}")
```
\*\*\*
### Bot.pauseBroadcast()
Pauses a running broadcast.
\*\*Syntax:\*\*
```python
Bot.pauseBroadcast(broadcast\_id)
```
\*\*Parameters:\*\*
\* `broadcast\_id` (Required): The broadcast ID to pause
\*\*Returns:\*\* Dictionary with success status
\*\*Example:\*\*
```python
result = Bot.pauseBroadcast(broadcast\_id="123")
if result['ok']:
Api.sendMessage("Broadcast paused successfully")
```
\*\*Note:\*\* Paused broadcasts can be resumed manually from the dashboard.
\*\*\*
### Bot.cancelBroadcast()
Cancels and removes a broadcast.
\*\*Syntax:\*\*
```python
Bot.cancelBroadcast(broadcast\_id=None)
```
\*\*Parameters:\*\*
\* `broadcast\_id` (Optional): Specific broadcast to cancel. If None, cancels all broadcasts.
\*\*Returns:\*\* Dictionary with:
\* `ok` (bool): Success status
\* `deleted\_count` (int): Number of broadcasts canceled
\*\*Example - Cancel Specific Broadcast:\*\*
```python
result = Bot.cancelBroadcast(broadcast\_id="123")
Api.sendMessage(f"Canceled {result['deleted\_count']} broadcast(s)")
```
\*\*Example - Cancel All Broadcasts:\*\*
```python
result = Bot.cancelBroadcast()
Api.sendMessage(f"Canceled all {result['deleted\_count']} broadcasts")
```
\*\*\*
## Real-World Use Cases
### 1. Promotional Campaign
```python
# /launch\_promo command (admin only)
if u != ADMIN\_USER\_ID:
Api.sendMessage("Unauthorized")
else:
Api.sendMessage("Launching promotional campaign...")
Bot.sendBroadcast(
function="sendPhoto",
photo="https://yoursite.com/promo.jpg",
caption="🎉 FLASH SALE! 50% OFF Everything!\nUse code: FLASH50\nOffer ends in 24 hours!"
)
Api.sendMessage("Promotional broadcast sent to all users!")
```
\*\*\*
### 2. Personalized Weekly Digest
```python
# /send\_weekly\_digest command
Bot.sendBroadcast(command="generate\_digest")
```
\*\*In generate\\_digest command:\*\*
```python
# Get user data
name = User.fetchData("name") or "there"
points\_earned = User.res("weekly\_points").value() or 0
total\_points = User.res("points").value() or 0
# Generate personalized digest
Api.sendMessage(f"📊 Weekly Digest for {name}")
Api.sendMessage(f"Points earned this week: {points\_earned}")
Api.sendMessage(f"Total points: {total\_points}")
# Reset weekly counter
User.res("weekly\_points").reset()
# Add recommendations based on activity
if points\_earned < 10:
Api.sendMessage("💡 Tip: Complete daily tasks to earn more points!")
else:
Api.sendMessage("🌟 Great work this week! Keep it up!")
```
\*\*\*
### 3. Targeted Segment Broadcasting
```python
# Send to premium users only
Bot.sendBroadcast(
code='''
is\_premium = User.fetchData("premium\_member")
if is\_premium:
Api.sendMessage("🌟 Premium Member Exclusive: Early access to new features!")
'''
)
# Send to inactive users
Bot.sendBroadcast(
code='''
last\_active = User.fetchData("last\_active") or 0
if time.time() - last\_active > 2592000: # 30 days
Api.sendMessage("We miss you! Come back for 500 bonus points!")
User.res("points").add(500)
'''
)
```
\*\*\*
### 4. Event Reminders
```python
# 24 hours before event
Bot.sendBroadcast(
function="sendMessage",
text="⏰ Reminder: Our webinar starts tomorrow at 3 PM EST!\nTopic: Advanced Bot Development\nRegister: /register"
)
# 1 hour before event
Bot.scheduleCommand(82800, "send\_event\_reminder") # 23 hours later
# In send\_event\_reminder command
Bot.sendBroadcast(
function="sendMessage",
text="🔔 Final Reminder: Webinar starts in 1 hour!\nJoin link: /join"
)
```
\*\*\*
### 5. System Announcements
```python
# Maintenance notification
Bot.sendBroadcast(
function="sendMessage",
text="🔧 Scheduled Maintenance\nThe bot will be offline for 30 minutes starting at 2 AM UTC.\nWe apologize for any inconvenience."
)
# Update notification
Bot.sendBroadcast(
function="sendMessage",
text="✨ New Update Available!\nVersion 2.0 Features:\n• Dark mode\n• Voice messages\n• Enhanced security\nUpdate now: /update"
)
```
\*\*\*
## Error Handling
### Common Errors and Solutions
\*\*Error: "You already have 2 running broadcasts"\*\*
```python
# Check broadcast status first
broadcasts = Bot.listBroadcasts()
running = [b for b in broadcasts if b['status'] == 'running']
if len(running) >= 2:
Api.sendMessage("Maximum broadcasts running. Please wait.")
else:
Bot.sendBroadcast(function="sendMessage", text="New broadcast")
```
\*\*Error: "Command doesn't exist"\*\*
```python
# Verify command exists before broadcasting
try:
Bot.sendBroadcast(command="nonexistent\_command")
except ValueError as e:
Api.sendMessage(f"Error: {str(e)}")
Api.sendMessage("Please create the command first.")
```
\*\*Error: "Invalid API key"\*\*
```python
# Verify bot\_id and api\_key combination
try:
Bot.sendBroadcast(
bot\_id="other\_bot\_id",
api\_key="invalid\_key",
function="sendMessage",
text="Test"
)
except PermissionError as e:
Api.sendMessage("API key validation failed")
```
\*\*Error: "Function not allowed for broadcasting"\*\*
```python
# Use only allowed functions
allowed\_functions = [
"sendMessage", "sendPhoto", "sendVideo", "sendAnimation",
"sendAudio", "sendDocument", "sendSticker", "sendPoll",
"sendLocation", "sendVenue", "sendContact", "sendDice",
"forwardMessage"
]
function\_name = "customFunction"
if function\_name not in allowed\_functions:
Api.sendMessage(f"Function '{function\_name}' not allowed")
else:
Bot.sendBroadcast(function=function\_name)
```
\*\*\*
## Best Practices
### 1. Test Before Broadcasting
Always test broadcasts with a small group first:
```python
# Test with admin only
if u == ADMIN\_USER\_ID:
Api.sendMessage("Testing broadcast content...")
Api.sendMessage("This is how it will look to users.")
Api.sendMessage("Proceed with full broadcast? /confirm\_broadcast")
```
### 2. Monitor Broadcast Status
Track broadcast progress:
```python
# After sending broadcast
broadcast\_result = Bot.sendBroadcast(
function="sendMessage",
text="Announcement"
)
broadcast\_id = broadcast\_result['broadcast\_id']
Bot.storeData("last\_broadcast\_id", broadcast\_id)
# Check later
status = Bot.broadcastStatus(broadcast\_id)
Api.sendMessage(f"Broadcast status: {status['status']}")
```
### 3. Avoid Spam
Respect your users by limiting broadcast frequency:
```python
last\_broadcast = Bot.fetchData("last\_broadcast\_time") or 0
current\_time = time.time()
# Minimum 24 hours between broadcasts
if current\_time - last\_broadcast < 86400:
Api.sendMessage("Please wait 24 hours between broadcasts")
else:
Bot.sendBroadcast(function="sendMessage", text="Announcement")
Bot.storeData("last\_broadcast\_time", current\_time)
```
### 4. Personalize Content
Make broadcasts relevant to each user:
```python
Bot.sendBroadcast(
code='''
language = User.fetchData("language") or "en"
if language == "es":
Api.sendMessage("¡Hola! Tenemos nuevas funciones.")
elif language == "fr":
Api.sendMessage("Bonjour! Nous avons de nouvelles fonctionnalités.")
else:
Api.sendMessage("Hello! We have new features.")
'''
)
```
### 5. Handle Errors Gracefully
Implement error handling in broadcast code:
```python
Bot.sendBroadcast(
code='''
try:
name = User.fetchData("name")
Api.sendMessage(f"Hello {name}!")
except Exception as e:
Api.sendMessage("Hello! We have an update for you.")
'''
)
```
\*\*\*
## Performance Tips
### 1. Optimize Broadcast Content
Keep broadcasts concise and focused:
```python
# Good: Clear and concise
Bot.sendBroadcast(
function="sendMessage",
text="🎉 New feature: Dark Mode\nEnable it in /settings"
)
# Avoid: Too long or complex
# Long paragraphs may cause user disengagement
```
### 2. Use Callbacks for Analytics
Track broadcast success:
```python
Bot.sendBroadcast(
function="sendMessage",
text="Survey: Rate our service /rate",
callback\_url="https://yoursite.com/track-broadcast"
)
# In webhook
callback\_data = options
success\_rate = callback\_data['total\_success'] / callback\_data['total']
Bot.storeData("broadcast\_success\_rate", success\_rate)
```
### 3. Schedule Off-Peak Broadcasts
Use scheduling for better delivery:
```python
# Schedule broadcast for 2 PM
delay = calculate\_seconds\_until\_2pm()
Bot.scheduleCommand(delay, "send\_scheduled\_broadcast")
# In send\_scheduled\_broadcast command
Bot.sendBroadcast(
function="sendMessage",
text="Daily tip: Stay active to earn more rewards!"
)
```
\*\*\*
## Summary
The broadcast system in TeleBot Studio provides:
\* \*\*Flexibility\*\*: Function, command, or code-based broadcasting
\* \*\*Control\*\*: Monitor, pause, and cancel broadcasts
\* \*\*Scalability\*\*: Reach all users efficiently
\* \*\*Personalization\*\*: Customize messages per user
\* \*\*Integration\*\*: Cross-bot broadcasting and callbacks
By following best practices and understanding the broadcast system's capabilities, you can create effective communication strategies that engage your users while maintaining platform stability.
\*\*\*
For more advanced use cases and integration examples, refer to the Real-World Use Cases documentation.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/broadcast-function.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.