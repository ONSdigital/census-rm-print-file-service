import hashlib
import json
from enum import Enum
from queue import Queue
from unittest.mock import Mock, patch

from app.message_listener import print_message_callback, \
    start_message_listener


def test_invalid_action_types_are_nacked(cleanup_test_files, init_logger, caplog):
    # Given
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
    }).encode()
    actual_hash = hashlib.sha256(json_body).hexdigest()
    mock_channel = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'

    # When
    print_message_callback(mock_channel, mock_method, mock_properties, json_body, cleanup_test_files.partial_files)

    # Then
    mock_channel.basic_nack.assert_called_with(delivery_tag=mock_method.delivery_tag, requeue=False)
    mock_channel.basic_ack.assert_not_called()
    assert "'NOT_A_VALID_ACTION_TYPE' is not a valid ActionType" in caplog.text
    assert 'Could not process message' in caplog.text
    assert f'"message_hash": "{actual_hash}"' in caplog.text
    assert 'MalformedMessageError' in caplog.text


def test_valid_action_type_is_acked(cleanup_test_files):
    # Given
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
    }).encode()

    # When
    mock_channel = Mock()
    mock_method = Mock()
    print_message_callback(mock_channel, mock_method, Mock(), json_body, cleanup_test_files.partial_files)

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


def test_invalid_json_messages_are_nacked(cleanup_test_files, init_logger, caplog):
    # Given
    invalid_json_body = b"not_valid_json"
    actual_hash = hashlib.sha256(invalid_json_body).hexdigest()
    mock_channel = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'

    # When
    print_message_callback(mock_channel, mock_method, mock_properties, invalid_json_body,
                           cleanup_test_files.partial_files)

    # Then
    mock_channel.basic_nack.assert_called_with(delivery_tag=mock_method.delivery_tag, requeue=False)
    mock_channel.basic_ack.assert_not_called()
    assert 'Could not process message' in caplog.text
    assert f'"message_hash": "{actual_hash}"' in caplog.text
    assert 'JSONDecodeError' in caplog.text


def test_template_not_found_messages_are_nacked(cleanup_test_files, init_logger, caplog):
    # Given
    class MockActionType(Enum):
        VALID_ACTION_TYPE_NO_TEMPLATE = 'VALID_ACTION_TYPE_NO_TEMPLATE'

    json_body = json.dumps({
        "actionType": MockActionType.VALID_ACTION_TYPE_NO_TEMPLATE.value,
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
    }).encode()
    actual_hash = hashlib.sha256(json_body).hexdigest()
    mock_channel = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'

    # When
    with patch('app.print_file_builder.ActionType', new=MockActionType):
        print_message_callback(mock_channel, mock_method, mock_properties, json_body, cleanup_test_files.partial_files)

    # Then
    mock_channel.basic_nack.assert_called_with(delivery_tag=mock_method.delivery_tag, requeue=False)
    mock_channel.basic_ack.assert_not_called()
    assert 'Template not found for action type: \\"VALID_ACTION_TYPE_NO_TEMPLATE\\"' in caplog.text
    assert 'Could not process message' in caplog.text
    assert f'"message_hash": "{actual_hash}"' in caplog.text
    assert 'TemplateNotFoundError' in caplog.text
