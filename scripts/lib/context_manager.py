#!/usr/bin/env python3
"""
Context Manager for Extended Thinking & Memory Integration
Implements Anthropic best practices for context preservation across Claude sessions

Based on official Anthropic guidance:
- Extended thinking block preservation
- Memory tool patterns for cross-session learning
- Context editing automation
- Security validation for memory operations
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class ThinkingBlock:
    """Represents a preserved thinking block from Claude's reasoning"""
    content: str
    turn_number: int
    timestamp: str
    sequence_position: int  # Position in sequence of consecutive thinking blocks
    tool_uses: List[str]  # Tool calls that followed this thinking

    def validate(self) -> bool:
        """Validate thinking block completeness per Anthropic constraints"""
        if not self.content:
            return False
        if self.turn_number < 0:
            return False
        if self.sequence_position < 0:
            return False
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ThinkingBlock':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ConversationContext:
    """Complete conversation context for pause/resume"""
    description: str
    timestamp: str
    current_task: str
    progress_made: List[str]
    decisions_made: List[Dict[str, str]]
    next_steps: List[str]
    blockers: List[str]
    relevant_files: List[Dict[str, str]]
    agents_involved: List[Dict[str, str]]
    thinking_blocks: List[ThinkingBlock]
    session_duration_estimate: str
    conversation_exchanges: int
    key_topics: List[str]
    project_name: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        data = asdict(self)
        # Convert ThinkingBlock objects to dicts
        data['thinking_blocks'] = [tb.to_dict() for tb in self.thinking_blocks]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'ConversationContext':
        """Create from dictionary"""
        # Convert thinking block dicts back to objects
        thinking_blocks = [ThinkingBlock.from_dict(tb) for tb in data.get('thinking_blocks', [])]
        data['thinking_blocks'] = thinking_blocks
        return cls(**data)


class SecurityValidator:
    """Security validation for memory operations per Anthropic guidance"""

    @staticmethod
    def validate_path(path: str, base_dir: str) -> str:
        """
        Prevent directory traversal attacks

        Anthropic guidance: "Memory files are read back into Claude's context,
        making them a potential vector for prompt injection."
        """
        base_dir_abs = os.path.abspath(base_dir)
        requested_abs = os.path.abspath(os.path.join(base_dir_abs, path))

        if not requested_abs.startswith(base_dir_abs):
            raise SecurityError(
                f"Path traversal attempt detected: {path} escapes {base_dir}"
            )

        return requested_abs

    @staticmethod
    def sanitize_content(content: str) -> str:
        """
        Prevent prompt injection via memory content

        Removes patterns that could manipulate Claude's behavior when
        memory is loaded back into context.
        """
        dangerous_patterns = [
            (r"<claude>.*?</claude>", "[REDACTED: POTENTIAL INJECTION]"),
            (r"IGNORE\s+PREVIOUS\s+INSTRUCTIONS", "[REDACTED: COMMAND INJECTION]"),
            (r"\[SYSTEM\]", "[REDACTED: SYSTEM TAG]"),
            (r"<system>.*?</system>", "[REDACTED: SYSTEM INJECTION]"),
            (r"You are now.*?instead", "[REDACTED: ROLE INJECTION]"),
        ]

        sanitized = content
        for pattern, replacement in dangerous_patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def audit_log(operation: str, path: str, success: bool, error: Optional[str] = None):
        """Log all memory operations for security review"""
        audit_dir = Path.home() / ".claude" / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)

        audit_file = audit_dir / f"memory-audit-{datetime.now().strftime('%Y-%m')}.jsonl"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "path": path,
            "success": success,
            "error": error,
            "pid": os.getpid()
        }

        with open(audit_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


class SecurityError(Exception):
    """Security validation error"""
    pass


class ContextManager:
    """
    Manages conversation context preservation and restoration

    Implements Anthropic best practices:
    - Extended thinking block preservation
    - Memory tool integration
    - Context editing automation
    - Security validation
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path.cwd()

        self.paused_contexts_dir = self.project_root / ".claude" / "paused-contexts"
        self.memory_dir = self.project_root / ".claude" / "memory"
        self.validator = SecurityValidator()

        # Ensure directories exist
        self.paused_contexts_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def save_context(self, context: ConversationContext) -> Path:
        """
        Save conversation context with thinking blocks

        Per Anthropic: "Include the complete unmodified block back to the API"
        """
        # Validate thinking blocks
        for tb in context.thinking_blocks:
            if not tb.validate():
                raise ValueError(f"Invalid thinking block at position {tb.sequence_position}")

        # Sanitize sensitive content
        context.description = self.validator.sanitize_content(context.description)
        context.current_task = self.validator.sanitize_content(context.current_task)

        # Determine save location (project-specific or global)
        if context.project_name:
            project_dir = self.project_root / "projects" / "active" / context.project_name
            if project_dir.exists():
                save_dir = project_dir / "paused-contexts"
                save_dir.mkdir(exist_ok=True)
            else:
                save_dir = self.paused_contexts_dir
        else:
            save_dir = self.paused_contexts_dir

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        slug = re.sub(r'[^a-z0-9]+', '-', context.description.lower())[:50]
        filename = f"{timestamp}-{slug}.json"

        filepath = save_dir / filename

        # Save as JSON
        try:
            with open(filepath, 'w') as f:
                json.dump(context.to_dict(), f, indent=2)

            self.validator.audit_log("save_context", str(filepath), True)
            return filepath

        except Exception as e:
            self.validator.audit_log("save_context", str(filepath), False, str(e))
            raise

    def load_context(self, filepath: Path) -> ConversationContext:
        """
        Load conversation context with thinking blocks

        Validates path security and reconstructs thinking blocks for continuation.
        """
        # Validate path
        validated_path = self.validator.validate_path(
            str(filepath),
            str(self.project_root)
        )

        try:
            with open(validated_path, 'r') as f:
                data = json.load(f)

            context = ConversationContext.from_dict(data)

            self.validator.audit_log("load_context", str(filepath), True)
            return context

        except Exception as e:
            self.validator.audit_log("load_context", str(filepath), False, str(e))
            raise

    def detect_active_project(self) -> Optional[str]:
        """
        Auto-detect active project from git branch and file access

        Multi-signal detection per research recommendations:
        1. Git branch name
        2. Recent file access patterns
        3. Project directory existence
        """
        # Signal 1: Git branch name
        try:
            import subprocess
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.project_root,
                text=True
            ).strip()

            if branch.startswith('feature-') or branch.startswith('fix-') or branch.startswith('research-'):
                project_dir = self.project_root / "projects" / "active" / branch
                if (project_dir / "spec.md").exists():
                    return branch

        except subprocess.CalledProcessError:
            pass

        # Signal 2: Recent file access (last 4 hours)
        projects_dir = self.project_root / "projects" / "active"
        if projects_dir.exists():
            recent_projects = []
            four_hours_ago = datetime.now().timestamp() - (4 * 3600)

            for project_dir in projects_dir.iterdir():
                if project_dir.is_dir():
                    spec_file = project_dir / "spec.md"
                    if spec_file.exists():
                        if spec_file.stat().st_mtime > four_hours_ago:
                            recent_projects.append(project_dir.name)

            if len(recent_projects) == 1:
                return recent_projects[0]

        return None

    def estimate_conversation_tokens(self) -> int:
        """
        Estimate current conversation token count

        This is a rough heuristic - actual token count requires Claude API.
        Used for context window management per Anthropic guidance.
        """
        # Rough estimate: 4 characters per token
        # This is conservative - actual may vary

        # Would need access to conversation history here
        # For now, return a placeholder that can be overridden
        return 0  # Implement when conversation history available

    def generate_context_summary(self, context: ConversationContext) -> str:
        """Generate human-readable summary of paused context"""
        summary = f"""# Paused Context: {context.description}

**Date**: {context.timestamp}
**Session Duration**: {context.session_duration_estimate}
**Primary Focus**: {context.current_task}

## Current Task

{context.current_task}

## Progress Made

"""
        for item in context.progress_made:
            summary += f"- {item}\n"

        summary += "\n## Decisions Made\n\n"
        for decision in context.decisions_made:
            summary += f"1. **Decision**: {decision.get('description', 'N/A')}\n"
            summary += f"   - **Rationale**: {decision.get('rationale', 'N/A')}\n"
            summary += f"   - **Implications**: {decision.get('implications', 'N/A')}\n\n"

        summary += "## Next Steps\n\n"
        for step in context.next_steps:
            summary += f"- [ ] {step}\n"

        if context.blockers:
            summary += "\n## Blockers & Questions\n\n"
            for blocker in context.blockers:
                summary += f"- {blocker}\n"

        summary += "\n## Relevant Files\n\n"
        for file_info in context.relevant_files:
            summary += f"- `{file_info.get('path', 'N/A')}` - {file_info.get('reason', 'N/A')}\n"

        if context.agents_involved:
            summary += "\n## Agents Involved\n\n"
            for agent in context.agents_involved:
                summary += f"- **{agent.get('name', 'N/A')}**: {agent.get('contribution', 'N/A')}\n"

        if context.thinking_blocks:
            summary += f"\n## Extended Thinking Preserved\n\n"
            summary += f"**Thinking blocks**: {len(context.thinking_blocks)} blocks preserved\n"
            summary += f"**Total reasoning turns**: {max([tb.turn_number for tb in context.thinking_blocks], default=0)}\n"
            summary += f"**Tool uses tracked**: {sum([len(tb.tool_uses) for tb in context.thinking_blocks])}\n\n"
            summary += "⚠️ **Important**: Thinking blocks are stored in JSON format for API restoration.\n"
            summary += "When resuming, these blocks ensure Claude continues reasoning from the exact point it left off.\n"

        summary += f"\n## Conversation Summary\n\n"
        summary += f"**Total exchanges**: {context.conversation_exchanges}\n"
        summary += f"**Key topics**: {', '.join(context.key_topics)}\n\n"

        summary += "---\n"
        summary += "*Paused via enhanced /pause command with extended thinking preservation*\n"
        summary += f"*Resume with: 'Continue from {context.description}'*\n"

        return summary


class MemoryManager:
    """
    Manages persistent memory across Claude sessions

    Implements Anthropic memory tool patterns:
    - view, create, str_replace, insert, delete, rename operations
    - Security validation
    - Cross-conversation learning
    """

    def __init__(self, memory_root: Optional[str] = None):
        if memory_root:
            self.memory_root = Path(memory_root)
        else:
            self.memory_root = Path.cwd() / ".claude" / "memory"

        self.memory_root.mkdir(parents=True, exist_ok=True)
        self.validator = SecurityValidator()

        # Initialize memory structure
        self._init_memory_structure()

    def _init_memory_structure(self):
        """Initialize memory directory structure"""
        subdirs = [
            "switch-contexts",      # /switch operation history
            "project-contexts",     # Project-specific memories
            "patterns",             # Learned patterns
            "preferences",          # User preferences
            "agent-knowledge"       # Cross-session agent learnings
        ]

        for subdir in subdirs:
            (self.memory_root / subdir).mkdir(exist_ok=True)

    def remember_switch(self, from_project: str, to_project: str,
                       preservation_method: str, duration_seconds: float):
        """
        Remember a switch operation for learning

        Implements cross-conversation learning per Anthropic memory tool guidance.
        """
        memory = {
            "from_project": from_project,
            "to_project": to_project,
            "preservation_method": preservation_method,
            "duration_seconds": duration_seconds,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }

        # Generate unique filename
        memory_hash = hashlib.sha256(
            f"{from_project}-{to_project}-{datetime.now()}".encode()
        ).hexdigest()[:12]

        filepath = self.memory_root / "switch-contexts" / f"switch-{memory_hash}.json"

        try:
            with open(filepath, 'w') as f:
                json.dump(memory, f, indent=2)

            self.validator.audit_log("remember_switch", str(filepath), True)

        except Exception as e:
            self.validator.audit_log("remember_switch", str(filepath), False, str(e))
            raise

    def query_switches(self, from_project: Optional[str] = None,
                      to_project: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query switch history for patterns"""
        switches_dir = self.memory_root / "switch-contexts"
        matches = []

        for switch_file in switches_dir.glob("switch-*.json"):
            try:
                with open(switch_file, 'r') as f:
                    switch_data = json.load(f)

                # Filter by criteria
                if from_project and switch_data.get("from_project") != from_project:
                    continue
                if to_project and switch_data.get("to_project") != to_project:
                    continue

                matches.append(switch_data)

            except Exception:
                continue

        return matches

    def suggest_switch_approach(self, from_project: str, to_project: str) -> Dict[str, Any]:
        """
        Suggest optimal switch approach based on learned patterns

        Uses memory to provide personalized recommendations.
        """
        similar_switches = self.query_switches(from_project, to_project)

        if not similar_switches:
            return {
                "suggestion": "commit",
                "confidence": 0.5,
                "reason": "No historical data - defaulting to commit"
            }

        # Analyze patterns
        commit_count = sum(1 for s in similar_switches if s.get("preservation_method") == "commit")
        stash_count = sum(1 for s in similar_switches if s.get("preservation_method") == "stash")

        avg_duration = sum(s.get("duration_seconds", 0) for s in similar_switches) / len(similar_switches)

        if commit_count > stash_count:
            suggestion = "commit"
            confidence = commit_count / len(similar_switches)
            reason = f"You usually commit when switching between these projects ({commit_count}/{len(similar_switches)} times)"
        else:
            suggestion = "stash"
            confidence = stash_count / len(similar_switches)
            reason = f"You usually stash when switching between these projects ({stash_count}/{len(similar_switches)} times)"

        return {
            "suggestion": suggestion,
            "confidence": confidence,
            "reason": reason,
            "avg_duration": avg_duration,
            "sample_size": len(similar_switches)
        }


# CLI interface for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: context_manager.py [save|load|detect-project]")
        sys.exit(1)

    command = sys.argv[1]
    manager = ContextManager()

    if command == "detect-project":
        project = manager.detect_active_project()
        print(f"Active project: {project or 'None detected'}")

    elif command == "save":
        # Example save
        context = ConversationContext(
            description="Testing context manager",
            timestamp=datetime.now().isoformat(),
            current_task="Implement context management",
            progress_made=["Created context manager", "Added thinking blocks"],
            decisions_made=[],
            next_steps=["Test in production", "Add more features"],
            blockers=[],
            relevant_files=[],
            agents_involved=[],
            thinking_blocks=[],
            session_duration_estimate="1 hour",
            conversation_exchanges=10,
            key_topics=["context management", "extended thinking"]
        )

        filepath = manager.save_context(context)
        print(f"Context saved: {filepath}")

    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: context_manager.py load <filepath>")
            sys.exit(1)

        filepath = Path(sys.argv[2])
        context = manager.load_context(filepath)
        print(f"Loaded context: {context.description}")
        print(f"Thinking blocks: {len(context.thinking_blocks)}")
