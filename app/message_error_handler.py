import base64
import hashlib
import logging

import requests
from structlog import wrap_logger

from app.rabbit_context import RabbitContext
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def _report_exception_for_advice(message_hash, service, queue, exception_class, exception_trace):
    exception_report_payload = {
        'messageHash': message_hash,
        'service': service,
        'queue': queue,
        'exceptionClass': exception_class,
        'exceptionMessage': exception_trace,
    }

    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/reportexception', json=exception_report_payload)
    response.raise_for_status()
    return response.json()


def _quarantine_message(body: bytes, message_hash, exception_class, properties):
    _quarantine_message_in_exception_manager(body, message_hash, exception_class, properties.headers)
    _quarantine_message_in_rabbit(body, properties)


def _quarantine_message_in_exception_manager(body: bytes, message_hash, exception_class, headers):
    quarantine_payload = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body).decode(),
        'service': Config.NAME,
        'queue': Config.RABBIT_QUEUE,
        'exceptionClass': exception_class,
        'routingKey': Config.RABBIT_ROUTING_KEY,
        'contentType': 'application/json',
        'headers': headers,
    }

    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/storeskippedmessage', json=quarantine_payload)
    response.raise_for_status()


def _quarantine_message_in_rabbit(body: bytes, properties):
    with RabbitContext(queue_name=Config.RABBIT_QUARANTINE_QUEUE) as rabbit:
        rabbit.channel.basic_publish(Config.RABBIT_QUARANTINE_EXCHANGE,
                                     rabbit.queue_name,
                                     body,
                                     properties=properties,
                                     mandatory=True)


def _peek_message(message_hash, body: bytes):
    peek_payload = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body).decode(),
    }

    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/peekreply', json=peek_payload)
    response.raise_for_status()


def handle_message_error(message_body: bytes, exception: Exception, channel, delivery_tag, properties):
    message_hash = hashlib.sha256(message_body).hexdigest()
    exception_class = type(exception).__name__

    try:
        advice = _report_exception_for_advice(message_hash, Config.NAME, Config.RABBIT_QUEUE, exception_class,
                                              repr(exception))

        if advice.get('skipIt'):
            logger.warn('Attempting to quarantine and skip bad message', message_hash=message_hash,
                        queue=Config.RABBIT_QUEUE, routing_key=Config.RABBIT_ROUTING_KEY)
            _quarantine_message(message_body, message_hash, exception_class, properties)
            channel.basic_nack(delivery_tag=delivery_tag, requeue=False)
            logger.warn('Successfully quarantined and skipped bad message', message_hash=message_hash,
                        queue=Config.RABBIT_QUEUE, routing_key=Config.RABBIT_ROUTING_KEY)
            return

        elif advice.get('peek'):
            _peek_message(message_hash, message_body)
            channel.basic_nack(delivery_tag=delivery_tag)
            return

        elif not advice.get('logIt', True):
            channel.basic_nack(delivery_tag=delivery_tag)
            return

    except Exception as e:
        # Suppress exceptions here so that if any of the error advice process fails for any reasons,
        # we fallback to default behaviour
        logger.error('Exception handling advice failed', error_message=repr(e))

    # Default/fallback behaviour is to log the error and nack the message
    logger.error('Could not process message', message_hash=message_hash, exception=exception)
    channel.basic_nack(delivery_tag=delivery_tag)
