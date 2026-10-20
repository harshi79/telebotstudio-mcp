# TeleBot Studio — Complete Documentation Index

Complete offline index of official TeleBot Studio reference documentation and verified implementation patterns bundled in this MCP server.

## Official Platform & Language Reference

- **Introduction to TeleBot Studio** (`introduction-to-telebot-studio.md`) — Platform overview, core objects (`Api`, `Bot`, `User`, `Account`, `Admin`, `Lib`, `Request`), and built-in library ecosystem
- **Getting Started with TeleBot Studio** (`getting-started.md`) — Account creation, @BotFather setup, first commands, testing, and bot launch
- **Commands in TBS** (`commands-in-tbs.md`) — Slash commands, wildcard `*` handlers, `/handler_callback_query`, deep links (`params`), chaining (`Bot.run`), and waiting for input
- **TBS Language Reference** (`tbs-language-reference.md`) — Full syntax reference for `Api`, `Bot`, `User`, `Account`, `Admin`, `Request`, global variables, exceptions (`StopExecution`), and sandbox rules
- **Bot Features and Functionalities** (`bot-features-and-functionalities.md`) — Keyboards, resources, membership verification, state flows, bot transfers, and error IDs
- **Advanced Features** (`advanced-features.md`) — Environment variables, scheduling (`Bot.scheduleCommand`), multi-bot orchestration, webhooks, and external integrations
- **Broadcast Function** (`broadcast-function.md`) — High-volume subscriber broadcasting, pause/resume/status tracking, rate safety, and error handling
- **Real-World Examples and Use Cases** (`real-world.md`) — End-to-end bot examples for referrals, storefronts, support desks, and automation
- **Tips, Best Practices, and Troubleshooting** (`tips-best-practices-and-troubleshooting.md`) — Debugging techniques, performance optimization, security guards, and common pitfalls
- **Frequently Asked Questions (FAQ)** (`faq.md`) — Platform limits, storage behavior, webhooks, libraries, and operational answers
- **Glossary and Key Concepts** (`glossary-and-key-concepts.md`) — Definitions of TBS objects, execution model, resources, webhooks, and platform terms
- **Conclusion and Next Steps** (`conclusion-and-next-steps.md`) — Architecture checklist, scaling tips, and next steps

## Built-in Libraries & v1.1.0 Reference

- **TeleBot Studio v1.1.0 Release Notes** (`telebot-studio-v1.1.0-media-libraries-gifts-webhooks-and-more.md`) — Complete changelog for Platform v1.1.0 / Telegram Bot API 10.1 (`Lib.PIL`, `Lib.CV`, `Lib.Security`, `Lib.TeleGifts`, expanded `Lib.Random`, `Lib.EVM` balances, `Lib.TON` helpers, `Bot.setWebhookResponse`, `fallback_command`, `options.headers` / `options.ip`)
- **TBS Libraries Reference** (`tbs-libraries.md`) — Complete reference for `Lib.Security`, `Lib.TeleGifts`, `Lib.Random`, `Lib.DateTime`, `Lib.CSV`, payment libraries, and AI helpers
- **TBS Libraries v1.1.0 Pointer** (`tbs-libraries-updated.md`) — Quick index of library additions introduced in v1.1.0
- **TBS Media Libraries (`Lib.PIL` & `Lib.CV`)** (`tbs-media-libraries-pil-and-cv-documentation.md`) — In-memory Pillow image manipulation and OpenCV computer vision / face detection
- **EVM Library Documentation (`Lib.EVM`)** (`evm-library-documentation.md`) — Wallet generation, native/ERC-20 balance lookups (`fetchBalance`, `fetchTokenBalance`), and transactions across EVM chains
- **TON Library Documentation (`Lib.TON`)** (`ton-library-documentation.md`) — TON wallets, Jetton wallet resolution (`get_jetton_wallet_address`), TON Connect (`register_ton_connect_wallet`), and transfers
- **RefLib Complete Documentation** (`reflib_complete_documentation.md`) — Built-in multi-feature referral tracking and reward library reference
- **TeleBot Studio REST API v2 Documentation** (`readme.md`) — Complete REST API v2 reference for external bot, command, and lifecycle automation (`https://api.telebotstudio.com/v2`)

## Implementation Patterns Knowledge Base (`patterns/`)

- **Pattern Standards & Index** (`patterns/README.md`, `patterns/TEMPLATE.md`)
- **UI Patterns** (`patterns/ui/README.md`):
  - `patterns/ui/inline-keyboard-navigation.md` — Multi-level inline menu navigation with history stack, home/back buttons, and `nav_`/`sys_`/`act_` dispatch
  - `patterns/ui/multi-step-form-wizard.md` — Step-by-step form input wizard with summary review and Confirm/Cancel buttons
  - `patterns/ui/paginated-list.md` — In-place `editMessageText` pagination with boundary clamping and page indicator
- **Admin Patterns** (`patterns/admin/README.md`):
  - `patterns/admin/admin-dashboard-broadcast.md` — Owner-only admin panel with subscriber tracking, media-preserving forward broadcast, and maintenance lock
- **Systems Patterns** (`patterns/systems/README.md`):
  - `patterns/systems/conversation-state-machine-guard.md` — Centralized conversation state machine with TTL expiry, global command escape hatch, and per-user rate throttling
- **Commerce Patterns** (`patterns/commerce/README.md`):
  - `patterns/commerce/referral-reward-system.md` — Deep-link refer-to-earn system with self-referral and replay fraud prevention
- **Storage Patterns** (`patterns/storage/README.md`):
  - `patterns/storage/user-profile-storage.md` — Per-user CRUD profile manager with individual field editing and two-step delete confirmation
- **Integration Patterns** (`patterns/integrations/README.md`):
  - `patterns/integrations/webhook-hmac-sync-response.md` — Verified external webhook handler using `Lib.Security.verifyHMAC`, `options.headers`/`options.ip`, `Bot.setWebhookResponse`, and async `fallback_command`
- **Utility Patterns** (`patterns/utilities/README.md`):
  - `patterns/utilities/todo-task-manager.md` — Personal checklist manager demonstrating quick-add, conversational add, and dynamic button rows

## MCP Retrieval Guidance

- Use `search_docs(query)` for general concepts and exact method/parameter names.
- Use `search_examples(query)`, `search_api(query)`, `search_library(query)`, `search_functions(query)`, or `search_errors(query)` for scoped retrieval.
- Use `get_page(name)` to load any full page above by filename or relative path (for example `get_page("tbs-libraries.md")` or `get_page("patterns/integrations/webhook-hmac-sync-response.md")`).
