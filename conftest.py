import shutil
from pathlib import Path

import pytest


@pytest.fixture
def cleanup_test_files():
    test_file_path = Path(__file__).parent.resolve().joinpath('tmp_test_files')
    if test_file_path.exists():
        shutil.rmtree(test_file_path)
    test_file_path.mkdir()
    partial_files_directory = test_file_path.joinpath('partial_files/')
    encrypted_files_directory = test_file_path.joinpath('encrypted_files/')
    partial_files_directory.mkdir(exist_ok=True)
    encrypted_files_directory.mkdir(exist_ok=True)
    yield test_file_path, partial_files_directory, encrypted_files_directory
    shutil.rmtree(test_file_path)
