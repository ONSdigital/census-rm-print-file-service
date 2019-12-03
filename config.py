import inspect
import os
from pathlib import Path


class MissingConfigError(Exception):
    pass


class Config:
    RABBIT_QUEUE = os.getenv('RABBIT_QUEUE', 'Action.Printer')
    RABBIT_EXCHANGE = os.getenv('RABBIT_EXCHANGE', 'action-outbound-exchange')
    RABBIT_HOST = os.getenv('RABBIT_HOST')
    RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
    RABBIT_VIRTUALHOST = os.getenv('RABBIT_VIRTUALHOST', '/')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')
    RABBIT_ROUTING_KEY = os.getenv('RABBIT_ROUTING_KEY', 'Action.Printer.binding')
    RABBIT_QUARANTINE_QUEUE = os.getenv('RABBIT_QUARANTINE_QUEUE', 'quarantineQueue')
    RABBIT_QUARANTINE_EXCHANGE = os.getenv('RABBIT_QUARANTINE_QUEUE', 'quarantineExchange')

    PARTIAL_FILES_DIRECTORY = Path(os.getenv('PARTIAL_FILES_DIRECTORY', 'partial_files/'))
    ENCRYPTED_FILES_DIRECTORY = Path(os.getenv('ENCRYPTED_FILES_DIRECTORY', 'encrypted_files/'))
    QUARANTINED_FILES_DIRECTORY = Path(os.getenv('QUARANTINED_FILES_DIRECTORY', 'quarantined_files/'))
    FILE_POLLING_DELAY_SECONDS = int(os.getenv('FILE_POLLING_DELAY_SECONDS', 10))

    READINESS_FILE_PATH = Path(os.getenv('READINESS_FILE_PATH', 'print-file-service-ready'))

    NAME = os.getenv('NAME', 'census-rm-print-file-service')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M%s')
    LOG_LEVEL_PIKA = os.getenv('LOG_LEVEL_PIKA', 'ERROR')
    LOG_LEVEL_PARAMIKO = os.getenv('LOG_LEVEL_PARAMIKO', 'ERROR')

    EXCEPTIONMANAGER_CONNECTION_HOST = os.getenv('EXCEPTIONMANAGER_CONNECTION_HOST')
    EXCEPTIONMANAGER_CONNECTION_PORT = os.getenv('EXCEPTIONMANAGER_CONNECTION_PORT')
    EXCEPTION_MANAGER_URL = f'http://{EXCEPTIONMANAGER_CONNECTION_HOST}:{EXCEPTIONMANAGER_CONNECTION_PORT}'

    SFTP_HOST = os.getenv('SFTP_HOST')
    SFTP_PORT = os.getenv('SFTP_PORT')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE')
    SFTP_PPO_DIRECTORY = os.getenv('SFTP_PPO_DIRECTORY')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY')

    MAX_FILE_SIZE_BYTES = int(os.getenv('MAX_FILE_SIZE_BYTES', 10 ** 9))

    OUR_PUBLIC_KEY_PATH = Path(os.getenv('OUR_PUBLIC_KEY_PATH')) if os.getenv('OUR_PUBLIC_KEY_PATH') else None
    QM_SUPPLIER_PUBLIC_KEY_PATH = Path(os.getenv('QM_SUPPLIER_PUBLIC_KEY_PATH')) if os.getenv(
        'QM_SUPPLIER_PUBLIC_KEY_PATH') else None
    PPO_SUPPLIER_PUBLIC_KEY_PATH = Path(os.getenv('PPO_SUPPLIER_PUBLIC_KEY_PATH')) if os.getenv(
        'PPO_SUPPLIER_PUBLIC_KEY_PATH') else None

    GNUPG_HOME = os.getenv('GNUPG_HOME')

    ENVIRONMENT = os.getenv('ENVIRONMENT', 'PROD')

    @classmethod
    def check_config(cls):
        missing_config_items = set()
        for config_key, config_value in (member for member in inspect.getmembers(cls) if
                                         not inspect.isbuiltin(member) and
                                         not inspect.isroutine(member) and
                                         not member[0].startswith('__') and
                                         not member[0].endswith('__')):
            if config_value is None:
                missing_config_items.add(config_key)
        if missing_config_items:
            raise MissingConfigError(f'Missing config items: {[item for item in missing_config_items]}')


class DevConfig(Config):
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '6672')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME', 'guest')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'guest')

    FILE_POLLING_DELAY_SECONDS = int(os.getenv('FILE_POLLING_DELAY_SECONDS', 1))

    EXCEPTIONMANAGER_CONNECTION_HOST = os.getenv('EXCEPTIONMANAGER_CONNECTION_HOST', 'localhost')
    EXCEPTIONMANAGER_CONNECTION_PORT = os.getenv('EXCEPTIONMANAGER_CONNECTION_PORT', '8666')
    EXCEPTION_MANAGER_URL = f'http://{EXCEPTIONMANAGER_CONNECTION_HOST}:{EXCEPTIONMANAGER_CONNECTION_PORT}'

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_keys/dummy_rsa')
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'secret')
    SFTP_PPO_DIRECTORY = os.getenv('SFTP_PPO_DIRECTORY', 'ppo_dev/print_services/')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY', 'qmprint_dev/print_services/')

    OUR_PUBLIC_KEY_PATH = Path(os.getenv('OUR_PUBLIC_KEY_PATH') or Path(__file__).parent.joinpath('dummy_keys')
                               .joinpath('our_dummy_public.asc'))
    QM_SUPPLIER_PUBLIC_KEY_PATH = Path(
        os.getenv('QM_SUPPLIER_PUBLIC_KEY_PATH') or Path(__file__).parent.joinpath('dummy_keys')
        .joinpath('dummy_qm_supplier_public_key.asc'))
    PPO_SUPPLIER_PUBLIC_KEY_PATH = Path(
        os.getenv('PPO_SUPPLIER_PUBLIC_KEY_PATH') or Path(__file__).parent.joinpath('dummy_keys')
        .joinpath('dummy_ppo_supplier_public_key.asc'))

    GNUPG_HOME = os.getenv('GNUPG_HOME', str(Path('~/.gnupg').absolute()))


class TestConfig(DevConfig):
    RABBIT_PORT = os.getenv('RABBIT_PORT', '35672')
    SFTP_PORT = os.getenv('SFTP_PORT', '2222')
    TMP_TEST_DIRECTORY = Path(__file__).parent.joinpath('tmp_test_files')
    PARTIAL_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('partial_files/')
    ENCRYPTED_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('encrypted_files/')
    QUARANTINED_FILES_DIRECTORY = TMP_TEST_DIRECTORY.joinpath('quarantined_files/')
    EXCEPTION_MANAGER_URL = 'http://test'


# Use dev or test defaults depending on environment
if Config.ENVIRONMENT == 'DEV':
    Config = DevConfig
elif Config.ENVIRONMENT == 'TEST':
    Config = TestConfig
