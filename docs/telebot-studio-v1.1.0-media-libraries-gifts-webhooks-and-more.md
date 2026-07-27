> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/telebot-studio-v1.1.0-media-libraries-gifts-webhooks-and-more.md).
# TeleBot Studio v1.1.0 — Media Libraries, Gifts, Webhooks & More
\*TeleBot Studio Documentation — Changelog\*
\*Platform v1.1.0 · Telegram Bot API 10.1 · Released July 2026\*
This is TeleBot Studio's first major update since launch — and it's a big one. This release adds full image editing and computer vision libraries, a complete cryptographic toolkit, Telegram Gifts support, a synchronous webhook response system, long-running HTTP request support, and a long list of quality-of-life improvements across the dashboard.
Everything below is available immediately in the TPY sandbox — no imports, no setup, just start calling the new methods.
\*\*\*
## What's New
### 🖼️ Image Editing — `Lib.PIL`
A complete image editing toolkit, built on Pillow. Load an image, transform it, draw on it, and send it — all in-memory, no file system access needed.
| Method                                                                       | Purpose                                            |
| ---------------------------------------------------------------------------- | -------------------------------------------------- |
| `openFromBytes` / `toBytes`                                                  | Load an image from bytes, export it back out       |
| `createImage` / `createGradient`                                             | Generate a blank canvas or a gradient from scratch |
| `resize` / `crop` / `rotate` / `flip`                                        | Basic transforms                                   |
| `adjustBrightness` / `adjustContrast` / `adjustColor` / `adjustSharpness`    | Fine-tune an image                                 |
| `applyFilter` / `invert`                                                     | Blur, sharpen, grayscale, emboss, and more         |
| `composite` / `paste` / `blend` / `addBorder` / `addWatermark` / `applyMask` | Combine and layer images                           |
| `drawText` / `drawRectangle` / `drawCircle` / `drawLine`                     | Draw directly onto an image                        |
| `convertMode` / `splitChannels` / `mergeChannels` / `getSize`                | Work with color channels and dimensions            |
```python
# Download an image, add a watermark, and send it back
resp = Request.get("https://example.com/photo.jpg")
img = Lib.PIL.openFromBytes(resp.content)
img = Lib.PIL.drawText(img, "© My Bot", (10, 10), color=(255, 255, 255))
Bot.sendPhoto(photo=Lib.PIL.toBytes(img, format="PNG"))
```
📖 See the full [TBS Media Libraries (PIL & CV) Documentation](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation) for every parameter and more examples.
### 📷 Computer Vision — `Lib.CV`
A second, OpenCV-based image library for more advanced processing — including real face detection.
| Method                                                            | Purpose                                  |
| ----------------------------------------------------------------- | ---------------------------------------- |
| `readImage` / `toBytes` / `createBlank`                           | Load, export, and create images          |
| `resize` / `rotate` / `perspectiveTransform`                      | Geometric transforms                     |
| `convertColor` / `threshold` / `adaptiveThreshold`                | Color space and thresholding             |
| `applyFilter` / `detectEdges` / `morphOperations` / `blendImages` | Filters and effects                      |
| `drawText` / `drawRectangle` / `findContours` / `drawContours`    | Drawing and shape detection              |
| `detectFaces` / `drawFaces`                                       | Real face detection, with bounding boxes |
```python
img = Lib.CV.readImage(resp.content)
faces = Lib.CV.detectFaces(img)
img = Lib.CV.drawFaces(img, faces)
Bot.sendPhoto(photo=Lib.CV.toBytes(img))
```
📖 See the full [TBS Media Libraries (PIL & CV) Documentation](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation) for every parameter and more examples.
### 🔐 Cryptography — `Lib.Security`
A full cryptographic toolkit for signature verification, encryption, and hashing — commonly needed for payment webhook verification and secure data storage.
| Method                                      | Purpose                                                      |
| ------------------------------------------- | ------------------------------------------------------------ |
| `signHMAC` / `verifyHMAC`                   | HMAC signing and verification (SHA-256, SHA-512, MD5)        |
| `verifyEd25519`                             | Ed25519 signature verification                               |
| `verifyPaymentGatewayWebhook`               | Convenience wrapper for verifying payment webhook signatures |
| `generateKey` / `encryptAES` / `decryptAES` | AES encryption, powered by Fernet                            |
| `hashSHA256` / `hashSHA512` / `hashMD5`     | One-way hashing                                              |
```python
signature = Lib.Security.signHMAC(secret\_key, payload)
if Lib.Security.verifyHMAC(secret\_key, payload, signature):
    Bot.sendMessage(text="Signature verified ✅")
```
📖 See the full [TBS Libraries Reference](https://help.telebotstudio.com/tbs-libraries) for every parameter and more examples.
### 🎁 Telegram Gifts — `Lib.TeleGifts`
Send Telegram gifts (paid in Stars) to any user — not limited to Premium accounts. Comes with a built-in catalog and full send history.
| Method                                                     | Purpose                                           |
| ---------------------------------------------------------- | ------------------------------------------------- |
| `getGiftCatalog` / `getGiftByKey` / `getGiftById`          | Browse the gift catalog                           |
| `getGiftsByCategory` / `searchGifts` / `getGiftPriceRange` | Filter and search gifts                           |
| `sendGift` / `sendGiftById`                                | Send a gift to a user                             |
| `getGiftHistory` / `getGiftStats`                          | Track every gift sent, with success/failure stats |
| `setGiftSetting` / `getGiftSetting` / `getAllGiftSettings` | Store your own gift-related settings              |
```python
gift = Lib.TeleGifts.getGiftByKey("rose")
result = Lib.TeleGifts.sendGift(user\_id=u, gift\_key="rose", message="Thanks for joining!")
if result.ok:
    Bot.sendMessage(text="Gift sent! 🌹")
```
📖 See the full [TBS Libraries Reference](https://help.telebotstudio.com/tbs-libraries) for every parameter and more examples.
### 🎲 Expanded `Lib.Random`
Eleven new methods, on top of the existing `integer`, `string`, `decimal`, and `ascii`:
`hex`, `bytes`, `uuid`, `password`, `choice`, `sample`, `shuffle`, `weightedChoice`, `boolean`, `range`, `gaussian`
```python
winner = Lib.Random.weightedChoice(["Common", "Rare", "Legendary"], weights=[70, 25, 5])
```
📖 See the full [TBS Libraries Reference](https://help.telebotstudio.com/tbs-libraries) for parameter details on each method.
### ⛓️ Wallet Balances — `Lib.EVM`
Check native and token balances directly, without needing a separate blockchain explorer call.
| Method              | Purpose                                                |
| ------------------- | ------------------------------------------------------ |
| `fetchBalance`      | Native coin balance for any address                    |
| `fetchTokenBalance` | ERC-20 token balance, with automatic decimal detection |
📖 See the [EVM Library Documentation](https://help.telebotstudio.com/evm-library-documentation) for supported networks and full parameter details.
### 💎 TON Improvements — `Lib.TON`
| Method                        | Purpose                                                                 |
| ----------------------------- | ----------------------------------------------------------------------- |
| `get\_jetton\_wallet\_address`   | Resolve a Jetton wallet address directly, without a full balance lookup |
| `register\_ton\_connect\_wallet` | Finalize a TON Connect session once a wallet approves the connection    |
📖 See the [TON Library Documentation](https://help.telebotstudio.com/ton-library-documentation) for the full TON Connect flow.
### 🔁 Webhook Result Sync
External HTTP calls that trigger your bot via a webhook URL can now get a \*\*real response back in the same request\*\* — no second callback URL needed.
```python
# Inside a webhook-triggered command
result = {"status": "verified", "user\_id": u}
Bot.setWebhookResponse(result)
```
The external caller's original HTTP request receives `{"ok": true, "result": {"status": "verified", "user\_id": "..."}}` directly. Also available as `Api.setWebhookResponse` on the low-level object.
### ⏱️ Long-Running HTTP Requests
`Request.get` / `.post` / `.put` / `.delete` / `.patch` now support requests that take longer than 120 seconds, via a `fallback\_command`:
```python
result = Request.get(
    "https://slow-api.example.com/data",
    timeout=200,
    fallback\_command="handle\_result"
)
# Returns immediately: {"task\_id": "...", "status": "processing", ...}
# "handle\_result" is triggered later with the real response in options.\*
```
Requests are also now protected by an SSRF guard (blocking internal/reserved network addresses) and a real, enforced size limit — not just a header check.
### 📡 Webhook Context — `options.headers` and `options.ip`
Commands triggered via a webhook URL can now read the caller's request headers and IP address:
```python
Bot.sendMessage(text="Caller IP: " + str(options.ip))
Bot.sendMessage(text="Custom header: " + str(options.headers.get("X-Custom-Header")))
```
### ✅ Multi-Channel Membership Checks
`CheckMembership` now accepts a list of channels, requiring membership in all of them:
```python
if CheckMembership(["channel\_one", "channel\_two"], u):
    Bot.sendMessage(text="You've joined both channels!")
```
Genuine errors (bad channel name, bot not an admin) now raise a clear error instead of silently returning the same result as "not joined."
### 📢 Broadcast Control
Broadcast limits have also been increased: up to \*\*3 simultaneous broadcasts per bot\*\* (up from 2), and \*\*5,000 simultaneous broadcasts platform-wide\*\* (up from 1,000).
Four new methods give you finer control over running broadcasts:
```python
# Get live progress of a running broadcast
progress = Bot.broadcastProgress(broadcast\_id)
# Adjust sending speed on the fly
Bot.updateBroadcastSpeed(broadcast\_id, speed=15)
# Permanently stop a broadcast (keeps its record and stats, unlike cancelBroadcast)
Bot.stopBroadcast(broadcast\_id)
# Re-run a previous broadcast with the same content
Bot.sendCloneBroadcast(broadcast\_id)
```
📖 See the full [Broadcast Function Documentation](https://help.telebotstudio.com/broadcast-function) for every parameter and more examples.
### 🗓️ Command Scheduling Improvements
`Bot.scheduleCommand` now returns a real task ID, and two new methods give you full control over scheduled commands:
```python
job = Bot.scheduleCommand(3600, "send\_reminder")
# later:
Bot.cancelScheduledCommand(job.id)
# or clear everything for a user, or the whole bot:
Bot.resetScheduledCommands(user\_id=u)
```
📖 See the full [Advanced Scheduling Techniques Documentation](https://help.telebotstudio.com/advanced-features#advanced-scheduling-techniques) for every parameter and more examples.
### 🤖 Bot Cloning
```python
result = Account.cloneBot(botid, new\_token="123456:ABC-DEF...")
```
Clones a bot's commands and environment variables (with values) into a fresh bot. Bot data is intentionally not copied.
### ⏳ Longer Execution Time
Commands can now run for up to \*\*160 seconds\*\*, up from 120.
📖 Full details on every object and method above are available in the [TBS Language Reference](https://help.telebotstudio.com/tbs-language-reference).
\*\*\*
## New Telegram Bot API Support
Alongside TBS-specific additions, this update brings full support for Telegram Bot API 8.0 through 10.1 — the entire range of newer methods are callable directly through the `Api`/`Bot` object, exactly like any other Telegram method.
### 🎁 Gifts & Stars
| Method                     | Description                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `sendGift`                 | Send a Telegram Gift (Stars) to a user or channel chat — also available at a higher level via `Lib.TeleGifts` |
| `getAvailableGifts`        | Retrieve the current live gift catalog directly from Telegram                                                 |
| `getUserGifts`             | List the gifts a user has received                                                                            |
| `giftPremiumSubscription`  | Gift a Telegram Premium subscription to a user                                                                |
| `convertGiftToStars`       | Convert a received gift into Stars                                                                            |
| `upgradeGift`              | Upgrade a regular gift to its unique/collectible version                                                      |
| `transferGift`             | Transfer an owned gift to another user                                                                        |
| `getMyStarBalance`         | Get the bot's own current Stars balance                                                                       |
| `getStarTransactions`      | Retrieve the bot's Stars transaction history                                                                  |
| `refundStarPayment`        | Refund a Stars payment                                                                                        |
| `editUserStarSubscription` | Modify a user's Stars subscription                                                                            |
### 💬 Rich Messages & Media
| Method                                     | Description                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| `sendRichMessage` / `sendRichMessageDraft` | Send rich-formatted messages beyond standard text/HTML formatting           |
| `sendLivePhoto`                            | Send Telegram's live photo format (a short video paired with a still image) |
```python
Bot.sendLivePhoto(live\_photo=video\_bytes, photo=photo\_bytes)
```
### 🏢 Business Accounts
| Method                                                                            | Description                                                      |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `getBusinessConnection`                                                           | Retrieve a business account connection                           |
| `readBusinessMessage`                                                             | Mark an incoming message as read on behalf of a business account |
| `setBusinessAccountName` / `setBusinessAccountUsername` / `setBusinessAccountBio` | Update a managed business account's profile                      |
| `setBusinessAccountProfilePhoto` / `removeBusinessAccountProfilePhoto`            | Manage a business account's profile photo                        |
| `setBusinessAccountGiftSettings`                                                  | Configure gift settings for a business account                   |
| `getBusinessAccountStarBalance` / `transferBusinessAccountStars`                  | Manage a business account's Stars balance                        |
### 📖 Stories
| Method                                    | Description                                                    |
| ----------------------------------------- | -------------------------------------------------------------- |
| `postStory` / `editStory` / `deleteStory` | Post, edit, and delete stories on behalf of a business account |
### ✅ Checklists & Suggested Posts
| Method                                          | Description                             |
| ----------------------------------------------- | --------------------------------------- |
| `sendChecklist` / `editMessageChecklist`        | Send and edit interactive checklists    |
| `approveSuggestedPost` / `declineSuggestedPost` | Respond to suggested posts in a channel |
### 🛡️ Verification & Reactions
| Method                                                | Description                        |
| ----------------------------------------------------- | ---------------------------------- |
| `verifyUser` / `verifyChat`                           | Apply Telegram verification badges |
| `removeUserVerification` / `removeChatVerification`   | Remove verification badges         |
| `deleteMessageReaction` / `deleteAllMessageReactions` | Manage message reactions           |
| `getUserChatBoosts`                                   | Retrieve a user's chat boosts      |
### 🎨 Colored Buttons & Premium Emoji
Both inline keyboard buttons and regular reply keyboard buttons can now be styled with a background color.
\*\*Colored inline keyboard buttons:\*\*
```python
keyboard = {
    "inline\_keyboard": [[
        {"text": "✅ Confirm", "callback\_data": "confirm", "style": "bg\_success"},
        {"text": "❌ Cancel", "callback\_data": "cancel", "style": "bg\_danger"},
        {"text": "ℹ️ Info", "callback\_data": "info", "style": "bg\_primary"}
    ]]
}
Bot.sendMessage(text="Choose an option:", reply\_markup=keyboard)
```
\*\*Colored reply keyboard buttons:\*\*
```python
keyboard = {
    "keyboard": [[
        {"text": "🟢 Start", "style": "bg\_success"},
        {"text": "🔴 Stop", "style": "bg\_danger"}
    ]],
    "resize\_keyboard": True
}
Bot.sendMessage(text="Control panel:", reply\_markup=keyboard)
```
Available `style` values for both button types: `bg\_primary` (blue, for main actions), `bg\_danger` (red, for destructive actions), `bg\_success` (green, for positive actions).
\*\*Premium custom emoji in message text:\*\* send a custom emoji directly in message text using the `<tg-emoji>` HTML tag with `parse\_mode="HTML"`. The tag must wrap the emoji's own regular fallback character:
```python
Bot.sendMessage(
    text='Welcome to the team! <tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>',
    parse\_mode="HTML"
)
```
\*\*Note:\*\* custom emoji in message text — and custom emoji icons on buttons (via `icon\_custom\_emoji\_id`) — require the \*\*bot owner's own Telegram account\*\* to have an active Telegram Premium subscription (or a Fragment-purchased bot username). This requirement applies only to the emoji itself; colored button styling (`style`) has no such requirement and works for every bot.
📖 The full parameter reference for every Telegram Bot API method and object — including `Api`/`Bot`, all built-in libraries, and every predefined variable — is available in the [TBS Language Reference](https://help.telebotstudio.com/tbs-language-reference).
\*\*\*
## Improvements & Fixes
\* \*\*`call` object\*\* now exposes `.from\_user`, giving you the real user who tapped an inline button — previously only accessible via the message object, which (in callback contexts) reflects the bot itself, not the user.
\* \*\*CSV library\*\* — fixed a bug where `.delete(index)` (remove one row) was being silently overridden by a duplicate method, making it behave like `.clear()` (wipe the whole table) instead. Both now work correctly and independently.
\* \*\*Reply markup objects\*\* — `reply\_markup` now correctly accepts `ReplyKeyboardMarkup`, `ReplyKeyboardRemove`, and `ForceReply` objects passed directly, not just plain dictionaries.
\*\*\*
## Dashboard & Workflow Improvements
Alongside the language-level additions, the dashboard has received a substantial set of organizational and workflow upgrades:
\* \*\*Bot Folders and Command Folders\*\* — organize both your bot list and each bot's command list into folders, with full create/rename/delete support.
\* \*\*Bulk Selection\*\* — select multiple bots or commands at once to pin or delete them in a single action.
\* \*\*Recycle Bin\*\* — deleted bots and commands are now recoverable for 30 days before permanent removal, with the option to restore individually or all at once.
\* \*\*Custom Bot Names\*\* — give any bot a display name separate from its Telegram username, editable at any time.
\* \*\*Sorting & Filtering\*\* — bot and command lists can now be sorted by newest, oldest, or most recently updated, with pinned items always shown first.
\* \*\*Bot Admins & Global Admins\*\* — grant other users admin access to a specific bot, or to your entire account.
\* \*\*Bot Transfers\*\* — transfer a bot to another TeleBot Studio account by email, with configurable approval policies and a trusted-sender whitelist.
\* \*\*Code Search & Replace\*\* — search across all of a bot's commands and replace text in bulk, with full undo history.
\* \*\*Command Import & Export\*\* — export commands as JSON, YAML, or plain text, edit them externally (including with AI tools), and re-import — with the option to update existing commands or only add new ones.
\* \*\*Migration Tool\*\* — our built-in migration tool on the website can now transform all of the commands from TBC platform (TPY language) to our TBS platform (TBS language) in one shot, by simply uploading the exported full bot file from the TBC platform's Manage tab and importing it into our migration tool on our website. This returns a transformed commands and code file that can be imported into any of your existing TBS bots using Import Commands in the Manage tab — or, upon transformation, you can also directly select any of your existing bots to import all those commands into right away.
\* \*\*Automatic HTML Repair\*\* — messages and captions sent with `parse\_mode="HTML"` now have broken or malformed HTML automatically corrected before sending, preventing `can't parse entities` errors entirely.
\* \*\*In-Editor Code Formatting\*\* — a one-click code formatter is now available directly in the command editor.
### 🛠️ New: Admin Panel
Every bot now has a dedicated \*\*Admin Panel\*\* tab for managing broadcasts, users, and bot data, organized into six sub-tabs:
\* \*\*Analytics\*\* — a real-time overview of your bot's activity: total commands executed, active users, broadcast performance, and overall usage trends.
\* \*\*Users\*\* — browse every Telegram user who has interacted with your bot, see when they joined and were last active, block or unblock individual users, and export the full user list to a file.
\* \*\*Broadcasts\*\* — view every broadcast you've sent or currently have running, with live progress and status. Pause, resume, stop, or re-run any broadcast directly from this tab.
\* \*\*Bot Data\*\* — browse, edit, and delete your bot's stored key-value data directly from the dashboard, without needing to write a command to inspect it.
\* \*\*User Data\*\* — the same, scoped per user — see and manage any piece of data your commands have saved for a specific Telegram user.
\* \*\*Permissions\*\* — grant other TeleBot Studio accounts admin access to this specific bot, so you can collaborate on managing a bot without sharing your own account credentials.
\*\*\*
## Notes
\* \*\*Backward compatible.\*\* All existing bots and commands continue to work exactly as before — every addition in this update is opt-in.
\* \*\*No restart required.\*\* New library and method access is available immediately on your next command execution.
Questions or feedback? Join our help group at [t.me/TeleBotStudioChat](https://t.me/TeleBotStudioChat).
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/telebot-studio-v1.1.0-media-libraries-gifts-webhooks-and-more.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
