import csv
import logging
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Collection, Iterable

from structlog import wrap_logger

import app.sftp as sftp
from app.constants import PackCode, ActionType
from app.encryption import pgp_encrypt_message
from app.manifest_file_builder import generate_manifest_file
from app.mappings import PACK_CODE_TO_DATASET, \
    SUPPLIER_TO_SFTP_DIRECTORY, DATASET_TO_SUPPLIER, SUPPLIER_TO_PRINT_TEMPLATE
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def process_complete_file(complete_partial_file: Path, action_type: ActionType, pack_code: PackCode, batch_id,
                          batch_quantity, context_logger):
    supplier = DATASET_TO_SUPPLIER[PACK_CODE_TO_DATASET[pack_code]]

    context_logger.info('Encrypting print file')
    encrypted_print_file, filename = encrypt_print_file(complete_partial_file, pack_code, supplier)

    if is_file_over_size(encrypted_print_file):
        context_logger.info('Encrypted file too large, splitting it into two',
                            file_size_bytes=encrypted_print_file.stat().st_size)
        split_partial_file(complete_partial_file, action_type, pack_code, batch_id, int(batch_quantity))
        context_logger.info('File successfully split, removing encrypted file')
        encrypted_print_file.unlink()
        return

    manifest_file = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(f'{filename}.manifest')
    context_logger.info('Creating manifest for print file', manifest_file=manifest_file.name)
    generate_manifest_file(manifest_file, encrypted_print_file, pack_code)
    temporary_files_paths = [encrypted_print_file, manifest_file]

    context_logger.info('Sending files to SFTP', file_paths=list(map(str, temporary_files_paths)))

    try:
        copy_files_to_sftp(temporary_files_paths, SUPPLIER_TO_SFTP_DIRECTORY[supplier])

    except Exception as ex:
        context_logger.error('Failed to send files to SFTP', file_paths=list(map(str, temporary_files_paths)))
        context_logger.warn('Deleting failed encrypted and manifest print files',
                            file_paths=list(map(str, temporary_files_paths)))
        delete_local_files(temporary_files_paths)
        raise ex

    # TODO upload encrypted print file and manifest to GCS

    context_logger.info('Successfully sent print files to SFTP', file_paths=list(map(str, temporary_files_paths)))
    temporary_files_paths.append(complete_partial_file)
    context_logger.info('Deleting local files', file_paths=list(map(str, temporary_files_paths)))
    delete_local_files(temporary_files_paths)

    # Wait for a second so there is no chance of reusing the same file name
    sleep(1)


def is_file_over_size(_file: Path):
    return _file.lstat().st_size > Config.MAX_FILE_SIZE_BYTES


def split_partial_file(partial_file: Path, action_type: ActionType, pack_code: PackCode, batch_id,
                       batch_quantity: int):
    if batch_quantity < 2:
        raise ValueError('Cannot split file with less than 2 rows')

    first_chunk_quantity = batch_quantity // 2

    first_chunk_name = f'{action_type.value}.{pack_code.value}.{batch_id}_1.{first_chunk_quantity}'
    second_chunk_name = f'{action_type.value}.{pack_code.value}.{batch_id}_2.{batch_quantity - first_chunk_quantity}'

    # TODO use more memory efficient method to read/write partial file
    with open(partial_file) as open_partial_file:
        partial_file_lines = open_partial_file.readlines()
    first_chunk_path = Config.PARTIAL_FILES_DIRECTORY.joinpath(first_chunk_name)
    with open(first_chunk_path, 'w') as first_chunk_write:
        first_chunk_write.write(''.join(partial_file_lines[:first_chunk_quantity]))

    second_chunk_path = Config.PARTIAL_FILES_DIRECTORY.joinpath(second_chunk_name)
    with open(second_chunk_path, 'w') as second_chunk_write:
        second_chunk_write.write(''.join(partial_file_lines[first_chunk_quantity:]))
    del partial_file_lines

    partial_file.unlink()


def encrypt_print_file(print_file, pack_code: PackCode, supplier):
    encrypted_message = pgp_encrypt_message(print_file.read_text(), supplier)
    filename = f'{pack_code.value}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}'
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
    logger.warn('Quarantined partial print file', quarantined_file_path=str(quarantine_destination))


def check_partial_files(partial_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        action_type, pack_code, batch_id, batch_quantity = get_metadata_from_partial_file_name(print_file.name)
        actual_number_of_lines = sum(1 for _ in print_file.open())
        if int(batch_quantity) == actual_number_of_lines:
            context_logger = logger.bind(action_type=action_type.value,
                                         pack_code=pack_code.value,
                                         batch_id=batch_id,
                                         batch_quantity=batch_quantity)

            context_logger.info('Checking complete file for duplicates')
            if not check_partial_has_no_duplicates(print_file, pack_code):
                context_logger.warn('Quarantining print file with duplicates')
                quarantine_partial_file(print_file)
                return
            context_logger.info('File has no duplicates, beginning processing')
            process_complete_file(print_file, action_type, pack_code, batch_id, batch_quantity, context_logger)


def get_metadata_from_partial_file_name(partial_file_name: str):
    action_type, pack_code, batch_id, batch_quantity = partial_file_name.split('.')
    return ActionType(action_type), PackCode(pack_code), batch_id, batch_quantity


def start_file_sender(readiness_queue):
    logger.info('Testing connection to SFTP target directories')
    with sftp.SftpUtility(Config.SFTP_QM_DIRECTORY):
        logger.info('Successfully connected to SFTP QM directory', sftp_directory=Config.SFTP_QM_DIRECTORY)
    with sftp.SftpUtility(Config.SFTP_PPO_DIRECTORY):
        logger.info('Successfully connected to SFTP PPD directory', sftp_directory=Config.SFTP_PPO_DIRECTORY)
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


def check_partial_has_no_duplicates(partial_file_path: Path, pack_code: PackCode):
    uacs = set()
    fieldnames = SUPPLIER_TO_PRINT_TEMPLATE[DATASET_TO_SUPPLIER[PACK_CODE_TO_DATASET[pack_code]]]
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
