from datetime import datetime
from unittest.mock import patch

import pytest

from app.constants import PackCode
from app.manifest_file_builder import create_manifest
from app.mappings import PACK_CODE_TO_DESCRIPTION, PACK_CODE_TO_DATASET
from test.unit_tests import RESOURCE_FILE_PATH


@patch('app.manifest_file_builder.datetime')
@pytest.mark.parametrize("pack_code", [pack_code for pack_code in PackCode])
def test_create_manifest(patch_datetime, pack_code):
    # Given
    dummy_print_file = RESOURCE_FILE_PATH.joinpath("dummy_print_file.txt")
    row_count = 100
    patched_date = datetime.utcnow()
    patch_datetime.utcnow.return_value = patched_date
    expected_manifest = {
        'schemaVersion': '1',
        'description': PACK_CODE_TO_DESCRIPTION[pack_code],
        'dataset': PACK_CODE_TO_DATASET[pack_code].value,
        'version': '1',
        'manifestCreated': patched_date.isoformat(timespec='milliseconds') + 'Z',
        'sourceName': 'ONS_RM',
        'files': [
            {
                'name': dummy_print_file.name,
                'relativePath': './',
                'sizeBytes': '19',  # Calculated size of the dummy print file
                'md5sum': '79cad6cda5ebe6b9bdbdbb6a56587e28',  # Calculated md5 of the dummy print file
                'rows': row_count
            }
        ]
    }

    # When
    actual_manifest = create_manifest(dummy_print_file, pack_code, row_count)

    assert expected_manifest == actual_manifest
