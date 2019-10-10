import base64
import hashlib
import logging
from contextlib import suppress

import requests
from structlog import wrap_logger

from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def report_exception(message_hash, service, queue, exception_class, exception_trace):
    exception_report = {
        'messageHash': message_hash,
        'service': service,
        'queue': queue,
        'exceptionClass': exception_class,
        'exceptionMessage': exception_trace,
    }
    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/reportexception', json=exception_report)
    response.raise_for_status()
    return response.json()


def quarantine_message(message_hash, body, service, queue, exception_class, routing_key, headers):
    quarantine = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body),
        'service': service,
        'queue': queue,
        'exceptionClass': exception_class,
        'routingKey': routing_key,
        'contentType': 'application/json',
        'headers': headers,
    }
    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/storeskippedmessage', json=quarantine)
    response.raise_for_status()
    return response.json()


def peek_message(message_hash, body):
    peek = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body),
    }
    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/peekreply', json=peek)
    response.raise_for_status()
    return response.json()


def handle_bad_message(channel, delivery_tag, body, exception: Exception, queue, routing_key, headers):
    message_hash = hashlib.sha256(body).hexdigest()
    exception_class = type(exception).__name__

    # If any message exception service interaction fail we want to just log the error and nack
    with suppress(Exception):
        advice = report_exception(message_hash, Config.NAME, queue, exception_class, str(exception))

        if advice['skipIt']:
            logger.warn('Attempting to quarantine and ack bad message message', message_hash=message_hash, queue=queue,
                        routing_key=routing_key)
            quarantine_message(message_hash, body, Config.NAME, queue, exception_class, routing_key, headers)
            channel.basic_ack(delivery_tag=delivery_tag)
            return

        if advice['peek']:
            peek_message(message_hash, body)
            channel.basic_nack(delivery_tag=delivery_tag)
            return

        if not advice['logIt']:
            channel.basic_nack(delivery_tag=delivery_tag)
            return

    logger.error('Failure processing message', message_hash=message_hash, exception=exception)
    channel.basic_nack(delivery_tag=delivery_tag)
    return
