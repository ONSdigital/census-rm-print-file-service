import hashlib
import json
from datetime import datetime
from pathlib import Path

from app.constants import PackCode
from app.mappings import PACK_CODE_TO_DESCRIPTION, PACK_CODE_TO_DATASET


def generate_manifest_file(manifest_file_path: Path, print_file_path: Path, pack_code: PackCode):
    manifest = create_manifest(print_file_path, pack_code)
    manifest_file_path.write_text(json.dumps(manifest))


def create_manifest(print_file_path: Path, pack_code: PackCode) -> dict:
    return {
        'schemaVersion': '1',
        'description': PACK_CODE_TO_DESCRIPTION[pack_code],
        'dataset': PACK_CODE_TO_DATASET[pack_code].value,
        'version': '1',
        'manifestCreated': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
        'sourceName': 'ONS_RM',
        'files': [
            {
                'name': print_file_path.name,
                'relativePath': './',
                'sizeBytes': str(print_file_path.stat().st_size),
                'md5sum': hashlib.md5(print_file_path.read_text().encode()).hexdigest()
            }
        ]
    }
