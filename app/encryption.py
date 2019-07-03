import pgpy

from config import Config

PPD_SUPPLIER_KEY, _ = pgpy.PGPKey.from_file(Config.PPD_SUPPLIER_PUBLIC_KEY_PATH)
QM_SUPPLIER_KEY, _ = pgpy.PGPKey.from_file(Config.QM_SUPPLIER_PUBLIC_KEY_PATH)


class EncryptionFailedException(Exception):
    pass


def get_supplier_public_key(supplier):
    return {'PPD': PPD_SUPPLIER_KEY,
            'QM': QM_SUPPLIER_KEY}[supplier]


def pgp_encrypt_message(message, supplier):
    # A key can be loaded from a file, like so:
    our_key, _ = pgpy.PGPKey.from_file(Config.OUR_PUBLIC_KEY_PATH)
    supplier_key = get_supplier_public_key(supplier)

    # this creates a standard message from text
    # it will also be compressed, by default with ZIP DEFLATE, unless otherwise specified
    text_message = pgpy.PGPMessage.new(message)

    cipher = pgpy.constants.SymmetricKeyAlgorithm.AES256
    session_key = cipher.gen_key()

    # encrypt the message to multiple recipients
    encrypted_message_v1 = our_key.encrypt(text_message, cipher=cipher, sessionkey=session_key)
    encrypted_message_v2 = supplier_key.encrypt(encrypted_message_v1, cipher=cipher, sessionkey=session_key)

    # do at least this as soon as possible after encrypting to the final recipient
    del session_key

    if encrypted_message_v2.is_encrypted:
        return str(encrypted_message_v2)
    raise EncryptionFailedException
