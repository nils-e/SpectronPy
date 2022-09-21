import logging

# Basic logger configuration found in __init__.py


def set_selenium_log_level(level):
    selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(level)
