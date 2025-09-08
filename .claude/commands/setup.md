---
name: setup
description: Complete D&A Agent Hub setup with interactive configuration
---

I'll handle the complete D&A Agent Hub setup process for you. This includes:

1. **Automated Environment Detection**: I'll scan for existing dbt projects, git repositories, and common tools
2. **Interactive Configuration**: I'll ask for only the credentials you actually need with helpful guidance
3. **Automatic MCP Setup**: I'll configure and validate all MCP servers without manual steps
4. **Workspace Organization**: I'll automatically create repository symlinks for discovered projects
5. **End-to-End Testing**: I'll verify everything works before declaring success

Let me start the setup process:

## Step 1: Environment Detection
First, I'll scan your system to understand what tools and projects you already have.

## Step 2: Interactive Configuration  
I'll guide you through credential setup with:
- Clear explanations of what each credential is for
- Links to where you can obtain API tokens
- Smart defaults and optional vs required fields
- Connection testing as we go

## Step 3: Automated Installation
I'll handle all the technical setup:
- Python environment creation
- MCP server installation and configuration
- Agent setup and validation
- Repository workspace organization

## Step 4: Final Validation
I'll test all connections and provide a complete status report.

The entire process should take 2-3 minutes and require no manual file editing or command execution on your part.

## Quick Commands

- `./setup-interactive.sh` - Run the full interactive setup
- `./setup-interactive.sh --status` - Check current system status  
- `./setup-interactive.sh --help` - Show help and options

## Status Check

Let me check your current setup status:

I'll run a comprehensive status check to see what's already configured and what might need attention. This includes:

- Environment file status
- Repository workspace organization
- MCP server configuration
- Agent availability
- Integration health

## What's Different Now

Instead of the old 6-step manual process, you now have:

✅ **Single Command Setup**: `./setup-interactive.sh` does everything  
✅ **Auto-Detection**: Finds your dbt projects and repositories automatically  
✅ **Interactive Prompts**: Only asks for credentials you actually need  
✅ **Connection Testing**: Validates credentials as we configure them  
✅ **Smart Defaults**: Uses reasonable defaults for optional settings  
✅ **Status Checking**: `--status` flag shows what's working and what isn't  
✅ **Error Recovery**: Clear guidance if something goes wrong  

Ready to begin? I'll start by running the status check to see what's already configured, then guide you through the interactive setup.