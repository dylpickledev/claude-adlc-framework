# Azure Quick Reference Guide

**Purpose**: Fast lookup for common Azure patterns, commands, and troubleshooting
**Audience**: GraniteRock Data & Analytics team
**Last Updated**: 2025-01-04

## Quick Decision Trees

### When to Use Which Azure Service

#### Container Hosting
```
Need Kubernetes control? → AKS
Need serverless microservices? → Container Apps
Need simple container deployment? → Container Instances
Need managed web app hosting? → App Service
```

#### Data Platform
```
Need unified data warehouse + big data? → Azure Synapse
Need advanced ML and Spark processing? → Azure Databricks
Need data integration and ETL? → Azure Data Factory
Need real-time analytics? → Azure Stream Analytics
```

#### Messaging
```
Need discrete event notifications? → Event Grid
Need high-throughput telemetry? → Event Hubs
Need reliable message queuing? → Service Bus
```

#### Infrastructure as Code
```
Azure-only deployment? → Bicep
Multi-cloud deployment? → Terraform
Legacy templates? → ARM (migrate to Bicep)
```

### Authentication Decision Tree
```
Azure resource to Azure resource? → Managed Identity
Azure AD user authentication? → OAuth 2.0 + OIDC
Cross-cloud (Azure to AWS)? → OIDC + IAM Web Identity
Legacy application? → Service Principal (migrate to managed identity)
```

## Common Commands

### Azure CLI - Resource Management
```bash
# Login
az login
az account list --output table
az account set --subscription "subscription-name"

# Resource Groups
az group create --name rg-prod --location eastus
az group list --output table
az group delete --name rg-dev --yes --no-wait

# View resources
az resource list --resource-group rg-prod --output table
az resource show --ids /subscriptions/.../resourceGroups/rg-prod/providers/Microsoft.KeyVault/vaults/kv-name
```

### Azure CLI - Networking
```bash
# VNet and Subnets
az network vnet create --resource-group rg-prod --name vnet-hub --address-prefix 10.0.0.0/16
az network vnet subnet create --resource-group rg-prod --vnet-name vnet-hub --name snet-app --address-prefix 10.0.1.0/24

# NSG Rules
az network nsg rule create \
  --resource-group rg-prod \
  --nsg-name nsg-app \
  --name allow-https \
  --priority 100 \
  --source-address-prefixes '*' \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp

# Private Endpoints
az network private-endpoint create \
  --resource-group rg-prod \
  --name pe-sql \
  --vnet-name vnet-hub \
  --subnet snet-private-endpoints \
  --private-connection-resource-id /subscriptions/.../Microsoft.Sql/servers/sqlserver \
  --group-id sqlServer \
  --connection-name sql-connection
```

### Azure CLI - Identity & Access
```bash
# Managed Identity
az identity create --name id-app-prod --resource-group rg-prod
az identity show --name id-app-prod --resource-group rg-prod --query principalId -o tsv

# RBAC Assignments
az role assignment create \
  --assignee <principal-id> \
  --role "Key Vault Secrets User" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<kv>

az role assignment list --assignee <principal-id> --output table
```

### Azure CLI - Key Vault
```bash
# Create Key Vault with RBAC
az keyvault create \
  --name kv-app-prod \
  --resource-group rg-prod \
  --location eastus \
  --enable-rbac-authorization true \
  --enable-soft-delete true \
  --retention-days 90 \
  --enable-purge-protection true

# Secrets
az keyvault secret set --vault-name kv-app-prod --name db-password --value "SecurePassword123"
az keyvault secret show --vault-name kv-app-prod --name db-password --query value -o tsv
az keyvault secret list --vault-name kv-app-prod --output table
```

### Azure CLI - Monitoring
```bash
# Enable diagnostic settings
az monitor diagnostic-settings create \
  --name send-to-log-analytics \
  --resource /subscriptions/.../resourceGroups/rg-prod/providers/Microsoft.KeyVault/vaults/kv-app \
  --workspace /subscriptions/.../resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/log-prod \
  --logs '[{"category": "AuditEvent", "enabled": true}]' \
  --metrics '[{"category": "AllMetrics", "enabled": true}]'

# Query Log Analytics
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "AzureDiagnostics | where TimeGenerated > ago(1h) | take 10"
```

## Common Kusto Queries

### Application Insights
```kql
// Slow requests (>1 second)
requests
| where duration > 1000
| summarize
    count(),
    p50=percentile(duration, 50),
    p95=percentile(duration, 95),
    p99=percentile(duration, 99)
  by operation_Name
| order by p99 desc

// Failed requests
requests
| where success == false
| summarize failure_count = count() by resultCode, operation_Name
| order by failure_count desc

// Dependency failures
dependencies
| where success == false
| summarize failure_count = count() by type, name, resultCode
| order by failure_count desc

// Exceptions
exceptions
| summarize exception_count = count() by type, outerMessage
| order by exception_count desc
```

### Key Vault Audit
```kql
// Key Vault access patterns
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.KEYVAULT"
| where OperationName == "SecretGet"
| summarize access_count = count() by CallerIPAddress, bin(TimeGenerated, 1h)
| order by access_count desc

// Key Vault failures
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.KEYVAULT"
| where ResultSignature != "OK"
| summarize failure_count = count() by OperationName, ResultSignature
| order by failure_count desc
```

### Network NSG Flow Logs
```kql
// Top blocked connections
AzureNetworkAnalytics_CL
| where FlowStatus_s == "D"  // Denied
| summarize blocked_count = count() by
    SrcIP_s,
    DestIP_s,
    DestPort_d,
    L7Protocol_s
| order by blocked_count desc
| take 20
```

## Quick Troubleshooting

### HTTP 401 Unauthorized
```
1. Check Authorization header present
2. Verify token not expired (decode JWT at jwt.io)
3. Validate audience claim matches resource
4. Confirm token signature (kid matches signing key)
5. For Key Vault: Check token generation before request
```

### HTTP 403 Forbidden
```
1. Check RBAC role assignments (az role assignment list)
2. Verify correct principal ID used (not application ID)
3. Check Key Vault firewall rules (if applicable)
4. Confirm WAF not blocking request
5. Wait 5-10 minutes for RBAC replication
```

### HTTP 500 Internal Server Error
```
1. Check Azure Service Health for outages
2. Review Application Insights for exceptions
3. Check backend health in Application Gateway
4. Open Azure support ticket (shouldn't occur)
```

### Cannot Resolve Private Endpoint
```
1. Verify Private DNS Zone linked to VNet
2. Check custom DNS forwarding to 168.63.129.16
3. Enable network policies on subnet
4. Test: nslookup <service>.privatelink.<service>.windows.net
5. Confirm A record in Private DNS Zone
```

### Managed Identity 403 Error
```
1. Get principal ID: az identity show --query principalId
2. Verify RBAC assignment: az role assignment list --assignee <principal-id>
3. Check Key Vault RBAC enabled: az keyvault show --query properties.enableRbacAuthorization
4. Wait 5-10 minutes for RBAC propagation
5. Review network restrictions (Key Vault firewall)
```

## Cost Optimization Quick Wins

### Immediate Actions
```
1. Review Azure Advisor cost recommendations
2. Implement auto-shutdown for dev/test VMs
3. Rightsize VMs (check last 30 days utilization)
4. Delete unused resources (orphaned disks, NICs, IPs)
5. Enable soft delete on resources to prevent accidental loss
```

### Reserved Instances Strategy
```
For VMs running 24/7:
- Predictable workload → 3-year RI (72% savings)
- Some variability → 1-year RI (up to 40% savings)
- Region-flexible RIs preferred

For dev/test:
- Spot VMs (90% savings, can be evicted)
- Auto-shutdown outside business hours
- B-series burstable VMs
```

### Data Storage Optimization
```
1. ADLS Gen2: Move old data to Archive tier
2. Azure SQL: Use elastic pools for multiple databases
3. Cosmos DB: Use serverless for variable workloads
4. Blob Storage: Implement lifecycle policies
5. Log Analytics: Use Basic Logs for debug/audit data
```

## Security Hardening Checklist

### Identity & Access
- [ ] Enable managed identities (eliminate secrets)
- [ ] Use Azure RBAC instead of access policies
- [ ] Implement conditional access policies
- [ ] Enable MFA for all admin accounts
- [ ] Review RBAC assignments quarterly

### Network Security
- [ ] Use private endpoints for PaaS services
- [ ] Implement NSG rules at subnet level
- [ ] Disable public access where possible
- [ ] Configure Key Vault firewall
- [ ] Use Azure Firewall for centralized control

### Data Protection
- [ ] Enable encryption at rest (all services)
- [ ] Use TLS 1.2+ for all connections
- [ ] Enable soft delete on Key Vault, Storage
- [ ] Implement backup and disaster recovery
- [ ] Enable diagnostic logging

### Monitoring & Compliance
- [ ] Enable Microsoft Defender for Cloud
- [ ] Configure Azure Policy for governance
- [ ] Send logs to Log Analytics workspace
- [ ] Set up alerts for security events
- [ ] Regular compliance dashboard review

## Bicep Quick Patterns

### Key Vault with RBAC
```bicep
resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
  }
}
```

### App Service with Managed Identity
```bicep
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-app'
  location: location
}

resource app 'Microsoft.Web/sites@2023-01-01' = {
  name: 'app-${uniqueString(resourceGroup().id)}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      minTlsVersion: '1.2'
      keyVaultReferenceIdentity: identity.id
    }
  }
}
```

### Private Endpoint
```bicep
resource pe 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-sql'
  location: location
  properties: {
    subnet: { id: subnet.id }
    privateLinkServiceConnections: [
      {
        name: 'sql-connection'
        properties: {
          privateLinkServiceId: sqlServer.id
          groupIds: [ 'sqlServer' ]
        }
      }
    ]
  }
}
```

## Python Quick Patterns

### Managed Identity Authentication
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
kv_client = SecretClient(
    vault_url="https://kv-name.vault.azure.net/",
    credential=credential
)
secret = kv_client.get_secret("db-password")
```

### Application Insights Logging
```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=<key>'
))

logger.info('Event', extra={
    'custom_dimensions': {
        'user_id': 'user123',
        'action': 'purchase'
    }
})
```

## Common Anti-Patterns to Avoid

### Security
- ❌ Using client secrets instead of managed identities
- ❌ Implicit grant flow for SPAs (use Auth Code + PKCE)
- ❌ Broad permissions (Contributor at subscription level)
- ❌ Sharing credentials across environments
- ❌ Storing secrets in code or config files

### Networking
- ❌ Overlapping VNet address spaces
- ❌ Single large subnet for entire VNet
- ❌ Not planning for address space growth
- ❌ Excessive NSG rules (use ASGs instead)
- ❌ Missing network policies for private endpoints

### Cost
- ❌ Reserving VMs before rightsizing
- ❌ Running production on pay-as-you-go
- ❌ No auto-shutdown for dev/test
- ❌ Over-provisioning storage tiers
- ❌ Ignoring Azure Advisor recommendations

### Architecture
- ❌ Cross-region Log Analytics queries in prod
- ❌ Using access policies instead of RBAC for Key Vault
- ❌ Allowlist approach to Azure Policy
- ❌ No retry logic for transient failures
- ❌ Missing distributed tracing in microservices

## Resources

### Documentation
- Microsoft Learn: https://learn.microsoft.com
- Azure Architecture Center: https://learn.microsoft.com/azure/architecture
- Azure Updates: https://azure.microsoft.com/updates

### Tools
- Azure CLI: https://learn.microsoft.com/cli/azure
- Azure PowerShell: https://learn.microsoft.com/powershell/azure
- Bicep: https://learn.microsoft.com/azure/azure-resource-manager/bicep
- VS Code Azure Extensions

### Pricing
- Azure Pricing Calculator: https://azure.microsoft.com/pricing/calculator
- Azure Advisor: https://portal.azure.com/#blade/Microsoft_Azure_Expert/AdvisorMenuBlade
- Cost Management: https://portal.azure.com/#blade/Microsoft_Azure_CostManagement

---

For detailed patterns and complete examples, see:
- Agent definition: `.claude/agents/azure-expert.md`
- Patterns library: `.claude/memory/patterns/azure-patterns.md`
- Full documentation: `knowledge/da-agent-hub/azure-expert-documentation.md`
