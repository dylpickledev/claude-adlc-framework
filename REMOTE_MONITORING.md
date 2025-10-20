# Remote Monitoring Setup

Monitor your DA Agent Hub work from anywhere via iPhone using Tailscale + tmux + Mosh.

## Quick Start

### From Mac:
```bash
/start [issue#|"idea"]  # Auto-creates tmux session
# Work normally in Claude Code
```

### From iPhone (Blink Shell):
```bash
mosh dylanmorrish@macbook-fair  # Persistent connection
tmux attach -t feature-<project-name>  # See Claude working
```

## Complete Setup

### One-Time Mac Setup ✅ DONE
- [x] Tailscale installed and connected
- [x] SSH enabled (Remote Login)
- [x] Mac won't sleep when plugged in
- [x] tmux configured (~/.tmux.conf)
- [x] Mosh installed

### One-Time iPhone Setup
1. **Tailscale**: Already installed ✅
2. **Blink Shell**: Installed ($21.99) ✅
3. **Configure Mosh in Blink**:
   - Config → Hosts → Edit macbook-fair
   - Enable "Use Mosh"
   - Save

## Workflow

### Start New Project
```bash
/start 123  # or /start "Build new feature"
```
- Creates project structure
- Creates dedicated tmux session: `feature-<project-name>`
- Shows connection instructions

### Monitor from iPhone
```bash
# Connect (survives phone lock/network changes)
mosh dylanmorrish@macbook-fair

# List all active sessions
tmux ls

# Attach to specific project
tmux attach -t feature-<project-name>

# Scroll through output with finger
# Detach: Ctrl+b then d (or just close Blink)
```

### Check Active Sessions
```bash
/monitor  # Lists all tmux sessions
```

### Switch Projects
```bash
/switch feature-other-project
# Shows if tmux session available
```

### Complete Project
```bash
/complete feature-<project-name>
# Automatically kills tmux session
```

## Key Features

**Persistent Sessions**
- Claude keeps running even when you disconnect
- Resume exactly where you left off
- Survives Mac sleep/wake

**Mobile-Friendly**
- Touch scrolling enabled
- Large scrollback buffer (50k lines)
- Clear status bar

**Mosh Benefits**
- Survives phone lock/unlock
- Handles WiFi → Cellular transitions
- Instant reconnection
- Works through VPN changes

**Parallel Work**
- Multiple projects = multiple tmux sessions
- Monitor different work streams
- Easy to switch between contexts

## Connection Details

**Mac Tailscale Name**: `macbook-fair`
**Mac Tailscale IP**: `100.86.192.18`
**iPhone Tailscale IP**: `100.89.51.126`

**SSH**: `ssh dylanmorrish@macbook-fair`
**Mosh**: `mosh dylanmorrish@macbook-fair` (recommended for mobile)

## Troubleshooting

**Can't connect from iPhone:**
- Check Tailscale connected on both devices
- Try IP instead: `mosh dylanmorrish@100.86.192.18`

**Disconnects when phone locks:**
- Use Mosh instead of SSH
- Configure in Blink: Hosts → Use Mosh

**tmux session not found:**
- Check available: `tmux ls`
- Session may have been killed
- Restart with `/start`

**Mac unreachable:**
- Check Mac didn't sleep (should be plugged in)
- Verify Tailscale running on Mac

## Files Changed

- `scripts/start.sh`: Auto-create tmux sessions
- `scripts/switch.sh`: Show tmux session availability
- `scripts/finish.sh`: Auto-cleanup tmux sessions
- `scripts/monitor.sh`: List active sessions
- `.claude/commands/monitor.md`: /monitor slash command

## Next Steps

1. **Test it**: Configure Mosh in Blink
2. **Try it**: Lock phone while connected - should stay connected
3. **Use it**: Monitor actual Claude work from anywhere

---

**Branch**: `feature/tmux-worktree-integration`
**Ready for**: Testing and PR if successful
