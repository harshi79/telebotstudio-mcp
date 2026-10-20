# Implementation Patterns

Verified-structure, copy-paste-ready TeleBot Studio implementation patterns organized into 7 domain categories.

Each pattern is a self-contained Markdown file with complete runnable TBS code, step-by-step execution flows, API references, and pitfall guides. Every pattern follows the standard structure defined in [TEMPLATE.md](TEMPLATE.md).

## Categories

| Category | Patterns | Description |
|:---|:---:|:---|
| [ui](ui/) | 3 | User-facing interactions — multi-level menus, form wizards, paginated lists |
| [admin](admin/) | 1 | Bot owner tools — dashboards, subscriber tracking, broadcast & maintenance lock |
| [systems](systems/) | 1 | Core infrastructure — TTL state machines, rate throttling, `StopExecution`-safe error guards |
| [commerce](commerce/) | 1 | Monetization & growth — deep-link referral tracking and reward balances |
| [storage](storage/) | 1 | Data persistence — per-user CRUD profiles, partial edits, delete confirmation |
| [integrations](integrations/) | 1 | External services — HMAC-verified webhooks, `Bot.setWebhookResponse`, async `fallback_command` |
| [utilities](utilities/) | 1 | Reusable helpers — dynamic inline button rows, quick-add & conversational checklists |

## Pattern Catalog (9 Patterns)

| Category | Pattern | Commands | Summary |
|:---|:---|:---|:---|
| **UI** | [Inline Keyboard Navigation System](ui/inline-keyboard-navigation.md) | `/menu`, `/handler_callback_query` | Multi-level nested inline menus with history stack, home/back buttons, and `nav_`/`sys_`/`act_` dispatch |
| **UI** | [Multi-Step Form Wizard](ui/multi-step-form-wizard.md) | `/form`, `*`, `/handler_callback_query` | 3-step input wizard with `/cancel` abort and summary Confirm/Cancel buttons |
| **UI** | [Paginated List with Next/Prev Navigation](ui/paginated-list.md) | `/list`, `/handler_callback_query` | Smooth `editMessageText` list pagination with page indicator and bounds protection |
| **Admin** | [Admin Dashboard with Broadcast & Maintenance Mode](admin/admin-dashboard-broadcast.md) | `/admin`, `/start`, `*`, `/handler_callback_query` | Owner-only control panel with subscriber stats, media-preserving forward broadcast, and maintenance lock |
| **Systems** | [Conversation State Machine with TTL & Rate Guard](systems/conversation-state-machine-guard.md) | `/ticket`, `/cancel`, `*`, `/handler_callback_query` | Structured session state with inactivity timeout, per-user cooldown guard, and `Bot.errorID()` error boundary |
| **Commerce** | [Referral & Reward System](commerce/referral-reward-system.md) | `/start`, `/referral`, `/handler_callback_query` | Deep-link refer-to-earn flow with self-referral and duplicate-registration fraud protection |
| **Storage** | [User Profile Storage with Edit & Delete](storage/user-profile-storage.md) | `/profile`, `/profile set`, `/profile clear`, `*`, `/handler_callback_query` | Complete per-user CRUD profile flow with field-level edits and two-step delete confirmation |
| **Integrations** | [Verified External Webhook Receiver & Async API Callback](integrations/webhook-hmac-sync-response.md) | `/webhook_payment`, `/trigger_report`, `/handle_report_result` | HMAC-SHA256 webhook verification, idempotency, `Bot.setWebhookResponse`, and long-running `Request.post` via `fallback_command` |
| **Utilities** | [Todo Task Manager](utilities/todo-task-manager.md) | `/todo`, `*`, `/handler_callback_query` | Personal checklist with instant `/todo <task>`, conversational add, and dynamic 3-column button rows |

> *Total: **9 pattern implementations** across all **7 categories** (3 UI + 1 Admin + 1 Systems + 1 Commerce + 1 Storage + 1 Integrations + 1 Utilities).*

## Adding a New Pattern

1. Copy [TEMPLATE.md](TEMPLATE.md) into the appropriate category folder
2. Name the file in lowercase kebab-case (e.g. `inline-menu.md`)
3. Fill in every section completely — runnable code only, no placeholders
4. Set `verified: true` only after live testing on TeleBot Studio (record the bot/environment in `tested_with`)
5. Add the pattern to both the category `README.md` and the Pattern Catalog table above
6. Run `python build_index.py --validate` to confirm clean indexing with zero chunk warnings

## Naming Conventions

- Use lowercase with hyphens: `inline-keyboard-menu.md`, not `InlineKeyboardMenu.md`
- Match the primary feature the pattern demonstrates
- One pattern per file — split complex multi-domain workflows into composable patterns

## Documentation Standards

- Every pattern must use the [TEMPLATE.md](TEMPLATE.md) structure
- Code must be complete and runnable — no pseudocode, no `# your code here`
- The `verified` field must remain `false` until tested against the live TeleBot Studio runtime
- The `tested_with` field must identify the bot ID or environment used for verification
