# Admin Patterns

Bot owner and operator tools — patterns for managing bots, users, and content at scale.

## What Belongs Here

- Admin dashboards and control panels
- User management (ban, mute, whitelist)
- Broadcast and announcement systems
- Usage analytics and statistics
- Content management and scheduling
- Role-based access control
- Log viewers and debug tools
- Backup and restore workflows

## What Does NOT Belong Here

- Broadcast message formatting → [ui](../ui/) (if it's about the keyboard/UI)
- Storing admin configuration → [storage](../storage/)
- Webhook-based analytics → [integrations](../integrations/)

## Naming Conventions

- `admin-<feature>.md` — general admin patterns
- `broadcast-<feature>.md` — broadcast-specific patterns
- `analytics-<feature>.md` — stats and reporting patterns
- `rbac-<feature>.md` — role-based access patterns
- `moderation-<feature>.md` — user moderation patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For admin patterns specifically:

- **Commands**: list every `/command` the pattern exposes — distinguish owner commands from user-facing ones
- **Callback Handlers**: list inline button handlers used in the admin interface
- **Security**: explicitly note how the pattern restricts access to authorized users
- Include the authorization check code separately so it can be reused

## How to Write an Admin Pattern

1. Define who has access (owner only, specific user IDs, role check)
2. List the admin actions the pattern supports
3. Write the complete TBS code including the access guard
4. Show the execution flow for both authorized and unauthorized access
5. Note the impact on bot performance when used at scale
