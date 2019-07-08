import json
import logging
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Collection

import hashlib
from structlog import wrap_logger

import app.sftp as sftp
from app.encryption import pgp_encrypt_message
from config import Config

QM_SUPPLIER = 'QM'
PPD_SUPPLIER = 'PPD'

PRODUCTPACK_CODE_TO_DESCRIPTION = {
    'P_IC_ICL1': 'Initial contact letter households - England',
    'P_IC_ICL2': 'Initial contact letter households - Wales',
    'P_IC_ICL4': 'Initial contact letter households - Northern Ireland',
    'P_IC_H1': 'Initial contact questionnaire households - England',
    'P_IC_H2': 'Initial contact questionnaire households - Wales',
    'P_IC_H4': 'Initial contact questionnaire households - Northern Ireland'
}

PACK_CODE_TO_SUPPLIER = {
    'P_IC_ICL1': PPD_SUPPLIER,
    'P_IC_ICL2': PPD_SUPPLIER,
    'P_IC_ICL4': PPD_SUPPLIER,
    'P_IC_H1': QM_SUPPLIER,
    'P_IC_H2': QM_SUPPLIER,
    'P_IC_H4': QM_SUPPLIER
}

SUPPLIER_TO_SFTP_DIRECTORY = {
    QM_SUPPLIER: Config.SFTP_QM_DIRECTORY,
    PPD_SUPPLIER: Config.SFTP_PPD_DIRECTORY
}


logger = wrap_logger(logging.getLogger(__name__))


def process_complete_file(file: Path, pack_code):
    message = file.read_text()
    supplier = PACK_CODE_TO_SUPPLIER[pack_code]
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
    copy_files_to_sftp(file_paths, SUPPLIER_TO_SFTP_DIRECTORY[supplier])

    # Move files to sent directory
    logger.info('Moving to sent files directory', file_paths=file_paths)
    for sent_file in file_paths:
        sent_file.replace(Config.SENT_FILES_DIRECTORY.joinpath(sent_file.name))


def check_files(partial_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        action_type, pack_code, batch_id, batch_quantity = print_file.name.split('.')
        actual_number_of_lines = sum(1 for _ in print_file.open())
        if int(batch_quantity) == actual_number_of_lines:
            process_complete_file(print_file, pack_code)
            logger.info('Removing unencrypted file', file_name=print_file.name)
            print_file.unlink()


def start_file_sender(readiness_queue):
    # TODO Connect to SFTP etc. before readying
    readiness_queue.put(True)
    logger.info('Started file sender')
    while True:
        check_files(Config.PARTIAL_FILES_DIRECTORY)
        sleep(2)


def copy_files_to_sftp(file_paths: Collection[Path], remote_directory):
    with sftp.SftpUtility(remote_directory) as sftp_client:
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
