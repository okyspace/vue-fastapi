from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak.apps-crc.testing/",
    realm_name="CommonServices",
    client_id="appstore",
    client_secret_key="K5egGlT3AlaQxy3VsG1Q4TB9sHYvX7ME",
)

app = FastAPI()

# OAuth2 Authorization Code Bearer
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://keycloak.apps-crc.testing/auth/realms/CommonServices/protocol/openid-connect/auth",
    tokenUrl="http://keycloak.apps-crc.testing/auth/realms/CommonServices/protocol/openid-connect/token",
)

@app.get("/")
async def home(token: str = Depends(oauth2_scheme)):
    # Validate the token using Keycloak

    # Your secured endpoint logic here
    return {"message": "This is a secured endpoint"}

@app.get("/students")
async def get_students(token: str = Depends(oauth2_scheme)):
    # Validate the token using Keycloak
    token_info = keycloak_openid.introspect(token)

    print("get students")

    if not token_info["active"]:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Your secured endpoint logic here
    return {"message": "This is a secured endpoint"}
