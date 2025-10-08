#!/bin/bash
# Test Snowflake Connection with Key Pair Authentication
# Verifies MCP credentials from 1Password work correctly

set -e

echo "🔍 Testing Snowflake Connection"
echo "================================"
echo ""

# Self-locate and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Load credentials directly from 1Password
echo "🔐 Loading credentials from 1Password..."
export SNOWFLAKE_ACCOUNT=$(op read "op://GRC/DA Agent Hub - Snowflake/account")
export SNOWFLAKE_USER=$(op read "op://GRC/DA Agent Hub - Snowflake/username")
export SNOWFLAKE_AUTH_METHOD=$(op read "op://GRC/DA Agent Hub - Snowflake/auth_method")
export SNOWFLAKE_PRIVATE_KEY_PATH=$(op read "op://GRC/DA Agent Hub - Snowflake/private_key_path")
export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=$(op read "op://GRC/DA Agent Hub - Snowflake/private_key_passphrase")
export SNOWFLAKE_WAREHOUSE=$(op read "op://GRC/DA Agent Hub - Snowflake/warehouse")
export SNOWFLAKE_DATABASE=$(op read "op://GRC/DA Agent Hub - Snowflake/database")
export SNOWFLAKE_SCHEMA=$(op read "op://GRC/DA Agent Hub - Snowflake/schema")
export SNOWFLAKE_ROLE=$(op read "op://GRC/DA Agent Hub - Snowflake/role")

# Verify required env vars
REQUIRED_VARS=(
    "SNOWFLAKE_ACCOUNT"
    "SNOWFLAKE_USER"
    "SNOWFLAKE_AUTH_METHOD"
    "SNOWFLAKE_PRIVATE_KEY_PATH"
    "SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"
    "SNOWFLAKE_WAREHOUSE"
    "SNOWFLAKE_DATABASE"
    "SNOWFLAKE_SCHEMA"
)

echo "📋 Checking environment variables..."
MISSING_VARS=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    else
        if [[ "$var" == *"PASSPHRASE"* ]] || [[ "$var" == *"PASSWORD"* ]]; then
            echo "  ✅ $var: [REDACTED]"
        else
            echo "  ✅ $var: ${!var}"
        fi
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo ""
    echo "❌ Missing required variables:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    exit 1
fi

# Check if private key file exists
echo ""
echo "🔑 Checking private key file..."
if [ ! -f "$SNOWFLAKE_PRIVATE_KEY_PATH" ]; then
    echo "❌ Private key not found: $SNOWFLAKE_PRIVATE_KEY_PATH"
    echo "   Run: ./scripts/setup-snowflake-keypair.sh"
    exit 1
fi
echo "  ✅ Private key found: $SNOWFLAKE_PRIVATE_KEY_PATH"

# Test connection with Python
echo ""
echo "🔌 Testing Snowflake connection..."
python3 - <<'PYTHON_EOF'
import snowflake.connector
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load private key
print("  🔓 Loading private key...")
with open(os.environ['SNOWFLAKE_PRIVATE_KEY_PATH'], 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=os.environ['SNOWFLAKE_PRIVATE_KEY_PASSPHRASE'].encode(),
        backend=default_backend()
    )

# Serialize to PKCS8 format for Snowflake
pkcs8_key = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Connect
print("  🔌 Connecting to Snowflake...")
conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user=os.environ['SNOWFLAKE_USER'],
    private_key=pkcs8_key,
    warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
    database=os.environ['SNOWFLAKE_DATABASE'],
    schema=os.environ['SNOWFLAKE_SCHEMA']
)

# Test query
print("  📊 Running test query...")
cursor = conn.cursor()
cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
result = cursor.fetchone()

print("")
print("✅ CONNECTION SUCCESSFUL!")
print("")
print("Connection details:")
print(f"  User:      {result[0]}")
print(f"  Role:      {result[1]}")
print(f"  Warehouse: {result[2]}")
print(f"  Database:  {result[3]}")
print(f"  Schema:    {result[4]}")

cursor.close()
conn.close()
PYTHON_EOF

# Test result
if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ All tests passed!"
    echo "================================"
    echo ""
    echo "Next steps:"
    echo "  1. Restart Claude Code to activate MCP server"
    echo "  2. Run: ./scripts/post-restart-debug.sh"
    echo ""
else
    echo ""
    echo "================================"
    echo "❌ Connection test failed"
    echo "================================"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Verify public key added to Snowflake user"
    echo "  2. Check 1Password credentials are correct"
    echo "  3. Ensure passphrase matches key encryption"
    echo ""
    exit 1
fi
