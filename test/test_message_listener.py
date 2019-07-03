import json
from queue import Queue
from unittest.mock import Mock, patch

import pytest

from message_listener import TemplateNotFoundError, generate_print_row, print_message_callback, start_message_listener


def test_generate_print_row_valid_ICL1E(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "ICL1E",
        "batchId": "1",
        "batchQuantity": 3,
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
    })

    # When
    generate_print_row(json_body, partial_files_directory)

    # Then
    generated_print_file = partial_files_directory.joinpath('ICL1E.P_IC_ICL1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref|Mr|Test|McTest|123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_generate_print_row_valid_ICHHQE(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "ICHHQE",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "caseRef": "test_caseref",
        "title": "Mr",
        "forename": "Test",
        "surname": "McTest",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "P_IC_H1"
    })

    # When
    generate_print_row(json_body, partial_files_directory)

    # Then
    generated_print_file = partial_files_directory.joinpath('ICHHQE.P_IC_H1.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_caseref|'
        'Mr|Test|McTest|123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n')


def test_generate_print_row_template_not_found(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "NOT_A_VALID_ACTION_TYPE",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "c",
        "title": "Mr",
        "forename": "Test",
        "surname": "McTest",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "PC_ICL_1"
    })

    # When/Then
    with pytest.raises(TemplateNotFoundError):
        generate_print_row(json_body, partial_files_directory)


def test_invalid_action_types_are_nacked(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "NOT_A_VALID_ACTION_TYPE",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "c",
        "title": "Mr",
        "forename": "Test",
        "surname": "McTest",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "PC_ICL_1"
    })

    # When
    mocked_channel = Mock()
    mocked_method = Mock()
    print_message_callback(mocked_channel, mocked_method, Mock(), json_body, partial_files_directory)

    # Then
    mocked_channel.basic_nack.assert_called_with(delivery_tag=mocked_method.delivery_tag)


def test_valid_action_type_is_acked(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "ICL1E",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "c",
        "title": "Mr",
        "forename": "Test",
        "surname": "McTest",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "PC_ICL_1"
    })

    # When
    mock_channel = Mock()
    mock_method = Mock()
    print_message_callback(mock_channel, mock_method, Mock(), json_body, partial_files_directory)

    # Then
    mock_channel.basic_ack.assert_called_with(delivery_tag=mock_method.delivery_tag)


def test_start_message_listener_queues_ready():
    # Given
    with patch('message_listener.RabbitContext'):
        readiness_queue = Queue()

        # When
        start_message_listener(readiness_queue)

    # Then
    assert readiness_queue.get(timeout=1)
