# Integration Patterns

External service connections — patterns for communicating with APIs, webhooks, and third-party platforms.

## What Belongs Here

- REST API consumption patterns
- Webhook receiver and sender patterns
- OAuth and authentication flows with external services
- Third-party platform integrations (Notion, Google Sheets, Airtable, etc.)
- Message queue and event patterns
- HTTP request/response handling
- Rate limit compliance for external APIs
- Data transformation and mapping

## What Does NOT Belong Here

- Storing API keys → [storage](../storage/) (for persistence) or credential management (for session-scoped)
- UI for displaying external data → [ui](../ui/)
- Internal bot state → [systems](../systems/)

## Naming Conventions

- `api-<service>-<feature>.md` — REST API integration patterns
- `webhook-<service>-<feature>.md` — webhook patterns
- `oauth-<service>.md` — authentication flow patterns
- `sync-<service>-<feature>.md` — data synchronization patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For integration patterns specifically:

- **APIs Used**: list every external endpoint the pattern calls, with method and URL
- Document the expected request and response format for each external API
- Note authentication requirements and how credentials are managed
- Include rate limit handling and retry strategies

## How to Write an Integration Pattern

1. Define the external service and what data flows between it and the bot
2. Document the external API endpoints used (method, URL, request/response format)
3. Write the complete TBS code including error handling for external failures
4. Show the execution flow including the external API call sequence
5. Note rate limits, timeouts, and fallback behavior
