from pathlib import Path
from time import sleep

import structlog

logger = structlog.get_logger()


def process_complete_file(file: Path):
    # Encrypt
    # create manifest
    # sftp
    logger.info(f'doing the file stuff on {file}')


def check_files(partial_files_dir: Path, sent_files_dir: Path):
    for print_file in partial_files_dir.rglob('*'):
        file_name_parts = print_file.name.split('.')
        expected_number_of_lines = int(file_name_parts[2])
        actual_number_of_lines = sum(1 for _ in print_file.open())

        if expected_number_of_lines == actual_number_of_lines:
            process_complete_file(print_file)
            print_file.replace(sent_files_dir.joinpath(print_file.name))
            logger.info(f"File hero has encrypted the file [{print_file}],"
                        f" created a manifest and SFTP'ed the two files")


def start_file_sender(readiness_queue):
    logger.info('Starting file sender')
    sent_files_dir = Path('sent_files')
    complete_files_dir = Path('complete_files')

    logger.info('Started file sender')
    readiness_queue.put(True)
    while True:
        check_files(complete_files_dir, sent_files_dir)
        sleep(2)
