# assertions.py

from selenium.webdriver.remote.webelement import WebElement

import lib.finders as finders
from lib import logging
from lib.exception import ExpectationNotMet
from lib.result import _verify_match

logger = logging.getLogger(__name__)


def assert_selector(element_or_locator: WebElement | str, by=None, wait=None, **kwargs) -> None:
    """
    Assert the selector is in the DOM

    count: int | bool
        count of >= X; verify that X amount of elements are found and that they all match the expectations.
        count of 0 | False; get all elements and check that at least 1 matches the expectations.

    visible: bool
        visible of True; verify that the elements are in the DOM and within the viewport.
        visible of False; verify that the element is in the DOM.

    text: str
        verify that the elements include the text.
    """

    default_kwargs = {
        'count': 1,
        'visible': False
    }
    expectations = default_kwargs | kwargs
    expected_count = expectations.get('count', None)
    results = []

    for element in finders.all(element_or_locator, by, wait):
        results.append(_verify_match(element, expectations))

    summarized_results = [x.summarize_all() for x in results]

    if not any(summarized_results) or \
            (expected_count and expected_count != summarized_results.count(True)):
        msg = "Assertion failed!\n"
        msg += f"Found {len(summarized_results)} elements.\n"
        msg += f"{summarized_results.count(True)} elements matched expectations.\n"
        msg += _expectation_not_met(expectations)
        raise ExpectationNotMet(msg)


def assert_no_selector(element_or_locator: WebElement | str, by=None, wait=None, **kwargs) -> None:
    """
    Assert the selector matching the expectations is not in the DOM

    same parameter functions as `assert_selector`
    """

    default_kwargs = {
        'count': 0,
        'visible': False
    }
    expectations = default_kwargs | kwargs
    expected_count = expectations.get('count', None)
    results = []

    for element in finders.all(element_or_locator, by, wait):
        results.append(_verify_match(element, expectations))

    summarized_results = [x.summarize_all() for x in results]

    if (not expected_count and any(summarized_results)) or \
            (any(summarized_results) and expected_count and expected_count == summarized_results.count(True)):
        msg = "Assertion failed!\n"
        msg += f"Found {len(summarized_results)} elements.\n"
        msg += f"{summarized_results.count(True)} elements matched expectations.\n"
        msg += _negative_expectation_not_met(expectations)
        raise ExpectationNotMet(msg)


def _negative_expectation_not_met(expectation):
    return f"Found an element that matched all expectations:: \n\tExpected no match: {expectation}"


def _expectation_not_met(expectation):
    return f"Failed to match all elements to all expectations:: \n\tExpected a match: {expectation}"
