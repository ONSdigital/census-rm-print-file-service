import fnmatch
import json
from pathlib import Path
from time import sleep

import paramiko
import pgpy
import pytest

from app.rabbit_context import RabbitContext
from config import TestConfig

ICL1E_message_template = {
    "actionType": "ICL1E",
    "batchId": "1",
    "batchQuantity": None,
    "uac": "test_uac",
    "caseRef": "test_caseref",
    "title": "Mr",
    "forename": "Test",
    "surname": "McTest",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": "P_IC_ICL1"
}

ICHHQW_message_template = {
    "actionType": "ICHHQE",
    "batchId": "1",
    "batchQuantity": None,
    "uac": "english_uac",
    'qid': "english_qid",
    'uacWales': "welsh_uac",
    'qidWales': "welsh_qid",
    "caseRef": "test_caseref",
    "title": "Mr",
    "forename": "Test",
    "surname": "McTest",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": "P_IC_H2"
}


def test_end_to_end_with_ppd(clear_down_sftp_folders):
    # Given
    send_action_messages(ICL1E_message_template, quantity=3)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 ICL1E_message_template['packCode'])

    # Then
    with sftp.open(TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file) as actual_manifest_file:
        manifest_json = json.loads(actual_manifest_file.read())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['version'] == '1'
    assert manifest_json['description'] == 'Initial contact letter households - England'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'PPD1.1'
    assert manifest_json['files'][0]['relativePath'] == './'

    with sftp.open(TestConfig.SFTP_PPO_DIRECTORY + matched_print_file) as actual_print_file:
        decrypted_print_file = decrypt_message(actual_print_file.read(),
                                               Path(__file__).parents[2].joinpath('dummy_keys',
                                                                                  'dummy_ppd_supplier_private_key.asc'),
                                               'test')

    assert decrypted_print_file == (
        'test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n'
        'test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n'
        'test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_end_to_end_with_qm(clear_down_sftp_folders):
    # Given
    send_action_messages(ICHHQW_message_template, quantity=3)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 ICHHQW_message_template['packCode'])

    # Then
    with sftp.open(TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file) as actual_manifest_file:
        manifest_json = json.loads(actual_manifest_file.read())

    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['version'] == '1'
    assert manifest_json['description'] == 'Initial contact questionnaire households - Wales'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['dataset'] == 'QM3.2'
    assert manifest_json['files'][0]['relativePath'] == './'

    with sftp.open(TestConfig.SFTP_QM_DIRECTORY + matched_print_file) as actual_print_file:
        decrypted_print_file = decrypt_message(actual_print_file.read(),
                                               Path(__file__).parents[2].joinpath('dummy_keys',
                                                                                  'dummy_qm_supplier_private_key.asc'),
                                               'supplier')
    assert decrypted_print_file == (
        'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
        'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
        'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
        'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
        'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
        'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n')


def open_sftp_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()
    return sftp


def get_print_and_manifest_filenames(sftp, remote_directory, pack_code, max_attempts=10):
    attempts = 0
    while attempts <= max_attempts:
        matched_print_files = [filename for filename in sftp.listdir(remote_directory)
                               if fnmatch.fnmatch(filename, f'{pack_code}_*.csv')]
        matched_manifest_files = [filename for filename in sftp.listdir(remote_directory)
                                  if fnmatch.fnmatch(filename, f'{pack_code}_*.manifest')]
        attempts += 1
        if len(matched_print_files) and len(matched_manifest_files):
            break
        sleep(1)
    else:
        raise AssertionError('Reached timeout before files was created')
    assert len(matched_manifest_files) == 1
    assert len(matched_print_files) == 1
    return matched_manifest_files[0], matched_print_files[0]


def send_action_messages(message_dict, quantity):
    message_dict['batchQuantity'] = str(quantity)
    with RabbitContext() as rabbit:
        for _ in range(quantity):
            rabbit.channel.basic_publish(exchange='', routing_key=TestConfig.RABBIT_QUEUE,
                                         body=json.dumps(message_dict))


def decrypt_message(message, key_file_path, key_passphrase):
    key, _ = pgpy.PGPKey.from_file(key_file_path)
    with key.unlock(key_passphrase):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = key.decrypt(encrypted_text_message)
        return message_text.message


@pytest.fixture
def clear_down_sftp_folders():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].resolve().joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()

    for file in sftp.listdir(TestConfig.SFTP_PPO_DIRECTORY):
        sftp.remove(TestConfig.SFTP_PPO_DIRECTORY + file)

    for file in sftp.listdir(TestConfig.SFTP_QM_DIRECTORY):
        sftp.remove(TestConfig.SFTP_QM_DIRECTORY + file)
