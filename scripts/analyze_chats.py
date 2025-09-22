#!/usr/bin/env python3

"""
analyze_chats.py - Claude chat analysis for DA Agent Hub training

Analyzes Claude Code conversation histories to extract agent effectiveness patterns,
identify knowledge gaps, and generate improvement recommendations for the ADLC system.

Usage: python3 analyze_chats.py <claude_project_dir> <repo_root>
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import re

def analyze_conversations(project_dir, repo_root):
    """Analyze all JSONL files in Claude project directory"""

    project_path = Path(project_dir)
    repo_path = Path(repo_root)

    if not project_path.exists():
        print(f"❌ Claude project directory not found: {project_path}")
        return None

    # Find all conversation files
    conversations = list(project_path.glob('*.jsonl'))
    print(f"📁 Analyzing {len(conversations)} conversation files...")

    # Initialize metrics
    metrics = {
        'agent_usage': defaultdict(int),
        'agent_effectiveness': defaultdict(list),
        'knowledge_gaps': defaultdict(int),
        'collaboration_patterns': [],
        'common_queries': defaultdict(int),
        'user_satisfaction_signals': defaultdict(int),
        'conversation_count': len(conversations),
        'analysis_date': datetime.now().isoformat()
    }

    # Analyze each conversation
    total_messages = 0
    for conv_file in conversations:
        try:
            conv_metrics = analyze_single_conversation(conv_file)
            total_messages += conv_metrics.get('message_count', 0)

            # Aggregate metrics
            for agent, count in conv_metrics.get('agents_used', {}).items():
                metrics['agent_usage'][agent] += count

            for gap in conv_metrics.get('knowledge_gaps', []):
                metrics['knowledge_gaps'][gap] += 1

            for query in conv_metrics.get('common_queries', []):
                metrics['common_queries'][query] += 1

            metrics['collaboration_patterns'].extend(conv_metrics.get('collaborations', []))

        except Exception as e:
            print(f"⚠️  Error analyzing {conv_file.name}: {e}")
            continue

    metrics['total_messages'] = total_messages

    # Generate analysis report
    generate_analysis_report(metrics, repo_path)

    # Generate improvement recommendations
    generate_improvement_recommendations(metrics, repo_path)

    return metrics

def analyze_single_conversation(conv_file):
    """Analyze a single conversation file"""

    conv_metrics = {
        'message_count': 0,
        'agents_used': defaultdict(int),
        'knowledge_gaps': [],
        'common_queries': [],
        'collaborations': [],
        'user_corrections': 0,
        'retry_attempts': 0
    }

    messages = []

    # Read JSONL file
    try:
        with open(conv_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    msg = json.loads(line)
                    messages.append(msg)
                    conv_metrics['message_count'] += 1
    except Exception as e:
        print(f"⚠️  Error reading {conv_file}: {e}")
        return conv_metrics

    # Analyze message patterns
    for i, msg in enumerate(messages):
        if msg.get('type') == 'user':
            # Look for agent invocations
            content = msg.get('message', '')
            agents_mentioned = extract_agent_mentions(content)
            for agent in agents_mentioned:
                conv_metrics['agents_used'][agent] += 1

            # Look for retry patterns
            if is_retry_attempt(content, messages[:i]):
                conv_metrics['retry_attempts'] += 1

            # Look for user corrections
            if is_user_correction(content):
                conv_metrics['user_corrections'] += 1

            # Extract common query patterns
            queries = extract_query_patterns(content)
            conv_metrics['common_queries'].extend(queries)

        elif msg.get('type') == 'assistant':
            # Look for knowledge gaps in responses
            gaps = identify_knowledge_gaps(msg.get('message', ''))
            conv_metrics['knowledge_gaps'].extend(gaps)

    # Identify collaboration patterns
    conv_metrics['collaborations'] = identify_collaboration_patterns(messages)

    return conv_metrics

def extract_agent_mentions(content):
    """Extract mentions of specialist agents from user messages"""

    # Known agent patterns
    agents = [
        'dbt-expert', 'snowflake-expert', 'tableau-expert', 'da-architect',
        'business-context', 'dlthub-expert', 'orchestra-expert', 'prefect-expert',
        'documentation-expert', 'github-sleuth-expert', 'issue-lifecycle-expert'
    ]

    mentioned_agents = []
    content_lower = content.lower()

    for agent in agents:
        if agent in content_lower or agent.replace('-', ' ') in content_lower:
            mentioned_agents.append(agent)

    # Also look for general agent invocation patterns
    if re.search(r'\buse.*agent\b|\bagent.*help\b|\bspecialist\b', content_lower):
        if not mentioned_agents:
            mentioned_agents.append('general-agent-request')

    return mentioned_agents

def is_retry_attempt(content, previous_messages):
    """Detect if this is a retry attempt for a previous request"""

    retry_indicators = [
        'try again', 'retry', 'can you', 'please help', 'still need',
        'not working', 'different approach', 'another way'
    ]

    content_lower = content.lower()
    return any(indicator in content_lower for indicator in retry_indicators)

def is_user_correction(content):
    """Detect if user is correcting a previous assistant response"""

    correction_indicators = [
        'actually', 'no that\'s not', 'incorrect', 'wrong', 'not quite',
        'let me clarify', 'i meant', 'correction', 'instead'
    ]

    content_lower = content.lower()
    return any(indicator in content_lower for indicator in correction_indicators)

def extract_query_patterns(content):
    """Extract common query patterns for analysis"""

    patterns = []
    content_lower = content.lower()

    # Technical patterns
    if 'dbt' in content_lower and ('model' in content_lower or 'test' in content_lower):
        patterns.append('dbt-model-query')

    if 'snowflake' in content_lower and ('performance' in content_lower or 'cost' in content_lower):
        patterns.append('snowflake-optimization-query')

    if 'tableau' in content_lower and ('dashboard' in content_lower or 'report' in content_lower):
        patterns.append('tableau-dashboard-query')

    # Process patterns
    if any(word in content_lower for word in ['workflow', 'process', 'pipeline']):
        patterns.append('workflow-process-query')

    # Architecture patterns
    if any(word in content_lower for word in ['architecture', 'design', 'integration']):
        patterns.append('architecture-design-query')

    return patterns

def identify_knowledge_gaps(assistant_content):
    """Identify potential knowledge gaps in assistant responses"""

    gaps = []
    content_lower = assistant_content.lower()

    # Common gap indicators
    gap_indicators = [
        'i don\'t have specific information',
        'would need more context',
        'not familiar with',
        'outside my knowledge',
        'recommend consulting',
        'might want to check'
    ]

    for indicator in gap_indicators:
        if indicator in content_lower:
            gaps.append('general-knowledge-gap')
            break

    # Specific technical gaps
    if 'need to research' in content_lower or 'look into this' in content_lower:
        gaps.append('technical-research-needed')

    return gaps

def identify_collaboration_patterns(messages):
    """Identify multi-agent collaboration patterns"""

    patterns = []

    # Look for messages mentioning multiple agents
    for msg in messages:
        if msg.get('type') == 'user':
            content = msg.get('message', '').lower()
            agents_in_msg = extract_agent_mentions(content)

            if len(agents_in_msg) > 1:
                patterns.append({
                    'type': 'multi-agent-request',
                    'agents': agents_in_msg,
                    'context': content[:100] + '...' if len(content) > 100 else content
                })

    return patterns

def generate_analysis_report(metrics, repo_path):
    """Generate comprehensive analysis report"""

    output_dir = repo_path / 'knowledge' / 'da-agent-hub' / 'training' / 'analysis-results'
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    username = os.getenv('USER', 'unknown')
    report_file = output_dir / f'{username}_analysis_{timestamp}.md'

    with open(report_file, 'w') as f:
        f.write(f"""# Claude Chat Analysis Report

**Generated**: {metrics['analysis_date']}
**Conversations Analyzed**: {metrics['conversation_count']}
**Total Messages**: {metrics['total_messages']}

## Agent Usage Statistics

""")

        # Agent usage table
        if metrics['agent_usage']:
            f.write("| Agent | Usage Count | Frequency |\n")
            f.write("|-------|-------------|----------|\n")

            total_usage = sum(metrics['agent_usage'].values())
            for agent, count in sorted(metrics['agent_usage'].items(), key=lambda x: x[1], reverse=True):
                frequency = f"{(count/total_usage)*100:.1f}%"
                f.write(f"| {agent} | {count} | {frequency} |\n")

        f.write(f"\n## Common Query Patterns\n\n")

        if metrics['common_queries']:
            for query, count in sorted(metrics['common_queries'].items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"- **{query}**: {count} occurrences\n")

        f.write(f"\n## Knowledge Gaps Identified\n\n")

        if metrics['knowledge_gaps']:
            for gap, count in sorted(metrics['knowledge_gaps'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{gap}**: {count} instances\n")

        f.write(f"\n## Collaboration Patterns\n\n")

        collab_count = len(metrics['collaboration_patterns'])
        f.write(f"Multi-agent collaboration requests: {collab_count}\n\n")

        if metrics['collaboration_patterns']:
            for pattern in metrics['collaboration_patterns'][:5]:  # Show top 5
                agents = ', '.join(pattern['agents'])
                f.write(f"- **Agents**: {agents}\n")
                f.write(f"  **Context**: {pattern['context']}\n\n")

    print(f"📊 Analysis report saved: {report_file}")

def generate_improvement_recommendations(metrics, repo_path):
    """Generate specific improvement recommendations"""

    output_dir = repo_path / 'knowledge' / 'da-agent-hub' / 'training' / 'analysis-results'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    username = os.getenv('USER', 'unknown')
    rec_file = output_dir / f'{username}_recommendations_{timestamp}.md'

    with open(rec_file, 'w') as f:
        f.write(f"""# Agent Improvement Recommendations

**Generated**: {metrics['analysis_date']}
**Based on**: {metrics['conversation_count']} conversations

## High-Priority Improvements

""")

        # Generate recommendations based on usage patterns
        if metrics['agent_usage']:
            most_used = max(metrics['agent_usage'].items(), key=lambda x: x[1])
            f.write(f"### 1. Enhance {most_used[0]} (Most Used Agent)\n")
            f.write(f"- **Usage**: {most_used[1]} invocations\n")
            f.write(f"- **Recommendation**: Prioritize knowledge base updates for this agent\n")
            f.write(f"- **Action**: Create PR to enhance agent with latest patterns\n\n")

        # Knowledge gap recommendations
        if metrics['knowledge_gaps']:
            top_gap = max(metrics['knowledge_gaps'].items(), key=lambda x: x[1])
            f.write(f"### 2. Address Knowledge Gap: {top_gap[0]}\n")
            f.write(f"- **Frequency**: {top_gap[1]} occurrences\n")
            f.write(f"- **Recommendation**: Research and document solutions\n")
            f.write(f"- **Action**: Update relevant agent knowledge base\n\n")

        # Query pattern recommendations
        if metrics['common_queries']:
            top_query = max(metrics['common_queries'].items(), key=lambda x: x[1])
            f.write(f"### 3. Optimize for Common Query: {top_query[0]}\n")
            f.write(f"- **Frequency**: {top_query[1]} requests\n")
            f.write(f"- **Recommendation**: Create specialized response patterns\n")
            f.write(f"- **Action**: Add quick-reference guides to agents\n\n")

        f.write("""## Implementation Suggestions

### Agent File Updates
1. **Document new patterns** discovered in conversations
2. **Add troubleshooting sections** for common issues
3. **Include examples** of successful problem resolution
4. **Update integration guides** for multi-agent workflows

### Knowledge Base Enhancements
1. **Create quick-reference guides** for frequent queries
2. **Document cross-system patterns** for complex issues
3. **Add performance optimization** playbooks
4. **Include team collaboration** best practices

### Process Improvements
1. **Streamline agent selection** for common scenarios
2. **Improve multi-agent coordination** workflows
3. **Create feedback loops** for continuous improvement
4. **Establish metrics tracking** for effectiveness

## Next Steps

1. Review recommendations with team
2. Prioritize improvements based on impact
3. Create separate PRs for agent enhancements
4. Schedule regular analysis to track progress

---

*Use this analysis to create targeted improvements to the DA Agent Hub ADLC system.*
""")

    print(f"💡 Recommendations saved: {rec_file}")

def main():
    """Main analysis function"""

    if len(sys.argv) != 3:
        print("Usage: python3 analyze_chats.py <claude_project_dir> <repo_root>")
        sys.exit(1)

    claude_project_dir = sys.argv[1]
    repo_root = sys.argv[2]

    print("🔬 Starting Claude chat analysis for DA Agent Hub training...")

    try:
        metrics = analyze_conversations(claude_project_dir, repo_root)

        if metrics:
            print(f"✅ Analysis complete!")
            print(f"📊 Processed {metrics['conversation_count']} conversations")
            print(f"💬 Analyzed {metrics['total_messages']} messages")
            print(f"🤖 Found {len(metrics['agent_usage'])} different agents in use")
            print(f"💡 Identified {len(metrics['knowledge_gaps'])} knowledge gap types")
        else:
            print("❌ Analysis failed")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()