#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <authorization_code>"
  echo ""
  echo "First run: /tmp/get-auth-code.sh to get the URL"
  echo "Then provide the code from the redirect URL"
  exit 1
fi

AUTH_CODE="$1"
TENANT_ID="1d1bbedc-e179-4e6b-a55e-c500085f1eec"
CLIENT_ID="2f1463e8-52ce-499e-9296-4cd125f35f4e"
CLIENT_SECRET="***REMOVED***"
REDIRECT_URI="https://apps.grc-ops.com/oauth2/idpresponse"

echo "==============================================="
echo "Step 2: Exchange Authorization Code for Tokens"
echo "==============================================="
echo ""
echo "Authorization Code: ${AUTH_CODE:0:20}..."
echo "Token Endpoint: https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token"
echo ""
echo "Exchanging code for tokens..."
echo ""

RESPONSE=$(curl -s -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "code=$AUTH_CODE" \
  -d "redirect_uri=$REDIRECT_URI" \
  -d "grant_type=authorization_code" \
  -d "scope=openid email profile")

echo "==============================================="
echo "Response from Azure AD:"
echo "==============================================="
echo ""

# Pretty print JSON if jq is available, otherwise raw
if command -v jq &> /dev/null; then
  echo "$RESPONSE" | jq '.'
else
  echo "$RESPONSE"
fi

echo ""
echo "==============================================="
echo "Analysis:"
echo "==============================================="
echo ""

# Check for error
if echo "$RESPONSE" | grep -q '"error"'; then
  ERROR_CODE=$(echo "$RESPONSE" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
  ERROR_DESC=$(echo "$RESPONSE" | grep -o '"error_description":"[^"]*"' | cut -d'"' -f4)
  
  echo "❌ TOKEN EXCHANGE FAILED"
  echo ""
  echo "Error Code: $ERROR_CODE"
  echo "Description: $ERROR_DESC"
  echo ""
  echo "This is likely the same error ALB is receiving!"
  echo ""
  echo "Next steps:"
  echo "1. Search for '$ERROR_CODE' in Azure documentation"
  echo "2. Check azure-561-troubleshooting-alternatives.md for solutions"
  
elif echo "$RESPONSE" | grep -q '"access_token"'; then
  echo "✅ TOKEN EXCHANGE SUCCESSFUL!"
  echo ""
  echo "Azure AD configuration is working correctly."
  echo "The 561 error is likely caused by:"
  echo "  - ALB configuration issue"
  echo "  - UserInfo endpoint accessibility"
  echo "  - Scope mismatch between ALB and Azure AD"
  echo ""
  echo "Next steps:"
  echo "1. Verify ALB OIDC configuration matches Azure AD"
  echo "2. Test UserInfo endpoint accessibility from ALB"
  echo "3. Check ALB access logs for detailed error"
  
else
  echo "⚠️ UNEXPECTED RESPONSE"
  echo ""
  echo "The response doesn't contain an error or access_token."
  echo "Check the response above for details."
fi

echo ""
echo "==============================================="
