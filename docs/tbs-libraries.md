> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/tbs-libraries.md).
# TBS Libraries Reference
## Introduction
TeleBot Studio provides a comprehensive collection of built-in libraries (accessed via `Lib`) that extend your bot's capabilities far beyond basic messaging. These libraries are pre-loaded and ready to use—no import statements needed. From handling cryptocurrency payments to managing AI conversations, from working with dates to generating random values, TBS libraries give you powerful tools to build sophisticated bots quickly.
### Why Use TBS Libraries?
\* \*\*Zero Setup\*\*: All libraries are pre-configured and immediately available
\* \*\*Battle-Tested\*\*: Production-ready code used by thousands of bots
\* \*\*Fully Integrated\*\*: Designed specifically for the TBS environment
\* \*\*Comprehensive\*\*: Cover payments, blockchain, AI, data management, referrals, and more
\* \*\*Simple Syntax\*\*: Clean, intuitive API design for rapid development
### No Imports Required
Unlike traditional Python, TBS libraries are automatically available in your bot commands. Simply use `Lib.LibraryName` to access any library:
```python
# No imports needed! Just use directly
random\_num = Lib.Random.integer(1, 100)
current\_time = Lib.DateTime.utcnow()
ref\_link = Lib.RefLib.getLink()
```
\*\*\*
## Core Libraries
### Lib.Random
Generate random values for games, giveaways, unique identifiers, and more.
#### Methods
| Method | Parameters | Returns | Description |
| --------- | ------------------------------------------ | ------- | ---------------------------------------------- |
| `integer` | `min` (int), `max` (int) | int | Random integer between min and max (inclusive) |
| `string` | `length` (int), `char\_set` (str, optional) | str | Random string of specified length |
| `decimal` | `min` (float), `max` (float) | float | Random decimal number between min and max |
| `ascii` | `length` (int) | str | Random ASCII string of specified length |
#### New Methods \*(Added in v1.1.0)\*
| Method           | Parameters                                                                     | Returns | Description                                                 |
| ---------------- | ------------------------------------------------------------------------------ | ------- | ----------------------------------------------------------- |
| `hex`            | `length` (int)                                                                 | str     | Random hexadecimal string of specified length               |
| `bytes`          | `length` (int)                                                                 | bytes   | Random bytes object of specified length                     |
| `uuid`           | None                                                                           | str     | A random UUID4 string                                       |
| `password`       | `length` (int), `use\_digits` (bool, optional), `use\_specials` (bool, optional) | str     | Random password with configurable digits/special characters |
| `choice`         | `data` (list)                                                                  | any     | One random element from a list                              |
| `sample`         | `data` (list), `k` (int)                                                       | list    | `k` unique random elements from a list                      |
| `shuffle`        | `data` (list)                                                                  | list    | Returns a new shuffled copy of a list (original unchanged)  |
| `weightedChoice` | `data` (list), `weights` (list)                                                | any     | One element chosen according to relative weights            |
| `boolean`        | None                                                                           | bool    | Random True/False                                           |
| `range`          | `start` (int), `stop` (int), `count` (int)                                     | list    | `count` unique integers sampled from a range                |
| `gaussian`       | `mean` (float), `stddev` (float)                                               | float   | Random float from a Gaussian (normal) distribution          |
#### Examples
```python
# Roll a dice
dice = Lib.Random.integer(1, 6)
Api.sendMessage(f"🎲 You rolled: {dice}")
# Generate verification code
code = Lib.Random.string(6)
User.storeData("verification\_code", code)
Api.sendMessage(f"Your verification code: {code}")
# Generate random price
price = Lib.Random.decimal(9.99, 49.99)
Api.sendMessage(f"Today's special price: ${price:.2f}")
# Generate secure token
token = Lib.Random.ascii(32)
User.storeData("api\_token", token)
# New in v1.1.0: generate a secure password
password = Lib.Random.password(12)
Api.sendMessage(f"Your temporary password: {password}")
# New in v1.1.0: weighted giveaway prize selection
prize = Lib.Random.weightedChoice(["Common", "Rare", "Legendary"], weights=[70, 25, 5])
Api.sendMessage(f"🎁 You won: {prize}!")
# New in v1.1.0: pick unique winners from a participant list
winners = Lib.Random.sample(participant\_ids, 3)
```
\*\*Use Cases:\*\*
\* Random giveaways and contests
\* Dice games and gambling
\* Verification codes
\* Unique session IDs
\* Random pricing for promotions
\*\*\*
### Lib.DateTime
Work with dates, times, and timestamps for scheduling, logging, and time-based features.
#### Methods
| Method | Parameters | Returns | Description |
| ---------- | -------------------- | -------- | ---------------------------------- |
| `utcnow` | None | datetime | Current UTC date and time |
| `date\_now` | None | date | Current UTC date |
| `time` | None | float | Current UNIX timestamp |
| `now` | `timezone\_str` (str) | datetime | Current time in specified timezone |
#### Examples
```python
# Log activity time
timestamp = Lib.DateTime.time()
User.storeData("last\_active", timestamp)
# Show current time
current = Lib.DateTime.utcnow()
Api.sendMessage(f"Current time (UTC): {current}")
# Get time in specific timezone
ny\_time = Lib.DateTime.now("America/New\_York")
Api.sendMessage(f"New York time: {ny\_time}")
# Calculate time difference
start\_time = User.fetchData("session\_start")
if start\_time:
elapsed = Lib.DateTime.time() - start\_time
Api.sendMessage(f"Session duration: {int(elapsed)} seconds")
```
\*\*Use Cases:\*\*
\* Activity logging
\* Session tracking
\* Scheduling features
\* Time-based rewards
\* Timezone conversions
\*\*\*
### Lib.CSV
Manage structured data with CSV files—perfect for leaderboards, surveys, and data collection.
#### Creating a CSV Table
```python
csv = Lib.CSV.Table("filename.csv")
```
#### Table Methods
| Method | Parameters | Returns | Description |
| ------------ | ------------------------------- | ------- | ---------------------------------- |
| `create` | `headers` (list) | bool | Initialize CSV with column headers |
| `insert` | `row` (dict) | bool | Add a new row |
| `update` | `index` (int), `new\_row` (dict) | bool | Update existing row |
| `delete` | `index` (int) | bool | Delete a row |
| `get` | None | list | Get all rows |
| `row` | `index` (int) | dict | Get specific row |
| `find` | `\*\*criteria` | list | Find rows matching criteria |
| `count` | None | int | Get total number of rows |
| `toString` | None | str | Export as CSV string |
| `fromString` | `csv\_string` (str) | bool | Import from CSV string |
| `clear`      | None                            | bool    | \*(Added in v1.1.0)\* Wipes the entire table (all rows and headers) |
#### Examples
```python
# Create leaderboard
leaderboard = Lib.CSV.Table("scores.csv")
leaderboard.create(["player", "score", "date"])
# Add player score
leaderboard.insert({
"player": "Alice",
"score": 1500,
"date": "2024-01-15"
})
# Update score
leaderboard.update(0, {"score": 1750})
# Find high scorers
top\_players = leaderboard.find(score=1500)
for player in top\_players:
Api.sendMessage(f"🏆 {player['player']}: {player['score']}")
# Get all data
all\_scores = leaderboard.get()
message = "📊 Leaderboard:\n"
for i, row in enumerate(all\_scores, 1):
message += f"{i}. {row['player']}: {row['score']}\n"
Api.sendMessage(message)
# Count entries
total = leaderboard.count()
Api.sendMessage(f"Total players: {total}")
# New in v1.1.0: clear the entire table
leaderboard.clear()
```
\*\*Use Cases:\*\*
\* Leaderboards and rankings
\* Survey data collection
\* User registration forms
\* Event attendance tracking
\* Order management
\*\*\*
## Media Libraries
TeleBot Studio also includes two dedicated image-processing libraries: \*\*`Lib.PIL`\*\* for general-purpose image editing (resizing, cropping, text, watermarks, filters), and \*\*`Lib.CV`\*\* for advanced computer vision, including real face detection.
Both libraries work entirely in-memory — load an image from bytes, transform it, and send it straight back to Telegram.
```python
resp = Request.get("https://example.com/photo.jpg")
img = Lib.PIL.openFromBytes(resp.content)
img = Lib.PIL.drawText(img, "Hello!", (10, 10))
Bot.sendPhoto(photo=Lib.PIL.toBytes(img, format="PNG"))
```
📖 For the complete method reference, parameters, and examples for both libraries, see the [\*\*TBS Media Libraries (PIL & CV) Documentation\*\*](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation).
\*\*\*
## Security Libraries
### Lib.Security \*(Added in v1.1.0)\*
A cryptographic toolkit for HMAC signing, signature verification, AES encryption, and hashing — commonly needed for verifying payment gateway webhooks and securing stored data.
#### Methods
| Method                        | Parameters                                                                   | Returns | Description                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| `signHMAC`                    | `secret` (str), `data` (str), `algorithm` (str, optional)                    | str     | Creates an HMAC signature (hex string). `algorithm` can be `"sha256"` (default), `"sha512"`, or `"md5"` |
| `verifyHMAC`                  | `secret` (str), `data` (str), `signature` (str), `algorithm` (str, optional) | bool    | Verifies an HMAC signature using a timing-safe comparison                                               |
| `verifyEd25519`               | `public\_key\_hex` (str), `signature\_hex` (str), `data` (str)                  | bool    | Verifies an Ed25519 signature. Never raises — returns `False` on any invalid input                      |
| `verifyPaymentGatewayWebhook` | `public\_key\_hex` (str), `signature\_hex` (str), `raw\_body` (str)              | bool    | Convenience wrapper for verifying Ed25519-signed payment gateway webhooks                               |
| `generateKey`                 | None                                                                         | str     | Generates a new AES (Fernet) encryption key                                                             |
| `encryptAES`                  | `plaintext` (str), `key` (str)                                               | str     | Encrypts a string, returning an encrypted token                                                         |
| `decryptAES`                  | `token` (str), `key` (str)                                                   | str     | Decrypts a token back to the original plaintext                                                         |
| `hashSHA256`                  | `data` (str)                                                                 | str     | SHA-256 hash (hex string)                                                                               |
| `hashSHA512`                  | `data` (str)                                                                 | str     | SHA-512 hash (hex string)                                                                               |
| `hashMD5`                     | `data` (str)                                                                 | str     | MD5 hash (hex string). Not suitable for security purposes                                               |
#### Examples
```python
# Sign and verify data with HMAC
secret = "my-webhook-secret"
signature = Lib.Security.signHMAC(secret, request\_body)
if Lib.Security.verifyHMAC(secret, request\_body, signature):
    Api.sendMessage("✅ Signature verified!")
# Verify a payment gateway webhook
is\_valid = Lib.Security.verifyPaymentGatewayWebhook(
    public\_key\_hex="...",
    signature\_hex=options.headers.get("X-Signature"),
    raw\_body=options.data
)
if is\_valid:
    Api.sendMessage("✅ Payment webhook verified")
# Encrypt and store sensitive data
key = Lib.Security.generateKey()
User.storeData("encryption\_key", key)
encrypted = Lib.Security.encryptAES("sensitive user data", key)
User.storeData("encrypted\_field", encrypted)
# Decrypt it later
stored\_key = User.fetchData("encryption\_key")
stored\_data = User.fetchData("encrypted\_field")
original = Lib.Security.decryptAES(stored\_data, stored\_key)
# Hash a value
hashed = Lib.Security.hashSHA256("some input string")
```
\*\*Use Cases:\*\*
\* Verifying payment gateway webhook signatures
\* Securely storing sensitive user data
\* API request signing
\* Data integrity checks
\*\*\*
## Blockchain Libraries
### Lib.EVM
Interact with 31+ Ethereum-compatible blockchains including Ethereum, BSC, Polygon, Avalanche, Arbitrum, and more.
#### Supported Networks
Ethereum, BSC, Polygon, Avalanche, Fantom, Arbitrum, Optimism, Base, ZKSync, Scroll, Linea, Harmony, Cronos, Moonriver, Moonbeam, Celo, Heco, Okexchain, Xdai, KCC, Metis, Aurora, Boba, Kava, Fuse, Evmos, Canto, Astar, Telos, Rootstock, TTcoin
#### Methods
| Method | Parameters | Description |
| ------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `generateKey` | None | Generate new private key |
| `storeKey` | `private\_key` (str) | Store private key securely |
| `sendCoin` | `value`, `to`, `rpc\_url`, `private\_key`, `network`, `retry`, `estimate\_gas` | Send native coin (ETH, BNB, MATIC, etc.) |
| `sendToken` | `value`, `to`, `contract\_address`, `rpc\_url`, `private\_key`, `network`, `retry`, `estimate\_gas` | Send ERC-20 tokens |
| `networks` | None | Get list of supported networks |
| `getRPC` | `network` (str) | Get default RPC URL for network |
#### New Methods \*(Added in v1.1.0)\*
| Method              | Parameters                                                                                                         | Description                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `fetchBalance`      | `address`, `network` (optional), `rpc\_url` (optional), `unit` (optional)                                           | Returns the native coin balance of an address. `unit` can be `"wei"`, `"gwei"`, or `"ether"` (default) |
| `fetchTokenBalance` | `address`, `contract\_address`, `network` (optional), `rpc\_url` (optional), `decimals` (optional), `raw` (optional) | Returns the ERC-20 token balance of an address, with automatic decimal detection                       |
#### Examples
```python
# Generate and store wallet
private\_key = Lib.EVM.generateKey()
Lib.EVM.storeKey(private\_key)
Api.sendMessage("✅ Wallet created!")
# Send ETH
tx\_hash = Lib.EVM.sendCoin(
value=0.1,
to="0xRecipientAddress",
network="ethereum",
estimate\_gas=True
)
Api.sendMessage(f"Transaction: {tx\_hash}")
# Send USDT on Polygon
tx\_hash = Lib.EVM.sendToken(
value=50,
to="0xRecipientAddress",
contract\_address="0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
network="polygon",
estimate\_gas=True
)
Api.sendMessage(f"✅ Sent 50 USDT: {tx\_hash}")
# Get supported networks
networks = Lib.EVM.networks()
Api.sendMessage(f"Supported networks: {len(networks)}")
# New in v1.1.0: check a wallet's native balance
balance = Lib.EVM.fetchBalance("0xWalletAddress", network="ethereum")
Api.sendMessage(f"Balance: {balance} ETH")
# New in v1.1.0: check a wallet's token balance
usdt\_balance = Lib.EVM.fetchTokenBalance(
    "0xWalletAddress",
    contract\_address="0xdAC17F958D2ee523a2206206994597C13D831ec7",
    network="ethereum"
)
Api.sendMessage(f"USDT Balance: {usdt\_balance}")
```
\*\*Use Cases:\*\*
\* Crypto payment processing
\* Token airdrops
\* NFT minting
\* DeFi integrations
\* Multi-chain wallets
\*\*\*
### Lib.TON
Complete integration with The Open Network (TON) blockchain for payments, jettons, and TON Connect.
#### Wallet Management
| Method | Parameters | Description |
| -------------- | --------------------------- | ------------------------------------- |
| `createWallet` | None | Generate new TON wallet with mnemonic |
| `storeKey` | `mnemonics` (str) | Store mnemonic phrase |
| `getAddress` | `mnemonics` (str, optional) | Get wallet address |
#### TON Operations
| Method | Parameters | Description |
| -------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| `balance` | `address`, `api\_key`, `endpoint` | Check TON balance |
| `send` | `to\_address`, `amount`, `comment`, `mnemonics`, `api\_key`, `endpoint`, `is\_testnet` | Send TON |
| `transactions` | `address`, `api\_key`, `endpoint`, `limit` | Get transaction history |
#### TON Connect
| Method | Parameters | Description |
| ---------------- | --------------------------------------------------------------- | ------------------------------------- |
| `connectSession` | `user\_id`, `expiry\_seconds` | Create wallet connection session |
| `verifySession` | `session\_id` | Check if wallet connected |
| `requestPayment` | `to\_address`, `amount`, `comment`, `callback\_url`, `return\_url` | Request payment from connected wallet |
| `register\_ton\_connect\_wallet` | `session\_id`, `wallet\_address`                                  | \*(Added in v1.1.0)\* Marks a session as connected and stores the connected wallet address — used inside your own callback once a wallet approves the connection |
#### Jetton Operations
| Method | Parameters | Description |
| -------------- | ---------------------------------------------------------------------------------------- | ----------------------- |
| `tokenInfo` | `jetton\_master\_address`, `api\_key`, `endpoint` | Get token metadata |
| `tokenBalance` | `owner\_address`, `jetton\_master\_address`, `api\_key`, `endpoint` | Check jetton balance |
| `requestToken` | `to\_address`, `jetton\_master\_address`, `amount`, `comment`, `callback\_url`, `return\_url` | Request jetton transfer |
| `get\_jetton\_wallet\_address` | `owner\_address`, `jetton\_master\_address`, `api\_key` (optional), `endpoint` (optional)    | \*(Added in v1.1.0)\* Resolves the Jetton wallet address for an owner, without needing a full balance lookup |
#### Examples
```python
# Create wallet
wallet = Lib.TON.createWallet()
Api.sendMessage(f"💎 Address: {wallet['address']}")
Api.sendMessage(f"🔐 Mnemonic: {wallet['mnemonic']}")
# Check balance
balance = Lib.TON.balance("EQD...")
Api.sendMessage(f"Balance: {balance} TON")
# Send TON
Lib.TON.send(
to\_address="EQD...",
amount=1.5,
comment="Payment for service"
)
Api.sendMessage("✅ TON sent!")
# TON Connect - Create session
session = Lib.TON.connectSession(user\_id=u, expiry\_seconds=300)
Api.sendMessage(f"Connect: {session['connect\_url']}")
# Request payment via TON Connect
payment = Lib.TON.requestPayment(
to\_address="EQD...",
amount=5,
comment="Subscription payment"
)
# New in v1.1.0: finalize a TON Connect session once the wallet approves
result = Lib.TON.register\_ton\_connect\_wallet(session['session\_id'], wallet\_address="EQD...")
if result['ok']:
    Api.sendMessage("✅ Wallet connected!")
# New in v1.1.0: resolve a Jetton wallet address directly
jetton\_wallet = Lib.TON.get\_jetton\_wallet\_address(
    owner\_address="EQD...",
    jetton\_master\_address="EQC..."
)
Api.sendMessage(f"Jetton wallet: {jetton\_wallet}")
```
\*\*Use Cases:\*\*
\* TON payments
\* Jetton (token) transfers
\* Wallet connection via TON Connect
\* Payment requests
\* Balance checking
\*\*\*
## AI Libraries
### Lib.AI
Unified interface for multiple AI providers (OpenAI, Gemini) with consistent API.
#### Creating AI Client
```python
# OpenAI client
openai = Lib.AI.client(
provider="openai",
apiKey="your-api-key",
baseUrl="https://api.openai.com/v1" # optional
)
# Gemini client
gemini = Lib.AI.client(
provider="gemini",
apiKey="your-gemini-key"
)
```
#### Client Methods
| Method | Parameters | Description |
| ----------------- | ------------------------------------------------ | -------------------------- |
| `chat` | `model`, `messages`, `temperature`, `max\_tokens` | Generate chat completion |
| `createAssistant` | `model`, `name`, `instructions`, `tools` | Create AI assistant |
| `createThread` | None | Create conversation thread |
| `addMessage` | `thread\_id`, `role`, `content` | Add message to thread |
| `run` | `thread\_id`, `assistant\_id` | Run assistant on thread |
| `getStatus` | `thread\_id`, `run\_id` | Check run status |
| `getMessages` | `thread\_id`, `limit` | Get thread messages |
#### Examples
```python
# Simple chat with OpenAI
openai = Lib.AI.client(provider="openai", apiKey="sk-...")
response = openai.chat(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a helpful bot assistant."},
{"role": "user", "content": msg}
]
)
Api.sendMessage(response["choices"][0]["message"]["content"])
# Use Gemini
gemini = Lib.AI.client(provider="gemini", apiKey="...")
response = gemini.chat(
model="gemini-2.0-flash",
messages=[
{"role": "user", "content": "Explain quantum computing simply"}
]
)
Api.sendMessage(response["choices"][0]["message"]["content"])
# Create assistant
assistant = openai.createAssistant(
model="gpt-4",
name="Support Bot",
instructions="You help users with bot questions."
)
thread = openai.createThread()
openai.addMessage(thread["id"], "user", "How do I create commands?")
run = openai.run(thread["id"], assistant["id"])
```
\*\*Use Cases:\*\*
\* AI chatbots
\* Content generation
\* Code assistance
\* Translation services
\* Question answering
\*\*\*
## Payment Libraries
### Lib.Oxapay
Complete cryptocurrency payment gateway integration supporting 20+ cryptocurrencies.
#### Creating Client
```python
oxapay = Lib.Oxapay.client("your\_merchant\_api\_key")
```
#### Payment Methods
| Method | Parameters | Description |
| --------------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
| `createAddress` | `network`, `to\_currency`, `auto\_withdrawal`, `callback\_url`, `email`, `order\_id`, `description` | Generate static payment address |
| `createInvoice` | `amount`, `currency`, `network`, `callback\_url`, `email`, `order\_id`, `description`, `return\_url` | Create payment invoice |
| `invoice` | `track\_id` | Check invoice status |
| `revokeAddress` | `address` | Disable static address |
#### Payout Methods
| Method | Parameters | Description |
| --------------- | ------------------------------------------------------------------------- | ------------------- |
| `payout` | `address`, `amount`, `currency`, `network`, `callback\_url`, `description` | Create withdrawal |
| `payoutStatus` | `track\_id` | Check payout status |
| `payoutHistory` | `from\_date`, `to\_date`, `page` | Get payout history |
#### Account Methods
| Method | Parameters | Description |
| ----------- | ------------------------------ | ----------------------------- |
| `info` | None | Get merchant account info |
| `allowance` | None | Get balance for each currency |
| `rate` | `from\_currency`, `to\_currency` | Get exchange rates |
| `history` | `from\_date`, `to\_date`, `page` | Get payment history |
#### Whitelist Methods
| Method | Parameters | Description |
| ----------------- | -------------------------------- | ------------------------- |
| `whitelist` | None | Get whitelisted addresses |
| `addWhitelist` | `address`, `currency`, `network` | Add to whitelist |
| `removeWhitelist` | `address`, `currency`, `network` | Remove from whitelist |
#### Examples
```python
# Create client
oxapay = Lib.Oxapay.client("your\_merchant\_key")
# Create static address
address = oxapay.createAddress(
network="BSC",
callback\_url="https://yourbot.com/callback"
)
Api.sendMessage(f"Send payment to: {address['data']['address']}")
# Create invoice
invoice = oxapay.createInvoice(
amount=100,
currency="USDT",
network="TRC20",
description="Premium subscription",
return\_url="https://t.me/yourbot"
)
Api.sendMessage(f"Pay here: {invoice['data']['payment\_url']}")
# Check payment status
status = oxapay.invoice(track\_id="12345")
if status['data']['status'] == "Paid":
Api.sendMessage("✅ Payment confirmed!")
User.storeData("premium", True)
# Send payout
payout = oxapay.payout(
address="0xRecipientAddress",
amount=50,
currency="USDT",
network="BSC"
)
Api.sendMessage(f"Payout sent: {payout['data']['track\_id']}")
# Get account balance
balance = oxapay.allowance()
Api.sendMessage(f"Balance: {balance['data']}")
```
\*\*Use Cases:\*\*
\* Cryptocurrency payments
\* Subscription billing
\* Automated payouts
\* Multi-currency support
\* Payment tracking
\*\*\*
### Lib.Crypto
Get real-time cryptocurrency prices and conversions.
#### Methods
| Method | Parameters | Description |
| ----------- | ------------------------------------------------------------ | -------------------------- |
| `get\_price` | `ids` (str), `vs\_currencies` (str) | Get current prices |
| `convert` | `amount` (float), `from\_currency` (str), `to\_currency` (str) | Convert between currencies |
#### Examples
```python
# Get BTC price
price = Lib.Crypto.get\_price("bitcoin", "usd")
Api.sendMessage(f"BTC Price: ${price['bitcoin']['usd']}")
# Get multiple prices
prices = Lib.Crypto.get\_price("bitcoin,ethereum", "usd,eur")
Api.sendMessage(f"BTC: ${prices['bitcoin']['usd']}")
Api.sendMessage(f"ETH: ${prices['ethereum']['usd']}")
# Convert crypto
btc\_amount = 0.5
usd\_value = Lib.Crypto.convert(btc\_amount, "BTC", "USD")
Api.sendMessage(f"{btc\_amount} BTC = ${usd\_value:.2f}")
```
\*\*Use Cases:\*\*
\* Price displays
\* Currency conversion
\* Portfolio tracking
\* Payment calculations
\* Market alerts
\*\*\*
## Gifting Libraries
### Lib.TeleGifts \*(Added in v1.1.0)\*
Send Telegram Gifts (paid in Stars) to any user — not limited to Premium accounts. Comes with a built-in catalog and full send history tracking.
#### Catalog Methods
| Method               | Parameters                 | Returns | Description                                                                                     |
| -------------------- | -------------------------- | ------- | ----------------------------------------------------------------------------------------------- |
| `getGiftCatalog`     | `category` (str, optional) | list    | Returns the gift catalog, optionally filtered by category (`"Budget"`, `"Premium"`, `"Luxury"`) |
| `getGiftByKey`       | `gift\_key` (str)           | dict    | Get a single gift's details by its key                                                          |
| `getGiftById`        | `gift\_id` (str)            | dict    | Get a single gift's details by its real Telegram gift ID                                        |
| `getGiftsByCategory` | None                       | dict    | Returns all gifts grouped by category                                                           |
| `searchGifts`        | `query` (str)              | list    | Search gifts by name, description, or emoji                                                     |
| `getGiftPriceRange`  | None                       | dict    | Returns min/max/average price and per-category price ranges                                     |
#### Sending Methods
| Method         | Parameters                                                          | Returns | Description                               |
| -------------- | ------------------------------------------------------------------- | ------- | ----------------------------------------- |
| `sendGift`     | `user\_id`, `gift\_key`, `message` (optional), `bot\_token` (optional) | dict    | Sends a gift by its catalog key           |
| `sendGiftById` | `user\_id`, `gift\_id`, `message` (optional), `bot\_token` (optional)  | dict    | Sends a gift by its real Telegram gift ID |
#### History & Settings
| Method               | Parameters                                                                        | Returns | Description                                 |
| -------------------- | --------------------------------------------------------------------------------- | ------- | ------------------------------------------- |
| `getGiftHistory`     | `limit` (int, optional), `status` (str, optional), `recipient\_id` (str, optional) | list    | Returns a log of every gift send attempt    |
| `getGiftStats`       | None                                                                              | dict    | Returns total sent, failed, and Stars spent |
| `setGiftSetting`     | `key` (str), `value` (any)                                                        | bool    | Store a custom setting                      |
| `getGiftSetting`     | `key` (str), `default` (any, optional)                                            | any     | Retrieve a custom setting                   |
| `getAllGiftSettings` | None                                                                              | dict    | Retrieve all custom settings                |
#### Examples
```python
# Browse the catalog
catalog = Lib.TeleGifts.getGiftCatalog()
Api.sendMessage(f"We have {len(catalog)} gifts available!")
# Look up a specific gift
gift = Lib.TeleGifts.getGiftByKey("rose")
Api.sendMessage(f"{gift['name']} costs {gift['stars']} Stars")
# Send a gift
result = Lib.TeleGifts.sendGift(
    user\_id=u,
    gift\_key="rose",
    message="Thanks for joining our channel!"
)
if result['ok']:
    Api.sendMessage("🌹 Gift sent!")
else:
    Api.sendMessage(f"❌ Could not send gift: {result['error']}")
# Check price range for budgeting
prices = Lib.TeleGifts.getGiftPriceRange()
Api.sendMessage(f"Gifts range from {prices['min\_stars']} to {prices['max\_stars']} Stars")
# View sending history and stats
history = Lib.TeleGifts.getGiftHistory(limit=10)
stats = Lib.TeleGifts.getGiftStats()
Api.sendMessage(f"Total gifts sent: {stats['total\_sent']} ({stats['total\_stars\_spent']} Stars spent)")
```
\*\*Use Cases:\*\*
\* Rewarding loyal users
\* Giveaway prizes
\* Referral bonuses
\* Milestone celebrations
\* Customer appreciation campaigns
\*\*\*
## Growth & Marketing Libraries
### Lib.RefLib
Complete referral tracking system for viral growth and user acquisition.
#### Core Methods
| Method | Parameters | Returns | Description |
| ---------------- | ----------------------------------------------------------- | --------- | ----------------------------- |
| `getLink` | `bot\_name` (str, optional), `prefix` (str, optional) | str | Generate unique referral link |
| `track` | `on\_attracted`, `on\_touch\_own\_link`, `on\_already\_attracted` | bool | Track referral from /start |
| `getRefList` | `user\_id` (str, optional) | list | Get list of referred users |
| `getRefCount` | `user\_id` (str, optional) | int | Get total referral count |
| `getTopList` | `limit` (int, optional) | dict | Get referral leaderboard |
| `getAttractedBy` | None | dict/None | Get referrer information |
| `getRank` | `user\_id` (str, optional) | int | Get leaderboard position |
| `getStats` | `user\_id` (str, optional) | dict | Get comprehensive statistics |
#### Examples
```python
# Generate referral link
link = Lib.RefLib.getLink()
Api.sendMessage(f"🔗 Your link: {link}")
# Track referrals in /start command
Lib.RefLib.track(
on\_attracted=lambda ref: Api.sendMessage(f"🎉 New referral: {ref['first\_name']}!"),
on\_touch\_own\_link=lambda: Api.sendMessage("❌ Can't refer yourself!"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
# Show user stats
count = Lib.RefLib.getRefCount()
rank = Lib.RefLib.getRank()
Api.sendMessage(f"📊 Referrals: {count} | Rank: #{rank}")
# Display leaderboard
top = Lib.RefLib.getTopList(limit=10)
message = "🏆 Top Referrers:\n"
for i, (user\_id, count) in enumerate(top.items(), 1):
message += f"{i}. User {user\_id}: {count}\n"
Api.sendMessage(message)
# Get referral list
refs = Lib.RefLib.getRefList()
for ref in refs:
Api.sendMessage(f"• {ref['first\_name']} - {ref['date']}")
# Check who referred current user
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(f"Referred by: {referrer['first\_name']}")
```
\*\*Use Cases:\*\*
\* Viral growth campaigns
\* Referral reward programs
\* Multi-level marketing
\* Affiliate tracking
\* User acquisition contests
\* Community building
\*\*\*
## Integration Libraries
### Lib.Webhook
Generate webhook URLs for external integrations and bot-to-bot communication.
#### Method
| Method | Parameters | Description |
| ----------- | ----------------------------------------------------------------- | -------------------- |
| `getUrlFor` | `command`, `user\_id`, `chat\_id`, `bot\_id`, `api\_key`, `\*\*options` | Generate webhook URL |
#### Examples
```python
# Basic webhook
webhook = Lib.Webhook.getUrlFor(
command="process\_payment",
user\_id=u
)
Api.sendMessage(f"Payment webhook: {webhook}")
# Bot-to-bot webhook
webhook = Lib.Webhook.getUrlFor(
command="sync\_data",
bot\_id="other\_bot\_id",
api\_key="other\_bot\_key"
)
# Webhook with options
webhook = Lib.Webhook.getUrlFor(
command="notify",
user\_id=u,
redirect\_to="https://example.com/success"
)
# In webhook command, access data
data = options.get("data")
json\_data = options.get("json")
```
\*\*New in v1.1.0:\*\* commands triggered via a webhook URL can now also read the caller's request headers and IP address directly:
```python
# In a webhook-triggered command
caller\_ip = options.ip
custom\_header = options.headers.get("X-Custom-Header")
```
\*\*New in v1.1.0 — Webhook Result Sync:\*\* webhook-triggered commands can send a real response back to the external caller in the same request, using `Bot.setWebhookResponse()` (or `Api.setWebhookResponse()`):
```python
# In a webhook-triggered command
result = {"status": "verified", "user\_id": u}
Bot.setWebhookResponse(result)
# The external caller's HTTP request receives this result directly
```
\*\*Use Cases:\*\*
\* Payment notifications
\* Bot-to-bot communication
\* External API callbacks
\* Event notifications
\* Data synchronization
\*\*\*
## Practical Examples
### Complete Referral Reward Bot
```python
# /start command - Track referrals
def handle\_referral(ref):
# Reward new user
User.res("points").add(100)
Api.sendMessage("🎉 You earned 100 points!")
# Reward referrer
User.resOf("points", ref['id']).add(50)
Api.sendMessage(
chat\_id=ref['id'],
text=f"✅ {message.from\_user.first\_name} joined! +50 points"
)
Lib.RefLib.track(
on\_attracted=handle\_referral,
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
# /referral command - Show link and stats
link = Lib.RefLib.getLink()
count = Lib.RefLib.getRefCount()
rank = Lib.RefLib.getRank()
Api.sendMessage(f"""
🔗 Your Referral Link:
{link}
📊 Stats:
• Referrals: {count}
• Rank: #{rank}
• Earn 50 points per referral!
""")
```
### Crypto Payment Bot
```python
# Create payment address
oxapay = Lib.Oxapay.client("merchant\_key")
address = oxapay.createAddress(
network="BSC",
callback\_url=Lib.Webhook.getUrlFor("payment\_received", user\_id=u)
)
User.storeData("payment\_address", address['data']['address'])
User.storeData("payment\_track", address['data']['track\_id'])
Api.sendMessage(f"💰 Send USDT (BSC) to:\n`{address['data']['address']}`")
# In payment\_received command
track\_id = User.fetchData("payment\_track")
status = oxapay.invoice(track\_id)
if status['data']['status'] == "Paid":
Api.sendMessage("✅ Payment confirmed! Activating premium...")
User.storeData("premium", True)
```
### AI Assistant Bot
```python
# Initialize AI
ai = Lib.AI.client(provider="openai", apiKey="sk-...")
# Get or create thread
thread\_id = User.fetchData("ai\_thread")
if not thread\_id:
thread = ai.createThread()
thread\_id = thread["id"]
User.storeData("ai\_thread", thread\_id)
# Chat
ai.addMessage(thread\_id, "user", msg)
run = ai.run(thread\_id, "assistant\_id")
# Wait and get response
time.sleep(2)
messages = ai.getMessages(thread\_id, limit=1)
response = messages["data"][0]["content"][0]["text"]["value"]
Api.sendMessage(response)
```
### Leaderboard System
```python
# Create leaderboard
leaderboard = Lib.CSV.Table("game\_scores.csv")
# Initialize if needed
if leaderboard.count() == 0:
leaderboard.create(["user\_id", "username", "score", "date"])
# Add/update score
score = 1500
user\_name = message.from\_user.first\_name
# Check if user exists
existing = leaderboard.find(user\_id=str(u))
if existing:
# Update score
for i, row in enumerate(leaderboard.get()):
if row["user\_id"] == str(u):
if int(row["score"]) < score:
leaderboard.update(i, {"score": score})
Api.sendMessage(f"🎉 New high score: {score}!")
break
else:
# Add new entry
leaderboard.insert({
"user\_id": str(u),
"username": user\_name,
"score": score,
"date": Lib.DateTime.date\_now()
})
# Show top 10
all\_scores = sorted(leaderboard.get(), key=lambda x: int(x["score"]), reverse=True)
message = "🏆 Top 10 Leaderboard:\n\n"
for i, player in enumerate(all\_scores[:10], 1):
message += f"{i}. {player['username']}: {player['score']}\n"
Api.sendMessage(message)
```
### Random Giveaway
```python
# Collect participants
participants = Lib.CSV.Table("giveaway.csv")
if participants.count() == 0:
participants.create(["user\_id", "username"])
# Add participant
participants.insert({
"user\_id": str(u),
"username": message.from\_user.first\_name
})
Api.sendMessage("✅ You're entered in the giveaway!")
# Select winner (in admin command)
all\_participants = participants.get()
if len(all\_participants) > 0:
winner\_index = Lib.Random.integer(0, len(all\_participants) - 1)
winner = all\_participants[winner\_index]
Api.sendMessage(f"🎊 Winner: {winner['username']} (ID: {winner['user\_id']})")
```
\*\*\*
### Gift Reward Bot \*(New in v1.1.0)\*
```python
# Reward a user with a gift after they complete an action
result = Lib.TeleGifts.sendGift(
    user\_id=u,
    gift\_key="teddy\_bear",
    message="Thanks for being an awesome member!"
)
if result['ok']:
    Api.sendMessage("🧸 Enjoy your gift!")
else:
    Api.sendMessage("Sorry, we couldn't send your gift right now.")
```
## Best Practices
### Security
1. \*\*Never expose API keys in messages\*\*
```python
# Bad
Api.sendMessage(f"Your API key: {api\_key}")
# Good
User.storeData("api\_key", api\_key)
Api.sendMessage("API key saved securely!")
```
2. \*\*Validate webhook data\*\*
```python
# In webhook command
if "json" in options:
data = options["json"]
# Validate expected fields
if "amount" in data and "status" in data:
# Process payment
pass
```
3. \*\*Verify webhook signatures before trusting incoming data\*\* \*(New in v1.1.0)\*
```python
# In webhook command
is\_valid = Lib.Security.verifyHMAC(webhook\_secret, options.data, options.headers.get("X-Signature"))
if not is\_valid:
    Bot.setWebhookResponse({"ok": False, "error": "Invalid signature"})
    raise StopExecution()
```
### Performance
1. \*\*Reuse AI threads\*\*
```python
# Store thread ID to avoid creating new threads
thread\_id = User.fetchData("ai\_thread")
if not thread\_id:
thread = ai.createThread()
User.storeData("ai\_thread", thread["id"])
```
2. \*\*Cache API responses\*\*
```python
# Cache crypto prices (update every 5 minutes)
last\_update = User.fetchData("price\_update\_time") or 0
current\_time = Lib.DateTime.time()
if current\_time - last\_update > 300: # 5 minutes
price = Lib.Crypto.get\_price("bitcoin", "usd")
User.storeData("btc\_price", price['bitcoin']['usd'])
User.storeData("price\_update\_time", current\_time)
else:
price = User.fetchData("btc\_price")
```
### Error Handling
1. \*\*Handle API errors gracefully\*\*
```python
try:
tx\_hash = Lib.EVM.sendCoin(
value=0.1,
to=recipient,
network="ethereum"
)
Api.sendMessage(f"✅ Sent! TX: {tx\_hash}")
except Exception as e:
Api.sendMessage(f"❌ Error: {str(e)}")
# Log error for admin
Bot.storeData("last\_error", str(e))
```
\*\*\*
## Summary
TBS Libraries provide everything you need to build sophisticated Telegram bots:
| Library               | Purpose                 | Key Features                                                                                                                                    |
| --------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| \*\*Random\*\*            | Randomization           | Integers, strings, decimals, ASCII, UUIDs, passwords, weighted choices, and more                                                                |
| \*\*DateTime\*\*          | Time management         | UTC time, timestamps, timezones                                                                                                                 |
| \*\*CSV\*\*               | Data storage            | Tables, queries, export/import                                                                                                                  |
| \*\*PIL\*\* \*(new)\*       | Image editing           | Resize, crop, draw, filters, watermarks — [see full docs](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation)          |
| \*\*CV\*\* \*(new)\*        | Computer vision         | Face detection, contours, perspective transforms — [see full docs](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation) |
| \*\*Security\*\* \*(new)\*  | Cryptography            | HMAC, Ed25519, AES encryption, hashing                                                                                                          |
| \*\*EVM\*\*               | EVM blockchains         | 31+ networks, tokens, native coins, balance checking                                                                                            |
| \*\*TON\*\*               | TON blockchain          | Wallets, jettons, TON Connect                                                                                                                   |
| \*\*AI\*\*                | Artificial Intelligence | OpenAI, Gemini, assistants                                                                                                                      |
| \*\*Oxapay\*\*            | Crypto payments         | Invoices, payouts, tracking                                                                                                                     |
| \*\*Crypto\*\*            | Price data              | Real-time prices, conversions                                                                                                                   |
| \*\*TeleGifts\*\* \*(new)\* | Telegram Gifts          | Send Stars-based gifts, catalog, history tracking                                                                                               |
| \*\*RefLib\*\*            | Referral system         | Link generation, tracking, leaderboards                                                                                                         |
| \*\*Webhook\*\*           | Integrations            | External callbacks, bot communication, synchronous responses                                                                                    |
All libraries are:
\* ✅ Pre-loaded and ready to use
\* ✅ No installation or imports needed
\* ✅ Production-tested and reliable
\* ✅ Fully documented with examples
\* ✅ Designed for TBS environment
Start building powerful bots today with TBS Libraries!
\*\*\*
\*For more information, visit\* [\*TeleBotStudio.com\*](https://TeleBotStudio.com)
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/tbs-libraries.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.