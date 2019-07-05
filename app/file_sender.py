import hashlib
import os
from typing import Collection

import app.sftp as sftp
import json
import logging
from datetime import datetime
from pathlib import Path
from time import sleep

from structlog import wrap_logger

from app.encryption import pgp_encrypt_message
from config import Config


PRODUCTPACK_CODE_TO_DESCRIPTION = {
    'D_FD_H1': 'Household Questionnaire pack for England',
    'D_FD_H2': 'Household Questionnaire pack for Wales (English)',
    'D_FD_H2W': 'Household Questionnaire pack for Wales (Welsh)',
    'D_FD_H4': 'Household Questionnaire pack for Northern Ireland (English)',
    'D_FD_HC1': 'Continuation Questionnaire pack for England',
    'D_FD_HC2': 'Continuation Questionnaire pack for Wales (English)',
    'D_FD_HC2W': 'Continuation Questionnaire pack for Wales (Welsh)',
    'D_FD_HC4': 'Continuation Questionnaire pack for Northern Ireland (English)',
    'D_FD_I1': 'Individual Questionnaire pack for England',
    'D_FD_I2': 'Individual Questionnaire pack for Wales (English)',
    'D_FD_I2W': 'Individual Questionnaire pack for Wales (Welsh)',
    'D_FD_I4': 'Individual Questionnaire pack for Northern Ireland (English)',
    'D_CCS_CH1': 'CCS Interviewer Household Questionnaire for England and Wales',
    'D_CCS_CH2W': 'CCS Interviewer Household Questionnaire for Wales (Welsh)',
    'D_CCS_CHP1': 'CCS Postback Questionnaire for England and Wales (English)',
    'D_CCS_CHP2W': 'CCS Postback Questionnaire for Wales (Welsh)',
    'D_CCS_CCP1': 'CCS Postback Continuation Questionnaire for England & Wales',
    'D_CCS_CCP2W': 'CCS Postback Continuation Questionnaire for Wales (Welsh)',
    'D_CCS_CCE1': 'CCS Interviewer CE Manager for England & Wales (English)',
    'D_CCS_CCE2W': 'CCS Interviewer CE Manager for Wales (Welsh)',
    'P_IC_ICL1': 'Initial contact letter households - England',
    'P_IC_ICL2': 'Initial contact letter households - Wales',
    'P_IC_ICL4': 'Initial contact letter households - Northern Ireland',
    'P_IC_H1': 'Initial contact questionnaire households - England',
    'P_IC_H2': 'Initial contact questionnaire households - Wales',
    'P_IC_H4': 'Initial contact questionnaire households - Northern Ireland'
}


logger = wrap_logger(logging.getLogger(__name__))


def process_complete_file(file: Path, pack_code):
    message = file.read_text()
    # First encrypt the file and write it to encrypted directory
    logger.info('Encrypting file', file_name=file.name)
    encrypted_message = pgp_encrypt_message(message)
    filename = f'{pack_code}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}'
    print_file = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(f'{filename}.csv')
    logger.info('Writing encrypted file', file_name=print_file.name)
    with open(print_file, 'w') as encrypted_file:
        encrypted_file.write(encrypted_message)

    # Create the manifest
    manifest_file = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(f'{filename}.manifest')
    logger.info('Creating manifest file', manifest_file=manifest_file.name)
    generate_manifest_file(manifest_file, print_file, pack_code)
    file_paths = [print_file, manifest_file]

    # Send files to sftp
    logger.info('Sending files to SFTP', file_paths=file_paths)
    copy_files_to_sftp(file_paths)

    # Move files to sent directory
    logger.info('Moving to sent files directory', file_paths=file_paths)
    for sent_file in file_paths:
        sent_file.replace(Config.SENT_FILES_DIRECTORY.joinpath(sent_file.name))


def check_files(partial_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        file_name_parts = print_file.name.split('.')
        expected_number_of_lines = int(file_name_parts[3])
        pack_code = file_name_parts[1]
        actual_number_of_lines = sum(1 for _ in print_file.open())
        if expected_number_of_lines == actual_number_of_lines:
            process_complete_file(print_file, pack_code)
            logger.info('Removing unencrypted file', file_name=print_file.name)
            os.remove(print_file.as_posix())


def start_file_sender(readiness_queue):
    # TODO Connect to SFTP etc. before readying
    readiness_queue.put(True)
    logger.info('Started file sender')
    while True:
        check_files(Config.PARTIAL_FILES_DIRECTORY)
        sleep(2)


def copy_files_to_sftp(file_paths: Collection[Path]):
    with sftp.SftpUtility() as sftp_client:
        logger.info('Copying files to SFTP remote', sftp_directory=sftp_client.sftp_directory)
        for file_path in file_paths:
            sftp_client.put_file(local_path=str(file_path), filename=file_path.name)
        logger.info(f'All {len(file_paths)} files successfully written to SFTP remote',
                    sftp_directory=sftp_client.sftp_directory)


def generate_manifest_file(manifest_file_path: Path, print_file_path: Path, productpack_code: str):
    manifest = create_manifest(print_file_path, productpack_code)
    manifest_file_path.write_text(json.dumps(manifest))


def create_manifest(print_file_path: Path, productpack_code: str) -> dict:
    return {
        'schemaVersion': '1',
        'description': PRODUCTPACK_CODE_TO_DESCRIPTION[productpack_code],
        'dataset': 'PPD1.1',
        'version': '1',
        'manifestCreated': datetime.utcnow().isoformat(),
        'sourceName': 'ONS_RM',
        'files': [
            {
                'name': print_file_path.name,
                'relativePath': './',
                'sizeBytes': str(print_file_path.stat().st_size),
                'md5Sum': hashlib.md5(print_file_path.read_text().encode()).hexdigest()
            }
        ]
    }
