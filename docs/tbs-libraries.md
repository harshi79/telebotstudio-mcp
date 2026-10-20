# TBS Libraries Reference
## Introduction
TeleBot Studio provides a comprehensive collection of built-in libraries (accessed via `Lib`) that extend your bot's capabilities far beyond basic messaging. These libraries are pre-loaded and ready to use—no import statements needed. From handling cryptocurrency payments to managing AI conversations, from working with dates to generating random values, TBS libraries give you powerful tools to build sophisticated bots quickly.
### Why Use TBS Libraries?
* **Zero Setup**: All libraries are pre-configured and immediately available
* **Battle-Tested**: Production-ready code used by thousands of bots
* **Fully Integrated**: Designed specifically for the TBS environment
* **Comprehensive**: Cover payments, blockchain, AI, data management, referrals, and more
* **Simple Syntax**: Clean, intuitive API design for rapid development
### No Imports Required
Unlike traditional Python, TBS libraries are automatically available in your bot commands. Simply use `Lib.LibraryName` to access any library:
```python
# No imports needed! Just use directly
random_num = Lib.Random.integer(1, 100)
current_time = Lib.DateTime.utcnow()
ref_link = Lib.RefLib.getLink()
```
***
## Core Libraries
### Lib.Random
Generate random values for games, giveaways, unique identifiers, and more.
#### Methods
| Method | Parameters | Returns | Description |
| --------- | ------------------------------------------ | ------- | ---------------------------------------------- |
| `integer` | `min` (int), `max` (int) | int | Random integer between min and max (inclusive) |
| `string` | `length` (int), `char_set` (str, optional) | str | Random string of specified length |
| `decimal` | `min` (float), `max` (float) | float | Random decimal number between min and max |
| `ascii` | `length` (int) | str | Random ASCII string of specified length |
#### New Methods *(Added in v1.1.0)*
| Method           | Parameters                                                                     | Returns | Description                                                 |
| ---------------- | ------------------------------------------------------------------------------ | ------- | ----------------------------------------------------------- |
| `hex`            | `length` (int)                                                                 | str     | Random hexadecimal string of specified length               |
| `bytes`          | `length` (int)                                                                 | bytes   | Random bytes object of specified length                     |
| `uuid`           | None                                                                           | str     | A random UUID4 string                                       |
| `password`       | `length` (int), `use_digits` (bool, optional), `use_specials` (bool, optional) | str     | Random password with configurable digits/special characters |
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
User.storeData("verification_code", code)
Api.sendMessage(f"Your verification code: {code}")
# Generate random price
price = Lib.Random.decimal(9.99, 49.99)
Api.sendMessage(f"Today's special price: ${price:.2f}")
# Generate secure token
token = Lib.Random.ascii(32)
User.storeData("api_token", token)
# New in v1.1.0: generate a secure password
password = Lib.Random.password(12)
Api.sendMessage(f"Your temporary password: {password}")
# New in v1.1.0: weighted giveaway prize selection
prize = Lib.Random.weightedChoice(["Common", "Rare", "Legendary"], weights=[70, 25, 5])
Api.sendMessage(f"🎁 You won: {prize}!")
# New in v1.1.0: pick unique winners from a participant list
winners = Lib.Random.sample(participant_ids, 3)
```
**Use Cases:**
* Random giveaways and contests
* Dice games and gambling
* Verification codes
* Unique session IDs
* Random pricing for promotions
***
### Lib.DateTime
Work with dates, times, and timestamps for scheduling, logging, and time-based features.
#### Methods
| Method | Parameters | Returns | Description |
| ---------- | -------------------- | -------- | ---------------------------------- |
| `utcnow` | None | datetime | Current UTC date and time |
| `date_now` | None | date | Current UTC date |
| `time` | None | float | Current UNIX timestamp |
| `now` | `timezone_str` (str) | datetime | Current time in specified timezone |
#### Examples
```python
# Log activity time
timestamp = Lib.DateTime.time()
User.storeData("last_active", timestamp)
# Show current time
current = Lib.DateTime.utcnow()
Api.sendMessage(f"Current time (UTC): {current}")
# Get time in specific timezone
ny_time = Lib.DateTime.now("America/New_York")
Api.sendMessage(f"New York time: {ny_time}")
# Calculate time difference
start_time = User.fetchData("session_start")
if start_time:
elapsed = Lib.DateTime.time() - start_time
Api.sendMessage(f"Session duration: {int(elapsed)} seconds")
```
**Use Cases:**
* Activity logging
* Session tracking
* Scheduling features
* Time-based rewards
* Timezone conversions
***
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
| `update` | `index` (int), `new_row` (dict) | bool | Update existing row |
| `delete` | `index` (int) | bool | Delete a row |
| `get` | None | list | Get all rows |
| `row` | `index` (int) | dict | Get specific row |
| `find` | `**criteria` | list | Find rows matching criteria |
| `count` | None | int | Get total number of rows |
| `toString` | None | str | Export as CSV string |
| `fromString` | `csv_string` (str) | bool | Import from CSV string |
| `clear`      | None                            | bool    | *(Added in v1.1.0)* Wipes the entire table (all rows and headers) |
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
top_players = leaderboard.find(score=1500)
for player in top_players:
Api.sendMessage(f"🏆 {player['player']}: {player['score']}")
# Get all data
all_scores = leaderboard.get()
message = "📊 Leaderboard:\n"
for i, row in enumerate(all_scores, 1):
message += f"{i}. {row['player']}: {row['score']}\n"
Api.sendMessage(message)
# Count entries
total = leaderboard.count()
Api.sendMessage(f"Total players: {total}")
# New in v1.1.0: clear the entire table
leaderboard.clear()
```
**Use Cases:**
* Leaderboards and rankings
* Survey data collection
* User registration forms
* Event attendance tracking
* Order management
***
## Media Libraries
TeleBot Studio also includes two dedicated image-processing libraries: **`Lib.PIL`** for general-purpose image editing (resizing, cropping, text, watermarks, filters), and **`Lib.CV`** for advanced computer vision, including real face detection.
Both libraries work entirely in-memory — load an image from bytes, transform it, and send it straight back to Telegram.
```python
resp = Request.get("https://example.com/photo.jpg")
img = Lib.PIL.openFromBytes(resp.content)
img = Lib.PIL.drawText(img, "Hello!", (10, 10))
Bot.sendPhoto(photo=Lib.PIL.toBytes(img, format="PNG"))
```
📖 For the complete method reference, parameters, and examples for both libraries, see the [**TBS Media Libraries (PIL & CV) Documentation**](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation).
***
## Security Libraries
### Lib.Security *(Added in v1.1.0)*
A cryptographic toolkit for HMAC signing, signature verification, AES encryption, and hashing — commonly needed for verifying payment gateway webhooks and securing stored data.
#### Methods
| Method                        | Parameters                                                                   | Returns | Description                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------- |
| `signHMAC`                    | `secret` (str), `data` (str), `algorithm` (str, optional)                    | str     | Creates an HMAC signature (hex string). `algorithm` can be `"sha256"` (default), `"sha512"`, or `"md5"` |
| `verifyHMAC`                  | `secret` (str), `data` (str), `signature` (str), `algorithm` (str, optional) | bool    | Verifies an HMAC signature using a timing-safe comparison                                               |
| `verifyEd25519`               | `public_key_hex` (str), `signature_hex` (str), `data` (str)                  | bool    | Verifies an Ed25519 signature. Never raises — returns `False` on any invalid input                      |
| `verifyPaymentGatewayWebhook` | `public_key_hex` (str), `signature_hex` (str), `raw_body` (str)              | bool    | Convenience wrapper for verifying Ed25519-signed payment gateway webhooks                               |
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
signature = Lib.Security.signHMAC(secret, request_body)
if Lib.Security.verifyHMAC(secret, request_body, signature):
    Api.sendMessage("✅ Signature verified!")
# Verify a payment gateway webhook
is_valid = Lib.Security.verifyPaymentGatewayWebhook(
    public_key_hex="...",
    signature_hex=options.headers.get("X-Signature"),
    raw_body=options.data
)
if is_valid:
    Api.sendMessage("✅ Payment webhook verified")
# Encrypt and store sensitive data
key = Lib.Security.generateKey()
User.storeData("encryption_key", key)
encrypted = Lib.Security.encryptAES("sensitive user data", key)
User.storeData("encrypted_field", encrypted)
# Decrypt it later
stored_key = User.fetchData("encryption_key")
stored_data = User.fetchData("encrypted_field")
original = Lib.Security.decryptAES(stored_data, stored_key)
# Hash a value
hashed = Lib.Security.hashSHA256("some input string")
```
**Use Cases:**
* Verifying payment gateway webhook signatures
* Securely storing sensitive user data
* API request signing
* Data integrity checks
***
## Blockchain Libraries
### Lib.EVM
Interact with 31+ Ethereum-compatible blockchains including Ethereum, BSC, Polygon, Avalanche, Arbitrum, and more.
#### Supported Networks
Ethereum, BSC, Polygon, Avalanche, Fantom, Arbitrum, Optimism, Base, ZKSync, Scroll, Linea, Harmony, Cronos, Moonriver, Moonbeam, Celo, Heco, Okexchain, Xdai, KCC, Metis, Aurora, Boba, Kava, Fuse, Evmos, Canto, Astar, Telos, Rootstock, TTcoin
#### Methods
| Method | Parameters | Description |
| ------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `generateKey` | None | Generate new private key |
| `storeKey` | `private_key` (str) | Store private key securely |
| `sendCoin` | `value`, `to`, `rpc_url`, `private_key`, `network`, `retry`, `estimate_gas` | Send native coin (ETH, BNB, MATIC, etc.) |
| `sendToken` | `value`, `to`, `contract_address`, `rpc_url`, `private_key`, `network`, `retry`, `estimate_gas` | Send ERC-20 tokens |
| `networks` | None | Get list of supported networks |
| `getRPC` | `network` (str) | Get default RPC URL for network |
#### New Methods *(Added in v1.1.0)*
| Method              | Parameters                                                                                                         | Description                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `fetchBalance`      | `address`, `network` (optional), `rpc_url` (optional), `unit` (optional)                                           | Returns the native coin balance of an address. `unit` can be `"wei"`, `"gwei"`, or `"ether"` (default) |
| `fetchTokenBalance` | `address`, `contract_address`, `network` (optional), `rpc_url` (optional), `decimals` (optional), `raw` (optional) | Returns the ERC-20 token balance of an address, with automatic decimal detection                       |
#### Examples
```python
# Generate and store wallet
private_key = Lib.EVM.generateKey()
Lib.EVM.storeKey(private_key)
Api.sendMessage("✅ Wallet created!")
# Send ETH
tx_hash = Lib.EVM.sendCoin(
value=0.1,
to="0xRecipientAddress",
network="ethereum",
estimate_gas=True
)
Api.sendMessage(f"Transaction: {tx_hash}")
# Send USDT on Polygon
tx_hash = Lib.EVM.sendToken(
value=50,
to="0xRecipientAddress",
contract_address="0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
network="polygon",
estimate_gas=True
)
Api.sendMessage(f"✅ Sent 50 USDT: {tx_hash}")
# Get supported networks
networks = Lib.EVM.networks()
Api.sendMessage(f"Supported networks: {len(networks)}")
# New in v1.1.0: check a wallet's native balance
balance = Lib.EVM.fetchBalance("0xWalletAddress", network="ethereum")
Api.sendMessage(f"Balance: {balance} ETH")
# New in v1.1.0: check a wallet's token balance
usdt_balance = Lib.EVM.fetchTokenBalance(
    "0xWalletAddress",
    contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7",
    network="ethereum"
)
Api.sendMessage(f"USDT Balance: {usdt_balance}")
```
**Use Cases:**
* Crypto payment processing
* Token airdrops
* NFT minting
* DeFi integrations
* Multi-chain wallets
***
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
| `balance` | `address`, `api_key`, `endpoint` | Check TON balance |
| `send` | `to_address`, `amount`, `comment`, `mnemonics`, `api_key`, `endpoint`, `is_testnet` | Send TON |
| `transactions` | `address`, `api_key`, `endpoint`, `limit` | Get transaction history |
#### TON Connect
| Method | Parameters | Description |
| ---------------- | --------------------------------------------------------------- | ------------------------------------- |
| `connectSession` | `user_id`, `expiry_seconds` | Create wallet connection session |
| `verifySession` | `session_id` | Check if wallet connected |
| `requestPayment` | `to_address`, `amount`, `comment`, `callback_url`, `return_url` | Request payment from connected wallet |
| `register_ton_connect_wallet` | `session_id`, `wallet_address`                                  | *(Added in v1.1.0)* Marks a session as connected and stores the connected wallet address — used inside your own callback once a wallet approves the connection |
#### Jetton Operations
| Method | Parameters | Description |
| -------------- | ---------------------------------------------------------------------------------------- | ----------------------- |
| `tokenInfo` | `jetton_master_address`, `api_key`, `endpoint` | Get token metadata |
| `tokenBalance` | `owner_address`, `jetton_master_address`, `api_key`, `endpoint` | Check jetton balance |
| `requestToken` | `to_address`, `jetton_master_address`, `amount`, `comment`, `callback_url`, `return_url` | Request jetton transfer |
| `get_jetton_wallet_address` | `owner_address`, `jetton_master_address`, `api_key` (optional), `endpoint` (optional)    | *(Added in v1.1.0)* Resolves the Jetton wallet address for an owner, without needing a full balance lookup |
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
to_address="EQD...",
amount=1.5,
comment="Payment for service"
)
Api.sendMessage("✅ TON sent!")
# TON Connect - Create session
session = Lib.TON.connectSession(user_id=u, expiry_seconds=300)
Api.sendMessage(f"Connect: {session['connect_url']}")
# Request payment via TON Connect
payment = Lib.TON.requestPayment(
to_address="EQD...",
amount=5,
comment="Subscription payment"
)
# New in v1.1.0: finalize a TON Connect session once the wallet approves
result = Lib.TON.register_ton_connect_wallet(session['session_id'], wallet_address="EQD...")
if result['ok']:
    Api.sendMessage("✅ Wallet connected!")
# New in v1.1.0: resolve a Jetton wallet address directly
jetton_wallet = Lib.TON.get_jetton_wallet_address(
    owner_address="EQD...",
    jetton_master_address="EQC..."
)
Api.sendMessage(f"Jetton wallet: {jetton_wallet}")
```
**Use Cases:**
* TON payments
* Jetton (token) transfers
* Wallet connection via TON Connect
* Payment requests
* Balance checking
***
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
| `chat` | `model`, `messages`, `temperature`, `max_tokens` | Generate chat completion |
| `createAssistant` | `model`, `name`, `instructions`, `tools` | Create AI assistant |
| `createThread` | None | Create conversation thread |
| `addMessage` | `thread_id`, `role`, `content` | Add message to thread |
| `run` | `thread_id`, `assistant_id` | Run assistant on thread |
| `getStatus` | `thread_id`, `run_id` | Check run status |
| `getMessages` | `thread_id`, `limit` | Get thread messages |
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
**Use Cases:**
* AI chatbots
* Content generation
* Code assistance
* Translation services
* Question answering
***
## Payment Libraries
### Lib.Oxapay
Complete cryptocurrency payment gateway integration supporting 20+ cryptocurrencies.
#### Creating Client
```python
oxapay = Lib.Oxapay.client("your_merchant_api_key")
```
#### Payment Methods
| Method | Parameters | Description |
| --------------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
| `createAddress` | `network`, `to_currency`, `auto_withdrawal`, `callback_url`, `email`, `order_id`, `description` | Generate static payment address |
| `createInvoice` | `amount`, `currency`, `network`, `callback_url`, `email`, `order_id`, `description`, `return_url` | Create payment invoice |
| `invoice` | `track_id` | Check invoice status |
| `revokeAddress` | `address` | Disable static address |
#### Payout Methods
| Method | Parameters | Description |
| --------------- | ------------------------------------------------------------------------- | ------------------- |
| `payout` | `address`, `amount`, `currency`, `network`, `callback_url`, `description` | Create withdrawal |
| `payoutStatus` | `track_id` | Check payout status |
| `payoutHistory` | `from_date`, `to_date`, `page` | Get payout history |
#### Account Methods
| Method | Parameters | Description |
| ----------- | ------------------------------ | ----------------------------- |
| `info` | None | Get merchant account info |
| `allowance` | None | Get balance for each currency |
| `rate` | `from_currency`, `to_currency` | Get exchange rates |
| `history` | `from_date`, `to_date`, `page` | Get payment history |
#### Whitelist Methods
| Method | Parameters | Description |
| ----------------- | -------------------------------- | ------------------------- |
| `whitelist` | None | Get whitelisted addresses |
| `addWhitelist` | `address`, `currency`, `network` | Add to whitelist |
| `removeWhitelist` | `address`, `currency`, `network` | Remove from whitelist |
#### Examples
```python
# Create client
oxapay = Lib.Oxapay.client("your_merchant_key")
# Create static address
address = oxapay.createAddress(
network="BSC",
callback_url="https://yourbot.com/callback"
)
Api.sendMessage(f"Send payment to: {address['data']['address']}")
# Create invoice
invoice = oxapay.createInvoice(
amount=100,
currency="USDT",
network="TRC20",
description="Premium subscription",
return_url="https://t.me/yourbot"
)
Api.sendMessage(f"Pay here: {invoice['data']['payment_url']}")
# Check payment status
status = oxapay.invoice(track_id="12345")
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
Api.sendMessage(f"Payout sent: {payout['data']['track_id']}")
# Get account balance
balance = oxapay.allowance()
Api.sendMessage(f"Balance: {balance['data']}")
```
**Use Cases:**
* Cryptocurrency payments
* Subscription billing
* Automated payouts
* Multi-currency support
* Payment tracking
***
### Lib.Crypto
Get real-time cryptocurrency prices and conversions.
#### Methods
| Method | Parameters | Description |
| ----------- | ------------------------------------------------------------ | -------------------------- |
| `get_price` | `ids` (str), `vs_currencies` (str) | Get current prices |
| `convert` | `amount` (float), `from_currency` (str), `to_currency` (str) | Convert between currencies |
#### Examples
```python
# Get BTC price
price = Lib.Crypto.get_price("bitcoin", "usd")
Api.sendMessage(f"BTC Price: ${price['bitcoin']['usd']}")
# Get multiple prices
prices = Lib.Crypto.get_price("bitcoin,ethereum", "usd,eur")
Api.sendMessage(f"BTC: ${prices['bitcoin']['usd']}")
Api.sendMessage(f"ETH: ${prices['ethereum']['usd']}")
# Convert crypto
btc_amount = 0.5
usd_value = Lib.Crypto.convert(btc_amount, "BTC", "USD")
Api.sendMessage(f"{btc_amount} BTC = ${usd_value:.2f}")
```
**Use Cases:**
* Price displays
* Currency conversion
* Portfolio tracking
* Payment calculations
* Market alerts
***
## Gifting Libraries
### Lib.TeleGifts *(Added in v1.1.0)*
Send Telegram Gifts (paid in Stars) to any user — not limited to Premium accounts. Comes with a built-in catalog and full send history tracking.
#### Catalog Methods
| Method               | Parameters                 | Returns | Description                                                                                     |
| -------------------- | -------------------------- | ------- | ----------------------------------------------------------------------------------------------- |
| `getGiftCatalog`     | `category` (str, optional) | list    | Returns the gift catalog, optionally filtered by category (`"Budget"`, `"Premium"`, `"Luxury"`) |
| `getGiftByKey`       | `gift_key` (str)           | dict    | Get a single gift's details by its key                                                          |
| `getGiftById`        | `gift_id` (str)            | dict    | Get a single gift's details by its real Telegram gift ID                                        |
| `getGiftsByCategory` | None                       | dict    | Returns all gifts grouped by category                                                           |
| `searchGifts`        | `query` (str)              | list    | Search gifts by name, description, or emoji                                                     |
| `getGiftPriceRange`  | None                       | dict    | Returns min/max/average price and per-category price ranges                                     |
#### Sending Methods
| Method         | Parameters                                                          | Returns | Description                               |
| -------------- | ------------------------------------------------------------------- | ------- | ----------------------------------------- |
| `sendGift`     | `user_id`, `gift_key`, `message` (optional), `bot_token` (optional) | dict    | Sends a gift by its catalog key           |
| `sendGiftById` | `user_id`, `gift_id`, `message` (optional), `bot_token` (optional)  | dict    | Sends a gift by its real Telegram gift ID |
#### History & Settings
| Method               | Parameters                                                                        | Returns | Description                                 |
| -------------------- | --------------------------------------------------------------------------------- | ------- | ------------------------------------------- |
| `getGiftHistory`     | `limit` (int, optional), `status` (str, optional), `recipient_id` (str, optional) | list    | Returns a log of every gift send attempt    |
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
    user_id=u,
    gift_key="rose",
    message="Thanks for joining our channel!"
)
if result['ok']:
    Api.sendMessage("🌹 Gift sent!")
else:
    Api.sendMessage(f"❌ Could not send gift: {result['error']}")
# Check price range for budgeting
prices = Lib.TeleGifts.getGiftPriceRange()
Api.sendMessage(f"Gifts range from {prices['min_stars']} to {prices['max_stars']} Stars")
# View sending history and stats
history = Lib.TeleGifts.getGiftHistory(limit=10)
stats = Lib.TeleGifts.getGiftStats()
Api.sendMessage(f"Total gifts sent: {stats['total_sent']} ({stats['total_stars_spent']} Stars spent)")
```
**Use Cases:**
* Rewarding loyal users
* Giveaway prizes
* Referral bonuses
* Milestone celebrations
* Customer appreciation campaigns
***
## Growth & Marketing Libraries
### Lib.RefLib
Complete referral tracking system for viral growth and user acquisition.
#### Core Methods
| Method | Parameters | Returns | Description |
| ---------------- | ----------------------------------------------------------- | --------- | ----------------------------- |
| `getLink` | `bot_name` (str, optional), `prefix` (str, optional) | str | Generate unique referral link |
| `track` | `on_attracted`, `on_touch_own_link`, `on_already_attracted` | bool | Track referral from /start |
| `getRefList` | `user_id` (str, optional) | list | Get list of referred users |
| `getRefCount` | `user_id` (str, optional) | int | Get total referral count |
| `getTopList` | `limit` (int, optional) | dict | Get referral leaderboard |
| `getAttractedBy` | None | dict/None | Get referrer information |
| `getRank` | `user_id` (str, optional) | int | Get leaderboard position |
| `getStats` | `user_id` (str, optional) | dict | Get comprehensive statistics |
#### Examples
```python
# Generate referral link
link = Lib.RefLib.getLink()
Api.sendMessage(f"🔗 Your link: {link}")
# Track referrals in /start command
Lib.RefLib.track(
on_attracted=lambda ref: Api.sendMessage(f"🎉 New referral: {ref['first_name']}!"),
on_touch_own_link=lambda: Api.sendMessage("❌ Can't refer yourself!"),
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
)
# Show user stats
count = Lib.RefLib.getRefCount()
rank = Lib.RefLib.getRank()
Api.sendMessage(f"📊 Referrals: {count} | Rank: #{rank}")
# Display leaderboard
top = Lib.RefLib.getTopList(limit=10)
message = "🏆 Top Referrers:\n"
for i, (user_id, count) in enumerate(top.items(), 1):
message += f"{i}. User {user_id}: {count}\n"
Api.sendMessage(message)
# Get referral list
refs = Lib.RefLib.getRefList()
for ref in refs:
Api.sendMessage(f"• {ref['first_name']} - {ref['date']}")
# Check who referred current user
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(f"Referred by: {referrer['first_name']}")
```
**Use Cases:**
* Viral growth campaigns
* Referral reward programs
* Multi-level marketing
* Affiliate tracking
* User acquisition contests
* Community building
***
## Integration Libraries
### Lib.Webhook
Generate webhook URLs for external integrations and bot-to-bot communication.
#### Method
| Method | Parameters | Description |
| ----------- | ----------------------------------------------------------------- | -------------------- |
| `getUrlFor` | `command`, `user_id`, `chat_id`, `bot_id`, `api_key`, `**options` | Generate webhook URL |
#### Examples
```python
# Basic webhook
webhook = Lib.Webhook.getUrlFor(
command="process_payment",
user_id=u
)
Api.sendMessage(f"Payment webhook: {webhook}")
# Bot-to-bot webhook
webhook = Lib.Webhook.getUrlFor(
command="sync_data",
bot_id="other_bot_id",
api_key="other_bot_key"
)
# Webhook with options
webhook = Lib.Webhook.getUrlFor(
command="notify",
user_id=u,
redirect_to="https://example.com/success"
)
# In webhook command, access data
data = options.get("data")
json_data = options.get("json")
```
**New in v1.1.0:** commands triggered via a webhook URL can now also read the caller's request headers and IP address directly:
```python
# In a webhook-triggered command
caller_ip = options.ip
custom_header = options.headers.get("X-Custom-Header")
```
**New in v1.1.0 — Webhook Result Sync:** webhook-triggered commands can send a real response back to the external caller in the same request, using `Bot.setWebhookResponse()` (or `Api.setWebhookResponse()`):
```python
# In a webhook-triggered command
result = {"status": "verified", "user_id": u}
Bot.setWebhookResponse(result)
# The external caller's HTTP request receives this result directly
```
**Use Cases:**
* Payment notifications
* Bot-to-bot communication
* External API callbacks
* Event notifications
* Data synchronization
***
## Practical Examples
### Complete Referral Reward Bot
```python
# /start command - Track referrals
def handle_referral(ref):
# Reward new user
User.res("points").add(100)
Api.sendMessage("🎉 You earned 100 points!")
# Reward referrer
User.resOf("points", ref['id']).add(50)
Api.sendMessage(
chat_id=ref['id'],
text=f"✅ {message.from_user.first_name} joined! +50 points"
)
Lib.RefLib.track(
on_attracted=handle_referral,
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
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
oxapay = Lib.Oxapay.client("merchant_key")
address = oxapay.createAddress(
network="BSC",
callback_url=Lib.Webhook.getUrlFor("payment_received", user_id=u)
)
User.storeData("payment_address", address['data']['address'])
User.storeData("payment_track", address['data']['track_id'])
Api.sendMessage(f"💰 Send USDT (BSC) to:\n`{address['data']['address']}`")
# In payment_received command
track_id = User.fetchData("payment_track")
status = oxapay.invoice(track_id)
if status['data']['status'] == "Paid":
Api.sendMessage("✅ Payment confirmed! Activating premium...")
User.storeData("premium", True)
```
### AI Assistant Bot
```python
# Initialize AI
ai = Lib.AI.client(provider="openai", apiKey="sk-...")
# Get or create thread
thread_id = User.fetchData("ai_thread")
if not thread_id:
thread = ai.createThread()
thread_id = thread["id"]
User.storeData("ai_thread", thread_id)
# Chat
ai.addMessage(thread_id, "user", msg)
run = ai.run(thread_id, "assistant_id")
# Wait and get response
time.sleep(2)
messages = ai.getMessages(thread_id, limit=1)
response = messages["data"][0]["content"][0]["text"]["value"]
Api.sendMessage(response)
```
### Leaderboard System
```python
# Create leaderboard
leaderboard = Lib.CSV.Table("game_scores.csv")
# Initialize if needed
if leaderboard.count() == 0:
leaderboard.create(["user_id", "username", "score", "date"])
# Add/update score
score = 1500
user_name = message.from_user.first_name
# Check if user exists
existing = leaderboard.find(user_id=str(u))
if existing:
# Update score
for i, row in enumerate(leaderboard.get()):
if row["user_id"] == str(u):
if int(row["score"]) < score:
leaderboard.update(i, {"score": score})
Api.sendMessage(f"🎉 New high score: {score}!")
break
else:
# Add new entry
leaderboard.insert({
"user_id": str(u),
"username": user_name,
"score": score,
"date": Lib.DateTime.date_now()
})
# Show top 10
all_scores = sorted(leaderboard.get(), key=lambda x: int(x["score"]), reverse=True)
message = "🏆 Top 10 Leaderboard:\n\n"
for i, player in enumerate(all_scores[:10], 1):
message += f"{i}. {player['username']}: {player['score']}\n"
Api.sendMessage(message)
```
### Random Giveaway
```python
# Collect participants
participants = Lib.CSV.Table("giveaway.csv")
if participants.count() == 0:
participants.create(["user_id", "username"])
# Add participant
participants.insert({
"user_id": str(u),
"username": message.from_user.first_name
})
Api.sendMessage("✅ You're entered in the giveaway!")
# Select winner (in admin command)
all_participants = participants.get()
if len(all_participants) > 0:
winner_index = Lib.Random.integer(0, len(all_participants) - 1)
winner = all_participants[winner_index]
Api.sendMessage(f"🎊 Winner: {winner['username']} (ID: {winner['user_id']})")
```
***
### Gift Reward Bot *(New in v1.1.0)*
```python
# Reward a user with a gift after they complete an action
result = Lib.TeleGifts.sendGift(
    user_id=u,
    gift_key="teddy_bear",
    message="Thanks for being an awesome member!"
)
if result['ok']:
    Api.sendMessage("🧸 Enjoy your gift!")
else:
    Api.sendMessage("Sorry, we couldn't send your gift right now.")
```
## Best Practices
### Security
1. **Never expose API keys in messages**
```python
# Bad
Api.sendMessage(f"Your API key: {api_key}")
# Good
User.storeData("api_key", api_key)
Api.sendMessage("API key saved securely!")
```
2. **Validate webhook data**
```python
# In webhook command
if "json" in options:
data = options["json"]
# Validate expected fields
if "amount" in data and "status" in data:
# Process payment
pass
```
3. **Verify webhook signatures before trusting incoming data** *(New in v1.1.0)*
```python
# In webhook command
is_valid = Lib.Security.verifyHMAC(webhook_secret, options.data, options.headers.get("X-Signature"))
if not is_valid:
    Bot.setWebhookResponse({"ok": False, "error": "Invalid signature"})
    raise StopExecution()
```
### Performance
1. **Reuse AI threads**
```python
# Store thread ID to avoid creating new threads
thread_id = User.fetchData("ai_thread")
if not thread_id:
thread = ai.createThread()
User.storeData("ai_thread", thread["id"])
```
2. **Cache API responses**
```python
# Cache crypto prices (update every 5 minutes)
last_update = User.fetchData("price_update_time") or 0
current_time = Lib.DateTime.time()
if current_time - last_update > 300: # 5 minutes
price = Lib.Crypto.get_price("bitcoin", "usd")
User.storeData("btc_price", price['bitcoin']['usd'])
User.storeData("price_update_time", current_time)
else:
price = User.fetchData("btc_price")
```
### Error Handling
1. **Handle API errors gracefully**
```python
try:
tx_hash = Lib.EVM.sendCoin(
value=0.1,
to=recipient,
network="ethereum"
)
Api.sendMessage(f"✅ Sent! TX: {tx_hash}")
except Exception as e:
Api.sendMessage(f"❌ Error: {str(e)}")
# Log error for admin
Bot.storeData("last_error", str(e))
```
***
## Summary
TBS Libraries provide everything you need to build sophisticated Telegram bots:
| Library               | Purpose                 | Key Features                                                                                                                                    |
| --------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Random**            | Randomization           | Integers, strings, decimals, ASCII, UUIDs, passwords, weighted choices, and more                                                                |
| **DateTime**          | Time management         | UTC time, timestamps, timezones                                                                                                                 |
| **CSV**               | Data storage            | Tables, queries, export/import                                                                                                                  |
| **PIL** *(new)*       | Image editing           | Resize, crop, draw, filters, watermarks — [see full docs](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation)          |
| **CV** *(new)*        | Computer vision         | Face detection, contours, perspective transforms — [see full docs](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation) |
| **Security** *(new)*  | Cryptography            | HMAC, Ed25519, AES encryption, hashing                                                                                                          |
| **EVM**               | EVM blockchains         | 31+ networks, tokens, native coins, balance checking                                                                                            |
| **TON**               | TON blockchain          | Wallets, jettons, TON Connect                                                                                                                   |
| **AI**                | Artificial Intelligence | OpenAI, Gemini, assistants                                                                                                                      |
| **Oxapay**            | Crypto payments         | Invoices, payouts, tracking                                                                                                                     |
| **Crypto**            | Price data              | Real-time prices, conversions                                                                                                                   |
| **TeleGifts** *(new)* | Telegram Gifts          | Send Stars-based gifts, catalog, history tracking                                                                                               |
| **RefLib**            | Referral system         | Link generation, tracking, leaderboards                                                                                                         |
| **Webhook**           | Integrations            | External callbacks, bot communication, synchronous responses                                                                                    |
All libraries are:
* ✅ Pre-loaded and ready to use
* ✅ No installation or imports needed
* ✅ Production-tested and reliable
* ✅ Fully documented with examples
* ✅ Designed for TBS environment
Start building powerful bots today with TBS Libraries!
***
*For more information, visit* [*TeleBotStudio.com*](https://TeleBotStudio.com)
