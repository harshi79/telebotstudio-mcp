# Implementation Patterns

Verified, copy-paste-ready TeleBot Studio implementation patterns organized by category.

Each pattern is a self-contained Markdown file with complete working code, execution flow, and usage notes. Patterns use the standard template defined in [TEMPLATE.md](TEMPLATE.md).

## Categories

| Category | Description |
|:---|:---|
| [ui](ui/) | User-facing interactions — menus, keyboards, inline buttons, navigation flows |
| [admin](admin/) | Bot owner tools — dashboards, user management, analytics, broadcasting |
| [systems](systems/) | Core bot infrastructure — middleware, state machines, error handling, session management |
| [commerce](commerce/) | Payments, subscriptions, referrals, credits, storefronts |
| [storage](storage/) | Data persistence — databases, caching, file handling, user data |
| [integrations](integrations/) | External services — APIs, webhooks, third-party platforms |
| [utilities](utilities/) | Reusable helpers — formatters, validators, converters, text processing |

## Adding a New Pattern

1. Copy [TEMPLATE.md](TEMPLATE.md) into the correct category folder
2. Rename the file to match the pattern name (e.g. `inline-menu.md`)
3. Fill in every section — incomplete patterns will not be accepted
4. Set `verified: true` only after testing against the live API
5. Add the pattern filename to this index table under its category

## Naming Conventions

- Use lowercase with hyphens: `inline-keyboard-menu.md`, not `InlineKeyboardMenu.md`
- Match the primary feature the pattern demonstrates
- One pattern per file — split complex patterns into composable parts

## Documentation Standards

- Every pattern must use the [TEMPLATE.md](TEMPLATE.md) structure
- Code must be complete and runnable — no pseudocode, no `// your code here`
- The `verified` field must be `false` until tested against the live TeleBot Studio API
- The `tested_with` field must name the bot ID or environment used for verification
