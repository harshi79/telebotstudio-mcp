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
***
## Introduction
`Lib.RefLib` is TBS's complete referral tracking system that enables you to build viral growth features into your bot. It handles everything from generating unique referral links to tracking who referred whom, maintaining leaderboards, and providing comprehensive analytics.
### Key Features
✅ **Automatic Link Generation** - Unique referral links for each user
✅ **Real-time Tracking** - Instant referral detection from /start command
✅ **Campaign Tracking** - Custom prefixes for marketing campaigns
✅ **Leaderboards** - Built-in ranking and top referrers
✅ **Analytics** - Comprehensive statistics and insights
✅ **Multi-tier Support** - Track referral chains
✅ **Anti-fraud** - Prevents self-referral and duplicates
### How It Works
1. **User generates referral link** using `getLink()`
2. **User shares link** with friends via social media, messages, etc.
3. **New user clicks link** and starts bot with `/start`
4. **RefLib tracks automatically** using `track()` in your /start command
5. **Both users get rewards** via your custom callback functions
6. **System maintains stats** for leaderboards and analytics
***
## Quick Start
### Basic Implementation (5 minutes)
```python
# Command: start
# In your /start command, add this:
def handle_new_referral(referrer_info):
"""Called when someone joins via referral link"""
# Welcome the new user
Api.sendMessage("🎉 Welcome! You earned 100 points!")
User.res("points").add(100)
# Reward the referrer
referrer_id = referrer_info['id']
User.resOf("points", referrer_id).add(50)
# Notify the referrer
Api.sendMessage(
chat_id=referrer_id,
text=f"✅ {message.from_user.first_name} joined via your link! +50 points"
)
# Track referrals automatically
Lib.RefLib.track(
on_attracted=handle_new_referral,
on_touch_own_link=lambda: Api.sendMessage("❌ You can't refer yourself!"),
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
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
***
## Core Methods
### 1. getLink()
Generate a unique referral link for the current user.
#### Syntax
```python
Lib.RefLib.getLink(bot_name=None, prefix=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| ---------- | ---- | ----------- | ----------------------------------- |
| `bot_name` | str | Current bot | Bot username (optional) |
| `prefix` | str | None | Custom campaign prefix for tracking |
#### Returns
* **str**: Complete referral link (e.g., `https://t.me/yourbot?start=ref_123456`)
#### Examples
```python
# Basic usage - generates link for current user
link = Lib.RefLib.getLink()
Api.sendMessage(f"Your link: {link}")
# With custom bot name
link = Lib.RefLib.getLink(bot_name="myotherbot")
Api.sendMessage(f"Link: {link}")
# With campaign prefix for tracking
summer_link = Lib.RefLib.getLink(prefix="summer2024")
twitter_link = Lib.RefLib.getLink(prefix="twitter")
youtube_link = Lib.RefLib.getLink(prefix="youtube")
# Send different links for different campaigns
Api.sendMessage(f"Summer promo: {summer_link}")
```
#### Use Cases
* Generate personal referral links
* Create campaign-specific tracking links
* Share links via different channels
* Track marketing campaign performance
***
### 2. track()
Automatically track referrals when users start the bot. **Must be called in /start command.**
#### Syntax
```python
Lib.RefLib.track(
on_attracted=None,
on_touch_own_link=None,
on_already_attracted=None
)
```
#### Parameters
| Parameter | Type | Description |
| ---------------------- | -------- | ---------------------------------------------------------------------- |
| `on_attracted` | function | Called when new user joins via referral (receives referrer\_info dict) |
| `on_touch_own_link` | function | Called when user clicks their own link |
| `on_already_attracted` | function | Called when existing user clicks referral link again |
#### Callback Data Structures
**on\_attracted** receives referrer\_info dict:
```python
{
'id': '123456789', # Referrer's user ID
'first_name': 'John', # Referrer's first name
'username': 'johndoe', # Referrer's username (may be None)
'date': '2024-01-15 10:30', # When they referred this user
'prefix': 'summer2024' # Campaign prefix (if used)
}
```
#### Returns
* **bool**: True if tracking was successful
#### Examples
```python
# Simple tracking with inline callbacks
Lib.RefLib.track(
on_attracted=lambda ref: Api.sendMessage(f"Welcome! Referred by {ref['first_name']}"),
on_touch_own_link=lambda: Api.sendMessage("That's your own link!"),
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
)
# Detailed tracking with custom functions
def handle_new_referral(referrer_info):
new_user_name = message.from_user.first_name
referrer_name = referrer_info['first_name']
referrer_id = referrer_info['id']
# Welcome new user
Api.sendMessage(
f"🎉 Welcome {new_user_name}!\n"
f"You were referred by {referrer_name}\n"
f"+100 points!"
)
User.res("points").add(100)
# Reward referrer
User.resOf("points", referrer_id).add(50)
# Notify referrer
Api.sendMessage(
chat_id=referrer_id,
text=f"🎊 {new_user_name} joined via your link!\n+50 points"
)
# Check for milestones
ref_count = Lib.RefLib.getRefCount(referrer_id)
if ref_count == 10:
User.resOf("points", referrer_id).add(500)
Api.sendMessage(
chat_id=referrer_id,
text="🏆 MILESTONE! 10 referrals achieved! +500 bonus points!"
)
def handle_self_referral():
Api.sendMessage(
"❌ Nice try! You can't refer yourself 😉\n"
"Share your link with friends instead!"
)
def handle_returning_user():
last_visit = User.fetchData("last_visit")
Api.sendMessage(f"Welcome back! Last visit: {last_visit}")
User.storeData("last_visit", Lib.DateTime.utcnow())
Lib.RefLib.track(
on_attracted=handle_new_referral,
on_touch_own_link=handle_self_referral,
on_already_attracted=handle_returning_user
)
# Campaign-based tracking
def handle_campaign_referral(referrer_info):
campaign = referrer_info.get('prefix', 'direct')
# Different rewards based on campaign
campaign_rewards = {
'youtube': {'new_user': 150, 'referrer': 75},
'twitter': {'new_user': 125, 'referrer': 60},
'instagram': {'new_user': 100, 'referrer': 50},
'direct': {'new_user': 100, 'referrer': 50}
}
rewards = campaign_rewards.get(campaign, campaign_rewards['direct'])
# Reward both users
User.res("points").add(rewards['new_user'])
User.resOf("points", referrer_info['id']).add(rewards['referrer'])
Api.sendMessage(
f"🎉 Welcome from {campaign.upper()}!\n"
f"You earned {rewards['new_user']} points!"
)
Lib.RefLib.track(on_attracted=handle_campaign_referral)
```
#### Use Cases
* Automatic referral detection
* Reward distribution
* Campaign performance tracking
* User onboarding
* Fraud prevention
***
### 3. getRefList()
Get detailed list of all users referred by a specific user.
#### Syntax
```python
Lib.RefLib.getRefList(user_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ---------------------------- |
| `user_id` | str | Current user | User ID to get referrals for |
#### Returns
* **list**: List of dictionaries containing referral details
Each referral dict contains:
```python
{
'id': '987654321', # Referred user's ID
'first_name': 'Alice', # Referred user's first name
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
name = ref['first_name']
username = f"@{ref['username']}" if ref['username'] else "No username"
date = ref['date'][:10] # Just the date part
message += f"{i}. {name} ({username})\n 📅 {date}\n\n"
Api.sendMessage(message)
# Get another user's referrals (admin command)
target_user = "123456789"
refs = Lib.RefLib.getRefList(user_id=target_user)
Api.sendMessage(f"User {target_user} has {len(refs)} referrals")
# Show recent referrals only (last 7 days)
refs = Lib.RefLib.getRefList()
from datetime import datetime, timedelta
week_ago = datetime.now() - timedelta(days=7)
recent_refs = [
ref for ref in refs
if datetime.strptime(ref['date'], '%Y-%m-%d %H:%M') > week_ago
]
Api.sendMessage(f"New referrals this week: {len(recent_refs)}")
# Export referral list to CSV
refs = Lib.RefLib.getRefList()
csv = Lib.CSV.Table("my_referrals.csv")
csv.create(["id", "name", "username", "date"])
for ref in refs:
csv.insert({
"id": ref['id'],
"name": ref['first_name'],
"username": ref.get('username', 'N/A'),
"date": ref['date']
})
Api.sendMessage("✅ Referral list exported!")
# Check if specific user was referred by current user
target_id = "987654321"
refs = Lib.RefLib.getRefList()
is_referred = any(ref['id'] == target_id for ref in refs)
if is_referred:
Api.sendMessage("Yes, this user was referred by you!")
```
#### Use Cases
* Display referral lists
* Export referral data
* Check referral relationships
* Generate reports
* Audit referral chains
***
### 4. getRefCount()
Get total number of referrals for a user.
#### Syntax
```python
Lib.RefLib.getRefCount(user_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------ |
| `user_id` | str | Current user | User ID to get count for |
#### Returns
* **int**: Total number of referrals
#### Examples
```python
# Get current user's referral count
count = Lib.RefLib.getRefCount()
Api.sendMessage(f"You have {count} referrals")
# Get another user's count
user_id = "123456789"
count = Lib.RefLib.getRefCount(user_id)
Api.sendMessage(f"User {user_id} has {count} referrals")
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
next_milestone = None
for milestone in sorted(milestones.keys()):
if count < milestone:
next_milestone = milestone
break
if next_milestone:
needed = next_milestone - count
Api.sendMessage(
f"You have {count} referrals!\n"
f"Get {needed} more for {milestones[next_milestone]['reward']} bonus points!"
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
* Display referral counts
* Check milestones
* Unlock features
* Progress tracking
* Reward distribution
***
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
* **dict**: Dictionary mapping user\_id to referral count, sorted by count (descending)
Format: `{'user_id': count, 'user_id': count, ...}`
#### Examples
```python
# Get top 10 referrers
top = Lib.RefLib.getTopList(limit=10)
message = "🏆 Top 10 Referrers:\n\n"
medals = ["🥇", "🥈", "🥉"]
for i, (user_id, count) in enumerate(top.items(), 1):
medal = medals[i-1] if i <= 3 else f"{i}."
message += f"{medal} User {user_id}: {count} referrals\n"
Api.sendMessage(message)
# Get top 3 with detailed info
top3 = Lib.RefLib.getTopList(limit=3)
message = "🏆 Top 3 Referrers:\n\n"
prizes = ["🥇 1st Place - $100", "🥈 2nd Place - $50", "🥉 3rd Place - $25"]
for i, (user_id, count) in enumerate(top3.items()):
# Get user info from your database or Telegram API
message += f"{prizes[i]}\n"
message += f"User {user_id}: {count} referrals\n\n"
Api.sendMessage(message)
# Show leaderboard with user's position
top = Lib.RefLib.getTopList(limit=20)
my_rank = Lib.RefLib.getRank()
message = "🏆 Leaderboard:\n\n"
for i, (user_id, count) in enumerate(top.items(), 1):
marker = "👉" if user_id == str(u) else " "
message += f"{marker} {i}. User {user_id}: {count}\n"
message += f"\n📍 Your rank: #{my_rank}"
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
total_refs = sum(top.values())
message = "📊 Referral Distribution:\n\n"
for i, (user_id, count) in enumerate(top.items(), 1):
percentage = (count / total_refs * 100) if total_refs > 0 else 0
message += f"{i}. User {user_id}: {count} ({percentage:.1f}%)\n"
Api.sendMessage(message)
```
#### Use Cases
* Display leaderboards
* Announce contest winners
* Show top performers
* Competitive features
* Reward distribution
***
### 6. getAttractedBy()
Get information about who referred the current user.
#### Syntax
```python
Lib.RefLib.getAttractedBy()
```
#### Parameters
None (always gets info for current user)
#### Returns
* **dict** if user was referred, containing:
```python
{
'id': '123456789', # Referrer's user ID
'first_name': 'John', # Referrer's first name
'username': 'johndoe', # Referrer's username (may be None)
'date': '2024-01-15 10:30' # When you were referred
}
```
* **None** if user joined directly (not referred)
#### Examples
```python
# Check if user was referred
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(
f"You were referred by {referrer['first_name']}\n"
f"Joined: {referrer['date']}"
)
else:
Api.sendMessage("You joined directly (no referral)")
# Show referrer with username
referrer = Lib.RefLib.getAttractedBy()
if referrer:
username = f"@{referrer['username']}" if referrer['username'] else "No username"
Api.sendMessage(f"Referred by: {referrer['first_name']} ({username})")
# Thank your referrer
referrer = Lib.RefLib.getAttractedBy()
if referrer:
Api.sendMessage(
chat_id=referrer['id'],
text=f"💙 {message.from_user.first_name} just thanked you for the referral!"
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
tier2_referrer = User.fetchData("referred_by", user_id=referrer['id'])
if tier2_referrer:
User.resOf("points", tier2_referrer).add(25)
Api.sendMessage("Rewards distributed to your referral chain!")
else:
Api.sendMessage("Direct referrer rewarded!")
else:
Api.sendMessage("No referrer to reward")
```
#### Use Cases
* Display referrer info
* Multi-tier rewards
* Referral relationship tracking
* Thank your referrer features
* Referral chain analysis
***
### 7. getRank()
Get user's position in the referral leaderboard.
#### Syntax
```python
Lib.RefLib.getRank(user_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ----------------------- |
| `user_id` | str | Current user | User ID to get rank for |
#### Returns
* **int**: User's rank (1-based, where 1 is top referrer). Returns 0 if user has no referrals.
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
above_you = list(top.values())[rank-2] # Person one rank above
needed = above_you - count + 1
Api.sendMessage(
f"Your rank: #{rank}\n"
f"Get {needed} more referrals to move up!"
)
# Compare with another user
my_rank = Lib.RefLib.getRank()
their_rank = Lib.RefLib.getRank(user_id="123456789")
if my_rank < their_rank:
Api.sendMessage(f"You're ahead! Your rank: #{my_rank}, Theirs: #{their_rank}")
else:
Api.sendMessage(f"They're ahead. Your rank: #{my_rank}, Theirs: #{their_rank}")
```
#### Use Cases
* Display user ranking
* Rank-based rewards
* Progress tracking
* Competitive features
* Status display
***
### 8. getStats()
Get comprehensive referral statistics for a user.
#### Syntax
```python
Lib.RefLib.getStats(user_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------ |
| `user_id` | str | Current user | User ID to get stats for |
#### Returns
* **dict**: Dictionary containing comprehensive statistics
```python
{
'total': 25, # Total referrals
'recent_7d': 5, # Referrals in last 7 days
'recent_30d': 15, # Referrals in last 30 days
'rank': 3, # Current leaderboard rank
'top_10_percent': True # Whether in top 10% of referrers
}
```
#### Examples
```python
# Display comprehensive stats
stats = Lib.RefLib.getStats()
message = f"""
📊 Your Referral Statistics
👥 Total Referrals: {stats['total']}
📅 Last 7 Days: {stats['recent_7d']}
📅 Last 30 Days: {stats['recent_30d']}
🏆 Current Rank: #{stats['rank']}
⭐ Top 10%: {'Yes' if stats['top_10_percent'] else 'No'}
"""
Api.sendMessage(message)
# Performance analysis
stats = Lib.RefLib.getStats()
if stats['recent_7d'] > stats['recent_30d'] / 4:
Api.sendMessage("🔥 You're on fire! Growing faster this week!")
elif stats['recent_7d'] == 0:
Api.sendMessage("📉 No new referrals this week. Time to share your link!")
# Achievement badges
stats = Lib.RefLib.getStats()
badges = []
if stats['total'] >= 100:
badges.append("💯 Century")
if stats['total'] >= 50:
badges.append("⭐ Star")
if stats['top_10_percent']:
badges.append("🏆 Elite")
if stats['recent_7d'] >= 10:
badges.append("🔥 Hot Streak")
if badges:
Api.sendMessage(f"Your badges: {' '.join(badges)}")
# Weekly report
stats = Lib.RefLib.getStats()
message = f"""
📈 Weekly Referral Report
This Week: {stats['recent_7d']} new referrals
This Month: {stats['recent_30d']} new referrals
All Time: {stats['total']} total
Current Rank: #{stats['rank']}
Status: {'Top Performer 🌟' if stats['top_10_percent'] else 'Keep Growing 💪'}
{get_motivational_message(stats)}
"""
Api.sendMessage(message)
def get_motivational_message(stats):
if stats['recent_7d'] == 0:
return "Share your link to get back on track!"
elif stats['recent_7d'] >= 5:
return "Amazing week! You're crushing it!"
else:
return "Good progress! Keep sharing!"
# Compare time periods
stats = Lib.RefLib.getStats()
weekly_avg = stats['recent_30d'] / 4
if stats['recent_7d'] > weekly_avg:
improvement = ((stats['recent_7d'] - weekly_avg) / weekly_avg * 100)
Api.sendMessage(f"📈 Up {improvement:.1f}% vs your 30-day average!")
```
#### Use Cases
* Performance tracking
* Weekly/monthly reports
* Achievement systems
* Growth analysis
* Motivation features
***
### 9. clearUserData()
Clear all referral data for a specific user (admin function).
#### Syntax
```python
Lib.RefLib.clearUserData(user_id=None)
```
#### Parameters
| Parameter | Type | Default | Description |
| --------- | ---- | ------------ | ------------------------- |
| `user_id` | str | Current user | User ID to clear data for |
#### Returns
* **bool**: True if successful
#### Examples
```python
# Admin command to clear user data
if message.from_user.id in ADMIN_IDS:
target_user = "123456789"
Lib.RefLib.clearUserData(user_id=target_user)
Api.sendMessage(f"✅ Cleared referral data for user {target_user}")
else:
Api.sendMessage("❌ Admin only")
# User requests data deletion
Lib.RefLib.clearUserData() # Clears current user's data
Api.sendMessage("Your referral data has been deleted")
# Reset contest
if message.from_user.id == ADMIN_ID:
# Get all participants
top = Lib.RefLib.getTopList(limit=1000)
for user_id in top.keys():
Lib.RefLib.clearUserData(user_id=user_id)
Api.sendMessage(f"🔄 Contest reset! Cleared data for {len(top)} users")
```
#### Use Cases
* Data deletion requests
* Contest resets
* Fraud removal
* User account cleanup
* Admin moderation
***
## Advanced Examples
### Multi-Tier Referral System
```python
# /start command - Track with multi-tier rewards
def handle_referral(referrer_info):
referrer_id = referrer_info['id']
new_user_name = message.from_user.first_name
# Tier 1: Direct referrer (50 points)
User.resOf("points", referrer_id).add(50)
Api.sendMessage(
chat_id=referrer_id,
text=f"🎉 {new_user_name} joined! +50 points (Tier 1)"
)
# Tier 2: Store who referred current user
User.storeData("referred_by", referrer_id)
# Check if referrer was also referred (tier 2)
tier2_referrer = User.fetchData("referred_by", user_id=referrer_id)
if tier2_referrer:
User.resOf("points", tier2_referrer).add(25)
Api.sendMessage(
chat_id=tier2_referrer,
text=f"💰 {new_user_name} joined via your referral chain! +25 points (Tier 2)"
)
# Welcome new user
Api.sendMessage(f"Welcome {new_user_name}! +100 points")
User.res("points").add(100)
Lib.RefLib.track(on_attracted=handle_referral)
```
### Campaign Performance Tracking
```python
# Generate campaign links
youtube_link = Lib.RefLib.getLink(prefix="youtube")
twitter_link = Lib.RefLib.getLink(prefix="twitter")
instagram_link = Lib.RefLib.getLink(prefix="instagram")
# /start command - Track campaigns
def track_campaign(referrer_info):
campaign = referrer_info.get('prefix', 'direct')
# Store campaign data in CSV
campaigns = Lib.CSV.Table("campaigns.csv")
if campaigns.count() == 0:
campaigns.create(["campaign", "referrer_id", "new_user_id", "date"])
campaigns.insert({
"campaign": campaign,
"referrer_id": referrer_info['id'],
"new_user_id": str(u),
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
User.resOf("points", referrer_info['id']).add(points)
Api.sendMessage(f"Welcome from {campaign.upper()}!")
Lib.RefLib.track(on_attracted=track_campaign)
# /campaign_stats command - View performance
campaigns = Lib.CSV.Table("campaigns.csv")
all_data = campaigns.get()
stats = {}
for row in all_data:
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
if message.from_user.id == ADMIN_ID:
Bot.storeData("contest_active", True)
Bot.storeData("contest_start", Lib.DateTime.time())
Bot.storeData("contest_end", Lib.DateTime.time() + (7 * 24 * 60 * 60)) # 7 days
Api.sendMessage("🎪 7-day referral contest started!")
# /contest_status command
if Bot.fetchData("contest_active"):
end_time = Bot.fetchData("contest_end")
time_left = end_time - Lib.DateTime.time()
days_left = int(time_left / (24 * 60 * 60))
top3 = Lib.RefLib.getTopList(limit=3)
my_rank = Lib.RefLib.getRank()
my_count = Lib.RefLib.getRefCount()
message = f"""
🎪 REFERRAL CONTEST
⏰ Time Left: {days_left} days
🏆 Current Leaders:
"""
prizes = ["$100 💰", "$50 💵", "$25 💸"]
for i, (user_id, count) in enumerate(top3.items()):
message += f"{i+1}. User {user_id}: {count} refs - {prizes[i]}\n"
message += f"\n📍 Your Position: #{my_rank} ({my_count} referrals)\n"
message += f"\n{Lib.RefLib.getLink()}"
Api.sendMessage(message)
# /end_contest command
if message.from_user.id == ADMIN_ID:
if Bot.fetchData("contest_active"):
Bot.storeData("contest_active", False)
# Get winners
top3 = Lib.RefLib.getTopList(limit=3)
winners = list(top3.items())
# Distribute prizes
prizes = [10000, 5000, 2500]
for i, (user_id, count) in enumerate(winners):
User.resOf("points", user_id).add(prizes[i])
Api.sendMessage(
chat_id=user_id,
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
current_level = None
next_level = None
for i, level in enumerate(levels):
if level["min"] <= count <= level["max"]:
current_level = level
if i < len(levels) - 1:
next_level = levels[i + 1]
break
message = f"{current_level['icon']} Level: {current_level['name']}\n"
message += f"Referrals: {count}\n\n"
if next_level:
needed = next_level["min"] - count
message += f"Next: {next_level['name']} {next_level['icon']}\n"
message += f"Get {needed} more referrals to level up!"
Api.sendMessage(message)
# Give level-based perks (store in user's own data)
perks = {
"Bronze": {"daily_bonus": 10},
"Silver": {"daily_bonus": 25, "support_priority": True},
"Gold": {"daily_bonus": 50, "support_priority": True, "exclusive_features": True},
"Platinum": {"daily_bonus": 100, "support_priority": True, "exclusive_features": True, "vip": True},
"Diamond": {"daily_bonus": 250, "support_priority": True, "exclusive_features": True, "vip": True, "lifetime_premium": True}
}
level_name = current_level['name']
if level_name in perks:
user_perks = perks[level_name]
# Store perks as JSON string or individual keys
User.storeData("daily_bonus", user_perks.get("daily_bonus", 0))
if user_perks.get("support_priority"):
User.storeData("support_priority", True)
if user_perks.get("exclusive_features"):
User.storeData("exclusive_features", True)
if user_perks.get("vip"):
User.storeData("vip", True)
if user_perks.get("lifetime_premium"):
User.storeData("lifetime_premium", True)
```
***
## Complete Bot Examples
### Example 1: Simple Referral Reward Bot
```python
# Command: start
# Track referrals and give rewards
def handle_new_referral(ref):
# Welcome new user
Api.sendMessage(
f"🎉 Welcome! You were referred by {ref['first_name']}\n"
"You earned 100 points!"
)
User.res("points").add(100)
# Reward referrer
Api.sendMessage(
chat_id=ref['id'],
text=f"✅ {message.from_user.first_name} joined via your link! +50 points"
)
User.resOf("points", ref['id']).add(50)
# Check milestones
check_milestone(ref['id'])
def check_milestone(user_id):
count = Lib.RefLib.getRefCount(user_id)
milestones = {5: 250, 10: 500, 25: 1500, 50: 5000}
if count in milestones:
bonus = milestones[count]
User.resOf("points", user_id).add(bonus)
Api.sendMessage(
chat_id=user_id,
text=f"🎊 MILESTONE! {count} referrals! +{bonus} bonus points!"
)
Lib.RefLib.track(
on_attracted=handle_new_referral,
on_touch_own_link=lambda: Api.sendMessage("❌ That's your own referral link!"),
on_already_attracted=lambda: Api.sendMessage("Welcome back! Type /help to see commands.")
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
my_rank = Lib.RefLib.getRank()
my_count = Lib.RefLib.getRefCount()
message = "🏆 Top 10 Referrers:\n\n"
medals = ["🥇", "🥈", "🥉"]
for i, (user_id, count) in enumerate(top.items(), 1):
medal = medals[i-1] if i <= 3 else f"{i}."
highlight = "👉 " if user_id == str(u) else ""
message += f"{highlight}{medal} User {user_id}: {count} referrals\n"
message += f"\n📍 Your rank: #{my_rank} ({my_count} referrals)"
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
name = ref['first_name']
username = f"@{ref['username']}" if ref['username'] else "No username"
date = ref['date'][:10]
message += f"{i}. {name} ({username})\n 📅 Joined: {date}\n\n"
Api.sendMessage(message)
```
### Example 2: Premium Unlock via Referrals
```python
# Command: start
# Track referrals
def handle_new_referral(ref):
Api.sendMessage(
f"🎉 Welcome! Referred by {ref['first_name']}\n\n"
"Get 5 referrals to unlock Premium for FREE! 🌟"
)
check_premium_unlock(u)
Api.sendMessage(
chat_id=ref['id'],
text=f"✅ {message.from_user.first_name} joined via your link!"
)
check_premium_unlock(ref['id'])
def check_premium_unlock(user_id):
count = Lib.RefLib.getRefCount(user_id)
has_premium = User.fetchData("premium", user_id=user_id)
if count >= 5 and not has_premium:
User.storeData("premium", True, user_id=user_id)
Api.sendMessage(
chat_id=user_id,
text="✨ PREMIUM UNLOCKED! You have 5+ referrals! 🎊"
)
Lib.RefLib.track(
on_attracted=handle_new_referral,
on_already_attracted=lambda: Api.sendMessage("Welcome back! Type /help")
)
# Command: premium
# Check premium status
has_premium = User.fetchData("premium")
count = Lib.RefLib.getRefCount()
if has_premium:
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
has_premium = User.fetchData("premium")
if has_premium:
message = f"✨ Premium Active!\n\nYour link: {link}\n\nKeep sharing! 🚀"
else:
needed = 5 - count
progress = "🟢" * count + "⚪" * needed
message = f"""
Premium Progress: {count}/5
{progress}
Your Referral Link:
{link}
Get {needed} more referrals to unlock Premium! ✨
"""
Api.sendMessage(message)
```
***
## Best Practices
### 1. Always Call track() in /start
```python
# ✅ CORRECT - track() in /start command
# Command: start
Lib.RefLib.track(
on_attracted=handle_referral,
on_touch_own_link=lambda: Api.sendMessage("Can't refer yourself!"),
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
)
# ❌ WRONG - Don't call track() in other commands
# Command: referral
Lib.RefLib.track(...) # This won't work!
```
### 2. Reward Both Users
```python
# ✅ CORRECT - Reward both referrer and new user
def handle_referral(referrer_info):
# Reward new user
User.res("points").add(100)
Api.sendMessage("Welcome! +100 points")
# Reward referrer
User.resOf("points", referrer_info['id']).add(50)
Api.sendMessage(
chat_id=referrer_info['id'],
text="New referral! +50 points"
)
Lib.RefLib.track(on_attracted=handle_referral)
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
next_milestone = None
for milestone in [5, 10, 25, 50, 100]:
if count < milestone:
next_milestone = milestone
break
if next_milestone:
needed = next_milestone - count
Api.sendMessage(
f"You have {count} referrals!\n"
f"Get {needed} more for a bonus! 🎁"
)
```
### 5. Use Prefixes for Campaign Tracking
```python
# ✅ CORRECT - Track different marketing channels
youtube_link = Lib.RefLib.getLink(prefix="youtube")
twitter_link = Lib.RefLib.getLink(prefix="twitter")
email_link = Lib.RefLib.getLink(prefix="email")
# Then in track():
def handle_referral(referrer_info):
source = referrer_info.get('prefix', 'direct')
# Log or reward differently based on source
campaigns = Lib.CSV.Table("campaigns.csv")
if campaigns.count() == 0:
campaigns.create(["source", "date"])
campaigns.insert({"source": source, "date": str(Lib.DateTime.utcnow())})
Lib.RefLib.track(on_attracted=handle_referral)
```
### 6. Cache Data When Possible
```python
# ✅ CORRECT - Cache expensive operations
cached_count = User.fetchData("cached_ref_count")
cache_time = User.fetchData("ref_cache_time") or 0
if Lib.DateTime.time() - cache_time > 3600: # 1 hour
count = Lib.RefLib.getRefCount()
User.storeData("cached_ref_count", count)
User.storeData("ref_cache_time", Lib.DateTime.time())
else:
count = cached_count
# ❌ WRONG - Calling getRefCount() too frequently
count = Lib.RefLib.getRefCount() # Don't do this in every message
```
### 7. Handle Edge Cases
```python
# ✅ CORRECT - Handle all scenarios
Lib.RefLib.track(
on_attracted=lambda ref: handle_referral(ref),
on_touch_own_link=lambda: Api.sendMessage("Can't refer yourself! 😊"),
on_already_attracted=lambda: Api.sendMessage("Welcome back! 👋")
)
# ❌ WRONG - Missing callbacks
Lib.RefLib.track(on_attracted=handle_referral) # What about self-referral?
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
Next bonus at: {next_milestone} referrals
Start earning! 🚀
"""
# ❌ WRONG - Unclear or unmotivating
Api.sendMessage(f"Link: {link}") # Too minimal
```
***
## Common Patterns
### Pattern 1: Basic Referral Bot
```python
# Minimal viable referral system
# Command: start
def handle_referral(ref):
User.res("points").add(100)
User.resOf("points", ref['id']).add(50)
Api.sendMessage("Welcome! +100 points")
Api.sendMessage(chat_id=ref['id'], text="New referral! +50 points")
Lib.RefLib.track(on_attracted=handle_referral)
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
my_rank = Lib.RefLib.getRank()
message = "🏆 Leaderboard:\n\n"
for i, (uid, count) in enumerate(top.items(), 1):
marker = "👉" if uid == str(u) else ""
message += f"{marker}{i}. User {uid}: {count}\n"
message += f"\n📍 Your rank: #{my_rank}"
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
Bot.storeData("contest_end", Lib.DateTime.time() + (7*24*60*60))
# Users check status
time_left = Bot.fetchData("contest_end") - Lib.DateTime.time()
days = int(time_left / 86400)
top3 = Lib.RefLib.getTopList(limit=3)
Api.sendMessage(f"Contest ends in {days} days!\n\nLeaders:\n{format_top3(top3)}")
```
***
## Troubleshooting
### Issue: Referrals Not Being Tracked
**Problem:** New users clicking referral links but not being tracked.
**Solution:**
* Ensure `track()` is called in `/start` command (not other commands)
* Check that callbacks are properly defined
* Verify users are actually using /start (not just opening the bot)
```python
# ✅ Correct placement
# Command: start
Lib.RefLib.track(on_attracted=handle_referral)
# ❌ Wrong placement
# Command: referral
Lib.RefLib.track(on_attracted=handle_referral) # Won't work!
```
### Issue: Self-Referral Not Blocked
**Problem:** Users able to refer themselves.
**Solution:**
* Always provide `on_touch_own_link` callback:
```python
Lib.RefLib.track(
on_attracted=handle_referral,
on_touch_own_link=lambda: Api.sendMessage("Can't refer yourself!"), # Important!
on_already_attracted=lambda: Api.sendMessage("Welcome back!")
)
```
### Issue: Referral Count Seems Wrong
**Problem:** `getRefCount()` returns unexpected numbers.
**Solution:**
* Check if you're passing correct `user_id` parameter
* Verify you're not accidentally clearing data
* Remember it only counts successful referrals (tracked via `track()`)
```python
# Get current user's count
my_count = Lib.RefLib.getRefCount()
# Get specific user's count
their_count = Lib.RefLib.getRefCount(user_id="123456789")
```
### Issue: Leaderboard Empty
**Problem:** `getTopList()` returns empty dict.
**Solution:**
* Ensure `track()` has been set up and users have been referred
* Check that you're using `track()` in /start command
* Verify referrals are actually happening
### Issue: Campaign Prefix Not Working
**Problem:** Prefix not being detected in referrer\_info.
**Solution:**
* Ensure you're generating links with prefix:
```python
# ✅ Correct
link = Lib.RefLib.getLink(prefix="youtube")
# Then access in callback:
def handle_referral(referrer_info):
prefix = referrer_info.get('prefix') # Will be "youtube"
```
### Issue: Stats Showing 0 for Recent Periods
**Problem:** `getStats()` shows 0 for recent\_7d or recent\_30d.
**Solution:**
* Check that you have actual referrals in those time periods
* Verify your system time/timezone is correct
* Remember stats are based on referral dates, not current activity
***
## Summary
`Lib.RefLib` provides everything you need for a complete referral system:
✅ **Easy Setup** - Just add `track()` to your /start command
✅ **Automatic Tracking** - No manual referral detection needed
✅ **Complete Analytics** - Counts, ranks, stats, and leaderboards
✅ **Flexible Rewards** - Custom callbacks for any reward system
✅ **Campaign Tracking** - Monitor performance of different channels
✅ **Anti-Fraud** - Built-in self-referral prevention
Start building your viral bot today with `Lib.RefLib`! 🚀
***
*For more information, visit* [*TeleBotStudio.com*](https://TeleBotStudio.com)
