#!/bin/bash
# Snowflake Key Pair Authentication Setup
# Generates RSA key pair and stores in 1Password for MCP authentication

set -e

echo "🔐 Snowflake Key Pair Authentication Setup"
echo "=========================================="
echo ""

# Configuration
KEY_DIR="$HOME/.snowflake"
PRIVATE_KEY="$KEY_DIR/snowflake_rsa_key.p8"
PUBLIC_KEY="$KEY_DIR/snowflake_rsa_key.pub"
OP_ITEM="DA Agent Hub - Snowflake"

# Create key directory
echo "📁 Creating key directory: $KEY_DIR"
mkdir -p "$KEY_DIR"
chmod 700 "$KEY_DIR"

# Check if keys already exist
if [ -f "$PRIVATE_KEY" ]; then
    echo "⚠️  Keys already exist at $PRIVATE_KEY"
    read -p "Overwrite existing keys? (y/N): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Aborting. Using existing keys."
        exit 1
    fi
    echo "🗑️  Removing old keys..."
    rm -f "$PRIVATE_KEY" "$PUBLIC_KEY"
fi

# Prompt for passphrase
echo ""
echo "🔑 Enter passphrase to encrypt private key:"
echo "   (Store this in 1Password - you'll need it for authentication)"
read -s -p "Passphrase: " PASSPHRASE
echo ""
read -s -p "Confirm passphrase: " PASSPHRASE_CONFIRM
echo ""

if [ "$PASSPHRASE" != "$PASSPHRASE_CONFIRM" ]; then
    echo "❌ Passphrases don't match!"
    exit 1
fi

if [ -z "$PASSPHRASE" ]; then
    echo "❌ Passphrase cannot be empty!"
    exit 1
fi

# Generate private key
echo ""
echo "🔐 Generating encrypted RSA private key..."
openssl genrsa 2048 2>/dev/null | \
    openssl pkcs8 -topk8 -inform PEM -out "$PRIVATE_KEY" \
    -v2 aes256 -passout "pass:$PASSPHRASE"

chmod 600 "$PRIVATE_KEY"
echo "✅ Private key: $PRIVATE_KEY"

# Generate public key
echo "🔓 Generating RSA public key..."
openssl rsa -in "$PRIVATE_KEY" -pubout -out "$PUBLIC_KEY" \
    -passin "pass:$PASSPHRASE" 2>/dev/null

chmod 644 "$PUBLIC_KEY"
echo "✅ Public key: $PUBLIC_KEY"

# Extract public key for Snowflake (remove headers/footers)
PUBLIC_KEY_SNOWFLAKE=$(grep -v "BEGIN PUBLIC KEY" "$PUBLIC_KEY" | \
                       grep -v "END PUBLIC KEY" | \
                       tr -d '\n')

# Display public key
echo ""
echo "=========================================="
echo "📋 PUBLIC KEY FOR SNOWFLAKE"
echo "=========================================="
echo ""
echo "Copy this value (without quotes) and run in Snowflake as ACCOUNTADMIN:"
echo ""
echo "ALTER USER CLAUDE SET RSA_PUBLIC_KEY='$PUBLIC_KEY_SNOWFLAKE';"
echo ""
echo "=========================================="
echo ""

# Ask user to confirm Snowflake setup
read -p "Have you added the public key to Snowflake? (y/N): " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Please add the public key to Snowflake before continuing."
    echo "   Keys saved at: $KEY_DIR"
    echo "   Run this script again when ready to update 1Password."
    exit 0
fi

# Update 1Password
echo ""
echo "🔐 Updating 1Password credentials..."
echo "   Item: $OP_ITEM"

# Check if op CLI is available
if ! command -v op &> /dev/null; then
    echo "❌ 1Password CLI (op) not found!"
    echo "   Install: brew install --cask 1password-cli"
    exit 1
fi

# Update 1Password item
op item edit "$OP_ITEM" \
    "auth_method[text]=private_key" \
    "private_key_path[text]=$PRIVATE_KEY" \
    "private_key_passphrase[password]=$PASSPHRASE" \
    --vault "GRC"

echo "✅ 1Password updated successfully!"

# Update MCP config template
CONFIG_FILE="config/snowflake_tools_config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    echo ""
    echo "📝 Updating MCP config template..."

    # Backup original
    cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"

    # Update auth_method default
    sed -i '' 's/auth_method: "${SNOWFLAKE_AUTH_METHOD}"/auth_method: "private_key"/' "$CONFIG_FILE"

    echo "✅ Config updated (backup: ${CONFIG_FILE}.bak)"
fi

# Summary
echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Claude Code to reload credentials"
echo "2. Test connection: ./scripts/test-snowflake-connection.sh"
echo ""
echo "Key locations:"
echo "  Private key: $PRIVATE_KEY"
echo "  Public key:  $PUBLIC_KEY"
echo "  1Password:   $OP_ITEM"
echo ""
echo "Security notes:"
echo "  - Private key is encrypted with your passphrase"
echo "  - Passphrase stored in 1Password vault"
echo "  - Keys have restrictive permissions (600/644)"
echo ""
