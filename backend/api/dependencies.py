import logging
from typing import Any

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from backend.core.config import settings
from backend.core.messages import ErrorMessages, LogMessages
from backend.services.auth_service import AuthService
from backend.services.session_manager import SessionManager
from backend.services.project_service import ProjectService

logger = logging.getLogger(__name__)

security = HTTPBearer()


SUPABASE_BASE_URL = settings.SUPABASE_URL
JWKS_URL = f"{SUPABASE_BASE_URL}/auth/v1/.well-known/jwks.json"
AUDIENCE = "authenticated"

_jwks_cache = None

def get_jwks():
    """Fetches public keys from Supabase JWKS endpoint"""
    global _jwks_cache
    if _jwks_cache is None:
        try:
            response = requests.get(JWKS_URL, timeout=5)
            response.raise_for_status()
            _jwks_cache = response.json()
        except Exception as e:
            logger.error(f"Could not fetch JWKS: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service unavailable"
            )
    return _jwks_cache

def validate_jwt_token(token: str) -> str:
    """Verifies the ES256 JWT against Supabase Public Keys"""
    try:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        alg = header.get("alg")

        if not kid:
            raise JWTError("Missing 'kid' in token header")


        jwks = get_jwks()
        key_data = next((key for key in jwks["keys"] if key["kid"] == kid), None)
        
        if not key_data:
            global _jwks_cache
            _jwks_cache = None
            jwks = get_jwks()
            key_data = next((key for key in jwks["keys"] if key["kid"] == kid), None)
            
            if not key_data:
                raise JWTError("Could not find matching public key for kid")

        payload: dict[str, Any] = jwt.decode(
            token,
            key_data, 
            algorithms=[alg],
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "require_exp": True,
            },
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.INVALID_TOKEN_MISSING_USER,
            )

        return str(user_id)

    except JWTError as err:
        logger.warning(LogMessages.JWT_VALIDATION_FAILED.format(error=err))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid session: {str(err)}",
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Dependency to get the current user ID"""
    return validate_jwt_token(credentials.credentials)

def get_auth_service() -> AuthService:
    """Dependency to get the AuthService instance"""
    return AuthService()

def get_project_service():
    return ProjectService()

def get_session_manager():
    return SessionManager()