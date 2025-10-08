# Snowflake Key Pair Authentication Setup for MCP

This guide walks through setting up key pair authentication for the Snowflake MCP server, which is required when your Snowflake account enforces network policy restrictions.

## Why Key Pair Authentication?

**Problem**: Your Snowflake account (FC41459) returns error: "Network policy is required"
- This means password/PAT authentication is blocked by account security policy
- Account requires OAuth or key pair authentication

**Solution**: RSA key pair authentication
- ✅ Bypasses network policy restriction
- ✅ More secure than password-based auth
- ✅ Recommended by Snowflake for programmatic access
- ✅ No token rotation needed
- ✅ Works with MCP server

## Prerequisites

- 1Password CLI installed: `brew install --cask 1password-cli`
- Access to Snowflake account with ability to modify your user
- OpenSSL installed (comes with macOS)

## Step-by-Step Setup

### 1. Generate Key Pair and Store in 1Password

Run the automated setup script:

```bash
./scripts/setup-snowflake-keypair.sh
```

This script will:
1. Create `~/.snowflake/` directory with secure permissions
2. Generate encrypted RSA private key (you'll set passphrase)
3. Generate public key
4. Display public key for Snowflake
5. Update 1Password credentials automatically

**What gets stored where:**
- Private key: `~/.snowflake/snowflake_rsa_key.p8` (encrypted, 600 permissions)
- Public key: `~/.snowflake/snowflake_rsa_key.pub` (644 permissions)
- Passphrase: 1Password vault (encrypted)
- Key paths: 1Password vault (for MCP launcher)

### 2. Add Public Key to Snowflake

The setup script will display the public key. Copy it and run in Snowflake:

```sql
-- Connect to Snowflake as ACCOUNTADMIN or as your user
USE ROLE ACCOUNTADMIN;

-- Add public key to your user
ALTER USER CLAUDE SET RSA_PUBLIC_KEY='MIIBIjANBgkq...your-key-here...';

-- Verify it's set
DESC USER CLAUDE;
```

Look for `RSA_PUBLIC_KEY_FP` in the output - this confirms the key is registered.

### 3. Test Connection

Test that everything works before restarting Claude:

```bash
./scripts/test-snowflake-connection.sh
```

**Expected output:**
```
✅ CONNECTION SUCCESSFUL!

Connection details:
  User:      CLAUDE
  Role:      DEVELOPER
  Warehouse: TABLEAU_WH
  Database:  ANALYTICS_DW
  Schema:    PROD_SALES_DM
```

### 4. Restart Claude Code

The MCP server will now use key pair authentication automatically:

1. Quit Claude Code completely
2. Restart Claude Code
3. Verify MCP loaded: `./scripts/post-restart-debug.sh`

## How It Works

### 1Password Integration

The setup script updates your `Snowflake MCP Credentials` 1Password item with:

```
auth_method: private_key
private_key_path: /Users/YourUser/.snowflake/snowflake_rsa_key.p8
private_key_passphrase: [your-passphrase-encrypted]
```

### MCP Launcher Flow

1. `scripts/load-secrets.sh` loads credentials from 1Password
2. `scripts/launch-snowflake-mcp.sh` detects `auth_method=private_key`
3. Injects key path + passphrase into temp config
4. Launches Snowflake MCP with key pair auth
5. Snowflake validates public key matches your user

### Security Model

**Private Key Protection:**
- Encrypted with AES-256 using your passphrase
- Stored locally with 600 permissions (owner read/write only)
- Passphrase stored in 1Password vault (encrypted at rest)

**Authentication Flow:**
```
MCP Server → Load private key from ~/.snowflake/
          → Decrypt with passphrase from 1Password
          → Sign authentication request
          → Snowflake validates with stored public key
          → Connection established
```

**Key Benefits:**
- Private key never transmitted over network
- Passphrase required to use key (2-factor security)
- Public key in Snowflake is useless without private key
- Key rotation is simple (regenerate and update Snowflake)

## Troubleshooting

### "Private key not found" Error

```bash
# Verify key exists
ls -la ~/.snowflake/

# Re-run setup if missing
./scripts/setup-snowflake-keypair.sh
```

### "Failed to decrypt private key" Error

- Passphrase in 1Password doesn't match key encryption
- Update 1Password with correct passphrase:

```bash
op item edit "Snowflake MCP Credentials" \
  "private_key_passphrase[password]=correct-passphrase" \
  --vault "GraniteRock"
```

### "Invalid public key" Error from Snowflake

```sql
-- Check public key is registered
DESC USER CLAUDE;

-- Remove and re-add if needed
ALTER USER CLAUDE UNSET RSA_PUBLIC_KEY;
ALTER USER CLAUDE SET RSA_PUBLIC_KEY='new-key-here';
```

### Connection Still Uses Password

- Check 1Password has `auth_method=private_key`
- Verify launcher script detects key pair mode
- Clear MCP cache and restart Claude

## Key Rotation

To rotate keys (recommended every 90 days):

```bash
# Generate new key pair
./scripts/setup-snowflake-keypair.sh

# Update Snowflake (use new public key from script output)
ALTER USER CLAUDE SET RSA_PUBLIC_KEY='new-key';

# Test connection
./scripts/test-snowflake-connection.sh

# Restart Claude Code
```

Old keys can be kept for a transition period, then deleted:

```bash
# After confirming new key works
rm ~/.snowflake/snowflake_rsa_key.p8.old
rm ~/.snowflake/snowflake_rsa_key.pub.old
```

## Security Best Practices

1. **Never commit private keys to git** - `.gitignore` already excludes `~/.snowflake/`
2. **Use strong passphrase** - Minimum 16 characters, mix of types
3. **Rotate keys regularly** - Every 90 days recommended
4. **Audit key usage** - Check Snowflake login history periodically
5. **Revoke unused keys** - Remove old public keys from Snowflake user

## Additional Resources

- [Snowflake Key Pair Authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth)
- [Python Connector Key Pair Auth](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#key-pair-authentication)
- [1Password CLI Reference](https://developer.1password.com/docs/cli/reference/)
