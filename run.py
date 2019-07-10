import logging
import sys

from structlog import configure, wrap_logger
from structlog.processors import TimeStamper, JSONRenderer
from structlog.stdlib import add_log_level, filter_by_level

from app.run_daemons import run_daemons
from config import Config


def run():
    Config.check_config()
    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Starting print file service', app_log_level=Config.LOG_LEVEL, pika_log_level=Config.LOG_LEVEL_PIKA,
                paramiko_log_level=Config.LOG_LEVEL_PARAMIKO, environment=Config.ENVIRONMENT)
    initialise_directories()
    run_daemons()


def initialise_directories():
    Config.PARTIAL_FILES_DIRECTORY.mkdir(exist_ok=True)
    Config.ENCRYPTED_FILES_DIRECTORY.mkdir(exist_ok=True)


def logger_initial_config():
    def add_service(_1, _2, event_dict):
        """
        Add the service name to the event dict.
        """
        event_dict["service"] = Config.NAME
        return event_dict

    logging.basicConfig(stream=sys.stdout, level=Config.LOG_LEVEL, format="%(message)s")

    configure(
        processors=[
            add_log_level,
            filter_by_level,
            add_service,
            TimeStamper(fmt=Config.LOG_DATE_FORMAT, utc=True, key="created_at"),
            JSONRenderer(),
        ]
    )

    logging.getLogger('pika').setLevel(Config.LOG_LEVEL_PIKA)
    logging.getLogger('paramiko').setLevel(Config.LOG_LEVEL_PARAMIKO)


if __name__ == '__main__':
    run()
