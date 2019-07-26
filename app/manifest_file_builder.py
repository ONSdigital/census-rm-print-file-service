import hashlib
import json
from datetime import datetime
from pathlib import Path

from app.mappings import PRODUCTPACK_CODE_TO_DESCRIPTION, PACK_CODE_TO_DATASET


def generate_manifest_file(manifest_file_path: Path, print_file_path: Path, productpack_code: str):
    manifest = create_manifest(print_file_path, productpack_code)
    manifest_file_path.write_text(json.dumps(manifest))


def create_manifest(print_file_path: Path, productpack_code: str) -> dict:
    return {
        'schemaVersion': '1',
        'description': PRODUCTPACK_CODE_TO_DESCRIPTION[productpack_code],
        'dataset': PACK_CODE_TO_DATASET[productpack_code],
        'version': '1',
        'manifestCreated': datetime.utcnow().isoformat(),
        'sourceName': 'ONS_RM',
        'files': [
            {
                'name': print_file_path.name,
                'relativePath': './',
                'sizeBytes': str(print_file_path.stat().st_size),
                'md5Sum': hashlib.md5(print_file_path.read_text().encode()).hexdigest()
            }
        ]
    }
