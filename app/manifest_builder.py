import hashlib
import json
from datetime import datetime
from pathlib import Path

QM_DATASET = 'QM3.2'
PPD_DATASET = 'PPD1.1'


def get_description_for_productpack_code(productpack_code):
    return {
        # TODO
        'P_IC_H1': 'placeholder',
        'P_IC_H2': 'placeholder',
        'P_IC_H4': 'placeholder',
        'P_IC_ICL1': 'placeholder',
        'P_IC_ICL2': 'placeholder',
        'P_IC_ICL4': 'placeholder',
    }[productpack_code]


def get_dataset_for_productpack_code(productpack_code):
    return {
        'P_IC_H1': QM_DATASET,
        'P_IC_H2': QM_DATASET,
        'P_IC_H4': QM_DATASET,
        'P_IC_ICL1': PPD_DATASET,
        'P_IC_ICL2': PPD_DATASET,
        'P_IC_ICL4': PPD_DATASET,
    }[productpack_code]


def generate_manifest_file(manifest_file_path: Path, print_file_path: Path, productpack_code: str):
    manifest = create_manifest(print_file_path, productpack_code)
    manifest_file_path.write_text(json.dumps(manifest))


def create_manifest(print_file_path: Path, productpack_code: str) -> dict:
    return {
        'schemaVersion': '1',
        'description': get_description_for_productpack_code(productpack_code),
        'dataset': get_dataset_for_productpack_code(productpack_code),
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
