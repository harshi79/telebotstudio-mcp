> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/readme.md).
# TeleBot Studio API v2 Documentation
Welcome to the TeleBot Studio API v2 documentation. This comprehensive guide covers all API endpoints, authentication methods, and best practices for programmatically managing your bots.
\*\*\*
## Overview
The TeleBot Studio API v2 provides a complete RESTful interface for managing bots, commands, and bot operations. With flexible authentication options and comprehensive endpoints, you can integrate TeleBot Studio into your workflows and automate bot management.
\*\*Base URL:\*\* `https://api.telebotstudio.com/v2`
\*\*API Features:\*\*
\* ✅ Flexible authentication (JWT cookies or API keys)
\* ✅ Complete bot lifecycle management
\* ✅ Command creation, update, and deletion
\* ✅ Bot control (start, stop, restart)
\* ✅ Data export and import
\* ✅ Cross-origin resource sharing (CORS) enabled
\*\*\*
## Authentication
TeleBot Studio API v2 supports two authentication methods:
### 1. JWT Cookie Authentication
Used by the web interface for user sessions.
\*\*Cookie Name:\*\* `login\_token`\
\*\*Algorithm:\*\* HS256\
\*\*Expiration:\*\* 6 hours (default) or 30 days (with "remember me")
This method is automatically handled by the web interface and requires no additional setup for browser-based access.
### 2. API Key Authentication
Used for programmatic access via scripts, applications, or command-line tools.
\*\*Where to Find Your API Key:\*\*
1. Log in to TeleBotStudio.com
2. Go to Account Settings
3. Copy your API key from the API section
\*\*Three Ways to Authenticate:\*\*
\*\*Method 1: Authorization Header (Recommended)\*\*
```bash
Authorization: Bearer YOUR\_API\_KEY
```
\*\*Method 2: Query Parameter\*\*
```bash
?api\_key=YOUR\_API\_KEY
```
\*\*Method 3: JSON Body\*\*
```json
{
"api\_key": "YOUR\_API\_KEY"
}
```
\*\*\*
## Getting Your API Key
```bash
# Sign up
curl -X POST https://api.telebotstudio.com/signup \
-H "Content-Type: application/json" \
-d '{
"email": "your@email.com",
"password": "your\_password"
}'
# Response includes API key
{
"ok": true,
"result": "User created successfully",
"api\_key": "YOUR\_API\_KEY\_HERE"
}
# Sign in (if already registered)
curl -X POST https://api.telebotstudio.com/signin \
-H "Content-Type: application/json" \
-d '{
"email": "your@email.com",
"password": "your\_password"
}'
# Response includes API key
{
"ok": true,
"result": "Signed in successfully",
"api\_key": "YOUR\_API\_KEY\_HERE"
}
```
\*\*\*
## Bot Management Endpoints
### Create Bot
Creates a new bot with a Telegram bot token.
\*\*Endpoint:\*\* `POST /v2/create-bot`
\*\*Authentication:\*\* Required
\*\*Request Body:\*\*
```json
{
"bot\_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
}
```
\*\*Response:\*\*
```json
{
"ok": true,
"result": {
"botid": "12345678",
"bot\_name": "MyBot",
"bot\_username": "my\_bot"
}
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/create-bot \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{
"bot\_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
}'
```
\*\*Python Example:\*\*
```python
import requests
api\_key = "YOUR\_API\_KEY"
headers = {"Authorization": f"Bearer {api\_key}"}
response = requests.post(
"https://api.telebotstudio.com/v2/create-bot",
headers=headers,
json={"bot\_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"}
)
result = response.json()
if result['ok']:
bot\_id = result['result']['botid']
print(f"Bot created: {bot\_id}")
```
\*\*\*
### Delete Bot
Soft deletes a bot (marks as deleted, preserves data).
\*\*Endpoint:\*\* `DELETE /v2/bots/{botid}`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Bot deleted successfully"
}
```
\*\*Example:\*\*
```bash
curl -X DELETE https://api.telebotstudio.com/v2/bots/12345678 \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
### Update Bot Token
Updates the Telegram bot token for an existing bot.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/update-bot-token`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Request Body:\*\*
```json
{
"token": "987654321:NEWtokenABCdefGHIjklMNO"
}
```
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Token updated and bot started successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/update-bot-token \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{
"token": "987654321:NEWtokenABCdefGHIjklMNO"
}'
```
\*\*Note:\*\* This endpoint automatically starts the bot after updating the token.
\*\*\*
## Command Management Endpoints
### Create Command
Creates a new command for a bot.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/commands`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Request Body:\*\*
```json
{
"command": "hello",
"code": "Api.sendMessage('Hello World!')"
}
```
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Command created successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/commands \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{
"command": "start",
"code": "Api.sendMessage(\"Welcome to my bot!\")"
}'
```
\*\*Python Example:\*\*
```python
command\_code = """
Api.sendMessage("Welcome!")
Api.sendMessage("Available commands:")
Api.sendMessage("/help - Get help")
Api.sendMessage("/about - About bot")
"""
response = requests.post(
f"https://api.telebotstudio.com/v2/bots/{bot\_id}/commands",
headers=headers,
json={"command": "start", "code": command\_code}
)
```
\*\*\*
### Get Command
Retrieves details of a specific command.
\*\*Endpoint:\*\* `GET /v2/bots/{botid}/command/by-name`
\*\*Authentication:\*\* Required
\*\*Query Parameters:\*\*
\* `command\_name` (Required): Command name
\*\*Response:\*\*
```json
{
"ok": true,
"command": {
"command": "start",
"code": "Api.sendMessage('Welcome!')",
"is\_pinned": false
}
}
```
\*\*Example:\*\*
```bash
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/command/by-name?command\_name=start" \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
### Update Command
Updates an existing command's code.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/command/by-name/update`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Request Body:\*\*
```json
{
"command\_name": "start",
"code": "Api.sendMessage('Updated welcome message!')"
}
```
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Command updated successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/update \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{
"command\_name": "start",
"code": "Api.sendMessage(\"Updated!\")"
}'
```
\*\*\*
### Delete Command
Deletes a command from the bot.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/command/by-name/delete`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Request Body:\*\*
```json
{
"command\_name": "old\_command"
}
```
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Command deleted successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/delete \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{"command\_name": "old\_command"}'
```
\*\*\*
### List All Commands
Retrieves all commands for a bot.
\*\*Endpoint:\*\* `GET /v2/bots/{botid}/commands`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Response:\*\*
```json
{
"ok": true,
"commands": [
{
"command": "start",
"code": "Api.sendMessage('Welcome!')",
"is\_pinned": false
},
{
"command": "help",
"code": "Api.sendMessage('Help menu')",
"is\_pinned": false
}
]
}
```
\*\*Example:\*\*
```bash
curl -X GET https://api.telebotstudio.com/v2/bots/12345678/commands \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
## Command Name Encoding
For certain endpoints that require command names in the URL path or when working with special characters (including emojis, spaces, or slashes), command names must be properly encoded.
### When Encoding is Required
Command name encoding is \*\*required\*\* when:
\* Command contains a forward slash (e.g., `/start`, `/help`)
\* Command contains spaces (e.g., `user info`)
\* Command contains special characters or emojis (e.g., `💰 Donate`, `🎉 Welcome`)
\* Using URL path-based endpoints (legacy endpoints)
Command name encoding is \*\*NOT required\*\* when:
\* Using the `/command/by-name` endpoints (recommended)
\* Sending command name in request body or query parameters
### Encoding Methods
\*\*Method 1: Using `/command/by-name` Endpoints (Recommended)\*\*
These endpoints accept command names directly without encoding:
```bash
# Get command - no encoding needed
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/command/by-name?command\_name=/start" \
-H "Authorization: Bearer YOUR\_API\_KEY"
# Update command - no encoding needed
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/update \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{
"command\_name": "/start",
"code": "Api.sendMessage(\"Welcome!\")"
}'
# Delete command - no encoding needed
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/delete \
-H "Authorization: Bearer YOUR\_API\_KEY" \
-H "Content-Type: application/json" \
-d '{"command\_name": "/start"}'
```
\*\*Method 2: Base64 Encoding (For Legacy URL Path Endpoints)\*\*
If you need to use URL path-based endpoints, encode command names using Base64:
### Encoding Process
1. \*\*Original Command\*\*: `/start`
2. \*\*UTF-8 Encoding\*\*: Convert to bytes
3. \*\*Base64 Encoding\*\*: `L3N0YXJ0`
4. \*\*URL\*\*: `/v2/bots/{botid}/commands/L3N0YXJ0`
### Encoding Examples Table
| Original Command | Base64 Encoded | Description |
| ---------------- | ------------------ | ------------------- |
| `/start` | `L3N0YXJ0` | Basic slash command |
| `/help` | `L2hlbHA=` | Help command |
| `/settings` | `L3NldHRpbmdz` | Settings command |
| `hello` | `aGVsbG8=` | No slash |
| `hello\_world` | `aGVsbG9fd29ybGQ=` | Underscore |
| `user info` | `dXNlciBpbmZv` | Space character |
| `💰 Donate` | `8J+SsCBEb25hdGU=` | Emoji with space |
| `🎉 Welcome` | `8J+OiSBXZWxjb21l` | Emoji command |
### Code Examples for Encoding
\*\*Python:\*\*
```python
import base64
def encode\_command(command\_name):
"""Encode command name to Base64"""
return base64.b64encode(command\_name.encode('utf-8')).decode('ascii')
def decode\_command(encoded):
"""Decode Base64 command name"""
return base64.b64decode(encoded.encode('ascii')).decode('utf-8')
# Examples
print(encode\_command('/start')) # L3N0YXJ0
print(encode\_command('/help')) # L2hlbHA=
print(encode\_command('💰 Donate')) # 8J+SsCBEb25hdGU=
# Decode back
print(decode\_command('L3N0YXJ0')) # /start
```
\*\*JavaScript/Node.js:\*\*
```javascript
function encodeCommand(commandName) {
// Encode to Base64
return Buffer.from(commandName, 'utf8').toString('base64');
}
function decodeCommand(encoded) {
// Decode from Base64
return Buffer.from(encoded, 'base64').toString('utf8');
}
// Examples
console.log(encodeCommand('/start')); // L3N0YXJ0
console.log(encodeCommand('/help')); // L2hlbHA=
console.log(encodeCommand('💰 Donate')); // 8J+SsCBEb25hdGU=
// Decode back
console.log(decodeCommand('L3N0YXJ0')); // /start
```
\*\*PHP:\*\*
```php
php function encodeCommand($commandName) {
return base64\_encode($commandName);
}
function decodeCommand($encoded) {
return base64\_decode($encoded);
}
// Examples
echo encodeCommand('/start'); // L3N0YXJ0
echo encodeCommand('/help'); // L2hlbHA=
echo encodeCommand('💰 Donate'); // 8J+SsCBEb25hdGU=
?
```
\*\*cURL Examples with Encoding:\*\*
```bash
# Encode command name
COMMAND\_NAME="/start"
ENCODED=$(echo -n "$COMMAND\_NAME" | base64)
echo "Encoded: $ENCODED" # L3N0YXJ0
# Get command (using encoded name in URL path)
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/commands/$ENCODED" \
-H "Authorization: Bearer YOUR\_API\_KEY"
# For emoji commands
EMOJI\_COMMAND="💰 Donate"
ENCODED\_EMOJI=$(echo -n "$EMOJI\_COMMAND" | base64)
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/commands/$ENCODED\_EMOJI" \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
### Comparison: Encoded vs Non-Encoded Endpoints
| Feature | `/command/by-name` (Recommended) | Legacy URL Path |
| ---------------------- | -------------------------------- | -------------------- |
| \*\*Encoding Required\*\* | ❌ No | ✅ Yes (Base64) |
| \*\*Emoji Support\*\* | ✅ Direct | ✅ Via encoding |
| \*\*Space Support\*\* | ✅ Direct | ✅ Via encoding |
| \*\*Special Characters\*\* | ✅ Direct | ✅ Via encoding |
| \*\*Ease of Use\*\* | ✅ Simple | ⚠️ Requires encoding |
| \*\*URL Length\*\* | ✅ Shorter | ⚠️ Longer |
| \*\*Recommended\*\* | ✅ Yes | ⚠️ Legacy only |
### Best Practices
1. \*\*Use `/command/by-name` endpoints\*\* for new integrations (no encoding needed)
2. \*\*Use Base64 encoding\*\* only for legacy URL path endpoints
3. \*\*Always use UTF-8 encoding\*\* before Base64 conversion
4. \*\*Test with special characters\*\* (emojis, spaces, Unicode) during development
5. \*\*URL-encode the Base64 string\*\* if your HTTP client doesn't do it automatically
### Complete Example with Encoding
\*\*Python Complete Example:\*\*
```python
import base64
import requests
class CommandManager:
def \_\_init\_\_(self, api\_key, bot\_id):
self.api\_key = api\_key
self.bot\_id = bot\_id
self.base\_url = "https://api.telebotstudio.com/v2"
self.headers = {"Authorization": f"Bearer {api\_key}"}
# Method 1: No encoding (Recommended)
def get\_command\_simple(self, command\_name):
"""Get command without encoding"""
response = requests.get(
f"{self.base\_url}/bots/{self.bot\_id}/command/by-name",
headers=self.headers,
params={"command\_name": command\_name}
)
return response.json()
def update\_command\_simple(self, command\_name, code):
"""Update command without encoding"""
response = requests.post(
f"{self.base\_url}/bots/{self.bot\_id}/command/by-name/update",
headers=self.headers,
json={"command\_name": command\_name, "code": code}
)
return response.json()
# Method 2: With encoding (Legacy)
@staticmethod
def encode\_command(command\_name):
"""Encode command name to Base64"""
return base64.b64encode(command\_name.encode('utf-8')).decode('ascii')
def get\_command\_encoded(self, command\_name):
"""Get command with Base64 encoding (legacy)"""
encoded = self.encode\_command(command\_name)
response = requests.get(
f"{self.base\_url}/bots/{self.bot\_id}/commands/{encoded}",
headers=self.headers
)
return response.json()
# Usage
manager = CommandManager("YOUR\_API\_KEY", "12345678")
# Recommended approach - no encoding
result = manager.get\_command\_simple("/start")
manager.update\_command\_simple("/start", 'Api.sendMessage("Welcome!")')
# Works with emojis too
result = manager.get\_command\_simple("💰 Donate")
manager.update\_command\_simple("💰 Donate", 'Api.sendMessage("Thanks!")')
# Legacy approach - with encoding
result = manager.get\_command\_encoded("/start")
```
\*\*\*
## Bot Control Endpoints
### Start Bot
Starts a bot by setting its webhook.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/start`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Bot started successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/start \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
### Stop Bot
Stops a bot by removing its webhook.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/stop`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Bot stopped successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/stop \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
### Restart Bot
Stops and starts a bot in one operation.
\*\*Endpoint:\*\* `POST /v2/bots/{botid}/restart`
\*\*Authentication:\*\* Required
\*\*URL Parameters:\*\*
\* `botid` (Required): Bot identifier
\*\*Response:\*\*
```json
{
"ok": true,
"result": "Bot restarted successfully"
}
```
\*\*Example:\*\*
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/restart \
-H "Authorization: Bearer YOUR\_API\_KEY"
```
\*\*\*
## Error Responses
### Authentication Errors
\*\*Missing Authentication:\*\*
```json
{
"ok": false,
"result": "Authentication required"
}
```
\*\*Invalid API Key:\*\*
```json
{
"ok": false,
"result": "Invalid API key"
}
```
\*\*Expired Token:\*\*
```json
{
"ok": false,
"result": "Token has expired"
}
```
### Resource Errors
\*\*Bot Not Found:\*\*
```json
{
"ok": false,
"result": "Bot not found or not owned by you"
}
```
\*\*Command Not Found:\*\*
```json
{
"ok": false,
"result": "Command not found"
}
```
### Validation Errors
\*\*Invalid Bot Token:\*\*
```json
{
"ok": false,
"result": "Invalid bot token format"
}
```
\*\*Missing Required Field:\*\*
```json
{
"ok": false,
"result": "Bot token is required"
}
```
\*\*\*
## Rate Limiting
\*\*Limits:\*\*
\* 60 requests per minute per IP address
\* 1000 requests per hour per API key
\*\*Headers:\*\*
\* `X-RateLimit-Limit`: Maximum requests per window
\* `X-RateLimit-Remaining`: Remaining requests
\* `X-RateLimit-Reset`: UTC timestamp when limit resets
\*\*Rate Limit Exceeded Response:\*\*
```json
{
"ok": false,
"result": "Rate limit exceeded. Try again in 60 seconds."
}
```
\*\*\*
## Code Examples
### Complete Bot Creation Workflow
\*\*Python:\*\*
```python
import requests
class TeleBotStudioAPI:
def \_\_init\_\_(self, api\_key):
self.api\_key = api\_key
self.base\_url = "https://api.telebotstudio.com/v2"
self.headers = {"Authorization": f"Bearer {api\_key}"}
def create\_bot(self, bot\_token):
"""Create a new bot"""
response = requests.post(
f"{self.base\_url}/create-bot",
headers=self.headers,
json={"bot\_token": bot\_token}
)
return response.json()
def create\_command(self, bot\_id, command\_name, code):
"""Create a command"""
response = requests.post(
f"{self.base\_url}/bots/{bot\_id}/commands",
headers=self.headers,
json={"command": command\_name, "code": code}
)
return response.json()
def start\_bot(self, bot\_id):
"""Start a bot"""
response = requests.post(
f"{self.base\_url}/bots/{bot\_id}/start",
headers=self.headers
)
return response.json()
# Usage
api = TeleBotStudioAPI("YOUR\_API\_KEY")
# Create bot
result = api.create\_bot("123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
bot\_id = result['result']['botid']
print(f"Bot created: {bot\_id}")
# Add /start command
start\_code = 'Api.sendMessage("Welcome to my bot!")'
api.create\_command(bot\_id, "start", start\_code)
# Add /help command
help\_code = 'Api.sendMessage("Available commands:\\n/start - Start\\n/help - Help")'
api.create\_command(bot\_id, "help", help\_code)
# Start bot
api.start\_bot(bot\_id)
print("Bot started successfully!")
```
\*\*\*
\*\*Node.js:\*\*
```javascript
const axios = require('axios');
class TeleBotStudioAPI {
constructor(apiKey) {
this.apiKey = apiKey;
this.baseUrl = 'https://api.telebotstudio.com/v2';
this.headers = { 'Authorization': `Bearer ${apiKey}` };
}
async createBot(botToken) {
const response = await axios.post(
`${this.baseUrl}/create-bot`,
{ bot\_token: botToken },
{ headers: this.headers }
);
return response.data;
}
async createCommand(botId, commandName, code) {
const response = await axios.post(
`${this.baseUrl}/bots/${botId}/commands`,
{ command: commandName, code: code },
{ headers: this.headers }
);
return response.data;
}
async startBot(botId) {
const response = await axios.post(
`${this.baseUrl}/bots/${botId}/start`,
{},
{ headers: this.headers }
);
return response.data;
}
}
// Usage
(async () => {
const api = new TeleBotStudioAPI('YOUR\_API\_KEY');
// Create bot
const result = await api.createBot('123456789:ABCdefGHIjklMNOpqrsTUVwxyz');
const botId = result.result.botid;
console.log(`Bot created: ${botId}`);
// Add commands
await api.createCommand(botId, 'start', 'Api.sendMessage("Welcome!")');
await api.createCommand(botId, 'help', 'Api.sendMessage("Help menu")');
// Start bot
await api.startBot(botId);
console.log('Bot started!');
})();
```
\*\*\*
### Bulk Command Management
```python
def bulk\_create\_commands(api, bot\_id, commands\_dict):
"""Create multiple commands at once"""
results = []
for cmd\_name, cmd\_code in commands\_dict.items():
result = api.create\_command(bot\_id, cmd\_name, cmd\_code)
results.append({
'command': cmd\_name,
'success': result['ok']
})
return results
# Define commands
commands = {
"start": 'Api.sendMessage("Welcome to my bot!")',
"help": 'Api.sendMessage("Help menu")',
"about": 'Api.sendMessage("About this bot")',
"settings": 'Api.sendMessage("Settings menu")'
}
# Create all commands
results = bulk\_create\_commands(api, bot\_id, commands)
print(f"Created {sum(1 for r in results if r['success'])} commands")
```
\*\*\*
## Best Practices
### 1. Security
\*\*Protect Your API Key:\*\*
```python
# ❌ Wrong - Don't hardcode in source
api\_key = "my\_actual\_api\_key\_12345"
# ✅ Correct - Use environment variables
import os
api\_key = os.getenv('TELEBOT\_API\_KEY')
```
\*\*Use HTTPS Only:\*\*
```python
# ✅ Always use HTTPS
base\_url = "https://api.telebotstudio.com/v2"
# ❌ Never use HTTP
# base\_url = "http://telebotstudio.com/v2"
```
\*\*Rotate API Keys Regularly:\*\*
\* Generate new API keys every 90 days
\* Immediately revoke keys if compromised
\* Use different keys for different applications
### 2. Error Handling
\*\*Implement Robust Error Handling:\*\*
```python
def safe\_api\_call(func, \*args, \*\*kwargs):
"""Wrapper for API calls with error handling"""
max\_retries = 3
retry\_delay = 2
for attempt in range(max\_retries):
try:
response = func(\*args, \*\*kwargs)
if response['ok']:
return response
else:
print(f"API error: {response['result']}")
return None
except requests.exceptions.Timeout:
print(f"Timeout on attempt {attempt + 1}")
if attempt < max\_retries - 1:
time.sleep(retry\_delay)
except requests.exceptions.RequestException as e:
print(f"Request failed: {e}")
return None
return None
# Usage
result = safe\_api\_call(api.create\_bot, "123456789:TOKEN")
```
### 3. Rate Limiting
\*\*Respect Rate Limits:\*\*
```python
import time
class RateLimitedAPI:
def \_\_init\_\_(self, api\_key, requests\_per\_minute=50):
self.api = TeleBotStudioAPI(api\_key)
self.min\_interval = 60 / requests\_per\_minute
self.last\_request = 0
def \_wait\_if\_needed(self):
"""Wait if necessary to respect rate limit"""
elapsed = time.time() - self.last\_request
if elapsed < self.min\_interval:
time.sleep(self.min\_interval - elapsed)
self.last\_request = time.time()
def create\_command(self, \*args, \*\*kwargs):
self.\_wait\_if\_needed()
return self.api.create\_command(\*args, \*\*kwargs)
# Usage
limited\_api = RateLimitedAPI("YOUR\_API\_KEY", requests\_per\_minute=50)
```
### 4. Logging
\*\*Log All API Interactions:\*\*
```python
import logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s',
filename='telebot\_api.log'
)
def log\_api\_call(endpoint, method, response):
"""Log API call details"""
logging.info(f"{method} {endpoint} - Status: {response.get('ok')}")
if not response.get('ok'):
logging.error(f"Error: {response.get('result')}")
# Usage
response = api.create\_bot(bot\_token)
log\_api\_call('/v2/create-bot', 'POST', response)
```
\*\*\*
## Common Use Cases
### 1. Automated Bot Deployment
```python
def deploy\_bot(api\_key, bot\_token, commands):
"""Complete bot deployment workflow"""
api = TeleBotStudioAPI(api\_key)
# Step 1: Create bot
print("Creating bot...")
result = api.create\_bot(bot\_token)
if not result['ok']:
print(f"Failed to create bot: {result['result']}")
return False
bot\_id = result['result']['botid']
print(f"Bot created with ID: {bot\_id}")
# Step 2: Add commands
print("Adding commands...")
for cmd\_name, cmd\_code in commands.items():
result = api.create\_command(bot\_id, cmd\_name, cmd\_code)
if result['ok']:
print(f" ✓ {cmd\_name}")
else:
print(f" ✗ {cmd\_name}: {result['result']}")
# Step 3: Start bot
print("Starting bot...")
result = api.start\_bot(bot\_id)
if result['ok']:
print("✓ Bot deployed successfully!")
return True
else:
print(f"Failed to start bot: {result['result']}")
return False
# Usage
commands = {
"start": 'Api.sendMessage("Welcome!")',
"help": 'Api.sendMessage("Help menu")',
}
deploy\_bot("YOUR\_API\_KEY", "BOT\_TOKEN", commands)
```
### 2. Bot Backup and Restore
```python
def backup\_bot(api, bot\_id):
"""Backup all bot commands"""
response = requests.get(
f"{api.base\_url}/bots/{bot\_id}/commands",
headers=api.headers
)
if response.json()['ok']:
commands = response.json()['commands']
backup = {cmd['command']: cmd['code'] for cmd in commands}
# Save to file
with open(f'bot\_{bot\_id}\_backup.json', 'w') as f:
json.dump(backup, f, indent=2)
print(f"Backed up {len(backup)} commands")
return backup
return None
def restore\_bot(api, bot\_id, backup\_file):
"""Restore commands from backup"""
with open(backup\_file, 'r') as f:
commands = json.load(f)
for cmd\_name, cmd\_code in commands.items():
api.create\_command(bot\_id, cmd\_name, cmd\_code)
print(f"Restored {len(commands)} commands")
```
\*\*\*
## Support
For additional help:
\* \*\*Documentation:\*\* 
\* \*\*API Status:\*\* 
\* \*\*Contact:\*\* 
\*\*\*
## Changelog
### Version 2.0 (Current)
\* ✅ Flexible authentication (JWT + API key)
\* ✅ Simplified command management endpoints
\* ✅ Enhanced error messages
\* ✅ Rate limiting with headers
\* ✅ CORS support
\* ✅ Bot control endpoints (start/stop/restart)
\*\*\*
\*\*Last Updated:\*\* 2025-11-02
\*TeleBot Studio API v2 - Build, Deploy, Scale. Free Forever.\*
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/readme.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.