> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/evm-library-documentation.md).
# EVM Library Documentation
The EVM Library in TeleBot Studio enables seamless integration with Ethereum and 30+ EVM-compatible blockchain networks. Build powerful cryptocurrency bots with wallet management, native coin transfers, token operations, and automatic gas optimization.
\*\*\*
## Introduction
The EVM Library (`Lib.EVM`) provides a unified, powerful interface for interacting with Ethereum Virtual Machine compatible blockchains. Whether you're sending ETH, transferring ERC-20 tokens, or building a DeFi bot, this library handles the complexity for you.
\*\*Key Features:\*\*
\* \*\*31+ Supported Networks\*\* - Ethereum, BSC, Polygon, Arbitrum, and more
\* \*\*Automatic Gas Estimation\*\* - No manual gas calculations needed
\* \*\*Retry Logic\*\* - Automatic retry on recoverable errors
\* \*\*Proxy Support\*\* - Built-in proxy rotation to avoid rate limits
\* \*\*Secure Key Management\*\* - Encrypted private key storage
\* \*\*Token Support\*\* - Full ERC-20 token transfer capabilities
\*\*\*
## Supported Networks
TeleBot Studio supports 31 major EVM-compatible blockchain networks:
| Network           | Chain ID   | Default RPC                              |
| ----------------- | ---------- | ---------------------------------------- |
| \*\*Ethereum\*\*      | 1          | <https://ethereum.publicnode.com>        |
| \*\*BSC (Binance)\*\* | 56         | <https://bsc-dataseed.binance.org>       |
| \*\*Polygon\*\*       | 137        | <https://polygon-rpc.com>                |
| \*\*Avalanche\*\*     | 43114      | <https://api.avax.network/ext/bc/C/rpc>  |
| \*\*Fantom\*\*        | 250        | <https://rpc.ftm.tools>                  |
| \*\*Arbitrum\*\*      | 42161      | <https://arb1.arbitrum.io/rpc>           |
| \*\*Optimism\*\*      | 10         | <https://mainnet.optimism.io>            |
| \*\*Base\*\*          | 8453       | <https://mainnet.base.org>               |
| \*\*ZKSync\*\*        | 324        | <https://mainnet.era.zksync.io>          |
| \*\*Scroll\*\*        | 534352     | <https://rpc.scroll.io>                  |
| \*\*Linea\*\*         | 59144      | <https://rpc.linea.build>                |
| \*\*Harmony\*\*       | 1666600000 | <https://api.harmony.one>                |
| \*\*Cronos\*\*        | 25         | <https://evm.cronos.org>                 |
| \*\*Moonriver\*\*     | 1285       | <https://rpc.moonriver.moonbeam.network> |
| \*\*Moonbeam\*\*      | 1284       | <https://rpc.api.moonbeam.network>       |
| \*\*Celo\*\*          | 42220      | <https://forno.celo.org>                 |
| \*\*Boba\*\*          | 288        | <https://mainnet.boba.network>           |
| \*\*Metis\*\*         | 1088       | <https://andromeda.metis.io>             |
| \*\*Aurora\*\*        | 1313161554 | <https://mainnet.aurora.dev>             |
| \*\*Kava\*\*          | 2222       | <https://evm.kava.io>                    |
| \*\*Fuse\*\*          | 122        | <https://rpc.fuse.io>                    |
| \*\*Evmos\*\*         | 9001       | <https://eth.bd.evmos.org:8545>          |
| \*\*Canto\*\*         | 7700       | <https://canto.slingshot.finance>        |
| \*\*Astar\*\*         | 592        | <https://evm.astar.network>              |
| \*\*Telos\*\*         | 40         | <https://mainnet.telos.net/evm>          |
| \*\*Rootstock\*\*     | 30         | <https://public-node.rsk.co>             |
| \*\*TTcoin\*\*        | 22023      | <https://mainnet-rpc.thundercore.com>    |
| \*\*Heco\*\*          | 128        | <https://http-mainnet.hecochain.com>     |
| \*\*Okexchain\*\*     | 66         | <https://exchainrpc.okex.org>            |
| \*\*Xdai (Gnosis)\*\* | 100        | <https://rpc.gnosischain.com>            |
| \*\*KCC\*\*           | 321        | <https://rpc-mainnet.kcc.network>        |
\*\*Note:\*\* \*(Updated in v1.1.0)\* The default RPC for Ethereum and Heco has changed from Ankr's endpoints, which now require an API key for free-tier access, to no-authentication-required public endpoints. If you were previously passing a custom `rpc\_url` to work around this, it's no longer necessary — though custom `rpc\_url` values are always supported if you prefer your own provider.
\*\*\*
## Getting Started
The EVM Library is globally available - no import statements needed:
```python
# ✅ Correct - Direct usage
networks = Lib.EVM.networks()
# ❌ Wrong - No imports allowed
# import Lib.EVM  # This will cause an error
```
\*\*\*
## Key Management
### Lib.EVM.generateKey()
Generates a new random private key.
\*\*Syntax:\*\*
```python
Lib.EVM.generateKey()
```
\*\*Returns:\*\* String containing a new private key
\*\*Example:\*\*
```python
# /create\_wallet command
private\_key = Lib.EVM.generateKey()
Api.sendMessage("🔐 New Wallet Created!")
Api.sendMessage("⚠️ SAVE THIS PRIVATE KEY SECURELY:")
Api.sendMessage(f"`{private\_key}`")
Api.sendMessage("\n⚠️ Never share your private key with anyone!")
# Store securely
Lib.EVM.storeKey(private\_key)
Api.sendMessage("\n✅ Private key stored securely")
```
\*\*Security Warning:\*\* Private keys grant full access to wallet funds. Always store them securely and never expose them in logs or public messages.
\*\*\*
### Lib.EVM.storeKey()
Securely stores a private key for later use.
\*\*Syntax:\*\*
```python
Lib.EVM.storeKey(private\_key)
```
\*\*Parameters:\*\*
\* `private\_key` (Required): The private key to store (with or without '0x' prefix)
\*\*Returns:\*\* String confirming storage
\*\*Note:\*\* Stored private keys are encrypted and associated with your bot and user.
\*\*\*
## Network Information
### Lib.EVM.networks()
Returns information about all supported blockchain networks.
\*\*Syntax:\*\*
```python
Lib.EVM.networks()
```
\*\*Returns:\*\* Dictionary with network details:
\* Network name as key
\* Chain ID, RPC URL, and other metadata as values
\*\*Example:\*\*
```python
# /networks command
networks = Lib.EVM.networks()
Api.sendMessage("🌐 Supported Networks:")
for name, info in list(networks.items())[:10]:  # Show first 10
    Api.sendMessage(f"{name}: Chain ID {info['chain\_id']}")
Api.sendMessage(f"\nTotal: {len(networks)} networks supported")
```
\*\*\*
### Lib.EVM.getRPC()
Gets the default RPC URL for a specific network.
\*\*Syntax:\*\*
```python
Lib.EVM.getRPC(network)
```
\*\*Parameters:\*\*
\* `network` (Required): Network name (e.g., "ethereum", "bsc", "polygon")
\*\*Returns:\*\* String containing the RPC URL
\*\*Example:\*\*
```python
# Get RPC for Ethereum
eth\_rpc = Lib.EVM.getRPC("ethereum")
Api.sendMessage(f"Ethereum RPC: {eth\_rpc}")
# Get RPC for BSC
bsc\_rpc = Lib.EVM.getRPC("bsc")
Api.sendMessage(f"BSC RPC: {bsc\_rpc}")
```
\*\*\*
## Native Coin Transfers
### Lib.EVM.sendCoin()
Sends native blockchain coins (ETH, BNB, MATIC, etc.) to another address.
\*\*Syntax:\*\*
```python
Lib.EVM.sendCoin(
    network,
    to,
    value,
    private\_key=None,
    gas\_limit=None,
    gas\_price=None,
    proxy=None,
    estimate\_gas=True,
    retry=False
)
```
\*\*Parameters:\*\*
\* `network` (Required): Network name (e.g., "ethereum", "bsc", "polygon")
\* `to` (Required): Recipient wallet address
\* `value` (Required): Amount to send (in native coin, e.g., ETH)
\* `private\_key` (Optional): Sender's private key (uses stored if not provided)
\* `gas\_limit` (Optional): Manual gas limit (auto-estimated if not provided)
\* `gas\_price` (Optional): Gas price in Gwei (uses current network price if not provided)
\* `proxy` (Optional): Proxy configuration (automatic proxy rotation by default)
\* `estimate\_gas` (Optional): Auto-estimate gas (default: True)
\* `retry` (Optional): Retry once on failure (default: False)
\*\*Returns:\*\* String containing the transaction hash
\*\*Example - Send on BSC:\*\*
```python
# Send BNB on Binance Smart Chain
tx\_hash = Lib.EVM.sendCoin(
    network="bsc",
    to="0xRecipientAddress",
    value=0.1  # 0.1 BNB
)
Api.sendMessage(f"Transaction: {tx\_hash}")
```
\*\*Example - Manual Gas Settings:\*\*
```python
# Send with custom gas settings
tx\_hash = Lib.EVM.sendCoin(
    network="ethereum",
    to="0xRecipientAddress",
    value=0.01,
    gas\_limit=21000,
    gas\_price=30  # 30 Gwei
)
```
\*\*\*
## Token Transfers
### Lib.EVM.sendToken()
Sends ERC-20 tokens to another address.
\*\*Syntax:\*\*
```python
Lib.EVM.sendToken(
    network,
    to,
    value,
    contract\_address,
    private\_key=None,
    gas\_limit=None,
    gas\_price=None,
    proxy=None,
    estimate\_gas=True,
    retry=False
)
```
\*\*Parameters:\*\*
\* `network` (Required): Network name
\* `to` (Required): Recipient wallet address
\* `value` (Required): Amount of tokens to send
\* `contract\_address` (Required): Token contract address
\* `private\_key` (Optional): Sender's private key (uses stored if not provided)
\* `gas\_limit` (Optional): Manual gas limit
\* `gas\_price` (Optional): Gas price in Gwei
\* `proxy` (Optional): Proxy configuration
\* `estimate\_gas` (Optional): Auto-estimate gas (default: True)
\* `retry` (Optional): Retry once on failure (default: False)
\*\*Returns:\*\* String containing the transaction hash
\*\*Example - Send USDT on Ethereum:\*\*
```python
# Send 100 USDT
usdt\_contract = "0xdac17f958d2ee523a2206206994597c13d831ec7"
tx\_hash = Lib.EVM.sendToken(
    network="ethereum",
    to="0xRecipientAddress",
    value=100,  # 100 USDT (6 decimals handled automatically)
    contract\_address=usdt\_contract
)
Api.sendMessage("✅ Sent 100 USDT!")
Api.sendMessage(f"Transaction: {tx\_hash}")
```
\*\*\*
## Balance Checking \*(Added in v1.1.0)\*
### Lib.EVM.fetchBalance()
Checks the native coin balance of any address, without needing an external block explorer.
\*\*Syntax:\*\*
```python
Lib.EVM.fetchBalance(address, network=None, rpc\_url=None, unit="ether")
```
\*\*Parameters:\*\*
\* `address` (Required): Wallet address to check
\* `network` (Optional): Network name (e.g., "ethereum", "bsc", "polygon") — required if `rpc\_url` is not provided
\* `rpc\_url` (Optional): Custom RPC endpoint — required if `network` is not provided
\* `unit` (Optional): `"wei"`, `"gwei"`, or `"ether"` (default)
\*\*Returns:\*\* Float representing the balance in the requested unit (or int if `unit="wei"`)
\*\*Example:\*\*
```python
# /balance command
address = User.fetchData("eth\_address")
if not address:
    Api.sendMessage("No wallet found. Create one: /create\_wallet")
else:
    try:
        balance = Lib.EVM.fetchBalance(address, network="ethereum")
        Api.sendMessage(f"💰 Balance: {balance} ETH")
    except Exception as e:
        Api.sendMessage(f"Error checking balance: {str(e)}")
```
\*\*Example - Check Balance on Multiple Networks:\*\*
```python
address = User.fetchData("eth\_address")
networks = ["ethereum", "bsc", "polygon"]
Api.sendMessage("💰 Your Balances:")
for network in networks:
    try:
        balance = Lib.EVM.fetchBalance(address, network=network)
        Api.sendMessage(f"{network.title()}: {balance}")
    except Exception as e:
        Api.sendMessage(f"{network.title()}: Error - {str(e)}")
```
\*\*\*
### Lib.EVM.fetchTokenBalance()
Checks the ERC-20 token balance of any address, with automatic decimal detection.
\*\*Syntax:\*\*
```python
Lib.EVM.fetchTokenBalance(address, contract\_address, network=None, rpc\_url=None, decimals=None, raw=False)
```
\*\*Parameters:\*\*
\* `address` (Required): Wallet address to check
\* `contract\_address` (Required): Token contract address
\* `network` (Optional): Network name — required if `rpc\_url` is not provided
\* `rpc\_url` (Optional): Custom RPC endpoint — required if `network` is not provided
\* `decimals` (Optional): Manually specify decimals — auto-detected from the contract if omitted
\* `raw` (Optional): If True, returns the unscaled on-chain integer instead of a human-readable float
\*\*Returns:\*\* Float representing the token balance (or int if `raw=True`)
\*\*Example:\*\*
```python
# /token\_balance command
address = User.fetchData("eth\_address")
usdt\_contract = "0xdac17f958d2ee523a2206206994597c13d831ec7"
try:
    balance = Lib.EVM.fetchTokenBalance(address, usdt\_contract, network="ethereum")
    Api.sendMessage(f"💰 USDT Balance: {balance}")
except Exception as e:
    Api.sendMessage(f"Error: {str(e)}")
```
\*\*Example - Verify Balance Before Sending:\*\*
```python
usdt\_contract = "0xdac17f958d2ee523a2206206994597c13d831ec7"
sender\_balance = Lib.EVM.fetchTokenBalance(sender\_address, usdt\_contract, network="ethereum")
if sender\_balance < amount:
    Api.sendMessage(f"❌ Insufficient balance. You have {sender\_balance} USDT")
else:
    tx\_hash = Lib.EVM.sendToken(
        network="ethereum",
        to=recipient,
        value=amount,
        contract\_address=usdt\_contract
    )
    Api.sendMessage(f"✅ Sent {amount} USDT: {tx\_hash}")
```
\*\*\*
## Best Practices
### 1. Security
\*\*Never expose private keys:\*\*
```python
# ❌ Wrong - Don't send private key
Api.sendMessage(f"Your key: {private\_key}")
# ✅ Correct - Store securely
Lib.EVM.storeKey(private\_key)
Api.sendMessage("✅ Private key stored securely")
```
### 2. Error Handling
\*\*Always wrap transactions in try-except:\*\*
```python
try:
    tx\_hash = Lib.EVM.sendCoin(
        network="ethereum",
        to=recipient,
        value=amount
    )
    Api.sendMessage(f"✅ Success: {tx\_hash}")
except ValueError as ve:
    Api.sendMessage(f"❌ Invalid input: {str(ve)}")
except Exception as e:
    error\_id = Bot.errorID()
    Api.sendMessage(f"❌ Error {error\_id}: {str(e)}")
```
### 3. Gas Optimization
\*\*Use automatic gas estimation:\*\*
```python
# ✅ Recommended - Auto gas estimation
tx\_hash = Lib.EVM.sendCoin(
    network="ethereum",
    to=recipient,
    value=amount,
    estimate\_gas=True
)
```
### 4. Retry Logic
\*\*Enable retry for important transactions:\*\*
```python
# Enable retry for better reliability
tx\_hash = Lib.EVM.sendCoin(
    network="ethereum",
    to=recipient,
    value=amount,
    retry=True  # Retry once on failure
)
```
\*\*\*
## Troubleshooting
### Common Issues
\*\*"Invalid private key"\*\*
```python
# Solution: Validate format before storing
if not private\_key.startswith('0x'):
    private\_key = '0x' + private\_key
if len(private\_key) != 66:
    Api.sendMessage("Invalid key format")
```
\*\*"Network timeout"\*\*
```python
# Solution: Enable retry
tx\_hash = Lib.EVM.sendCoin(
    network="ethereum",
    to=recipient,
    value=amount,
    retry=True  # Automatically retry once
)
```
\*\*\*
## Platform Limitations
\* \*\*Code execution timeout:\*\* 160 seconds maximum
\* \*\*Sleep function:\*\* 10 seconds maximum
\* \*\*No import statements:\*\* All libraries are pre-loaded
\*\*\*
## Summary
The EVM Library in TeleBot Studio provides:
✅ \*\*31+ Blockchain Networks\*\* - Ethereum, BSC, Polygon, and more
✅ \*\*Automatic Gas Estimation\*\* - No manual calculations needed
✅ \*\*Retry Logic\*\* - Automatic recovery from transient errors
✅ \*\*Secure Key Management\*\* - Encrypted storage
✅ \*\*Token Support\*\* - Full ERC-20 functionality
✅ \*\*Balance Checking\*\* - Native and token balances \*(Added in v1.1.0)\*
\*\*\*
## Further Resources
\* \*\*Ethereum Documentation:\*\* <https://ethereum.org/developers>
\* \*\*Block Explorers:\*\*
  \* Ethereum: <https://etherscan.io>
  \* BSC: <https://bscscan.com>
  \* Polygon: <https://polygonscan.com>
\* \*\*Token Lists:\*\* <https://tokenlists.org>
\*\*\*
For TON blockchain integration, see the [TON Library Documentation](/ton-library-documentation.md).
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/evm-library-documentation.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
