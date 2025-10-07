#!/bin/bash

TENANT_ID="1d1bbedc-e179-4e6b-a55e-c500085f1eec"
CLIENT_ID="2f1463e8-52ce-499e-9296-4cd125f35f4e"
REDIRECT_URI="https://apps.grc-ops.com/oauth2/idpresponse"

AUTH_URL="https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/authorize?client_id=$CLIENT_ID&response_type=code&redirect_uri=$REDIRECT_URI&scope=openid%20email%20profile"

echo "==============================================="
echo "Step 1: Get Authorization Code"
echo "==============================================="
echo ""
echo "Open this URL in your browser:"
echo ""
echo "$AUTH_URL"
echo ""
echo "After you authenticate, you'll be redirected to:"
echo "https://apps.grc-ops.com/oauth2/idpresponse?code=XXXXX&state=XXXXX"
echo ""
echo "Copy the entire 'code' parameter value (the long string after code=)"
echo "It will look something like: 0.AXwA3L4b..."
echo ""
echo "==============================================="
