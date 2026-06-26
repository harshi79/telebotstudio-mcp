> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/introduction-to-telebot-studio.md).
# Introduction to TeleBot Studio
### Welcome to TeleBot Studio (TBS)
TeleBot Studio (TBS) is an innovative platform designed to make building, managing, and hosting Telegram bots simple and accessible. With its powerful custom programming language called \*\*TeleBot Syntax (TBS)\*\* and an intuitive interface, the platform enables both beginners and experienced developers to create highly customizable bots tailored to their unique requirements. Whether you're building bots for business automation, community engagement, or personal projects, TeleBot Studio provides the flexibility and performance you need.
### What is TeleBot Studio?
TeleBot Studio is a comprehensive Telegram bot development platform that empowers users to create and host bots with ease. Using its custom programming language, \*\*TeleBot Syntax (TBS)\*\*, along with a user-friendly dashboard, TBS allows you to:
\* Build bots with sophisticated features and functionality
\* Manage multiple bots through a streamlined interface
\* Host bots reliably with built-in infrastructure
\* Access a wide range of pre-built libraries for payments, blockchain, data management, and more
\*\*Platform Highlights\*\*
\* \*\*Zero Cost\*\*: Completely free platform with no usage limits or hidden fees
\* \*\*Custom Language\*\*: Purpose-built TBS syntax optimized for Telegram bot development
\* \*\*Enterprise Ready\*\*: Suitable for both hobby projects and production-grade applications
\* \*\*Global Access\*\*: Available worldwide at [TeleBotStudio.com](https://TeleBotStudio.com)
### Getting Started with TeleBot Studio
Building your first bot on TBS is straightforward and takes just a few minutes:
1. \*\*Create Your Account\*\*: Sign up with your email and password at [TeleBotStudio.com](https://TeleBotStudio.com)
2. \*\*Obtain a Bot Token\*\*: Get your Telegram Bot API token from @BotFather on Telegram
3. \*\*Add Your Bot\*\*: Enter the API token in the TBS dashboard to register your bot
4. \*\*Write Commands\*\*: Define bot commands using TBS to make your bot interactive
5. \*\*Launch\*\*: Activate your bot and start serving users immediately
For assistance and community support, join our help group: 
### Understanding Commands and TBS
#### Commands
Commands are the fundamental building blocks of every bot created on TeleBot Studio. A command is triggered when users send specific keywords or messages to your bot (such as `/start` or `/help`). Each command defines how your bot responds and behaves in different situations. Commands must be written using \*\*TeleBot Syntax (TBS)\*\*.
Example of a simple command:
```python
Api.sendMessage("Hello! Welcome to my bot.")
```
Commands enable you to:
\* Respond intelligently to user inputs
\* Send messages, photos, documents, and other media
\* Interact with external APIs and services
\* Manage user data and bot state
\* Create complex workflows and automations
#### TeleBot Syntax (TBS)
TeleBot Syntax (TBS) is a Python-based custom language developed specifically for TeleBot Studio. It provides a comprehensive set of built-in tools, libraries, and predefined objects to streamline bot development without requiring imports.
Key features of TBS:
\* \*\*No Imports Required\*\*: All functionality is available globally without import statements
\* \*\*Built-in Libraries\*\*: Integrated support for payments (Coinbase, Paytm), blockchain operations (EVM, TON), HTTP requests, data storage, and more
\* \*\*Secure Environment\*\*: Restricted execution context ensures safe code execution
\* \*\*Simple Syntax\*\*: Easy-to-learn commands that make bot development accessible to everyone
\* \*\*Pre-defined Objects\*\*: Access to `Api`, `Bot`, `User`, `Account`, `Admin`, `Lib`, and `Request` objects
\* \*\*Command Management\*\*: Advanced features like `Bot.run()`, `Bot.scheduleCommand()`, and `Bot.waitForInput()` for creating complex interactions
\*\*Example using TBS:\*\*
```python
# Get user's first name
name = message.from\_user.first\_name
# Send personalized welcome message
Api.sendMessage(f"Welcome {name}! Thanks for using our bot.")
# Store user data
User.storeData("joined\_date", Lib.DateTime.now())
```
### Core Objects in TBS
TeleBot Syntax provides several built-in objects for different purposes:
#### Api Object
The `Api` object provides direct access to all Telegram Bot API methods. Use this for sending messages, media, and managing chat interactions.
```python
# Send a message
Api.sendMessage("Hello World!")
# Send a photo
Api.sendPhoto("https://example.com/image.jpg", caption="Check this out!")
# Send document
Api.sendDocument("https://example.com/file.pdf")
```
#### Bot Object
The `Bot` object handles platform-specific operations like command routing, data management, and bot control.
```python
# Run another command
Bot.run("help")
# Schedule a command for later
Bot.scheduleCommand(60, "reminder")
# Wait for user's next input
Bot.waitForInput("process\_response")
# Store bot-wide data
Bot.storeData("total\_users", 1000)
# Get bot information
bot\_details = Bot.getInfo()
```
#### User Object
The `User` object manages user-specific data and resources.
```python
# Store user data
User.storeData("score", 100)
# Get user data
score = User.fetchData("score")
# Get user resources
points = User.res("points")
points.add(10)
```
#### Account Object
The `Account` object handles account-level data accessible across all your bots.
```python
# Store account-wide settings
Account.storeData("api\_key", "your\_key\_here")
# Retrieve account data
api\_key = Account.fetchData("api\_key")
```
#### Admin Object
The `Admin` object provides administrative control over bot resources.
```python
# Access admin resources
admin\_res = Admin.res("user\_count")
# Get resource value
total\_users = admin\_res.value()
```
#### Lib Object
The `Lib` object gives access to all built-in libraries for payments, blockchain, data management, and more.
```python
# Access HTTP library
response = Request.get("https://api.example.com/data")
# Use DateTime library
current\_time = Lib.DateTime.now()
# Work with CSV data
csv\_table = Lib.CSV.Table("users.csv")
```
### Key Features of TeleBot Studio
1. \*\*Blazing Fast Performance\*\*: TBS is optimized for speed, ensuring your bots respond instantly to user requests
2. \*\*Complete Customization\*\*: TeleBot Syntax allows you to customize every aspect of your bot's functionality and create unique features
3. \*\*Free Forever\*\*: Completely free platform with no hidden costs, usage limits, or subscription fees
4. \*\*Universal Bot Support\*\*: Build any type of bot you can imagine - from simple chatbots to complex automation systems, payment processors, and blockchain integrations
5. \*\*Reliable Hosting\*\*: Your bots are hosted on robust infrastructure, eliminating server management concerns
6. \*\*Rich Library Ecosystem\*\*: Pre-built libraries for:
\* Payment processing (Coinbase, Paytm)
\* Blockchain interactions (EVM networks, TON blockchain)
\* Data management (CSV, JSON)
\* HTTP requests and API integrations
\* Date and time operations
\* AI integrations (Gemini, OpenAI compatible)
\* And much more
### The Future of TeleBot Studio
TeleBot Studio is continuously evolving with regular updates and new features. The platform roadmap includes:
1. \*\*Enhanced User Interface\*\*: A redesigned dashboard for even better bot management experience
2. \*\*Expanded Library Support\*\*: Additional libraries and integrations based on community feedback
3. \*\*Advanced Analytics\*\*: Real-time monitoring and detailed insights into your bot's performance
4. \*\*Community Features\*\*: Bot templates, sharing, and collaboration tools
### Why Choose TeleBot Studio?
TeleBot Studio stands out among bot development platforms for several compelling reasons:
\*\*Ease of Use\*\*
\* No complex server setup or deployment process
\* Intuitive dashboard for managing all aspects of your bots
\* Clear documentation and active community support
\* Simple signup process with email and password only
\*\*Cost-Effective\*\*
\* Completely free with no hidden charges
\* No credit card required
\* No usage caps or throttling
\* No premium tiers or paid features
\*\*Powerful Features\*\*
\* Full access to Telegram Bot API
\* Extensive library ecosystem for common tasks
\* Advanced command chaining and workflow management
\* Real-time execution with minimal latency
\*\*Secure and Reliable\*\*
\* Sandboxed execution environment for safe code running
\* Reliable hosting infrastructure
\* Regular platform updates and improvements
\* Active error logging and debugging tools
### Join the TeleBot Studio Community
We have an active and helpful community ready to assist you:
\* \*\*Help Group\*\*: Get support and share ideas at 
\* \*\*Documentation\*\*: Comprehensive guides and references for all features
\* \*\*Regular Updates\*\*: Stay informed about new features and improvements
### Next Steps
Ready to get started? Here's what to do next:
1. \*\*Sign Up\*\*: Create your free account at [TeleBotStudio.com](https://TeleBotStudio.com)
2. \*\*Explore Documentation\*\*: Read the Getting Started guide to build your first bot
3. \*\*Join Community\*\*: Connect with other developers in our help group
4. \*\*Start Building\*\*: Create your first bot and bring your ideas to life
Welcome to TeleBot Studio - where bot development is simple, powerful, and free!
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/introduction-to-telebot-studio.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.