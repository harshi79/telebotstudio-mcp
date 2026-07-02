# Commerce Patterns

Monetization and transaction patterns — payments, subscriptions, and virtual economies.

## What Belongs Here

- Payment processing (Telegram Stars, external gateways)
- Subscription management (trial, recurring, expiry)
- Referral and invite reward systems
- Credit and token systems
- Storefronts and product catalogs
- Invoice generation and receipt handling
- Promo codes and discounts
- Wallet and balance tracking

## What Does NOT Belong Here

- Store UI/keyboard layout → [ui](../ui/)
- Storing transaction records → [storage](../storage/)
- Payment gateway API calls → [integrations](../integrations/)

## Naming Conventions

- `payment-<feature>.md` — payment processing patterns
- `subscription-<feature>.md` — subscription lifecycle patterns
- `referral-<feature>.md` — referral system patterns
- `credits-<feature>.md` — virtual currency patterns
- `store-<feature>.md` — storefront patterns
- `promo-<feature>.md` — discount and promo code patterns

## Documentation Standards

Follow the standard [TEMPLATE.md](../TEMPLATE.md). For commerce patterns specifically:

- **Commands**: list every `/command` the pattern exposes to users
- **Callback Handlers**: list inline button handlers for purchase flows
- **Security**: note how the pattern prevents replay attacks, duplicate charges, and balance manipulation
- Include the exact payment lifecycle (invoice → pre_checkout → successful_payment)

## How to Write a Commerce Pattern

1. Define the transaction model — what is being bought or exchanged
2. List every step in the payment or transaction flow
3. Write the complete TBS code including error recovery
4. Show the execution flow for success, failure, and cancellation
5. Note how the pattern handles edge cases (insufficient funds, expired subscription, duplicate requests)
