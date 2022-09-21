# driver.py

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.timeouts import Timeouts

from . import globals as world


class SpectronDriver(WebDriver):

    def __init__(self, kwargs):
        from . import matchers
        from . import finders

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
        world.default_wait_time = timeouts.implicit_wait
