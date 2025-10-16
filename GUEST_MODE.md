# DA Agent Hub - Guest Mode

> Test drive da-agent-hub with your own repositories using someone else's Claude Code installation

## What is Guest Mode?

Guest Mode creates an isolated "sandbox" session where you can test da-agent-hub with **your own GitHub repositories** while using the **host's Claude Code installation and API credits**.

Think of it like a "private browsing" mode for Claude Code - your work stays isolated, but you get to use the full system.

## What Gets Isolated vs Shared

### Isolated (Your Own)
- ✅ GitHub authentication (your `gh` login)
- ✅ Git configuration (your name/email)
- ✅ Repository clones (your repos, not the host's)
- ✅ Project files and work artifacts
- ✅ Working directory

### Shared (Host's)
- ✅ Claude Code CLI installation
- ✅ Anthropic API credits (host pays)
- ✅ da-agent-hub scripts and agents
- ✅ MCP server configurations
- ✅ Python environment and dependencies

## Quick Start for Guests

### 1. Host Creates Your Session
```bash
# Host runs this
./scripts/guest-mode.sh start workshop-demo
```

### 2. Activate Your Session
```bash
# You run this
source .guest-sessions/workshop-demo/activate.sh
```

### 3. Authenticate with Your GitHub
```bash
# Use your GitHub account
gh auth login

# Configure your git identity
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 4. Use da-agent-hub Normally
```bash
# Create an idea in YOUR repository
claude /capture "Build customer analytics dashboard"

# Research with specialist agents
claude /research 123

# Start development
claude /start 123

# Complete project
claude /complete feature-customer-analytics
```

### 5. When Done
```bash
# Exit guest mode
source .guest-sessions/workshop-demo/deactivate.sh

# Host cleans up
./scripts/guest-mode.sh stop workshop-demo
```

## Host Guide

### Creating Guest Sessions

**For workshops/demos:**
```bash
./scripts/guest-mode.sh start workshop-2024-01-15
```

**For individual testing:**
```bash
./scripts/guest-mode.sh start alice-evaluation
```

### Managing Sessions

**List active sessions:**
```bash
./scripts/guest-mode.sh list
```

**Stop a session (with optional archive):**
```bash
./scripts/guest-mode.sh stop workshop-demo
```

**Clean up all sessions:**
```bash
./scripts/guest-mode.sh cleanup
```

## Use Cases

### 1. Workshop/Training Sessions
- Create one session per workshop
- Multiple attendees can use same laptop sequentially
- Each person authenticates with their own GitHub
- Clean slate for each participant

### 2. Evaluation/Testing
- Let potential users test with their actual data stack
- No need to share your credentials or repos
- They experience real da-agent-hub workflow
- Easy cleanup after evaluation

### 3. Pair Programming
- Collaborate with different GitHub contexts
- Switch between host and guest mode quickly
- Guest brings their repos, host provides infrastructure

### 4. Demos
- Show da-agent-hub to stakeholders
- Let them try it hands-on safely
- No risk to your production environment

## Security & Privacy

### What Guests CAN Access
- Their own GitHub repositories (after authentication)
- da-agent-hub scripts and documentation
- Claude Code AI capabilities (via your API credits)
- MCP tools (using your configurations)

### What Guests CANNOT Access
- Your GitHub repositories
- Your personal files outside the guest session
- Your git credentials or API keys
- Your repository configurations
- Any work from other guest sessions

### Best Practices
1. **Always stop sessions when done** - Removes guest's authentication
2. **Archive important work** - Guest sessions can be archived before removal
3. **Review guest work** - Check what was created before cleanup
4. **Monitor API usage** - Guest uses your Claude Code credits
5. **Trust your guests** - They'll have access to Claude Code's capabilities

## Technical Details

### Environment Isolation

Guest mode creates isolated:
- `GH_CONFIG_DIR` - Separate GitHub CLI config
- `GIT_CONFIG_GLOBAL` - Separate git configuration
- Working directory - All work in `.guest-sessions/<name>/`

### File Structure

```
.guest-sessions/
└── workshop-demo/
    ├── activate.sh              # Session activation script
    ├── deactivate.sh            # Session cleanup script
    ├── .session-info            # Metadata about session
    ├── .gitconfig              # Guest's git config
    ├── .config/gh/             # Guest's GitHub CLI config
    ├── config/
    │   └── repositories.json   # Guest's repo configuration
    ├── repos/                  # Guest's cloned repositories
    ├── knowledge/              # Guest's knowledge sources
    └── projects/               # Guest's active projects
```

### Cleanup

**Manual cleanup:**
```bash
./scripts/guest-mode.sh stop <session-name>
```

**Automatic archiving:**
- Sessions are archived to `.guest-sessions-archive/` before removal
- Archives are `.tar.gz` files with timestamp
- Can be restored if needed

## Limitations

1. **One session at a time** - Guest activates one session per shell
2. **Host's API credits** - Usage counts against host's Anthropic account
3. **Shared MCP config** - Guest uses host's MCP server setup
4. **No persistent auth** - GitHub auth removed when session ends
5. **Local only** - Guest work stays on host's laptop

## Troubleshooting

### "Session already exists"
```bash
# List existing sessions
./scripts/guest-mode.sh list

# Stop the existing session first
./scripts/guest-mode.sh stop <session-name>
```

### "gh auth failed"
```bash
# Guest needs to authenticate with their GitHub
gh auth login

# Follow the prompts to authenticate
```

### "Permission denied"
```bash
# Make sure script is executable
chmod +x scripts/guest-mode.sh
```

### "Cannot access host repositories"
This is by design - guest mode isolates you from host's repositories. Use your own repositories instead.

## FAQ

**Q: Does the guest need a Claude Code account?**
A: No, they use the host's installation and API credits.

**Q: Can multiple guests use the same laptop?**
A: Yes, but sequentially. Create separate sessions for each person.

**Q: What happens to the guest's work?**
A: It's stored in `.guest-sessions/<name>/` and can be archived or deleted.

**Q: Can the guest commit to their repositories?**
A: Yes, they authenticate with their own GitHub account and can push/pull normally.

**Q: Does this work with private repositories?**
A: Yes, as long as the guest authenticates with `gh auth login`.

**Q: How much does this cost the host?**
A: Guest usage counts against host's Claude API credits (same as normal usage).

**Q: Can the host see what the guest is doing?**
A: Yes, all guest files are in `.guest-sessions/<name>/` on the host's system.

## Advanced: Persisting Guest Sessions

If you want to let a guest continue their work across multiple visits:

```bash
# Don't stop the session between visits
# Guest can reactivate the same session
source .guest-sessions/workshop-demo/activate.sh

# Their GitHub auth and work will still be there
```

**Note:** This keeps the guest's GitHub credentials on your system until you explicitly stop the session.

## Support

For issues or questions:
- Check the main README.md
- Review SETUP.md for general setup
- See CLAUDE.md for workflow documentation

---

**Happy testing!** Guest mode makes it easy to share da-agent-hub without compromising security or requiring guests to set up their own installation.
