import logging
import sys

from structlog import configure, wrap_logger
from structlog.processors import TimeStamper, JSONRenderer
from structlog.stdlib import add_log_level, filter_by_level

from app.run_daemons import run_daemons
from config import Config


def run():
    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Starting print file service', logging_level=Config.LOG_LEVEL, logging_level_pika=Config.LOG_LEVEL_PIKA)
    initialise_directories()
    run_daemons()


def initialise_directories():
    Config.PARTIAL_FILES_DIRECTORY.mkdir(exist_ok=True)
    Config.SENT_FILES_DIRECTORY.mkdir(exist_ok=True)
    Config.ENCRYPTED_FILES_DIRECTORY.mkdir(exist_ok=True)
    Config.MANIFEST_FILES_DIRECTORY.mkdir(exist_ok=True)


def logger_initial_config(
        service_name=None, log_level=None, logger_format=None, logger_date_format=None
):
    if not logger_date_format:
        logger_date_format = Config.LOG_DATE_FORMAT
    if not log_level:
        log_level = Config.LOG_LEVEL
    if not logger_format:
        logger_format = "%(message)s"
    if not service_name:
        service_name = Config.NAME
    try:
        indent = int(Config.LOG_JSON_INDENT)
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

    logging.getLogger('pika').setLevel(Config.LOG_LEVEL_PIKA)


if __name__ == '__main__':
    run()
