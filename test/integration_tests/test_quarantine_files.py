from pathlib import Path
from time import sleep

import pytest

from test.integration_tests.utilities import build_test_messages, send_action_messages, ICL_message_template, \
    print_questionnaire_message_template

QUARANTINED_FILES_DIRECTORY = Path(__file__).parents[2].joinpath('working_files',
                                                                 'quarantined_files')


def test_icl1e_with_duplicate_uacs_is_quarantined():
    # Given
    messages, batch_id = build_test_messages(ICL_message_template, 3, 'ICL1E', 'P_IC_ICL1')
    messages[0]['uac'] = 'test_duplicate'
    messages[2]['uac'] = 'test_duplicate'
    send_action_messages(messages)
    expected_quarantined_file = QUARANTINED_FILES_DIRECTORY.joinpath(f'ICL1E.P_IC_ICL1.{batch_id}.3')

    # When
    wait_for_quarantined_file(expected_quarantined_file)

    # Then
    assert expected_quarantined_file.read_text() == (
        'test_duplicate|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
        '1|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n'
        'test_duplicate|test_caseref||||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n')


def test_ichhqw_with_duplicate_uacs_is_quarantined():
    # Given
    messages, batch_id = build_test_messages(print_questionnaire_message_template, 3, 'ICHHQW', 'P_IC_H2')
    messages[0]['uac'] = 'test_duplicate'
    messages[2]['uacWales'] = 'test_duplicate'
    send_action_messages(messages)
    expected_quarantined_file = QUARANTINED_FILES_DIRECTORY.joinpath(f'ICHHQW.P_IC_H2.{batch_id}.3')

    # When
    wait_for_quarantined_file(expected_quarantined_file)

    # Then
    assert expected_quarantined_file.read_text() == (
        'test_duplicate|english_qid|1|welsh_qid|test_qm_coordinator_id|'
        '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
        '2|english_qid|3|welsh_qid|test_qm_coordinator_id|'
        '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n'
        '4|english_qid|test_duplicate|welsh_qid|test_qm_coordinator_id|'
        '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H2\n')


def wait_for_quarantined_file(expected_quarantined_file, max_attempts=10):
    for _attempt in range(max_attempts):
        if expected_quarantined_file.exists():
            break
        sleep(1)
    else:
        pytest.fail('Reached max attempts before file was quarantined created')
