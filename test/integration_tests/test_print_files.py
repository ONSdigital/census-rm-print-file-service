import fnmatch
import json
from pathlib import Path
from time import sleep

import paramiko
import pgpy
import pytest

from app.constants import ActionType, PackCode
from config import TestConfig
from test.integration_tests.utilities import build_test_messages, send_action_messages, ICL_message_template, \
    print_questionnaire_message_template, P_OR_message_template, PPD1_3_message_template, reminder_message_template


def test_ICL1E(sftp_client):
    # Given
    icl1e_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL1E', 'P_IC_ICL1')
    send_action_messages(icl1e_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - England',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_ICL1E_split_files(sftp_client):
    # Given
    icl1e_messages, _ = build_test_messages(ICL_message_template, 20, 'ICL1E', 'P_IC_ICL1')
    send_action_messages(icl1e_messages)

    # When
    matched_manifest_files, matched_print_files = get_multiple_print_and_manifest_filenames(
        sftp_client, TestConfig.SFTP_PPO_DIRECTORY, 'P_IC_ICL1')

    # Then
    get_and_check_multiple_manifest_files(sftp=sftp_client, remote_manifest_directory=TestConfig.SFTP_PPO_DIRECTORY,
                                          manifest_files=matched_manifest_files,
                                          expected_values={'description': 'Initial contact letter households - England',
                                                           'dataset': 'PPD1.1'})

    get_and_check_multiple_print_files(
        sftp=sftp_client,
        remote_print_file_directory=TestConfig.SFTP_PPO_DIRECTORY,
        print_files=matched_print_files,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected=('0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '1|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '2|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '3|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '4|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '5|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '6|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '7|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '8|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '9|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '10|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '11|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '12|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '13|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '14|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '15|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '16|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '17|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '18|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '19|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
                  '20|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'))


def test_ICL2W(sftp_client):
    # Given
    icl2w_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL2B')
    send_action_messages(icl2w_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL2B')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL2B||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Wales',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_ICL4N(sftp_client):
    # Given
    icl4n_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL4')
    send_action_messages(icl4n_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL4||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Northern Ireland',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_ICHHQE(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQE', 'P_IC_H1')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1||\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1||\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - England',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_ICHHQW(sftp_client):
    # Given
    ichhqw_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQW', 'P_IC_H2')
    send_action_messages(ichhqw_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2||\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2||\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Wales',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_ICHHQN(sftp_client):
    # Given
    ichhqn_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQN', 'P_IC_H4')
    send_action_messages(ichhqn_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4||\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4||\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Northern Ireland',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_H1(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for England',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_H2(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_H2W(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H2W')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H2W')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_H4(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H4')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_HC1(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for England',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_HC2(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_HC2W(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC2W')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC2W')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_HC4(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC4')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4||\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4||\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_RL_1RL1_1(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RL_1RL1_1', 'P_RL_1RL1_1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RL_1RL1_1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RL_1RL1_1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': '1st Reminder, Letter - for England addresses',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_LP_HL1(sftp_client):
    # Given
    messages, _ = build_test_messages(PPD1_3_message_template, 1, 'P_LP_HLX', 'P_LP_HL1', uac=False)
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_LP_HL1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_LP_HL1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire Large Print pack for England',
                                    'dataset': 'PPD1.3'}, decrypted_print_file=decrypted_print_file)


def test_P_TB_TBPOL1(sftp_client):
    # Given
    messages, _ = build_test_messages(PPD1_3_message_template, 1, 'P_TB_TBX', 'P_TB_TBPOL1', uac=False)
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_TB_TBPOL1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_TB_TBPOL1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Translation Booklet for England & Wales - Polish',
                                    'dataset': 'PPD1.3'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_I1(sftp_client):
    # Given
    messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I1')
    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I1||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for England',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_I2(sftp_client):
    # Given
    messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I2')
    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I2||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_I2W(sftp_client):
    # Given
    messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I2W')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I2W')
    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I2W||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_OR_I4(sftp_client):
    # Given
    messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I4')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I4')
    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I4||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'}, decrypted_print_file=decrypted_print_file)


def test_P_QU_H2(sftp_client):
    # Given
    messages, _ = build_test_messages(print_questionnaire_message_template, 3, ActionType.P_QU_H2.value,
                                      PackCode.P_QU_H2.value)
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_QU_H2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2||\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2||\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2||\n'))

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': '3rd Reminder, Questionnaire - for Wales addresses',
                                    'dataset': 'QM3.3'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL1_1(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL1_1', 'P_RD_2RL1_1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL1_1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL1_1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 1 English',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL2B_1(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL2B_1', 'P_RD_2RL2B_1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL2B_1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL2B_1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 1 Welsh',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL1_2(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL1_2', 'P_RD_2RL1_2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL1_2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL1_2||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 2 English',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL2B_2(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL2B_2', 'P_RD_2RL2B_2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL2B_2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL2B_2||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 2 Welsh',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL1_3(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL1_3', 'P_RD_2RL1_3')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL1_3')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL1_3||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 3 English',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_P_RD_2RL2B_3(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RD_2RL2B_3', 'P_RD_2RL2B_3')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RD_2RL2B_3')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RD_2RL2B_3||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Response driven reminder group 3 Welsh',
                                    'dataset': 'PPD1.2'}, decrypted_print_file=decrypted_print_file)


def test_CE1_IC01(sftp_client):
    # Given
    ce1_ic01_messages, _ = build_test_messages(ICL_message_template, 1, 'CE1_IC01', 'D_CE1A_ICLCR1', ce=True)
    send_action_messages(ce1_ic01_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_CE1A_ICLCR1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_CE1A_ICLCR1|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'CE1 ICL with UAC for England (Hand Delivery) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE1_IC02(sftp_client):
    # Given
    ce1_ic02_messages, _ = build_test_messages(ICL_message_template, 1, 'CE1_IC02', 'D_CE1A_ICLCR2B', ce=True)
    send_action_messages(ce1_ic02_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_CE1A_ICLCR2B')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_CE1A_ICLCR2B|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'CE1 ICL with UAC for Wales (Hand Delivery) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC03_1(sftp_client):
    # Given
    ce_ic03_1_messages, _ = build_test_messages(ICL_message_template, 1, 'CE_IC03_1', 'D_ICA_ICLR1', ce=True)
    send_action_messages(ce_ic03_1_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_ICA_ICLR1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_ICA_ICLR1|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual ICL with UAC for England (Hand Delivery) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC04_1(sftp_client):
    # Given
    ce_ic04_1_messages, _ = build_test_messages(ICL_message_template, 1, 'CE_IC04_1', 'D_ICA_ICLR2B', ce=True)
    send_action_messages(ce_ic04_1_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_ICA_ICLR2B')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_ICA_ICLR2B|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual ICL with UAC for Wales (Hand Delivery) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC05(sftp_client):
    # Given
    ce_ic05_messages, _ = build_test_messages(ICL_message_template, 1, 'CE_IC05', 'D_CE4A_ICLR4', ce=True)
    send_action_messages(ce_ic05_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_CE4A_ICLR4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_CE4A_ICLR4|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'CE resident letter',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC06(sftp_client):
    # Given
    ce_ic06_messages, _ = build_test_messages(ICL_message_template, 1, 'CE_IC06', 'D_CE4A_ICLS4', ce=True)
    send_action_messages(ce_ic06_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'D_CE4A_ICLS4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|D_CE4A_ICLS4|english_qid|ONS'
                 '|ppo_field_coordinator_id|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'CE student letter',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC08(sftp_client):
    # Given
    ce_ic08_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'CE_IC08', 'D_FDCE_I4', ce=True)
    send_action_messages(ce_ic08_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'D_FDCE_I4')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected='0|english_qid|1|welsh_qid|ppo_field_coordinator_id||||123 Fake Street|Duffryn||Newport|NPXXXX'
                 '|D_FDCE_I4|ONS|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for NI (Hand delivery) Addressed',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC09(sftp_client):
    # Given
    ce_ic09_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'CE_IC09', 'D_FDCE_I1', ce=True)
    send_action_messages(ce_ic09_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'D_FDCE_I1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected='0|english_qid|1|welsh_qid|ppo_field_coordinator_id||||123 Fake Street|Duffryn||Newport|NPXXXX'
                 '|D_FDCE_I1|ONS|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for England (Hand delivery) Addressed',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_CE_IC10(sftp_client):
    # Given
    ce_ic10_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'CE_IC10', 'D_FDCE_I2',
                                              ce=True)
    send_action_messages(ce_ic10_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'D_FDCE_I2')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected='0|english_qid|1|welsh_qid|ppo_field_coordinator_id||||123 Fake Street|Duffryn||Newport|NPXXXX'
                 '|D_FDCE_I2|ONS|dummy_field_officer_id\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Wales (Hand delivery) Addressed',
                                    'dataset': 'QM3.2'}, decrypted_print_file=decrypted_print_file)


def test_SPG_IC11(sftp_client):
    # Given
    spg_ic11_messages, _ = build_test_messages(ICL_message_template, 1, 'SPG_IC11', 'P_ICCE_ICL1')
    send_action_messages(spg_ic11_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_ICCE_ICL1')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_ICCE_ICL1||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household ICL with UAC for England (Post Out) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_SPG_IC12(sftp_client):
    # Given
    spg_ic12_messages, _ = build_test_messages(ICL_message_template, 1, 'SPG_IC12', 'P_ICCE_ICL2B')
    send_action_messages(spg_ic12_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_ICCE_ICL2B')

    # Then
    decrypted_print_file = get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_ICCE_ICL2B||||\n')

    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household ICL with UAC for Wales (Post Out) Addressed',
                                    'dataset': 'PPD1.1'}, decrypted_print_file=decrypted_print_file)


def test_our_decryption_key(sftp_client):
    # Given
    icl1e_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL1E', 'P_IC_ICL1')
    send_action_messages(icl1e_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL1')

    # Then
    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'our_dummy_private.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n')


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
        pytest.fail('Reached max attempts before files were created')
    assert len(matched_manifest_files) == 1
    assert len(matched_print_files) == 1
    return matched_manifest_files[0], matched_print_files[0]


def get_multiple_print_and_manifest_filenames(sftp, remote_directory, pack_code, max_attempts=10):
    for _attempt in range(max_attempts):
        matched_print_files = [filename for filename in sftp.listdir(remote_directory)
                               if fnmatch.fnmatch(filename, f'{pack_code}_*.csv.gpg')]
        matched_manifest_files = [filename for filename in sftp.listdir(remote_directory)
                                  if fnmatch.fnmatch(filename, f'{pack_code}_*.manifest')]
        if len(matched_print_files) == 2 and len(matched_manifest_files) == 2:
            break
        sleep(5)
    else:
        pytest.fail('Reached max attempts before files were created')
    assert len(matched_manifest_files) == 2
    assert len(matched_print_files) == 2
    return matched_manifest_files, matched_print_files


def get_and_check_manifest_file(sftp, remote_manifest_path, expected_values, decrypted_print_file):
    with sftp.open(remote_manifest_path) as actual_manifest_file:
        manifest_json = json.loads(actual_manifest_file.read())
    for key, value in expected_values.items():
        assert manifest_json[key] == value
    actual_row_count = len(decrypted_print_file.splitlines())

    assert actual_row_count == manifest_json['files'][0]['rows']
    assert manifest_json['files'][0]['relativePath'] == './'
    assert manifest_json['sourceName'] == 'ONS_RM'
    assert manifest_json['schemaVersion'] == '1'
    assert manifest_json['version'] == '1'


def get_and_check_multiple_manifest_files(sftp, remote_manifest_directory, manifest_files, expected_values):
    remote_paths = [f'{remote_manifest_directory}{man_files}' for man_files in manifest_files]
    for remote_manifest_path in remote_paths:
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
    return decrypted_print_file


def get_and_check_multiple_print_files(sftp, remote_print_file_directory, print_files, decryption_key_path,
                                       decryption_key_passphrase, expected):
    print_file_paths = [f'{remote_print_file_directory}{print_file}' for print_file in print_files]
    for path in print_file_paths:
        with sftp.open(path) as actual_print_file:
            decrypted_print_file = decrypt_message(actual_print_file.read(),
                                                   decryption_key_path,
                                                   decryption_key_passphrase)
        assert decrypted_print_file in expected
        assert len(decrypted_print_file.splitlines()) == 10


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


@pytest.fixture()
def sftp_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    yield ssh_client.open_sftp()
    ssh_client.close()
