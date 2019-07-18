import logging
import multiprocessing
import queue
from time import sleep

from retrying import retry
from structlog import wrap_logger

from app.file_sender import start_file_sender
from app.message_listener import start_message_listener
from app.readiness_file import ReadinessFile
from config import Config

logger = wrap_logger(logging.getLogger(__name__))


class DaemonStartupError(Exception):
    pass


def run_daemons():
    process_manager = multiprocessing.Manager()
    message_listener_daemon = run_in_daemon(start_message_listener, 'message-listener', process_manager)
    file_sender_daemon = run_in_daemon(start_file_sender, 'file-sender', process_manager)

    with ReadinessFile(Config.READINESS_FILE_PATH):
        logger.info('Started print service')
        while True:
            if not file_sender_daemon.is_alive():
                logger.error('File sender daemon died, attempting to restart')
                file_sender_daemon = retry_run_daemon(start_file_sender, 'file-sender', process_manager)
            if not message_listener_daemon.is_alive():
                logger.error('Message listener daemon died, attempting to restart')
                message_listener_daemon = retry_run_daemon(start_message_listener, 'message-listener', process_manager)
            sleep(1)


def run_in_daemon(target, name, process_manager, timeout=3) -> multiprocessing.Process:
    readiness_queue = process_manager.Queue()
    daemon = multiprocessing.Process(target=target, args=[readiness_queue], daemon=True, name=name)
    daemon.start()
    try:
        if readiness_queue.get(block=True, timeout=timeout):
            return daemon
    except queue.Empty as err:
        raise DaemonStartupError(f'Error starting daemon: [{name}]') from err


@retry(wait_exponential_multiplier=1000, wait_exponential_max=20000, stop_max_attempt_number=10)
def retry_run_daemon(target, name, process_manager, timeout=3):
    return run_in_daemon(target, name, process_manager, timeout=timeout)
