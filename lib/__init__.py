# from .application import Application
# from .assertions import assert_selector, assert_no_selector
# from .configuration import Configuration
# from .driver import SpectronDriver
# from .element import wrap_element, SpectronElement
# from .exception import *
# from .expected import text_to_be_present_in_element, title_contains
# from .finders import *
# from .globals import *
# from .helper import to_seconds, generate_target
# from .logging import set_selenium_log_level
# from .matchers import Title, URL, Element
# from .query import query
# from .result import ResultDict, Result

from . import application
from . import assertions
from . import configuration
from . import driver
from . import element
from . import exception
from . import expected
from . import finders
from . import globals
from . import helper
from . import matchers
from . import query
from . import result

import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S"
)