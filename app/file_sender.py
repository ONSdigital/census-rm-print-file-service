import csv
import logging
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Collection, Iterable

from structlog import wrap_logger

import app.sftp as sftp
from app.encryption import pgp_encrypt_message
from app.manifest_file_builder import generate_manifest_file
from app.mappings import PACK_CODE_TO_DATASET, \
    SUPPLIER_TO_SFTP_DIRECTORY, DATASET_TO_SUPPLIER, DATASET_TO_PRINT_TEMPLATE
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def process_complete_file(print_file: Path, pack_code):
    supplier = DATASET_TO_SUPPLIER[PACK_CODE_TO_DATASET[pack_code]]

    logger.info('Encrypting print_file', file_name=print_file.name)
    encrypted_print_file, filename = encrypt_print_file(print_file, pack_code, supplier)

    manifest_file = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(f'{filename}.manifest')
    logger.info('Creating manifest print_file', manifest_file=manifest_file.name)
    generate_manifest_file(manifest_file, encrypted_print_file, pack_code)
    file_paths = [encrypted_print_file, manifest_file]

    logger.info('Sending files to SFTP', file_paths=list(map(str, file_paths)))
    copy_files_to_sftp(file_paths, SUPPLIER_TO_SFTP_DIRECTORY[supplier])

    # TODO upload encrypted print file and manifest to GCS

    file_paths.append(print_file)
    logger.info('Deleting local files', file_paths=list(map(str, file_paths)))
    delete_local_files(file_paths)


def encrypt_print_file(print_file, pack_code, supplier):
    encrypted_message = pgp_encrypt_message(print_file.read_text(), supplier)
    filename = f'{pack_code}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}'
    encrypted_print_file = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(f'{filename}.csv.gpg')
    logger.info('Writing encrypted file', file_name=encrypted_print_file.name)
    encrypted_print_file.write_text(encrypted_message)
    return encrypted_print_file, filename


def delete_local_files(file_paths: Iterable[Path]):
    for file_path in file_paths:
        file_path.unlink()


def quarantine_partial_file(partial_file_path: Path):
    quarantine_destination = Config.QUARANTINED_FILES_DIRECTORY.joinpath(partial_file_path.name)
    partial_file_path.replace(quarantine_destination)
    logger.info('Quarantined partial print file', quarantined_file_path=str(quarantine_destination))


def check_partial_files(partial_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        action_type, pack_code, batch_id, batch_quantity = print_file.name.split('.')
        actual_number_of_lines = sum(1 for _ in print_file.open())
        if int(batch_quantity) == actual_number_of_lines:
            if not check_partial_has_no_duplicates(print_file, pack_code):
                logger.info('Quarantining print file with duplicates', partial_file_name=print_file.name)
                quarantine_partial_file(print_file)
                return
            process_complete_file(print_file, pack_code)


def start_file_sender(readiness_queue):
    logger.info('Testing connection to SFTP target directories')
    with sftp.SftpUtility(Config.SFTP_QM_DIRECTORY):
        logger.info('Successfully connected to SFTP QM directory')
    with sftp.SftpUtility(Config.SFTP_PPO_DIRECTORY):
        logger.info('Successfully connected to SFTP PPD directory')
    readiness_queue.put(True)
    logger.info('Started file sender')
    while True:
        check_partial_files(Config.PARTIAL_FILES_DIRECTORY)
        sleep(Config.FILE_POLLING_DELAY_SECONDS)


def copy_files_to_sftp(file_paths: Collection[Path], remote_directory):
    with sftp.SftpUtility(remote_directory) as sftp_client:
        logger.info('Copying files to SFTP remote', sftp_directory=sftp_client.sftp_directory)
        for file_path in file_paths:
            sftp_client.put_file(local_path=str(file_path), filename=file_path.name)
        logger.info(f'All {len(file_paths)} files successfully written to SFTP remote',
                    sftp_directory=sftp_client.sftp_directory)


def check_partial_has_no_duplicates(partial_file_path: Path, pack_code: str):
    uacs = set()
    fieldnames = DATASET_TO_PRINT_TEMPLATE[PACK_CODE_TO_DATASET[pack_code]]
    with open(partial_file_path) as partial_file:
        reader = csv.DictReader(partial_file, fieldnames=fieldnames, delimiter='|')
        uac_columns = {fieldname for fieldname in fieldnames if 'uac' in fieldname}
        for line_number, row in enumerate(reader, 1):
            if any((row.get(uac_column) and row.get(uac_column) in uacs) for uac_column in uac_columns):
                logger.error('Duplicate uac found in print file',
                             partial_file_name=partial_file_path.name,
                             line_number=line_number)
                return False
            for uac_column in uac_columns:
                uacs.add(row[uac_column])
    return True
