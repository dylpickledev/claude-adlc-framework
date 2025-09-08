---
name: setup
description: Complete D&A Agent Hub setup with interactive configuration
---

I'll handle the complete D&A Agent Hub setup process for you. This streamlined setup includes:

## ✨ **New Interactive Setup Features**

### 🔍 **Automated Environment Detection**
- Scans for existing dbt projects across your system
- Detects git repositories for workspace organization  
- Validates required tools (python3, git, claude CLI)
- Reports optional tools (dbt, snowsql, psql) if available

### 🎯 **Smart Credential Collection**
- **Selective Configuration**: Only prompts for integrations you want to use
- **Existing Value Preservation**: Detects and offers to keep current credentials
- **Live Connection Testing**: Validates credentials as you enter them
- **Clear Guidance**: Direct links to token generation pages

### 🏗️ **Repository Configuration System**
- **JSON-Based Repository Management**: Uses `config/repositories.json` for centralized repo configuration
- **Authenticated Cloning**: Uses GitHub tokens for private repositories
- **Batch Repository Operations**: Clones all configured repositories in one step
- **Update-Aware**: Can update existing repositories or skip them based on configuration

### 🔧 **Enhanced Technical Setup**
- **Developer Customization Framework**: Creates `developer/` directory for personal configurations
- **Comprehensive Git Ignore**: Automatically generates complete `.gitignore` 
- **Agent Installation**: Copies agents to `~/.claude/agents/`
- **MCP Auto-Configuration**: Automatically sets up all MCP servers

## 🎛️ **Available Commands**

### Primary Commands
- **`./setup.sh`** - Run the full interactive setup
- **`./setup.sh --status`** - Check current system status and configuration
- **`./setup.sh --help`** - Show detailed help and options

## 📋 **Supported Integrations**

### Core Data Stack
- **dbt Cloud**: API token and environment configuration for transformation management
- **Snowflake**: Complete connection details with key-based authentication
  - Account, user, private key, warehouse, database, schema, role

### Workflow & Project Management
- **ClickUp**: Client credentials and team ID for project management integration
- **Orchestra**: API URL and key for workflow orchestration

### Optional Integrations  
- **Freshservice**: API key and domain for IT service management
- **GitHub**: Personal access token for authenticated repository access
- **Tableau**: Server connection details for business intelligence integration

## 🔄 **Setup Workflow**

### Phase 1: Discovery
1. **Environment Scanning**: Locates dbt projects and git repositories
2. **Tool Validation**: Ensures required dependencies are installed
3. **Existing Configuration**: Loads any previous environment setup

### Phase 2: Configuration
1. **Interactive Credential Collection**: Prompts only for needed integrations
2. **Connection Validation**: Tests each integration as configured
3. **Environment Generation**: Creates comprehensive `.env` file

### Phase 3: Implementation  
1. **Repository Cloning**: Uses `config/repositories.json` to clone all configured repos
2. **Python Environment**: Sets up virtual environment with required packages
3. **Agent & MCP Setup**: Installs agents and configures MCP servers
4. **Developer Framework**: Creates customization structure

### Phase 4: Validation
1. **System Health Check**: Validates Claude CLI and MCP configuration
2. **Integration Count**: Reports number of successfully configured integrations
3. **Next Steps Guidance**: Provides clear instructions for getting started

## 🎯 **Status Checking**

The `--status` command provides comprehensive system health information:

- **Environment Configuration**: Shows configured integrations
- **Repository Workspace**: Reports linked repository count
- **MCP Server Status**: Validates MCP configuration file
- **Agent Availability**: Counts installed agents

## 🧩 **Repository Configuration**

The setup now uses `config/repositories.json` for repository management:

```json
{
  "repos": {
    "project-name": {
      "url": "https://github.com/user/repo.git",
      "branch": "main",
      "description": "Project description",
      "env_var": "PROJECT_DIR"
    }
  },
  "knowledge": {
    "docs-repo": {
      "url": "https://github.com/user/docs.git", 
      "branch": "main",
      "description": "Documentation repository",
      "type": "git_repository"
    }
  },
  "settings": {
    "clone_method": "https",
    "depth": null,
    "update_existing": true,
    "check_git_access": true,
    "fallback_to_symlink": true
  }
}
```

## 🔧 **Developer Customization**

Post-setup customization through `developer/customize.sh`:
- Personal repository symlinks
- Custom environment variables  
- Additional MCP servers
- Personal configuration files

## 🚀 **Quick Start**

1. **Run Setup**: `./setup.sh` - Complete interactive configuration
2. **Restart Claude**: `claude restart` - Load MCP servers  
3. **Check Status**: `./setup.sh --status` - Verify everything works
4. **Customize**: `./developer/customize.sh` - Add personal configurations

## 📊 **Key Features**

✅ **Single Command Experience**: Complete setup in one interactive session  
✅ **Repository Configuration System**: JSON-based centralized repository management with rich metadata  
✅ **Authenticated Git Operations**: GitHub token integration for private repos with fallback options  
✅ **Developer Customization Framework**: Personal configuration system isolated from git tracking  
✅ **Enhanced Status Reporting**: Comprehensive system health dashboard showing all integrations  
✅ **Connection Validation**: Real-time credential testing for dbt Cloud and format validation  
✅ **Smart Environment Detection**: Automatic discovery of existing tools and projects
✅ **Multi-Integration Support**: Supports 6+ different service integrations with selective configuration

The setup process typically completes in 2-3 minutes with no manual file editing required.