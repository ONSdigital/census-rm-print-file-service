from pathlib import Path

import pgpy
import pytest

from app.constants import Supplier
from app.encryption import pgp_encrypt_message

DUMMY_KEYS_PATH = Path(__file__).parents[3].joinpath('dummy_keys')


@pytest.mark.parametrize("supplier, supplier_key_path, supplier_passphrase",
                         [(Supplier.PPO, DUMMY_KEYS_PATH.joinpath('dummy_ppo_supplier_private_key.asc'), 'test'),
                          (Supplier.QM, DUMMY_KEYS_PATH.joinpath('dummy_qm_supplier_private_key.asc'), 'supplier')])
def test_pgp_encrypt_message(supplier, supplier_key_path, supplier_passphrase):
    # Given
    message = 'test_message'

    # When
    encrypted_message = pgp_encrypt_message(message, supplier)

    # Then
    supplier_decrypted_message = decrypt_message(encrypted_message,
                                                 supplier_key_path,
                                                 supplier_passphrase)

    rm_decrypted_message = decrypt_message(encrypted_message,
                                           DUMMY_KEYS_PATH.joinpath('our_dummy_private.asc'),
                                           'test')

    assert supplier_decrypted_message == message, 'Supplier key should be able to decrypt the message'
    assert rm_decrypted_message == message, 'RM key should be able to decrypt the message'


def decrypt_message(message, key_file_path, key_passphrase):
    key, _ = pgpy.PGPKey.from_file(key_file_path)
    with key.unlock(key_passphrase):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = key.decrypt(encrypted_text_message)
        return message_text.message
