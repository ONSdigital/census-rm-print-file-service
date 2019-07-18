from unittest.mock import patch

import pytest

from app.run_daemons import DaemonStartupError, run_daemons


@patch('app.file_sender.sftp.SftpUtility')
@patch('app.message_listener.RabbitContext')
def test_sftp_failure_blocks_app_startup(_patched_sftp_utility, patched_sftp_utility):
    patched_sftp_utility.side_effect = raise_exception
    with pytest.raises(DaemonStartupError) as err:
        run_daemons()
        assert str(err) == 'Error starting daemon: [file-sender]'


@patch('app.file_sender.sftp.SftpUtility')
@patch('app.message_listener.RabbitContext')
def test_rabbit_connection_failure_blocks_app_startup(patched_rabbit_context, _patched_sftp_utility):
    patched_rabbit_context.side_effect = raise_exception
    with pytest.raises(DaemonStartupError) as err:
        run_daemons()
        assert str(err) == 'Error starting daemon: [message-listener]'


def raise_exception(*_, **_kwargs):
    raise Exception('An error happened')
