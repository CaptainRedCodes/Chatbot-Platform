class ErrorMessages:
    """Error messages shown to users"""

    # Authentication Errors
    INVALID_CREDENTIALS = "Invalid email or password"
    INVALID_TOKEN = "Invalid authentication token"
    INVALID_TOKEN_MISSING_USER = "Invalid token: missing user identifier"
    LOGOUT_FAILED = "Failed to log out"
    REGISTRATION_FAILED = "Registration failed"
    AUTHENTICATION_FAILED = "Authentication failed"

    # Project Errors
    PROJECT_FAILED = "Error Creating the project"
    PROJECT_UPDATE_FAILED = "Error Updating the project"
    PROJECT_DELETE_FAILED = "Error Deleting the project"
    PROJECT_NOT_FOUND = "Project not found"

    # LLM Service Errors
    LLM_RESPONSE_FAILED = "Failed to generate AI response"
    LLM_INVALID_MESSAGE_FORMAT = "Invalid message format provided"
    LLM_API_ERROR = "Error communicating with AI service"
    LLM_EMPTY_RESPONSE = "AI returned an empty response"

    # Session Service Errors
    SESSION_NOT_FOUND = "Session not found"
    SESSION_CREATE_FAILED = "Failed to create chat session"
    SESSION_UPDATE_FAILED = "Failed to update chat session"
    SESSION_DELETE_FAILED = "Failed to delete chat session"
    SESSION_LOAD_FAILED = "Failed to load session from database"
    SESSION_UNAUTHORIZED = "Unauthorized access to this session"
    SESSION_DB_ERROR = "Database error while managing session"

    # Memory Errors
    MEMORY_LOAD_FAILED = "Failed to load conversation memory"
    MEMORY_SAVE_FAILED = "Failed to save message to database"
    MEMORY_SUMMARIZE_FAILED = "Failed to summarize conversation"


class SuccessMessages:
    """Success messages shown to users"""

    LOGOUT_SUCCESS = "Successfully logged out"
    PASSWORD_RESET_SENT = "Password reset email sent"

    PROJECT_CREATED = "Successfully created the project"
    PROJECT_UPDATED = "Successfully Updated the project"
    PROJECT_DELETED = "Successfully Deleted the project"

    # Session Success Messages
    SESSION_CREATED = "Chat session created successfully"
    SESSION_UPDATED = "Chat session updated successfully"
    SESSION_DELETED = "Chat session deleted successfully"


class LogMessages:
    """Internal log messages"""

    USER_CREATED = "User created: {user_id}"
    USER_LOGGED_IN = "User logged in: {user_id}"
    USER_LOGGED_OUT = "User logged out successfully"


    # JWT validation
    JWT_MISSING_SUB = "Token is valid but missing 'sub' claim"
    JWT_VALIDATION_FAILED = "JWT validation failed: {error}"
    JWT_KEY_NOT_FOUND = "JWT Key is not found"