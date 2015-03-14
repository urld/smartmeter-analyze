import logging
import logging.config
import os.path

__version__ = '0.2.0'

LOGGING_CONF = os.path.join(os.path.dirname(__file__), "logging.conf")
logging.config.fileConfig(LOGGING_CONF)
