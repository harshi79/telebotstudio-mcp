> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/reflib\_complete\_documentation.md).
# RefLib Library Documentation
## Table of Contents
1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Core Methods](#core-methods)
4. [Advanced Examples](#advanced-examples)
5. [Complete Bot Examples](#complete-bot-examples)
6. [Best Practices](#best-practices)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)
\*\*\*
## Introduction
`Lib.RefLib` is TBS's complete referral tracking system that enables you to build viral growth features into your bot. It handles everything from generating unique referral links to tracking who referred whom, maintaining leaderboards, and providing comprehensive analytics.
### Key Features
✅ \*\*Automatic Link Generation\*\* - Unique referral links for each user\
✅ \*\*Real-time Tracking\*\* - Instant referral detection from /start command\
✅ \*\*Campaign Tracking\*\* - Custom prefixes for marketing campaigns\
✅ \*\*Leaderboards\*\* - Built-in ranking and top referrers\
✅ \*\*Analytics\*\* - Comprehensive statistics and insights\
✅ \*\*Multi-tier Support\*\* - Track referral chains\
✅ \*\*Anti-fraud\*\* - Prevents self-referral and duplicates
### How It Works
1. \*\*User generates referral link\*\* using `getLink()`
2. \*\*User shares link\*\* with friends via social media, messages, etc.
3. \*\*New user clicks link\*\* and starts bot with `/start`
4. \*\*RefLib tracks automatically\*\* using `track()` in your /start command
5. \*\*Both users get rewards\*\* via your custom callback functions
6. \*\*System maintains stats\*\* for leaderboards and analytics
\*\*\*
## Quick Start
### Basic Implementation (5 minutes)
```python
# Command: start
# In your /start command, add this:
def handle\_new\_referral(referrer\_info):
"""Called when someone joins via referral link"""
# Welcome the new user
Api.sendMessage("🎉 Welcome! You earned 100 points!")
User.res("points").add(100)
# Reward the referrer
referrer\_id = referrer\_info['id']
User.resOf("points", referrer\_id).add(50)
# Notify the referrer
Api.sendMessage(
chat\_id=referrer\_id,
text=f"✅ {message.from\_user.first\_name} joined via your link! +50 points"
)
# Track referrals automatically
Lib.RefLib.track(
on\_attracted=handle\_new\_referral,
on\_touch\_own\_link=lambda: Api.sendMessage("❌ You can't refer yourself!"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
# Command: referral
# Show user their referral link and stats
link = Lib.RefLib.getLink()
count = Lib.RefLib.getRefCount()
rank = Lib.RefLib.getRank()
message = f"""
🔗 Your Referral Link:
{link}
📊 Your Stats:
• Total Referrals: {count}
• Your Rank: #{rank}
💰 Rewards:
• You earn: 50 points per referral
• They earn: 100 welcome points
Share your link and earn! 🚀
"""
Api.sendMessage(message)
```
That's it! You now have a complete referral system.
\*\*\*
## Core Methods
### 1. getLink()
Generate a unique referral link for the current user.
#### Syntax
```python
Lib.RefLib.getLink(bot\_name=None, prefix=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| ---------- | ---- | ----------- | ----------------------------------- |
| `bot\_name` | str | Current bot | Bot username (optional) |
| `prefix` | str | None | Custom campaign prefix for tracking |
#### Returns
\* \*\*str\*\*: Complete referral link (e.g., `https://t.me/yourbot?start=ref\_123456`)
#### Examples
```python
# Basic usage - generates link for current user
link = Lib.RefLib.getLink()
Api.sendMessage(f"Your link: {link}")
# With custom bot name
link = Lib.RefLib.getLink(bot\_name="myotherbot")
Api.sendMessage(f"Link: {link}")
# With campaign prefix for tracking
summer\_link = Lib.RefLib.getLink(prefix="summer2024")
twitter\_link = Lib.RefLib.getLink(prefix="twitter")
youtube\_link = Lib.RefLib.getLink(prefix="youtube")
# Send different links for different campaigns
Api.sendMessage(f"Summer promo: {summer\_link}")
```
#### Use Cases
\* Generate personal referral links
\* Create campaign-specific tracking links
\* Share links via different channels
\* Track marketing campaign performance
\*\*\*
### 2. track()
Automatically track referrals when users start the bot. \*\*Must be called in /start command.\*\*
#### Syntax
```python
Lib.RefLib.track(
on\_attracted=None,
on\_touch\_own\_link=None,
on\_already\_attracted=None
)
```
#### Parameters
| Parameter | Type | Description |
| ---------------------- | -------- | ---------------------------------------------------------------------- |
| `on\_attracted` | function | Called when new user joins via referral (receives referrer\\_info dict) |
| `on\_touch\_own\_link` | function | Called when user clicks their own link |
| `on\_already\_attracted` | function | Called when existing user clicks referral link again |
#### Callback Data Structures
\*\*on\\_attracted\*\* receives referrer\\_info dict:
```python
{
'id': '123456789', # Referrer's user ID
'first\_name': 'John', # Referrer's first name
'username': 'johndoe', # Referrer's username (may be None)
'date': '2024-01-15 10:30', # When they referred this user
'prefix': 'summer2024' # Campaign prefix (if used)
}
```
#### Returns
\* \*\*bool\*\*: True if tracking was successful
#### Examples
```python
# Simple tracking with inline callbacks
Lib.RefLib.track(
on\_attracted=lambda ref: Api.sendMessage(f"Welcome! Referred by {ref['first\_name']}"),
on\_touch\_own\_link=lambda: Api.sendMessage("That's your own link!"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
# Detailed tracking with custom functions
def handle\_new\_referral(referrer\_info):
new\_user\_name = message.from\_user.first\_name
referrer\_name = referrer\_info['first\_name']
referrer\_id = referrer\_info['id']
# Welcome new user
Api.sendMessage(
f"🎉 Welcome {new\_user\_name}!\n"
f"You were referred by {referrer\_name}\n"
f"+100 points!"
)
User.res("points").add(100)
# Reward referrer
User.resOf("points", referrer\_id).add(50)
# Notify referrer
Api.sendMessage(
chat\_id=referrer\_id,
text=f"🎊 {new\_user\_name} joined via your link!\n+50 points"
)
# Check for milestones
ref\_count = Lib.RefLib.getRefCount(referrer\_id)
if ref\_count == 10:
User.resOf("points", referrer\_id).add(500)
Api.sendMessage(
chat\_id=referrer\_id,
text="🏆 MILESTONE! 10 referrals achieved! +500 bonus points!"
)
def handle\_self\_referral():
Api.sendMessage(
"❌ Nice try! You can't refer yourself 😉\n"
"Share your link with friends instead!"
)
def handle\_returning\_user():
last\_visit = User.fetchData("last\_visit")
Api.sendMessage(f"Welcome back! Last visit: {last\_visit}")
User.storeData("last\_visit", Lib.DateTime.utcnow())
Lib.RefLib.track(
on\_attracted=handle\_new\_referral,
on\_touch\_own\_link=handle\_self\_referral,
on\_already\_attracted=handle\_returning\_user
)
# Campaign-based tracking
def handle\_campaign\_referral(referrer\_info):
campaign = referrer\_info.get('prefix', 'direct')
# Different rewards based on campaign
campaign\_rewards = {
'youtube': {'new\_user': 150, 'referrer': 75},
'twitter': {'new\_user': 125, 'referrer': 60},
'instagram': {'new\_user': 100, 'referrer': 50},
'direct': {'new\_user': 100, 'referrer': 50}
}
rewards = campaign\_rewards.get(campaign, campaign\_rewards['direct'])
# Reward both users
User.res("points").add(rewards['new\_user'])
User.resOf("points", referrer\_info['id']).add(rewards['referrer'])
Api.sendMessage(
f"🎉 Welcome from {campaign.upper()}!\n"
f"You earned {rewards['new\_user']} points!"
)
Lib.RefLib.track(on\_attracted=handle\_campaign\_referral)
```
#### Use Cases
\* Automatic referral detection
\* Reward distribution
\* Campaign performance tracking
\* User onboarding
\* Fraud prevention
\*\*\*
### 3. getRefList()
Get detailed list of all users referred by a specific user.
#### Syntax
```python
Lib.RefLib.getRefList(user\_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ---------------------------- |
| `user\_id` | str | Current user | User ID to get referrals for |
#### Returns
\* \*\*list\*\*: List of dictionaries containing referral details
Each referral dict contains:
```python
{
'id': '987654321', # Referred user's ID
'first\_name': 'Alice', # Referred user's first name
'username': 'alice123', # Referred user's username (may be None)
'date': '2024-01-15 10:30' # When they were referred
}
```
#### Examples
```python
# Get current user's referrals
refs = Lib.RefLib.getRefList()
if not refs:
Api.sendMessage("You haven't referred anyone yet! Share your link!")
else:
message = f"👥 Your Referrals ({len(refs)}):\n\n"
for i, ref in enumerate(refs, 1):
name = ref['first\_name']
username = f"@{ref['username']}" if ref['username'] else "No username"
date = ref['date'][:10] # Just the date part
message += f"{i}. {name} ({username})\n 📅 {date}\n\n"
Api.sendMessage(message)
# Get another user's referrals (admin command)
target\_user = "123456789"
refs = Lib.RefLib.getRefList(user\_id=target\_user)
Api.sendMessage(f"User {target\_user} has {len(refs)} referrals")
# Show recent referrals only (last 7 days)
refs = Lib.RefLib.getRefList()
from datetime import datetime, timedelta
week\_ago = datetime.now() - timedelta(days=7)
recent\_refs = [
ref for ref in refs
if datetime.strptime(ref['date'], '%Y-%m-%d %H:%M') > week\_ago
]
Api.sendMessage(f"New referrals this week: {len(recent\_refs)}")
# Export referral list to CSV
refs = Lib.RefLib.getRefList()
csv = Lib.CSV.Table("my\_referrals.csv")
csv.create(["id", "name", "username", "date"])
for ref in refs:
csv.insert({
"id": ref['id'],
"name": ref['first\_name'],
"username": ref.get('username', 'N/A'),
"date": ref['date']
})
Api.sendMessage("✅ Referral list exported!")
# Check if specific user was referred by current user
target\_id = "987654321"
refs = Lib.RefLib.getRefList()
is\_referred = any(ref['id'] == target\_id for ref in refs)
if is\_referred:
Api.sendMessage("Yes, this user was referred by you!")
```
#### Use Cases
\* Display referral lists
\* Export referral data
\* Check referral relationships
\* Generate reports
\* Audit referral chains
\*\*\*
### 4. getRefCount()
Get total number of referrals for a user.
#### Syntax
```python
Lib.RefLib.getRefCount(user\_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------ |
| `user\_id` | str | Current user | User ID to get count for |
#### Returns
\* \*\*int\*\*: Total number of referrals
#### Examples
```python
# Get current user's referral count
count = Lib.RefLib.getRefCount()
Api.sendMessage(f"You have {count} referrals")
# Get another user's count
user\_id = "123456789"
count = Lib.RefLib.getRefCount(user\_id)
Api.sendMessage(f"User {user\_id} has {count} referrals")
# Check for milestones
count = Lib.RefLib.getRefCount()
milestones = {
5: {"reward": 100, "message": "5 referrals! +100 bonus"},
10: {"reward": 250, "message": "10 referrals! +250 bonus"},
25: {"reward": 750, "message": "25 referrals! +750 bonus"},
50: {"reward": 2000, "message": "50 referrals! +2000 bonus"},
100: {"reward": 5000, "message": "100 referrals! +5000 bonus"}
}
if count in milestones:
milestone = milestones[count]
User.res("points").add(milestone["reward"])
Api.sendMessage(f"🎉 {milestone['message']}")
# Progress to next milestone
count = Lib.RefLib.getRefCount()
next\_milestone = None
for milestone in sorted(milestones.keys()):
if count < milestone:
next\_milestone = milestone
break
if next\_milestone:
needed = next\_milestone - count
Api.sendMessage(
f"You have {count} referrals!\n"
f"Get {needed} more for {milestones[next\_milestone]['reward']} bonus points!"
)
# Unlock premium based on referrals
count = Lib.RefLib.getRefCount()
if count >= 5:
User.storeData("premium", True)
Api.sendMessage("✨ Premium unlocked! You have 5+ referrals!")
else:
needed = 5 - count
Api.sendMessage(f"Get {needed} more referrals to unlock Premium!")
```
#### Use Cases
\* Display referral counts
\* Check milestones
\* Unlock features
\* Progress tracking
\* Reward distribution
\*\*\*
### 5. getTopList()
Get leaderboard of top referrers.
#### Syntax
```python
Lib.RefLib.getTopList(limit=10)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------- | --------------------------------- |
| `limit` | int | 10 | Number of top referrers to return |
#### Returns
\* \*\*dict\*\*: Dictionary mapping user\\_id to referral count, sorted by count (descending)
Format: `{'user\_id': count, 'user\_id': count, ...}`
#### Examples
```python
# Get top 10 referrers
top = Lib.RefLib.getTopList(limit=10)
message = "🏆 Top 10 Referrers:\n\n"
medals = ["🥇", "🥈", "🥉"]
for i, (user\_id, count) in enumerate(top.items(), 1):
medal = medals[i-1] if i <= 3 else f"{i}."
message += f"{medal} User {user\_id}: {count} referrals\n"
Api.sendMessage(message)
# Get top 3 with detailed info
top3 = Lib.RefLib.getTopList(limit=3)
message = "🏆 Top 3 Referrers:\n\n"
prizes = ["🥇 1st Place - $100", "🥈 2nd Place - $50", "🥉 3rd Place - $25"]
for i, (user\_id, count) in enumerate(top3.items()):
# Get user info from your database or Telegram API
message += f"{prizes[i]}\n"
message += f"User {user\_id}: {count} referrals\n\n"
Api.sendMessage(message)
# Show leaderboard with user's position
top = Lib.RefLib.getTopList(limit=20)
my\_rank = Lib.RefLib.getRank()
message = "🏆 Leaderboard:\n\n"
for i, (user\_id, count) in enumerate(top.items(), 1):
marker = "👉" if user\_id == str(u) else " "
message += f"{marker} {i}. User {user\_id}: {count}\n"
message += f"\n📍 Your rank: #{my\_rank}"
Api.sendMessage(message)
# Contest winners
top = Lib.RefLib.getTopList(limit=3)
if len(top) >= 3:
winners = list(top.items())
# Reward winners
User.resOf("balance", winners[0][0]).add(10000) # 1st place
User.resOf("balance", winners[1][0]).add(5000) # 2nd place
User.resOf("balance", winners[2][0]).add(2500) # 3rd place
# Announce winners
Api.sendMessage(
f"🎊 Contest Winners:\n\n"
f"🥇 {winners[0][0]}: {winners[0][1]} refs - 10,000 points\n"
f"🥈 {winners[1][0]}: {winners[1][1]} refs - 5,000 points\n"
f"🥉 {winners[2][0]}: {winners[2][1]} refs - 2,500 points"
)
# Leaderboard with percentages
top = Lib.RefLib.getTopList(limit=10)
total\_refs = sum(top.values())
message = "📊 Referral Distribution:\n\n"
for i, (user\_id, count) in enumerate(top.items(), 1):
percentage = (count / total\_refs \* 100) if total\_refs > 0 else 0
message += f"{i}. User {user\_id}: {count} ({percentage:.1f}%)\n"
Api.sendMessage(message)
```
#### Use Cases
\* Display leaderboards
\* Announce contest winners
\* Show top performers
\* Competitive features
\* Reward distribution
\*\*\*
### 6. getAttractedBy()
Get information about who referred the current user.
#### Syntax
```python
Lib.RefLib.getAttractedBy()
```
#### Parameters
None (always gets info for current user)
#### Returns
\* \*\*dict\*\* if user was referred, containing:
```python
{
'id': '123456789', # Referrer's user ID
'first\_name': 'John', # Referrer's first name
'username': 'johndoe', # Referrer's username (may be None)
'date': '2024-01-15 10:30' # When you were referred
}
```
\* \*\*None\*\* if user joined directly (not referred)
#### Examples
```python
# Check if user was referred
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(
f"You were referred by {referrer['first\_name']}\n"
f"Joined: {referrer['date']}"
)
else:
Api.sendMessage("You joined directly (no referral)")
# Show referrer with username
referrer = Lib.RefLib.getAttractedBy()
if referrer:
username = f"@{referrer['username']}" if referrer['username'] else "No username"
Api.sendMessage(f"Referred by: {referrer['first\_name']} ({username})")
# Thank your referrer
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(
chat\_id=referrer['id'],
text=f"💙 {message.from\_user.first\_name} just thanked you for the referral!"
)
Api.sendMessage("Thank you message sent to your referrer!")
else:
Api.sendMessage("You weren't referred by anyone")
# Multi-level referral rewards
referrer = Lib.RefLib.getAttractedBy()
if referrer:
# Give reward to direct referrer (tier 1)
User.resOf("points", referrer['id']).add(50)
# Check if referrer was also referred (tier 2)
tier2\_referrer = User.fetchData("referred\_by", user\_id=referrer['id'])
if tier2\_referrer:
User.resOf("points", tier2\_referrer).add(25)
Api.sendMessage("Rewards distributed to your referral chain!")
else:
Api.sendMessage("Direct referrer rewarded!")
else:
Api.sendMessage("No referrer to reward")
```
#### Use Cases
\* Display referrer info
\* Multi-tier rewards
\* Referral relationship tracking
\* Thank your referrer features
\* Referral chain analysis
\*\*\*
### 7. getRank()
Get user's position in the referral leaderboard.
#### Syntax
```python
Lib.RefLib.getRank(user\_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ----------------------- |
| `user\_id` | str | Current user | User ID to get rank for |
#### Returns
\* \*\*int\*\*: User's rank (1-based, where 1 is top referrer). Returns 0 if user has no referrals.
#### Examples
```python
# Get current user's rank
rank = Lib.RefLib.getRank()
if rank == 0:
Api.sendMessage("Start referring to get ranked!")
elif rank == 1:
Api.sendMessage("🥇 You're #1! Top referrer!")
elif rank <= 3:
Api.sendMessage(f"🏆 You're #{rank}! Keep it up!")
elif rank <= 10:
Api.sendMessage(f"📊 You're #{rank} in top 10!")
else:
Api.sendMessage(f"Your rank: #{rank}")
# Show rank with stats
rank = Lib.RefLib.getRank()
count = Lib.RefLib.getRefCount()
Api.sendMessage(
f"📊 Your Stats:\n\n"
f"🏆 Rank: #{rank}\n"
f"👥 Referrals: {count}"
)
# Rank-based rewards
rank = Lib.RefLib.getRank()
if rank == 1:
Api.sendMessage("🥇 #1 Referrer! Here's 1000 bonus points!")
User.res("points").add(1000)
elif rank <= 5:
Api.sendMessage(f"🏆 Top 5 Referrer (#{rank})! Here's 500 bonus points!")
User.res("points").add(500)
elif rank <= 10:
Api.sendMessage(f"⭐ Top 10 Referrer (#{rank})! Here's 250 bonus points!")
User.res("points").add(250)
# Progress towards better rank
rank = Lib.RefLib.getRank()
count = Lib.RefLib.getRefCount()
if rank > 1:
# Get count of person above you
top = Lib.RefLib.getTopList(limit=rank)
above\_you = list(top.values())[rank-2] # Person one rank above
needed = above\_you - count + 1
Api.sendMessage(
f"Your rank: #{rank}\n"
f"Get {needed} more referrals to move up!"
)
# Compare with another user
my\_rank = Lib.RefLib.getRank()
their\_rank = Lib.RefLib.getRank(user\_id="123456789")
if my\_rank < their\_rank:
Api.sendMessage(f"You're ahead! Your rank: #{my\_rank}, Theirs: #{their\_rank}")
else:
Api.sendMessage(f"They're ahead. Your rank: #{my\_rank}, Theirs: #{their\_rank}")
```
#### Use Cases
\* Display user ranking
\* Rank-based rewards
\* Progress tracking
\* Competitive features
\* Status display
\*\*\*
### 8. getStats()
Get comprehensive referral statistics for a user.
#### Syntax
```python
Lib.RefLib.getStats(user\_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------ |
| `user\_id` | str | Current user | User ID to get stats for |
#### Returns
\* \*\*dict\*\*: Dictionary containing comprehensive statistics
```python
{
'total': 25, # Total referrals
'recent\_7d': 5, # Referrals in last 7 days
'recent\_30d': 15, # Referrals in last 30 days
'rank': 3, # Current leaderboard rank
'top\_10\_percent': True # Whether in top 10% of referrers
}
```
#### Examples
```python
# Display comprehensive stats
stats = Lib.RefLib.getStats()
message = f"""
📊 Your Referral Statistics
👥 Total Referrals: {stats['total']}
📅 Last 7 Days: {stats['recent\_7d']}
📅 Last 30 Days: {stats['recent\_30d']}
🏆 Current Rank: #{stats['rank']}
⭐ Top 10%: {'Yes' if stats['top\_10\_percent'] else 'No'}
"""
Api.sendMessage(message)
# Performance analysis
stats = Lib.RefLib.getStats()
if stats['recent\_7d'] > stats['recent\_30d'] / 4:
Api.sendMessage("🔥 You're on fire! Growing faster this week!")
elif stats['recent\_7d'] == 0:
Api.sendMessage("📉 No new referrals this week. Time to share your link!")
# Achievement badges
stats = Lib.RefLib.getStats()
badges = []
if stats['total'] >= 100:
badges.append("💯 Century")
if stats['total'] >= 50:
badges.append("⭐ Star")
if stats['top\_10\_percent']:
badges.append("🏆 Elite")
if stats['recent\_7d'] >= 10:
badges.append("🔥 Hot Streak")
if badges:
Api.sendMessage(f"Your badges: {' '.join(badges)}")
# Weekly report
stats = Lib.RefLib.getStats()
message = f"""
📈 Weekly Referral Report
This Week: {stats['recent\_7d']} new referrals
This Month: {stats['recent\_30d']} new referrals
All Time: {stats['total']} total
Current Rank: #{stats['rank']}
Status: {'Top Performer 🌟' if stats['top\_10\_percent'] else 'Keep Growing 💪'}
{get\_motivational\_message(stats)}
"""
Api.sendMessage(message)
def get\_motivational\_message(stats):
if stats['recent\_7d'] == 0:
return "Share your link to get back on track!"
elif stats['recent\_7d'] >= 5:
return "Amazing week! You're crushing it!"
else:
return "Good progress! Keep sharing!"
# Compare time periods
stats = Lib.RefLib.getStats()
weekly\_avg = stats['recent\_30d'] / 4
if stats['recent\_7d'] > weekly\_avg:
improvement = ((stats['recent\_7d'] - weekly\_avg) / weekly\_avg \* 100)
Api.sendMessage(f"📈 Up {improvement:.1f}% vs your 30-day average!")
```
#### Use Cases
\* Performance tracking
\* Weekly/monthly reports
\* Achievement systems
\* Growth analysis
\* Motivation features
\*\*\*
### 9. clearUserData()
Clear all referral data for a specific user (admin function).
#### Syntax
```python
Lib.RefLib.clearUserData(user\_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------- |
| `user\_id` | str | Current user | User ID to clear data for |
#### Returns
\* \*\*bool\*\*: True if successful
#### Examples
```python
# Admin command to clear user data
if message.from\_user.id in ADMIN\_IDS:
target\_user = "123456789"
Lib.RefLib.clearUserData(user\_id=target\_user)
Api.sendMessage(f"✅ Cleared referral data for user {target\_user}")
else:
Api.sendMessage("❌ Admin only")
# User requests data deletion
Lib.RefLib.clearUserData() # Clears current user's data
Api.sendMessage("Your referral data has been deleted")
# Reset contest
if message.from\_user.id == ADMIN\_ID:
# Get all participants
top = Lib.RefLib.getTopList(limit=1000)
for user\_id in top.keys():
Lib.RefLib.clearUserData(user\_id=user\_id)
Api.sendMessage(f"🔄 Contest reset! Cleared data for {len(top)} users")
```
#### Use Cases
\* Data deletion requests
\* Contest resets
\* Fraud removal
\* User account cleanup
\* Admin moderation
\*\*\*
## Advanced Examples
### Multi-Tier Referral System
```python
# /start command - Track with multi-tier rewards
def handle\_referral(referrer\_info):
referrer\_id = referrer\_info['id']
new\_user\_name = message.from\_user.first\_name
# Tier 1: Direct referrer (50 points)
User.resOf("points", referrer\_id).add(50)
Api.sendMessage(
chat\_id=referrer\_id,
text=f"🎉 {new\_user\_name} joined! +50 points (Tier 1)"
)
# Tier 2: Store who referred current user
User.storeData("referred\_by", referrer\_id)
# Check if referrer was also referred (tier 2)
tier2\_referrer = User.fetchData("referred\_by", user\_id=referrer\_id)
if tier2\_referrer:
User.resOf("points", tier2\_referrer).add(25)
Api.sendMessage(
chat\_id=tier2\_referrer,
text=f"💰 {new\_user\_name} joined via your referral chain! +25 points (Tier 2)"
)
# Welcome new user
Api.sendMessage(f"Welcome {new\_user\_name}! +100 points")
User.res("points").add(100)
Lib.RefLib.track(on\_attracted=handle\_referral)
```
### Campaign Performance Tracking
```python
# Generate campaign links
youtube\_link = Lib.RefLib.getLink(prefix="youtube")
twitter\_link = Lib.RefLib.getLink(prefix="twitter")
instagram\_link = Lib.RefLib.getLink(prefix="instagram")
# /start command - Track campaigns
def track\_campaign(referrer\_info):
campaign = referrer\_info.get('prefix', 'direct')
# Store campaign data in CSV
campaigns = Lib.CSV.Table("campaigns.csv")
if campaigns.count() == 0:
campaigns.create(["campaign", "referrer\_id", "new\_user\_id", "date"])
campaigns.insert({
"campaign": campaign,
"referrer\_id": referrer\_info['id'],
"new\_user\_id": str(u),
"date": str(Lib.DateTime.utcnow())
})
# Campaign-specific rewards
rewards = {
'youtube': 100,
'twitter': 75,
'instagram': 75,
'direct': 50
}
points = rewards.get(campaign, 50)
User.resOf("points", referrer\_info['id']).add(points)
Api.sendMessage(f"Welcome from {campaign.upper()}!")
Lib.RefLib.track(on\_attracted=track\_campaign)
# /campaign\_stats command - View performance
campaigns = Lib.CSV.Table("campaigns.csv")
all\_data = campaigns.get()
stats = {}
for row in all\_data:
campaign = row['campaign']
stats[campaign] = stats.get(campaign, 0) + 1
message = "📊 Campaign Performance:\n\n"
for campaign, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
message += f"{campaign}: {count} referrals\n"
Api.sendMessage(message)
```
### Referral Contest System
```python
# /contest command - Start contest
if message.from\_user.id == ADMIN\_ID:
Bot.storeData("contest\_active", True)
Bot.storeData("contest\_start", Lib.DateTime.time())
Bot.storeData("contest\_end", Lib.DateTime.time() + (7 \* 24 \* 60 \* 60)) # 7 days
Api.sendMessage("🎪 7-day referral contest started!")
# /contest\_status command
if Bot.fetchData("contest\_active"):
end\_time = Bot.fetchData("contest\_end")
time\_left = end\_time - Lib.DateTime.time()
days\_left = int(time\_left / (24 \* 60 \* 60))
top3 = Lib.RefLib.getTopList(limit=3)
my\_rank = Lib.RefLib.getRank()
my\_count = Lib.RefLib.getRefCount()
message = f"""
🎪 REFERRAL CONTEST
⏰ Time Left: {days\_left} days
🏆 Current Leaders:
"""
prizes = ["$100 💰", "$50 💵", "$25 💸"]
for i, (user\_id, count) in enumerate(top3.items()):
message += f"{i+1}. User {user\_id}: {count} refs - {prizes[i]}\n"
message += f"\n📍 Your Position: #{my\_rank} ({my\_count} referrals)\n"
message += f"\n{Lib.RefLib.getLink()}"
Api.sendMessage(message)
# /end\_contest command
if message.from\_user.id == ADMIN\_ID:
if Bot.fetchData("contest\_active"):
Bot.storeData("contest\_active", False)
# Get winners
top3 = Lib.RefLib.getTopList(limit=3)
winners = list(top3.items())
# Distribute prizes
prizes = [10000, 5000, 2500]
for i, (user\_id, count) in enumerate(winners):
User.resOf("points", user\_id).add(prizes[i])
Api.sendMessage(
chat\_id=user\_id,
text=f"🎊 You won {i+1} place in the contest! +{prizes[i]} points!"
)
Api.sendMessage("Contest ended! Winners notified.")
```
### Gamified Referral System
```python
# /level command - Show referral level
count = Lib.RefLib.getRefCount()
levels = [
{"name": "Rookie", "min": 0, "max": 4, "icon": "🌱"},
{"name": "Bronze", "min": 5, "max": 9, "icon": "🥉"},
{"name": "Silver", "min": 10, "max": 24, "icon": "🥈"},
{"name": "Gold", "min": 25, "max": 49, "icon": "🥇"},
{"name": "Platinum", "min": 50, "max": 99, "icon": "💎"},
{"name": "Diamond", "min": 100, "max": 999999, "icon": "💠"}
]
current\_level = None
next\_level = None
for i, level in enumerate(levels):
if level["min"] <= count <= level["max"]:
current\_level = level
if i < len(levels) - 1:
next\_level = levels[i + 1]
break
message = f"{current\_level['icon']} Level: {current\_level['name']}\n"
message += f"Referrals: {count}\n\n"
if next\_level:
needed = next\_level["min"] - count
message += f"Next: {next\_level['name']} {next\_level['icon']}\n"
message += f"Get {needed} more referrals to level up!"
Api.sendMessage(message)
# Give level-based perks (store in user's own data)
perks = {
"Bronze": {"daily\_bonus": 10},
"Silver": {"daily\_bonus": 25, "support\_priority": True},
"Gold": {"daily\_bonus": 50, "support\_priority": True, "exclusive\_features": True},
"Platinum": {"daily\_bonus": 100, "support\_priority": True, "exclusive\_features": True, "vip": True},
"Diamond": {"daily\_bonus": 250, "support\_priority": True, "exclusive\_features": True, "vip": True, "lifetime\_premium": True}
}
level\_name = current\_level['name']
if level\_name in perks:
user\_perks = perks[level\_name]
# Store perks as JSON string or individual keys
User.storeData("daily\_bonus", user\_perks.get("daily\_bonus", 0))
if user\_perks.get("support\_priority"):
User.storeData("support\_priority", True)
if user\_perks.get("exclusive\_features"):
User.storeData("exclusive\_features", True)
if user\_perks.get("vip"):
User.storeData("vip", True)
if user\_perks.get("lifetime\_premium"):
User.storeData("lifetime\_premium", True)
```
\*\*\*
## Complete Bot Examples
### Example 1: Simple Referral Reward Bot
```python
# Command: start
# Track referrals and give rewards
def handle\_new\_referral(ref):
# Welcome new user
Api.sendMessage(
f"🎉 Welcome! You were referred by {ref['first\_name']}\n"
"You earned 100 points!"
)
User.res("points").add(100)
# Reward referrer
Api.sendMessage(
chat\_id=ref['id'],
text=f"✅ {message.from\_user.first\_name} joined via your link! +50 points"
)
User.resOf("points", ref['id']).add(50)
# Check milestones
check\_milestone(ref['id'])
def check\_milestone(user\_id):
count = Lib.RefLib.getRefCount(user\_id)
milestones = {5: 250, 10: 500, 25: 1500, 50: 5000}
if count in milestones:
bonus = milestones[count]
User.resOf("points", user\_id).add(bonus)
Api.sendMessage(
chat\_id=user\_id,
text=f"🎊 MILESTONE! {count} referrals! +{bonus} bonus points!"
)
Lib.RefLib.track(
on\_attracted=handle\_new\_referral,
on\_touch\_own\_link=lambda: Api.sendMessage("❌ That's your own referral link!"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back! Type /help to see commands.")
)
# Command: ref
# Show referral link and stats
link = Lib.RefLib.getLink()
count = Lib.RefLib.getRefCount()
rank = Lib.RefLib.getRank()
points = User.res("points").value()
message = f"""
🔗 Your Referral Link:
{link}
📊 Your Stats:
• Points: {points}
• Referrals: {count}
• Rank: #{rank if rank > 0 else 'Unranked'}
💰 Rewards:
• You earn: 50 points per referral
• They earn: 100 points for joining
• Bonus at 5, 10, 25, 50 referrals!
Share your link to earn! 🚀
"""
Api.sendMessage(message)
# Command: leaderboard
# Show top referrers
top = Lib.RefLib.getTopList(limit=10)
my\_rank = Lib.RefLib.getRank()
my\_count = Lib.RefLib.getRefCount()
message = "🏆 Top 10 Referrers:\n\n"
medals = ["🥇", "🥈", "🥉"]
for i, (user\_id, count) in enumerate(top.items(), 1):
medal = medals[i-1] if i <= 3 else f"{i}."
highlight = "👉 " if user\_id == str(u) else ""
message += f"{highlight}{medal} User {user\_id}: {count} referrals\n"
message += f"\n📍 Your rank: #{my\_rank} ({my\_count} referrals)"
Api.sendMessage(message)
# Command: myrefs
# Show detailed referral list
refs = Lib.RefLib.getRefList()
if not refs:
Api.sendMessage(
"You haven't referred anyone yet!\n\n"
f"Share your link: {Lib.RefLib.getLink()}"
)
else:
message = f"👥 Your Referrals ({len(refs)}):\n\n"
for i, ref in enumerate(refs, 1):
name = ref['first\_name']
username = f"@{ref['username']}" if ref['username'] else "No username"
date = ref['date'][:10]
message += f"{i}. {name} ({username})\n 📅 Joined: {date}\n\n"
Api.sendMessage(message)
```
### Example 2: Premium Unlock via Referrals
```python
# Command: start
# Track referrals
def handle\_new\_referral(ref):
Api.sendMessage(
f"🎉 Welcome! Referred by {ref['first\_name']}\n\n"
"Get 5 referrals to unlock Premium for FREE! 🌟"
)
check\_premium\_unlock(u)
Api.sendMessage(
chat\_id=ref['id'],
text=f"✅ {message.from\_user.first\_name} joined via your link!"
)
check\_premium\_unlock(ref['id'])
def check\_premium\_unlock(user\_id):
count = Lib.RefLib.getRefCount(user\_id)
has\_premium = User.fetchData("premium", user\_id=user\_id)
if count >= 5 and not has\_premium:
User.storeData("premium", True, user\_id=user\_id)
Api.sendMessage(
chat\_id=user\_id,
text="✨ PREMIUM UNLOCKED! You have 5+ referrals! 🎊"
)
Lib.RefLib.track(
on\_attracted=handle\_new\_referral,
on\_already\_attracted=lambda: Api.sendMessage("Welcome back! Type /help")
)
# Command: premium
# Check premium status
has\_premium = User.fetchData("premium")
count = Lib.RefLib.getRefCount()
if has\_premium:
Api.sendMessage(
"✨ Premium Status: ACTIVE\n\n"
"Premium Features:\n"
"✅ Ad-free experience\n"
"✅ Priority support\n"
"✅ Exclusive content\n"
"✅ Special badge\n\n"
f"You have {count} referrals. Thank you!"
)
else:
needed = max(0, 5 - count)
link = Lib.RefLib.getLink()
if needed == 0:
User.storeData("premium", True)
Api.sendMessage("✨ Premium unlocked! You have 5 referrals!")
else:
Api.sendMessage(
f"❌ Premium Status: INACTIVE\n\n"
f"Current Referrals: {count}/5\n"
f"Get {needed} more referrals to unlock Premium!\n\n"
f"Your link: {link}\n\n"
"Premium Benefits:\n"
"✨ Ad-free experience\n"
"✨ Priority support\n"
"✨ Exclusive content\n"
"✨ Special badge"
)
# Command: ref
# Show progress
link = Lib.RefLib.getLink()
count = Lib.RefLib.getRefCount()
has\_premium = User.fetchData("premium")
if has\_premium:
message = f"✨ Premium Active!\n\nYour link: {link}\n\nKeep sharing! 🚀"
else:
needed = 5 - count
progress = "🟢" \* count + "⚪" \* needed
message = f"""
Premium Progress: {count}/5
{progress}
Your Referral Link:
{link}
Get {needed} more referrals to unlock Premium! ✨
"""
Api.sendMessage(message)
```
\*\*\*
## Best Practices
### 1. Always Call track() in /start
```python
# ✅ CORRECT - track() in /start command
# Command: start
Lib.RefLib.track(
on\_attracted=handle\_referral,
on\_touch\_own\_link=lambda: Api.sendMessage("Can't refer yourself!"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
# ❌ WRONG - Don't call track() in other commands
# Command: referral
Lib.RefLib.track(...) # This won't work!
```
### 2. Reward Both Users
```python
# ✅ CORRECT - Reward both referrer and new user
def handle\_referral(referrer\_info):
# Reward new user
User.res("points").add(100)
Api.sendMessage("Welcome! +100 points")
# Reward referrer
User.resOf("points", referrer\_info['id']).add(50)
Api.sendMessage(
chat\_id=referrer\_info['id'],
text="New referral! +50 points"
)
Lib.RefLib.track(on\_attracted=handle\_referral)
# ❌ WRONG - Only rewarding one side reduces sharing motivation
```
### 3. Use Milestones for Motivation
```python
# ✅ CORRECT - Clear milestones create goals
milestones = {
5: {"reward": 250, "message": "Bronze Badge Unlocked!"},
10: {"reward": 500, "message": "Silver Badge Unlocked!"},
25: {"reward": 1500, "message": "Gold Badge Unlocked!"},
50: {"reward": 5000, "message": "Platinum Badge Unlocked!"}
}
count = Lib.RefLib.getRefCount()
if count in milestones:
milestone = milestones[count]
User.res("points").add(milestone["reward"])
Api.sendMessage(f"🎉 {milestone['message']} +{milestone['reward']} points!")
```
### 4. Show Progress
```python
# ✅ CORRECT - Show clear progress to next goal
count = Lib.RefLib.getRefCount()
next\_milestone = None
for milestone in [5, 10, 25, 50, 100]:
if count < milestone:
next\_milestone = milestone
break
if next\_milestone:
needed = next\_milestone - count
Api.sendMessage(
f"You have {count} referrals!\n"
f"Get {needed} more for a bonus! 🎁"
)
```
### 5. Use Prefixes for Campaign Tracking
```python
# ✅ CORRECT - Track different marketing channels
youtube\_link = Lib.RefLib.getLink(prefix="youtube")
twitter\_link = Lib.RefLib.getLink(prefix="twitter")
email\_link = Lib.RefLib.getLink(prefix="email")
# Then in track():
def handle\_referral(referrer\_info):
source = referrer\_info.get('prefix', 'direct')
# Log or reward differently based on source
campaigns = Lib.CSV.Table("campaigns.csv")
if campaigns.count() == 0:
campaigns.create(["source", "date"])
campaigns.insert({"source": source, "date": str(Lib.DateTime.utcnow())})
Lib.RefLib.track(on\_attracted=handle\_referral)
```
### 6. Cache Data When Possible
```python
# ✅ CORRECT - Cache expensive operations
cached\_count = User.fetchData("cached\_ref\_count")
cache\_time = User.fetchData("ref\_cache\_time") or 0
if Lib.DateTime.time() - cache\_time > 3600: # 1 hour
count = Lib.RefLib.getRefCount()
User.storeData("cached\_ref\_count", count)
User.storeData("ref\_cache\_time", Lib.DateTime.time())
else:
count = cached\_count
# ❌ WRONG - Calling getRefCount() too frequently
count = Lib.RefLib.getRefCount() # Don't do this in every message
```
### 7. Handle Edge Cases
```python
# ✅ CORRECT - Handle all scenarios
Lib.RefLib.track(
on\_attracted=lambda ref: handle\_referral(ref),
on\_touch\_own\_link=lambda: Api.sendMessage("Can't refer yourself! 😊"),
on\_already\_attracted=lambda: Api.sendMessage("Welcome back! 👋")
)
# ❌ WRONG - Missing callbacks
Lib.RefLib.track(on\_attracted=handle\_referral) # What about self-referral?
```
### 8. Clear Communication
```python
# ✅ CORRECT - Clear, motivating messages
message = f"""
🔗 Your Referral Link:
{link}
How it works:
1. Share your link with friends
2. They join and get 100 points
3. You get 50 points per referral
4. Reach milestones for bonuses!
Current: {count} referrals
Next bonus at: {next\_milestone} referrals
Start earning! 🚀
"""
# ❌ WRONG - Unclear or unmotivating
Api.sendMessage(f"Link: {link}") # Too minimal
```
\*\*\*
## Common Patterns
### Pattern 1: Basic Referral Bot
```python
# Minimal viable referral system
# Command: start
def handle\_referral(ref):
User.res("points").add(100)
User.resOf("points", ref['id']).add(50)
Api.sendMessage("Welcome! +100 points")
Api.sendMessage(chat\_id=ref['id'], text="New referral! +50 points")
Lib.RefLib.track(on\_attracted=handle\_referral)
# Command: ref
link = Lib.RefLib.getLink()
count = Lib.RefLib.getRefCount()
Api.sendMessage(f"Link: {link}\nReferrals: {count}")
```
### Pattern 2: Leaderboard Competition
```python
# Competitive referral system with rankings
# Command: leaderboard
top = Lib.RefLib.getTopList(limit=10)
my\_rank = Lib.RefLib.getRank()
message = "🏆 Leaderboard:\n\n"
for i, (uid, count) in enumerate(top.items(), 1):
marker = "👉" if uid == str(u) else ""
message += f"{marker}{i}. User {uid}: {count}\n"
message += f"\n📍 Your rank: #{my\_rank}"
Api.sendMessage(message)
```
### Pattern 3: Premium Unlock
```python
# Unlock features via referrals
# Command: premium
count = Lib.RefLib.getRefCount()
if count >= 5:
User.storeData("premium", True)
Api.sendMessage("✨ Premium unlocked!")
else:
needed = 5 - count
Api.sendMessage(f"Get {needed} more referrals for Premium")
```
### Pattern 4: Time-Limited Contest
```python
# Weekly/monthly contests
# Admin starts contest
Bot.storeData("contest\_end", Lib.DateTime.time() + (7\*24\*60\*60))
# Users check status
time\_left = Bot.fetchData("contest\_end") - Lib.DateTime.time()
days = int(time\_left / 86400)
top3 = Lib.RefLib.getTopList(limit=3)
Api.sendMessage(f"Contest ends in {days} days!\n\nLeaders:\n{format\_top3(top3)}")
```
\*\*\*
## Troubleshooting
### Issue: Referrals Not Being Tracked
\*\*Problem:\*\* New users clicking referral links but not being tracked.
\*\*Solution:\*\*
\* Ensure `track()` is called in `/start` command (not other commands)
\* Check that callbacks are properly defined
\* Verify users are actually using /start (not just opening the bot)
```python
# ✅ Correct placement
# Command: start
Lib.RefLib.track(on\_attracted=handle\_referral)
# ❌ Wrong placement
# Command: referral
Lib.RefLib.track(on\_attracted=handle\_referral) # Won't work!
```
### Issue: Self-Referral Not Blocked
\*\*Problem:\*\* Users able to refer themselves.
\*\*Solution:\*\*
\* Always provide `on\_touch\_own\_link` callback:
```python
Lib.RefLib.track(
on\_attracted=handle\_referral,
on\_touch\_own\_link=lambda: Api.sendMessage("Can't refer yourself!"), # Important!
on\_already\_attracted=lambda: Api.sendMessage("Welcome back!")
)
```
### Issue: Referral Count Seems Wrong
\*\*Problem:\*\* `getRefCount()` returns unexpected numbers.
\*\*Solution:\*\*
\* Check if you're passing correct `user\_id` parameter
\* Verify you're not accidentally clearing data
\* Remember it only counts successful referrals (tracked via `track()`)
```python
# Get current user's count
my\_count = Lib.RefLib.getRefCount()
# Get specific user's count
their\_count = Lib.RefLib.getRefCount(user\_id="123456789")
```
### Issue: Leaderboard Empty
\*\*Problem:\*\* `getTopList()` returns empty dict.
\*\*Solution:\*\*
\* Ensure `track()` has been set up and users have been referred
\* Check that you're using `track()` in /start command
\* Verify referrals are actually happening
### Issue: Campaign Prefix Not Working
\*\*Problem:\*\* Prefix not being detected in referrer\\_info.
\*\*Solution:\*\*
\* Ensure you're generating links with prefix:
```python
# ✅ Correct
link = Lib.RefLib.getLink(prefix="youtube")
# Then access in callback:
def handle\_referral(referrer\_info):
prefix = referrer\_info.get('prefix') # Will be "youtube"
```
### Issue: Stats Showing 0 for Recent Periods
\*\*Problem:\*\* `getStats()` shows 0 for recent\\_7d or recent\\_30d.
\*\*Solution:\*\*
\* Check that you have actual referrals in those time periods
\* Verify your system time/timezone is correct
\* Remember stats are based on referral dates, not current activity
\*\*\*
## Summary
`Lib.RefLib` provides everything you need for a complete referral system:
✅ \*\*Easy Setup\*\* - Just add `track()` to your /start command\
✅ \*\*Automatic Tracking\*\* - No manual referral detection needed\
✅ \*\*Complete Analytics\*\* - Counts, ranks, stats, and leaderboards\
✅ \*\*Flexible Rewards\*\* - Custom callbacks for any reward system\
✅ \*\*Campaign Tracking\*\* - Monitor performance of different channels\
✅ \*\*Anti-Fraud\*\* - Built-in self-referral prevention
Start building your viral bot today with `Lib.RefLib`! 🚀
\*\*\*
\*For more information, visit\* [\*TeleBotStudio.com\*](https://TeleBotStudio.com)
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/reflib\_complete\_documentation.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.