# query.py
from typing import Optional

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as Expected
from selenium.webdriver.support.wait import WebDriverWait

import logging

logger = logging.getLogger(__name__)


def query(driver, locator: str, by: By, wait: int, **kwargs) -> list[Optional[WebElement]]:
    results: list[WebElement] = []

    try:
        elements: list[WebElement] = WebDriverWait(driver, wait).until(
            Expected.presence_of_all_elements_located(
                (by, locator)
            )
        )

        if kwargs.get('maximum', None) == 1:
            results = [elements[0]]
        else:
            results = elements

    except TimeoutException:
        pass

    return results
