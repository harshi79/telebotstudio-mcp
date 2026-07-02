# Utility Patterns

Reusable helper patterns — small, composable pieces that other patterns depend on.

## What Belongs Here

- Text formatters (Markdown, HTML, message templates)
- Input validators (email, phone, URL, custom formats)
- Data converters (units, currencies, timezones, encodings)
- Text processing (truncation, escaping, sanitization)
- Message builders (response composers, template engines)
- Calculation helpers (pricing, distances, durations)
- ID and token generators
- Date and time utilities

## What Does NOT Belong Here

- Complete bot features → belongs in a domain-specific category
- Data storage operations → [storage](../storage/)
- External API calls → [integrations](../integrations/)

## Naming Conventions

- `formatter-<feature>.md` — text formatting patterns
- `validator-<feature>.md` — input validation patterns
- `converter-<feature>.md` — data conversion patterns
- `builder-<feature>.md` — message composition patterns
- `calculator-<feature>.md` — computation patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For utility patterns specifically:

- **Commands**: may be minimal or none — utilities are often called by other patterns, not directly by users
- Focus on the function signature: what goes in, what comes out
- Document edge cases and invalid inputs explicitly
- Keep the code short and focused — utilities should do one thing well

## How to Write a Utility Pattern

1. Define the single responsibility the utility fulfills
2. List the inputs and expected outputs with examples
3. Write the complete TBS code — keep it minimal and focused
4. Show 2-3 usage examples inside other patterns
5. Note any limitations or inputs that are not handled
