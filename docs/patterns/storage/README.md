# Storage Patterns

Data persistence and retrieval — patterns for storing, caching, and managing bot and user data.

## What Belongs Here

- Database operations (create, read, update, delete)
- Caching strategies (read-through, write-through, TTL)
- File upload and download handling
- User profile and preference storage
- Configuration management
- Data migration and schema versioning
- Queue and job storage
- Key-value and document storage patterns

## What Does NOT Belong Here

- UI for browsing data → [ui](../ui/)
- External database APIs → [integrations](../integrations/)
- State machine logic → [systems](../systems/)

## Naming Conventions

- `database-<feature>.md` — database operation patterns
- `cache-<feature>.md` — caching patterns
- `user-store-<feature>.md` — user data patterns
- `file-<feature>.md` — file handling patterns
- `config-<feature>.md` — configuration patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For storage patterns specifically:

- **Commands**: list every command that reads or writes data
- **APIs Used**: specify which TeleBot Studio storage API or external database is used
- Document the data schema — what fields exist and their types
- Include read and write patterns separately when the logic differs

## How to Write a Storage Pattern

1. Define the data model — what is being stored and why
2. Show the schema or data structure
3. Write the complete TBS code for create, read, update, and delete operations
4. Trace the execution flow for each operation
5. Note concurrency, consistency, and performance implications
