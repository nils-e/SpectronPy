# driver.py

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.timeouts import Timeouts

import lib.globals


class SpectronDriver(WebDriver):

    def __init__(self, kwargs):
        import lib.matchers as matchers
        import lib.finders as finders

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
        self._set_wait_timers(timeouts)

    def _set_wait_timers(self, timeouts: Timeouts):
        self.timeouts = timeouts
        lib.globals.default_wait_time = timeouts.implicit_wait
