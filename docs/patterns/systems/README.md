# Systems Patterns

Core bot infrastructure — patterns for bot internals, state management, and cross-cutting concerns.

## What Belongs Here

- State machines and conversation state tracking
- Error handling and fallback strategies
- Session and context management
- Middleware and request processing pipelines
- Rate limiting and throttling
- Message routing and dispatch
- Graceful degradation patterns
- Startup and initialization sequences

## What Does NOT Belong Here

- User-facing error messages → [ui](../ui/)
- Storing session data → [storage](../storage/)
- External service health checks → [integrations](../integrations/)

## Naming Conventions

- `state-machine-<feature>.md` — state tracking patterns
- `error-handler-<feature>.md` — error handling patterns
- `middleware-<feature>.md` — request processing patterns
- `rate-limiter-<feature>.md` — throttling patterns
- `router-<feature>.md` — message routing patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For systems patterns specifically:

- **Commands**: list every command that relies on the system behavior
- **Execution Flow**: show the internal processing sequence, not just the user-visible result
- Document the state transitions explicitly (before state → trigger → after state)
- Include failure scenarios and recovery paths

## How to Write a Systems Pattern

1. Define the problem the infrastructure solves
2. Show the data structures or state model the pattern uses
3. Write the complete TBS code
4. Trace the execution flow including error paths
5. Note thread safety, concurrency, and performance considerations
