import os
from pathlib import Path


class Config:
    RABBIT_QUEUE = os.getenv('RABBIT_QUEUE', 'Action.Printer')
    RABBIT_HOST = os.getenv('RABBIT_HOST')
    RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
    RABBIT_VIRTUALHOST = os.getenv('RABBIT_VIRTUALHOST', '/')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

    PARTIAL_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'partial_files/'))
    SENT_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'sent_files/'))
    ENCRYPTED_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'encrypted_files/'))
    MANIFEST_FILES_DIRECTORY = Path(os.getenv('MANIFEST_FILES_DIRECTORY', 'manifest_files/'))

    READINESS_FILE_PATH = Path(os.getenv('READINESS_FILE_PATH', 'print-file-service-ready'))

    NAME = os.getenv('NAME', 'census-rm-print-file-service')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M%s')
    LOG_JSON_INDENT = os.getenv('LOG_JSON_INDENT')
    LOG_LEVEL_PIKA = os.getenv('LOG_LEVEL_PIKA', 'ERROR')

    OUR_PUBLIC_KEY_PATH = os.getenv('OUR_PUBLIC_KEY_PATH')
    PPD_SUPPLIER_PUBLIC_KEY_PATH = os.getenv('PPD_SUPPLIER_PUBLIC_KEY_PATH')
    QM_SUPPLIER_PUBLIC_KEY_PATH = os.getenv('QM_SUPPLIER_PUBLIC_KEY_PATH')

    PPD_SFTP_DIRECTORY = os.getenv('PPD_SFTP_DIRECTORY')
    QM_SFTP_DIRECTORY = os.getenv('QM_SFTP_DIRECTORY')
    SFTP_HOST = os.getenv('SFTP_HOST')
    SFTP_PORT = int(os.getenv('SFTP_PORT', 22))
    SFTP_USERNAME = os.getenv('SFTP_USERNAME')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE')


class DevConfig(Config):
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '6672')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME', 'guest')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'guest')

    PPD_SFTP_DIRECTORY = os.getenv('PPD_SFTP_DIRECTORY', 'ppd/')
    QM_SFTP_DIRECTORY = os.getenv('QM_SFTP_DIRECTORY', 'qm/')
    OUR_PUBLIC_KEY_PATH = os.getenv('OUR_PUBLIC_KEY_PATH', 'dummy_keys/our_dummy_public.asc')
    PPD_SUPPLIER_PUBLIC_KEY_PATH = os.getenv('PPD_SUPPLIER_PUBLIC_KEY_PATH', 'dummy_keys/supplier_dummy_public.asc')
    QM_SUPPLIER_PUBLIC_KEY_PATH = os.getenv('QM_SUPPLIER_PUBLIC_KEY_PATH', 'dummy_keys/supplier_dummy_public.asc')

    SFTP_HOST = os.getenv('SFTP_HOST', 'sftp')
    SFTP_PORT = int(os.getenv('SFTP_PORT', 22))
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_keys/id_rsa')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'secret')


# Use dev defaults in dev environment
if os.getenv('ENVIRONMENT') == 'DEV':
    Config = DevConfig
