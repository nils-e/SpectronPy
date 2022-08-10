# SpectronPy

SpectronPy is a Python implementation of Spectron for testing Electron. It allows you to easily use selenium to test your [Electron](https://www.electronjs.org/docs/latest) application.

JS Spectron was [deprecated](https://github.com/electron-userland/spectron#-spectron-is-officially-deprecated-as-of-february-1-2022).

## OS Support
- [x] Mac OS
- [ ] Windows
- [ ] Linux

## Installation


## Usage
```python
import time
from lib.application import Application

# Optional
config = {
    'app_port': 9000,
    'electron_log_path': 'electron.log',
    'chromedriver_log_path': 'chrome.log',
    'wait_timeout': 3000,
}

app = Application(
    app_path='/Applications/Slack.app/Contents/MacOS/Slack',
    chromedriver_version="96.0.4664.35",
    config=config
)
app.start()

time.sleep(5)
print(app.client.title)
app.take_screenshot()

app.stop()
```

## Application API

### Options
- `app_path` - required. Path to electron application. Path is relative to the current working directory.
- `chromedriver_version` - required. Version of chromedriver to download. This must match the version of the Electron application.
- `config` - optional.

#### Config
- `app_port` - Electron debugger port. WebDriver will connect to this. Default: `9515`
- `chrome_driver_args` - Electron debugger port. WebDriver will connect to this.
- `chromedriver_cache` - Cache for chromedriver version. Default: `7` days
- `chromedriver_log_path` - Location for Chrome log file to output. ex: `chrome.log`
- `chromedriver_verbose` - Set chromedriver to verbose with `--verbose`.
- `chromedriver_path` - Path to chromedriver. Path is relative to the current working directory.
- `electron_args` - Arguments passed to the electron application.
- `electron_log_path` - Location for Electron log file to output. ex: `electron.log`
- `start_timeout` - Timeout for webdriver start up. Default: `10000`
- `stop_timeout` - Timeout for Application termination. Default: `5000`
- `wait_timeout` - Timeout for WebDriver. Refer to WebDriver class for `set_page_load_timeout`, `set_script_timeout`, `implicitly_wait`. Default: `5000`
- `webdriver_options` - Options which are passed to webdriver.
- `working_directory` - Default: `cwd()`

### Properties

#### client
`Type: WebDriver`

SpectronPy is using [Selenium](https://selenium-python.readthedocs.io/) under the hood. The `client` variable is exposed so you can access all the typical Selenium functionality. It is attached  to the `Application` instance. 

## Finders
`WIP`

## Methods
    def __init__(self, app_path: str, chromedriver_version: str, config=None)
Initialize Application.

    def start(self) -> None
Starts both the Electron application and webdriver on the same port.

    def stop(self) -> None
Using the webdriver functions to stop the application and chromedriver.

    def terminate(self) -> None

Terminates the application via OS-specific functions using PID. This is useful if `stop()` doesn't work as expected.

    def restart(self) -> None
Restart the application and webdriver.

    async def start_client(self) -> WebDriver
Configure and start webdriver. Returns a Webdriver instance.

    def start_app(self) -> Popen
Start Electron application in subprocess.

    def wait_until_window_loaded(self)
Not implemented yet.

    def is_running(self) -> bool
Returns current running status of the Electron application.

    def get_settings(self) -> Configuration
Returns the Application options set earlier.

    def switch_to_main_window(self) -> None
Switch Webdriver to main window.

    def take_screenshot(self, filename=None, folder=None) -> None
Take a screenshot of the Electron application.

## Test Libraries

### Use with Behave
Check the example in this repo on how to implement it. While in [example/behave](/example/behave) run:
```python
behave
```

### Use with PytestBDD
`WIP`


## Development
1) Install `python >= 3.10`
2) `git clone https://github.com/nils-e/SpectronPy.git`
3) Create a virtual env: `python -m venv venv`
4) Activate venv: `source ./venv/bin/activate`
5) Install packages: `pip install -e .`
6) Run an example: `python example/spectron.py`

## To do
- Implement wait_until_window_loaded
- Implement Finders
- Add logfile to logger
- Add PytestBDD Example