# TBS Language Reference
## Overview
TBS (TeleBot Syntax) is a Python-like programming language designed specifically for building Telegram bots on the TeleBot Studio platform. It provides a secure, efficient environment with built-in functions, objects, and libraries for creating powerful bot interactions.
### Key Features
* **No Import Statements**: All functionality is built-in - no import statements required or allowed
* **Python-like Syntax**: Familiar Python syntax for easy learning
* **Secure Execution**: Sandboxed environment with restricted access for safety
* **Built-in Objects**: Pre-configured objects for bot operations, user management, and data storage
* **Extensive Libraries**: Ready-to-use libraries for payments, blockchain, AI, and more
### Security and Restrictions
TBS operates in a sandboxed environment with the following security measures:
* **No `eval()` or `exec()`**: These functions are disabled to prevent arbitrary code execution
* **No System Access**: No access to `os`, `sys`, `subprocess`, or similar system modules
* **Controlled File Access**: Files accessible only through provided APIs
* **Isolated Execution**: Each bot runs in its own isolated environment
* **No Import Statements**: All required functionality is pre-loaded in the environment
These restrictions protect the platform infrastructure, prevent malicious code execution, and ensure bots cannot interfere with each other.
***
## Built-in Types and Functions
### Data Types
TBS supports the following Python data types:
| Type | Description | Example |
| ------- | --------------------- | ---------------------------- |
| `str` | String/text | `"Hello World"` |
| `int` | Integer number | `42` |
| `float` | Floating-point number | `3.14` |
| `bool` | Boolean value | `True`, `False` |
| `dict` | Dictionary/object | `{"name": "Bot", "id": 123}` |
| `list` | List/array | `[1, 2, 3, 4]` |
| `set` | Set (unique values) | `{1, 2, 3}` |
| `tuple` | Immutable sequence | `(1, 2, 3)` |
### Built-in Functions
| Function | Description | Example |
| ------------------------------ | ------------------------------------- | -------------------------------------------------------- |
| `abs(x)` | Returns absolute value | `abs(-5)` → `5` |
| `all(iterable)` | Returns True if all elements are true | `all([True, True, False])` → `False` |
| `any(iterable)` | Returns True if any element is true | `any([False, True, False])` → `True` |
| `bin(x)` | Converts integer to binary string | `bin(10)` → `'0b1010'` |
| `bool(x)` | Converts value to boolean | `bool(1)` → `True` |
| `callable(x)` | Checks if object is callable | `callable(len)` → `True` |
| `chr(i)` | Returns character from Unicode | `chr(65)` → `'A'` |
| `dict()` | Creates a dictionary | `dict(a=1, b=2)` |
| `divmod(a, b)` | Returns quotient and remainder | `divmod(10, 3)` → `(3, 1)` |
| `enumerate(iterable)` | Returns enumerated object | `list(enumerate(['a', 'b']))` → `[(0, 'a'), (1, 'b')]` |
| `filter(func, iterable)` | Filters iterable by function | `list(filter(lambda x: x > 0, [-1, 0, 1]))` → `[1]` |
| `float(x)` | Converts to floating-point | `float("3.14")` → `3.14` |
| `format(value, format_spec)` | Formats a value | `format(3.14159, '.2f')` → `'3.14'` |
| `getattr(obj, name)` | Gets object attribute | `getattr(obj, 'name')` |
| `hasattr(obj, name)` | Checks if attribute exists | `hasattr(obj, 'name')` |
| `hash(x)` | Returns hash value | `hash("hello")` |
| `hex(x)` | Converts integer to hex | `hex(255)` → `'0xff'` |
| `id(x)` | Returns object ID | `id(my_obj)` |
| `int(x)` | Converts to integer | `int("42")` → `42` |
| `isinstance(obj, type)` | Checks object type | `isinstance(5, int)` → `True` |
| `issubclass(class, classinfo)` | Checks subclass | `issubclass(bool, int)` → `True` |
| `iter(iterable)` | Returns iterator | `iter([1, 2, 3])` |
| `len(x)` | Returns length | `len([1, 2, 3])` → `3` |
| `list()` | Creates a list | `list((1, 2, 3))` → `[1, 2, 3]` |
| `map(func, iterable)` | Applies function to items | `list(map(str, [1, 2, 3]))` → `['1', '2', '3']` |
| `max(iterable)` | Returns maximum value | `max([1, 5, 3])` → `5` |
| `min(iterable)` | Returns minimum value | `min([1, 5, 3])` → `1` |
| `next(iterator)` | Gets next item from iterator | `next(iter([1, 2]))` → `1` |
| `oct(x)` | Converts integer to octal | `oct(8)` → `'0o10'` |
| `ord(c)` | Returns Unicode code point | `ord('A')` → `65` |
| `pow(x, y)` | Returns x to the power of y | `pow(2, 3)` → `8` |
| `range(start, stop, step)` | Generates number sequence | `list(range(5))` → `[0, 1, 2, 3, 4]` |
| `reversed(seq)` | Returns reversed iterator | `list(reversed([1, 2, 3]))` → `[3, 2, 1]` |
| `round(number, ndigits)` | Rounds to n digits | `round(3.14159, 2)` → `3.14` |
| `set()` | Creates a set | `set([1, 2, 2, 3])` → `{1, 2, 3}` |
| `slice(start, stop, step)` | Creates slice object | `slice(1, 5, 2)` |
| `sorted(iterable)` | Returns sorted list | `sorted([3, 1, 2])` → `[1, 2, 3]` |
| `str(x)` | Converts to string | `str(42)` → `"42"` |
| `sum(iterable)` | Returns sum of items | `sum([1, 2, 3])` → `6` |
| `tuple()` | Creates a tuple | `tuple([1, 2, 3])` → `(1, 2, 3)` |
| `type(x)` | Returns object type | `type(5)` → `` |
| `zip(iter1, iter2)` | Combines iterables | `list(zip([1, 2], ['a', 'b']))` → `[(1, 'a'), (2, 'b')]` |
***
## Global Variables
TBS provides several global variables automatically available in every command:
| Variable | Type | Description |
| ------------- | -------- | ------------------------------------------------------------------ |
| `msg` | `str` | Raw text content of the incoming message |
| `message` | `object` | Full Telegram update object with sender, chat, and message details |
| `u` | `str` | User ID of the current user interacting with the bot |
| `params` | `str` | Additional parameters from command (e.g., `/start referral_id`) |
| `options` | `dict` | Additional data passed to commands (webhook responses, etc.) |
| `update_type` | `str` | Type of current update (e.g., "message", "callback\_query") |
| `bot_id` | `str` | Unique identifier of the current bot |
| `bot_token` | `str` | Telegram Bot API token for the current bot |
### Update Type Values
The `update_type` variable can have these values:
* `"message"` - Regular text message
* `"callback_query"` - Inline keyboard button press
* `"inline_query"` - Inline query from user
* `"edited_message"` - Message was edited
* `"channel_post"` - Post in a channel
* `"my_chat_member"` - Bot's member status changed
* `"chat_member"` - Chat member status changed
***
## Core Objects
### Api Object
The `Api` object provides direct access to all Telegram Bot API methods. Use this for standard Telegram operations.
#### Message Sending Methods
| Method | Parameters | Description |
| ---------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `sendMessage` | `text` (required), `chat_id`, `parse_mode`, `reply_markup`, etc. | Sends a text message |
| `sendPhoto` | `photo` (required), `chat_id`, `caption`, `reply_markup`, etc. | Sends a photo |
| `sendAudio` | `audio` (required), `chat_id`, `caption`, `duration`, etc. | Sends an audio file |
| `sendDocument` | `document` (required), `chat_id`, `caption`, etc. | Sends a document |
| `sendVideo` | `video` (required), `chat_id`, `caption`, `duration`, etc. | Sends a video |
| `sendAnimation` | `animation` (required), `chat_id`, `caption`, etc. | Sends an animation (GIF) |
| `sendVoice` | `voice` (required), `chat_id`, `caption`, `duration`, etc. | Sends a voice message |
| `sendVideoNote` | `video_note` (required), `chat_id`, `length`, `duration`, etc. | Sends a video note |
| `sendLocation` | `latitude` (required), `longitude` (required), `chat_id`, etc. | Sends a location |
| `sendVenue` | `latitude` (required), `longitude` (required), `title` (required), `address` (required), `chat_id`, etc. | Sends a venue |
| `sendContact` | `phone_number` (required), `first_name` (required), `chat_id`, `last_name`, etc. | Sends a contact |
| `sendPoll` | `question` (required), `options` (required), `chat_id`, `is_anonymous`, etc. | Sends a poll |
| `sendDice` | `emoji`, `chat_id` | Sends an animated emoji (dice, darts, etc.) |
| `sendSticker` | `sticker` (required), `chat_id`, etc. | Sends a sticker |
| `sendMediaGroup` | `media` (required), `chat_id` | Sends multiple photos/videos as album |
**Example:**
```python
# Send a simple message
Api.sendMessage("Hello! Welcome to our bot!")
# Send a photo with caption
Api.sendPhoto(
photo="https://example.com/image.jpg",
caption="Check out this image!"
)
# Send a message with inline keyboard
keyboard = {
"inline_keyboard": [[
{"text": "Option 1", "callback_data": "opt1"},
{"text": "Option 2", "callback_data": "opt2"}
]]
}
Api.sendMessage(
text="Choose an option:",
reply_markup=keyboard
)
```
#### Message Editing Methods
| Method | Parameters | Description |
| ------------------------ | --------------------------------------------------------------------------------------------- | -------------------------------- |
| `editMessageText` | `text` (required), `message_id`, `chat_id`, `inline_message_id`, `parse_mode`, `reply_markup` | Edits text of a message |
| `editMessageCaption` | `caption`, `message_id`, `chat_id`, `inline_message_id`, `reply_markup` | Edits caption of a media message |
| `editMessageMedia` | `media` (required), `message_id`, `chat_id`, `inline_message_id`, `reply_markup` | Edits media in a message |
| `editMessageReplyMarkup` | `reply_markup`, `message_id`, `chat_id`, `inline_message_id` | Edits reply markup of a message |
| `deleteMessage` | `message_id` (required), `chat_id` | Deletes a message |
| `deleteMessages` | `message_ids` (required), `chat_id` | Deletes multiple messages |
**Example:**
```python
# Edit a message
Api.editMessageText(
text="Updated message text",
message_id=123456
)
# Delete a message
Api.deleteMessage(message_id=123456)
```
#### Chat Management Methods
| Method | Parameters | Description |
| --------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------ |
| `getChat` | `chat_id` | Gets information about a chat |
| `getChatAdministrators` | `chat_id` | Gets list of chat administrators |
| `getChatMember` | `chat_id` (required), `user_id` (required) | Gets information about a chat member |
| `getChatMemberCount` | `chat_id` | Gets number of members in a chat |
| `banChatMember` | `chat_id` (required), `user_id` (required), `until_date`, `revoke_messages` | Bans a user from a chat |
| `unbanChatMember` | `chat_id` (required), `user_id` (required), `only_if_banned` | Unbans a user from a chat |
| `restrictChatMember` | `chat_id` (required), `user_id` (required), `permissions` (required), `until_date` | Restricts a chat member |
| `promoteChatMember` | `chat_id` (required), `user_id` (required), permissions... | Promotes a chat member to admin |
| `setChatAdministratorCustomTitle` | `chat_id` (required), `user_id` (required), `custom_title` (required) | Sets custom title for admin |
| `setChatPhoto` | `photo` (required), `chat_id` | Sets chat photo |
| `deleteChatPhoto` | `chat_id` | Deletes chat photo |
| `setChatTitle` | `title` (required), `chat_id` | Sets chat title |
| `setChatDescription` | `description`, `chat_id` | Sets chat description |
| `pinChatMessage` | `message_id` (required), `chat_id`, `disable_notification` | Pins a message |
| `unpinChatMessage` | `message_id`, `chat_id` | Unpins a message |
| `unpinAllChatMessages` | `chat_id` | Unpins all messages |
| `leaveChat` | `chat_id` | Makes bot leave a chat |
**Example:**
```python
# Get chat information
chat_info = Api.getChat(chat_id=-1001234567890)
Api.sendMessage(f"Chat title: {chat_info.title}")
# Ban a user
Api.banChatMember(
chat_id=-1001234567890,
user_id=123456789
)
# Pin a message
Api.pinChatMessage(message_id=message.message_id)
```
#### Forum Topic Methods
| Method | Parameters | Description |
| ----------------------------------- | ------------------------------------------------------------------------- | -------------------------------------- |
| `getForumTopicIconStickers` | None | Gets list of forum topic icon stickers |
| `createForumTopic` | `name` (required), `chat_id`, `icon_color`, `icon_custom_emoji_id` | Creates a forum topic |
| `editForumTopic` | `message_thread_id` (required), `chat_id`, `name`, `icon_custom_emoji_id` | Edits forum topic |
| `closeForumTopic` | `message_thread_id` (required), `chat_id` | Closes forum topic |
| `reopenForumTopic` | `message_thread_id` (required), `chat_id` | Reopens forum topic |
| `deleteForumTopic` | `message_thread_id` (required), `chat_id` | Deletes forum topic |
| `unpinAllForumTopicMessages` | `message_thread_id` (required), `chat_id` | Unpins all messages in topic |
| `editGeneralForumTopic` | `name` (required), `chat_id` | Edits general forum topic name |
| `closeGeneralForumTopic` | `chat_id` | Closes general forum topic |
| `reopenGeneralForumTopic` | `chat_id` | Reopens general forum topic |
| `hideGeneralForumTopic` | `chat_id` | Hides general forum topic |
| `unhideGeneralForumTopic` | `chat_id` | Unhides general forum topic |
| `unpinAllGeneralForumTopicMessages` | `chat_id` | Unpins all messages in general topic |
**Example:**
```python
# Create a forum topic
topic = Api.createForumTopic(
name="General Discussion",
icon_color=0x6FB9F0
)
# Close a topic
Api.closeForumTopic(message_thread_id=topic.message_thread_id)
```
#### Sticker Methods
| Method | Parameters | Description |
| ----------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `sendSticker` | `sticker` (required), `chat_id`, `emoji`, `reply_markup` | Sends a sticker |
| `getStickerSet` | `name` (required) | Gets sticker set |
| `getCustomEmojiStickers` | `custom_emoji_ids` (required) | Gets custom emoji stickers |
| `uploadStickerFile` | `user_id` (required), `sticker` (required), `sticker_format` (required) | Uploads sticker file |
| `createNewStickerSet` | `user_id` (required), `name` (required), `title` (required), `stickers` (required), `sticker_type` | Creates new sticker set |
| `addStickerToSet` | `user_id` (required), `name` (required), `sticker` (required) | Adds sticker to set |
| `setStickerPositionInSet` | `sticker` (required), `position` (required) | Sets sticker position |
| `deleteStickerFromSet` | `sticker` (required) | Deletes sticker from set |
| `replaceStickerInSet` | `user_id` (required), `name` (required), `old_sticker` (required), `sticker` (required) | Replaces sticker in set |
| `setStickerEmojiList` | `sticker` (required), `emoji_list` (required) | Sets sticker emoji list |
| `setStickerKeywords` | `sticker` (required), `keywords` | Sets sticker keywords |
| `setStickerMaskPosition` | `sticker` (required), `mask_position` | Sets sticker mask position |
| `setStickerSetTitle` | `name` (required), `title` (required) | Sets sticker set title |
| `setStickerSetThumbnail` | `name` (required), `user_id` (required), `thumbnail` | Sets sticker set thumbnail |
| `setCustomEmojiStickerSetThumbnail` | `name` (required), `custom_emoji_id` | Sets custom emoji sticker thumbnail |
| `deleteStickerSet` | `name` (required) | Deletes sticker set |
**Example:**
```python
# Send a sticker
Api.sendSticker(
sticker="CAACAgIAAxkBAAEMXYZl...",
emoji="😊"
)
# Get sticker set
sticker_set = Api.getStickerSet(name="my_sticker_pack")
```
#### Inline Mode Methods
| Method | Parameters | Description |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `answerInlineQuery` | `inline_query_id` (required), `results` (required), `cache_time`, `is_personal`, `next_offset` | Answers inline query |
| `answerWebAppQuery` | `web_app_query_id` (required), `result` (required) | Answers web app query |
| `savePreparedInlineMessage` | `user_id` (required), `result` (required), `allow_user_chats`, `allow_bot_chats`, `allow_group_chats`, `allow_channel_chats` | Saves prepared inline message |
**Example:**
```python
# Answer inline query
results = [
{
"type": "article",
"id": "1",
"title": "Result 1",
"input_message_content": {"message_text": "Content 1"}
}
]
Api.answerInlineQuery(
inline_query_id=message.id,
results=results
)
```
#### Payment Methods
| Method | Parameters | Description |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `sendInvoice` | `title` (required), `description` (required), `payload` (required), `currency` (required), `prices` (required), `provider_token`, `chat_id` | Sends invoice |
| `createInvoiceLink` | `title` (required), `description` (required), `payload` (required), `currency` (required), `prices` (required), `provider_token` | Creates invoice link |
| `answerShippingQuery` | `shipping_query_id` (required), `ok` (required), `shipping_options`, `error_message` | Answers shipping query |
| `answerPreCheckoutQuery` | `pre_checkout_query_id` (required), `ok` (required), `error_message` | Answers pre-checkout query |
| `getStarTransactions` | `offset`, `limit` | Gets star transactions |
| `refundStarPayment` | `user_id` (required), `telegram_payment_charge_id` (required) | Refunds star payment |
**Example:**
```python
# Send invoice
Api.sendInvoice(
title="Premium Subscription",
description="One month of premium features",
payload="premium_sub_1m",
currency="USD",
prices=[{"label": "Premium", "amount": 999}]
)
# Refund star payment
Api.refundStarPayment(
user_id=123456789,
telegram_payment_charge_id="charge_id"
)
```
#### Game Methods
| Method | Parameters | Description |
| ------------------- | -------------------------------------------------------------------------------------------------- | --------------------- |
| `sendGame` | `game_short_name` (required), `chat_id`, `reply_markup` | Sends a game |
| `setGameScore` | `user_id` (required), `score` (required), `chat_id`, `message_id`, `force`, `disable_edit_message` | Sets game score |
| `getGameHighScores` | `user_id` (required), `chat_id`, `message_id` | Gets game high scores |
**Example:**
```python
# Send game
Api.sendGame(game_short_name="my_game")
# Set score
Api.setGameScore(
user_id=123456789,
score=1500
)
```
#### Other Methods
| Method | Parameters | Description |
| --------------------------------- | --------------------------------------------------------------------- | ------------------------------------------- |
| `forwardMessage` | `message_id` (required), `from_chat_id` (required), `chat_id` | Forwards a message |
| `forwardMessages` | `message_ids` (required), `from_chat_id` (required), `chat_id` | Forwards multiple messages |
| `copyMessage` | `message_id` (required), `from_chat_id` (required), `chat_id` | Copies a message |
| `copyMessages` | `message_ids` (required), `from_chat_id` (required), `chat_id` | Copies multiple messages |
| `sendChatAction` | `action` (required), `chat_id` | Sends chat action (typing, uploading, etc.) |
| `setMessageReaction` | `message_id` (required), `reaction`, `is_big`, `chat_id` | Sets message reaction |
| `getUserProfilePhotos` | `user_id` (required), `offset`, `limit` | Gets user's profile photos |
| `getFile` | `file_id` (required) | Gets file information |
| `banChatSenderChat` | `sender_chat_id` (required), `chat_id` | Bans channel in chat |
| `unbanChatSenderChat` | `sender_chat_id` (required), `chat_id` | Unbans channel in chat |
| `getUserChatBoosts` | `chat_id` (required), `user_id` (required) | Gets user's boosts in chat |
| `getBusinessConnection` | `business_connection_id` (required) | Gets business connection info |
| `answerCallbackQuery` | `callback_query_id`, `text`, `show_alert`, `url` | Answers callback query |
| `setMyCommands` | `commands` (required), `scope`, `language_code` | Sets bot commands |
| `deleteMyCommands` | `scope`, `language_code` | Deletes bot commands |
| `getMyCommands` | `scope`, `language_code` | Gets bot commands |
| `setMyName` | `name`, `language_code` | Sets bot name |
| `getMyName` | `language_code` | Gets bot name |
| `setMyDescription` | `description`, `language_code` | Sets bot description |
| `getMyDescription` | `language_code` | Gets bot description |
| `setMyShortDescription` | `short_description`, `language_code` | Sets bot short description |
| `getMyShortDescription` | `language_code` | Gets bot short description |
| `setChatMenuButton` | `menu_button`, `chat_id` | Sets chat menu button |
| `getChatMenuButton` | `chat_id` | Gets chat menu button |
| `setMyDefaultAdministratorRights` | `rights`, `for_channels` | Sets default admin rights |
| `getMyDefaultAdministratorRights` | `for_channels` | Gets default admin rights |
| `setPassportDataErrors` | `user_id` (required), `errors` (required) | Sets passport data errors |
| `sendGift` | `user_id` (required), `gift_id` (required), `text`, `text_parse_mode` | Sends a gift |
| `getMe` | None | Gets bot information |
| `logOut` | None | Logs out from cloud |
| `close` | None | Closes bot instance |
| `getWebhookInfo` | None | Gets webhook information |
**Example:**
```python
# Show typing indicator
Api.sendChatAction(action="typing")
# Answer callback query with alert
Api.answerCallbackQuery(
callback_query_id=message.id,
text="Button clicked!",
show_alert=True
)
# Get bot info
bot_info = Api.getMe()
Api.sendMessage(f"Bot username: @{bot_info.username}")
# Set message reaction
Api.setMessageReaction(
message_id=123,
reaction=[{"type": "emoji", "emoji": "👍"}]
)
# Send gift
Api.sendGift(
user_id=123456789,
gift_id="premium_gift_1"
)
```
### Bot Object
The `Bot` object provides platform-specific methods for advanced bot operations, data management, broadcasting, and scheduling.
#### Platform Methods
| Method | Parameters | Description |
| ----------------- | --------------------------------------------------------------------------- | --------------------------------------------------- |
| `run` | `command` (required), `options` | Executes another command |
| `scheduleCommand` | `command` (required), `seconds` (required), `options` | Schedules command execution |
| `waitForInput` | `command` (required) | Waits for user's next message and passes to command |
| `sendBroadcast` | `code`, `command`, `function`, `callback_url`, `warnings`, \*\*kwargs | Sends message to all bot users |
| `cancelBroadcast` | `broadcast_id` (required) | Cancels a running broadcast |
| `listBroadcasts` | None | Lists all broadcasts for the bot |
| `broadcastStatus` | `broadcast_id` (required) | Gets status of a broadcast |
| `pauseBroadcast` | `broadcast_id` (required) | Pauses a running broadcast |
| `getInfo` | `bot_id`, `api_key` | Gets bot information |
| `start` | `bot_token` (required) | Starts the bot (sets webhook) |
| `stop` | None | Stops the bot (removes webhook) |
| `getStatus` | None | Gets bot running status |
| `transfer` | `email` (required), `bot_id` (required), `bot_token`, `run_now` | Transfers bot to another user |
| `createCaptcha` | `user_id` | Creates a captcha for user verification |
| `verifyCaptcha` | `user_id` (required), `code` (required) | Verifies a captcha code |
| `sendCaptcha` | `user_id` | Sends captcha image to user |
| `randomID` | None | Generates random 8-character ID |
| `uniqueID` | None | Generates unique ID based on timestamp |
| `errorID` | None | Generates error tracking ID |
| `webhookURL` | `command` (required), `user_id`, `chat_id`, \*\*options | Generates webhook URL for command |
| `paymentURL` | `amount` (required), `currency`, `description`, `success_url`, `cancel_url` | Generates payment URL |
**Example:**
```python
# Execute another command
Bot.run("welcome_message")
# Schedule a command to run in 5 minutes
Bot.scheduleCommand("reminder", 300)
# Wait for user input
Bot.waitForInput("process_name")
# Get bot status
status = Bot.getStatus()
if status["is_running"]:
Api.sendMessage("Bot is online!")
```
#### Data Management Methods
| Method | Parameters | Description |
| -------------------- | -------------------------------------------- | ----------------------------- |
| `storeData` | `name` (required), `data` (required), `user` | Stores data for a user |
| `fetchData` | `name` (required), `user` | Retrieves stored data |
| `removeData` | `name` (required), `user` | Deletes stored data |
| `exportData` | `name` (required), `user`, `output_format` | Exports data as file |
| `exportAllData` | `name`, `output_format` | Exports all user data |
| `exportBotUsersFile` | `output_format` | Exports list of all bot users |
**Example:**
```python
# Store user data
Bot.storeData("user_score", 100)
# Retrieve user data
score = Bot.fetchData("user_score")
Api.sendMessage(f"Your score: {score}")
# Delete user data
Bot.removeData("temp_data")
# Export data as file
file = Bot.exportData("user_preferences", output_format="json")
Api.sendDocument(file)
```
#### Resource Management
| Method | Parameters | Description |
| ------ | -------------------------- | --------------------------------- |
| `res` | `resource_name` (required) | Gets/manages a bot-level resource |
**Example:**
```python
# Create/access a global bot resource
total_uses = Bot.res("total_uses")
total_uses.add(1)
current = total_uses.value()
Api.sendMessage(f"Bot used {current} times")
```
#### Broadcasting
The `sendBroadcast` method allows sending messages to all bot users efficiently.
**Parameters:**
* `code`: Custom TBS code to execute for each user
* `command`: Name of command to execute
* `function`: Telegram function to use (e.g., "send\_message")
* `callback_url`: URL to call after broadcast completes
* `warnings`: Whether to show warnings
* `**kwargs`: Additional parameters for the function
**Example:**
```python
# Broadcast using a function
Bot.sendBroadcast(
function="send_message",
text="🎉 New feature alert! Check out our latest updates."
)
# Broadcast using a command
Bot.sendBroadcast(command="send_promotion")
# Broadcast with custom code
Bot.sendBroadcast(
code='''
name = User.fetchData("name") or "User"
Api.sendMessage(f"Hello {name}! Here's your daily update.")
'''
)
```
### User Object
The `User` object manages user-specific data and resources.
#### Data Methods
| Method | Parameters | Description |
| ---------------- | -------------------------------------------- | ----------------------------------------- |
| `storeData` | `name` (required), `data` (required), `user` | Stores data for current or specified user |
| `fetchData` | `name` (required), `user` | Retrieves user data |
| `removeData` | `name` (required), `user` | Deletes user data |
| `exportData` | `name` (required), `user`, `output_format` | Exports user data as file |
| `exportAllData` | `name`, `output_format` | Exports all data for user |
| `exportUserData` | `user` (required), `output_format` | Exports all data for specific user |
**Example:**
```python
# Store user preference
User.storeData("language", "en")
# Get user data
lang = User.fetchData("language")
if lang == "en":
Api.sendMessage("Hello!")
else:
Api.sendMessage("Hola!")
# Store complex data
user_profile = {
"name": "John",
"age": 25,
"interests": ["coding", "gaming"]
}
User.storeData("profile", user_profile)
```
#### Resource Methods
| Method | Parameters | Description |
| ------- | --------------------------------------------- | ---------------------------------------- |
| `res` | `resource_name` (required) | Gets/manages a resource for current user |
| `resOf` | `resource_name` (required), `user` (required) | Gets/manages a resource for another user |
**Example:**
```python
# Manage user points
points = User.res("points")
points.add(10)
Api.sendMessage(f"You earned 10 points! Total: {points.value()}")
# Check another user's resource
other_points = User.resOf("points", "123456789")
Api.sendMessage(f"User has {other_points.value()} points")
```
### Account Object
The `Account` object manages account-level data that persists across all bots owned by the account.
#### Data Methods
| Method | Parameters | Description |
| --------------- | ------------------------------------ | ---------------------------- |
| `storeData` | `name` (required), `data` (required) | Stores account-level data |
| `fetchData` | `name` (required) | Retrieves account data |
| `removeData` | `name` (required) | Deletes account data |
| `exportData` | `name` (required), `output_format` | Exports account data as file |
| `exportAllData` | `name`, `output_format` | Exports all account data |
**Example:**
```python
# Store account settings
Account.storeData("theme", "dark")
# Get account data
theme = Account.fetchData("theme")
Api.sendMessage(f"Your theme: {theme}")
```
#### Bot Management Methods
| Method | Parameters | Description |
| ----------- | ---------------------------- | ------------------------------------- |
| `botStats` | `botid` (required) | Gets statistics for a specific bot |
| `botUsage` | `botid` (required), `period` | Gets usage statistics |
| `botsStats` | None | Gets statistics for all bots |
| `stats` | None | Gets comprehensive account statistics |
**Example:**
```python
# Get bot statistics
stats = Account.botStats("1234567")
Api.sendMessage(f"Bot has {stats['total_users']} users")
# Get all bots stats
all_stats = Account.botsStats()
Api.sendMessage(f"You have {all_stats['total_bots']} bots")
```
#### User Management Methods
| Method | Parameters | Description |
| ----------------------- | ------------------------ | ---------------------------------- |
| `banUser` | `user_id` (required) | Blocks a user from using the bot |
| `unbanUser` | `user_id` (required) | Unblocks a previously blocked user |
| `bannedUsers` | `botid` (required) | Gets list of blocked users |
| `exportBannedUsersFile` | `botid`, `output_format` | Exports blocked users as file |
**Example:**
```python
# Block a user
result = Account.banUser("123456789")
Api.sendMessage("User has been blocked")
# Get blocked users
blocked = Account.bannedUsers("1234567")
Api.sendMessage(f"Blocked users: {len(blocked['result'])}")
```
#### Resource Methods
| Method | Parameters | Description |
| ------ | -------------------------- | ----------------------------------- |
| `res` | `resource_name` (required) | Gets/manages account-level resource |
**Example:**
```python
# Account-level resource (shared across all bots)
subscription = Account.res("subscription_points")
subscription.add(100)
Api.sendMessage(f"Account points: {subscription.value()}")
```
### Admin Object
The `Admin` object provides administrative operations on resources.
#### Resource Methods
| Method | Parameters | Description |
| ------ | -------------------------- | ------------------------------ |
| `res` | `resource_name` (required) | Gets admin resource operations |
The Admin resource object has additional methods:
* `exportAllData(limit)`: Exports top users by resource value
* `removeAllData(user)`: Clears all resources for all or specific user
* `fetchAllResourcesOfUser(user_id, output_format)`: Exports all resources for a user
**Example:**
```python
# Get admin access to a resource
admin_points = Admin.res("points")
# Get top 10 users by points
top_users = admin_points.exportAllData(10)
# Clear all points for a user
admin_points.removeAllDataOfUser("123456789")
# Get all resources for a user
user_resources = admin_points.fetchAllResourcesOfUser("123456789", "json")
Api.sendDocument(user_resources)
```
***
## Library Reference (Lib)
TBS provides extensive libraries for various functionalities. Access them through the `Lib` namespace (no import needed).
### Lib.Random
Generates random values for various purposes.
| Method | Parameters | Description | Example |
| --------- | ---------------------------------- | ------------------- | ------------------------------ |
| `integer` | `min` (required), `max` (required) | Random integer | `Lib.Random.integer(1, 100)` |
| `string` | `length` (required) | Random string | `Lib.Random.string(10)` |
| `decimal` | `min` (required), `max` (required) | Random float | `Lib.Random.decimal(0.0, 1.0)` |
| `ascii` | `length` (required) | Random ASCII string | `Lib.Random.ascii(8)` |
**Example:**
```python
# Random number for game
dice = Lib.Random.integer(1, 6)
Api.sendMessage(f"You rolled: {dice}")
# Random code generation
code = Lib.Random.string(8)
User.storeData("verification_code", code)
Api.sendMessage(f"Your code: {code}")
```
### Lib.DateTime
Handles date and time operations.
| Method | Parameters | Description | Example |
| ---------- | ------------------------- | ------------------------ | -------------------------------------- |
| `utcnow` | None | Current UTC datetime | `Lib.DateTime.utcnow()` |
| `date_now` | None | Current UTC date | `Lib.DateTime.date_now()` |
| `time` | None | Current UNIX timestamp | `Lib.DateTime.time()` |
| `now` | `timezone_str` (required) | Current time in timezone | `Lib.DateTime.now("America/New_York")` |
**Example:**
```python
# Get current time
current = Lib.DateTime.utcnow()
Api.sendMessage(f"Current time: {current}")
# Get timestamp
timestamp = Lib.DateTime.time()
User.storeData("last_seen", timestamp)
# Get time in specific timezone
ny_time = Lib.DateTime.now("America/New_York")
Api.sendMessage(f"NYC time: {ny_time}")
```
### Lib.CSV
Manages CSV files for data storage.
| Method | Parameters | Description |
| ------- | --------------------- | ------------------------- |
| `Table` | `filename` (required) | Creates CSV table handler |
#### Table Methods
| Method | Parameters | Description |
| ------------ | -------------------------------------------- | ---------------------------- |
| `create` | `headers` (required) | Creates CSV with headers |
| `insert` | `row` (required) | Adds a row to CSV |
| `update` | `row_index` (required), `new_row` (required) | Updates a row |
| `delete` | `row_index` (required) | Deletes a row |
| `get` | None | Gets all rows |
| `row` | `row_index` (required) | Gets specific row |
| `find` | `**criteria` | Finds rows matching criteria |
| `count` | None | Returns number of rows |
| `toString` | None | Exports CSV as string |
| `fromString` | `csv_string` (required) | Imports CSV from string |
**Example:**
```python
# Create CSV table
csv = Lib.CSV.Table("leaderboard.csv")
# Create with headers
csv.create(["name", "score", "date"])
# Insert row
csv.insert({"name": "Alice", "score": 100, "date": "2024-01-01"})
# Update row
csv.update(0, {"score": 150})
# Get specific row
row = csv.row(0)
Api.sendMessage(f"{row['name']}: {row['score']}")
# Find rows
high_scorers = csv.find(score=100)
# Get all data
all_data = csv.get()
for row in all_data:
Api.sendMessage(f"{row['name']}: {row['score']}")
# Count rows
total = csv.count()
Api.sendMessage(f"Total entries: {total}")
# Delete row
csv.delete(0)
```
### Lib.EVM
Handles Ethereum Virtual Machine (EVM) blockchain operations for 31+ networks.
#### Supported Networks
Ethereum, BSC, Polygon, Avalanche, Fantom, Arbitrum, Optimism, Base, ZKSync, Scroll, Linea, and many more.
| Method | Parameters | Description |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `generateKey` | None | Generates new private key |
| `storeKey` | `private_key` (required) | Stores private key |
| `sendCoin` | `value` (required), `to` (required), `rpc_url`, `private_key`, `network`, `retry`, `estimate_gas` | Sends native coin (ETH, BNB, etc.) |
| `sendToken` | `value` (required), `to` (required), `contract_address` (required), `rpc_url`, `private_key`, `network`, `retry`, `estimate_gas` | Sends ERC-20 tokens |
| `networks` | None | Gets list of supported networks |
| `getRPC` | `network` (required) | Gets default RPC for network |
**Example:**
```python
# Generate wallet
private_key = Lib.EVM.generateKey()
Lib.EVM.storeKey(private_key)
# Send ETH
tx_hash = Lib.EVM.sendCoin(
value=0.1,
to="0xRecipientAddress",
network="ethereum",
estimate_gas=True
)
Api.sendMessage(f"Transaction: {tx_hash}")
# Send ERC-20 tokens
token_tx = Lib.EVM.sendToken(
value=100,
to="0xRecipientAddress",
contract_address="0xTokenContract",
network="polygon",
estimate_gas=True
)
```
### Lib.TON
Handles The Open Network (TON) blockchain operations.
#### Wallet Methods
| Method | Parameters | Description |
| -------------- | ---------------------- | ---------------------- |
| `createWallet` | None | Creates new TON wallet |
| `storeKey` | `mnemonics` (required) | Stores wallet mnemonic |
| `getAddress` | `mnemonics` | Gets wallet address |
#### Transaction Methods
| Method | Parameters | Description |
| -------------- | --------------------------------------------------------------------------------------------------------- | ------------------------ |
| `balance` | `address` (required), `api_key`, `endpoint` | Gets TON balance |
| `send` | `to_address` (required), `amount` (required), `comment`, `mnemonics`, `api_key`, `endpoint`, `is_testnet` | Sends TON |
| `transactions` | `address` (required), `api_key`, `endpoint`, `limit` | Gets recent transactions |
#### TON Connect Methods
| Method | Parameters | Description |
| ---------------- | ------------------------------------------------------------------------------------- | -------------------------------------- |
| `connectSession` | `user_id` (required), `expiry_seconds` | Creates wallet connection session |
| `verifySession` | `session_id` (required) | Verifies wallet connection |
| `requestPayment` | `to_address` (required), `amount` (required), `comment`, `callback_url`, `return_url` | Requests payment from connected wallet |
#### Jetton Methods
| Method | Parameters | Description |
| -------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `tokenInfo` | `jetton_master_address` (required), `api_key`, `endpoint` | Gets token metadata |
| `tokenBalance` | `owner_address` (required), `jetton_master_address` (required), `api_key`, `endpoint` | Gets token balance |
| `requestToken` | `to_address` (required), `jetton_master_address` (required), `amount` (required), `comment`, `callback_url`, `return_url` | Requests token transfer |
**Example:**
```python
# Create wallet
wallet = Lib.TON.createWallet()
Api.sendMessage(f"Address: {wallet['address']}")
Api.sendMessage(f"Mnemonic: {wallet['mnemonic']}")
# Check balance
balance = Lib.TON.balance("EQD...")
Api.sendMessage(f"Balance: {balance} TON")
# Send TON
Lib.TON.send(
to_address="EQD...",
amount=0.5,
comment="Payment for service"
)
```
### Lib.AI
Unified AI library supporting multiple providers.
| Method | Parameters | Description |
| -------- | ----------------------------------------------------- | ----------------- |
| `client` | `provider` (required), `apiKey` (required), `baseUrl` | Creates AI client |
**Supported Providers:**
* `"openai"` - OpenAI GPT models
* `"gemini"` - Google Gemini models
#### AI Client Methods
| Method | Parameters | Description |
| ----------------- | ---------------------------------------------------------------------- | --------------------------- |
| `chat` | `model` (required), `messages` (required), `temperature`, `max_tokens` | Creates chat completion |
| `createAssistant` | `model` (required), `name`, `instructions`, `tools` | Creates AI assistant |
| `createThread` | None | Creates conversation thread |
| `addMessage` | `thread_id` (required), `role` (required), `content` (required) | Adds message to thread |
| `run` | `thread_id` (required), `assistant_id` (required) | Runs assistant on thread |
| `getStatus` | `thread_id` (required), `run_id` (required) | Gets run status |
| `getMessages` | `thread_id` (required), `limit` | Gets thread messages |
**Example:**
```python
# Using OpenAI
openai = Lib.AI.client(
provider="openai",
apiKey="your-api-key"
)
response = openai.chat(
model="gpt-4o",
messages=[
{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": msg}
]
)
Api.sendMessage(response["choices"][0]["message"]["content"])
# Using Gemini
gemini = Lib.AI.client(
provider="gemini",
apiKey="your-gemini-key"
)
response = gemini.chat(
model="gemini-2.0-flash",
messages=[
{"role": "user", "content": msg}
]
)
Api.sendMessage(response["choices"][0]["message"]["content"])
```
### Lib.Oxapay
Integrates with Oxapay payment system for cryptocurrency payments.
| Method | Parameters | Description |
| -------- | ----------------------------- | ------------------------------ |
| `client` | `merchant_api_key` (required) | Creates Oxapay client |
| `post` | `merchant_api_key` (required) | Legacy method (same as client) |
#### Oxapay Client Methods
Once you create an Oxapay client, you have access to these methods:
| Method | Parameters | Required/Optional | Description |
| ----------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------- |
| `createAddress` | `network`, `to_currency`, `auto_withdrawal`, `callback_url`, `email`, `order_id`, `description` | `network` required, others optional | Generates static address for payments |
| `createInvoice` | `amount`, `currency`, `network`, `callback_url`, `email`, `order_id`, `description`, `return_url` | `amount`, `currency` required | Creates payment invoice |
| `invoice` | `track_id` | Required | Gets invoice status |
| `payout` | `address`, `amount`, `currency`, `network`, `callback_url`, `description` | `address`, `amount`, `currency` required | Creates payout (withdrawal) |
| `payoutStatus` | `track_id` | Required | Checks payout status |
| `payoutHistory` | `from_date`, `to_date`, `page` | All optional | Gets payout history |
| `revokeAddress` | `address` | Required | Revokes/disables static address |
| `history` | `from_date`, `to_date`, `page` | All optional | Gets payment history |
| `whitelist` | None | None | Gets whitelisted addresses |
| `addWhitelist` | `address`, `currency`, `network` | `address`, `currency` required | Adds address to whitelist |
| `removeWhitelist` | `address`, `currency`, `network` | `address`, `currency` required | Removes address from whitelist |
| `info` | None | None | Gets merchant account info |
| `rate` | `from_currency`, `to_currency` | Both optional | Gets exchange rates |
| `allowance` | None | None | Gets merchant balance |
**Example:**
```python
# Create client
oxapay = Lib.Oxapay.client("your_merchant_api_key")
# Create static address
address_result = oxapay.createAddress(
network="BSC",
callback_url="https://yoursite.com/callback"
)
Api.sendMessage(f"Send payment to: {address_result['data']['address']}")
# Create invoice
invoice = oxapay.createInvoice(
amount=50,
currency="USDT",
network="TRC20",
description="Premium subscription",
return_url="https://yourbot.com/success"
)
Api.sendMessage(f"Pay here: {invoice['data']['payment_url']}")
# Check invoice status
status = oxapay.invoice(track_id="123456")
if status['status'] == "Paid":
Api.sendMessage("Payment confirmed!")
# Create payout
payout_result = oxapay.payout(
address="0xRecipientAddress",
amount=25,
currency="USDT",
network="BSC"
)
# Get payment history
history = oxapay.history(
from_date="2024-01-01",
to_date="2024-12-31",
page=1
)
# Manage whitelist
oxapay.addWhitelist(
address="0xTrustedAddress",
currency="USDT",
network="BSC"
)
# Get account info
account = oxapay.info()
Api.sendMessage(f"Balance: {account['data']['balance']}")
# Get exchange rates
rates = oxapay.rate(from_currency="BTC", to_currency="USDT")
```
### Lib.Crypto
Handles cryptocurrency conversions and pricing.
| Method | Parameters | Description |
| ----------- | ------------------------------------------------------------------------- | ------------------------------ |
| `convert` | `amount` (required), `from_currency` (required), `to_currency` (required) | Converts between currencies |
| `get_price` | `currency` (required) | Gets current price of currency |
**Example:**
```python
# Convert BTC to USD
usd_value = Lib.Crypto.convert(0.1, "BTC", "USD")
Api.sendMessage(f"0.1 BTC = ${usd_value}")
# Get current price
btc_price = Lib.Crypto.get_price("BTC")
Api.sendMessage(f"BTC price: ${btc_price}")
```
### Lib.Webhook
Generates webhook URLs for external integrations.
| Method | Parameters | Description |
| ----------- | ---------------------------------------------------------------------------- | --------------------- |
| `getUrlFor` | `command` (required), `user_id`, `chat_id`, `bot_id`, `api_key`, \*\*options | Generates webhook URL |
**Example:**
```python
# Create webhook URL
webhook = Lib.Webhook.getUrlFor(
command="process_payment",
user_id=u
)
Api.sendMessage(f"Webhook: {webhook}")
```
***
### Utility Functions
| Function | Description | Example |
| ------------------ | --------------------------------------------- | ------------------------------------------------- |
| `bunchify(dict)` | Converts dict to object with attribute access | `obj = bunchify({"name": "Bot"})` then `obj.name` |
| `isNumeric(value)` | Checks if value is numeric | `isNumeric("123")` → `True` |
**Example:**
```python
# Convert dict to object
data = {"name": "Alice", "score": 100}
obj = bunchify(data)
Api.sendMessage(f"{obj.name} scored {obj.score}")
# Check if numeric
if isNumeric(msg):
number = int(msg)
Api.sendMessage(f"You entered: {number}")
```
***
## Standard Libraries
### time Module
| Function | Description | Example |
| --------------------- | --------------------------------- | --------------- |
| `time.time()` | Gets current UNIX timestamp | `time.time()` |
| `time.sleep(seconds)` | Pauses execution (max 10 seconds) | `time.sleep(2)` |
**Example:**
```python
# Get timestamp
timestamp = time.time()
User.storeData("last_active", timestamp)
# Pause execution
Api.sendMessage("Processing...")
time.sleep(3)
Api.sendMessage("Done!")
```
### base64 Module
| Function | Description | Example |
| -------------------------- | ----------------------- | ------------------------------ |
| `base64.b64encode(bytes)` | Encodes bytes to base64 | `base64.b64encode(b"hello")` |
| `base64.b64decode(string)` | Decodes base64 to bytes | `base64.b64decode("aGVsbG8=")` |
**Example:**
```python
# Encode text
encoded = base64.b64encode(b"secret message")
Api.sendMessage(f"Encoded: {encoded}")
# Decode text
decoded = base64.b64decode(encoded)
Api.sendMessage(f"Decoded: {decoded}")
```
### hashlib Module
| Function | Description | Example |
| ----------------------- | -------------------- | ------------------------------------- |
| `hashlib.sha256(bytes)` | Creates SHA-256 hash | `hashlib.sha256(b"text").hexdigest()` |
| `hashlib.md5(bytes)` | Creates MD5 hash | `hashlib.md5(b"text").hexdigest()` |
**Example:**
```python
# Hash password
password = "mypassword"
hashed = hashlib.sha256(password.encode()).hexdigest()
User.storeData("password_hash", hashed)
# Verify password
input_hash = hashlib.sha256(msg.encode()).hexdigest()
stored_hash = User.fetchData("password_hash")
if input_hash == stored_hash:
Api.sendMessage("Login successful!")
```
### regex/re Module
| Function | Description | Example |
| ---------------------------------- | ------------------------ | --------------------------------------------------- |
| `regex.match(pattern, string)` | Matches pattern at start | `regex.match(r"^\d+$", "123")` |
| `regex.search(pattern, string)` | Searches for pattern | `regex.search(r"@\w+", "Hello @user")` |
| `regex.findall(pattern, string)` | Finds all matches | `regex.findall(r"\d+", "I have 2 cats and 3 dogs")` |
| `regex.sub(pattern, repl, string)` | Replaces pattern | `regex.sub(r"\d", "X", "abc123")` |
**Example:**
```python
# Validate email
if regex.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", msg):
Api.sendMessage("Valid email!")
else:
Api.sendMessage("Invalid email")
# Extract mentions
mentions = regex.findall(r"@(\w+)", msg)
Api.sendMessage(f"Mentioned: {', '.join(mentions)}")
```
***
## Request Module
The `Request` module provides HTTP client functionality for making API calls.
### Methods
| Method | Parameters | Description |
| ---------------- | ------------------------------------------------------------------ | ----------------------- |
| `Request.get` | `url` (required), `headers`, `timeout`, \*\*kwargs | Performs GET request |
| `Request.post` | `url` (required), `data`, `json`, `headers`, `timeout`, \*\*kwargs | Performs POST request |
| `Request.put` | `url` (required), `data`, `json`, `headers`, `timeout`, \*\*kwargs | Performs PUT request |
| `Request.delete` | `url` (required), `headers`, `timeout`, \*\*kwargs | Performs DELETE request |
| `Request.patch` | `url` (required), `data`, `json`, `headers`, `timeout`, \*\*kwargs | Performs PATCH request |
### Response Object
The response object has these properties:
* `status_code`: HTTP status code
* `text`: Response text
* `content`: Response bytes
* `headers`: Response headers
* `json()`: Parse response as JSON
* `ok`: True if status code is 2xx
**Example:**
```python
# GET request
response = Request.get("https://api.example.com/data")
if response.ok:
data = response.json()
Api.sendMessage(f"Data: {data}")
# POST request with JSON
response = Request.post(
url="https://api.example.com/submit",
json={"name": "John", "email": "john@example.com"},
headers={"Authorization": "Bearer token123"}
)
if response.status_code == 200:
Api.sendMessage("Submitted successfully!")
```
***
## Control Flow
### StopExecution
Use `raise StopExecution()` to immediately stop command execution and optionally return a value.
**Example:**
```python
# Stop execution conditionally
if not User.fetchData("registered"):
Api.sendMessage("Please register first!")
raise StopExecution()
# Continue with registered users only
Api.sendMessage("Welcome back!")
# Stop with return value
result = {"status": "success", "user_id": u}
raise StopExecution(result)
```
***
## Resource Management
Resources are numeric values that can be tracked per-user, globally for a bot, or at account level.
### Resource Object Methods
All resource objects (from `User.res()`, `Bot.res()`, `Account.res()`, `Admin.res()`) have these methods:
| Method | Description | Example |
| ------------- | -------------------- | ----------------- |
| `value()` | Gets current value | `points.value()` |
| `add(amount)` | Adds to value | `points.add(10)` |
| `cut(amount)` | Subtracts from value | `points.cut(5)` |
| `set(amount)` | Sets specific value | `points.set(100)` |
| `reset()` | Resets to zero | `points.reset()` |
**Example:**
```python
# User-specific points
points = User.res("points")
points.add(10)
current = points.value()
if current >= 100:
Api.sendMessage("Congratulations! You reached 100 points!")
# Redeem points
points.cut(100)
User.storeData("premium", True)
# Global bot counter
visitors = Bot.res("total_visitors")
visitors.add(1)
Api.sendMessage(f"You are visitor #{int(visitors.value())}")
# Account-level resource
subscription = Account.res("subscription_credits")
if subscription.value() > 0:
subscription.cut(1)
# Provide premium feature
else:
Api.sendMessage("Please purchase more credits")
```
***
## Best Practices
### 1. Data Storage
**Do:**
```python
# Store structured data
user_data = {
"name": msg,
"joined": time.time(),
"status": "active"
}
User.storeData("profile", user_data)
```
**Don't:**
```python
# Don't store sensitive data unencrypted
User.storeData("password", msg) # Bad!
# Use hashing instead
User.storeData("password_hash", hashlib.sha256(msg.encode()).hexdigest())
```
### 2. Error Handling
**Do:**
```python
# Handle potential errors
data = User.fetchData("settings")
if data is None:
# Set defaults
data = {"language": "en", "notifications": True}
User.storeData("settings", data)
```
**Don't:**
```python
# Don't assume data exists
settings = User.fetchData("settings")
lang = settings["language"] # Can crash if settings is None
```
### 3. Resource Management
**Do:**
```python
# Use resources for numeric tracking
points = User.res("points")
points.add(10)
# Check before deducting
if points.value() >= 50:
points.cut(50)
Api.sendMessage("Purchase successful!")
else:
Api.sendMessage("Insufficient points")
```
**Don't:**
```python
# Don't use data storage for simple counters
count = User.fetchData("count") or 0
count += 1
User.storeData("count", count) # Use resources instead!
```
### 4. Command Chaining
**Do:**
```python
# Use command chaining for multi-step processes
Api.sendMessage("What's your name?")
Bot.waitForInput("get_age")
# In get_age command:
name = msg
User.storeData("name", name)
Api.sendMessage("What's your age?")
Bot.waitForInput("finish_registration")
```
### 5. Broadcasting
**Do:**
```python
# Use broadcasts for announcements
Bot.sendBroadcast(
code='''
name = User.fetchData("name") or "User"
Api.sendMessage(f"Hi {name}! Check out our new features.")
'''
)
```
**Don't:**
```python
# Don't try to manually loop through all users
# This won't work and is inefficient
users = Bot.exportBotUsersFile() # Don't do this for broadcasting
```
### 6. API Method Usage
**Do:**
```python
# Use Api for Telegram operations
Api.sendMessage("Hello!")
Api.sendPhoto(
photo="https://example.com/image.jpg",
caption="Check this out!"
)
```
**Don't:**
```python
# Don't mix Bot and Api unnecessarily
# Api is for Telegram API methods
# Bot is for platform-specific features
```
***
## Common Patterns
### Registration Flow
```python
# /start command
if params:
User.storeData("referrer", params)
if not User.fetchData("registered"):
Api.sendMessage("Welcome! What's your name?")
Bot.waitForInput("register_name")
raise StopExecution()
Api.sendMessage("Welcome back!")
# register_name command
name = msg
User.storeData("name", name)
Api.sendMessage("Great! What's your email?")
Bot.waitForInput("register_email")
# register_email command
email = msg
if regex.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
User.storeData("email", email)
User.storeData("registered", True)
# Reward referrer
referrer = User.fetchData("referrer")
if referrer:
ref_points = User.resOf("points", referrer)
ref_points.add(10)
Api.sendMessage("Registration complete! 🎉")
else:
Api.sendMessage("Invalid email. Try again:")
Bot.waitForInput("register_email")
```
### Points System
```python
# Award points
points = User.res("points")
points.add(10)
Api.sendMessage(f"You earned 10 points! Total: {int(points.value())}")
# Check and redeem
points = User.res("points")
current = points.value()
if msg == "/redeem":
if current >= 100:
points.cut(100)
Api.sendMessage("Redeemed 100 points for premium access!")
User.storeData("premium", True)
else:
Api.sendMessage(f"Need 100 points. You have {int(current)}")
```
### Quiz System
```python
# Start quiz
questions = [
{"q": "What is 2+2?", "a": "4"},
{"q": "Capital of France?", "a": "Paris"},
{"q": "Largest ocean?", "a": "Pacific"}
]
User.storeData("quiz_questions", questions)
User.storeData("quiz_index", 0)
User.res("quiz_score").reset()
Api.sendMessage(questions[0]["q"])
Bot.waitForInput("quiz_answer")
# quiz_answer command
questions = User.fetchData("quiz_questions")
index = User.fetchData("quiz_index")
score = User.res("quiz_score")
if msg.lower() == questions[index]["a"].lower():
score.add(1)
Api.sendMessage("Correct! ✅")
else:
Api.sendMessage(f"Wrong! The answer was: {questions[index]['a']}")
index += 1
User.storeData("quiz_index", index)
if index < len(questions):
Api.sendMessage(questions[index]["q"])
Bot.waitForInput("quiz_answer")
else:
final_score = int(score.value())
Api.sendMessage(f"Quiz complete! Your score: {final_score}/{len(questions)}")
```
### Payment Processing
```python
# /buy command
amount = 10.00
currency = "USD"
# Create payment URL
payment_url = Bot.paymentURL(
amount=amount,
currency=currency,
description="Premium subscription",
success_url="https://t.me/yourbot?start=payment_success",
cancel_url="https://t.me/yourbot?start=payment_cancel"
)
keyboard = {
"inline_keyboard": [[
{"text": "Pay $10", "url": payment_url}
]]
}
Api.sendMessage("Click to complete payment:", reply_markup=keyboard)
# Payment success handler
if params == "payment_success":
User.storeData("premium", True)
User.storeData("premium_until", time.time() + (30 * 86400)) # 30 days
Api.sendMessage("Payment successful! Premium activated.")
```
### Scheduled Reminders
```python
# /remind command
Api.sendMessage("What should I remind you about?")
Bot.waitForInput("reminder_text")
# reminder_text command
reminder = msg
User.storeData("reminder_text", reminder)
Api.sendMessage("In how many minutes?")
Bot.waitForInput("reminder_time")
# reminder_time command
if isNumeric(msg):
minutes = int(msg)
seconds = minutes * 60
reminder = User.fetchData("reminder_text")
# Schedule the reminder
Bot.scheduleCommand("send_reminder", seconds)
Api.sendMessage(f"Reminder set for {minutes} minutes!")
else:
Api.sendMessage("Please enter a number:")
Bot.waitForInput("reminder_time")
# send_reminder command
reminder = User.fetchData("reminder_text")
Api.sendMessage(f"⏰ Reminder: {reminder}")
```
***
## Troubleshooting
### Common Issues
1. **"NameError: name 'X' is not defined"**
* You're trying to use a variable or function that doesn't exist
* Check spelling and make sure you've defined it
* Remember: no import statements are needed or allowed
2. **"KeyError: 'key'"**
* Trying to access a dictionary key that doesn't exist
* Use `.get()` method: `data.get("key", default_value)`
3. **"TypeError: 'NoneType' object is not subscriptable"**
* Trying to access elements of None (usually from fetchData)
* Always check if data exists before using it
4. **"AttributeError: 'X' object has no attribute 'Y'"**
* Trying to access a method/attribute that doesn't exist
* Check the object type and available methods
### Debug Tips
```python
# Check what data exists
data = User.fetchData("profile")
Api.sendMessage(f"Profile data: {data}")
# Check variable types
Api.sendMessage(f"Type: {type(msg)}, Value: {msg}")
# Log resource values
points = User.res("points")
Api.sendMessage(f"Points: {points.value()}")
# Check update type
Api.sendMessage(f"Update type: {update_type}")
```
***
## Utility Objects
TBS provides utility objects for common operations with clean method interfaces.
### JSON Object
The `JSON` object handles JSON encoding and decoding operations.
| Method | Description | Example |
| --------------------- | ------------------------------ | --------------------------------- |
| `JSON.encode(obj)` | Converts object to JSON string | `JSON.encode({"name": "Bot"})` |
| `JSON.decode(string)` | Parses JSON string to object | `JSON.decode('{"key": "value"}')` |
| `JSON.dumps(obj)` | Same as encode (alias) | `JSON.dumps(data)` |
| `JSON.parse(string)` | Same as decode (alias) | `JSON.parse(json_str)` |
**Example:**
```python
# Convert to JSON
data = {"username": "john_doe", "score": 150}
json_string = JSON.encode(data)
User.storeData("user_json", json_string)
# Parse JSON
stored = User.fetchData("user_json")
parsed = JSON.decode(stored)
Api.sendMessage(f"User: {parsed['username']}, Score: {parsed['score']}")
```
### URL Object
The `URL` object handles URL encoding and query string operations.
| Method | Description | Example |
| ----------------------- | --------------------------- | ----------------------------- |
| `URL.encode(text)` | URL-encodes a string | `URL.encode("hello world")` |
| `URL.decode(text)` | URL-decodes a string | `URL.decode("hello%20world")` |
| `URL.parseQuery(query)` | Parses query string to dict | `URL.parseQuery("a=1&b=2")` |
**Example:**
```python
# Encode for URL
search_term = "bot development"
encoded = URL.encode(search_term)
url = f"https://api.example.com/search?q={encoded}"
# Decode from URL
encoded_text = "hello%20world%21"
decoded = URL.decode(encoded_text)
Api.sendMessage(decoded) # "hello world!"
# Parse query string
query = "user=123&action=buy&item=premium"
params = URL.parseQuery(query)
Api.sendMessage(f"User {params['user']} wants to {params['action']} {params['item']}")
```
### Hash Object
The `Hash` object provides hashing functions for security and data integrity.
| Method | Description | Example |
| ------------------- | ------------------- | ----------------------- |
| `Hash.md5(text)` | Creates MD5 hash | `Hash.md5("password")` |
| `Hash.sha1(text)` | Creates SHA1 hash | `Hash.sha1("data")` |
| `Hash.sha256(text)` | Creates SHA256 hash | `Hash.sha256("secure")` |
**Example:**
```python
# Hash password for storage
password = msg
hashed = Hash.sha256(password)
User.storeData("password_hash", hashed)
# Verify password
input_password = msg
input_hash = Hash.sha256(input_password)
stored_hash = User.fetchData("password_hash")
if input_hash == stored_hash:
Api.sendMessage("✅ Login successful!")
else:
Api.sendMessage("❌ Invalid password")
# Generate unique ID
user_id = str(u)
unique_token = Hash.md5(user_id + str(time.time()))
Api.sendMessage(f"Your token: {unique_token}")
```
***
## Additional Resources
### Official Documentation
* TeleBot Studio Website: https://telebotstudio.com
* Telegram Bot API: https://core.telegram.org/bots/api
### Getting Help
* Check the FAQ section in your TeleBot Studio dashboard
* Review example bots in the platform
* Test your code with small incremental changes
***
*This documentation covers TBS (TeleBot Syntax). For the latest updates, always check the official TeleBot Studio platform.*
