#!/usr/bin/env python3

"""
Unified MCP Server Management Script
Handles all MCP server operations: add, remove, list, status
"""

import json
import os
import subprocess
import sys
import argparse
from pathlib import Path

class MCPManager:
    def __init__(self):
        self.script_dir = Path(__file__).parent.parent
        self.env_path = self.script_dir / ".env"
        
        # Hardcoded server configurations
        self.servers = {
            "dbt-mcp": {
                "command": "uvx",
                "args": ["dbt-mcp"],
                "env": {
                    "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
                }
            },
            "freshservice-mcp": {
                "command": "uvx", 
                "args": ["freshservice-mcp"],
                "env": {
                    "FRESHSERVICE_APIKEY": "${FRESHSERVICE_APIKEY}",
                    "FRESHSERVICE_DOMAIN": "${FRESHSERVICE_DOMAIN}",
                    "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
                }
            }
        }

    def load_json_file(self, file_path):
        """Load JSON file with error handling"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {file_path}: {e}")
            return {}

    def run_claude_command(self, cmd_args):
        """Run claude command and return success status"""
        try:
            result = subprocess.run(cmd_args, capture_output=True, text=True, check=False)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def add_mcp_server(self, server_name, server_config):
        """Add individual MCP server using claude mcp add command"""
        cmd = ["claude", "mcp", "add", server_name]
        
        # Add command and args
        if "command" in server_config:
            cmd.append(server_config["command"])
            
            if "args" in server_config:
                # Fix relative paths to be absolute
                args = []
                for arg in server_config["args"]:
                    if arg.startswith("mcp-servers/"):
                        args.append(str(self.script_dir / arg))
                    else:
                        args.append(arg)
                cmd.extend(args)
        
        # Add environment variables
        if "env" in server_config:
            for key, value in server_config["env"].items():
                cmd.extend(["-e", f"{key}={value}"])
        
        success, stdout, stderr = self.run_claude_command(cmd)
        
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

    def add_all_servers(self):
        """Add all MCP servers from configuration"""
        print("Adding MCP servers...")
        success_count = 0
        total_count = len(self.servers)
        
        for server_name, server_config in self.servers.items():
            print(f"\nAdding {server_name}...")
            if self.add_mcp_server(server_name, server_config):
                success_count += 1
        
        print(f"\nCompleted: {success_count}/{total_count} servers processed")
        
        if not self.env_path.exists():
            print(f"\n⚠ WARNING: .env file not found")
            print("Copy .env.template to .env and configure credentials")
        
        print("\nNext steps:")
        print("1. Restart Claude: claude restart")
        print("2. Verify servers: claude mcp list")
        
        return success_count > 0

    def remove_server(self, server_name):
        """Remove specific MCP server"""
        print(f"Removing MCP server: {server_name}")
        success, stdout, stderr = self.run_claude_command(["claude", "mcp", "remove", server_name])
        
        if success:
            print(f"✓ Removed MCP server: {server_name}")
            return True
        else:
            print(f"⚠ Failed to remove '{server_name}' (may not exist)")
            return False

    def list_servers(self):
        """List all configured MCP servers"""
        print("Configured MCP servers:")
        success, stdout, stderr = self.run_claude_command(["claude", "mcp", "list"])
        if success:
            print(stdout)
        else:
            print("Failed to list servers")
        return success

    def check_status(self):
        """Check MCP server status and environment"""
        print("MCP Server Status:")
        self.list_servers()
        
        if not self.env_path.exists():
            print("\n⚠ WARNING: .env file missing")
            print("Servers may not connect without proper credentials")
        else:
            print("\n✓ .env file found")
        
        print("\nNote: Additional servers planned for future releases")
        print("See FUTURE-IMPROVEMENTS.md for roadmap")

    def restart_claude(self):
        """Restart Claude to reload MCP servers"""
        print("Restarting Claude...")
        success, stdout, stderr = self.run_claude_command(["claude", "restart"])
        if success:
            print("✓ Claude restarted")
        else:
            print("Failed to restart Claude")
        return success

def main():
    parser = argparse.ArgumentParser(description="MCP Server Management")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add subcommands
    subparsers.add_parser("add", help="Add MCP servers from configuration")
    
    remove_parser = subparsers.add_parser("remove", help="Remove MCP server")
    remove_parser.add_argument("server_name", help="Name of server to remove")
    
    subparsers.add_parser("list", help="List configured MCP servers")
    subparsers.add_parser("status", help="Check server status")
    subparsers.add_parser("restart", help="Restart Claude")
    
    args = parser.parse_args()
    manager = MCPManager()
    
    if args.command == "add":
        manager.add_all_servers()
    elif args.command == "remove":
        manager.remove_server(args.server_name)
    elif args.command == "list":
        manager.list_servers()
    elif args.command == "status":
        manager.check_status()
    elif args.command == "restart":
        manager.restart_claude()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()