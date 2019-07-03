import logging
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Collection

from structlog import wrap_logger

from app import sftp_utility
from app.encryption import pgp_encrypt_message
from app.manifest_builder import generate_manifest_file
from app.sftp_utility import SftpUtility
from config import Config

logger = wrap_logger(logging.getLogger(__name__))

QM_SUPPLIER = 'QM'
PPD_SUPPLIER = 'PPD'


def process_complete_file(print_file_path: Path):
    action_type, pack_code, batch_id, batch_quantity = print_file_path.name.split('.')
    print_file_name = get_print_file_name(pack_code)

    # Encrypt
    logger.info('Encrypting print file', file=str(print_file_path))
    encrypted_print_file_path = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(print_file_name)
    encrypted_message = pgp_encrypt_message(print_file_path.read_text(), get_supplier_for_pack_code(pack_code))
    encrypted_print_file_path.write_text(encrypted_message)
    logger.info('Encrypted print file', file=str(print_file_path), encrypted_print_file=str(encrypted_print_file_path))

    # Create manifest
    logger.info('Generating manifest for encrypted print file', encrypted_print_file=str(encrypted_print_file_path))
    manifest_file_path = Config.MANIFEST_FILES_DIRECTORY.joinpath(f'{print_file_name}.manifest')
    generate_manifest_file(manifest_file_path, encrypted_print_file_path, pack_code)

    # Send to SFTP
    logger.info('Sending encrypted print file and manifest to SFTP',
                encrypted_print_file=str(encrypted_print_file_path),
                manifest_file_path=str(manifest_file_path))
    copy_files_to_sftp((manifest_file_path, encrypted_print_file_path), pack_code)

    # Delete files
    # TODO Shred files?
    logger.info('Cleaning up local files',
                files_to_delete=[
                    str(file_path) for file_path in (print_file_path, encrypted_print_file_path, manifest_file_path)])
    print_file_path.unlink()
    encrypted_print_file_path.unlink()
    manifest_file_path.unlink()


def check_files(partial_files_dir: Path):
    for print_file_path in partial_files_dir.rglob('*'):
        file_name_parts = print_file_path.name.split('.')
        expected_number_of_lines = int(file_name_parts[3])
        actual_number_of_lines = sum(1 for _ in print_file_path.open())

        if expected_number_of_lines == actual_number_of_lines:
            logger.info('Processing complete print file', print_file_path=str(print_file_path))
            process_complete_file(print_file_path)
            logger.info('Finished processing print file', print_file_path=str(print_file_path))


def start_file_sender(readiness_queue):
    logger.info('Connecting to SFTP target directories')
    with SftpUtility(Config.QM_SFTP_DIRECTORY):
        logger.info('Connected to SFTP QM directory')
    with SftpUtility(Config.PPD_SFTP_DIRECTORY):
        logger.info('Connected to SFTP PPD directory')
    readiness_queue.put(True)
    logger.info('Started file sender')
    while True:
        check_files(Config.PARTIAL_FILES_DIRECTORY)
        sleep(2)


def get_supplier_for_pack_code(pack_code):
    return {
        'P_IC_H1': QM_SUPPLIER,
        'P_IC_H2': QM_SUPPLIER,
        'P_IC_H4': QM_SUPPLIER,
        'P_IC_ICL1': PPD_SUPPLIER,
        'P_IC_ICL2': PPD_SUPPLIER,
        'P_IC_ICL4': PPD_SUPPLIER,
    }[pack_code]


def get_print_file_name(pack_code):
    return f'{pack_code}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}.csv'


def get_sftp_directory(pack_code):
    return {
        'P_IC_H1': Config.QM_SFTP_DIRECTORY,
        'P_IC_H2': Config.QM_SFTP_DIRECTORY,
        'P_IC_H4': Config.QM_SFTP_DIRECTORY,
        'P_IC_ICL1': Config.PPD_SFTP_DIRECTORY,
        'P_IC_ICL2': Config.PPD_SFTP_DIRECTORY,
        'P_IC_ICL4': Config.PPD_SFTP_DIRECTORY,
    }[pack_code]


def copy_files_to_sftp(file_paths: Collection[Path], pack_code):
    with sftp_utility.SftpUtility(get_sftp_directory(pack_code)) as sftp_client:
        logger.info('Copying files to SFTP remote directory', remote_directory=sftp_client.sftp_directory)
        for file_path in file_paths:
            sftp_client.put_file(local_path=str(file_path), filename=file_path.name)
    logger.info('All files successfully written to SFTP', remote_directory=sftp_client.sftp_directory,
                files=[str(file_path) for file_path in file_paths])
