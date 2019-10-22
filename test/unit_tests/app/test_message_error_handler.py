import base64
import hashlib
from unittest.mock import Mock, patch

import pika

from app.message_error_handler import handle_error
from config import TestConfig


def test_handle_error_reports_exception(init_logger, caplog):
    # Given
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')

    expected_exception_report = {
        'messageHash': message_hash,
        'service': TestConfig.NAME,
        'queue': TestConfig.RABBIT_QUEUE,
        'exceptionClass': type(processing_exception),
        'exceptionMessage': repr(processing_exception),
    }

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.side_effect = mock_reporting_failure
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    # Then
    assert patched_post.called_once_with(TestConfig.EXCEPTION_MANAGER_URL, expected_exception_report)


def test_handle_error_falls_back_on_logging(init_logger, caplog):
    # Given
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.side_effect = mock_reporting_failure
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    # Then
    assert 'Failure processing message' in caplog.text
    assert 'An exception during message processing' in caplog.text
    assert message_hash in caplog.text


def test_handle_error_log_it(init_logger, caplog):
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')
    mock_advice = {'logIt': True}

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.return_value.json.return_value = mock_advice
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    # Then
    assert 'Failure processing message' in caplog.text
    assert 'An exception during message processing' in caplog.text
    assert message_hash in caplog.text


def test_handle_error_no_log(init_logger, caplog):
    # Given
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')
    mock_advice = {'logIt': False}

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.return_value.json.return_value = mock_advice
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    assert 'Failure processing message' not in caplog.text
    assert message_hash not in caplog.text
    assert 'An exception during message processing' not in caplog.text


def test_handle_error_quarantine_message(init_logger, caplog):
    # Given
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')
    mock_advice = {'skipIt': True}
    expected_quarantine_message = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(message).decode(),
        'service': TestConfig.NAME,
        'queue': TestConfig.RABBIT_QUEUE,
        'exceptionClass': type(processing_exception).__name__,
        'routingKey': TestConfig.RABBIT_ROUTING_KEY,
        'contentType': 'application/json',
        'headers': None,
    }

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.return_value.json.return_value = mock_advice
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    post_calls = patched_post.call_args_list

    assert len(post_calls) == 2
    assert post_calls[1][0][0] == f'{TestConfig.EXCEPTION_MANAGER_URL}/storeskippedmessage'
    assert post_calls[1][1]['json'] == expected_quarantine_message

    assert 'Failure processing message' not in caplog.text
    assert '"event": "Attempting to quarantine and ack bad message message"' in caplog.text
    assert message_hash in caplog.text
    assert 'An exception during message processing' not in caplog.text


def test_handle_error_peek_message(init_logger, caplog):
    # Given
    mock_channel = Mock(pika.adapters.blocking_connection.BlockingChannel)
    mock_method = Mock()
    mock_properties = Mock()
    mock_properties.message_id = 'mock_message_id'
    message = b'Iamamessage'
    message_hash = hashlib.sha256(message).hexdigest()
    processing_exception = Exception('An exception during message processing')
    mock_advice = {'peek': True}
    expected_peek_message = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(message).decode(),
    }

    # When
    with patch('app.message_error_handler.requests.post') as patched_post:
        patched_post.return_value.json.return_value = mock_advice
        handle_error(mock_channel, mock_method.delivery_tag, message, processing_exception, None)

    post_calls = patched_post.call_args_list

    assert len(post_calls) == 2
    assert post_calls[1][0][0] == f'{TestConfig.EXCEPTION_MANAGER_URL}/peekreply'
    assert post_calls[1][1]['json'] == expected_peek_message

    assert 'Failure processing message' not in caplog.text
    assert message_hash not in caplog.text
    assert 'An exception during message processing' not in caplog.text


def mock_reporting_failure():
    raise Exception('Mocked failure to report exception')
