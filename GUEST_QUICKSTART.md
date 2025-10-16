# Guest Mode Quick Start

> 5-minute setup to test da-agent-hub with your own repositories

## Step 1: Activate Your Session (Host Does This)

The host will run:
```bash
./scripts/guest-mode.sh start <your-name>
```

## Step 2: Enter Guest Mode

```bash
source .guest-sessions/<your-name>/activate.sh
```

You'll see: `[GUEST: <your-name>]` in your terminal prompt

## Step 3: Authenticate with YOUR GitHub

```bash
# Login with your GitHub account
gh auth login

# Configure your git identity
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Step 4: Test da-agent-hub with Your Repos

### Capture an Idea
```bash
claude /capture "Build customer analytics dashboard"
# Creates GitHub issue in YOUR repository
```

### Research an Approach
```bash
claude /research 123  # Use YOUR issue number
# Specialist agents analyze YOUR project
```

### Start Development
```bash
claude /start 123
# Creates project structure for YOUR work
```

### Switch Context (if needed)
```bash
claude /switch
# Save work and switch branches
```

### Complete Project
```bash
claude /complete feature-customer-analytics
# Archives project, closes YOUR GitHub issue
```

## Step 5: Exit Guest Mode

```bash
source .guest-sessions/<your-name>/deactivate.sh
```

## What You're Testing

- ✅ **Your GitHub repos** - All work uses your repositories
- ✅ **Your git identity** - Commits show your name/email
- ✅ **Full da-agent-hub** - All commands and agents available
- ✅ **MCP integration** - Real-time data access (if configured)
- ✅ **Specialist agents** - Role-based and tool-specific experts

## What You're Using from Host

- ✅ **Claude Code CLI** - Installed and configured
- ✅ **API credits** - Host's Anthropic account
- ✅ **Agent definitions** - Pre-configured role and specialist agents
- ✅ **Scripts** - All da-agent-hub commands

## Common Commands

| Command | Purpose |
|---------|---------|
| `/capture "idea"` | Create GitHub issue in your repo |
| `/research <issue#>` | Deep analysis with specialist agents |
| `/start <issue#>` | Begin development from issue |
| `/switch` | Save work and switch branches |
| `/complete <project>` | Finish and archive project |

## Need Help?

- Full docs: [GUEST_MODE.md](GUEST_MODE.md)
- da-agent-hub guide: [README.md](README.md)
- Workflow details: [CLAUDE.md](CLAUDE.md)

## After Testing

When you're done:
```bash
# Exit guest mode
source .guest-sessions/<your-name>/deactivate.sh

# Let the host know you're finished
# They'll run: ./scripts/guest-mode.sh stop <your-name>
```

---

**Questions during testing?** Ask the host - they're familiar with the system!

**Want your own installation?** See [SETUP.md](SETUP.md) for installation guide.
