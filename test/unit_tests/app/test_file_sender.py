import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, call

import paramiko
import pytest

from app.constants import PackCode
from app.file_sender import copy_files_to_sftp, process_complete_file, \
    check_partial_has_no_duplicates, quarantine_partial_file, check_partial_files, split_partial_file, \
    get_metadata_from_partial_file_name, write_file_to_bucket, upload_files_to_bucket
from app.manifest_file_builder import generate_manifest_file
from config import TestConfig
from google.cloud import exceptions

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
    context_logger = Mock()
    with patch('app.file_sender.sftp.SftpUtility') as patched_sftp, patch('app.file_sender.datetime') as patch_datetime:
        mock_time = datetime(2019, 1, 1, 7, 6, 5)
        patch_datetime.utcnow.return_value = mock_time
        process_complete_file(complete_file_path, PackCode.P_IC_ICL1, context_logger)

    put_sftp_call_kwargs = [kwargs for _, kwargs in
                            patched_sftp.return_value.__enter__.return_value.put_file.call_args_list]

    iso_mocked = mock_time.strftime("%Y-%m-%dT%H-%M-%S")

    assert put_sftp_call_kwargs[0]['local_path'] == str(
        cleanup_test_files.encrypted_files.joinpath(f'P_IC_ICL1_{iso_mocked}.csv.gpg'))
    assert put_sftp_call_kwargs[0]['filename'] == f'P_IC_ICL1_{iso_mocked}.csv.gpg'
    assert put_sftp_call_kwargs[1]['local_path'] == str(
        cleanup_test_files.encrypted_files.joinpath(f'P_IC_ICL1_{iso_mocked}.manifest'))
    assert put_sftp_call_kwargs[1]['filename'] == f'P_IC_ICL1_{iso_mocked}.manifest'


def test_processing_complete_file_splits_and_uploads_correct_files(cleanup_test_files, reduce_max_partial_file_size):
    # This file is roughly 800B and we've reduced the max file size limit to 500B
    shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.10'),
                    TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.10'))
    with patch('app.file_sender.datetime') as patch_datetime:
        mock_time = datetime(2019, 1, 1, 7, 6, 5)
        patch_datetime.utcnow.return_value = mock_time
        check_partial_files(TestConfig.PARTIAL_FILES_DIRECTORY)

    split_partial_files = list(Path(TestConfig.PARTIAL_FILES_DIRECTORY).iterdir())

    assert len(split_partial_files) == 2
    assert split_partial_files[1].name == 'ICL1E.P_IC_ICL1.1_1.5'
    assert split_partial_files[0].name == 'ICL1E.P_IC_ICL1.1_2.5'


def test_local_files_are_deleted_after_upload(cleanup_test_files):
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.1')))
    context_logger = Mock()
    with patch('app.file_sender.sftp.SftpUtility'):
        process_complete_file(complete_file_path, PackCode.P_IC_ICL1, context_logger)

    with pytest.raises(StopIteration):
        next(TestConfig.PARTIAL_FILES_DIRECTORY.iterdir())
    with pytest.raises(StopIteration):
        next(TestConfig.ENCRYPTED_FILES_DIRECTORY.iterdir())


def test_generating_manifest_file_ppd(cleanup_test_files):
    manifest_file = cleanup_test_files.encrypted_files.joinpath('P_IC_ICL1_2019-07-05T08-15-41.manifest')
    print_file = resource_file_path.joinpath('P_IC_ICL1_2019-07-05T08-15-41.csv.gpg')
    generate_manifest_file(manifest_file, print_file, PackCode.P_IC_ICL1)

    manifest_json = json.loads(manifest_file.read_text())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['description'] == 'Initial contact letter households - England'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'PPD1.1'


def test_generating_manifest_file_qm(cleanup_test_files):
    manifest_file = cleanup_test_files.encrypted_files.joinpath('P_IC_H1_2019-07-08T11-57-11.manifest')
    print_file = resource_file_path.joinpath('P_IC_H1_2019-07-08T11-57-11.csv.gpg')
    generate_manifest_file(manifest_file, print_file, PackCode.P_IC_H1)

    manifest_json = json.loads(manifest_file.read_text())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['description'] == 'Initial contact questionnaire households - England'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'QM3.2'


def test_check_partial_has_no_duplicates_with_duplicates(cleanup_test_files):
    # Given
    partial_duplicate_path = resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.2.duplicate_uac')
    mock_logger = Mock()

    # When
    result = check_partial_has_no_duplicates(partial_duplicate_path, PackCode.P_IC_ICL1, mock_logger)

    # Then
    assert not result, 'Check should return False for file with duplicates'
    mock_logger.error.assert_called_once_with('Duplicate uac found in print file', line_number=2)


def test_check_partial_has_no_duplicates_without_duplicates(cleanup_test_files):
    # Given
    partial_duplicate_path = resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.2')

    # When
    result = check_partial_has_no_duplicates(partial_duplicate_path, PackCode.P_IC_ICL1, Mock())

    # Then
    assert result


def test_quarantine_partial_file(cleanup_test_files):
    # Given
    partial_print_file = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.2.duplicate_uac'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.2')))
    partial_print_file_text = partial_print_file.read_text()
    expected_destination = Path(TestConfig.QUARANTINED_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.2'))

    # When
    quarantine_partial_file(partial_print_file)

    # Then
    assert not partial_print_file.exists()
    assert expected_destination.exists()
    assert expected_destination.read_text() == partial_print_file_text


def test_failed_encrypted_files_and_manifests_are_deleted(cleanup_test_files):
    # Given
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.1')))
    context_logger = Mock()
    sftp_failure_exception_message = 'Simulate SFTP transfer failure'

    def simulate_sftp_failure(*_args, **_kwargs):
        raise Exception(sftp_failure_exception_message)

    with patch('app.file_sender.sftp.paramiko.SSHClient') as client, \
            pytest.raises(Exception) as raised_exception:
        client.return_value.open_sftp.side_effect = simulate_sftp_failure

        # When
        process_complete_file(complete_file_path, PackCode.P_IC_ICL1, context_logger)

    # Then
    # Check encrypted_files_directory is empty
    assert not any(cleanup_test_files.encrypted_files.iterdir())

    # Check complete partial file is still there
    assert complete_file_path.exists()

    # Check original exception is re-raised
    assert str(raised_exception.value) == sftp_failure_exception_message


def test_check_partial_files_processes_complete_file(cleanup_test_files):
    # Given
    partial_file_path = Path(cleanup_test_files.partial_files.joinpath('ICL1E.P_IC_ICL1.1.1'))
    partial_file_path.touch()

    mock_storage_client = Mock()

    # When
    with patch('app.file_sender.sftp.paramiko.SSHClient') as client:
        client.return_value.open_sftp.return_value = mock_storage_client  # mock the sftp client connection
        mock_storage_client.stat.return_value.st_mode = paramiko.sftp_client.stat.S_IFDIR  # mock directory exists

        check_partial_files(cleanup_test_files.partial_files)
        client.assert_not_called()

        Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                             cleanup_test_files.partial_files.joinpath('ICL1E.P_IC_ICL1.1.1')))
        check_partial_files(cleanup_test_files.partial_files)

    # Then
    client.assert_called_once()


def test_split_partial_file(cleanup_test_files):
    # Given
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.8'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.8')))
    action_type, pack_code, batch_id, batch_quantity = get_metadata_from_partial_file_name(complete_file_path.name)

    # When
    split_partial_file(complete_file_path, action_type, pack_code, batch_id, int(batch_quantity))

    # Then
    split_partial_files = list(Path(TestConfig.PARTIAL_FILES_DIRECTORY).iterdir())

    assert len(split_partial_files) == 2

    for partial_file in split_partial_files:
        with open(partial_file, 'r') as split_file:
            split_file_lines = split_file.readlines()
            assert len(split_file_lines) == 4


def test_split_file_too_small(cleanup_test_files):
    # Given
    complete_file_path = Path(shutil.copyfile(resource_file_path.joinpath('ICL1E.P_IC_ICL1.1.1'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('ICL1E.P_IC_ICL1.1.1')))
    action_type, pack_code, batch_id, batch_quantity = get_metadata_from_partial_file_name(complete_file_path.name)

    # When
    with pytest.raises(ValueError) as e:
        split_partial_file(complete_file_path, action_type, pack_code, batch_id, int(batch_quantity))

    assert str(e.value) == 'Cannot split file with less than 2 rows'


def test_failing_write_to_gcp_bucket_is_handled():
    # When
    with patch('app.file_sender.storage.Client') as bucket_client:
        bucket_client.side_effect = exceptions.GoogleCloudError("bucket doesn't exist")

        try:
            write_file_to_bucket(None)
        except Exception:
            assert False, "Exception msgs from writing to GCP bucket should be handled"


def test_write_to_gcp_bucket():
    # Given
    test_printfile = Path('test1')
    test_manifest_file = Path('test2')
    mock_storage_client = Mock()
    mock_bucket = Mock()

    # When
    with patch('app.file_sender.storage') as google_storage, \
            patch('app.file_sender.Config') as config:
        config.SENT_PRINT_FILE_BUCKET = 'test'
        google_storage.Client.return_value = mock_storage_client  # mock the cloud client
        mock_storage_client.get_bucket.return_value = mock_bucket

        upload_files_to_bucket(test_printfile, test_manifest_file)

    mock_write_file = mock_bucket.blob

    # Then
    mock_write_file.assert_has_calls(
        [call('test1'), call().upload_from_filename(filename='test1'), call('test2'),
         call().upload_from_filename(filename='test2')])
