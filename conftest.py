import os
import shutil
from collections import namedtuple

import pytest

# Set the ENVIRONMENT to TEST before the first time config is imported so the app uses TestConfig
os.environ['ENVIRONMENT'] = 'TEST'
from config import TestConfig, Config  # noqa: E402, out of order by necessity
from app.logger import logger_initial_config  # noqa: E402, out of order by necessity

TestDirectories = namedtuple('TestDirectories',
                             ['test_files', 'partial_files', 'encrypted_files', 'quarantined_files', 'sorting_files'])
MAX_FILE_SIZE_BYTES_PRESET = Config.MAX_FILE_SIZE_BYTES


@pytest.fixture
def cleanup_test_files():
    test_file_path = TestConfig.TMP_TEST_DIRECTORY
    if test_file_path.exists():
        shutil.rmtree(test_file_path)
    test_file_path.mkdir()
    cleanup_test_files.partial_files = TestConfig.PARTIAL_FILES_DIRECTORY
    encrypted_files_directory = TestConfig.ENCRYPTED_FILES_DIRECTORY
    quarantined_file_directory = TestConfig.QUARANTINED_FILES_DIRECTORY
    sorting_file_directory = TestConfig.SORTING_FILES_DIRECTORY
    cleanup_test_files.partial_files.mkdir(exist_ok=True)
    encrypted_files_directory.mkdir(exist_ok=True)
    quarantined_file_directory.mkdir(exist_ok=True)
    sorting_file_directory.mkdir(exist_ok=True)
    yield TestDirectories(test_file_path, cleanup_test_files.partial_files, encrypted_files_directory,
                          quarantined_file_directory, sorting_file_directory)
    shutil.rmtree(test_file_path)


@pytest.fixture
def reduce_max_partial_file_size():
    TestConfig.MAX_FILE_SIZE_BYTES = int(5 * 10 ** 2)
    yield
    TestConfig.MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_BYTES_PRESET


@pytest.fixture
def init_logger():
    logger_initial_config()
