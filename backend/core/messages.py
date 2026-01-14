class ErrorMessages:
    """Error messages shown to users"""

    INVALID_CREDENTIALS = "Invalid email or password"
    INVALID_TOKEN = "Invalid authentication token"
    INVALID_TOKEN_MISSING_USER = "Invalid token: missing user identifier"

    LOGOUT_FAILED = "Failed to log out"
    REGISTRATION_FAILED = "Registration failed"
    AUTHENTICATION_FAILED = "Authentication failed"

    PROJECT_FAILED = "Error Creating the project"
    PROJECT_UPDATE_FAILED = "Error Updatng the project"
    PROJECT_DELETE_FAILED = "Error Deleteing the project "




class SuccessMessages:
    """Success messages shown to users"""

    LOGOUT_SUCCESS = "Successfully logged out"
    PASSWORD_RESET_SENT = "Password reset email sent"

    PROJECT_CREATED = "Successfully created the project"
    PROJECT_UPDATED = "Sucessfully Updated the project"
    PROJECT_DELETED = "Sucessfully Deleted the project"


class LogMessages:
    """Internal log messages"""

    USER_CREATED = "User created: {user_id}"
    USER_LOGGED_IN = "User logged in: {user_id}"
    USER_LOGGED_OUT = "User logged out successfully"

    # Settings loading
    LOADING_FROM_ENV = "Loading settings from environment variables (GSM disabled)"

    # JWT validation
    JWT_MISSING_SUB = "Token is valid but missing 'sub' claim"
    JWT_VALIDATION_FAILED = "JWT validation failed: {error}"
    JWT_KEY_NOT_FOUND = "JWT Key is not found"