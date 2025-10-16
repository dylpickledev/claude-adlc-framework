---
description: Manage guest mode sessions for testing da-agent-hub with guest repositories
---

# Guest Mode Management

Manage isolated guest sessions for testing da-agent-hub.

## Available Actions

### Start New Session
```bash
./scripts/guest-mode.sh start <session-name>
```

### List Active Sessions
```bash
./scripts/guest-mode.sh list
```

### Stop Session
```bash
./scripts/guest-mode.sh stop <session-name>
```

### Cleanup All Sessions
```bash
./scripts/guest-mode.sh cleanup
```

## Quick Reference

**Guest mode creates isolated sessions where testers can:**
- Use their own GitHub authentication
- Work with their own repositories
- Use your Claude Code installation and API credits
- Test da-agent-hub workflows safely

**What gets isolated:**
- GitHub CLI authentication (guest's account)
- Git configuration (guest's name/email)
- Repository clones (guest's repos)
- Working directory (all work in .guest-sessions/)

**What gets shared:**
- Claude Code installation (your CLI)
- Anthropic API credits (your account)
- da-agent-hub scripts and agents
- MCP server configurations

## Documentation

- Full guide: [GUEST_MODE.md](../../GUEST_MODE.md)
- Quick start for guests: [GUEST_QUICKSTART.md](../../GUEST_QUICKSTART.md)
- Main README: [README.md](../../README.md)

## Example Workflow

```bash
# 1. Host creates session
./scripts/guest-mode.sh start workshop-2024

# 2. Guest activates
source .guest-sessions/workshop-2024/activate.sh

# 3. Guest authenticates
gh auth login

# 4. Guest uses da-agent-hub
claude /capture "Test with my repos"

# 5. Guest deactivates
source .guest-sessions/workshop-2024/deactivate.sh

# 6. Host cleans up
./scripts/guest-mode.sh stop workshop-2024
```

## Use Cases

- **Workshops/Training** - Multiple sequential users on same laptop
- **Evaluation** - Let prospects test with their actual data stack
- **Pair Programming** - Collaborate with different GitHub contexts
- **Demos** - Show da-agent-hub hands-on safely

---

What would you like to do with guest mode?
