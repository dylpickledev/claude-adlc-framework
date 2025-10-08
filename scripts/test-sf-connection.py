#!/usr/bin/env python3
"""Test Snowflake connection with key pair authentication."""

import os
import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load private key
key_path = os.path.expanduser('~/.snowflake/snowflake_rsa_key.p8')
passphrase = os.environ.get('SNOWFLAKE_PRIVATE_KEY_PASSPHRASE', '').encode()

try:
    with open(key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passphrase,
            backend=default_backend()
        )
    print('✅ Private key loaded successfully')
except Exception as e:
    print(f'❌ Failed to load private key: {e}')
    sys.exit(1)

# Try to import snowflake connector
try:
    import snowflake.connector
    print('✅ snowflake-connector-python available')
except ImportError:
    print('❌ snowflake-connector-python not installed')
    sys.exit(1)

# Try to connect
try:
    conn = snowflake.connector.connect(
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        user=os.environ.get('SNOWFLAKE_USER'),
        private_key=private_key,
        database=os.environ.get('SNOWFLAKE_DATABASE', 'ANALYTICS_DW'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA', 'PROD_SALES_DM'),
        warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE', 'TABLEAU_WH'),
        role=os.environ.get('SNOWFLAKE_ROLE', 'BUSINESS_USER')
    )
    print(f'✅ Connected to Snowflake as {conn.user}@{conn.account}')

    # Try a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    version = cursor.fetchone()[0]
    print(f'✅ Snowflake version: {version}')

    cursor.close()
    conn.close()

except Exception as e:
    print(f'❌ Snowflake connection failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('\n✅ All connection tests passed!')
