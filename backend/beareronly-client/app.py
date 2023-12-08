# https://python-keycloak.readthedocs.io/en/latest/
# https://pypi.org/project/python-keycloak/

from fastapi import FastAPI, Depends, HTTPException, Security, status
from pydantic import Json
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

app = FastAPI()

# Create a KeycloakOpenID instance for the Bearer-only client
keycloak_bearer_only = KeycloakOpenID(
    server_url="http://keycloak.apps-crc.testing/",
    realm_name="CommonServices",
    client_id="test-app-backend",
    client_secret_key="AGZWTYZVj7ZZucUNrRpK2tQiLlBSfT6o",
    verify=True
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/auth",
    tokenUrl="http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/token"
)

async def get_idp_public_key():
    '''
    Obtain the public key of the keycloak
    '''
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_bearer_only.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    '''
    Return identity if valid token
    '''
    try:
        return keycloak_bearer_only.decode_token(token, key=await get_idp_public_key())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(identity: Json):
    return identity['name']

def get_current_user_role(identity: Json):
    return identity['client_roles']

@app.get("/")
async def home(
    identity: Json = Depends(get_auth)
) -> str:
    try:
        print(identity)
        name = get_current_user(identity)
        roles = get_current_user_role(identity)
        return f"{name} has logged in with roles {roles}"
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}") from e
