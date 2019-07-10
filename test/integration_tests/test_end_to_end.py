import fnmatch
import json
from pathlib import Path
from time import sleep

import paramiko
import pgpy
import pytest

from app.rabbit_context import RabbitContext
from config import TestConfig

ICL_message_template = {
    "actionType": None,
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
    "packCode": None
}

ICHHQ_message_template = {
    "actionType": None,
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
    "packCode": None
}


def test_icl1e_files():
    # Given
    icl1e_message = ICL_message_template.copy()
    icl1e_message.update({'actionType': 'ICL1E', 'batchQuantity': 1, 'packCode': 'P_IC_ICL1'})
    send_action_messages(icl1e_message, icl1e_message['batchQuantity'])
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 icl1e_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - England',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppd_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_icl2w_files():
    # Given
    icl2w_message = ICL_message_template.copy()
    icl2w_message.update({'actionType': 'ICL2W', 'batchQuantity': 1, 'packCode': 'P_IC_ICL2'})
    send_action_messages(icl2w_message, icl2w_message['batchQuantity'])
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 icl2w_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Wales',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppd_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL2\n')


def test_icl4n_files():
    # Given
    icl4n_message = ICL_message_template.copy()
    icl4n_message.update({'actionType': 'ICL2W', 'batchQuantity': 1, 'packCode': 'P_IC_ICL4'})
    send_action_messages(icl4n_message, icl4n_message['batchQuantity'])
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 icl4n_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Northern Ireland',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppd_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL4\n')


def test_ichhqe_files():
    # Given
    ichhqe_message = ICHHQ_message_template.copy()
    ichhqe_message.update({'actionType': 'ICHHQE', 'batchQuantity': 3, 'packCode': 'P_IC_H1'})
    send_action_messages(ichhqe_message, quantity=3)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 ichhqe_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - England',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'))


def test_ichhqw_files():
    # Given
    ichhqw_message = ICHHQ_message_template.copy()
    ichhqw_message.update({'actionType': 'ICHHQW', 'batchQuantity': 3, 'packCode': 'P_IC_H2'})
    send_action_messages(ichhqw_message, quantity=3)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 ichhqw_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Wales',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'))


def test_ichhqwn_files():
    # Given
    ichhqn_message = ICHHQ_message_template.copy()
    ichhqn_message.update({'actionType': 'ICHHQN', 'batchQuantity': 3, 'packCode': 'P_IC_H4'})
    send_action_messages(ichhqn_message, quantity=3)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 ichhqn_message['packCode'])

    # Then
    get_and_check_manifest_file(sftp=sftp,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Northern Ireland',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            'english_uac|english_qid|welsh_uac|welsh_qid|test_caseref|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'))


def test_our_decryption_key():
    # Given
    icl1e_message = ICL_message_template.copy()
    icl1e_message.update({'actionType': 'ICL1E', 'batchQuantity': 1, 'packCode': 'P_IC_ICL1'})
    send_action_messages(icl1e_message, icl1e_message['batchQuantity'])
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 icl1e_message['packCode'])

    # Then
    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'our_dummy_private.asc'),
        decryption_key_passphrase='test',
        expected='test_uac|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


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


def get_and_check_manifest_file(sftp, remote_manifest_path, expected_values):
    with sftp.open(remote_manifest_path) as actual_manifest_file:
        manifest_json = json.loads(actual_manifest_file.read())
    for key, value in expected_values.items():
        assert manifest_json[key] == value

    assert manifest_json['files'][0]['relativePath'] == './'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['version'] == '1'


def get_and_check_print_file(sftp, remote_print_file_path, decryption_key_path, decryption_key_passphrase, expected):
    with sftp.open(remote_print_file_path) as actual_print_file:
        decrypted_print_file = decrypt_message(actual_print_file.read(),
                                               decryption_key_path,
                                               decryption_key_passphrase)
    assert decrypted_print_file == expected


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


@pytest.fixture(autouse=True)
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
