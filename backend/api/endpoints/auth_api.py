import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.dependencies import get_auth_service, get_current_user, security
from backend.core.messages import ErrorMessages, SuccessMessages
from backend.models.auth import (
    AuthResponse,
    PasswordResetRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from backend.services.auth_service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)


def handle_auth_error(e: Exception) -> HTTPException:
    """
    Convert auth errors to appropriate HTTP exceptions
    """
    if isinstance(e, ValueError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Authentication error: {e!s}",
    )


def format_auth_response(result: dict[str, Any]) -> AuthResponse:
    """
    Format Supabase auth result into standardized response
    """
    full_name = result["user"].get("full_name", "")
    if not full_name:
        user_metadata = result["user"]["user_metadata"]
        if isinstance(user_metadata, dict):
            full_name = user_metadata.get("full_name")

    user_response = UserResponse(
        id=result["user"]["id"],
        email=result["user"]["email"],
        full_name=str(full_name),
        created_at=result["user"]["created_at"],
    )

    token_response = TokenResponse(
        access_token="",
        refresh_token="",
        token_type="bearer",
    )

    session_data = result.get("session")
    if (
        session_data
        and isinstance(session_data, dict)
        and session_data.get("access_token")
    ):
        token_response = TokenResponse(
            access_token=session_data["access_token"],
            refresh_token=session_data["refresh_token"],
            token_type="bearer",
        )

    return AuthResponse(user=user_response, token=token_response)

AuthUser = Annotated[AuthService,Depends(get_auth_service)]

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    auth_service: AuthUser,
) -> AuthResponse:
    """Register a new user account"""
    try:
        result = await auth_service.signup(user_data)
        return format_auth_response(result)
    except Exception as e:
        raise handle_auth_error(e) from e


@router.post("/login", response_model=AuthResponse)
async def login(
    user_data: UserLogin,
    auth_service: AuthUser,
) -> AuthResponse:
    """Log in with email and password"""
    try:
        result = await auth_service.login(user_data)
        return format_auth_response(result)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_CREDENTIALS,
        ) from None
    except Exception as e:
        raise handle_auth_error(e) from e


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    user_id:str=Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    """Log out the current user"""
    try:
        success = await auth_service.logout(user_id)
        if not success:
            raise HTTPException(
                status_code=500,
                detail=ErrorMessages.LOGOUT_FAILED)
        
        return {"message": SuccessMessages.LOGOUT_SUCCESS}
    except Exception as e:
        raise handle_auth_error(e) from e


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: PasswordResetRequest,
    auth_service: AuthUser
) -> dict[str, str]:
    """Request a password reset"""
    try:
        await auth_service.request_password_reset(request.email)
        return {"message": SuccessMessages.PASSWORD_RESET_SENT}
    except Exception as e:
        raise handle_auth_error(e) from e


@router.get("/session-check", status_code=status.HTTP_200_OK)
async def session_check(
    user_id: str = Depends(get_current_user)
) -> dict[str, Any]:
    """Check if the current session is valid"""
    return {"valid": True, "user_id": user_id}

