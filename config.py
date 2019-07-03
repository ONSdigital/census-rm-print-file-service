import os
from pathlib import Path


class Config:
    RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "Action.Printer")
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_PORT = os.getenv("RABBIT_PORT", "6672")
    RABBIT_VIRTUALHOST = os.getenv("RABBIT_VIRTUALHOST", "/")
    RABBIT_USERNAME = os.getenv("RABBIT_USERNAME", "guest")
    RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "guest")

    PARTIAL_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'partial_files/'))
    SENT_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'sent_files/'))

    READINESS_FILE_PATH = Path(os.getenv('READINESS_FILE_PATH', 'print-file-service-ready'))

    NAME = os.getenv("NAME", "census-rm-print-file-service")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOGGING_DATE_FORMAT = os.getenv("LOGGING_DATE_FORMAT", "%Y-%m-%dT%H:%M%s")
    JSON_INDENT_LOGGING = os.getenv("JSON_INDENT_LOGGING")
