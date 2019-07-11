import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, call

import paramiko
import pytest

from app.file_sender import copy_files_to_sftp, generate_manifest_file, process_complete_file
from config import TestConfig

resource_file_path = Path(__file__).parents[2].joinpath('resources')


def test_copy_files_to_sftp():
    # Given
    test_files = [Path('test1'), Path('test2'), Path('test3')]
    os.environ['SFTP_DIRECTORY'] = 'test_path'
    mock_storage_client = Mock()

    # When
    with patch('app.file_sender.sftp.paramiko.SSHClient') as client:
        client.return_value.open_sftp.return_value = mock_storage_client  # mock the sftp client connection
        mock_storage_client.stat.return_value.st_mode = paramiko.sftp_client.stat.S_IFDIR  # mock directory exists
        copy_files_to_sftp(test_files, 'testdir')

    mock_put_file = mock_storage_client.put

    # Then
    mock_put_file.assert_has_calls(
        [call(str(file_path), file_path.name) for file_path in test_files])


def test_processing_complete_file_uploads_correct_files(cleanup_test_files):
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.1')))
    with patch('app.file_sender.sftp.SftpUtility') as patched_sftp, patch('app.file_sender.datetime') as patch_datetime:
        mock_time = datetime(2019, 1, 1, 7, 6, 5)
        patch_datetime.utcnow.return_value = mock_time
        process_complete_file(complete_file_path, 'P_IC_ICL1')

    put_sftp_call_kwargs = [kwargs for _, kwargs in
                            patched_sftp.return_value.__enter__.return_value.put_file.call_args_list]

    iso_mocked = mock_time.strftime("%Y-%m-%dT%H-%M-%S")

    assert put_sftp_call_kwargs[0]['local_path'] == str(
        cleanup_test_files[2].joinpath(f'P_IC_ICL1_{iso_mocked}.csv'))
    assert put_sftp_call_kwargs[0]['filename'] == f'P_IC_ICL1_{iso_mocked}.csv'
    assert put_sftp_call_kwargs[1]['local_path'] == str(
        cleanup_test_files[2].joinpath(f'P_IC_ICL1_{iso_mocked}.manifest'))
    assert put_sftp_call_kwargs[1]['filename'] == f'P_IC_ICL1_{iso_mocked}.manifest'


def test_local_files_are_deleted_after_upload(cleanup_test_files):
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.1')))
    with patch('app.file_sender.sftp.SftpUtility'):
        process_complete_file(complete_file_path, 'P_IC_ICL1')

    with pytest.raises(StopIteration):
        next(TestConfig.PARTIAL_FILES_DIRECTORY.iterdir())
    with pytest.raises(StopIteration):
        next(TestConfig.ENCRYPTED_FILES_DIRECTORY.iterdir())


def test_generating_manifest_file_ppd(cleanup_test_files):
    encrypted_directory = cleanup_test_files[2]
    manifest_file = encrypted_directory.joinpath('P_IC_ICL1_2019-07-05T08-15-41.manifest')
    print_file = resource_file_path.joinpath('P_IC_ICL1_2019-07-05T08-15-41.csv')
    generate_manifest_file(manifest_file, print_file, 'P_IC_ICL1')

    manifest_json = json.loads(manifest_file.read_text())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['description'] == 'Initial contact letter households - England'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'PPD1.1'


def test_generating_manifest_file_qm(cleanup_test_files):
    encrypted_directory = cleanup_test_files[2]
    manifest_file = encrypted_directory.joinpath('P_IC_H1_2019-07-08T11-57-11.manifest')
    print_file = resource_file_path.joinpath('P_IC_H1_2019-07-08T11-57-11.csv')
    generate_manifest_file(manifest_file, print_file, 'P_IC_H1')

    manifest_json = json.loads(manifest_file.read_text())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['description'] == 'Initial contact questionnaire households - England'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'QM3.2'
