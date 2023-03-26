import logging

import pytest

from utils.url_sanitizer import get_base_url, get_hostname, validate_url

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "url",
    [
        "http://www.google.com",
        "https://www.google.com",
        "http://www.google.com/some_path/and_so_on",
        "http://www.google.com:5000",
        "http://www.google.com?args=1#and_some_comment",
    ],
)
def test_get_hostname(url: str):
    assert get_hostname(url) == "www.google.com"


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://www.google.com", "http://www.google.com"),
        ("http://www.google.com:5000", "http://www.google.com"),
        ("http://www.google.com?args=1#and_some_comment", "http://www.google.com"),
        ("http://www.google.com/some_path/", "http://www.google.com/some_path/"),
    ],
)
def test_get_base_url(url: str, expected: str):
    assert get_base_url(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        ("http://www.google.com"),
        ("https://www.google.com"),
        ("http://www.google.com:5000"),
        ("http://www.google.com?args=1#and_some_comment"),
        ("http://www.google.com/some_path/"),
    ],
)
def test_validate_url(url: str):
    assert validate_url(url) is None


@pytest.mark.parametrize(
    "url",
    [
        ("www.google.com"),
        ("http://?args=1#and_some_comment"),
        ("http:/some_path/"),
        ("asdasdasd"),
    ],
)
def test_validate_url_negative(url: str):
    with pytest.raises(ValueError, match="Illegal URL structure"):
        validate_url(url)
