import logging
from typing import Optional
from urllib.parse import urlparse

import utils.logging_config  # isort:skip

logger = logging.getLogger(__name__)

@staticmethod
def get_hostname(url: str) -> Optional[str]:
    """
    Extracts the hostname from the given URL
    """
    result = urlparse(url)
    return result.hostname

@staticmethod
def validate_url(url: str) -> str:
    """
    Validates that the given url is in the form of "http[s]://domain.[domains]+.TLD
    """
    logger.debug(f"Validating url: {url}")
    result = urlparse(url)

    if not result.scheme or not result.netloc:
        raise ValueError("Illegal URL structure")
    
    return url