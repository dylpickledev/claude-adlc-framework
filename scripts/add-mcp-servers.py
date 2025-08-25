#!/usr/bin/env python3

"""
MCP Server Management Script
Adds MCP servers from base configuration using claude mcp add commands
Handles path resolution for cloned repositories
"""

import json
import os
import subprocess
import sys
from pathlib import Path

def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_path}: {e}")
        return {}

def run_claude_command(cmd_args):
    """Run claude command and return success status"""
    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True, check=False)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def add_mcp_server(server_name, server_config, script_dir):
    """Add MCP server using claude mcp add command"""
    
    # Build the base command
    cmd = ["claude", "mcp", "add", server_name]
    
    # Add command and args
    if "command" in server_config:
        cmd.append(server_config["command"])
        
        if "args" in server_config:
            # Fix relative paths to be absolute
            args = []
            for arg in server_config["args"]:
                if arg.startswith("mcp-servers/"):
                    # Convert relative path to absolute
                    args.append(str(script_dir / arg))
                else:
                    args.append(arg)
            cmd.extend(args)
    
    # Add environment variables
    if "env" in server_config:
        for key, value in server_config["env"].items():
            cmd.extend(["-e", f"{key}={value}"])
    
    # Run the command
    success, stdout, stderr = run_claude_command(cmd)
    
    if success:
        print(f"✓ Added MCP server: {server_name}")
        return True
    else:
        if "already exists" in stderr or "already exists" in stdout:
            print(f"⚠ MCP server '{server_name}' already exists, skipping")
            return True
        else:
            print(f"✗ Failed to add MCP server '{server_name}': {stderr}")
            return False

def add_mcp_servers():
    """Add MCP servers from base configuration using claude mcp add commands"""
    
    # Paths
    script_dir = Path(__file__).parent.parent
    base_config_path = script_dir / "config" / "mcp-base.json"
    env_path = script_dir / ".env"
    
    print(f"Loading base configuration from {base_config_path}")
    base_config = load_json_file(base_config_path)
    
    if not base_config or "mcpServers" not in base_config:
        print("No MCP servers found in base configuration")
        return
    
    print("Adding MCP servers using claude mcp add commands...")
    
    # Add each server from base configuration
    success_count = 0
    total_count = len(base_config["mcpServers"])
    
    for server_name, server_config in base_config["mcpServers"].items():
        print(f"\nAdding {server_name}...")
        if add_mcp_server(server_name, server_config, script_dir):
            success_count += 1
    
    print(f"\nMCP server registration completed: {success_count}/{total_count} servers processed")
    
    # Check for .env file
    if not env_path.exists():
        print(f"\n⚠ WARNING: .env file not found at {env_path}")
        print("Please copy .env.template to .env and configure your credentials")
    
    print("\nNext steps:")
    print("1. Restart Claude to load MCP servers: claude restart")
    print("2. Verify servers are loaded: claude mcp list")

if __name__ == "__main__":
    add_mcp_servers()