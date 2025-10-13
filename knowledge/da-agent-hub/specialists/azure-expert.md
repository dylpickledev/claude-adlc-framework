# Azure Expert Agent - Comprehensive Documentation

**Created**: 2025-01-04
**Purpose**: 20+ year Azure enterprise expertise for GraniteRock Data & Analytics infrastructure
**Agent File**: `.claude/agents/azure-expert.md`
**Patterns File**: `.claude/memory/patterns/azure-patterns.md`

## Overview

The Azure Expert Agent provides enterprise-level expertise across all Azure services, with particular focus on cross-cloud integration (Azure + AWS), security best practices, and data analytics infrastructure. This agent is designed to support GraniteRock's hybrid cloud architecture and Data & Analytics platform.

## Research Summary

### Research Coverage (2025 Best Practices)

Comprehensive research was conducted across 9 major Azure expertise domains:

1. **Azure Active Directory / Microsoft Entra ID**
   - OAuth 2.0, OIDC, SAML authentication flows
   - Token configuration (v1.0 vs v2.0 differences)
   - Service principals vs managed identities
   - Enterprise applications and app registrations
   - Conditional access and security policies

2. **Azure Infrastructure & Networking**
   - Virtual Networks (VNets), subnets, NSG best practices
   - Private endpoints vs service endpoints decision matrix
   - Hub-and-spoke network architecture
   - Network security and segmentation strategies
   - Public IP management and security hardening

3. **Azure Compute Services**
   - AKS vs ACI vs Container Apps vs App Service comparison
   - Cost optimization (Reserved Instances, Spot VMs, rightsizing)
   - Auto-scaling and waste elimination strategies
   - Container deployment patterns for 2025

4. **Azure Data & Analytics**
   - Azure Synapse vs Databricks vs Data Factory selection guide
   - Lakehouse architecture best practices
   - Streaming-first vs batch ETL patterns
   - Data engineering security and RBAC implementation

5. **Azure DevOps & CI/CD**
   - Bicep vs Terraform vs ARM templates decision framework
   - CI/CD pipeline best practices with security scanning
   - Environment promotion strategies
   - Azure Verified Modules and reusability patterns

6. **Cross-Cloud Integration (Azure + AWS)**
   - Azure AD OIDC with AWS IAM federation
   - AWS ALB authentication with Azure AD
   - Managed identity to AWS resource access patterns
   - Hybrid cloud architecture and unified management

7. **Security & Compliance**
   - Microsoft Defender for Cloud capabilities
   - Azure Key Vault with RBAC (preferred over access policies)
   - Managed identity best practices
   - Compliance frameworks (HIPAA, SOC 2, ISO 27001, PCI DSS)

8. **Monitoring & Troubleshooting**
   - Azure Monitor and Application Insights optimization
   - Log Analytics workspace design and cost optimization
   - Performance troubleshooting patterns
   - Common error code resolution (401, 403, 500)

9. **Enterprise Integration Patterns**
   - Event Grid vs Event Hub vs Service Bus decision matrix
   - Logic Apps and API Management integration
   - Event-driven architecture patterns
   - Real-world integration examples

### Additional Research Areas

- **Azure Front Door & WAF**: Performance optimization, security configuration, CDN best practices
- **ExpressRoute & VPN Gateway**: Hybrid connectivity patterns, failover architectures, site-to-site VPN
- **Azure Policy & Blueprints**: Governance enforcement, compliance automation, hierarchical policy application
- **Cost Optimization**: Reserved Instances vs Spot VMs, rightsizing strategies, waste identification

## Key Capabilities

### 1. Cross-Cloud Authentication Expertise

**AWS ALB OIDC with Azure AD**
- Complete implementation pattern with Terraform and Bicep examples
- Token validation in backend applications (Python, C#)
- Troubleshooting guide for common OIDC authentication failures
- Security group egress rules and network configuration

**Managed Identity to AWS Resources**
- Azure AD OIDC provider configuration in AWS IAM
- Web Identity Federation with STS
- Short-lived token exchange patterns
- Production-ready Python implementation

### 2. Azure Infrastructure Architecture

**Hub-and-Spoke Network with Private Endpoints**
- Complete Bicep implementation
- Private DNS zone configuration
- VNet peering setup
- NSG rules for private endpoint security

**Key Vault with Managed Identity and RBAC**
- RBAC-based access control (2025 best practice)
- Network security configuration
- Application code examples (C#, Python)
- Automated secret retrieval patterns

### 3. Monitoring & Observability

**Application Insights Custom Telemetry**
- Custom events and metrics tracking
- Kusto query examples for analysis
- Performance monitoring patterns
- Exception tracking and alerting

**Log Analytics Cross-Resource Queries**
- Correlation across multiple resources
- Security pattern detection
- Cost analysis queries
- Performance optimization queries

### 4. Troubleshooting Expertise

**Common Error Resolution**
- HTTP 401: Token validation, authorization header issues
- HTTP 403: RBAC permissions, Key Vault firewall, WAF blocking
- HTTP 500: Backend errors, gateway issues, application failures
- Private endpoint DNS resolution failures
- Managed identity permission denied scenarios
- Data Factory pipeline failures

## Documentation Structure

### Agent Definition (`.claude/agents/azure-expert.md`)

**Sections**:
1. Core Competencies (detailed expertise in 9 domains)
2. Common Anti-Patterns to Avoid
3. Troubleshooting Decision Tree
4. GraniteRock-Specific Azure Integration
5. Learning Resources & Documentation
6. Coordination with Other Agents
7. Agent Behavior Guidelines

**Key Features**:
- 20+ year enterprise Azure expertise
- Production-ready code examples
- Real-world troubleshooting patterns
- Cross-cloud integration focus
- 2025 best practices and deprecation warnings

### Patterns Library (`.claude/memory/patterns/azure-patterns.md`)

**Included Patterns**:
- Cross-Cloud Authentication (Azure AD OIDC with AWS ALB)
- Azure Managed Identity to AWS Resources
- Hub-and-Spoke Network with Private Endpoints
- Key Vault with Managed Identity and RBAC
- Application Insights Custom Telemetry
- Log Analytics Cross-Resource Queries

**Error-Fix Sections**:
- Azure AD OIDC Token Validation Failures
- Private Endpoint DNS Resolution Failures
- Managed Identity Permission Denied (403)
- Azure Data Factory Pipeline Failures

**Architecture Decision Records**:
- Use Azure RBAC Instead of Key Vault Access Policies
- Use Bicep for Azure-Only, Terraform for Multi-Cloud

**Performance Optimization**:
- Azure Front Door with Caching and Compression
- Cost optimization strategies
- Query optimization patterns

## Integration with GraniteRock Infrastructure

### Current Project Support

**AWS ALB OIDC with Azure AD**
- Complete authentication flow documentation
- Terraform configuration examples
- Backend application token validation
- Security group and network configuration
- Troubleshooting guide for common issues

### Recommended Architecture Patterns

**For Data & Analytics Workloads**:
- Azure Synapse for unified data warehousing and analytics
- Azure Data Factory for ETL orchestration
- Managed identities for secure authentication
- Private endpoints for PaaS service security
- Azure Monitor for unified observability

**For Hybrid Connectivity**:
- ExpressRoute for predictable performance and large data transfers
- VPN Gateway as failover for business continuity
- Azure Route Server for dynamic route exchange
- Private DNS zones for hybrid name resolution

**For Security & Compliance**:
- Azure AD as central identity provider across Azure and AWS
- Microsoft Defender for Cloud for unified security management
- Azure Policy for governance enforcement
- Key Vault with RBAC and managed identities

## Usage Guidelines

### When to Use Azure Expert Agent

**Primary Use Cases**:
- Azure infrastructure design and architecture
- Cross-cloud authentication (Azure + AWS)
- Security and compliance implementation
- Performance optimization and troubleshooting
- Cost optimization strategies
- CI/CD pipeline design with Bicep/Terraform

### Coordination with Other Agents

**Escalation Patterns**:
- **AWS-specific configurations**: Coordinate with AWS expert on IAM roles, STS, ALB
- **Data pipeline architecture**: Collaborate with dbt-expert, snowflake-expert
- **Orchestration workflows**: Work with orchestra-expert for multi-cloud workflows
- **Documentation**: Engage documentation-expert for team knowledge sharing
- **Strategic decisions**: Consult da-architect for cross-platform architecture

### Communication Approach

**Problem-Solving Style**:
- Start with Azure native solutions (simpler, better integrated)
- Prefer managed services over IaaS (reduces operational burden)
- Validate security implications before suggesting configurations
- Provide cost estimates where relevant

**Documentation Standards**:
- Follow GraniteRock documentation standards via documentation-expert
- Document resource naming conventions and tagging strategies
- Capture architectural decision records (ADRs)
- Maintain runbooks for common troubleshooting scenarios

## 2025 Best Practices Summary

### Security Best Practices
- Use managed identities instead of client secrets
- Implement Azure RBAC instead of Key Vault access policies
- Use Authorization Code flow with PKCE (not implicit grant)
- Enable Microsoft Defender for Cloud
- Configure private endpoints for PaaS services

### Architecture Best Practices
- Hub-and-spoke network topology
- Private endpoints in hub for shared services
- Managed identities for all Azure-to-Azure authentication
- Azure Policy for governance enforcement
- Distributed tracing in microservices

### Cost Optimization Best Practices
- Reserved Instances for predictable workloads (up to 72% savings)
- Spot VMs for batch processing (up to 90% savings)
- Rightsizing before reserving capacity
- Auto-scaling and auto-shutdown for dev/test
- Azure Advisor weekly review

### DevOps Best Practices
- Bicep for Azure-only deployments
- Terraform for multi-cloud scenarios
- CI/CD pipelines with security scanning and approval gates
- Environment promotion (dev → test → staging → prod)
- Azure Verified Modules for reusability

## Key Deprecations & Migrations

**August 15, 2025**:
- Azure Front Door (classic) → Migrate to Standard/Premium
- Azure CDN from Microsoft (classic) → Migrate to Front Door

**General Deprecations**:
- Key Vault access policies → Migrate to Azure RBAC
- Implicit grant flow → Migrate to Authorization Code with PKCE
- Access policies for Key Vault → Azure RBAC

## Learning Resources

### Primary Sources
- Microsoft Learn (https://learn.microsoft.com)
- Azure Architecture Center
- Microsoft Tech Community
- Azure Updates blog

### Staying Current
- Follow Azure Updates for feature releases
- Review Azure Advisor recommendations weekly
- Monitor Microsoft Tech Community for patterns
- Track Gartner evaluations for Azure services

## Example Scenarios

### Scenario 1: Implement SSO for AWS Application
**Question**: "We need to implement SSO for an application running on AWS ALB using Azure AD"

**Azure Expert Response**:
1. Provide complete AWS ALB OIDC configuration with Azure AD
2. Share Terraform configuration for ALB listener rule
3. Explain token validation in backend application
4. Document troubleshooting steps for common issues
5. Coordinate with AWS expert for IAM configuration

### Scenario 2: Secure Azure SQL Access from App Service
**Question**: "How do we securely connect App Service to Azure SQL without storing credentials?"

**Azure Expert Response**:
1. Recommend managed identity (system-assigned or user-assigned)
2. Provide Bicep configuration for App Service with managed identity
3. Show SQL GRANT commands for managed identity access
4. Share application code examples (C#, Python)
5. Explain how to troubleshoot 403 permission issues

### Scenario 3: Design Hybrid Network Architecture
**Question**: "Design network architecture for Azure VNets connecting to on-premises datacenter"

**Azure Expert Response**:
1. Recommend hub-and-spoke topology
2. Suggest ExpressRoute with VPN Gateway failover
3. Provide Bicep implementation for VNets and peering
4. Design private endpoint strategy for PaaS services
5. Document DNS resolution strategy (Private DNS zones)

## Continuous Improvement

### Agent Enhancement Process
- Track common questions and patterns from usage
- Update agent definition with new Azure features
- Incorporate GraniteRock-specific learnings
- Review Microsoft announcements for deprecations
- Coordinate with other agents for integration improvements

### Feedback Loop
- Document successful troubleshooting patterns
- Capture architectural decision records
- Share learnings with da-architect for strategic decisions
- Update patterns library with new solutions
- Maintain compatibility with GraniteRock standards

## Conclusion

The Azure Expert Agent provides comprehensive enterprise-level Azure expertise covering infrastructure, security, data analytics, and cross-cloud integration. With detailed documentation, real-world code examples, and troubleshooting patterns, this agent supports GraniteRock's hybrid cloud architecture and Data & Analytics platform initiatives.

**Key Strengths**:
- 20+ year enterprise Azure expertise
- Cross-cloud authentication (Azure + AWS)
- Security and compliance focus
- Production-ready code examples
- Comprehensive troubleshooting guides
- 2025 best practices and deprecation awareness

**Primary Use Cases**:
- Azure infrastructure design
- Cross-cloud integration
- Security implementation
- Performance optimization
- Cost optimization
- DevOps and CI/CD

For specific Azure questions or architecture decisions, invoke the azure-expert agent through Claude Code's agent coordination system.
