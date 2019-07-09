import fnmatch

import json
from pathlib import Path
from time import sleep

import paramiko
import pytest

from app.rabbit_context import RabbitContext
from config import TestConfig


ICL1E_message_template = {
    "actionType": "ICL1E",
    "batchId": "1",
    "batchQuantity": 3,
    "uac": "test_uac",
    "caseRef": "test_caseref",
    "title": "Mr",
    "forename": "Test",
    "surname": "McTest",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": "P_IC_ICL1"
}

ICHHQE_message_template = {
    "actionType": "ICHHQE",
    "batchId": "1",
    "batchQuantity": 3,
    "uac": "test_uac",
    "caseRef": "test_caseref",
    "title": "Mr",
    "forename": "Test",
    "surname": "McTest",
    "addressLine1": "123 Fake Street",
    "addressLine2": "Duffryn",
    "townName": "Newport",
    "postcode": "NPXXXX",
    "packCode": "P_IC_H1"
}


def test_end_to_end_with_ppd(clear_down_sftp_folders):
    with RabbitContext() as rabbit:
        for _ in range(3):
            rabbit.channel.basic_publish(exchange='', routing_key=TestConfig.RABBIT_QUEUE,
                                         body=json.dumps(ICL1E_message_template))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].resolve().joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()
    attempts = 0
    while attempts <= 10:
        matched_print_files = [filename for filename in sftp.listdir(TestConfig.SFTP_PPO_DIRECTORY)
                               if fnmatch.fnmatch(filename, 'P_IC_ICL1_*.csv')]
        matched_manifest_files = [filename for filename in sftp.listdir(TestConfig.SFTP_PPO_DIRECTORY)
                                  if fnmatch.fnmatch(filename, 'P_IC_ICL1_*.manifest')]
        attempts += 1
        if len(matched_print_files) and len(matched_manifest_files):
            break
        sleep(1)
    else:
        raise AssertionError('Reached timeout before files was created')

    assert len(matched_manifest_files) == 1
    assert len(matched_print_files) == 1


def test_end_to_end_with_qm(clear_down_sftp_folders):
    with RabbitContext() as rabbit:
        for _ in range(3):
            rabbit.channel.basic_publish(exchange='', routing_key=TestConfig.RABBIT_QUEUE,
                                         body=json.dumps(ICHHQE_message_template))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].resolve().joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()
    attempts = 0
    while attempts <= 10:
        matched_print_files = [filename for filename in sftp.listdir(TestConfig.SFTP_QM_DIRECTORY)
                               if fnmatch.fnmatch(filename, 'P_IC_H1_*.csv')]
        matched_manifest_files = [filename for filename in sftp.listdir(TestConfig.SFTP_QM_DIRECTORY)
                                  if fnmatch.fnmatch(filename, 'P_IC_H1_*.manifest')]
        attempts += 1
        if len(matched_print_files) and len(matched_manifest_files):
            break
        sleep(1)
    else:
        raise AssertionError('Reached timeout before files was created')

    assert len(matched_manifest_files) == 1
    assert len(matched_print_files) == 1


@pytest.fixture
def clear_down_sftp_folders():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=TestConfig.SFTP_HOST,
                       port=int(TestConfig.SFTP_PORT),
                       username=TestConfig.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].resolve().joinpath(TestConfig.SFTP_KEY_FILENAME)),
                       passphrase=TestConfig.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()

    for file in sftp.listdir(TestConfig.SFTP_PPO_DIRECTORY):
        sftp.remove(TestConfig.SFTP_PPO_DIRECTORY + file)

    for file in sftp.listdir(TestConfig.SFTP_QM_DIRECTORY):
        sftp.remove(TestConfig.SFTP_QM_DIRECTORY + file)
