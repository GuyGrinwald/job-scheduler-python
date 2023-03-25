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
def get_base_url(url: str) -> str:
    """
    Removes any <params>, <query_params>, or <fragment> from the given URL
    """
    result = urlparse(url)
    return f"{result.scheme}://{result.hostname}{result.path}"  # path, if exists, starts with '/'


@staticmethod
def validate_url(url: str) -> str:
    """
    Validates that the given url is in the form of <scheme>://<netloc>/<path>?
    """
    result = urlparse(url)

    if not result.scheme or not result.netloc:
        raise ValueError("Illegal URL structure")

    return url
