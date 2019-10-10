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
    try:
        response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/reportexception', json=exception_report)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error('Error reporting exception', exception=e)


def quarantine_message(message_hash, body, service, queue, exception_class, routing_key, headers):
    quarantine = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body).decode(),
        'service': service,
        'queue': queue,
        'exceptionClass': exception_class,
        'routingKey': routing_key,
        'contentType': 'application/json',
        'headers': headers,
    }

    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/storeskippedmessage', json=quarantine)
    response.raise_for_status()
    return


def peek_message(message_hash, body):
    peek = {
        'messageHash': message_hash,
        'messagePayload': base64.b64encode(body).decode(),
    }

    response = requests.post(f'{Config.EXCEPTION_MANAGER_URL}/peekreply', json=peek)
    response.raise_for_status()
    return


def handle_error(channel, delivery_tag, body, exception: Exception, headers):
    message_hash = hashlib.sha256(body).hexdigest()
    exception_class = type(exception).__name__

    # Suppress exceptions here so that if any of the error advice process fails for any reasons,
    # we exit the context and fallback to default behaviour
    with suppress(Exception):
        advice = report_exception(message_hash, Config.NAME, Config.RABBIT_QUEUE, exception_class, str(exception))

        if advice['skipIt']:
            logger.warn('Attempting to quarantine and ack bad message message', message_hash=message_hash,
                        queue=Config.RABBIT_QUEUE, routing_key=Config.RABBIT_ROUTING_KEY)
            quarantine_message(message_hash, body, Config.NAME, Config.RABBIT_QUEUE, exception_class,
                               Config.RABBIT_ROUTING_KEY, headers)
            channel.basic_nack(delivery_tag=delivery_tag, requeue=False)
            return

        if advice['peek']:
            peek_message(message_hash, body)
            channel.basic_nack(delivery_tag=delivery_tag)
            return

        if not advice['logIt']:
            channel.basic_nack(delivery_tag=delivery_tag)
            return

    # Default/fallback behaviour is to log the error and nack the message
    logger.error('Failure processing message', message_hash=message_hash, exception=exception)
    channel.basic_nack(delivery_tag=delivery_tag)
    return
