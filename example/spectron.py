import time

from selenium.webdriver.common.by import By

from lib.application import Application

# Optional
config = {
    'app_port': 9000,
    'electron_log_path': 'electron.log',
    'chromedriver_log_path': 'chrome.log',
    'wait_timeout': 5000,
}

app = Application(
    app_path='/Applications/Slack.app/Contents/MacOS/Slack',
    chromedriver_version="96.0.4664.35",
    config=config
)
app.start()

time.sleep(5)
assert app.client.match.Title.has("Slack")

app.take_screenshot()

app.stop()
