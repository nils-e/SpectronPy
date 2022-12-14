# SpectronPy

SpectronPy is a Python implementation of Spectron for testing Electron. It allows you to easily use selenium to test your [Electron](https://www.electronjs.org/docs/latest) application. SpectronPy is not affiliated with the Spectron project.

JS Spectron was [deprecated](https://github.com/electron-userland/spectron#-spectron-is-officially-deprecated-as-of-february-1-2022) in early 2022.


## Installation
_Requires python 3.10_
```python
pip install spectronpy
```

## Usage
```python
from spectronpy import Application

# Optional
config = {
    'app_port': 9000,
    'wait_timeout': 3000,
}

# Initialize Application object with required parameters
app = Application(
    app_path='/Applications/Slack.app/Contents/MacOS/Slack',
    chromedriver_version="96.0.4664.35",
    config=config
)
app.start()

# Implicit wait for title to update
app.client.match.Title.has('slack', case_insensitive=True)
print(app.client.title)

app.take_screenshot()
app.stop()
```

## Application API

### Options
- `app_path` - **required.** Path to electron application or module.
- `chromedriver_version` - **required.** Version of chromedriver to download. This must match the version of the Electron application.
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
- `debug_timeout` - Timeout for pause functionality. Refer to `Application.pause()`. Default: `50000`

### Properties

#### Client
`Type: WebDriver`

SpectronPy is using [Selenium](https://selenium-python.readthedocs.io/) under the hood. The `client` variable is exposed so you can access all the typical Selenium functionality. It is attached  to the `Application` instance. 

#### Finders
Within the `client` object, you have access to the `find` property. These functions allow additional ways to find elements. These finders are all using implicit waiting by default which is set to `wait_timeout` in the configuration of `Application`. You can disable implicit waiting by setting the `wait_timeout` to 0.

- `all(locator: str, by=None, wait: int = None, **kwargs)` - Find all elements matching the arguments.
- `first(locator: str, by=None, wait: int = None, **kwargs)` - Find the first element matching the arguments.
- `element(locator: str, by=None, wait: int = None, **kwargs)` - Find an element matching the arguments. Expects only 1 exact match.
- `by_*(...)` - Similar to `element()` but uses different locator strategies.

```python
kwargs = {
    'text': None, # Matches the text inside the element.
    'ambiguous_check': None, # Check if only 1 element is found.
    'count': None, # Check if the number of elements returned equals the count.
    'minimum': None, # Check if at least this many elements were found.
    'visible': None, # Match all the elements currently in the viewport, not just the DOM.
}
```

#### Matchers
Within the `client` object, you have access to the `match` property. These functions allow additional ways to match element criteria. This is useful for assertions or waiting.

- `Title`
- `URL`
- `Element`

### Methods
Application class methods.

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
Configure and start webdriver.

    def start_app(self) -> Popen
Start Electron application.

    #WIP def wait_until_window_loaded(self)
Not implemented yet.

    def is_running(self) -> bool
Returns current running status of the Electron application.

    def get_settings(self) -> Configuration
Returns the current Application options.

    def switch_to_main_window(self) -> None
Switch to main window.

    def take_screenshot(self, filename=None, folder=None) -> None
Take a screenshot of the Electron application.

    def devtools_url(self) -> str
Provides a devtools url to be able to explore the selectors of your electron app via chrome.

    def pause(self, timeout=None) -> None
Initiate a pause. This is meant to be used for debugging automation code. Check out `start_debug_mode`.

    def unpause(self) -> None
Unpause a previous pause.

    def default_selector(self, by: By) -> None
Sets the default selector globally. Default: `By.ID`

    def start_debug_mode(self, timeout=None) -> None
Starts a debugger mode with a pause. Check terminal for devtools URL and click through to your application viewport via chrome. Here you can explore the selectors of your electron app.

## Test Libraries

### Use with Behave
Check the example in this repo on how to implement it. While in [example/behave](/example/behave), you can run all the tests with:
```python
behave
```

### Use with PytestBDD
`WIP`


## Development
1) Install `python >= 3.10`
2) Clone: `git clone https://github.com/nils-e/SpectronPy.git`
3) Create a virtual env: `python -m venv venv`
4) Activate venv: `source ./venv/bin/activate`
5) Install packages: `pip install -e .`
6) Run an example: `python example/spectron.py`

## To Do
- Implement wait_until_window_loaded
- Add logfile out to logger
- Add PytestBDD example
- Automatically open a debugger window
- Add kwarg parameter to finder/matcher
- Add commitizen
- Add python linter

## Resources
- https://github.com/electron-userland/spectron
- https://github.com/electron/electron-quick-start
  - Helped to implement the test app
- https://github.com/teamcapybara/capybara
  - A lot of guidance from one of my favorite selenium frameworks