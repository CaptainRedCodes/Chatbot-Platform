import logging
import os
from typing import Optional

from src.core.constants import EnvVars
from src.core.messages import LogMessages

logger = logging.getLogger(__name__)


def get_secret(secret_name: str, project_id: Optional[str] = None) -> str:
    """
    Retrieve a secret from environment variables.
    The project_id argument is kept for compatibility but ignored.
    """
    logger.debug(f"Attempting to retrieve secret {secret_name} from env")
    return os.environ.get(secret_name, "")


def load_secrets_from_gsm() -> None:
    """Legacy function kept for compatibility - no-op"""
    pass


def should_use_gsm() -> bool:
    """Always returns False as GSM is removed"""
    return False
