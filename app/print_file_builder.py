import csv
import json
import logging
from pathlib import Path

from structlog import wrap_logger

from app.constants import ActionType, PackCode
from app.exceptions import TemplateNotFoundError, MalformedMessageError
from app.mappings import ACTION_TYPE_TO_PRINT_TEMPLATE

logger = wrap_logger(logging.getLogger(__name__))


def generate_print_row(json_body: str, partial_files_directory: Path):
    print_message = json.loads(json_body)
    action_type, pack_code, batch_id, batch_quantity = get_message_metadata(print_message)
    logger.debug('Generating print file line for message', action_type=action_type.value, pack_code=pack_code.value,
                 batch_quantity=batch_quantity, batch_id=batch_id)
    template = ACTION_TYPE_TO_PRINT_TEMPLATE.get(action_type)
    if not template:
        raise TemplateNotFoundError(f'Template not found for action type: "{action_type.value}"')
    partial_print_file = partial_files_directory.joinpath(
        build_filename(action_type, pack_code, batch_id, batch_quantity))
    append_print_row(print_message, template, partial_print_file)


def build_filename(action_type, pack_code, batch_id, batch_quantity):
    return '.'.join((action_type.value, pack_code.value, batch_id, str(batch_quantity)))


def append_print_row(print_message, template, partial_print_file: Path):
    with open(partial_print_file, 'a') as print_file_append:
        writer = csv.DictWriter(print_file_append, fieldnames=template, delimiter='|')
        writer.writerow({key: value for key, value in print_message.items() if key in template})


def get_message_metadata(print_message):

    try:
        action_type = ActionType(print_message['actionType'])
        pack_code = PackCode(print_message['packCode'])
        batch_id = print_message['batchId']
        batch_quantity = int(print_message['batchQuantity'])
    except (ValueError, KeyError) as e:
        raise MalformedMessageError(e)
    return action_type, pack_code, batch_id, batch_quantity
