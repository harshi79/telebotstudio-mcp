> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/real-world.md).
# Real-World Examples and Use Cases
This section demonstrates how to apply TeleBot Studio's features and libraries in real-world scenarios. By combining workflows, advanced commands, and external integrations, you can create bots that solve practical problems and enhance user engagement.
\*\*\*
## Referral System
### Overview
A referral system tracks users who invite others to the bot and rewards them with points or other incentives. This use case involves:
1. Generating unique referral links
2. Tracking referrals
3. Rewarding users based on their referral count
4. Displaying leaderboards for top referrers
### Implementation
\*\*Step 1: Generate Unique Referral Links\*\*
In the `/start` command, include the user's ID as a parameter to generate a referral link:
```python
bot\_info = Bot.getInfo()
bot\_username = bot\_info['username']
Api.sendMessage(f"Invite your friends using this link:")
Api.sendMessage(f"t.me/{bot\_username}?start={u}")
```
\*\*Step 2: Track Referrals\*\*
In the `/start` command, check if a referral ID is provided:
```python
referrer\_id = params
if referrer\_id and referrer\_id != str(u):
# Check if this is first time being referred
already\_referred = User.fetchData("referred\_by")
if not already\_referred:
User.storeData("referred\_by", referrer\_id)
# Award points to referrer
referrer\_points = User.resOf("points", int(referrer\_id))
referrer\_points.add(10)
# Track referral count
referral\_count = Bot.res(f"referral\_count\_{referrer\_id}")
referral\_count.add(1)
# Notify referrer
Api.sendMessage(
f"User {u} joined using your referral link! You earned 10 points!",
chat\_id=int(referrer\_id)
)
Api.sendMessage("Welcome! You were referred by a friend.")
```
\*\*Step 3: Reward Users\*\*
Track and display referral rewards dynamically:
```python
# /mypoints command
user\_points = User.res("points")
Api.sendMessage(f"You have {user\_points.value()} points!")
```
\*\*Step 4: Create a Leaderboard\*\*
Display the top referrers:
```python
# /leaderboard command
# Get top 10 referrers
top\_referrers\_data = []
for i in range(100): # Check first 100 user IDs (example)
referral\_count = Bot.res(f"referral\_count\_{i}").value()
if referral\_count and referral\_count > 0:
top\_referrers\_data.append({"user": i, "count": referral\_count})
# Sort by count
top\_referrers\_data.sort(key=lambda x: x['count'], reverse=True)
top\_10 = top\_referrers\_data[:10]
Api.sendMessage("🏆 Top Referrers:")
for idx, entry in enumerate(top\_10, 1):
Api.sendMessage(f"{idx}. User {entry['user']}: {entry['count']} referrals")
```
\*\*\*
## Payment Automation Bot
### Overview
This bot automates payment handling using the `Lib.Oxapay` library. It can:
1. Generate payment requests
2. Confirm payment status
3. Notify users of successful payments
### Implementation
\*\*Step 1: Set Up Oxapay Client\*\*
Configure the Oxapay client with your API key:
```python
client = Lib.Oxapay.post("your\_merchant\_api\_key")
```
\*\*Step 2: Generate Payment Requests\*\*
Request payment for specific amounts:
```python
# /subscribe command
payment\_details = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Monthly subscription fee"
})
Api.sendMessage(f"Please make your payment here:")
Api.sendMessage(payment\_details["url"])
# Store payment ID for verification
User.storeData("pending\_payment\_id", payment\_details["id"])
```
\*\*Step 3: Verify Payment Status\*\*
Check payment status using webhooks or polling:
```python
# /check\_payment command
payment\_id = User.fetchData("pending\_payment\_id")
if not payment\_id:
Api.sendMessage("No pending payment found.")
else:
# Check payment status via webhook or API call
payment\_info = client.getPaymentStatus(payment\_id)
status = payment\_info.get("status", "pending")
if status == "completed":
Api.sendMessage("✅ Payment confirmed! Thank you!")
# Grant subscription
User.storeData("subscribed", True)
User.storeData("subscription\_date", time.time())
User.removeData("pending\_payment\_id")
# Award premium points
points = User.res("points")
points.add(1000)
elif status == "expired" or status == "cancelled":
Api.sendMessage("❌ Payment expired or cancelled.")
User.removeData("pending\_payment\_id")
else:
Api.sendMessage(f"Payment status: {status}")
```
\*\*\*
## Survey and Data Collection Bot
### Overview
This bot collects user input for surveys or forms and stores the data in a CSV file for easy analysis.
### Implementation
\*\*Step 1: Collect User Responses\*\*
Ask users a series of questions:
```python
# /survey command
Api.sendMessage("📋 Customer Satisfaction Survey")
Api.sendMessage("What is your name?")
Bot.waitForInput("survey\_get\_name")
```
Store the responses:
```python
# survey\_get\_name command
name = msg
User.storeData("survey\_name", name)
Api.sendMessage(f"Thanks {name}! What is your email?")
Bot.waitForInput("survey\_get\_email")
```
\*\*Continue Survey:\*\*
```python
# survey\_get\_email command
email = msg
User.storeData("survey\_email", email)
Api.sendMessage("How satisfied are you with our service? (1-5)")
Bot.waitForInput("survey\_get\_rating")
```
\*\*Step 2: Save Data to CSV\*\*
Save the collected data into a CSV file:
```python
# survey\_get\_rating command
rating = msg
if not rating.isdigit() or not (1 <= int(rating) <= 5):
Api.sendMessage("Please enter a number between 1 and 5:")
Bot.waitForInput("survey\_get\_rating")
else:
# Save to CSV
csv\_handler = Lib.CSV.Table("survey\_data.csv")
# Create CSV if doesn't exist
try:
csv\_handler.row(0)
except:
csv\_handler.create(["user\_id", "name", "email", "rating", "date"])
# Add response
csv\_handler.insert({
"user\_id": u,
"name": User.fetchData("survey\_name"),
"email": User.fetchData("survey\_email"),
"rating": rating,
"date": Lib.DateTime.utcnow()
})
Api.sendMessage("✅ Thank you! Your responses have been saved.")
# Cleanup
User.removeData("survey\_name")
User.removeData("survey\_email")
```
\*\*\*
## Crypto Airdrop Bot
### Overview
This bot automates cryptocurrency distributions using blockchain libraries.
### Implementation (TON Blockchain)
\*\*Step 1: Configure Wallet\*\*
Set up the distribution wallet:
```python
# Store wallet mnemonics (done once by admin)
Lib.TON.storeKey("your 24 word mnemonic phrase here")
```
\*\*Step 2: Distribute Airdrops\*\*
Send tokens to multiple recipients:
```python
# /start\_airdrop command (admin only)
if u != ADMIN\_USER\_ID:
Api.sendMessage("Unauthorized")
else:
recipients = [
{"address": "EQRecipient1...", "amount": 10},
{"address": "EQRecipient2...", "amount": 15},
{"address": "EQRecipient3...", "amount": 20}
]
Api.sendMessage(f"Starting airdrop to {len(recipients)} recipients...")
success\_count = 0
for recipient in recipients:
try:
result = Lib.TON.send(
to\_address=recipient["address"],
amount=recipient["amount"],
comment="Airdrop reward"
)
success\_count += 1
Api.sendMessage(f"✅ Sent {recipient['amount']} TON to {recipient['address'][:10]}...")
except Exception as e:
Api.sendMessage(f"❌ Failed: {recipient['address'][:10]}... - {str(e)}")
Api.sendMessage(f"Airdrop complete! {success\_count}/{len(recipients)} successful")
```
\*\*Step 3: User Registration for Airdrop\*\*
Collect wallet addresses:
```python
# /register\_wallet command
Api.sendMessage("Please enter your TON wallet address:")
Bot.waitForInput("save\_wallet")
```
```python
# save\_wallet command
wallet\_address = msg
# Basic validation
if wallet\_address.startswith("EQ") and len(wallet\_address) > 40:
User.storeData("wallet\_address", wallet\_address)
Api.sendMessage("✅ Wallet registered successfully!")
Api.sendMessage("You'll be notified when airdrop begins.")
else:
Api.sendMessage("Invalid TON address. Please try again:")
Bot.waitForInput("save\_wallet")
```
\*\*\*
## Real-Time Notification Bot
### Overview
This bot uses webhooks to send real-time updates based on external events, such as sales or user actions.
### Implementation
\*\*Step 1: Generate Webhook URL\*\*
Generate a webhook URL for notifications:
```python
# /setup\_notifications command
webhook\_url = Lib.Webhook.getUrlFor("send\_notification", user\_id=u)
Api.sendMessage("Your notification webhook:")
Api.sendMessage(webhook\_url)
Api.sendMessage("Configure this URL in your external system to receive notifications.")
User.storeData("webhook\_configured", True)
```
\*\*Step 2: Process Webhook Events\*\*
Handle incoming webhook events in a command:
```python
# send\_notification command
notification\_data = options
event\_type = notification\_data.get('type', 'general')
message = notification\_data.get('message', 'You have a new notification!')
if event\_type == 'sale':
amount = notification\_data.get('amount', 0)
Api.sendMessage(f"🎉 New Sale!")
Api.sendMessage(f"Amount: ${amount}")
# Award points
points = User.res("points")
points.add(int(amount) \* 10)
elif event\_type == 'alert':
Api.sendMessage(f"⚠️ Alert: {message}")
else:
Api.sendMessage(message)
```
\*\*\*
## Event Management Bot
### Overview
This bot manages events, allowing users to RSVP, receive reminders, and track attendance.
### Implementation
\*\*Step 1: Create Event\*\*
Admin creates an event:
```python
# /create\_event command (admin only)
if u != ADMIN\_USER\_ID:
Api.sendMessage("Unauthorized")
else:
Api.sendMessage("Enter event name:")
Bot.waitForInput("event\_name")
```
```python
# event\_name command
event\_name = msg
Bot.storeData("current\_event\_name", event\_name)
Api.sendMessage("Enter event date and time (YYYY-MM-DD HH:MM):")
Bot.waitForInput("event\_datetime")
```
```python
# event\_datetime command
event\_datetime = msg
event\_name = Bot.fetchData("current\_event\_name")
# Store event
event\_id = Bot.uniqueID()
Bot.storeData(f"event\_{event\_id}", {
"name": event\_name,
"datetime": event\_datetime,
"attendees": []
})
Api.sendMessage(f"✅ Event '{event\_name}' created!")
Api.sendMessage(f"Event ID: {event\_id}")
# Broadcast event announcement
Bot.sendBroadcast(
code=f"Api.sendMessage('📅 New Event: {event\_name}\\nDate: {event\_datetime}\\nRSVP: /rsvp\_{event\_id}')"
)
```
\*\*Step 2: RSVP System\*\*
Allow users to RSVP to an event:
```python
# /rsvp\_EVENT\_ID command (dynamic command)
event\_id = command.split("\_")[1] # Extract ID from command
event\_data = Bot.fetchData(f"event\_{event\_id}")
if not event\_data:
Api.sendMessage("Event not found")
else:
# Check if already RSVP'd
attendees = event\_data.get("attendees", [])
if u in attendees:
Api.sendMessage("You're already registered for this event!")
else:
attendees.append(u)
event\_data["attendees"] = attendees
Bot.storeData(f"event\_{event\_id}", event\_data)
User.storeData(f"rsvp\_{event\_id}", True)
Api.sendMessage(f"✅ You're registered for: {event\_data['name']}")
Api.sendMessage(f"Date: {event\_data['datetime']}")
```
\*\*Step 3: Event Reminders\*\*
Schedule reminders for attendees:
```python
# Admin schedules reminder (1 hour before event)
event\_data = Bot.fetchData(f"event\_{event\_id}")
attendees = event\_data.get("attendees", [])
for attendee\_id in attendees:
# Calculate seconds until 1 hour before event
# (In production, calculate from event\_datetime)
seconds\_until\_reminder = 3600 # Example: 1 hour
Bot.scheduleCommand(
seconds\_until\_reminder,
"send\_event\_reminder",
user\_id=attendee\_id,
params=event\_id
)
Api.sendMessage(f"Reminders scheduled for {len(attendees)} attendees")
```
```python
# send\_event\_reminder command
event\_id = params
event\_data = Bot.fetchData(f"event\_{event\_id}")
if event\_data:
Api.sendMessage(f"⏰ Reminder: {event\_data['name']}")
Api.sendMessage(f"Event starts in 1 hour!")
Api.sendMessage(f"Time: {event\_data['datetime']}")
```
\*\*\*
## E-Commerce Bot
### Overview
A comprehensive e-commerce bot with product catalog, shopping cart, and checkout.
### Implementation
\*\*Step 1: Product Catalog\*\*
```python
# /shop command
products = Bot.fetchData("products") or {
"1": {"name": "Product A", "price": 10.00, "stock": 50},
"2": {"name": "Product B", "price": 15.00, "stock": 30},
"3": {"name": "Product C", "price": 20.00, "stock": 20}
}
Api.sendMessage("🛍️ Welcome to our shop!")
for product\_id, product in products.items():
Api.sendMessage(
f"{product\_id}. {product['name']} - ${product['price']:.2f}\n"
f" Stock: {product['stock']} units\n"
f" Buy: /buy\_{product\_id}"
)
```
\*\*Step 2: Add to Cart\*\*
```python
# /buy\_1 command (dynamic)
product\_id = command.split("\_")[1]
products = Bot.fetchData("products")
product = products.get(product\_id)
if not product:
Api.sendMessage("Product not found")
else:
# Get user's cart
cart = User.fetchData("cart") or {}
if product\_id in cart:
cart[product\_id] += 1
else:
cart[product\_id] = 1
User.storeData("cart", cart)
Api.sendMessage(f"✅ Added {product['name']} to cart!")
Api.sendMessage(f"Cart total: {sum(cart.values())} items")
Api.sendMessage("View cart: /cart")
```
\*\*Step 3: View Cart and Checkout\*\*
```python
# /cart command
cart = User.fetchData("cart") or {}
if not cart:
Api.sendMessage("Your cart is empty")
else:
products = Bot.fetchData("products")
total = 0
Api.sendMessage("🛒 Your Cart:")
for product\_id, quantity in cart.items():
product = products[product\_id]
subtotal = product['price'] \* quantity
total += subtotal
Api.sendMessage(
f"{product['name']} x{quantity} = ${subtotal:.2f}"
)
Api.sendMessage(f"\n💰 Total: ${total:.2f}")
Api.sendMessage("Checkout: /checkout")
```
```python
# /checkout command
cart = User.fetchData("cart") or {}
if not cart:
Api.sendMessage("Your cart is empty")
else:
products = Bot.fetchData("products")
total = 0
for product\_id, quantity in cart.items():
total += products[product\_id]['price'] \* quantity
# Generate payment using Oxapay
client = Lib.Oxapay.post("YOUR\_MERCHANT\_API\_KEY")
invoice = client.createInvoice({
"amount": total,
"currency": "USD",
"description": f"Order for {len(cart)} items"
})
Api.sendMessage(f"Please complete payment:")
Api.sendMessage(invoice["url"])
User.storeData("pending\_order", {
"cart": cart,
"total": total,
"payment\_id": invoice["id"]
})
```
\*\*\*
## Customer Support Bot
### Overview
An intelligent customer support bot with ticket system and AI-powered responses.
### Implementation
\*\*Step 1: Create Support Ticket\*\*
```python
# /support command
Api.sendMessage("🎫 Create Support Ticket")
Api.sendMessage("Please describe your issue:")
Bot.waitForInput("create\_ticket")
```
```python
# create\_ticket command
issue\_description = msg
ticket\_id = Bot.uniqueID()
# Store ticket
Bot.storeData(f"ticket\_{ticket\_id}", {
"user\_id": u,
"description": issue\_description,
"status": "open",
"created": time.time(),
"messages": [{"user": u, "text": issue\_description, "time": time.time()}]
})
Api.sendMessage(f"✅ Ticket created: #{ticket\_id}")
Api.sendMessage("Our support team will respond shortly.")
# Notify admin
Api.sendMessage(
f"🎫 New Support Ticket #{ticket\_id}\nUser: {u}\n{issue\_description}",
chat\_id=ADMIN\_USER\_ID
)
```
\*\*Step 2: AI-Powered Auto-Response\*\*
```python
# create\_ticket command (enhanced with AI)
issue\_description = msg
# Get AI suggestion
ai\_client = Lib.AI.client(provider="openai", apiKey="YOUR\_API\_KEY")
response = ai\_client.chat(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a customer support assistant. Provide helpful solutions to user issues."},
{"role": "user", "content": issue\_description}
]
)
ai\_suggestion = response['choices'][0]['message']['content']
Api.sendMessage("💡 Suggested Solution:")
Api.sendMessage(ai\_suggestion)
Api.sendMessage("\nDid this help? /yes or /no")
User.storeData("pending\_feedback", {
"ticket\_id": ticket\_id,
"suggestion": ai\_suggestion
})
```
\*\*\*
## Subscription Management Bot
### Overview
Manage recurring subscriptions with automatic renewal reminders and payment processing.
### Implementation
\*\*Step 1: Subscribe\*\*
```python
# /subscribe command
Api.sendMessage("📦 Premium Subscription")
Api.sendMessage("Benefits:")
Api.sendMessage("• Unlimited access")
Api.sendMessage("• Priority support")
Api.sendMessage("• Exclusive features")
Api.sendMessage("\n💵 $9.99/month")
Api.sendMessage("\nSubscribe: /confirm\_subscribe")
```
\*\*Step 2: Process Subscription\*\*
```python
# /confirm\_subscribe command
# Generate payment using Oxapay
client = Lib.Oxapay.post("YOUR\_MERCHANT\_API\_KEY")
invoice = client.createInvoice({
"amount": total,
"currency": "USD",
"description": f"Order for {len(cart)} items"
})
Api.sendMessage(f"Please complete payment:")
Api.sendMessage(invoice["url"])
User.storeData("pending\_order", {
"cart": cart,
"total": total,
"payment\_id": invoice["id"]
})
```
\*\*Step 3: Renewal Reminders\*\*
```python
# After successful payment
User.storeData("subscription\_active", True)
User.storeData("subscription\_start", time.time())
User.storeData("subscription\_expires", time.time() + (30 \* 24 \* 3600)) # 30 days
# Schedule renewal reminder (25 days = 2,160,000 seconds)
Bot.scheduleCommand(2160000, "send\_renewal\_reminder")
Api.sendMessage("✅ Subscription activated!")
Api.sendMessage("Expires in 30 days")
```
```python
# send\_renewal\_reminder command
Api.sendMessage("⏰ Subscription Renewal Reminder")
Api.sendMessage("Your subscription expires in 5 days!")
Api.sendMessage("Renew now: /renew")
```
\*\*\*
These real-world use cases demonstrate the power and flexibility of TeleBot Studio. By combining features creatively, you can build bots for virtually any purpose—from e-commerce and customer support to blockchain applications and AI-powered assistants.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/real-world.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.