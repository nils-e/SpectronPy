# globals.py
from typing import Optional

from selenium.webdriver.chrome.webdriver import WebDriver

default_wait_time = None
driver = None
default_selector = None


def initialize():
    global default_wait_time, driver, default_selector


def get_default_wait_time():
    return default_wait_time


def get_driver() -> Optional[WebDriver]:
    return driver


def get_default_selector():
    return default_selector
