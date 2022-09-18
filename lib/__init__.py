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