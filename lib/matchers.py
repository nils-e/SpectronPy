from pprint import pprint
from typing import Optional, Pattern

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as Expected
from selenium.webdriver.support.wait import WebDriverWait

import re

from lib import logging

default_wait_time: Optional[int] = None
driver: Optional[WebDriver] = None
logger = logging.getLogger(__name__)


class Title:
    @classmethod
    def has(cls, title: str, wait: int = default_wait_time) -> bool:
        return _wait_until(Expected.title_contains(title), wait, _repr(cls, title))

    @classmethod
    def equals(cls, title: str, wait: int = default_wait_time) -> bool:
        return _wait_until(Expected.title_is(title), wait, _repr(cls, title))


class URL:
    @classmethod
    def has(cls, url: str, wait: int = default_wait_time) -> bool:
        return _wait_until(Expected.url_contains(url), wait, _repr(cls, url))

    @classmethod
    def equals(cls, url: str, wait: int = default_wait_time) -> bool:
        return _wait_until(Expected.url_to_be(url), wait, _repr(cls, url))

    @classmethod
    def matches(cls, url: str, wait: int = default_wait_time) -> bool:
        pattern: Pattern[str] = re.compile(url)
        return _wait_until(Expected.url_matches(pattern), wait, _repr(cls, url))

    @classmethod
    def changes(cls, url: str, wait: int = default_wait_time) -> bool:
        return _wait_until(Expected.url_changes(url), wait, _repr(cls, url))


# Private
def _wait_until(condition, wait: int = default_wait_time, debug_str=None) -> bool:
    if wait is None:
        wait = default_wait_time

    status = False
    try:
        return WebDriverWait(driver, wait).until(
            condition
        )
    except TimeoutException:
        logger.info(_timeout_str(condition, wait, debug_str))

    return status


def _repr(cls, pattern=None):
    if pattern:
        return f"{cls.__module__}.{cls.__qualname__} matching '{pattern}'"
    else:
        return f"{cls.__module__}.{cls.__qualname__}"


def _timeout_str(condition, wait, debug=None):
    if debug:
        return f"Could not find target in time:: {debug}, wait: {wait}"
    else:
        return f"Could not find target in time:: {condition.__qualname__} wait: {wait}"
