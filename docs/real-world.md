# Real-World Examples and Use Cases
This section demonstrates how to apply TeleBot Studio's features and libraries in real-world scenarios. By combining workflows, advanced commands, and external integrations, you can create bots that solve practical problems and enhance user engagement.
***
## Referral System
### Overview
A referral system tracks users who invite others to the bot and rewards them with points or other incentives. This use case involves:
1. Generating unique referral links
2. Tracking referrals
3. Rewarding users based on their referral count
4. Displaying leaderboards for top referrers
### Implementation
**Step 1: Generate Unique Referral Links**
In the `/start` command, include the user's ID as a parameter to generate a referral link:
```python
bot_info = Bot.getInfo()
bot_username = bot_info['username']
Api.sendMessage(f"Invite your friends using this link:")
Api.sendMessage(f"t.me/{bot_username}?start={u}")
```
**Step 2: Track Referrals**
In the `/start` command, check if a referral ID is provided:
```python
referrer_id = params
if referrer_id and referrer_id != str(u):
# Check if this is first time being referred
already_referred = User.fetchData("referred_by")
if not already_referred:
User.storeData("referred_by", referrer_id)
# Award points to referrer
referrer_points = User.resOf("points", int(referrer_id))
referrer_points.add(10)
# Track referral count
referral_count = Bot.res(f"referral_count_{referrer_id}")
referral_count.add(1)
# Notify referrer
Api.sendMessage(
f"User {u} joined using your referral link! You earned 10 points!",
chat_id=int(referrer_id)
)
Api.sendMessage("Welcome! You were referred by a friend.")
```
**Step 3: Reward Users**
Track and display referral rewards dynamically:
```python
# /mypoints command
user_points = User.res("points")
Api.sendMessage(f"You have {user_points.value()} points!")
```
**Step 4: Create a Leaderboard**
Display the top referrers:
```python
# /leaderboard command
# Get top 10 referrers
top_referrers_data = []
for i in range(100): # Check first 100 user IDs (example)
referral_count = Bot.res(f"referral_count_{i}").value()
if referral_count and referral_count > 0:
top_referrers_data.append({"user": i, "count": referral_count})
# Sort by count
top_referrers_data.sort(key=lambda x: x['count'], reverse=True)
top_10 = top_referrers_data[:10]
Api.sendMessage("🏆 Top Referrers:")
for idx, entry in enumerate(top_10, 1):
Api.sendMessage(f"{idx}. User {entry['user']}: {entry['count']} referrals")
```
***
## Payment Automation Bot
### Overview
This bot automates payment handling using the `Lib.Oxapay` library. It can:
1. Generate payment requests
2. Confirm payment status
3. Notify users of successful payments
### Implementation
**Step 1: Set Up Oxapay Client**
Configure the Oxapay client with your API key:
```python
client = Lib.Oxapay.post("your_merchant_api_key")
```
**Step 2: Generate Payment Requests**
Request payment for specific amounts:
```python
# /subscribe command
payment_details = client.createInvoice({
"amount": 10.00,
"currency": "USD",
"description": "Monthly subscription fee"
})
Api.sendMessage(f"Please make your payment here:")
Api.sendMessage(payment_details["url"])
# Store payment ID for verification
User.storeData("pending_payment_id", payment_details["id"])
```
**Step 3: Verify Payment Status**
Check payment status using webhooks or polling:
```python
# /check_payment command
payment_id = User.fetchData("pending_payment_id")
if not payment_id:
Api.sendMessage("No pending payment found.")
else:
# Check payment status via webhook or API call
payment_info = client.getPaymentStatus(payment_id)
status = payment_info.get("status", "pending")
if status == "completed":
Api.sendMessage("✅ Payment confirmed! Thank you!")
# Grant subscription
User.storeData("subscribed", True)
User.storeData("subscription_date", time.time())
User.removeData("pending_payment_id")
# Award premium points
points = User.res("points")
points.add(1000)
elif status == "expired" or status == "cancelled":
Api.sendMessage("❌ Payment expired or cancelled.")
User.removeData("pending_payment_id")
else:
Api.sendMessage(f"Payment status: {status}")
```
***
## Survey and Data Collection Bot
### Overview
This bot collects user input for surveys or forms and stores the data in a CSV file for easy analysis.
### Implementation
**Step 1: Collect User Responses**
Ask users a series of questions:
```python
# /survey command
Api.sendMessage("📋 Customer Satisfaction Survey")
Api.sendMessage("What is your name?")
Bot.waitForInput("survey_get_name")
```
Store the responses:
```python
# survey_get_name command
name = msg
User.storeData("survey_name", name)
Api.sendMessage(f"Thanks {name}! What is your email?")
Bot.waitForInput("survey_get_email")
```
**Continue Survey:**
```python
# survey_get_email command
email = msg
User.storeData("survey_email", email)
Api.sendMessage("How satisfied are you with our service? (1-5)")
Bot.waitForInput("survey_get_rating")
```
**Step 2: Save Data to CSV**
Save the collected data into a CSV file:
```python
# survey_get_rating command
rating = msg
if not rating.isdigit() or not (1 <= int(rating) <= 5):
Api.sendMessage("Please enter a number between 1 and 5:")
Bot.waitForInput("survey_get_rating")
else:
# Save to CSV
csv_handler = Lib.CSV.Table("survey_data.csv")
# Create CSV if doesn't exist
try:
csv_handler.row(0)
except:
csv_handler.create(["user_id", "name", "email", "rating", "date"])
# Add response
csv_handler.insert({
"user_id": u,
"name": User.fetchData("survey_name"),
"email": User.fetchData("survey_email"),
"rating": rating,
"date": Lib.DateTime.utcnow()
})
Api.sendMessage("✅ Thank you! Your responses have been saved.")
# Cleanup
User.removeData("survey_name")
User.removeData("survey_email")
```
***
## Crypto Airdrop Bot
### Overview
This bot automates cryptocurrency distributions using blockchain libraries.
### Implementation (TON Blockchain)
**Step 1: Configure Wallet**
Set up the distribution wallet:
```python
# Store wallet mnemonics (done once by admin)
Lib.TON.storeKey("your 24 word mnemonic phrase here")
```
**Step 2: Distribute Airdrops**
Send tokens to multiple recipients:
```python
# /start_airdrop command (admin only)
if u != ADMIN_USER_ID:
Api.sendMessage("Unauthorized")
else:
recipients = [
{"address": "EQRecipient1...", "amount": 10},
{"address": "EQRecipient2...", "amount": 15},
{"address": "EQRecipient3...", "amount": 20}
]
Api.sendMessage(f"Starting airdrop to {len(recipients)} recipients...")
success_count = 0
for recipient in recipients:
try:
result = Lib.TON.send(
to_address=recipient["address"],
amount=recipient["amount"],
comment="Airdrop reward"
)
success_count += 1
Api.sendMessage(f"✅ Sent {recipient['amount']} TON to {recipient['address'][:10]}...")
except Exception as e:
Api.sendMessage(f"❌ Failed: {recipient['address'][:10]}... - {str(e)}")
Api.sendMessage(f"Airdrop complete! {success_count}/{len(recipients)} successful")
```
**Step 3: User Registration for Airdrop**
Collect wallet addresses:
```python
# /register_wallet command
Api.sendMessage("Please enter your TON wallet address:")
Bot.waitForInput("save_wallet")
```
```python
# save_wallet command
wallet_address = msg
# Basic validation
if wallet_address.startswith("EQ") and len(wallet_address) > 40:
User.storeData("wallet_address", wallet_address)
Api.sendMessage("✅ Wallet registered successfully!")
Api.sendMessage("You'll be notified when airdrop begins.")
else:
Api.sendMessage("Invalid TON address. Please try again:")
Bot.waitForInput("save_wallet")
```
***
## Real-Time Notification Bot
### Overview
This bot uses webhooks to send real-time updates based on external events, such as sales or user actions.
### Implementation
**Step 1: Generate Webhook URL**
Generate a webhook URL for notifications:
```python
# /setup_notifications command
webhook_url = Lib.Webhook.getUrlFor("send_notification", user_id=u)
Api.sendMessage("Your notification webhook:")
Api.sendMessage(webhook_url)
Api.sendMessage("Configure this URL in your external system to receive notifications.")
User.storeData("webhook_configured", True)
```
**Step 2: Process Webhook Events**
Handle incoming webhook events in a command:
```python
# send_notification command
notification_data = options
event_type = notification_data.get('type', 'general')
message = notification_data.get('message', 'You have a new notification!')
if event_type == 'sale':
amount = notification_data.get('amount', 0)
Api.sendMessage(f"🎉 New Sale!")
Api.sendMessage(f"Amount: ${amount}")
# Award points
points = User.res("points")
points.add(int(amount) * 10)
elif event_type == 'alert':
Api.sendMessage(f"⚠️ Alert: {message}")
else:
Api.sendMessage(message)
```
***
## Event Management Bot
### Overview
This bot manages events, allowing users to RSVP, receive reminders, and track attendance.
### Implementation
**Step 1: Create Event**
Admin creates an event:
```python
# /create_event command (admin only)
if u != ADMIN_USER_ID:
Api.sendMessage("Unauthorized")
else:
Api.sendMessage("Enter event name:")
Bot.waitForInput("event_name")
```
```python
# event_name command
event_name = msg
Bot.storeData("current_event_name", event_name)
Api.sendMessage("Enter event date and time (YYYY-MM-DD HH:MM):")
Bot.waitForInput("event_datetime")
```
```python
# event_datetime command
event_datetime = msg
event_name = Bot.fetchData("current_event_name")
# Store event
event_id = Bot.uniqueID()
Bot.storeData(f"event_{event_id}", {
"name": event_name,
"datetime": event_datetime,
"attendees": []
})
Api.sendMessage(f"✅ Event '{event_name}' created!")
Api.sendMessage(f"Event ID: {event_id}")
# Broadcast event announcement
Bot.sendBroadcast(
code=f"Api.sendMessage('📅 New Event: {event_name}\\nDate: {event_datetime}\\nRSVP: /rsvp_{event_id}')"
)
```
**Step 2: RSVP System**
Allow users to RSVP to an event:
```python
# /rsvp_EVENT_ID command (dynamic command)
event_id = command.split("_")[1] # Extract ID from command
event_data = Bot.fetchData(f"event_{event_id}")
if not event_data:
Api.sendMessage("Event not found")
else:
# Check if already RSVP'd
attendees = event_data.get("attendees", [])
if u in attendees:
Api.sendMessage("You're already registered for this event!")
else:
attendees.append(u)
event_data["attendees"] = attendees
Bot.storeData(f"event_{event_id}", event_data)
User.storeData(f"rsvp_{event_id}", True)
Api.sendMessage(f"✅ You're registered for: {event_data['name']}")
Api.sendMessage(f"Date: {event_data['datetime']}")
```
**Step 3: Event Reminders**
Schedule reminders for attendees:
```python
# Admin schedules reminder (1 hour before event)
event_data = Bot.fetchData(f"event_{event_id}")
attendees = event_data.get("attendees", [])
for attendee_id in attendees:
# Calculate seconds until 1 hour before event
# (In production, calculate from event_datetime)
seconds_until_reminder = 3600 # Example: 1 hour
Bot.scheduleCommand(
seconds_until_reminder,
"send_event_reminder",
user_id=attendee_id,
params=event_id
)
Api.sendMessage(f"Reminders scheduled for {len(attendees)} attendees")
```
```python
# send_event_reminder command
event_id = params
event_data = Bot.fetchData(f"event_{event_id}")
if event_data:
Api.sendMessage(f"⏰ Reminder: {event_data['name']}")
Api.sendMessage(f"Event starts in 1 hour!")
Api.sendMessage(f"Time: {event_data['datetime']}")
```
***
## E-Commerce Bot
### Overview
A comprehensive e-commerce bot with product catalog, shopping cart, and checkout.
### Implementation
**Step 1: Product Catalog**
```python
# /shop command
products = Bot.fetchData("products") or {
"1": {"name": "Product A", "price": 10.00, "stock": 50},
"2": {"name": "Product B", "price": 15.00, "stock": 30},
"3": {"name": "Product C", "price": 20.00, "stock": 20}
}
Api.sendMessage("🛍️ Welcome to our shop!")
for product_id, product in products.items():
Api.sendMessage(
f"{product_id}. {product['name']} - ${product['price']:.2f}\n"
f" Stock: {product['stock']} units\n"
f" Buy: /buy_{product_id}"
)
```
**Step 2: Add to Cart**
```python
# /buy_1 command (dynamic)
product_id = command.split("_")[1]
products = Bot.fetchData("products")
product = products.get(product_id)
if not product:
Api.sendMessage("Product not found")
else:
# Get user's cart
cart = User.fetchData("cart") or {}
if product_id in cart:
cart[product_id] += 1
else:
cart[product_id] = 1
User.storeData("cart", cart)
Api.sendMessage(f"✅ Added {product['name']} to cart!")
Api.sendMessage(f"Cart total: {sum(cart.values())} items")
Api.sendMessage("View cart: /cart")
```
**Step 3: View Cart and Checkout**
```python
# /cart command
cart = User.fetchData("cart") or {}
if not cart:
Api.sendMessage("Your cart is empty")
else:
products = Bot.fetchData("products")
total = 0
Api.sendMessage("🛒 Your Cart:")
for product_id, quantity in cart.items():
product = products[product_id]
subtotal = product['price'] * quantity
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
for product_id, quantity in cart.items():
total += products[product_id]['price'] * quantity
# Generate payment using Oxapay
client = Lib.Oxapay.post("YOUR_MERCHANT_API_KEY")
invoice = client.createInvoice({
"amount": total,
"currency": "USD",
"description": f"Order for {len(cart)} items"
})
Api.sendMessage(f"Please complete payment:")
Api.sendMessage(invoice["url"])
User.storeData("pending_order", {
"cart": cart,
"total": total,
"payment_id": invoice["id"]
})
```
***
## Customer Support Bot
### Overview
An intelligent customer support bot with ticket system and AI-powered responses.
### Implementation
**Step 1: Create Support Ticket**
```python
# /support command
Api.sendMessage("🎫 Create Support Ticket")
Api.sendMessage("Please describe your issue:")
Bot.waitForInput("create_ticket")
```
```python
# create_ticket command
issue_description = msg
ticket_id = Bot.uniqueID()
# Store ticket
Bot.storeData(f"ticket_{ticket_id}", {
"user_id": u,
"description": issue_description,
"status": "open",
"created": time.time(),
"messages": [{"user": u, "text": issue_description, "time": time.time()}]
})
Api.sendMessage(f"✅ Ticket created: #{ticket_id}")
Api.sendMessage("Our support team will respond shortly.")
# Notify admin
Api.sendMessage(
f"🎫 New Support Ticket #{ticket_id}\nUser: {u}\n{issue_description}",
chat_id=ADMIN_USER_ID
)
```
**Step 2: AI-Powered Auto-Response**
```python
# create_ticket command (enhanced with AI)
issue_description = msg
# Get AI suggestion
ai_client = Lib.AI.client(provider="openai", apiKey="YOUR_API_KEY")
response = ai_client.chat(
model="gpt-4",
messages=[
{"role": "system", "content": "You are a customer support assistant. Provide helpful solutions to user issues."},
{"role": "user", "content": issue_description}
]
)
ai_suggestion = response['choices'][0]['message']['content']
Api.sendMessage("💡 Suggested Solution:")
Api.sendMessage(ai_suggestion)
Api.sendMessage("\nDid this help? /yes or /no")
User.storeData("pending_feedback", {
"ticket_id": ticket_id,
"suggestion": ai_suggestion
})
```
***
## Subscription Management Bot
### Overview
Manage recurring subscriptions with automatic renewal reminders and payment processing.
### Implementation
**Step 1: Subscribe**
```python
# /subscribe command
Api.sendMessage("📦 Premium Subscription")
Api.sendMessage("Benefits:")
Api.sendMessage("• Unlimited access")
Api.sendMessage("• Priority support")
Api.sendMessage("• Exclusive features")
Api.sendMessage("\n💵 $9.99/month")
Api.sendMessage("\nSubscribe: /confirm_subscribe")
```
**Step 2: Process Subscription**
```python
# /confirm_subscribe command
# Generate payment using Oxapay
client = Lib.Oxapay.post("YOUR_MERCHANT_API_KEY")
invoice = client.createInvoice({
"amount": total,
"currency": "USD",
"description": f"Order for {len(cart)} items"
})
Api.sendMessage(f"Please complete payment:")
Api.sendMessage(invoice["url"])
User.storeData("pending_order", {
"cart": cart,
"total": total,
"payment_id": invoice["id"]
})
```
**Step 3: Renewal Reminders**
```python
# After successful payment
User.storeData("subscription_active", True)
User.storeData("subscription_start", time.time())
User.storeData("subscription_expires", time.time() + (30 * 24 * 3600)) # 30 days
# Schedule renewal reminder (25 days = 2,160,000 seconds)
Bot.scheduleCommand(2160000, "send_renewal_reminder")
Api.sendMessage("✅ Subscription activated!")
Api.sendMessage("Expires in 30 days")
```
```python
# send_renewal_reminder command
Api.sendMessage("⏰ Subscription Renewal Reminder")
Api.sendMessage("Your subscription expires in 5 days!")
Api.sendMessage("Renew now: /renew")
```
***
These real-world use cases demonstrate the power and flexibility of TeleBot Studio. By combining features creatively, you can build bots for virtually any purpose—from e-commerce and customer support to blockchain applications and AI-powered assistants.
