# FILE: features/environment.py
from datetime import datetime
from behave.model import Scenario, Step
from behave.runner import Context
from lib.application import Application


# -----------------------------------------------------------------------------
# HOOKS:
# -----------------------------------------------------------------------------
# def before_all(context):

# def before_feature(context, feature):

def before_scenario(context: Context, scenario: Scenario):
    context.app = Application(
        app_path='/Applications/Slack.app/Contents/MacOS/Slack',
        chromedriver_version="96.0.4664.35",
        config={
            'app_port': 9000,
            'electron_log_path': 'logs/electron.log',
            'chromedriver_log_path': 'logs/chrome.log',
            'wait_timeout': 3000,
        }
    )


# def before_tag(context, tag):

# def before_step(context, step):

# def after_all(context):

# def after_feature(context, features):

def after_scenario(context: Context, scenario: Scenario):
    # Screenshot
    time = datetime.now().strftime("%H:%M:%S")
    context.app.take_screenshot(f'{scenario.name}-{time}.png', folder='screenshots')

    # Cleanup
    context.app.stop()


# def after_tag(context, tag):

def after_step(context, step: Step):
    print()
