# Behave Setup

In your `environment.py`, create a instance of `Application` and assign it to the global `context`.

```python
def before_scenario(context: Context, scenario: Scenario):
    context.app = Application(
        app_path='/Applications/Slack.app/Contents/MacOS/Slack',
        chromedriver_version="96.0.4664.35"
    )
```

Then create a new step definition that starts the application:

```python
@Given('the electron application starts')
def step_impl(context):
    context.app.start()
```

You can now use webdriver in `client`:

```python
@Then('find the application title and click the button')
def step_impl(context):
    print(context.app.client.title)
    my_button = context.app.client.find_element(By.ID, "my-button")
    my_button.click()
```

After add a hook in `environment.py` that will take a screenshot and stop the application:

```python
def after_scenario(context: Context, scenario: Scenario):
    # Screenshot
    time = datetime.now().strftime("%H:%M:%S")
    context.app.take_screenshot(f'{scenario.name}-{time}.png', folder='screenshots')

    # Cleanup
    context.app.stop()
```