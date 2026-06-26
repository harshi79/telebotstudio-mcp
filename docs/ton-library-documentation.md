> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/ton-library-documentation.md).
# TON Library Documentation
The TON Library in TeleBot Studio enables seamless integration with The Open Network (TON) blockchain. Build powerful cryptocurrency bots with wallet management, transactions, balance checking, and TON Connect integration.
\*\*\*
## Introduction
The TON Library (`Lib.TON`) provides comprehensive blockchain functionality without requiring complex setup or external dependencies. All functions are pre-loaded and ready to use in your TeleBot Studio bots.
\*\*Key Features:\*\*
\* Wallet creation and management
\* TON cryptocurrency transfers
\* Balance checking
\* Transaction history
\* TON Connect integration
\* Jetton (token) operations
\* Testnet and mainnet support
\*\*\*
## Getting Started
The TON Library is globally available - no import statements needed:
```python
# ✅ Correct - Direct usage
wallet = Lib.TON.createWallet()
# ❌ Wrong - No imports allowed
# import Lib.TON # This will cause an error
```
\*\*\*
## Wallet Management
### Lib.TON.createWallet()
Creates a new TON wallet with a unique address and mnemonic phrase.
\*\*Syntax:\*\*
```python
Lib.TON.createWallet()
```
\*\*Returns:\*\* Dictionary with:
\* `address` (str): Wallet address (user-friendly format)
\* `mnemonics` (str): 24-word recovery phrase
\*\*Example:\*\*
```python
# /create\_wallet command
wallet = Lib.TON.createWallet()
Api.sendMessage("🔐 New TON Wallet Created!")
Api.sendMessage(f"📍 Address:\n`{wallet['address']}`")
Api.sendMessage(f"🔑 Mnemonic (SAVE THIS SAFELY):\n`{wallet['mnemonics']}`")
Api.sendMessage("\n⚠️ Never share your mnemonic phrase with anyone!")
# Store mnemonics securely for future use
Lib.TON.storeKey(wallet['mnemonics'])
User.storeData("ton\_address", wallet['address'])
```
\*\*\*
### Lib.TON.storeKey()
Securely stores a mnemonic phrase for later use.
\*\*Syntax:\*\*
```python
Lib.TON.storeKey(mnemonics)
```
\*\*Parameters:\*\*
\* `mnemonics` (Required): 24-word mnemonic phrase as a string
\*\*Returns:\*\* Boolean (True on success)
\*\*Example:\*\*
```python
# /import\_wallet command
Api.sendMessage("Please send your 24-word mnemonic phrase:")
Bot.waitForInput("save\_mnemonics")
# In save\_mnemonics command
mnemonics = msg
# Validate mnemonic format
words = mnemonics.split()
if len(words) != 24:
Api.sendMessage("❌ Invalid mnemonic. Must be exactly 24 words.")
Api.sendMessage("Try again: /import\_wallet")
else:
try:
# Store and verify
Lib.TON.storeKey(mnemonics)
address = Lib.TON.getAddress()
Api.sendMessage("✅ Wallet imported successfully!")
Api.sendMessage(f"Address: `{address}`")
User.storeData("ton\_address", address)
except Exception as e:
Api.sendMessage(f"❌ Error: {str(e)}")
```
\*\*Security Note:\*\* Mnemonic phrases grant full access to wallets. Store them securely and never expose them in logs or messages.
\*\*\*
### Lib.TON.getAddress()
Retrieves the wallet address from stored or provided mnemonics.
\*\*Syntax:\*\*
```python
Lib.TON.getAddress(mnemonics=None)
```
\*\*Parameters:\*\*
\* `mnemonics` (Optional): 24-word mnemonic phrase. If None, uses stored mnemonics.
\*\*Returns:\*\* String containing the wallet address
\*\*Example - Using Stored Mnemonics:\*\*
```python
# /my\_wallet command
try:
address = Lib.TON.getAddress()
Api.sendMessage(f"Your TON address:\n`{address}`")
except ValueError as e:
Api.sendMessage("❌ No wallet found. Create one: /create\_wallet")
```
\*\*Example - Using Specific Mnemonics:\*\*
```python
# Get address without storing
mnemonics = "word1 word2 word3 ... word24"
address = Lib.TON.getAddress(mnemonics=mnemonics)
Api.sendMessage(f"Address: {address}")
```
\*\*\*
## TON Operations
### Lib.TON.balance()
Checks the TON balance of any address.
\*\*Syntax:\*\*
```python
Lib.TON.balance(address, api\_key=None, endpoint=None, is\_testnet=False)
```
\*\*Parameters:\*\*
\* `address` (Required): TON wallet address to check
\* `api\_key` (Optional): TON Center API key for higher rate limits
\* `endpoint` (Optional): Custom RPC endpoint URL
\* `is\_testnet` (Optional): If True, uses testnet (default: False)
\*\*Returns:\*\* Float representing balance in TON
\*\*Example - Check Own Balance:\*\*
```python
# /balance command
address = User.fetchData("ton\_address")
if not address:
Api.sendMessage("No wallet found. Create one: /create\_wallet")
else:
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"💰 Your Balance:")
Api.sendMessage(f"{balance} TON")
# Convert to USD (example rate)
usd\_value = balance \* 2.50 # Example: 1 TON = $2.50
Api.sendMessage(f"≈ ${usd\_value:.2f} USD")
except Exception as e:
Api.sendMessage(f"Error checking balance: {str(e)}")
```
\*\*Example - Check Any Address:\*\*
```python
# /check\_balance command
Api.sendMessage("Send me a TON address to check:")
Bot.waitForInput("process\_balance\_check")
# In process\_balance\_check command
address = msg
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"Address: {address[:10]}...{address[-10:]}")
Api.sendMessage(f"Balance: {balance} TON")
except Exception as e:
Api.sendMessage(f"Invalid address or error: {str(e)}")
```
\*\*Example - Testnet Balance:\*\*
```python
# Check testnet balance
testnet\_balance = Lib.TON.balance(address, is\_testnet=True)
Api.sendMessage(f"Testnet balance: {testnet\_balance} TON")
```
\*\*\*
### Lib.TON.send()
Sends TON cryptocurrency to another address.
\*\*Syntax:\*\*
```python
Lib.TON.send(
to\_address,
amount,
comment=None,
mnemonics=None,
api\_key=None,
endpoint=None,
is\_testnet=False
)
```
\*\*Parameters:\*\*
\* `to\_address` (Required): Recipient's TON address
\* `amount` (Required): Amount of TON to send (float)
\* `comment` (Optional): Transaction comment/memo
\* `mnemonics` (Optional): Sender's mnemonic phrase (uses stored if None)
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\* `is\_testnet` (Optional): Use testnet if True
\*\*Returns:\*\* Dictionary with:
\* `ok` (bool): Success status
\* `tx` (dict): Transaction details including:
\* `hash` (str): Transaction hash
\* `lt` (int): Logical time
\* `seqno` (int): Sequence number
\* `to\_address` (str): Recipient address
\* `from\_address` (str): Sender address
\* `amount\_ton` (float): Amount sent
\* `comment` (str): Transaction comment
\*\*Example - Basic Send:\*\*
```python
# /send\_ton command
Api.sendMessage("Recipient address:")
Bot.waitForInput("get\_recipient")
# In get\_recipient command
recipient = msg
User.storeData("send\_recipient", recipient)
Api.sendMessage("Amount to send (in TON):")
Bot.waitForInput("get\_amount")
# In get\_amount command
amount\_str = msg
if not amount\_str.replace('.', '').isdigit():
Api.sendMessage("Invalid amount. Try again: /send\_ton")
else:
amount = float(amount\_str)
recipient = User.fetchData("send\_recipient")
# Confirm transaction
Api.sendMessage("📤 Confirm Transaction:")
Api.sendMessage(f"To: {recipient[:10]}...{recipient[-10:]}")
Api.sendMessage(f"Amount: {amount} TON")
Api.sendMessage("Confirm? /confirm\_send or /cancel")
# In confirm\_send command
try:
recipient = User.fetchData("send\_recipient")
amount = float(User.fetchData("send\_amount"))
Api.sendMessage("⏳ Processing transaction...")
result = Lib.TON.send(
to\_address=recipient,
amount=amount,
comment="Payment via TeleBot Studio"
)
if result['ok']:
tx = result['tx']
Api.sendMessage("✅ Transaction Successful!")
Api.sendMessage(f"Hash: `{tx['hash']}`")
Api.sendMessage(f"Amount: {tx['amount\_ton']} TON")
Api.sendMessage(f"Fee: ~0.01 TON")
else:
Api.sendMessage("❌ Transaction failed")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
\*\*Example - Send with Comment:\*\*
```python
result = Lib.TON.send(
to\_address="EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
amount=0.5,
comment="Payment for service #12345"
)
```
\*\*Example - Check Balance Before Sending:\*\*
```python
address = Lib.TON.getAddress()
balance = Lib.TON.balance(address)
amount\_to\_send = 1.5
if balance < amount\_to\_send + 0.02: # Include estimated fee
Api.sendMessage(f"Insufficient balance. You have {balance} TON")
Api.sendMessage(f"Need at least {amount\_to\_send + 0.02} TON")
else:
result = Lib.TON.send(to\_address=recipient, amount=amount\_to\_send)
Api.sendMessage("Transaction sent!")
```
\*\*\*
### Lib.TON.transactions()
Retrieves transaction history for an address.
\*\*Syntax:\*\*
```python
Lib.TON.transactions(address, limit=10, api\_key=None, endpoint=None, is\_testnet=False)
```
\*\*Parameters:\*\*
\* `address` (Required): TON wallet address
\* `limit` (Optional): Number of transactions to retrieve (default: 10)
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\* `is\_testnet` (Optional): Use testnet if True
\*\*Returns:\*\* List of transaction dictionaries
\*\*Example - View Recent Transactions:\*\*
```python
# /transactions command
address = User.fetchData("ton\_address")
if not address:
Api.sendMessage("No wallet found. Create one: /create\_wallet")
else:
try:
txs = Lib.TON.transactions(address, limit=5)
Api.sendMessage(f"📜 Recent Transactions ({len(txs)}):")
for idx, tx in enumerate(txs, 1):
tx\_type = "Incoming" if tx.get('in\_msg') else "Outgoing"
amount = tx.get('amount', 0) / 1000000000 # Convert from nanotons
Api.sendMessage(f"\n{idx}. {tx\_type}")
Api.sendMessage(f"Amount: {amount:.4f} TON")
Api.sendMessage(f"Time: {tx.get('utime', 'Unknown')}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
\*\*Example - Monitor Incoming Payments:\*\*
```python
# Check for new payments
last\_checked = User.fetchData("last\_tx\_check") or 0
address = User.fetchData("ton\_address")
txs = Lib.TON.transactions(address, limit=20)
for tx in txs:
tx\_time = tx.get('utime', 0)
if tx\_time > last\_checked and tx.get('in\_msg'):
# New incoming payment
amount = tx.get('amount', 0) / 1000000000
Api.sendMessage(f"💰 New payment received: {amount:.4f} TON")
# Award points or credits
points = User.res("points")
points.add(int(amount \* 100)) # 100 points per TON
User.storeData("last\_tx\_check", time.time())
```
\*\*\*
## TON Connect Integration
TON Connect allows users to connect their existing wallets to your bot for secure, wallet-based authentication and transactions.
### Lib.TON.connectSession()
Creates a TON Connect session for wallet connection.
\*\*Syntax:\*\*
```python
Lib.TON.connectSession(user\_id, expiry\_seconds=86400)
```
\*\*Parameters:\*\*
\* `user\_id` (Required): Unique identifier for the user
\* `expiry\_seconds` (Optional): Session expiration time (default: 86400 = 24 hours)
\*\*Returns:\*\* Dictionary with:
\* `session\_id` (str): Unique session identifier
\* `connect\_url` (str): QR code / deep link URL for wallet connection
\*\*Example:\*\*
```python
# /connect\_wallet command
session = Lib.TON.connectSession(user\_id=str(u))
Api.sendMessage("🔗 Connect Your TON Wallet")
Api.sendMessage("Scan this QR code with your TON wallet:")
Api.sendMessage(f"`{session['connect\_url']}`")
Api.sendMessage("\nOr open this link in your wallet app:")
Api.sendMessage(session['connect\_url'])
# Store session ID
User.storeData("ton\_connect\_session", session['session\_id'])
Api.sendMessage("\nOnce connected, use /check\_connection")
```
\*\*\*
### Lib.TON.verifySession()
Checks if a wallet has connected to the session.
\*\*Syntax:\*\*
```python
Lib.TON.verifySession(session\_id)
```
\*\*Parameters:\*\*
\* `session\_id` (Required): Session ID from connectSession
\*\*Returns:\*\* Dictionary with:
\* `status` (str): "connected" or "pending"
\* `wallet\_address` (str): Connected wallet address (if connected)
\* `public\_key` (str): Public key (if connected)
\*\*Example:\*\*
```python
# /check\_connection command
session\_id = User.fetchData("ton\_connect\_session")
if not session\_id:
Api.sendMessage("No connection attempt found. Start: /connect\_wallet")
else:
status = Lib.TON.verifySession(session\_id)
if status['status'] == "connected":
wallet = status['wallet\_address']
Api.sendMessage("✅ Wallet Connected!")
Api.sendMessage(f"Address: `{wallet}`")
# Store connected wallet
User.storeData("connected\_wallet", wallet)
User.removeData("ton\_connect\_session")
else:
Api.sendMessage("⏳ Wallet not connected yet")
Api.sendMessage("Please scan the QR code with your wallet")
```
\*\*\*
### Lib.TON.requestPayment()
Requests a TON transfer from a connected wallet.
\*\*Syntax:\*\*
```python
Lib.TON.requestPayment(
to\_address,
amount,
comment=None,
callback\_url="",
return\_url=None
)
```
\*\*Parameters:\*\*
\* `to\_address` (Required): Recipient address
\* `amount` (Required): Amount in TON
\* `comment` (Optional): Transaction comment
\* `callback\_url` (Optional): Webhook URL for payment confirmation
\* `return\_url` (Optional): URL to return to after payment
\*\*Returns:\*\* Payment request object
\*\*Example:\*\*
```python
# /pay command
connected\_wallet = User.fetchData("connected\_wallet")
if not connected\_wallet:
Api.sendMessage("Connect wallet first: /connect\_wallet")
else:
# Merchant address
merchant\_address = "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N"
payment\_request = Lib.TON.requestPayment(
to\_address=merchant\_address,
amount=1.0,
comment=f"Order #{Bot.uniqueID()}",
callback\_url=Lib.Webhook.getUrlFor("payment\_confirmed", user\_id=u)
)
Api.sendMessage("💳 Payment Request Sent")
Api.sendMessage("Approve the transaction in your wallet")
# In payment\_confirmed command
payment\_data = options
Api.sendMessage("✅ Payment confirmed!")
Api.sendMessage("Thank you for your purchase!")
# Grant access or deliver product
User.storeData("premium\_member", True)
```
\*\*\*
## Jetton Operations
Jettons are tokens on the TON blockchain (similar to ERC-20 on Ethereum).
### Lib.TON.tokenInfo()
Retrieves metadata about a Jetton (token).
\*\*Syntax:\*\*
```python
Lib.TON.tokenInfo(jetton\_master\_address, api\_key=None, endpoint=None, is\_testnet=False)
```
\*\*Parameters:\*\*
\* `jetton\_master\_address` (Required): Master contract address of the Jetton
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\* `is\_testnet` (Optional): Use testnet if True
\*\*Returns:\*\* Dictionary with token metadata:
\* `name` (str): Token name
\* `symbol` (str): Token symbol
\* `decimals` (int): Number of decimals
\* `total\_supply` (str): Total supply
\*\*Example:\*\*
```python
# /token\_info command
jetton\_address = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
try:
token = Lib.TON.tokenInfo(jetton\_address)
Api.sendMessage("🪙 Token Information:")
Api.sendMessage(f"Name: {token['name']}")
Api.sendMessage(f"Symbol: {token['symbol']}")
Api.sendMessage(f"Decimals: {token['decimals']}")
Api.sendMessage(f"Supply: {token['total\_supply']}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
\*\*\*
### Lib.TON.tokenBalance()
Checks Jetton token balance for an address.
\*\*Syntax:\*\*
```python
Lib.TON.tokenBalance(
owner\_address,
jetton\_master\_address,
api\_key=None,
endpoint=None,
is\_testnet=False
)
```
\*\*Parameters:\*\*
\* `owner\_address` (Required): Wallet address to check
\* `jetton\_master\_address` (Required): Master contract of the Jetton
\* `api\_key` (Optional): TON Center API key
\* `endpoint` (Optional): Custom RPC endpoint
\* `is\_testnet` (Optional): Use testnet if True
\*\*Returns:\*\* Float representing token balance
\*\*Example:\*\*
```python
# /token\_balance command
user\_address = User.fetchData("ton\_address")
jetton\_address = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
if not user\_address:
Api.sendMessage("No wallet found. Create one: /create\_wallet")
else:
try:
balance = Lib.TON.tokenBalance(user\_address, jetton\_address)
token\_info = Lib.TON.tokenInfo(jetton\_address)
Api.sendMessage(f"💰 {token\_info['symbol']} Balance:")
Api.sendMessage(f"{balance} {token\_info['symbol']}")
except Exception as e:
Api.sendMessage(f"Error: {str(e)}")
```
\*\*\*
### Lib.TON.requestToken()
Requests a Jetton transfer from a connected wallet.
\*\*Syntax:\*\*
```python
Lib.TON.requestToken(
to\_address,
jetton\_master\_address,
amount,
comment=None,
callback\_url="",
return\_url=None
)
```
\*\*Parameters:\*\*
\* `to\_address` (Required): Recipient address
\* `jetton\_master\_address` (Required): Master contract of the Jetton
\* `amount` (Required): Amount of tokens
\* `comment` (Optional): Transaction comment
\* `callback\_url` (Optional): Webhook for confirmation
\* `return\_url` (Optional): Return URL
\*\*Returns:\*\* Token transfer request object
\*\*Example:\*\*
```python
# /send\_tokens command
connected\_wallet = User.fetchData("connected\_wallet")
if not connected\_wallet:
Api.sendMessage("Connect wallet first: /connect\_wallet")
else:
recipient = "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N"
jetton = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
request = Lib.TON.requestToken(
to\_address=recipient,
jetton\_master\_address=jetton,
amount=100,
comment="Token payment"
)
Api.sendMessage("Token transfer request sent to your wallet")
Api.sendMessage("Approve the transaction to complete")
```
\*\*\*
## Real-World Use Cases
### 1. Crypto Payment Bot
```python
# /start command
Api.sendMessage("Welcome to Crypto Payment Bot!")
Api.sendMessage("Commands:")
Api.sendMessage("/create\_wallet - Create new wallet")
Api.sendMessage("/import\_wallet - Import existing wallet")
Api.sendMessage("/balance - Check balance")
Api.sendMessage("/receive - Get payment address")
Api.sendMessage("/send - Send TON")
# /receive command
address = User.fetchData("ton\_address")
if address:
Api.sendMessage("💰 Receive TON:")
Api.sendMessage(f"`{address}`")
Api.sendMessage("Share this address to receive payments")
else:
Api.sendMessage("Create wallet first: /create\_wallet")
```
\*\*\*
### 2. Automated Payment Processing
```python
# Monitor for payments
# /check\_payments command (scheduled every 5 minutes)
address = Bot.fetchData("merchant\_address")
last\_check = Bot.fetchData("last\_payment\_check") or 0
txs = Lib.TON.transactions(address, limit=50)
for tx in txs:
if tx.get('utime', 0) > last\_check and tx.get('in\_msg'):
amount = tx.get('amount', 0) / 1000000000
sender = tx.get('source', 'Unknown')
# Find user by amount or comment
order\_id = extract\_order\_id(tx.get('comment', ''))
if order\_id:
# Process order
process\_order(order\_id, amount)
Api.sendMessage(f"✅ Payment received for order #{order\_id}", chat\_id=get\_user\_by\_order(order\_id))
Bot.storeData("last\_payment\_check", time.time())
```
\*\*\*
### 3. TON Connect Authentication
```python
# /login command
session = Lib.TON.connectSession(user\_id=str(u))
User.storeData("auth\_session", session['session\_id'])
Api.sendMessage("🔐 Login with TON Connect")
Api.sendMessage("Scan QR code with your wallet:")
Api.sendMessage(session['connect\_url'])
# Schedule verification check
Bot.scheduleCommand(5, "verify\_login")
# verify\_login command
session\_id = User.fetchData("auth\_session")
status = Lib.TON.verifySession(session\_id)
if status['status'] == "connected":
wallet = status['wallet\_address']
User.storeData("authenticated\_wallet", wallet)
User.storeData("logged\_in", True)
Api.sendMessage("✅ Logged in successfully!")
Api.sendMessage("Welcome back!")
else:
Bot.scheduleCommand(5, "verify\_login") # Check again in 5 seconds
```
\*\*\*
### 4. Token Gated Access
```python
# /premium command
address = User.fetchData("ton\_address")
token\_contract = "EQBl3gg6AAdjgjO2ZoNU5Q5EzUIl8XMNZrix8Z5dJmkHUfxI"
if not address:
Api.sendMessage("Connect wallet: /connect\_wallet")
else:
balance = Lib.TON.tokenBalance(address, token\_contract)
if balance >= 100: # Requires 100 tokens
Api.sendMessage("✅ Premium Access Granted!")
User.storeData("premium", True)
Api.sendMessage("Access premium features: /premium\_features")
else:
Api.sendMessage(f"❌ Insufficient tokens")
Api.sendMessage(f"You have: {balance}")
Api.sendMessage(f"Required: 100")
```
\*\*\*
## Best Practices
### 1. Security
\*\*Never log or expose mnemonic phrases:\*\*
```python
# ❌ Wrong
Api.sendMessage(f"Your mnemonics: {mnemonics}")
# ✅ Correct
Api.sendMessage("Mnemonics sent privately (check your saved messages)")
# Use user's Saved Messages or encrypt before sending
```
\*\*Validate addresses:\*\*
```python
def is\_valid\_ton\_address(address):
# Basic validation
if not address.startswith("EQ") and not address.startswith("UQ"):
return False
if len(address) != 48:
return False
return True
if not is\_valid\_ton\_address(recipient):
Api.sendMessage("Invalid TON address format")
```
### 2. Error Handling
\*\*Always wrap blockchain operations in try-except:\*\*
```python
try:
balance = Lib.TON.balance(address)
Api.sendMessage(f"Balance: {balance} TON")
except ConnectionError:
Api.sendMessage("Network error. Please try again.")
except ValueError as ve:
Api.sendMessage(f"Invalid address: {str(ve)}")
except Exception as e:
error\_id = Bot.errorID()
Api.sendMessage(f"Error {error\_id}: {str(e)}")
```
### 3. Testnet First
\*\*Test on testnet before mainnet:\*\*
```python
# Development: Use testnet
IS\_TESTNET = True
balance = Lib.TON.balance(address, is\_testnet=IS\_TESTNET)
result = Lib.TON.send(to\_address=addr, amount=0.1, is\_testnet=IS\_TESTNET)
# Production: Use mainnet
IS\_TESTNET = False
```
### 4. Transaction Confirmation
\*\*Always confirm before sending:\*\*
```python
# Show confirmation
Api.sendMessage("⚠️ Confirm Transaction:")
Api.sendMessage(f"To: {recipient}")
Api.sendMessage(f"Amount: {amount} TON")
Api.sendMessage(f"Fee: ~0.01 TON")
Api.sendMessage("\n/confirm to proceed\n/cancel to abort")
Bot.waitForInput("handle\_confirmation")
```
### 5. Rate Limiting
\*\*Respect API rate limits:\*\*
```python
# Cache balances for 1 minute
cached\_balance = User.fetchData("cached\_balance")
cache\_time = User.fetchData("cache\_time") or 0
if time.time() - cache\_time < 60:
Api.sendMessage(f"Balance: {cached\_balance} TON (cached)")
else:
balance = Lib.TON.balance(address)
User.storeData("cached\_balance", balance)
User.storeData("cache\_time", time.time())
Api.sendMessage(f"Balance: {balance} TON")
```
\*\*\*
## Platform Limitations
\* \*\*Code execution timeout:\*\* 160 seconds maximum
\* \*\*Sleep function:\*\* 10 seconds maximum
\* \*\*No import statements:\*\* All libraries are pre-loaded
\*\*\*
## Troubleshooting
### Common Issues
\*\*"No mnemonics provided or stored"\*\*
```python
# Solution: Store mnemonics first
Lib.TON.storeKey("your 24 word mnemonic phrase")
```
\*\*"Insufficient balance"\*\*
```python
# Solution: Check balance before sending
balance = Lib.TON.balance(address)
if balance < amount + 0.02: # Include fee
Api.sendMessage("Insufficient funds")
```
\*\*"Network timeout"\*\*
```python
# Solution: Retry with exponential backoff
attempts = 0
max\_attempts = 3
while attempts < max\_attempts:
try:
balance = Lib.TON.balance(address)
break
except:
attempts += 1
if attempts < max\_attempts:
time.sleep(2 \*\* attempts) # 2, 4, 8 seconds
else:
Api.sendMessage("Network error after multiple attempts")
```
\*\*\*
## Further Resources
\* \*\*TON Documentation:\*\* 
\* \*\*TON Connect:\*\* 
\* \*\*Testnet Faucet:\*\* 
\* \*\*Block Explorer:\*\* 
\*\*\*
The TON Library in TeleBot Studio provides everything you need to build powerful cryptocurrency bots on the TON blockchain. Start building today!
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/ton-library-documentation.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.