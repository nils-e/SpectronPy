# finders.py
from typing import Callable, TypeVar, Optional

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Expected

from lib import logging
from lib.exception import ExpectationNotNet

default_wait_time: Optional[int] = None
driver: Optional[WebDriver] = None
logger = logging.getLogger(__name__)


def by_css(css: str, wait: int = default_wait_time) -> WebElement:
    return element(css, By.CSS_SELECTOR, wait)


def by_name(name: str, wait: int = default_wait_time) -> WebElement:
    return element(name, By.NAME, wait)


def by_class(cls: str, wait: int = default_wait_time) -> WebElement:
    return element(cls, By.CLASS_NAME, wait)


def by_id(id: str, wait: int = default_wait_time) -> WebElement:
    return element(id, By.ID, wait)


def by_xpath(xpath: str, wait: int = default_wait_time) -> WebElement:
    return element(xpath, By.XPATH, wait)


def by_tag(tag: str, wait: int = default_wait_time) -> WebElement:
    return element(tag, By.TAG_NAME, wait)


def by_link_text(text: str, wait: int = default_wait_time) -> WebElement:
    return element(text, By.LINK_TEXT, wait)


def by_partial_link_text(text: str, wait: int = default_wait_time) -> WebElement:
    return element(text, By.PARTIAL_LINK_TEXT, wait)


def all(locator: tuple, wait: int = default_wait_time, **kwargs) -> list[WebElement | None]:
    elements = []
    try:
        elements = WebDriverWait(driver, wait).until(
            Expected.presence_of_all_elements_located(
                locator
            )
        )
    except TimeoutException:
        logger.info(_wait_time_expired(locator, wait))

    minimum_found = kwargs.get('minimum', None)
    if minimum_found and len(elements) < minimum_found:
        """Checks if at least the minimum number of elements were found"""
        logger.error(_minimum_expectation_not_met(locator, minimum_found, len(elements)))
        raise ExpectationNotNet(_minimum_expectation_not_met(locator, minimum_found, len(elements)))

    return elements


def first(locator: tuple, wait: int = default_wait_time) -> WebElement:
    return all(locator, wait=wait, minimum=1)[0]


def element(value: str, by=By.ID, wait: int = default_wait_time) -> WebElement:
    try:
        el = WebDriverWait(driver, wait).until(
            Expected.presence_of_element_located(
                (by, value)
            )
        )
    except TimeoutException as e:
        logger.error(_no_element_found((by, value)))
        raise NoSuchElementException(_no_element_found((by, value))) from e

    return el


# Private


def _wait_time_expired(locator: tuple, wait: int):
    return f"Wait time expired:: {locator}, wait time: {wait}"


def _minimum_expectation_not_met(locator: tuple, expectation: int, found: int):
    return f"Target did not match expectation:: {locator} \n\tMinimum Expected: {expectation} \n\tFound: {found}"


def _no_element_found(locator: tuple):
    return f"No element found:: {locator}"
