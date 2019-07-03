import logging
import sys

from structlog import configure
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import add_log_level, filter_by_level

from config import Config


def logger_initial_config(
        service_name=None, log_level=None, logger_format=None, logger_date_format=None
):
    if not logger_date_format:
        logger_date_format = Config.LOGGING_DATE_FORMAT
    if not log_level:
        log_level = Config.LOG_LEVEL
    if not logger_format:
        logger_format = "%(message)s"
    if not service_name:
        service_name = Config.NAME
    try:
        indent = int(Config.JSON_INDENT_LOGGING)
    except TypeError:
        indent = None
    except ValueError:
        indent = None

    def add_service(_1, _2, event_dict):
        """
        Add the service name to the event dict.
        """
        event_dict["service"] = service_name
        return event_dict

    logging.basicConfig(stream=sys.stdout, level=log_level, format=logger_format)

    configure(
        processors=[
            add_log_level,
            filter_by_level,
            add_service,
            TimeStamper(fmt=logger_date_format, utc=True, key="created_at"),
            JSONRenderer(indent=indent),
        ]
    )