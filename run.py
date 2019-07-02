import multiprocessing
from _queue import Empty
from pathlib import Path
from time import sleep

import structlog

from config import Config
from file_sender import start_file_sender
from message_listener import start_message_listener
from readiness import Readiness

logger = structlog.get_logger()


def main():
    initialise_directories()
    process_manager = multiprocessing.Manager()
    file_sender_daemon = run_in_daemon(start_file_sender, 'file-sender', process_manager)
    message_listener_daemon = run_in_daemon(start_message_listener, 'message-listener', process_manager)
    logger.info('Successfully started print service!')

    with Readiness(Config.READINESS_FILE_PATH):
        while True:
            if not file_sender_daemon.is_alive():
                raise RuntimeError('File sender died')
            if not message_listener_daemon.is_alive():
                raise RuntimeError('Message listener died')
            sleep(1)


def run_in_daemon(target, name, process_manager, timeout=10) -> multiprocessing.Process:
    readiness_queue = process_manager.Queue()
    daemon = multiprocessing.Process(target=target, args=[readiness_queue], daemon=True, name=name)
    daemon.start()
    try:
        if readiness_queue.get(block=True, timeout=timeout):
            return daemon
    except Empty:
        raise RuntimeError(f'Error starting daemon: [{name}]')


def initialise_directories():
    Path('partial_files').mkdir(exist_ok=True)
    Path('complete_files').mkdir(exist_ok=True)
    Path('sent_files').mkdir(exist_ok=True)


if __name__ == '__main__':
    main()
