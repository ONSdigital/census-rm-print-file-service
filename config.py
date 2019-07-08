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
    SENT_FILES_DIRECTORY = Path(os.getenv('SENT_FILES_DIRECTORY', 'sent_files/'))
    ENCRYPTED_FILES_DIRECTORY = Path(os.getenv('ENCRYPTED_FILES_DIRECTORY', 'encrypted_files/'))

    READINESS_FILE_PATH = Path(os.getenv('READINESS_FILE_PATH', 'print-file-service-ready'))

    NAME = os.getenv('NAME', 'census-rm-print-file-service')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M%s')
    LOG_JSON_INDENT = os.getenv('LOG_JSON_INDENT')
    LOG_LEVEL_PIKA = os.getenv('LOG_LEVEL_PIKA', 'ERROR')
    SFTP_HOST = os.getenv('SFTP_HOST')
    SFTP_PORT = os.getenv('SFTP_PORT')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE')
    SFTP_PPD_DIRECTORY = os.getenv('SFTP_PPD_DIRECTORY')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY')
    OUR_PUBLIC_KEY_PATH = os.getenv('OUR_PUBLIC_KEY_PATH')
    OTHER_PUBLIC_KEY_PATH = os.getenv('OTHER_PUBLIC_KEY_PATH')


class DevConfig(Config):
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '6672')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME', 'guest')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'guest')
    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_keys/dummy_rsa')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'secret')
    SFTP_PPD_DIRECTORY = os.getenv('SFTP_PPD_DIRECTORY', 'ppd/')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY', 'qm/')
    OUR_PUBLIC_KEY_PATH = Path(os.getenv('OUR_PUBLIC_KEY_PATH') or Path(__file__).parent.joinpath('dummy_keys')
                               .joinpath('our_dummy_public.asc'))
    OTHER_PUBLIC_KEY_PATH = Path(os.getenv('OTHER_PUBLIC_KEY_PATH') or Path(__file__).parent.joinpath('dummy_keys')
                                 .joinpath('supplier_dummy_public.asc'))


class TestConfig(DevConfig):
    RABBIT_PORT = os.getenv('RABBIT_PORT', '35672')
    SFTP_PORT = os.getenv('SFTP_PORT', '2222')
    TMP_TEST_DIRECTORY = Path(__file__).parent.resolve().joinpath('tmp_test_files')
    PARTIAL_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('partial_files/')
    SENT_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('sent_files/')
    ENCRYPTED_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('encrypted_files/')


# Use dev defaults in dev environment
if os.getenv('ENVIRONMENT') == 'DEV':
    Config = DevConfig
elif os.getenv('ENVIRONMENT') == 'TEST':
    Config = TestConfig
