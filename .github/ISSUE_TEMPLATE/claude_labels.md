# Claude Interaction Labels

Use these labels to trigger Claude actions on issues:

## 🏷️ Available Labels

### `claude:fix`
- **Purpose**: Automatically create a PR to fix the issue
- **When to use**: When you want Claude to implement a suggested fix
- **Result**: Claude will analyze and create a pull request

### `claude:investigate`
- **Purpose**: Perform deeper investigation
- **When to use**: When you need more analysis or context
- **Result**: Claude will add detailed findings to the issue

### `claude:collaborate`
- **Purpose**: Start interactive collaboration mode
- **When to use**: For back-and-forth discussion about the issue
- **Result**: Claude will respond to comments and questions

## 💬 Comment Commands

You can also mention `@claude` in comments:

- `@claude create PR` - Create a pull request with the fix
- `@claude investigate the upstream data quality` - Specific investigation
- `@claude what do you think about this approach?` - General discussion

## 👤 Assignment

Assign the issue to `claude[bot]` for automatic fix attempts.