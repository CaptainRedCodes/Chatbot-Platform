import logging
from typing import Any

from backend.core.messages import ErrorMessages, LogMessages
from backend.core.supabase_client import get_supabase_client
from backend.models.auth import UserCreate, UserLogin


logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations"""

    def __init__(self):
        self.client = get_supabase_client()
    

    async def signup(self, user_data: UserCreate) -> dict[str, Any]:
        """Register a new user in Supabase Auth"""
        try:
            auth_response = self.client.auth.sign_up(
                {
                    "email": user_data.email,
                    "password": user_data.password,
                    "options": {
                        "data": {
                            "full_name": user_data.full_name,
                        }
                    },
                }
            )

            if not hasattr(auth_response, "user") or not auth_response.user:
                raise ValueError(
                    f"{ErrorMessages.REGISTRATION_FAILED}: Could not create user"
                )

            logger.info(LogMessages.USER_CREATED.format(user_id=auth_response.user.id))

            return self._build_auth_dict(auth_response)

        except Exception as e:
            logger.error(f"Signup error: {e!s}")
            raise ValueError(f"{ErrorMessages.REGISTRATION_FAILED}: {e!s}") from e

    async def login(self, user_data: UserLogin) -> dict[str, Any]:
        """Authenticate a user with email and password"""
        try:
            auth_response = self.client.auth.sign_in_with_password(
                {
                    "email": user_data.email,
                    "password": user_data.password,
                }
            )

            if (
                not hasattr(auth_response, "user")
                or not auth_response.user
                or not auth_response.session
            ):
                raise ValueError(
                    f"{ErrorMessages.AUTHENTICATION_FAILED}: Invalid credentials"
                )

            logger.info(
                LogMessages.USER_LOGGED_IN.format(user_id=auth_response.user.id)
            )
            return self._build_auth_dict(auth_response)

        except Exception as e:
            logger.error(f"Login error: {e!s}")
            raise ValueError(f"{ErrorMessages.AUTHENTICATION_FAILED}: {e!s}") from e

    async def logout(self, user_id: str) -> bool:
        try:
            self.client.auth.admin.sign_out(user_id)
            logger.info(LogMessages.USER_LOGGED_OUT)
            return True
        except Exception as e:
            logger.error(f"Logout error: {e!s}")
            return False

    async def request_password_reset(self, email: str) -> bool:
        try:
            self.client.auth.reset_password_for_email(email)
            return True
        except Exception as e:
            logger.error(f"Password reset error: {e!s}")
            return False


    def _build_auth_dict(self, auth_response: Any) -> dict[str, Any]:
        """Build auth dict in format expected by format_auth_response helper"""
        user_metadata = auth_response.user.user_metadata
        if isinstance(user_metadata, str):
            logger.warning(f"User metadata is string instead of dict: {user_metadata}")
            user_metadata = {}
        elif user_metadata is None:
            user_metadata = {}

        full_name = ""
        if isinstance(user_metadata, dict):
            full_name = user_metadata.get("full_name", "")

        user_dict = {
            "id": auth_response.user.id,
            "email": auth_response.user.email,
            "user_metadata": user_metadata,
            "full_name": full_name,
            "created_at": auth_response.user.created_at,
        }

        session_dict = {}
        if auth_response.session:
            session_obj = auth_response.session
            access_token = getattr(session_obj, "access_token", None)
            refresh_token = getattr(session_obj, "refresh_token", None)

            if access_token:
                session_dict = {
                    "access_token": access_token,
                    "refresh_token": refresh_token or "",
                }

        return {
            "user": user_dict,
            "session": session_dict,
        }