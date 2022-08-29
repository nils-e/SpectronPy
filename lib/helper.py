# helper.py
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import lib.globals as glob


def to_seconds(ms_time):
    return ms_time / 1000


def generate_target(element_or_locator: str | WebElement, by=None) -> tuple | WebElement:
    """Generates a selenium locator if the object passed in isn't a WebElement"""
    if not isinstance(element_or_locator, WebElement):
        locator = element_or_locator
        if by is None:
            by = glob.get_default_selector()

        target: tuple[By, str] = (by, locator)
    else:
        target: WebElement = element_or_locator

    return target
