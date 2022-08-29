# finders.py
import logging
from typing import Optional

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as Expected

import lib.expected as SpectronExpected
from lib.element import wrap_element
from lib.exception import ExpectationNotMet, AmbiguousMatch
from lib.globals import get_driver, get_default_wait_time, get_default_selector
from lib.query import query

logger = logging.getLogger(__name__)


def by_css(css: str, wait: int = None, **kwargs) -> WebElement:
    return element(css, By.CSS_SELECTOR, wait, **kwargs)


def by_name(name: str, wait: int = None) -> WebElement:
    return element(name, By.NAME, wait)


def by_class(cls: str, wait: int = None) -> WebElement:
    return element(cls, By.CLASS_NAME, wait)


def by_id(id: str, wait: int = None) -> WebElement:
    return element(id, By.ID, wait)


def by_xpath(xpath: str, wait: int = None) -> WebElement:
    return element(xpath, By.XPATH, wait)


def by_tag(tag: str, wait: int = None) -> WebElement:
    return element(tag, By.TAG_NAME, wait)


def by_link_text(text: str, wait: int = None) -> WebElement:
    return element(text, By.LINK_TEXT, wait)


def by_partial_link_text(text: str, wait: int = None) -> WebElement:
    return element(text, By.PARTIAL_LINK_TEXT, wait)


def all(locator: str, by=None, wait: int = None, **kwargs) -> list[Optional[WebElement]]:
    if by is None:
        by = get_default_selector()

    if wait is None:
        wait = get_default_wait_time()

    rtn = []

    try:
        elems = query(get_driver(), locator, by, wait)
        rtn = list(map(wrap_element, elems))
    except TimeoutException as e:
        logger.info(_wait_time_expired((locator, by), wait))

    visibility = kwargs.get('visible', None)
    if visibility:
        """Filter only the elements within the current viewport"""
        rtn = list(filter(lambda x: Expected.visibility_of(x)(get_driver()), rtn))

    expected_text = kwargs.get('text', None)
    if expected_text:
        """Filter the elements that contain the text"""
        rtn = list(filter(lambda x: SpectronExpected.text_to_be_present_in_element(x, expected_text)(get_driver()), rtn))

    if kwargs.get('ambiguous_check', None) and len(rtn) > 1:
        """Checks if only 1 elements was found"""
        msg = f"Ambiguous match, found {len(rtn)} elements matching by {by} '{locator}'."
        logger.error(msg)
        raise AmbiguousMatch(msg)

    count = kwargs.get('count', None)
    if count and len(rtn) != count:
        """Checks if the number of elements was found"""
        logger.error(_count_expectation_not_met((locator, by), count, len(rtn)))
        raise ExpectationNotMet(_count_expectation_not_met((locator, by), count, len(rtn)))

    minimum_expected = kwargs.get('minimum', None)
    if minimum_expected and len(rtn) < minimum_expected:
        """Checks if at least the minimum number of elements was found"""
        logger.error(_minimum_expectation_not_met((locator, by), minimum_expected, len(rtn)))
        raise ExpectationNotMet(_minimum_expectation_not_met((locator, by), minimum_expected, len(rtn)))

    return rtn


def first(locator: str, by=None, wait: int = None, **kwargs) -> WebElement:
    return all(locator, by=by, wait=wait, minimum=1, **kwargs)[0]


def element(locator: str, by=None, wait: int = None, **kwargs) -> WebElement:
    if by is None:
        by = get_default_selector()

    if wait is None:
        wait = get_default_wait_time()

    elem: WebElement = all(locator, by, wait, count=1, ambiguous_check=True, **kwargs)[0]
    rtn = wrap_element(elem)

    return rtn


# Private


def _wait_time_expired(locator: tuple, wait: int):
    return f"Wait time expired:: {locator}, wait time: {wait}"


def _minimum_expectation_not_met(locator: tuple, expectation: int, found: int):
    return f"Target did not match expectation:: {locator} \n\tMinimum Expected: {expectation} \n\tFound: {found}"


def _count_expectation_not_met(locator: tuple, expectation: int, found: int):
    return f"Target did not match expectation:: {locator} \n\tExpected: {expectation} \n\tFound: {found}"


def _no_element_found(locator: tuple):
    return f"No element found:: {locator}"
