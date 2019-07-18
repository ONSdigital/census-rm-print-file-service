import logging
from pathlib import Path

from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


class ReadinessFile:
    def __init__(self, readiness_file: Path):
        self.readiness_file = readiness_file

    def __enter__(self):
        logger.debug('Creating readiness files', readiness_file_path=str(self.readiness_file))
        self.readiness_file.touch()

    def __exit__(self, *args):
        logger.debug('Removing readiness file', readiness_file_path=str(self.readiness_file))
        try:
            self.readiness_file.unlink()
        except FileNotFoundError:
            logger.error('Readiness file not found on exit', readiness_file_path=str(self.readiness_file))
