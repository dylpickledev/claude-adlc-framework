# /switch Command Protocol

## Purpose
Seamlessly switch between projects/tasks while preserving current work and preparing for new context. Implements complete workflow for context switching with work preservation.

## Usage
```bash
claude /switch [optional-target-branch]
```

## Protocol

### 1. Execute switch.sh Script
```bash
./scripts/switch.sh [optional-target-branch]
```

### 2. Complete Context Switch Workflow
The script automatically handles:
- **Auto-commit current work**: Saves progress with generated commit message
- **Push to remote**: Preserves work on remote repository
- **Switch to main**: Returns to clean main branch state
- **Sync main**: Ensures latest changes from remote
- **Optional branch switch**: Moves to specified target branch if provided

## Claude Instructions

When user runs `/switch [optional-target-branch]`:

1. **Execute the script**: Run `./scripts/switch.sh [optional-target-branch]`
2. **Monitor workflow steps**: Display each phase of the context switch
3. **Validate completion**: Confirm successful branch switch and work preservation
4. **Provide guidance**: Explain next steps for context clearing

### Response Format
```
🔄 Executing project/task switch workflow...
✅ Current work committed and pushed to remote
✅ Switched to main branch and synced
✅ Ready for new context

💡 Next steps:
   1. Use '/clear' to reset Claude Code conversation context
   2. Or restart Claude Code for completely fresh start
   3. Begin new work with clean state!

📁 Previous work preserved on: [previous-branch-name]
📁 Current branch: [current-branch-name]
```

## Workflow Automation

### Automatic Work Preservation
- **Staging**: All changes automatically staged with `git add .`
- **Commit Message**: Auto-generated based on branch type and description
- **Remote Push**: Ensures work is preserved remotely for recovery
- **Clean State**: Returns to main branch ready for new work

### Branch Management
- **Feature branches**: `feat:` commit prefix for feature work
- **Fix branches**: `fix:` commit prefix for bug fixes
- **Research branches**: `docs:` commit prefix for research/analysis
- **Other branches**: `chore:` commit prefix for general work

### Context Preparation
- **Clean repository**: No uncommitted changes or staging area conflicts
- **Synced main**: Latest changes from remote ensure current baseline
- **Clear guidance**: Instructions for Claude Code context reset
- **Resume capability**: Easy return to previous work when needed

## Integration with ADLC

### ADLC Phase Transitions
- **Complete current phase**: Preserve work at any point in development lifecycle
- **Clean context switch**: Fresh start for new phase or project
- **Seamless resumption**: Return to previous work without loss

### Project Management Integration
- **Work preservation**: All project files and context maintained
- **Traceability**: Git history maintains project progression
- **Team coordination**: Remote branches enable collaboration and review

## Usage Examples

### Example 1: Simple Context Switch
```bash
claude /switch
# → Saves current work, switches to main, ready for new task
```

### Example 2: Switch to Specific Project
```bash
claude /switch feature-customer-dashboard
# → Saves current work, switches to specified branch
```

### Example 3: Resume Previous Work
```bash
claude /switch research-performance-optimization
# → Returns to previous research project branch
```

## Error Handling
- **Uncommitted changes**: Automatically commits with descriptive message
- **Merge conflicts**: Provides clear resolution guidance
- **Remote issues**: Handles network connectivity and remote repository problems
- **Branch conflicts**: Clear error messages for branch management issues

## Success Criteria
- [ ] Current work committed and pushed to remote successfully
- [ ] Clean switch to target branch (main or specified)
- [ ] Repository in clean state with no uncommitted changes
- [ ] Clear guidance provided for Claude Code context reset
- [ ] Previous work easily recoverable via branch switching

## Benefits

### For Individual Workflow
- **Zero work loss**: All progress automatically preserved
- **Quick context switching**: Single command handles complete workflow
- **Clean mental model**: Fresh start for each new task
- **Easy resumption**: Simple return to previous work

### For Team Collaboration
- **Work visibility**: All branches pushed to remote for team access
- **Review readiness**: Committed work ready for pull request creation
- **Conflict avoidance**: Clean main branch reduces merge issues
- **Knowledge sharing**: Preserved work enables collaboration

---

*Complete context switching solution - preserving current work while preparing for new tasks with zero friction.*