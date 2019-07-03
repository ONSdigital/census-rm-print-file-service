import logging
import multiprocessing
from _queue import Empty
from time import sleep

from structlog import wrap_logger

from app.file_sender import start_file_sender
from app.message_listener import start_message_listener
from app.readiness_file import ReadinessFile
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def run_daemons():
    process_manager = multiprocessing.Manager()
    message_listener_daemon = run_in_daemon(start_message_listener, 'message-listener', process_manager)

    # File sender is stubbed
    file_sender_daemon = run_in_daemon(start_file_sender, 'file-sender', process_manager)

    logger.info('Successfully started print service!')

    with ReadinessFile(Config.READINESS_FILE_PATH):
        while True:
            if not file_sender_daemon.is_alive():
                raise RuntimeError('File sender died')
            if not message_listener_daemon.is_alive():
                raise RuntimeError('Message listener died')
            sleep(1)


def run_in_daemon(target, name, process_manager, timeout=3) -> multiprocessing.Process:
    readiness_queue = process_manager.Queue()
    daemon = multiprocessing.Process(target=target, args=[readiness_queue], daemon=True, name=name)
    daemon.start()
    try:
        if readiness_queue.get(block=True, timeout=timeout):
            return daemon
    except Empty:
        raise RuntimeError(f'Error starting daemon: [{name}]')
