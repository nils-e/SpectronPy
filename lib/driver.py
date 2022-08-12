# finders.py
from pprint import pprint

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.timeouts import Timeouts

import lib.matchers as matchers
import lib.finders as finders


class SpectronDriver(WebDriver):

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        matchers.driver = self
        finders.driver = self
        self.match = matchers
        self.find = finders

    def update_wait(self, wait_time: int):
        timeouts = Timeouts(
            implicit_wait=wait_time,
            page_load=wait_time,
            script=wait_time
        )
        self.timeouts = timeouts
        self.match.default_wait_time = timeouts.implicit_wait
        self.find.default_wait_time = timeouts.implicit_wait
