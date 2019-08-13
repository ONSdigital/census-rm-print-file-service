import json
import uuid

from app.rabbit_context import RabbitContext
from config import TestConfig

ICL_message_template = {
    "actionType": None,
    "batchId": None,
    "batchQuantity": None,
    "uac": None,
    "caseRef": "test_caseref",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": None
}
ICHHQ_message_template = {
    "actionType": None,
    "batchId": None,
    "batchQuantity": None,
    "uac": None,
    'qid': "english_qid",
    'uacWales': None,
    'qidWales': "welsh_qid",
    "caseRef": "test_caseref",
    "fieldCoordinatorId": "test_qm_coordinator_id",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": None
}
P_OR_message_template = {
    "actionType": None,
    "batchId": None,
    "batchQuantity": None,
    "uac": None,
    "qid": "english_qid",
    "caseRef": "test_caseref",
    "title": "Mr",
    "forename": "Test",
    "surname": "McTest",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": None
}


def build_test_messages(message_template, quantity, action_type, pack_code):
    messages = []
    batch_id = str(uuid.uuid4())
    for _ in range(quantity):
        messages.append(message_template.copy())
    test_uac = 0
    for message in messages:
        message.update({'actionType': action_type,
                        'batchQuantity': quantity,
                        'packCode': pack_code,
                        'batchId': batch_id,
                        'uac': str(test_uac)})
        test_uac += 1
        if 'uacWales' in message_template.keys():
            message['uacWales'] = str(test_uac)
            test_uac += 1
    return messages, batch_id


def send_action_messages(message_dicts):
    with RabbitContext() as rabbit:
        for message_dict in message_dicts:
            rabbit.channel.basic_publish(exchange='', routing_key=TestConfig.RABBIT_QUEUE,
                                         body=json.dumps(message_dict))
