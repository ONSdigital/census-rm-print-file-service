import fnmatch
import json
import uuid
from pathlib import Path
from time import sleep

import paramiko
import pgpy
import pytest

from app.rabbit_context import RabbitContext
from config import TestConfig

ICL_message_template = {
    "actionType": None,
    "batchId": None,
    "batchQuantity": None,
    "uac": None,
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
    "batchId": None,
    "batchQuantity": None,
    "uac": None,
    'qid': "english_qid",
    'uacWales': None,
    'qidWales': "welsh_qid",
    "caseRef": "test_caseref",
    "fieldCoordinatorId": "test_qm_coordinator_id",
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
    icl1e_messages, _ = build_test_messages(ICHHQ_message_template, 1, 'ICL1E', 'P_IC_ICL1')
    send_action_messages(icl1e_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL1')

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
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_icl2w_files():
    # Given
    icl2w_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL2B')
    send_action_messages(icl2w_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL2B')

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
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL2B\n')


def test_icl4n_files():
    # Given
    icl4n_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL4')
    send_action_messages(icl4n_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL4')

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
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL4\n')


def test_ichhqe_files():
    # Given
    ichhqe_messages, _ = build_test_messages(ICHHQ_message_template, 3, 'ICHHQE', 'P_IC_H1')
    send_action_messages(ichhqe_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H1')

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
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'))


def test_ichhqw_files():
    # Given
    ichhqw_messages, _ = build_test_messages(ICHHQ_message_template, 3, 'ICHHQW', 'P_IC_H2')
    send_action_messages(ichhqw_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H2')

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
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'))


def test_ichhqn_files():
    # Given
    ichhqn_messages, _ = build_test_messages(ICHHQ_message_template, 3, 'ICHHQN', 'P_IC_H4')
    send_action_messages(ichhqn_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H4')

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
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'))


def test_our_decryption_key():
    # Given
    icl1e_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL1E', 'P_IC_ICL1')
    send_action_messages(icl1e_messages)
    sftp = open_sftp_client()

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL1')

    # Then
    get_and_check_print_file(
        sftp=sftp,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'our_dummy_private.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_icl1e_with_duplicate_uacs_is_quarantined():
    # Given
    icl1e_messages, batch_id = build_test_messages(ICL_message_template, 3, 'ICL1E', 'P_IC_ICL1')
    icl1e_messages[0]['uac'] = 'test_duplicate'
    icl1e_messages[2]['uac'] = 'test_duplicate'
    send_action_messages(icl1e_messages)
    quarantined_files_directory = Path(__file__).parents[2].joinpath('working_files',
                                                                     'quarantined_files')
    expected_quarantined_file = quarantined_files_directory.joinpath(f'ICL1E.P_IC_ICL1.{batch_id}.3')

    # When
    for _attempt in range(10):
        if expected_quarantined_file.exists():
            break
        sleep(1)

    # Then
    assert expected_quarantined_file.read_text() == (
        'test_duplicate|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n'
        '1|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n'
        'test_duplicate|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_ichhqw_with_duplicate_uacs_is_quarantined():
    # Given
    icl1e_messages, batch_id = build_test_messages(ICHHQ_message_template, 3, 'ICHHQW', 'P_IC_H2')
    icl1e_messages[0]['uac'] = 'test_duplicate'
    icl1e_messages[2]['uacWales'] = 'test_duplicate'
    send_action_messages(icl1e_messages)
    quarantined_files_directory = Path(__file__).parents[2].joinpath('working_files',
                                                                     'quarantined_files')
    expected_quarantined_file = quarantined_files_directory.joinpath(f'ICHHQW.P_IC_H2.{batch_id}.3')

    # When
    for _attempt in range(10):
        if expected_quarantined_file.exists():
            break
        sleep(1)
    else:
        raise AssertionError('Reached max attempts before file was quarantined created')

    # Then
    assert expected_quarantined_file.read_text() == (
            'test_duplicate|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '4|english_qid|test_duplicate|welsh_qid|test_qm_coordinator_id|'
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
    for _attempt in range(max_attempts):
        matched_print_files = [filename for filename in sftp.listdir(remote_directory)
                               if fnmatch.fnmatch(filename, f'{pack_code}_*.csv.gpg')]
        matched_manifest_files = [filename for filename in sftp.listdir(remote_directory)
                                  if fnmatch.fnmatch(filename, f'{pack_code}_*.manifest')]
        if len(matched_print_files) and len(matched_manifest_files):
            break
        sleep(1)
    else:
        raise AssertionError('Reached max attempts before files were created')
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


def build_test_messages(message_template, quantity, action_type, pack_code):
    messages = []
    batch_id = str(uuid.uuid4())
    for _ in range(quantity):
        messages.append(message_template.copy())
    test_uac = 0
    for message in messages:
        message.update({'actionType': action_type,
                        'batchQuantity': quantity,
                        'packCode': pack_code,
                        'batchId': batch_id,
                        'uac': str(test_uac)})
        test_uac += 1
        if 'uacWales' in message_template.keys():
            message['uacWales'] = str(test_uac)
            test_uac += 1
    return messages, batch_id


def send_action_messages(message_dicts):
    with RabbitContext() as rabbit:
        for message_dict in message_dicts:
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
