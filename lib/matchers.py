import re
from typing import Pattern, TypeVar

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as Expected
from selenium.webdriver.support.wait import WebDriverWait

import lib.globals as glob
from lib import logging
import lib.expected as SpectronExpected
from lib.helper import generate_target

logger = logging.getLogger(__name__)

Element_Locator = TypeVar('Element_Locator', WebDriver, tuple[str, By], str)


class Title:
    @classmethod
    def has(cls, title: str, case_insensitive=False, wait=None) -> bool:
        return _wait_until(SpectronExpected.title_contains(title, case_insensitive), wait, _repr(cls, title))

    @classmethod
    def equals(cls, title: str, wait=None) -> bool:
        print(glob.get_driver().title)
        return _wait_until(Expected.title_is(title), wait, _repr(cls, title))


class URL:
    @classmethod
    def has(cls, url: str, wait=None) -> bool:
        return _wait_until(Expected.url_contains(url), wait, _repr(cls, url))

    @classmethod
    def equals(cls, url: str, wait=None) -> bool:
        return _wait_until(Expected.url_to_be(url), wait, _repr(cls, url))

    @classmethod
    def matches(cls, url: str, wait=None) -> bool:
        pattern: Pattern[str] = re.compile(url)
        return _wait_until(Expected.url_matches(pattern), wait, _repr(cls, url))

    @classmethod
    def changes(cls, url: str, wait=None) -> bool:
        return _wait_until(Expected.url_changes(url), wait, _repr(cls, url))


class Element:

    @classmethod
    def to_be_clickable(cls, element_or_locator: Element_Locator, by=None, wait=None) -> WebElement | bool:
        return _wait_until(
            Expected.element_to_be_clickable(generate_target(element_or_locator, by)),
            wait,
            _repr(cls, element_or_locator)
        )

    @classmethod
    def to_have_text(cls, element_or_locator: Element_Locator, text: str, wait=None) -> WebElement | bool:
        return _wait_until(
            SpectronExpected.text_to_be_present_in_element(generate_target(element_or_locator), text),
            wait,
            _repr(cls, text)
        )


# Private
def _wait_until(condition, wait: int = None, debug_str=None) -> WebElement | bool:
    if wait is None:
        wait = glob.get_default_wait_time()

    driver = glob.get_driver()

    rtn = False
    try:
        rtn = WebDriverWait(driver, wait).until(
            condition
        )
    except TimeoutException:
        logger.info(_timeout_str(condition, wait, debug_str))

    return rtn


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
