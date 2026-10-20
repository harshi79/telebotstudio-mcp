# Broadcast Function
The broadcast system in TeleBot Studio enables you to send messages or execute commands for multiple users simultaneously. This powerful feature is essential for announcements, notifications, promotional campaigns, and mass communications.
***
## Overview
Broadcasting in TeleBot Studio allows you to:
* Send messages to all bot users at once
* Execute commands across your entire user base
* Run custom code for personalized broadcasts
* Trigger external callbacks after broadcast completion
* Control and monitor broadcast status in real-time
***
## Core Broadcast Function
### Bot.sendBroadcast()
Sends a message or executes a command for all users of your bot.
**Syntax:**
```python
Bot.sendBroadcast(
code=None,
command=None,
function=None,
callback_url=None,
bot_id=None,
api_key=None,
**kwargs
)
```
**Parameters:**
* `code` (Optional): Custom TBS code to execute for the broadcast
* `command` (Optional): Name of a pre-defined command to execute
* `function` (Optional): Telegram Bot API function name (e.g., "sendMessage")
* `callback_url` (Optional): URL to call after broadcast execution
* `bot_id` (Optional): Target another bot by ID (requires api\_key)
* `api_key` (Optional): API key for accessing another bot
* `**kwargs` (Optional): Additional parameters for the function
**Important:** You must specify exactly ONE of: `code`, `command`, or `function`.
**Returns:** Dictionary with broadcast details:
* `ok` (bool): Success status
* `broadcast_id` (str): Unique broadcast identifier
* `status` (str): "running" or "queued"
* `estimated_users` (int): Number of users to receive broadcast
***
## Broadcast Limits and Constraints
### Per-Bot Limits
* **Maximum simultaneous broadcasts per bot:** 3 (updated in v1.1.0)
* **Users:** All bot users receive the broadcast
### Global Limits
* **Maximum simultaneous broadcasts globally:** 5000 (updated in v1.1.0)
### Validation
* Command must exist in the bot
* Function must be from allowed list
* Bot must be running
* Valid API key required for cross-bot broadcasts
***
## Broadcast Methods
### 1. Function-Based Broadcasting
Use Telegram Bot API functions directly.
**Allowed Functions:**
* `sendMessage` - Send text messages
* `sendPhoto` - Send images
* `sendVideo` - Send videos
* `sendAnimation` - Send GIFs/animations
* `sendAudio` - Send audio files
* `sendDocument` - Send documents
* `sendSticker` - Send stickers
* `sendPoll` - Send polls
* `sendLocation` - Send locations
* `sendVenue` - Send venues
* `sendContact` - Send contacts
* `sendDice` - Send dice animations
* `forwardMessage` - Forward messages
**Example - Simple Text Broadcast:**
```python
Bot.sendBroadcast(
function="sendMessage",
text="🎉 Exciting news! New features are now available!"
)
```
**Example - Photo Broadcast:**
```python
Bot.sendBroadcast(
function="sendPhoto",
photo="https://example.com/promo.jpg",
caption="Check out our latest product!"
)
```
**Example - Poll Broadcast:**
```python
Bot.sendBroadcast(
function="sendPoll",
question="What feature would you like next?",
options=["Dark Mode", "Voice Messages", "File Sharing", "Video Calls"],
is_anonymous=True
)
```
***
### 2. Command-Based Broadcasting
Execute a pre-defined command for all users.
**Example:**
```python
# Execute "weekly_update" command for all users
Bot.sendBroadcast(command="weekly_update")
```
**In the weekly\_update command:**
```python
# This command executes individually for each user
name = User.fetchData("name") or "there"
points = User.res("points").value() or 0
Api.sendMessage(f"Hello {name}! 👋")
Api.sendMessage(f"Your weekly summary:")
Api.sendMessage(f"• Points: {points}")
Api.sendMessage(f"• Rank: #{calculate_rank()}")
Api.sendMessage(f"Keep up the great work!")
```
**Benefits:**
* Personalized messages per user
* Access to user-specific data
* Complex logic execution
* Dynamic content generation
***
### 3. Code-Based Broadcasting
Execute custom TBS code dynamically.
**Example - Personalized Greeting:**
```python
Bot.sendBroadcast(
code='''
first_name = message.from_user.first_name
Api.sendMessage(f"Hello {first_name}! Don't miss our latest updates!")
'''
)
```
**Example - Conditional Messaging:**
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
**Example - Complex Logic:**
```python
Bot.sendBroadcast(
code='''
# Check last activity
last_active = User.fetchData("last_active") or 0
current_time = time.time()
days_inactive = (current_time - last_active) / 86400
if days_inactive > 30:
Api.sendMessage("We miss you! Come back for a special welcome bonus!")
points = User.res("points")
points.add(100)
elif days_inactive > 7:
Api.sendMessage("Haven't seen you in a while! Check out what's new!")
else:
Api.sendMessage("Thanks for being an active member!")
'''
)
```
***
## Cross-Bot Broadcasting
Send broadcasts from one bot to another's users.
**Syntax:**
```python
Bot.sendBroadcast(
bot_id="target_bot_id",
api_key="target_bot_api_key",
function="sendMessage",
text="Cross-bot notification"
)
```
**Example - Master Bot Coordinating Slave Bots:**
```python
# Master bot sends notification via Bot A
Bot.sendBroadcast(
bot_id="bot_a_id",
api_key="bot_a_api_key",
function="sendMessage",
text="Important announcement from Bot A!"
)
# Master bot sends notification via Bot B
Bot.sendBroadcast(
bot_id="bot_b_id",
api_key="bot_b_api_key",
function="sendMessage",
text="Important announcement from Bot B!"
)
```
**Security Note:** Never expose API keys in public code or logs.
***
## Callback URLs
Receive notifications after broadcast execution.
**Example:**
```python
Bot.sendBroadcast(
function="sendMessage",
text="Thank you for being with us!",
callback_url="https://example.com/broadcast-callback"
)
```
**Callback Payload:**
```json
{
"ok": true,
"bot_id": "123456789",
"success": true,
"total_success": 450,
"total_errors": 2,
"total": 452,
"status": "completed"
}
```
**Handling Callbacks:**
```python
# In your webhook endpoint
callback_data = options
success_rate = callback_data.get('total_success') / callback_data.get('total')
if success_rate > 0.95:
Api.sendMessage("Broadcast highly successful!", chat_id=ADMIN_ID)
else:
Api.sendMessage(f"Broadcast completed with {success_rate*100:.1f}% success", chat_id=ADMIN_ID)
```
***
## Managing Broadcasts
### Bot.listBroadcasts()
Lists all broadcasts for the bot.
**Syntax:**
```python
Bot.listBroadcasts()
```
**Returns:** List of broadcast dictionaries:
* `id` (int): Broadcast ID
* `status` (str): "running", "completed", or "failed"
* `created_at` (str): Creation timestamp
* `completed_at` (str): Completion timestamp (if finished)
**Example:**
```python
broadcasts = Bot.listBroadcasts()
Api.sendMessage("📊 Broadcast Status:")
for broadcast in broadcasts:
Api.sendMessage(f"ID: {broadcast['id']}")
Api.sendMessage(f"Status: {broadcast['status']}")
Api.sendMessage(f"Created: {broadcast['created_at']}")
Api.sendMessage("---")
```
***
### Bot.broadcastStatus()
Checks the status of a specific broadcast.
**Syntax:**
```python
Bot.broadcastStatus(broadcast_id)
```
**Parameters:**
* `broadcast_id` (Required): The broadcast ID to check
**Returns:** Dictionary with:
* `ok` (bool): Success status
* `id` (int): Broadcast ID
* `status` (str): Current status
* `error` (str): Error message if failed
**Example:**
```python
status = Bot.broadcastStatus(broadcast_id="123")
if status['ok']:
Api.sendMessage(f"Broadcast {status['id']}: {status['status']}")
else:
Api.sendMessage(f"Error: {status['error']}")
```
***
### Bot.pauseBroadcast()
Pauses a running broadcast.
**Syntax:**
```python
Bot.pauseBroadcast(broadcast_id)
```
**Parameters:**
* `broadcast_id` (Required): The broadcast ID to pause
**Returns:** Dictionary with success status
**Example:**
```python
result = Bot.pauseBroadcast(broadcast_id="123")
if result['ok']:
Api.sendMessage("Broadcast paused successfully")
```
**Note:** Paused broadcasts can be resumed manually from the dashboard.
***
### Bot.broadcastProgress()
Live progress: `Bot.broadcastProgress(broadcast_id)`.
### Bot.updateBroadcastSpeed()
Adjust speed: `Bot.updateBroadcastSpeed(broadcast_id, speed=15)`.
### Bot.stopBroadcast()
Stop (keep record): `Bot.stopBroadcast(broadcast_id)`.
### Bot.sendCloneBroadcast()
Re-run previous: `Bot.sendCloneBroadcast(broadcast_id)`.
### Bot.cancelBroadcast()
Cancels and removes a broadcast.
**Syntax:**
```python
Bot.cancelBroadcast(broadcast_id=None)
```
**Parameters:**
* `broadcast_id` (Optional): Specific broadcast to cancel. If None, cancels all broadcasts.
**Returns:** Dictionary with:
* `ok` (bool): Success status
* `deleted_count` (int): Number of broadcasts canceled
**Example - Cancel Specific Broadcast:**
```python
result = Bot.cancelBroadcast(broadcast_id="123")
Api.sendMessage(f"Canceled {result['deleted_count']} broadcast(s)")
```
**Example - Cancel All Broadcasts:**
```python
result = Bot.cancelBroadcast()
Api.sendMessage(f"Canceled all {result['deleted_count']} broadcasts")
```
***
## Real-World Use Cases
### 1. Promotional Campaign
```python
# /launch_promo command (admin only)
if u != ADMIN_USER_ID:
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
***
### 2. Personalized Weekly Digest
```python
# /send_weekly_digest command
Bot.sendBroadcast(command="generate_digest")
```
**In generate\_digest command:**
```python
# Get user data
name = User.fetchData("name") or "there"
points_earned = User.res("weekly_points").value() or 0
total_points = User.res("points").value() or 0
# Generate personalized digest
Api.sendMessage(f"📊 Weekly Digest for {name}")
Api.sendMessage(f"Points earned this week: {points_earned}")
Api.sendMessage(f"Total points: {total_points}")
# Reset weekly counter
User.res("weekly_points").reset()
# Add recommendations based on activity
if points_earned < 10:
Api.sendMessage("💡 Tip: Complete daily tasks to earn more points!")
else:
Api.sendMessage("🌟 Great work this week! Keep it up!")
```
***
### 3. Targeted Segment Broadcasting
```python
# Send to premium users only
Bot.sendBroadcast(
code='''
is_premium = User.fetchData("premium_member")
if is_premium:
Api.sendMessage("🌟 Premium Member Exclusive: Early access to new features!")
'''
)
# Send to inactive users
Bot.sendBroadcast(
code='''
last_active = User.fetchData("last_active") or 0
if time.time() - last_active > 2592000: # 30 days
Api.sendMessage("We miss you! Come back for 500 bonus points!")
User.res("points").add(500)
'''
)
```
***
### 4. Event Reminders
```python
# 24 hours before event
Bot.sendBroadcast(
function="sendMessage",
text="⏰ Reminder: Our webinar starts tomorrow at 3 PM EST!\nTopic: Advanced Bot Development\nRegister: /register"
)
# 1 hour before event
Bot.scheduleCommand(82800, "send_event_reminder") # 23 hours later
# In send_event_reminder command
Bot.sendBroadcast(
function="sendMessage",
text="🔔 Final Reminder: Webinar starts in 1 hour!\nJoin link: /join"
)
```
***
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
***
## Error Handling
### Common Errors and Solutions
**Error: "You already have 2 running broadcasts"**
```python
# Check broadcast status first
broadcasts = Bot.listBroadcasts()
running = [b for b in broadcasts if b['status'] == 'running']
if len(running) >= 2:
Api.sendMessage("Maximum broadcasts running. Please wait.")
else:
Bot.sendBroadcast(function="sendMessage", text="New broadcast")
```
**Error: "Command doesn't exist"**
```python
# Verify command exists before broadcasting
try:
Bot.sendBroadcast(command="nonexistent_command")
except ValueError as e:
Api.sendMessage(f"Error: {str(e)}")
Api.sendMessage("Please create the command first.")
```
**Error: "Invalid API key"**
```python
# Verify bot_id and api_key combination
try:
Bot.sendBroadcast(
bot_id="other_bot_id",
api_key="invalid_key",
function="sendMessage",
text="Test"
)
except PermissionError as e:
Api.sendMessage("API key validation failed")
```
**Error: "Function not allowed for broadcasting"**
```python
# Use only allowed functions
allowed_functions = [
"sendMessage", "sendPhoto", "sendVideo", "sendAnimation",
"sendAudio", "sendDocument", "sendSticker", "sendPoll",
"sendLocation", "sendVenue", "sendContact", "sendDice",
"forwardMessage"
]
function_name = "customFunction"
if function_name not in allowed_functions:
Api.sendMessage(f"Function '{function_name}' not allowed")
else:
Bot.sendBroadcast(function=function_name)
```
***
## Best Practices
### 1. Test Before Broadcasting
Always test broadcasts with a small group first:
```python
# Test with admin only
if u == ADMIN_USER_ID:
Api.sendMessage("Testing broadcast content...")
Api.sendMessage("This is how it will look to users.")
Api.sendMessage("Proceed with full broadcast? /confirm_broadcast")
```
### 2. Monitor Broadcast Status
Track broadcast progress:
```python
# After sending broadcast
broadcast_result = Bot.sendBroadcast(
function="sendMessage",
text="Announcement"
)
broadcast_id = broadcast_result['broadcast_id']
Bot.storeData("last_broadcast_id", broadcast_id)
# Check later
status = Bot.broadcastStatus(broadcast_id)
Api.sendMessage(f"Broadcast status: {status['status']}")
```
### 3. Avoid Spam
Respect your users by limiting broadcast frequency:
```python
last_broadcast = Bot.fetchData("last_broadcast_time") or 0
current_time = time.time()
# Minimum 24 hours between broadcasts
if current_time - last_broadcast < 86400:
Api.sendMessage("Please wait 24 hours between broadcasts")
else:
Bot.sendBroadcast(function="sendMessage", text="Announcement")
Bot.storeData("last_broadcast_time", current_time)
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
***
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
callback_url="https://yoursite.com/track-broadcast"
)
# In webhook
callback_data = options
success_rate = callback_data['total_success'] / callback_data['total']
Bot.storeData("broadcast_success_rate", success_rate)
```
### 3. Schedule Off-Peak Broadcasts
Use scheduling for better delivery:
```python
# Schedule broadcast for 2 PM
delay = calculate_seconds_until_2pm()
Bot.scheduleCommand(delay, "send_scheduled_broadcast")
# In send_scheduled_broadcast command
Bot.sendBroadcast(
function="sendMessage",
text="Daily tip: Stay active to earn more rewards!"
)
```
***
## Summary
The broadcast system in TeleBot Studio provides:
* **Flexibility**: Function, command, or code-based broadcasting
* **Control**: Monitor, pause, and cancel broadcasts
* **Scalability**: Reach all users efficiently
* **Personalization**: Customize messages per user
* **Integration**: Cross-bot broadcasting and callbacks
By following best practices and understanding the broadcast system's capabilities, you can create effective communication strategies that engage your users while maintaining platform stability.
***
For more advanced use cases and integration examples, refer to the Real-World Use Cases documentation.
