from app.run_daemons import run_daemons
from config import Config
from configure_logging import logger_initial_config


def main():
    logger_initial_config()
    initialise_directories()
    run_daemons()


def initialise_directories():
    Config.PARTIAL_FILES_DIRECTORY.mkdir(exist_ok=True)
    Config.SENT_FILES_DIRECTORY.mkdir(exist_ok=True)


if __name__ == '__main__':
    main()
