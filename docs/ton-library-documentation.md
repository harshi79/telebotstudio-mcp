# TON Library Documentation
The TON Library in TeleBot Studio enables seamless integration with The Open Network (TON) blockchain. Build powerful cryptocurrency bots with wallet management, transactions, balance checking, and TON Connect integration.
***
## Introduction
The TON Library (`Lib.TON`) provides comprehensive blockchain functionality without requiring complex setup or external dependencies. All functions are pre-loaded and ready to use in your TeleBot Studio bots.
**Key Features:**
* Wallet creation and management
* TON cryptocurrency transfers
* Balance checking
* Transaction history
* TON Connect integration
* Jetton (token) operations
* Testnet and mainnet support
***
## Getting Started
The TON Library is globally available - no import statements needed:
```python
# ✅ Correct - Direct usage
wallet = Lib.TON.createWallet()
# ❌ Wrong - No imports allowed
# import Lib.TON # This will cause an error
```
***
## Wallet Management
### Lib.TON.createWallet()
Creates a new TON wallet with a unique address and mnemonic phrase.
**Syntax:**
```python
Lib.TON.createWallet()
```
**Returns:** Dictionary with:
* `address` (str): Wallet address (user-friendly format)
* `mnemonics` (str): 24-word recovery phrase
**Example:**
```python
# /create_wallet command
wallet = Lib.TON.createWallet()
Api.sendMessage("🔐 New TON Wallet Created!")
Api.sendMessage(f"📍 Address:\n`{wallet['address']}`")
Api.sendMessage(f"🔑 Mnemonic (SAVE THIS SAFELY):\n`{wallet['mnemonics']}`")
Api.sendMessage("\n⚠️ Never share your mnemonic phrase with anyone!")
# Store mnemonics securely for future use
Lib.TON.storeKey(wallet['mnemonics'])
User.storeData("ton_address", wallet['address'])
```
***
### Lib.TON.storeKey()
Securely stores a mnemonic phrase for later use.
**Syntax:**
```python
Lib.TON.storeKey(mnemonics)
```
**Parameters:**
* `mnemonics` (Required): 24-word mnemonic phrase as a string
**Returns:** Boolean (True on success)
**Example:**
```python
# /import_wallet command
Api.sendMessage("Please send your 24-word mnemonic phrase:")
Bot.waitForInput("save_mnemonics")
# In save_mnemonics command
mnemonics = msg
# Validate mnemonic format
words = mnemonics.split()
if len(words) != 24:
Api.sendMessage("❌ Invalid mnemonic. Must be exactly 24 words.")
Api.sendMessage("Try again: /import_wallet")
else:
try:
# Store and verify
Lib.TON.storeKey(mnemonics)
address = Lib.TON.getAddress()
Api.sendMessage("✅ Wallet imported successfully!")
Api.sendMessage(f"Address: `{address}`")
User.storeData("ton_address", address)
except Exception as e:
Api.sendMessage(f"❌ Error: {str(e)}")
```
**Security Note:** Mnemonic phrases grant full access to wallets. Store them securely and never expose them in logs or messages.
***
### Lib.TON.getAddress()
Retrieves the wallet address from stored or provided mnemonics.
**Syntax:**
```python
Lib.TON.getAddress(mnemonics=None)
```
**Parameters:**
* `mnemonics` (Optional): 24-word mnemonic phrase. If None, uses stored mnemonics.
**Returns:** String containing the wallet address
**Example - Using Stored Mnemonics:**
```python
# /my_wallet command
try:
address = Lib.TON.getAddress()
Api.sendMessage(f"Your TON address:\n`{address}`")
except ValueError as e:
Api.sendMessage("❌ No wallet found. Create one: /create_wallet")
```
**Example - Using Specific Mnemonics:**
```python
# Get address without storing
mnemonics = "word1 word2 word3 ... word24"
address = Lib.TON.getAddress(mnemonics=mnemonics)
Api.sendMessage(f"Address: {address}")
```
***
## TON Operations
### Lib.TON.balance()
Checks the TON balance of any address.
**Syntax:**
```python
Lib.TON.balance(address, api_key=None, endpoint=None, is_testnet=False)
```
**Parameters:**
* `address` (Required): TON wallet address to check
* `api_key` (Optional): TON Center API key for higher rate limits
* `endpoint` (Optional): Custom RPC endpoint URL
* `is_testnet` (Optional): If True, uses testnet (default: False)
**Returns:** Float representing balance in TON
**Example - Check Own Balance:**
```python
# /balance command
address = User.fetchData("ton_address")
if not address:
Api.sendMessage("No wallet found. Create one: /create_wallet")
else:
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"💰 Your Balance:")
Api.sendMessage(f"{balance} TON")
# Convert to USD (example rate)
usd_value = balance * 2.50 # Example: 1 TON = $2.50
Api.sendMessage(f"≈ ${usd_value:.2f} USD")
except Exception as e:
Api.sendMessage(f"Error checking balance: {str(e)}")
```
**Example - Check Any Address:**
```python
# /check_balance command
Api.sendMessage("Send me a TON address to check:")
Bot.waitForInput("process_balance_check")
# In process_balance_check command
address = msg
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"Address: {address[:10]}...{address[-10:]}")
Api.sendMessage(f"Balance: {balance} TON")
except Exception as e:
Api.sendMessage(f"Invalid address or error: {str(e)}")
```
**Example - Testnet Balance:**
```python
# Check testnet balance
testnet_balance = Lib.TON.balance(address, is_testnet=True)
Api.sendMessage(f"Testnet balance: {testnet_balance} TON")
```
***
### Lib.TON.send()
Sends TON cryptocurrency to another address.
**Syntax:**
```python
Lib.TON.send(
to_address,
amount,
comment=None,
mnemonics=None,
api_key=None,
endpoint=None,
is_testnet=False
)
```
**Parameters:**
* `to_address` (Required): Recipient's TON address
* `amount` (Required): Amount of TON to send (float)
* `comment` (Optional): Transaction comment/memo
* `mnemonics` (Optional): Sender's mnemonic phrase (uses stored if None)
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
* `is_testnet` (Optional): Use testnet if True
**Returns:** Dictionary with:
* `ok` (bool): Success status
* `tx` (dict): Transaction details including:
* `hash` (str): Transaction hash
* `lt` (int): Logical time
* `seqno` (int): Sequence number
* `to_address` (str): Recipient address
* `from_address` (str): Sender address
* `amount_ton` (float): Amount sent
* `comment` (str): Transaction comment
**Example - Basic Send:**
```python
# /send_ton command
Api.sendMessage("Recipient address:")
Bot.waitForInput("get_recipient")
# In get_recipient command
recipient = msg
User.storeData("send_recipient", recipient)
Api.sendMessage("Amount to send (in TON):")
Bot.waitForInput("get_amount")
# In get_amount command
amount_str = msg
if not amount_str.replace('.', '').isdigit():
Api.sendMessage("Invalid amount. Try again: /send_ton")
else:
amount = float(amount_str)
recipient = User.fetchData("send_recipient")
# Confirm transaction
Api.sendMessage("📤 Confirm Transaction:")
Api.sendMessage(f"To: {recipient[:10]}...{recipient[-10:]}")
Api.sendMessage(f"Amount: {amount} TON")
Api.sendMessage("Confirm? /confirm_send or /cancel")
# In confirm_send command
try:
recipient = User.fetchData("send_recipient")
amount = float(User.fetchData("send_amount"))
Api.sendMessage("⏳ Processing transaction...")
result = Lib.TON.send(
to_address=recipient,
amount=amount,
comment="Payment via TeleBot Studio"
)
if result['ok']:
tx = result['tx']
Api.sendMessage("✅ Transaction Successful!")
Api.sendMessage(f"Hash: `{tx['hash']}`")
Api.sendMessage(f"Amount: {tx['amount_ton']} TON")
Api.sendMessage(f"Fee: ~0.01 TON")
else:
Api.sendMessage("❌ Transaction failed")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
**Example - Send with Comment:**
```python
result = Lib.TON.send(
to_address="EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
amount=0.5,
comment="Payment for service #12345"
)
```
**Example - Check Balance Before Sending:**
```python
address = Lib.TON.getAddress()
balance = Lib.TON.balance(address)
amount_to_send = 1.5
if balance < amount_to_send + 0.02: # Include estimated fee
Api.sendMessage(f"Insufficient balance. You have {balance} TON")
Api.sendMessage(f"Need at least {amount_to_send + 0.02} TON")
else:
result = Lib.TON.send(to_address=recipient, amount=amount_to_send)
Api.sendMessage("Transaction sent!")
```
***
### Lib.TON.transactions()
Retrieves transaction history for an address.
**Syntax:**
```python
Lib.TON.transactions(address, limit=10, api_key=None, endpoint=None, is_testnet=False)
```
**Parameters:**
* `address` (Required): TON wallet address
* `limit` (Optional): Number of transactions to retrieve (default: 10)
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
* `is_testnet` (Optional): Use testnet if True
**Returns:** List of transaction dictionaries
**Example - View Recent Transactions:**
```python
# /transactions command
address = User.fetchData("ton_address")
if not address:
Api.sendMessage("No wallet found. Create one: /create_wallet")
else:
try:
txs = Lib.TON.transactions(address, limit=5)
Api.sendMessage(f"📜 Recent Transactions ({len(txs)}):")
for idx, tx in enumerate(txs, 1):
tx_type = "Incoming" if tx.get('in_msg') else "Outgoing"
amount = tx.get('amount', 0) / 1000000000 # Convert from nanotons
Api.sendMessage(f"\n{idx}. {tx_type}")
Api.sendMessage(f"Amount: {amount:.4f} TON")
Api.sendMessage(f"Time: {tx.get('utime', 'Unknown')}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
**Example - Monitor Incoming Payments:**
```python
# Check for new payments
last_checked = User.fetchData("last_tx_check") or 0
address = User.fetchData("ton_address")
txs = Lib.TON.transactions(address, limit=20)
for tx in txs:
tx_time = tx.get('utime', 0)
if tx_time > last_checked and tx.get('in_msg'):
# New incoming payment
amount = tx.get('amount', 0) / 1000000000
Api.sendMessage(f"💰 New payment received: {amount:.4f} TON")
# Award points or credits
points = User.res("points")
points.add(int(amount * 100)) # 100 points per TON
User.storeData("last_tx_check", time.time())
```
***
## TON Connect Integration
TON Connect allows users to connect their existing wallets to your bot for secure, wallet-based authentication and transactions.
### Lib.TON.connectSession()
Creates a TON Connect session for wallet connection.
**Syntax:**
```python
Lib.TON.connectSession(user_id, expiry_seconds=86400)
```
**Parameters:**
* `user_id` (Required): Unique identifier for the user
* `expiry_seconds` (Optional): Session expiration time (default: 86400 = 24 hours)
**Returns:** Dictionary with:
* `session_id` (str): Unique session identifier
* `connect_url` (str): QR code / deep link URL for wallet connection
**Example:**
```python
# /connect_wallet command
session = Lib.TON.connectSession(user_id=str(u))
Api.sendMessage("🔗 Connect Your TON Wallet")
Api.sendMessage("Scan this QR code with your TON wallet:")
Api.sendMessage(f"`{session['connect_url']}`")
Api.sendMessage("\nOr open this link in your wallet app:")
Api.sendMessage(session['connect_url'])
# Store session ID
User.storeData("ton_connect_session", session['session_id'])
Api.sendMessage("\nOnce connected, use /check_connection")
```
***
### Lib.TON.verifySession()
Checks if a wallet has connected to the session.
**Syntax:**
```python
Lib.TON.verifySession(session_id)
```
**Parameters:**
* `session_id` (Required): Session ID from connectSession
**Returns:** Dictionary with:
* `status` (str): "connected" or "pending"
* `wallet_address` (str): Connected wallet address (if connected)
* `public_key` (str): Public key (if connected)
**Example:**
```python
# /check_connection command
session_id = User.fetchData("ton_connect_session")
if not session_id:
Api.sendMessage("No connection attempt found. Start: /connect_wallet")
else:
status = Lib.TON.verifySession(session_id)
if status['status'] == "connected":
wallet = status['wallet_address']
Api.sendMessage("✅ Wallet Connected!")
Api.sendMessage(f"Address: `{wallet}`")
# Store connected wallet
User.storeData("connected_wallet", wallet)
User.removeData("ton_connect_session")
else:
Api.sendMessage("⏳ Wallet not connected yet")
Api.sendMessage("Please scan the QR code with your wallet")
```
***
### Lib.TON.register_ton_connect_wallet() *(Added in v1.1.0)*
Marks a TON Connect session as connected and stores the wallet address — call this from your own callback once a wallet approves the connection request.
**Syntax:**
```python
Lib.TON.register_ton_connect_wallet(session_id, wallet_address)
```
**Parameters:**
* `session_id` (Required): The session ID from `connectSession()`
* `wallet_address` (Required): The wallet address that approved the connection
**Returns:** Dictionary with:
* `ok` (bool): Success status
* `session_id` (str): The session that was updated
* `wallet_address` (str): The wallet address that was registered
* `error` (str): Error message if `ok` is False
**Example:**
```python
# In your wallet-connection callback command, once the wallet approves:
session_id = User.fetchData("ton_connect_session")
approved_wallet = "EQD4FPq-PRDieyQKkizFTRtSDyucUIqrj0v_zXJmqaDp6_0t"
result = Lib.TON.register_ton_connect_wallet(session_id, approved_wallet)
if result['ok']:
    Api.sendMessage("✅ Wallet successfully linked!")
    User.storeData("connected_wallet", approved_wallet)
else:
    Api.sendMessage(f"❌ Could not link wallet: {result['error']}")
```
***
### Lib.TON.requestPayment()
Requests a TON transfer from a connected wallet.
**Syntax:**
```python
Lib.TON.requestPayment(
to_address,
amount,
comment=None,
callback_url="",
return_url=None
)
```
**Parameters:**
* `to_address` (Required): Recipient address
* `amount` (Required): Amount in TON
* `comment` (Optional): Transaction comment
* `callback_url` (Optional): Webhook URL for payment confirmation
* `return_url` (Optional): URL to return to after payment
**Returns:** Payment request object
**Example:**
```python
# /pay command
connected_wallet = User.fetchData("connected_wallet")
if not connected_wallet:
Api.sendMessage("Connect wallet first: /connect_wallet")
else:
# Merchant address
merchant_address = "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N"
payment_request = Lib.TON.requestPayment(
to_address=merchant_address,
amount=1.0,
comment=f"Order #{Bot.uniqueID()}",
callback_url=Lib.Webhook.getUrlFor("payment_confirmed", user_id=u)
)
Api.sendMessage("💳 Payment Request Sent")
Api.sendMessage("Approve the transaction in your wallet")
# In payment_confirmed command
payment_data = options
Api.sendMessage("✅ Payment confirmed!")
Api.sendMessage("Thank you for your purchase!")
# Grant access or deliver product
User.storeData("premium_member", True)
```
***
## Jetton Operations
Jettons are tokens on the TON blockchain (similar to ERC-20 on Ethereum).
### Lib.TON.tokenInfo()
Retrieves metadata about a Jetton (token).
**Syntax:**
```python
Lib.TON.tokenInfo(jetton_master_address, api_key=None, endpoint=None, is_testnet=False)
```
**Parameters:**
* `jetton_master_address` (Required): Master contract address of the Jetton
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
* `is_testnet` (Optional): Use testnet if True
**Returns:** Dictionary with token metadata:
* `name` (str): Token name
* `symbol` (str): Token symbol
* `decimals` (int): Number of decimals
* `total_supply` (str): Total supply
**Example:**
```python
# /token_info command
jetton_address = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
try:
token = Lib.TON.tokenInfo(jetton_address)
Api.sendMessage("🪙 Token Information:")
Api.sendMessage(f"Name: {token['name']}")
Api.sendMessage(f"Symbol: {token['symbol']}")
Api.sendMessage(f"Decimals: {token['decimals']}")
Api.sendMessage(f"Supply: {token['total_supply']}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
***
### Lib.TON.get_jetton_wallet_address() *(Added in v1.1.0)*
Resolves the Jetton wallet address for a specific owner, without needing a full balance lookup.
**Syntax:**
```python
Lib.TON.get_jetton_wallet_address(owner_address, jetton_master_address, api_key=None, endpoint=None)
```
**Parameters:**
* `owner_address` (Required): The wallet address that owns (or would own) the Jetton
* `jetton_master_address` (Required): Master contract address of the Jetton
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
**Returns:** String containing the resolved Jetton wallet address
**Example:**
```python
# /jetton_wallet command
owner_address = User.fetchData("ton_address")
jetton_address = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
try:
    jetton_wallet = Lib.TON.get_jetton_wallet_address(owner_address, jetton_address)
    Api.sendMessage(f"Your Jetton wallet address:\n`{jetton_wallet}`")
except Exception as e:
    Api.sendMessage(f"Error: {str(e)}")
```
***
### Lib.TON.tokenBalance()
Checks Jetton token balance for an address.
**Syntax:**
```python
Lib.TON.tokenBalance(
owner_address,
jetton_master_address,
api_key=None,
endpoint=None,
is_testnet=False
)
```
**Parameters:**
* `owner_address` (Required): Wallet address to check
* `jetton_master_address` (Required): Master contract of the Jetton
* `api_key` (Optional): TON Center API key
* `endpoint` (Optional): Custom RPC endpoint
* `is_testnet` (Optional): Use testnet if True
**Returns:** Float representing token balance
**Example:**
```python
# /token_balance command
user_address = User.fetchData("ton_address")
jetton_address = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
if not user_address:
Api.sendMessage("No wallet found. Create one: /create_wallet")
else:
try:
balance = Lib.TON.tokenBalance(user_address, jetton_address)
token_info = Lib.TON.tokenInfo(jetton_address)
Api.sendMessage(f"💰 {token_info['symbol']} Balance:")
Api.sendMessage(f"{balance} {token_info['symbol']}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
***
### Lib.TON.requestToken()
Requests a Jetton transfer from a connected wallet.
**Syntax:**
```python
Lib.TON.requestToken(
to_address,
jetton_master_address,
amount,
comment=None,
callback_url="",
return_url=None
)
```
**Parameters:**
* `to_address` (Required): Recipient address
* `jetton_master_address` (Required): Master contract of the Jetton
* `amount` (Required): Amount of tokens
* `comment` (Optional): Transaction comment
* `callback_url` (Optional): Webhook for confirmation
* `return_url` (Optional): Return URL
**Returns:** Token transfer request object
**Example:**
```python
# /send_tokens command
connected_wallet = User.fetchData("connected_wallet")
if not connected_wallet:
Api.sendMessage("Connect wallet first: /connect_wallet")
else:
recipient = "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N"
jetton = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
request = Lib.TON.requestToken(
to_address=recipient,
jetton_master_address=jetton,
amount=100,
comment="Token payment"
)
Api.sendMessage("Token transfer request sent to your wallet")
Api.sendMessage("Approve the transaction to complete")
```
***
## Real-World Use Cases
### 1. Crypto Payment Bot
```python
# /start command
Api.sendMessage("Welcome to Crypto Payment Bot!")
Api.sendMessage("Commands:")
Api.sendMessage("/create_wallet - Create new wallet")
Api.sendMessage("/import_wallet - Import existing wallet")
Api.sendMessage("/balance - Check balance")
Api.sendMessage("/receive - Get payment address")
Api.sendMessage("/send - Send TON")
# /receive command
address = User.fetchData("ton_address")
if address:
Api.sendMessage("💰 Receive TON:")
Api.sendMessage(f"`{address}`")
Api.sendMessage("Share this address to receive payments")
else:
Api.sendMessage("Create wallet first: /create_wallet")
```
***
### 2. Automated Payment Processing
```python
# Monitor for payments
# /check_payments command (scheduled every 5 minutes)
address = Bot.fetchData("merchant_address")
last_check = Bot.fetchData("last_payment_check") or 0
txs = Lib.TON.transactions(address, limit=50)
for tx in txs:
if tx.get('utime', 0) > last_check and tx.get('in_msg'):
amount = tx.get('amount', 0) / 1000000000
sender = tx.get('source', 'Unknown')
# Find user by amount or comment
order_id = extract_order_id(tx.get('comment', ''))
if order_id:
# Process order
process_order(order_id, amount)
Api.sendMessage(f"✅ Payment received for order #{order_id}", chat_id=get_user_by_order(order_id))
Bot.storeData("last_payment_check", time.time())
```
***
### 3. TON Connect Authentication
```python
# /login command
session = Lib.TON.connectSession(user_id=str(u))
User.storeData("auth_session", session['session_id'])
Api.sendMessage("🔐 Login with TON Connect")
Api.sendMessage("Scan QR code with your wallet:")
Api.sendMessage(session['connect_url'])
# Schedule verification check
Bot.scheduleCommand(5, "verify_login")
# verify_login command
session_id = User.fetchData("auth_session")
status = Lib.TON.verifySession(session_id)
if status['status'] == "connected":
wallet = status['wallet_address']
User.storeData("authenticated_wallet", wallet)
User.storeData("logged_in", True)
Api.sendMessage("✅ Logged in successfully!")
Api.sendMessage("Welcome back!")
else:
Bot.scheduleCommand(5, "verify_login") # Check again in 5 seconds
```
***
### 4. Token Gated Access
```python
# /premium command
address = User.fetchData("ton_address")
token_contract = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
if not address:
Api.sendMessage("Connect wallet: /connect_wallet")
else:
balance = Lib.TON.tokenBalance(address, token_contract)
if balance >= 100: # Requires 100 tokens
Api.sendMessage("✅ Premium Access Granted!")
User.storeData("premium", True)
Api.sendMessage("Access premium features: /premium_features")
else:
Api.sendMessage(f"❌ Insufficient tokens")
Api.sendMessage(f"You have: {balance}")
Api.sendMessage(f"Required: 100")
```
***
## Best Practices
### 1. Security
**Never log or expose mnemonic phrases:**
```python
# ❌ Wrong
Api.sendMessage(f"Your mnemonics: {mnemonics}")
# ✅ Correct
Api.sendMessage("Mnemonics sent privately (check your saved messages)")
# Use user's Saved Messages or encrypt before sending
```
**Validate addresses:**
```python
def is_valid_ton_address(address):
# Basic validation
if not address.startswith("EQ") and not address.startswith("UQ"):
return False
if len(address) != 48:
return False
return True
if not is_valid_ton_address(recipient):
Api.sendMessage("Invalid TON address format")
```
### 2. Error Handling
**Always wrap blockchain operations in try-except:**
```python
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"Balance: {balance} TON")
except ConnectionError:
Api.sendMessage("Network error. Please try again.")
except ValueError as ve:
Api.sendMessage(f"Invalid address: {str(ve)}")
except Exception as e:
error_id = Bot.errorID()
Api.sendMessage(f"Error {error_id}: {str(e)}")
```
### 3. Testnet First
**Test on testnet before mainnet:**
```python
# Development: Use testnet
IS_TESTNET = True
balance = Lib.TON.balance(address, is_testnet=IS_TESTNET)
result = Lib.TON.send(to_address=addr, amount=0.1, is_testnet=IS_TESTNET)
# Production: Use mainnet
IS_TESTNET = False
```
### 4. Transaction Confirmation
**Always confirm before sending:**
```python
# Show confirmation
Api.sendMessage("⚠️ Confirm Transaction:")
Api.sendMessage(f"To: {recipient}")
Api.sendMessage(f"Amount: {amount} TON")
Api.sendMessage(f"Fee: ~0.01 TON")
Api.sendMessage("\n/confirm to proceed\n/cancel to abort")
Bot.waitForInput("handle_confirmation")
```
### 5. Rate Limiting
**Respect API rate limits:**
```python
# Cache balances for 1 minute
cached_balance = User.fetchData("cached_balance")
cache_time = User.fetchData("cache_time") or 0
if time.time() - cache_time < 60:
Api.sendMessage(f"Balance: {cached_balance} TON (cached)")
else:
balance = Lib.TON.balance(address)
User.storeData("cached_balance", balance)
User.storeData("cache_time", time.time())
Api.sendMessage(f"Balance: {balance} TON")
```
***
## Platform Limitations
* **Code execution timeout:** 160 seconds maximum
* **Sleep function:** 10 seconds maximum
* **No import statements:** All libraries are pre-loaded
***
## Troubleshooting
### Common Issues
**"No mnemonics provided or stored"**
```python
# Solution: Store mnemonics first
Lib.TON.storeKey("your 24 word mnemonic phrase")
```
**"Insufficient balance"**
```python
# Solution: Check balance before sending
balance = Lib.TON.balance(address)
if balance < amount + 0.02: # Include fee
Api.sendMessage("Insufficient funds")
```
**"Network timeout"**
```python
# Solution: Retry with exponential backoff
attempts = 0
max_attempts = 3
while attempts < max_attempts:
try:
balance = Lib.TON.balance(address)
break
except:
attempts += 1
if attempts < max_attempts:
time.sleep(2 ** attempts) # 2, 4, 8 seconds
else:
Api.sendMessage("Network error after multiple attempts")
```
***
## Further Resources
* **TON Documentation:** 
* **TON Connect:** 
* **Testnet Faucet:** 
* **Block Explorer:** 
***
The TON Library in TeleBot Studio provides everything you need to build powerful cryptocurrency bots on the TON blockchain. Start building today!
