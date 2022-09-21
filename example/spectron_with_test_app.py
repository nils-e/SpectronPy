# Prerequisite:
# run `npm i` in `test/` folder

from selenium.webdriver.common.by import By
from spectronpy import Application, assert_selector

# Optional
config = {
    'app_port': 9000,
    'electron_log_path': 'electron.log',
    'chromedriver_log_path': 'chrome.log',
    'wait_timeout': 5000,
    # if you are using the electron module to run the app, need to pass the folder(test/) with `main.js` to electron
    'electron_args': ['test']
}

app = Application(
    app_path='test/node_modules/.bin/electron',  # <-- Electron module
    chromedriver_version="104.0.5112.79",
    config=config
)
app.start()
app.default_selector(By.CSS_SELECTOR)

# Find elements
all_links = app.client.find.all('span')
first_link = app.client.find.first('span')

# Asserts
assert app.client.find.element('span', text='16.15.0').text == first_link.text
assert all_links[0].text == first_link.text
assert app.client.match.Title.has('Hello World!', case_insensitive=True)
expected_text = first_link.text
assert_selector('span', text=expected_text, visible=True)

# Actions
app.client.find.first('button').click()

app.take_screenshot()

app.stop()
