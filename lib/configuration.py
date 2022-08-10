import os
from dataclasses import dataclass, asdict, field


@dataclass
class Configuration:
    """Configuration is all the options available to SpectronPy
    app_path
        Path to electron application. Path is relative to the current working directory.

    app_port
        Electron debugger port. WebDriver will connect to this.

    start_timeout
        Timeout for webdriver start up.

    wait_timeout
        Timeout for WebDriver. Refer to WebDriver class for set_page_load_timeout, set_script_timeout, implicitly_wait.

    stop_timeout
        Timeout for Application termination.

    electron_args
        Arguments passed to the electron application.

    working_directory

    chromedriver_cache
        Cache for chromedriver version

    webdriver_options
        Options passed to webdriver.

    chromedriver_version
        Version of chromedriver to download. This must match the version of the Electron application.

    chromedriver_path
        Path to chromedriver. Path is relative to the current working directory.

    chrome_driver_args
        Arguments passed to chromedriver.

    chromedriver_log_path
        Location for Chrome log file to output. ex: chrome.log

    chromedriver_verbose
        Set chromedriver to verbose with `--verbose`.

    electron_log_path
        Location for Electron log file to output. ex: electron.log

    """
    app_path: str = ''
    app_port: int = 9515
    start_timeout: int = 10000
    wait_timeout: int = 5000
    stop_timeout: int = 5000
    electron_args: list = field(default_factory=list)
    working_directory: str = os.getcwd()
    chromedriver_cache: int = 7
    webdriver_options: dict = field(default_factory=dict)
    chromedriver_version: str = ''
    chromedriver_path: str = ''
    chrome_driver_args: list = field(default_factory=list)
    chromedriver_log_path: str = ''
    chromedriver_verbose: bool = False
    electron_log_path: str = ''

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


