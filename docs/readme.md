# TeleBot Studio API v2 Documentation
Welcome to the TeleBot Studio API v2 documentation. This comprehensive guide covers all API endpoints, authentication methods, and best practices for programmatically managing your bots.
***
## Overview
The TeleBot Studio API v2 provides a complete RESTful interface for managing bots, commands, and bot operations. With flexible authentication options and comprehensive endpoints, you can integrate TeleBot Studio into your workflows and automate bot management.
**Base URL:** `https://api.telebotstudio.com/v2`
**API Features:**
* ✅ Flexible authentication (JWT cookies or API keys)
* ✅ Complete bot lifecycle management
* ✅ Command creation, update, and deletion
* ✅ Bot control (start, stop, restart)
* ✅ Data export and import
* ✅ Cross-origin resource sharing (CORS) enabled
***
## Authentication
TeleBot Studio API v2 supports two authentication methods:
### 1. JWT Cookie Authentication
Used by the web interface for user sessions.
**Cookie Name:** `login_token`
**Algorithm:** HS256
**Expiration:** 6 hours (default) or 30 days (with "remember me")
This method is automatically handled by the web interface and requires no additional setup for browser-based access.
### 2. API Key Authentication
Used for programmatic access via scripts, applications, or command-line tools.
**Where to Find Your API Key:**
1. Log in to TeleBotStudio.com
2. Go to Account Settings
3. Copy your API key from the API section
**Three Ways to Authenticate:**
**Method 1: Authorization Header (Recommended)**
```bash
Authorization: Bearer YOUR_API_KEY
```
**Method 2: Query Parameter**
```bash
?api_key=YOUR_API_KEY
```
**Method 3: JSON Body**
```json
{
"api_key": "YOUR_API_KEY"
}
```
***
## Getting Your API Key
```bash
# Sign up
curl -X POST https://api.telebotstudio.com/signup \
-H "Content-Type: application/json" \
-d '{
"email": "your@email.com",
"password": "your_password"
}'
# Response includes API key
{
"ok": true,
"result": "User created successfully",
"api_key": "YOUR_API_KEY_HERE"
}
# Sign in (if already registered)
curl -X POST https://api.telebotstudio.com/signin \
-H "Content-Type: application/json" \
-d '{
"email": "your@email.com",
"password": "your_password"
}'
# Response includes API key
{
"ok": true,
"result": "Signed in successfully",
"api_key": "YOUR_API_KEY_HERE"
}
```
***
## Bot Management Endpoints
### Create Bot
Creates a new bot with a Telegram bot token.
**Endpoint:** `POST /v2/create-bot`
**Authentication:** Required
**Request Body:**
```json
{
"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
}
```
**Response:**
```json
{
"ok": true,
"result": {
"botid": "12345678",
"bot_name": "MyBot",
"bot_username": "my_bot"
}
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/create-bot \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
}'
```
**Python Example:**
```python
import requests

api_key = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.post(
    "https://api.telebotstudio.com/v2/create-bot",
    headers=headers,
    json={"bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"},
)
result = response.json()
if result["ok"]:
    bot_id = result["result"]["botid"]
    print(f"Bot created: {bot_id}")
```
***
### Delete Bot
Soft deletes a bot (marks as deleted, preserves data).
**Endpoint:** `DELETE /v2/bots/{botid}`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Response:**
```json
{
"ok": true,
"result": "Bot deleted successfully"
}
```
**Example:**
```bash
curl -X DELETE https://api.telebotstudio.com/v2/bots/12345678 \
-H "Authorization: Bearer YOUR_API_KEY"
```
***
### Update Bot Token
Updates the Telegram bot token for an existing bot.
**Endpoint:** `POST /v2/bots/{botid}/update-bot-token`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Request Body:**
```json
{
"token": "987654321:NEWtokenABCdefGHIjklMNO"
}
```
**Response:**
```json
{
"ok": true,
"result": "Token updated and bot started successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/update-bot-token \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
"token": "987654321:NEWtokenABCdefGHIjklMNO"
}'
```
**Note:** This endpoint automatically starts the bot after updating the token.
***
## Command Management Endpoints
### Create Command
Creates a new command for a bot.
**Endpoint:** `POST /v2/bots/{botid}/commands`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Request Body:**
```json
{
"command": "hello",
"code": "Api.sendMessage('Hello World!')"
}
```
**Response:**
```json
{
"ok": true,
"result": "Command created successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/commands \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
"command": "start",
"code": "Api.sendMessage(\"Welcome to my bot!\")"
}'
```
**Python Example:**
```python
command_code = """
Api.sendMessage("Welcome!")
Api.sendMessage("Available commands:")
Api.sendMessage("/help - Get help")
Api.sendMessage("/about - About bot")
"""
response = requests.post(
f"https://api.telebotstudio.com/v2/bots/{bot_id}/commands",
headers=headers,
json={"command": "start", "code": command_code}
)
```
***
### Get Command
Retrieves details of a specific command by name.
**Endpoint:** `POST /v2/bots/{botid}/command/by-name`
> **Live API Note:** Production endpoints accept `POST` with a JSON body `{"command_name": "..."}` (`GET` returns `405 Method Not Allowed`).

**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Request Body:**
```json
{
  "command_name": "start"
}
```
**Response:**
```json
{
  "ok": true,
  "command": {
    "command": "start",
    "code": "Api.sendMessage('Welcome!')",
    "is_pinned": false
  }
}
```
**Example:**
```bash
curl -X POST "https://api.telebotstudio.com/v2/bots/12345678/command/by-name" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command_name": "start"}'
```
***
### Update Command
Updates an existing command's code.
**Endpoint:** `POST /v2/bots/{botid}/command/by-name/update`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Request Body:**
```json
{
"command_name": "start",
"code": "Api.sendMessage('Updated welcome message!')"
}
```
**Response:**
```json
{
"ok": true,
"result": "Command updated successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/update \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
"command_name": "start",
"code": "Api.sendMessage(\"Updated!\")"
}'
```
***
### Delete Command
Deletes a command from the bot.
**Endpoint:** `POST /v2/bots/{botid}/command/by-name/delete`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Request Body:**
```json
{
"command_name": "old_command"
}
```
**Response:**
```json
{
"ok": true,
"result": "Command deleted successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/delete \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{"command_name": "old_command"}'
```
***
### List All Commands
Retrieves all commands for a bot.
**Endpoint:** `GET /v2/bots/{botid}/commands/list`
> **Live API Note:** Use `/commands/list` to retrieve all commands (`POST /v2/bots/{botid}/commands` creates commands).

**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Response:**
```json
{
  "ok": true,
  "commands": [
    {
      "command": "start",
      "code": "Api.sendMessage('Welcome!')",
      "is_pinned": false
    },
    {
      "command": "help",
      "code": "Api.sendMessage('Help menu')",
      "is_pinned": false
    }
  ]
}
```
**Example:**
```bash
curl -X GET https://api.telebotstudio.com/v2/bots/12345678/commands/list \
  -H "Authorization: Bearer YOUR_API_KEY"
```
***
## Command Name Encoding
For certain endpoints that require command names in the URL path or when working with special characters (including emojis, spaces, or slashes), command names must be properly encoded.
### When Encoding is Required
Command name encoding is **required** when:
* Command contains a forward slash (e.g., `/start`, `/help`)
* Command contains spaces (e.g., `user info`)
* Command contains special characters or emojis (e.g., `💰 Donate`, `🎉 Welcome`)
* Using URL path-based endpoints (legacy endpoints)
Command name encoding is **NOT required** when:
* Using the `/command/by-name` endpoints (recommended)
* Sending command name in request body
### Encoding Methods
**Method 1: Using `/command/by-name` Endpoints (Recommended)**
These endpoints accept command names directly in JSON payloads without encoding:
```bash
# Get command - no encoding needed
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command_name": "/start"}'

# Update command - no encoding needed
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/update \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "command_name": "/start",
    "code": "Api.sendMessage(\"Welcome!\")"
  }'

# Delete command - no encoding needed
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/command/by-name/delete \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command_name": "/start"}'
```
**Method 2: Base64 Encoding (For Legacy URL Path Endpoints)**
If you need to use URL path-based endpoints, encode command names using Base64:
### Encoding Process
1. **Original Command**: `/start`
2. **UTF-8 Encoding**: Convert to bytes
3. **Base64 Encoding**: `L3N0YXJ0`
4. **URL**: `/v2/bots/{botid}/commands/L3N0YXJ0`
### Encoding Examples Table
| Original Command | Base64 Encoded | Description |
| ---------------- | ------------------ | ------------------- |
| `/start` | `L3N0YXJ0` | Basic slash command |
| `/help` | `L2hlbHA=` | Help command |
| `/settings` | `L3NldHRpbmdz` | Settings command |
| `hello` | `aGVsbG8=` | No slash |
| `hello_world` | `aGVsbG9fd29ybGQ=` | Underscore |
| `user info` | `dXNlciBpbmZv` | Space character |
| `💰 Donate` | `8J+SsCBEb25hdGU=` | Emoji with space |
| `🎉 Welcome` | `8J+OiSBXZWxjb21l` | Emoji command |
### Code Examples for Encoding
**Python:**
```python
import base64


def encode_command(command_name):
    """Encode command name to Base64."""
    return base64.b64encode(command_name.encode('utf-8')).decode('ascii')


def decode_command(encoded):
    """Decode Base64 command name."""
    return base64.b64decode(encoded.encode('ascii')).decode('utf-8')


# Examples
print(encode_command('/start'))      # L3N0YXJ0
print(encode_command('/help'))       # L2hlbHA=
print(encode_command('💰 Donate'))   # 8J+SsCBEb25hdGU=

# Decode back
print(decode_command('L3N0YXJ0'))    # /start
```
**JavaScript/Node.js:**
```javascript
function encodeCommand(commandName) {
  return Buffer.from(commandName, 'utf8').toString('base64');
}

function decodeCommand(encoded) {
  return Buffer.from(encoded, 'base64').toString('utf8');
}

// Examples
console.log(encodeCommand('/start'));     // L3N0YXJ0
console.log(encodeCommand('/help'));      // L2hlbHA=
console.log(encodeCommand('💰 Donate'));  // 8J+SsCBEb25hdGU=
console.log(decodeCommand('L3N0YXJ0'));   // /start
```
**PHP:**
```php
<?php
function encodeCommand($commandName) {
    return base64_encode($commandName);
}

function decodeCommand($encoded) {
    return base64_decode($encoded);
}

// Examples
echo encodeCommand('/start');    // L3N0YXJ0
echo encodeCommand('/help');     // L2hlbHA=
echo encodeCommand('💰 Donate'); // 8J+SsCBEb25hdGU=
?>
```
**cURL Examples with Encoding:**
```bash
# Encode command name
COMMAND_NAME="/start"
ENCODED=$(echo -n "$COMMAND_NAME" | base64)
echo "Encoded: $ENCODED" # L3N0YXJ0
# Get command (using encoded name in URL path)
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/commands/$ENCODED" \
-H "Authorization: Bearer YOUR_API_KEY"
# For emoji commands
EMOJI_COMMAND="💰 Donate"
ENCODED_EMOJI=$(echo -n "$EMOJI_COMMAND" | base64)
curl -X GET "https://api.telebotstudio.com/v2/bots/12345678/commands/$ENCODED_EMOJI" \
-H "Authorization: Bearer YOUR_API_KEY"
```
### Comparison: Encoded vs Non-Encoded Endpoints
| Feature | `/command/by-name` (Recommended) | Legacy URL Path |
| ---------------------- | -------------------------------- | -------------------- |
| **Encoding Required** | ❌ No | ✅ Yes (Base64) |
| **Emoji Support** | ✅ Direct | ✅ Via encoding |
| **Space Support** | ✅ Direct | ✅ Via encoding |
| **Special Characters** | ✅ Direct | ✅ Via encoding |
| **Ease of Use** | ✅ Simple | ⚠️ Requires encoding |
| **URL Length** | ✅ Shorter | ⚠️ Longer |
| **Recommended** | ✅ Yes | ⚠️ Legacy only |
### Best Practices
1. **Use `/command/by-name` endpoints** for new integrations (no encoding needed)
2. **Use Base64 encoding** only for legacy URL path endpoints
3. **Always use UTF-8 encoding** before Base64 conversion
4. **Test with special characters** (emojis, spaces, Unicode) during development
5. **URL-encode the Base64 string** if your HTTP client doesn't do it automatically
### Complete Example with Encoding
**Python Complete Example:**
```python
import base64
import requests


class CommandManager:
    def __init__(self, api_key, bot_id):
        self.api_key = api_key
        self.bot_id = bot_id
        self.base_url = "https://api.telebotstudio.com/v2"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    # Method 1: No encoding (Recommended)
    def get_command_simple(self, command_name):
        """Get command without encoding."""
        response = requests.post(
            f"{self.base_url}/bots/{self.bot_id}/command/by-name",
            headers=self.headers,
            json={"command_name": command_name},
        )
        return response.json()

    def update_command_simple(self, command_name, code):
        """Update command without encoding."""
        response = requests.post(
            f"{self.base_url}/bots/{self.bot_id}/command/by-name/update",
            headers=self.headers,
            json={"command_name": command_name, "code": code},
        )
        return response.json()

    # Method 2: With encoding (Legacy)
    @staticmethod
    def encode_command(command_name):
        """Encode command name to Base64."""
        return base64.b64encode(command_name.encode("utf-8")).decode("ascii")

    def get_command_encoded(self, command_name):
        """Get command with Base64 encoding (legacy)."""
        encoded = self.encode_command(command_name)
        response = requests.get(
            f"{self.base_url}/bots/{self.bot_id}/commands/{encoded}",
            headers=self.headers,
        )
        return response.json()


# Usage
manager = CommandManager("YOUR_API_KEY", "12345678")

# Recommended approach - no encoding
result = manager.get_command_simple("/start")
manager.update_command_simple("/start", 'Api.sendMessage("Welcome!")')

# Works with emojis too
result = manager.get_command_simple("💰 Donate")
manager.update_command_simple("💰 Donate", 'Api.sendMessage("Thanks!")')

# Legacy approach - with encoding
result = manager.get_command_encoded("/start")
```
***
## Bot Control Endpoints
### Start Bot
Starts a bot by setting its webhook.
**Endpoint:** `POST /v2/bots/{botid}/start`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Response:**
```json
{
"ok": true,
"result": "Bot started successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/start \
-H "Authorization: Bearer YOUR_API_KEY"
```
***
### Stop Bot
Stops a bot by removing its webhook.
**Endpoint:** `POST /v2/bots/{botid}/stop`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Response:**
```json
{
"ok": true,
"result": "Bot stopped successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/stop \
-H "Authorization: Bearer YOUR_API_KEY"
```
***
### Restart Bot
Stops and starts a bot in one operation.
**Endpoint:** `POST /v2/bots/{botid}/restart`
**Authentication:** Required
**URL Parameters:**
* `botid` (Required): Bot identifier
**Response:**
```json
{
"ok": true,
"result": "Bot restarted successfully"
}
```
**Example:**
```bash
curl -X POST https://api.telebotstudio.com/v2/bots/12345678/restart \
-H "Authorization: Bearer YOUR_API_KEY"
```
***
## Error Responses
### Authentication Errors
**Missing Authentication:**
```json
{
"ok": false,
"result": "Authentication required"
}
```
**Invalid API Key:**
```json
{
"ok": false,
"result": "Invalid API key"
}
```
**Expired Token:**
```json
{
"ok": false,
"result": "Token has expired"
}
```
### Resource Errors
**Bot Not Found:**
```json
{
"ok": false,
"result": "Bot not found or not owned by you"
}
```
**Command Not Found:**
```json
{
"ok": false,
"result": "Command not found"
}
```
### Validation Errors
**Invalid Bot Token:**
```json
{
"ok": false,
"result": "Invalid bot token format"
}
```
**Missing Required Field:**
```json
{
"ok": false,
"result": "Bot token is required"
}
```
***
## Rate Limiting
**Limits:**
* 60 requests per minute per IP address
* 1000 requests per hour per API key
**Headers:**
* `X-RateLimit-Limit`: Maximum requests per window
* `X-RateLimit-Remaining`: Remaining requests
* `X-RateLimit-Reset`: UTC timestamp when limit resets
**Rate Limit Exceeded Response:**
```json
{
"ok": false,
"result": "Rate limit exceeded. Try again in 60 seconds."
}
```
***
## Code Examples
### Complete Bot Creation Workflow
**Python:**
```python
import requests


class TeleBotStudioAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.telebotstudio.com/v2"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def create_bot(self, bot_token):
        """Create a new bot."""
        response = requests.post(
            f"{self.base_url}/create-bot",
            headers=self.headers,
            json={"bot_token": bot_token},
        )
        return response.json()

    def create_command(self, bot_id, command_name, code):
        """Create a command."""
        response = requests.post(
            f"{self.base_url}/bots/{bot_id}/commands",
            headers=self.headers,
            json={"command": command_name, "code": code},
        )
        return response.json()

    def start_bot(self, bot_id):
        """Start a bot."""
        response = requests.post(
            f"{self.base_url}/bots/{bot_id}/start",
            headers=self.headers,
        )
        return response.json()


# Usage
api = TeleBotStudioAPI("YOUR_API_KEY")

# Create bot
result = api.create_bot("123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
bot_id = result["result"]["botid"]
print(f"Bot created: {bot_id}")

# Add /start command
start_code = 'Api.sendMessage("Welcome to my bot!")'
api.create_command(bot_id, "start", start_code)

# Add /help command
help_code = 'Api.sendMessage("Available commands:\\n/start - Start\\n/help - Help")'
api.create_command(bot_id, "help", help_code)

# Start bot
api.start_bot(bot_id)
print("Bot started successfully!")
```
***
**Node.js:**
```javascript
const axios = require('axios');

class TeleBotStudioAPI {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.telebotstudio.com/v2';
    this.headers = { Authorization: `Bearer ${apiKey}` };
  }

  async createBot(botToken) {
    const response = await axios.post(
      `${this.baseUrl}/create-bot`,
      { bot_token: botToken },
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

(async () => {
  const api = new TeleBotStudioAPI('YOUR_API_KEY');
  const result = await api.createBot('123456789:ABCdefGHIjklMNOpqrsTUVwxyz');
  const botId = result.result.botid;
  console.log(`Bot created: ${botId}`);

  await api.createCommand(botId, 'start', 'Api.sendMessage("Welcome!")');
  await api.createCommand(botId, 'help', 'Api.sendMessage("Help menu")');
  await api.startBot(botId);
  console.log('Bot started!');
})();
```
***
### Bulk Command Management
```python
def bulk_create_commands(api, bot_id, commands_dict):
    """Create multiple commands at once."""
    results = []
    for cmd_name, cmd_code in commands_dict.items():
        result = api.create_command(bot_id, cmd_name, cmd_code)
        results.append({
            "command": cmd_name,
            "success": result["ok"],
        })
    return results


commands = {
    "start": 'Api.sendMessage("Welcome to my bot!")',
    "help": 'Api.sendMessage("Help menu")',
    "about": 'Api.sendMessage("About this bot")',
    "settings": 'Api.sendMessage("Settings menu")',
}
results = bulk_create_commands(api, bot_id, commands)
print(f"Created {sum(1 for r in results if r['success'])} commands")
```
***
## Best Practices
### 1. Security
**Protect Your API Key:**
```python
# ❌ Wrong - Don't hardcode in source
api_key = "my_actual_api_key_12345"

# ✅ Correct - Use environment variables
import os

api_key = os.getenv("TELEBOT_API_KEY")
```
**Use HTTPS Only:**
```python
# ✅ Always use HTTPS
base_url = "https://api.telebotstudio.com/v2"
# ❌ Never use HTTP
# base_url = "http://telebotstudio.com/v2"
```
**Rotate API Keys Regularly:**
* Generate new API keys every 90 days
* Immediately revoke keys if compromised
* Use different keys for different applications
### 2. Error Handling
**Implement Robust Error Handling:**
```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper for API calls with error handling."""
    max_retries = 3
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            response = func(*args, **kwargs)
            if response["ok"]:
                return response
            print(f"API error: {response['result']}")
            return None
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    return None


result = safe_api_call(api.create_bot, "123456789:TOKEN")
```
### 3. Rate Limiting
**Respect Rate Limits:**
```python
import time


class RateLimitedAPI:
    def __init__(self, api_key, requests_per_minute=50):
        self.api = TeleBotStudioAPI(api_key)
        self.min_interval = 60 / requests_per_minute
        self.last_request = 0

    def _wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

    def create_command(self, *args, **kwargs):
        self._wait_if_needed()
        return self.api.create_command(*args, **kwargs)


limited_api = RateLimitedAPI("YOUR_API_KEY", requests_per_minute=50)
```
### 4. Logging
**Log All API Interactions:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="telebot_api.log",
)


def log_api_call(endpoint, method, response):
    """Log API call details."""
    logging.info(f"{method} {endpoint} - Status: {response.get('ok')}")
    if not response.get("ok"):
        logging.error(f"Error: {response.get('result')}")


response = api.create_bot(bot_token)
log_api_call("/v2/create-bot", "POST", response)
```
***
## Common Use Cases
### 1. Automated Bot Deployment
```python
def deploy_bot(api_key, bot_token, commands):
    """Complete bot deployment workflow."""
    api = TeleBotStudioAPI(api_key)
    print("Creating bot...")
    result = api.create_bot(bot_token)
    if not result["ok"]:
        print(f"Failed to create bot: {result['result']}")
        return False
    bot_id = result["result"]["botid"]
    print(f"Bot created with ID: {bot_id}")

    print("Adding commands...")
    for cmd_name, cmd_code in commands.items():
        result = api.create_command(bot_id, cmd_name, cmd_code)
        if result["ok"]:
            print(f" ✓ {cmd_name}")
        else:
            print(f" ✗ {cmd_name}: {result['result']}")

    print("Starting bot...")
    result = api.start_bot(bot_id)
    if result["ok"]:
        print("✓ Bot deployed successfully!")
        return True
    print(f"Failed to start bot: {result['result']}")
    return False


commands = {
    "start": 'Api.sendMessage("Welcome!")',
    "help": 'Api.sendMessage("Help menu")',
}
deploy_bot("YOUR_API_KEY", "BOT_TOKEN", commands)
```
### 2. Bot Backup and Restore
```python
def backup_bot(api, bot_id):
    """Backup all bot commands."""
    response = requests.get(
        f"{api.base_url}/bots/{bot_id}/commands/list",
        headers=api.headers,
    )
    if response.json()["ok"]:
        commands = response.json()["commands"]
        backup = {cmd["command"]: cmd["code"] for cmd in commands}
        with open(f"bot_{bot_id}_backup.json", "w") as f:
            json.dump(backup, f, indent=2)
        print(f"Backed up {len(backup)} commands")
        return backup
    return None


def restore_bot(api, bot_id, backup_file):
    """Restore commands from backup."""
    with open(backup_file) as f:
        commands = json.load(f)
    for cmd_name, cmd_code in commands.items():
        api.create_command(bot_id, cmd_name, cmd_code)
    print(f"Restored {len(commands)} commands")
```
***
## Support
For additional help:
* **Documentation:** https://help.telebotstudio.com
* **Platform Dashboard:** https://telebotstudio.com
* **Community Support:** https://t.me/TeleBotStudioChat 
***
## Changelog
### Version 2.0 (Current)
* ✅ Flexible authentication (JWT + API key)
* ✅ Simplified command management endpoints
* ✅ Enhanced error messages
* ✅ Rate limiting with headers
* ✅ CORS support
* ✅ Bot control endpoints (start/stop/restart)
***
**Last Updated:** 2025-11-02
*TeleBot Studio API v2 - Build, Deploy, Scale. Free Forever.*
