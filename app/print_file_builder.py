import csv
import json
import logging
from pathlib import Path

from structlog import wrap_logger

from app.mappings import ACTION_TYPE_TO_PRINT_TEMPLATE

logger = wrap_logger(logging.getLogger(__name__))


class TemplateNotFoundError(Exception):
    pass


def generate_print_row(json_body: str, partial_file_path: Path):
    print_message = json.loads(json_body)
    logger.debug('Generating print file line for message', **print_message)
    template = ACTION_TYPE_TO_PRINT_TEMPLATE.get(print_message['actionType'])
    if not template:
        logger.error('No template found for action type', action_type=print_message.get('actionType'),
                     batch_id=print_message.get('batchId'))
        raise TemplateNotFoundError
    append_print_row(print_message, template, partial_file_path)


def get_filename(print_message):
    return (f"{print_message['actionType']}."
            f"{print_message['packCode']}."
            f"{print_message['batchId']}."
            f"{print_message['batchQuantity']}")


def append_print_row(print_message, template, partial_files_directory: Path):
    print_file = partial_files_directory.joinpath(get_filename(print_message))
    with open(print_file, 'a') as print_file_append:
        writer = csv.DictWriter(print_file_append, fieldnames=template, delimiter='|')
        writer.writerow({key: value for key, value in print_message.items() if key in template})
