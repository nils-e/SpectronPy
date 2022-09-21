from .application import Application
from .assertions import assert_selector, assert_no_selector
from .configuration import Configuration
from .driver import SpectronDriver
from .element import SpectronElement, wrap_element
from .exception import (
    POpenError,
    InvalidArgument,
    UnsupportedOS,
    NotInitialized,
    ClientError,
    ExpectationNotMet,
    AmbiguousMatch
)
from .expected import title_contains, text_to_be_present_in_element
from .globals import (
    get_driver,
    get_default_wait_time,
    get_default_selector,
    initialize
)
from .helper import to_seconds, generate_target
from .result import Result, ResultDict

import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S"
)