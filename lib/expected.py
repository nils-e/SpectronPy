# expected.py

from selenium.common import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement


def text_to_be_present_in_element(element_or_locator, text_):
    """ An expectation for checking if the given text is present in the
    specified element.
    returns True if the text is contained, False otherwise.
    """

    def _predicate(driver):
        try:
            target = element_or_locator
            if not isinstance(target, WebElement):
                target = driver.find_element(*target)
            element_text = target.text
            return text_ in element_text
        except StaleElementReferenceException:
            return False

    return _predicate


def title_contains(expected, case_insensitive=False):
    """ An expectation for checking that the title contains a substring.
    returns True when the title matches, False otherwise.
    """

    def _predicate(driver):
        actual = driver.title
        title = expected

        if case_insensitive:
            actual = actual.lower()
            title = title.lower()

        return title in actual

    return _predicate
