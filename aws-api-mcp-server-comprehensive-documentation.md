# AWS API MCP Server: Comprehensive Capabilities Documentation

**Version**: 1.0.0
**Package**: `awslabs.aws-api-mcp-server`
**Repository**: https://github.com/awslabs/mcp
**Official Docs**: https://awslabs.github.io/mcp/servers/aws-api-mcp-server/

---

## Executive Summary

The AWS API MCP Server is a Model Context Protocol server that enables AI assistants to interact with AWS services through AWS CLI commands. It provides programmatic access to manage AWS infrastructure while maintaining proper security controls, acting as a bridge between AI assistants and AWS services.

**Key Capabilities**:
- Execute AWS CLI commands with validation and error handling
- Suggest AWS CLI commands based on natural language queries using RAG (Retrieval-Augmented Generation)
- Provide structured guidance for complex AWS tasks (experimental)
- Access latest AWS API features beyond AI model knowledge cutoff dates

**Design Philosophy**: Single-user, local development focused, security-first with IAM-based access control

---

## Available Tools

### 1. call_aws (PRIMARY EXECUTION TOOL)

**Function Signature**: `mcp__aws-api__call_aws`

**Purpose**: Execute AWS CLI commands with validation and proper error handling. This is the PRIMARY tool to use when you are confident about the exact AWS CLI command needed.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cli_command` | string | Yes | The complete AWS CLI command to execute. MUST start with "aws" |
| `max_results` | integer | No | Optional limit for number of results (useful for pagination) |

#### Key Characteristics

**Command Requirements**:
- MUST start with "aws" and follow AWS CLI syntax
- Executed in `us-west-2` region by default (override with `--region`)
- All commands validated before execution
- Working directory: `/var/folders/rc/6zlzjt6d0qdcnxsw8ln5s6j80000gn/T/aws-api-mcp/workdir`
- File paths must use forward slash (/) separator (e.g., `c:/folder/file.txt`)

**Command Restrictions** (CRITICAL):
- ❌ NO bash/zsh pipes (|) or shell operators
- ❌ NO bash/zsh tools (grep, awk, sed, etc.)
- ❌ NO shell redirection operators (>, >>, <)
- ❌ NO command substitution ($())
- ❌ NO shell variables or environment variables
- ❌ NO relative paths - use absolute paths only

**Best Practices**:
- Use most specific service and operation names
- Use working directory for file writes unless user specifies otherwise
- Include `--region` when operating across regions
- Only use filters (`--filters`, `--query`, `--prefix`, `--pattern`) when necessary or explicitly requested

**Common Pitfalls**:
1. Missing required parameters
2. Incorrect parameter value formats
3. Missing `--region` for cross-region operations

#### Returns

CLI execution results with API response data or detailed error messages

#### Example Usage

```python
# List EC2 instances
call_aws(
  cli_command: "aws ec2 describe-instances --region us-east-1 --filters Name=instance-state-name,Values=running"
)

# Create S3 bucket
call_aws(
  cli_command: "aws s3api create-bucket --bucket my-bucket --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2"
)

# Update Lambda function
call_aws(
  cli_command: "aws lambda update-function-configuration --function-name data-processor --memory-size 1024"
)

# With pagination
call_aws(
  cli_command: "aws s3api list-objects-v2 --bucket my-large-bucket",
  max_results: 100
)
```

---

### 2. suggest_aws_commands (DISCOVERY TOOL)

**Function Signature**: `mcp__aws-api__suggest_aws_commands`

**Purpose**: Suggest AWS CLI commands based on natural language queries. This is a FALLBACK tool for when you're uncertain about the exact AWS CLI command needed.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language description of what you want to do in AWS. Max length: 2000 characters |

#### How It Works

Uses **RAG (Retrieval-Augmented Generation)** architecture:
1. **Knowledge Source**: AWS CLI command table documentation
2. **Embeddings**: M3 text embedding model converts queries and CLI commands into dense vectors
3. **Vector Search**: FAISS (Facebook AI Similarity Search) performs nearest neighbor search
4. **Result**: Up to 10 most likely CLI commands with confidence scores

**Technical Implementation** (v1.0.0):
- Converted to remote service (reduced startup time, removed local dependencies)
- Faster response times
- Always uses latest AWS CLI command table

#### When to Use

✅ **Use `suggest_aws_commands` when**:
- Unsure about exact AWS service or operation
- User's request is ambiguous or lacks details
- Need to explore multiple approaches
- Want to provide options to user

❌ **Use `call_aws` instead when**:
- Confident about exact command
- User's request is clear and specific
- Already know exact parameters and syntax
- Task requires immediate execution

#### Query Best Practices

**Query Formulation Guidelines**:
1. Include user's primary goal or intent
2. Specify relevant AWS services if mentioned
3. Include important parameters or conditions
4. Add context about environment or constraints
5. Mention specific requirements or preferences

**Query Granularity** (CRITICAL):
- Each query should be accomplishable by a SINGLE CLI command
- For multi-command requests, break down into individual tasks
- Call tool separately for each specific task

#### Example Queries

**Good Queries** (Single command scope):
```
"List all running EC2 instances in us-east-1 region"
"Get the size of my S3 bucket named 'my-backup-bucket'"
"List all IAM users who have AdministratorAccess policy"
"Create a new S3 bucket with versioning enabled and server-side encryption"
"Update the memory allocation of my Lambda function 'data-processor' to 1024MB"
"Add a new security group rule to allow inbound traffic on port 443"
"Tag all EC2 instances in the 'production' environment with 'Environment=prod'"
```

**Breaking Down Complex Requests**:

❌ Bad: "Set up a new EC2 instance with a security group and attach it to an EBS volume"

✅ Good (Break into 4 separate queries):
1. "Create a new security group with inbound rules for SSH and HTTP"
2. "Create a new EBS volume with 100GB size"
3. "Launch an EC2 instance with t2.micro instance type"
4. "Attach the EBS volume to the EC2 instance"

#### Returns

List of up to 10 AWS CLI commands with:
- The CLI command syntax
- Confidence score for the suggestion
- Required parameters
- Description of what the command does

#### Example Usage

```python
# Discovery phase
suggest_aws_commands(
  query: "List all running EC2 instances in us-east-1 region"
)
# Returns: [
#   {
#     "command": "aws ec2 describe-instances --region us-east-1 --filters Name=instance-state-name,Values=running",
#     "confidence": 0.95,
#     "parameters": ["--region", "--filters"],
#     "description": "Describes EC2 instances filtered by running state"
#   },
#   ...
# ]

# Then execute the best suggestion
call_aws(
  cli_command: "aws ec2 describe-instances --region us-east-1 --filters Name=instance-state-name,Values=running"
)
```

---

### 3. get_execution_plan (EXPERIMENTAL)

**Status**: ⚠️ Experimental - Requires `EXPERIMENTAL_AGENT_SCRIPTS="true"`

**Purpose**: Provides structured, step-by-step guidance for accomplishing complex AWS tasks through agent scripts.

#### What It Does

- Creates reusable workflows for complex AWS operations
- Provides prescriptive guidance for common AWS tasks
- Automates multi-step processes with validated workflows
- Helps navigate complex operations without trial-and-error

#### When to Use

- Complex multi-step AWS operations
- Common patterns that can be reused
- Tasks requiring coordination of multiple AWS services
- Situations where manual exploration would be inefficient

#### Enabling

Set environment variable:
```bash
export EXPERIMENTAL_AGENT_SCRIPTS="true"
```

Or in `.mcp.json`:
```json
{
  "mcpServers": {
    "awslabs.aws-api-mcp-server": {
      "env": {
        "EXPERIMENTAL_AGENT_SCRIPTS": "true"
      }
    }
  }
}
```

**Note**: This is an experimental feature and may change in future releases.

---

## Installation & Configuration

### Installation Methods

#### 1. Using uv (Recommended)
```bash
uvx --from awslabs.aws-api-mcp-server aws-api-mcp-server
```

#### 2. Python (pip)
```bash
pip install awslabs.aws-api-mcp-server
```

#### 3. Docker
```bash
docker pull <docker-hub-url>
```

#### 4. From Source
```bash
git clone https://github.com/awslabs/mcp
cd mcp/src/aws-api-mcp-server
pip install -e .
```

### Configuration for Claude Desktop

**Location**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Example Configuration**:
```json
{
  "mcpServers": {
    "awslabs.aws-api-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-api-mcp-server@latest"],
      "env": {
        "AWS_API_MCP_PROFILE_NAME": "my-aws-profile",
        "AWS_REGION": "us-west-2",
        "READ_OPERATIONS_ONLY": "true",
        "REQUIRE_MUTATION_CONSENT": "true",
        "AWS_API_MCP_WORKING_DIR": "/tmp/aws-mcp-workdir"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Configuration for Claude Code CLI

**Project-level** (`.mcp.json` in project root):
```bash
claude mcp add awslabs.aws-api-mcp-server -s project \
  -e AWS_API_MCP_PROFILE_NAME=my-aws-profile \
  -e AWS_REGION=us-west-2 \
  -e READ_OPERATIONS_ONLY=true \
  -- uvx awslabs.aws-api-mcp-server@latest
```

**Note**: After configuration changes, completely quit and restart Claude Desktop/Code for changes to take effect.

---

## Environment Variables

### Required/Recommended

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_API_MCP_PROFILE_NAME` | None | **RECOMMENDED**: Specifies AWS credentials profile from `~/.aws/credentials` |
| `AWS_REGION` | `us-east-1` | Sets default AWS region for commands |

### Security & Access Control

| Variable | Default | Description |
|----------|---------|-------------|
| `READ_OPERATIONS_ONLY` | `false` | Set to `"true"` to restrict to read-only operations only |
| `REQUIRE_MUTATION_CONSENT` | `false` | Set to `"true"` to require explicit user consent for non-read operations (requires client support) |
| `AWS_API_MCP_WORKING_DIR` | System temp | Sets working directory for file operations |
| `AWS_API_MCP_ALLOW_UNRESTRICTED_LOCAL_FILE_ACCESS` | `false` | Set to `"true"` to enable system-wide file access (⚠️ security risk) |

### Experimental Features

| Variable | Default | Description |
|----------|---------|-------------|
| `EXPERIMENTAL_AGENT_SCRIPTS` | `false` | Set to `"true"` to enable `get_execution_plan` tool |

---

## Credential Management

### AWS Credential Chain (Standard AWS Order)

The server follows standard AWS credential resolution:

1. **Environment Variables**:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (for temporary credentials)

2. **AWS Credentials File**: `~/.aws/credentials`
   ```ini
   [my-profile]
   aws_access_key_id = AKIAIOSFODNN7EXAMPLE
   aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   ```

3. **IAM Role** (if running on EC2 instance)

4. **Container Credentials** (if running in ECS)

### Recommended Approach

**Use Named Profiles** via `AWS_API_MCP_PROFILE_NAME`:

```json
{
  "env": {
    "AWS_API_MCP_PROFILE_NAME": "my-scoped-profile"
  }
}
```

**Best Practices**:
- ✅ Use temporary credentials via AWS SSO (most secure)
- ✅ Use named profiles with scoped-down permissions
- ✅ Rotate credentials regularly
- ❌ Avoid hardcoding access keys in environment variables
- ❌ Avoid using administrator credentials

---

## IAM Permissions & Security

### IAM Best Practices

**Principle of Least Privilege**:
- Always use scoped-down IAM credentials with minimal permissions necessary
- IAM permissions remain the **primary and most reliable security control**
- `READ_OPERATIONS_ONLY` provides an additional layer but IAM is foundational

**Example Scoped-Down Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:List*",
        "s3:Get*",
        "lambda:List*",
        "lambda:Get*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Read-Only Mode

**Enable via Environment Variable**:
```json
{
  "env": {
    "READ_OPERATIONS_ONLY": "true"
  }
}
```

**How It Works**:
- Compares each CLI command against a list of known read-only actions
- Only executes commands found in the allowed list
- Provides additional safety layer on top of IAM

**Important Notes**:
- "Read-Only" refers to AWS API classification, NOT file system
- Read-only API actions can still write to local file system if necessary
- IAM permissions take precedence - this is supplementary protection

**For AWS IAM MCP Server Specifically**:
```json
{
  "args": ["--readonly"]
}
```

### Mutation Consent

**Enable via Environment Variable**:
```json
{
  "env": {
    "REQUIRE_MUTATION_CONSENT": "true"
  }
}
```

**How It Works**:
- Asks explicit user consent before executing any non-read operations
- Uses elicitation (requires client that supports human-in-the-loop)
- Provides interactive confirmation for potentially destructive actions

### Security Warnings

**❌ DO NOT**:
- Connect to data sources with untrusted data (CloudWatch logs with raw user data, user-generated content in databases)
- Use in multi-tenant environments
- Use administrator credentials
- Enable unrestricted file system access without understanding risks

**✅ DO**:
- Use temporary credentials (AWS SSO)
- Use scoped-down IAM policies
- Enable `READ_OPERATIONS_ONLY` when possible
- Enable `REQUIRE_MUTATION_CONSENT` for additional safety
- Use clients that support command validation with human-in-the-loop
- Monitor logs for unexpected operations

---

## Limitations & Design Constraints

### Architecture Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Single-User Only** | NOT designed for multi-tenant environments | Deploy separate instances per user |
| **Local Development Focus** | Intended for STDIO mode as local server | Use for development/automation, not production services |
| **No Built-in Authentication** | HTTP mode has strict security warnings | Use STDIO mode (default), avoid HTTP mode |
| **File System Restrictions** | Restricted to `AWS_API_MCP_WORKING_DIR` by default | Set working directory appropriately, avoid unrestricted access |

### Transport Modes

**STDIO (Default)** - ✅ Recommended:
- Single-user local server
- Runs with user's permissions
- No network exposure
- Secure by design

**HTTP** - ⚠️ Use with extreme caution:
- No built-in authentication
- Security risks if exposed
- Requires additional security layers
- Not recommended for general use

### File System Access

**Default Behavior** (`AWS_API_MCP_ALLOW_UNRESTRICTED_LOCAL_FILE_ACCESS=false`):
- File operations restricted to `AWS_API_MCP_WORKING_DIR`
- Prevents accidental file overwrites
- Safer default

**Unrestricted Access** (`AWS_API_MCP_ALLOW_UNRESTRICTED_LOCAL_FILE_ACCESS=true`):
- ⚠️ Enables system-wide file access
- Risk of unintended file overwrites
- Only enable if absolutely necessary
- Understand security implications

---

## Logging & Monitoring

### Log Configuration

**Automatic Features**:
- Automatic log rotation enabled
- Logs contain operational data:
  - Command executions
  - Error messages
  - Debug information
  - Timestamps
  - Request/response metadata

**Optional CloudWatch Logs Integration**:
- Can send logs to CloudWatch Logs
- Requires appropriate IAM permissions
- Useful for centralized monitoring

### Log Locations

Check documentation for OS-specific log paths.

---

## Version History

### v1.0.0 (Current - October 2025)
- ✨ Converted `suggest_aws_command` tool to remote service
- ⚡ Reduced startup time significantly
- 📦 Removed several local installation dependencies
- 🛠️ Enhanced stability and performance
- 🧪 Added experimental `get_execution_plan` tool

### Pre-1.0.0
- Initial releases with local RAG implementation
- Basic `call_aws` and `suggest_aws_commands` tools

---

## Use Cases & Practical Examples

### Use Case 1: EC2 Instance Management

**Scenario**: List all running EC2 instances in a specific region

**Approach 1 - Direct** (if you know the command):
```python
call_aws(
  cli_command: "aws ec2 describe-instances --region us-east-1 --filters Name=instance-state-name,Values=running"
)
```

**Approach 2 - Discovery** (if unsure):
```python
# Step 1: Get suggestions
suggest_aws_commands(
  query: "List all running EC2 instances in us-east-1 region"
)

# Step 2: Review suggestions and execute best option
call_aws(
  cli_command: "<suggested-command-from-step-1>"
)
```

### Use Case 2: S3 Bucket Creation with Security

**Scenario**: Create a new S3 bucket with versioning and encryption

**Multi-Step Approach**:
```python
# Step 1: Create bucket
call_aws(
  cli_command: "aws s3api create-bucket --bucket my-encrypted-bucket --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2"
)

# Step 2: Enable versioning
call_aws(
  cli_command: "aws s3api put-bucket-versioning --bucket my-encrypted-bucket --versioning-configuration Status=Enabled"
)

# Step 3: Enable server-side encryption
call_aws(
  cli_command: "aws s3api put-bucket-encryption --bucket my-encrypted-bucket --server-side-encryption-configuration '{\"Rules\":[{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\":\"AES256\"}}]}'"
)

# Step 4: Block public access
call_aws(
  cli_command: "aws s3api put-public-access-block --bucket my-encrypted-bucket --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
)
```

### Use Case 3: Lambda Function Management

**Scenario**: Update Lambda function configuration

**Direct Approach**:
```python
# Update memory
call_aws(
  cli_command: "aws lambda update-function-configuration --function-name data-processor --memory-size 1024 --timeout 300 --region us-west-2"
)

# Update environment variables
call_aws(
  cli_command: "aws lambda update-function-configuration --function-name data-processor --environment Variables={DB_HOST=prod-db.example.com,LOG_LEVEL=INFO}"
)
```

### Use Case 4: IAM Security Audit

**Scenario**: Audit IAM users with administrator access

**Discovery and Execution**:
```python
# Step 1: Get suggestions for finding users
suggest_aws_commands(
  query: "List all IAM users in the account"
)

# Step 2: List all users
call_aws(
  cli_command: "aws iam list-users"
)
# Returns: { "Users": [...] }

# Step 3: For each user, check attached policies
# (This would be done programmatically in practice)
call_aws(
  cli_command: "aws iam list-attached-user-policies --user-name alice"
)
call_aws(
  cli_command: "aws iam list-attached-user-policies --user-name bob"
)

# Step 4: Check for AdministratorAccess policy
# Filter results where PolicyName = "AdministratorAccess"
```

### Use Case 5: CloudWatch Alarms for RDS

**Scenario**: Set up CPU utilization alarm for RDS instance

**Discovery First**:
```python
# Step 1: Get command suggestions
suggest_aws_commands(
  query: "Create CloudWatch alarm for high CPU utilization on RDS instance named prod-db"
)

# Step 2: Execute suggested command (example)
call_aws(
  cli_command: "aws cloudwatch put-metric-alarm --alarm-name prod-db-high-cpu --alarm-description 'Alarm when CPU exceeds 80%' --metric-name CPUUtilization --namespace AWS/RDS --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --dimensions Name=DBInstanceIdentifier,Value=prod-db"
)
```

### Use Case 6: VPC Security Group Management

**Scenario**: Add inbound rule to security group

**Discovery and Execution**:
```python
# Step 1: Suggest command
suggest_aws_commands(
  query: "Add a new security group rule to allow inbound HTTPS traffic on port 443 from anywhere"
)

# Step 2: Execute
call_aws(
  cli_command: "aws ec2 authorize-security-group-ingress --group-id sg-0123456789abcdef0 --protocol tcp --port 443 --cidr 0.0.0.0/0"
)
```

### Use Case 7: Bulk Resource Tagging

**Scenario**: Tag all production EC2 instances

**Multi-Step Approach**:
```python
# Step 1: List EC2 instances with specific tag
call_aws(
  cli_command: "aws ec2 describe-instances --filters Name=tag:Environment,Values=production --query 'Reservations[*].Instances[*].InstanceId' --output text"
)
# Returns: i-1234567890abcdef0 i-0987654321fedcba0 ...

# Step 2: Tag instances (example for one instance)
call_aws(
  cli_command: "aws ec2 create-tags --resources i-1234567890abcdef0 --tags Key=Environment,Value=prod Key=CostCenter,Value=engineering"
)
```

### Use Case 8: S3 Lifecycle Policy

**Scenario**: Configure S3 lifecycle policy to move objects to Glacier

**Discovery and Implementation**:
```python
# Step 1: Get suggestions
suggest_aws_commands(
  query: "Create S3 lifecycle policy to move objects older than 90 days to Glacier"
)

# Step 2: Execute (policy in JSON file)
call_aws(
  cli_command: "aws s3api put-bucket-lifecycle-configuration --bucket my-bucket --lifecycle-configuration file:///path/to/lifecycle-policy.json"
)
```

---

## Integration with Agent Workflows

### Decision Framework

```
┌─────────────────────────────────┐
│  Do you know exact AWS command? │
└────────────┬────────────────────┘
             │
       ┌─────┴─────┐
       │           │
      YES         NO
       │           │
       ▼           ▼
┌──────────┐  ┌──────────────────┐
│call_aws  │  │suggest_aws_      │
│(direct)  │  │commands (first)  │
└──────────┘  └────────┬─────────┘
                       │
                       ▼
              ┌────────────────┐
              │ Review options │
              │ Select best    │
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │ call_aws       │
              │ (execute)      │
              └────────────────┘

For complex multi-step operations:
┌─────────────────────────────┐
│ EXPERIMENTAL_AGENT_SCRIPTS  │
│ enabled?                    │
└────────┬────────────────────┘
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌─────────────────┐  ┌──────────────┐
│get_execution_    │  │ Manual multi-│
│plan (suggested)  │  │ step approach│
└─────────────────┘  └──────────────┘
```

### Error Handling Strategy

1. **Validation Errors**:
   - All commands validated before execution
   - Returns detailed error messages
   - Check command syntax, required parameters

2. **Permission Errors**:
   - Verify IAM permissions
   - Check `READ_OPERATIONS_ONLY` setting
   - Ensure AWS credentials are valid

3. **Service Errors**:
   - AWS service-specific errors (e.g., resource not found)
   - Check AWS service quotas/limits
   - Verify resource states

4. **Retry Logic**:
   - Supports retry for transient failures
   - Exponential backoff recommended
   - Check logs for debugging

### Performance Optimization

**Pagination**:
```python
# Use max_results for large result sets
call_aws(
  cli_command: "aws s3api list-objects-v2 --bucket huge-bucket",
  max_results: 1000  # Limit results
)
```

**Regional Endpoints**:
```python
# Use closest region for better performance
call_aws(
  cli_command: "aws ec2 describe-instances --region us-west-2"
)
```

**Result Caching**:
- Cache results when appropriate
- Reduce redundant API calls
- Implement TTL for cached data

---

## Comparison with Other AWS MCP Servers

### AWS API MCP vs AWS Documentation MCP

| Feature | AWS API MCP | AWS Documentation MCP |
|---------|-------------|----------------------|
| **Primary Purpose** | Execute AWS CLI commands, manage infrastructure | Read AWS documentation, search docs, get recommendations |
| **Use Case** | Infrastructure automation, resource management | Learning, reference, finding best practices |
| **Tools** | `call_aws`, `suggest_aws_commands`, `get_execution_plan` | `read_documentation`, `search_documentation`, `recommend` |
| **Requires AWS Credentials** | Yes | No |
| **Can Modify AWS Resources** | Yes | No |
| **When to Use** | Managing AWS infrastructure | Understanding AWS services, finding documentation |

### AWS API MCP vs AWS Serverless MCP

| Feature | AWS API MCP | AWS Serverless MCP |
|---------|-------------|-------------------|
| **Scope** | General AWS service management | Specialized for serverless applications |
| **Services Covered** | All AWS services via CLI | Lambda, API Gateway, Step Functions, EventBridge, SAM |
| **Abstraction Level** | Low-level (CLI commands) | Higher-level (serverless patterns) |
| **Use Case** | Any AWS resource management | Serverless application development |
| **Best Practices** | General AWS best practices | Serverless-specific patterns |

### AWS API MCP vs AWS Cloud Control API MCP

| Feature | AWS API MCP | Cloud Control API MCP |
|---------|-------------|---------------------|
| **API Used** | AWS CLI (service-specific APIs) | AWS Cloud Control API (unified API) |
| **Coverage** | All AWS services | Cloud Control API supported resources |
| **Natural Language** | Via `suggest_aws_commands` (RAG) | Native natural language interface |
| **Command Complexity** | Service-specific CLI syntax | Standardized CRUD operations |

### When to Use AWS API MCP

**Choose AWS API MCP when**:
- Need full power of AWS CLI across any service
- Performing general AWS resource management
- Automating infrastructure tasks
- Cross-service operations
- Service not yet supported by specialized MCP servers
- Need fine-grained control over AWS operations

**Choose Other MCP Servers when**:
- **AWS Documentation MCP**: Learning, research, finding best practices
- **AWS Serverless MCP**: Building serverless applications with guided patterns
- **Cloud Control API MCP**: Unified interface with natural language emphasis

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: "Command must start with 'aws'"

**Cause**: Invalid command format

**Solution**:
```python
# ❌ Wrong
call_aws(cli_command: "ec2 describe-instances")

# ✅ Correct
call_aws(cli_command: "aws ec2 describe-instances")
```

#### Issue 2: Permission Denied Errors

**Cause**: Insufficient IAM permissions

**Solution**:
1. Check IAM policy attached to credentials
2. Verify `READ_OPERATIONS_ONLY` setting if enabled
3. Ensure AWS credentials are valid and not expired

#### Issue 3: Region-Related Errors

**Cause**: Command executed in wrong region

**Solution**:
```python
# Always specify region explicitly
call_aws(
  cli_command: "aws ec2 describe-instances --region us-east-1"
)
```

#### Issue 4: File Path Issues

**Cause**: Relative paths or incorrect path separators

**Solution**:
```python
# ❌ Wrong (relative path, backslashes)
call_aws(cli_command: "aws s3 cp ./file.txt s3://bucket/")

# ✅ Correct (absolute path, forward slashes)
call_aws(cli_command: "aws s3 cp /absolute/path/to/file.txt s3://bucket/")
```

#### Issue 5: No Suggestions Returned

**Cause**: Query too vague or complex

**Solution**:
```python
# ❌ Too vague
suggest_aws_commands(query: "do something with EC2")

# ✅ Specific and actionable
suggest_aws_commands(query: "List all running EC2 instances in us-east-1 region")
```

---

## Best Practices Summary

### Security
- ✅ Use temporary credentials via AWS SSO
- ✅ Use scoped-down IAM policies (least privilege)
- ✅ Enable `READ_OPERATIONS_ONLY` when possible
- ✅ Enable `REQUIRE_MUTATION_CONSENT` for interactive confirmations
- ✅ Use named profiles via `AWS_API_MCP_PROFILE_NAME`
- ✅ Monitor logs for unexpected operations
- ❌ Never use administrator credentials
- ❌ Never connect to untrusted data sources
- ❌ Never use in multi-tenant environments

### Performance
- ✅ Use `max_results` for pagination on large datasets
- ✅ Specify regions explicitly for better performance
- ✅ Cache results when appropriate
- ✅ Use `suggest_aws_commands` to discover optimal commands
- ❌ Avoid unnecessary cross-region calls

### Workflow
- ✅ Use `call_aws` when you know the exact command
- ✅ Use `suggest_aws_commands` for discovery
- ✅ Break complex tasks into single-command queries
- ✅ Validate suggestions before execution
- ✅ Check logs for debugging
- ❌ Don't use shell operators (pipes, redirection)
- ❌ Don't use relative paths

### Maintenance
- ✅ Keep server updated to latest version
- ✅ Review IAM permissions regularly
- ✅ Rotate credentials regularly
- ✅ Monitor log files for issues
- ✅ Test in non-production first

---

## Resources & References

### Official Documentation
- **GitHub Repository**: https://github.com/awslabs/mcp
- **Official Docs**: https://awslabs.github.io/mcp/servers/aws-api-mcp-server/
- **PyPI Package**: https://pypi.org/project/awslabs.aws-api-mcp-server/

### AWS Blogs & Tutorials
- [Introducing AWS MCP Servers (Part 1)](https://aws.amazon.com/blogs/machine-learning/introducing-aws-mcp-servers-for-code-assistants-part-1/)
- [Unlocking the Power of MCP on AWS](https://aws.amazon.com/blogs/machine-learning/unlocking-the-power-of-model-context-protocol-mcp-on-aws/)
- [AWS Cloud Control API MCP Server](https://aws.amazon.com/blogs/devops/introducing-aws-cloud-control-api-mcp-server-natural-language-infrastructure-management-on-aws/)

### Related MCP Servers
- **AWS Documentation MCP**: https://awslabs.github.io/mcp/servers/aws-documentation-mcp-server
- **AWS Serverless MCP**: https://awslabs.github.io/mcp/servers/aws-serverless-mcp-server/
- **AWS IAM MCP**: https://awslabs.github.io/mcp/servers/iam-mcp-server/

### AWS CLI Documentation
- **AWS CLI Command Reference**: https://docs.aws.amazon.com/cli/latest/
- **AWS CLI Configuration**: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
- **IAM Best Practices**: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

---

## Changelog

### v1.0.0 (October 2025)
- Converted `suggest_aws_command` to remote service
- Reduced startup time
- Removed local dependencies
- Enhanced stability and performance
- Added experimental `get_execution_plan` tool

---

**Last Updated**: October 2025
**Maintained By**: AWS Labs
**License**: Apache 2.0 (check repository for details)
