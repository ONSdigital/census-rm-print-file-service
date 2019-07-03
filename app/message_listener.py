import csv
import functools
import json
import logging
from pathlib import Path

from structlog import wrap_logger

from app.rabbit_context import RabbitContext
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def start_message_listener(readiness_queue):
    logger.info('Starting print message listener')
    with RabbitContext() as rabbit:
        rabbit.channel.basic_consume(
            queue=rabbit.queue_name,
            on_message_callback=functools.partial(print_message_callback,
                                                  partial_file_path=Config.PARTIAL_FILES_DIRECTORY))
        readiness_queue.put(True)
        logger.info('Successfully started print message listener')
        rabbit.channel.start_consuming()


def print_message_callback(ch, method, _properties, body, partial_file_path: Path):
    try:
        generate_print_row(body, partial_file_path)
    except TemplateNotFoundError:
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return
    ch.basic_ack(delivery_tag=method.delivery_tag)


def generate_print_row(json_body: str, partial_file_path: Path):
    print_message = json.loads(json_body)
    logger.debug('Generating print file line for message', **print_message)
    template = get_template(print_message['actionType'])
    if not template:
        logger.error('No template found for action type', action_type=print_message.get('actionType'),
                     batch_id=print_message.get('batchId'))
        raise TemplateNotFoundError

    append_print_row(partial_file_path, print_message, template)


def get_filename(print_message):
    return (f"{print_message['actionType']}."
            f"{print_message['packCode']}."
            f"{print_message['batchId']}."
            f"{print_message['batchQuantity']}")


def append_print_row(partial_file_path: Path, print_message, template):
    print_file = partial_file_path.joinpath(get_filename(print_message))
    with open(print_file, 'a') as print_file_append:
        writer = csv.DictWriter(print_file_append, fieldnames=template, delimiter='|')
        writer.writerow({k: v for k, v in print_message.items() if k in template})


class TemplateNotFoundError(Exception):
    pass


def get_template(action_type: str):
    return {'ICL1E': INITIAL_CONTACT_TEMPLATE,
            'ICL2W': INITIAL_CONTACT_TEMPLATE,
            'ICL4N': INITIAL_CONTACT_TEMPLATE,
            'ICHHQE': QUESTIONNAIRE_TEMPLATE,
            'ICHHQW': QUESTIONNAIRE_TEMPLATE,
            'ICHHQN': QUESTIONNAIRE_TEMPLATE}.get(action_type)


INITIAL_CONTACT_TEMPLATE = ('uac',
                            'caseRef',
                            'title',
                            'forename',
                            'surname',
                            'addressLine1',
                            'addressLine2',
                            'addressLine3',
                            'townName',
                            'postcode',
                            'packCode')

QUESTIONNAIRE_TEMPLATE = ('uac',
                          'qid',
                          'uacWales',
                          'qidWales',
                          'caseRef',
                          'title',
                          'forename',
                          'surname',
                          'addressLine1',
                          'addressLine2',
                          'addressLine3',
                          'townName',
                          'postcode',
                          'packCode')
