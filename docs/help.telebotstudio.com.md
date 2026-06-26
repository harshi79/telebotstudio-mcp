Introduction to TeleBot Studio | TeleBot Studio - Help

GitBook Assistant

GitBook Assistant

arrow-up-right-and-arrow-down-left-from-center

GitBook Assistant

##### Good night

I'm here to help you with the docs.

What is this page about?What should I read next?Can you give an example?

`⌘Ctrl``i`

AI Based on your context

Send

[![](https://help.telebotstudio.com/~gitbook/image?url=https%3A%2F%2F3958141917-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252FG25B4fvavGSapLB80aPp%252Fsites%252Fsite_ic6Nu%252Ficon%252FEIUpdMRNoLFZdCJZCIKg%252F20251203_130310.png%3Falt%3Dmedia%26token%3De6c2d773-eef2-4f4a-9479-2cb1fe6da6a9&width=32&dpr=3&quality=100&sign=d277b6e9&sv=2)![](https://help.telebotstudio.com/~gitbook/image?url=https%3A%2F%2F3958141917-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252FG25B4fvavGSapLB80aPp%252Fsites%252Fsite_ic6Nu%252Ficon%252FEIUpdMRNoLFZdCJZCIKg%252F20251203_130310.png%3Falt%3Dmedia%26token%3De6c2d773-eef2-4f4a-9479-2cb1fe6da6a9&width=32&dpr=3&quality=100&sign=d277b6e9&sv=2)

TeleBot Studio - Help](/)

* [Introduction to TeleBot Studio](/)
* [Getting Started with TeleBot Studio](/getting-started)
* [Commands in TBS](/commands-in-tbs)
* [TBS Language Reference](/tbs-language-reference)
* [TBS Libraries Reference](/tbs-libraries)
* [Bot Features and Functionalities](/bot-features-and-functionalities)
* [Advanced Features](/advanced-features)
* [Real-World Examples and Use Cases](/real-world)
* [Tips, Best Practices, and Troubleshooting](/tips-best-practices-and-troubleshooting)
* [Frequently Asked Questions (FAQ)](/faq)
* [Glossary and Key Concepts](/glossary-and-key-concepts)
* [Broadcast Function](/broadcast-function)
* [TON Library Documentation](/ton-library-documentation)
* [Conclusion and Next Steps](/conclusion-and-next-steps)
* [EVM Library Documentation](/evm-library-documentation)
* [RefLib Library Documentation](/reflib_complete_documentation)
* [TeleBot Studio API v2 Documentation](/readme)

[Powered by GitBook](https://www.gitbook.com/?utm_source=content&utm_medium=trademark&utm_campaign=X8zOoKeThwFpUgv8acrb&utm_content=site_ic6Nu)

On this page

For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). This page is also available as [Markdown](https://help.telebotstudio.com/introduction-to-telebot-studio.md).

### Welcome to TeleBot Studio (TBS)

TeleBot Studio (TBS) is an innovative platform designed to make building, managing, and hosting Telegram bots simple and accessible. With its powerful custom programming language called **TeleBot Syntax (TBS)** and an intuitive interface, the platform enables both beginners and experienced developers to create highly customizable bots tailored to their unique requirements. Whether you're building bots for business automation, community engagement, or personal projects, TeleBot Studio provides the flexibility and performance you need.

### What is TeleBot Studio?

TeleBot Studio is a comprehensive Telegram bot development platform that empowers users to create and host bots with ease. Using its custom programming language, **TeleBot Syntax (TBS)**, along with a user-friendly dashboard, TBS allows you to:

* Build bots with sophisticated features and functionality
* Manage multiple bots through a streamlined interface
* Host bots reliably with built-in infrastructure
* Access a wide range of pre-built libraries for payments, blockchain, data management, and more

**Platform Highlights**

* **Zero Cost**: Completely free platform with no usage limits or hidden fees
* **Custom Language**: Purpose-built TBS syntax optimized for Telegram bot development
* **Enterprise Ready**: Suitable for both hobby projects and production-grade applications
* **Global Access**: Available worldwide at [TeleBotStudio.com](https://TeleBotStudio.com)

### Getting Started with TeleBot Studio

Building your first bot on TBS is straightforward and takes just a few minutes:

1. **Create Your Account**: Sign up with your email and password at [TeleBotStudio.com](https://TeleBotStudio.com)
2. **Obtain a Bot Token**: Get your Telegram Bot API token from @BotFather on Telegram
3. **Add Your Bot**: Enter the API token in the TBS dashboard to register your bot
4. **Write Commands**: Define bot commands using TBS to make your bot interactive
5. **Launch**: Activate your bot and start serving users immediately

For assistance and community support, join our help group: <https://t.me/TeleBotStudioChat>

### Understanding Commands and TBS

#### Commands

Commands are the fundamental building blocks of every bot created on TeleBot Studio. A command is triggered when users send specific keywords or messages to your bot (such as `/start` or `/help`). Each command defines how your bot responds and behaves in different situations. Commands must be written using **TeleBot Syntax (TBS)**.

Example of a simple command:

Commands enable you to:

* Respond intelligently to user inputs
* Send messages, photos, documents, and other media
* Interact with external APIs and services
* Manage user data and bot state
* Create complex workflows and automations

#### TeleBot Syntax (TBS)

TeleBot Syntax (TBS) is a Python-based custom language developed specifically for TeleBot Studio. It provides a comprehensive set of built-in tools, libraries, and predefined objects to streamline bot development without requiring imports.

Key features of TBS:

* **No Imports Required**: All functionality is available globally without import statements
* **Built-in Libraries**: Integrated support for payments (Coinbase, Paytm), blockchain operations (EVM, TON), HTTP requests, data storage, and more
* **Secure Environment**: Restricted execution context ensures safe code execution
* **Simple Syntax**: Easy-to-learn commands that make bot development accessible to everyone
* **Pre-defined Objects**: Access to `Api`, `Bot`, `User`, `Account`, `Admin`, `Lib`, and `Request` objects
* **Command Management**: Advanced features like `Bot.run()`, `Bot.scheduleCommand()`, and `Bot.waitForInput()` for creating complex interactions

**Example using TBS:**

### Core Objects in TBS

TeleBot Syntax provides several built-in objects for different purposes:

#### Api Object

The `Api` object provides direct access to all Telegram Bot API methods. Use this for sending messages, media, and managing chat interactions.

#### Bot Object

The `Bot` object handles platform-specific operations like command routing, data management, and bot control.

#### User Object

The `User` object manages user-specific data and resources.

#### Account Object

The `Account` object handles account-level data accessible across all your bots.

#### Admin Object

The `Admin` object provides administrative control over bot resources.

#### Lib Object

The `Lib` object gives access to all built-in libraries for payments, blockchain, data management, and more.

### Key Features of TeleBot Studio

1. **Blazing Fast Performance**: TBS is optimized for speed, ensuring your bots respond instantly to user requests
2. **Complete Customization**: TeleBot Syntax allows you to customize every aspect of your bot's functionality and create unique features
3. **Free Forever**: Completely free platform with no hidden costs, usage limits, or subscription fees
4. **Universal Bot Support**: Build any type of bot you can imagine - from simple chatbots to complex automation systems, payment processors, and blockchain integrations
5. **Reliable Hosting**: Your bots are hosted on robust infrastructure, eliminating server management concerns
6. **Rich Library Ecosystem**: Pre-built libraries for:

   * Payment processing (Coinbase, Paytm)
   * Blockchain interactions (EVM networks, TON blockchain)
   * Data management (CSV, JSON)
   * HTTP requests and API integrations
   * Date and time operations
   * AI integrations (Gemini, OpenAI compatible)
   * And much more

### The Future of TeleBot Studio

TeleBot Studio is continuously evolving with regular updates and new features. The platform roadmap includes:

1. **Enhanced User Interface**: A redesigned dashboard for even better bot management experience
2. **Expanded Library Support**: Additional libraries and integrations based on community feedback
3. **Advanced Analytics**: Real-time monitoring and detailed insights into your bot's performance
4. **Community Features**: Bot templates, sharing, and collaboration tools

### Why Choose TeleBot Studio?

TeleBot Studio stands out among bot development platforms for several compelling reasons:

**Ease of Use**

* No complex server setup or deployment process
* Intuitive dashboard for managing all aspects of your bots
* Clear documentation and active community support
* Simple signup process with email and password only

**Cost-Effective**

* Completely free with no hidden charges
* No credit card required
* No usage caps or throttling
* No premium tiers or paid features

**Powerful Features**

* Full access to Telegram Bot API
* Extensive library ecosystem for common tasks
* Advanced command chaining and workflow management
* Real-time execution with minimal latency

**Secure and Reliable**

* Sandboxed execution environment for safe code running
* Reliable hosting infrastructure
* Regular platform updates and improvements
* Active error logging and debugging tools

### Join the TeleBot Studio Community

We have an active and helpful community ready to assist you:

* **Help Group**: Get support and share ideas at <https://t.me/TeleBotStudioChat>
* **Documentation**: Comprehensive guides and references for all features
* **Regular Updates**: Stay informed about new features and improvements

### Next Steps

Ready to get started? Here's what to do next:

1. **Sign Up**: Create your free account at [TeleBotStudio.com](https://TeleBotStudio.com)
2. **Explore Documentation**: Read the Getting Started guide to build your first bot
3. **Join Community**: Connect with other developers in our help group
4. **Start Building**: Create your first bot and bring your ideas to life

Welcome to TeleBot Studio - where bot development is simple, powerful, and free!

[NextGetting Started with TeleBot Studio](/getting-started)

Last updated 6 months ago

* [Welcome to TeleBot Studio (TBS)](#welcome-to-telebot-studio-tbs)
* [What is TeleBot Studio?](#what-is-telebot-studio)
* [Getting Started with TeleBot Studio](#getting-started-with-telebot-studio)
* [Understanding Commands and TBS](#understanding-commands-and-tbs)
* [Core Objects in TBS](#core-objects-in-tbs)
* [Key Features of TeleBot Studio](#key-features-of-telebot-studio)
* [The Future of TeleBot Studio](#the-future-of-telebot-studio)
* [Why Choose TeleBot Studio?](#why-choose-telebot-studio)
* [Join the TeleBot Studio Community](#join-the-telebot-studio-community)
* [Next Steps](#next-steps)

GitBook AssistantAskCopy

```
Api.sendMessage("Hello! Welcome to my bot.")
```

GitBook AssistantAskCopy

```
# Get user's first name
name = message.from_user.first_name

# Send personalized welcome message
Api.sendMessage(f"Welcome {name}! Thanks for using our bot.")

# Store user data
User.storeData("joined_date", Lib.DateTime.now())
```

GitBook AssistantAskCopy

```
# Send a message
Api.sendMessage("Hello World!")

# Send a photo
Api.sendPhoto("https://example.com/image.jpg", caption="Check this out!")

# Send document
Api.sendDocument("https://example.com/file.pdf")
```

GitBook AssistantAskCopy

```
# Run another command
Bot.run("help")

# Schedule a command for later
Bot.scheduleCommand(60, "reminder")

# Wait for user's next input
Bot.waitForInput("process_response")

# Store bot-wide data
Bot.storeData("total_users", 1000)

# Get bot information
bot_details = Bot.getInfo()
```

GitBook AssistantAskCopy

```
# Store user data
User.storeData("score", 100)

# Get user data
score = User.fetchData("score")

# Get user resources
points = User.res("points")
points.add(10)
```

GitBook AssistantAskCopy

```
# Store account-wide settings
Account.storeData("api_key", "your_key_here")

# Retrieve account data
api_key = Account.fetchData("api_key")
```

GitBook AssistantAskCopy

```
# Access admin resources
admin_res = Admin.res("user_count")

# Get resource value
total_users = admin_res.value()
```

GitBook AssistantAskCopy

```
# Access HTTP library
response = Request.get("https://api.example.com/data")

# Use DateTime library
current_time = Lib.DateTime.now()

# Work with CSV data
csv_table = Lib.CSV.Table("users.csv")
```