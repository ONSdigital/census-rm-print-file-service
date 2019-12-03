from pathlib import Path

from gnupg import GPG

from app.mappings import SUPPLIER_TO_KEY_PATH
from config import Config


class PrintFileEncrypter:

    def __init__(self):
        self.gpg = GPG(gnupghome=Config.GNUPG_HOME)
        self.supplier_to_fingerprint = {}
        self._import_supplier_keys()
        self.our_key_fingerprint = self._import_our_key()

    def _import_supplier_keys(self):
        for supplier, supplier_key_path in SUPPLIER_TO_KEY_PATH.items():
            with open(supplier_key_path, 'rb') as key:
                import_result = self.gpg.import_keys(key.read())
            self.supplier_to_fingerprint[supplier] = import_result.fingerprints[0]

    def _import_our_key(self):
        with open(Config.OUR_PUBLIC_KEY_PATH, 'rb') as our_key:
            import_result = self.gpg.import_keys(our_key.read())
        return import_result.fingerprints[0]

    def encrypt_print_file(self, print_file_path: Path, output_path: Path, supplier):
        print(f'ENCRYPTER:', output_path, str(output_path.absolute()))
        with open(print_file_path, 'rb') as print_file:
            self.gpg.encrypt_file(print_file,
                                  [self.our_key_fingerprint, self.supplier_to_fingerprint[supplier]],
                                  output=str(output_path.absolute()),
                                  symmetric='AES256')
