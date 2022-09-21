import time
from behave import Given, When, Then


@Given('the electron application starts')
def step_impl(context):
    context.app.start()


@When('the application is visible')
def step_impl(context):
    time.sleep(5)


@Then('the application title has "{title}"')
def step_impl(context, title):
    assert title in context.app.client.title, \
        f"Title doesn't include '{title}' in '{context.app.client.title}'"
