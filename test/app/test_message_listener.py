import json
from queue import Queue
from unittest.mock import Mock, patch

from app.message_listener import print_message_callback, \
    start_message_listener


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
        "packCode": "P_IC_ICL1"
    })

    # When
    mocked_channel = Mock()
    mocked_method = Mock()
    print_message_callback(mocked_channel, mocked_method, Mock(), json_body, partial_files_directory)

    # Then
    mocked_channel.basic_nack.assert_called_with(delivery_tag=mocked_method.delivery_tag)
    mocked_channel.basic_ack.assert_not_called()


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
        "packCode": "P_IC_ICL1"
    })

    # When
    mock_channel = Mock()
    mock_method = Mock()
    print_message_callback(mock_channel, mock_method, Mock(), json_body, partial_files_directory)

    # Then
    mock_channel.basic_ack.assert_called_with(delivery_tag=mock_method.delivery_tag)


@patch('app.message_listener.RabbitContext')
def test_start_message_listener_queues_ready(_patch_rabbit):
    # Given
    readiness_queue = Queue()

    # When
    start_message_listener(readiness_queue)

    # Then
    assert readiness_queue.get(timeout=1)
