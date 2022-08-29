from selenium.webdriver.common.by import By

from lib.application import Application
from lib.assertions import assert_selector

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
app.default_selector(By.CSS_SELECTOR)

# Find elements
all_links = app.client.find.all('.p-channel_sidebar__channel', text='selenium')
first_link = app.client.find.first('.p-channel_sidebar__channel', text='selenium')

# Asserts
assert app.client.find.element('.p-channel_sidebar__channel', text='selenium').text == first_link.text
assert all_links[0].text == first_link.text
assert app.client.match.Title.has('slack', case_insensitive=True)
expected_text = first_link.text
assert_selector('.p-channel_sidebar__channel', text=expected_text, visible=True)

# Actions
app.client.find.first('button').click()

app.take_screenshot()

app.stop()
