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
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - England',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_ICL2W(sftp_client):
    # Given
    icl2w_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL2B')
    send_action_messages(icl2w_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL2B')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Wales',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL2B\n')


def test_ICL4N(sftp_client):
    # Given
    icl4n_messages, _ = build_test_messages(ICL_message_template, 1, 'ICL2W', 'P_IC_ICL4')
    send_action_messages(icl4n_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_IC_ICL4')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact letter households - Northern Ireland',
                                    'dataset': 'PPD1.1'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL4\n')


def test_ICHHQE(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQE', 'P_IC_H1')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - England',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n'))


def test_ICHHQW(sftp_client):
    # Given
    ichhqw_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQW', 'P_IC_H2')
    send_action_messages(ichhqw_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H2')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Wales',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'))


def test_ICHHQN(sftp_client):
    # Given
    ichhqn_messages, _ = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQN', 'P_IC_H4')
    send_action_messages(ichhqn_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_IC_H4')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Initial contact questionnaire households - Northern Ireland',
                                    'dataset': 'QM3.2'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H4\n'))


def test_P_OR_H1(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for England',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H1\n'))


def test_P_OR_H2(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H2')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2\n'))


def test_P_OR_H2W(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H2W')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H2W')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H2W\n'))


def test_P_OR_H4(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_H4')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_H4')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_H4\n'))


def test_P_OR_HC1(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for England',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC1\n'))


def test_P_OR_HC2(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC2')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC2')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2\n'))


def test_P_OR_HC2W(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC2W')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC2W')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC2W\n'))


def test_P_OR_HC4(sftp_client):
    # Given
    messages, _ = build_test_messages(P_OR_message_template, 3, 'P_OR_HX', 'P_OR_HC4')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_HC4')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Continuation Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4\n'
            '1|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4\n'
            '2|english_qid||||Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_HC4\n'))


def test_P_RL_1RL1_1(sftp_client):
    # Given
    messages, _ = build_test_messages(reminder_message_template, 1, 'P_RL_1RL1_1', 'P_RL_1RL1_1')
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_RL_1RL1_1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': '1st Reminder, Letter - for England addresses',
                                    'dataset': 'PPD1.2'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_RL_1RL1_1\n')


def test_P_LP_HL1(sftp_client):
    # Given
    messages, _ = build_test_messages(PPD1_3_message_template, 1, 'P_LP_HLX', 'P_LP_HL1', uac=False)
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_LP_HL1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Household Questionnaire Large Print pack for England',
                                    'dataset': 'PPD1.3'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_LP_HL1\n')


def test_P_TB_TBPOL1(sftp_client):
    # Given
    messages, _ = build_test_messages(PPD1_3_message_template, 1, 'P_TB_TBX', 'P_TB_TBPOL1', uac=False)
    send_action_messages(messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_PPO_DIRECTORY,
                                                                                 'P_TB_TBPOL1')

    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_PPO_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Translation Booklet for England & Wales - Polish',
                                    'dataset': 'PPD1.3'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_PPO_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_ppo_supplier_private_key.asc'),
        decryption_key_passphrase='test',
        expected='|test_caseref|Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_TB_TBPOL1\n')


def test_P_OR_I1(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I1')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I1')
    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for England',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I1\n'))


def test_P_OR_I2(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I2')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I2')
    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Wales (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I2\n'))


def test_P_OR_I2W(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I2W')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I2W')
    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Wales (Welsh)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I2W\n'))


def test_P_OR_I4(sftp_client):
    # Given
    ichhqe_messages, _ = build_test_messages(print_questionnaire_message_template, 1, 'P_OR_IX', 'P_OR_I4')
    send_action_messages(ichhqe_messages)

    # When
    matched_manifest_file, matched_print_file = get_print_and_manifest_filenames(sftp_client,
                                                                                 TestConfig.SFTP_QM_DIRECTORY,
                                                                                 'P_OR_I4')
    # Then
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': 'Individual Questionnaire for Northern Ireland (English)',
                                    'dataset': 'QM3.4'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_OR_I4\n'))


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
    get_and_check_manifest_file(sftp=sftp_client,
                                remote_manifest_path=TestConfig.SFTP_QM_DIRECTORY + matched_manifest_file,
                                expected_values={
                                    'description': '3rd Reminder, Questionnaire - for Wales addresses',
                                    'dataset': 'QM3.3'})

    get_and_check_print_file(
        sftp=sftp_client,
        remote_print_file_path=TestConfig.SFTP_QM_DIRECTORY + matched_print_file,
        decryption_key_path=Path(__file__).parents[2].joinpath('dummy_keys',
                                                               'dummy_qm_supplier_private_key.asc'),
        decryption_key_passphrase='supplier',
        expected=(
            '0|english_qid|1|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2\n'
            '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2\n'
            '4|english_qid|5|welsh_qid|test_qm_coordinator_id|'
            '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_QU_H2\n'))


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
        expected='0|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


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
