# UI Patterns

User-facing interaction patterns — how bots present information and collect input from users.

## What Belongs Here

- Inline keyboard menus and navigation
- Reply keyboard layouts
- Multi-step conversation flows (wizards)
- Paginated lists and carousels
- Confirmation dialogs
- Form input collection
- Media galleries and file pickers
- Language and settings selectors

## What Does NOT Belong Here

- Payment or checkout flows → [commerce](../commerce/)
- Data storage for user choices → [storage](../storage/)
- External API rendering → [integrations](../integrations/)

## Naming Conventions

- `inline-keyboard-<feature>.md` — inline button patterns
- `reply-keyboard-<feature>.md` — reply keyboard patterns
- `wizard-<feature>.md` — multi-step conversation patterns
- `paginator-<feature>.md` — pagination patterns
- `selector-<feature>.md` — option selection patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For UI patterns specifically:

- **Commands**: list every `/command` and `*` handler the pattern uses
- **Callback Handlers**: list every `callback_query` handler — this is critical for inline keyboard patterns
- **Execution Flow**: show the button press → callback → response sequence explicitly
- Include the exact keyboard layout using a table or ASCII diagram

## How to Write a UI Pattern

1. Start from the user's perspective — what do they see and press?
2. Define every command and callback handler the pattern needs
3. Write the complete TBS code in a single copy-paste block
4. Trace the execution flow step by step
5. Note any edge cases (empty results, back navigation, cancel behavior)
