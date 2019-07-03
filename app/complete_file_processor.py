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


def process_complete_file(file: Path):
    # TODO Encrypt, create manifest, send to sftp, delete partial file
    action_type, pack_code, batch_id, batch_quantity = file.name.split('.')
    print_file_name = get_print_file_name(pack_code)

    # Encypt
    logger.info('Encrypting complete print file', file=file)
    encrypted_print_file_path = Config.ENCRYPTED_FILES_DIRECTORY.joinpath(print_file_name)
    encrypted_message = pgp_encrypt_message(file.read_text(), get_supplier_for_pack_code(pack_code))
    encrypted_print_file_path.write_text(encrypted_message)
    logger.info('Encrypted complete print file', file=file, encrypted_print_file=encrypted_print_file_path)

    # Create manifest
    logger.info('Generating manifest for encrypted print file', encrypted_print_file=encrypted_print_file_path)
    manifest_file_path = Config.MANIFEST_FILES_DIRECTORY.joinpath(f'{print_file_name}.manifest')
    generate_manifest_file(manifest_file_path, encrypted_print_file_path, pack_code)

    # Send to SFTP
    copy_files_to_sftp((manifest_file_path, encrypted_print_file_path), pack_code)

    # TODO Delete


def check_files(partial_files_dir: Path, sent_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        file_name_parts = print_file.name.split('.')
        expected_number_of_lines = int(file_name_parts[3])
        actual_number_of_lines = sum(1 for _ in print_file.open())

        if expected_number_of_lines == actual_number_of_lines:
            process_complete_file(print_file)
            print_file.replace(sent_files_dir.joinpath(print_file.name))
            logger.info(f"File hero has encrypted the file [{print_file}],"
                        f" created a manifest and SFTP'ed the two files")


def start_file_sender(readiness_queue):
    logger.info('Connecting to SFTP target directories')
    with SftpUtility(Config.QM_SFTP_DIRECTORY):
        logger.info('Connected to SFTP QM directory')
    with SftpUtility(Config.PPD_SFTP_DIRECTORY):
        logger.info('Connected to SFTP PPD directory')
    readiness_queue.put(True)
    logger.info('Started file sender')
    while True:
        check_files(Config.PARTIAL_FILES_DIRECTORY, Config.SENT_FILES_DIRECTORY)
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
        print(f'Copying files to SFTP remote {sftp_client.sftp_directory}')
        for file_path in file_paths:
            sftp_client.put_file(local_path=str(file_path), filename=file_path.name)
        print(f'All {len(file_paths)} files successfully written to {sftp_client.sftp_directory}')
