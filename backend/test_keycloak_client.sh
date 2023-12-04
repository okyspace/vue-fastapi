# https://developers.redhat.com/blog/2020/01/29/api-login-and-jwt-token-generation-using-keycloak#test_your_new_client

echo "Test Keycloak Client"
curl -L -X POST \
    'http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/token' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'client_id=appstore' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode 'client_secret=K5egGlT3AlaQxy3VsG1Q4TB9sHYvX7ME' \
    --data-urlencode 'scope=openid' \
    --data-urlencode 'username=okaiyong' \
    --data-urlencode 'password=1' \


# https://nieldw.medium.com/using-curl-to-authenticate-with-jwt-bearer-tokens-55b7fac506bd

echo "Get token"
TOKEN=$(curl -L -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Accept: application/json' \
    --data-urlencode 'client_id=appstore' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode 'client_secret=K5egGlT3AlaQxy3VsG1Q4TB9sHYvX7ME' \
    --data-urlencode 'scope=openid' \
    --data-urlencode 'username=okaiyong' \
    --data-urlencode 'password=1' \
    'http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/token' \
    | jq -r '.access_token')

echo "Test secured endpoint"
curl \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer ${TOKEN}" \
    http://127.0.0.1:8000
