from fastapi import Depends, HTTPException, Request, status
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from jose import JWTError, jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID

from ..config.config import config
from ..models.iam import TokenData
from .dependencies.mongo_client import get_db


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak.apps-crc.testing/",
    realm_name="CommonServices",
    client_id="appstore",
    client_secret_key="K5egGlT3AlaQxy3VsG1Q4TB9sHYvX7ME",
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/auth",
    tokenUrl="http://keycloak.apps-crc.testing/realms/CommonServices/protocol/openid-connect/token",
)

def decode_jwt(token: str) -> TokenData:
    """Decode JWT token

    Args:
        token (str): Encoded JWT

    Raises:
        HTTPException: If no secret key is set in app config

    Returns:
        TokenData: Decoded JWT as Pydantic data model
    """
    if config.SECRET_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No secret key set",
        )
    payload = jwt.decode(
        token,
        config.SECRET_KEY,
        algorithms=[config.ALGORITHM],
    )
    return TokenData(
        user_id=payload.get("sub", None),
        name=payload.get("name", None),
        role=payload.get("role", None),
        exp=payload.get("exp", None),
    )

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db),
    csrf: CsrfProtect = Depends(),
) -> TokenData:
    """Get current user from JWT token

    Args:
        request (Request): Incoming HTTP request
        token (str, optional): Encoded JWT. Defaults to Depends(oauth2_scheme).
        db (_type_, optional): MongoDB connection. Defaults to Depends(get_db).
        csrf (CsrfProtect, optional): CSRF Protection. Defaults to Depends().

    Raises:
        CREDENTIALS_EXCEPTION: If token does not provide a user or role
        HTTPException: If token is expired
        CREDENTIALS_EXCEPTION: If token is invalid or CSRF token is invalid
        HTTPException: If token does not reference a valid user

    Returns:
        TokenData: _description_
    """
    db, mongo_client = db
    try:
        csrf.validate_csrf_in_cookies(request)
        token_info = keycloak_openid.introspect(token)

        if not token_info["active"]:
            raise HTTPException(
                status_code=401,
                detail="Invalid token or token expired"
            )
    except (JWTError, CsrfProtectError) as err:
        raise CREDENTIALS_EXCEPTION from err
    # authorisation check done, return token data
    token_data = decode_jwt(token)
    return token_data
