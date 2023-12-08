# https://developers.redhat.com/blog/2020/01/29/api-login-and-jwt-token-generation-using-keycloak#test_your_new_client

# generate a token from frontend public client
TOKEN_FRONTEND=$(curl -L -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Accept: application/json' \
    --data-urlencode 'client_id=test-app-frontend' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode 'username=okaiyong' \
    --data-urlencode 'password=1' \
    'http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/token' \
    | jq -r '.access_token')

echo $TOKEN_FRONTEND

# call a backend api with this token; the token contains audience aud based on backend client
curl -X GET \
    -H "Authorization: Bearer ${TOKEN_FRONTEND}" \
    "http://127.0.0.1:8000"
