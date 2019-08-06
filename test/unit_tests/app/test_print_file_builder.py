import json

import pytest

from app.print_file_builder import generate_print_row, TemplateNotFoundError


def test_generate_print_row_valid_ICL1E(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "ICL1E",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "P_IC_ICL1"
    })

    # When
    generate_print_row(json_body, partial_files_directory)

    # Then
    generated_print_file = partial_files_directory.joinpath('ICL1E.P_IC_ICL1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|P_IC_ICL1\n')


def test_generate_print_row_valid_ICHHQE(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "ICHHQE",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "caseRef": "test_caseref",  # NB: ignored
        "fieldCoordinatorId": "test_qm_coordinator_id",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "P_IC_H1"
    })

    # When
    generate_print_row(json_body, partial_files_directory)

    # Then
    generated_print_file = partial_files_directory.joinpath('ICHHQE.P_IC_H1.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id|'
        '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1\n')


def test_generate_print_row_template_not_found(cleanup_test_files):
    # Given
    partial_files_directory = cleanup_test_files[1]
    json_body = json.dumps({
        "actionType": "NOT_A_VALID_ACTION_TYPE",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "c",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "PC_ICL_1"
    })

    # When/Then
    with pytest.raises(TemplateNotFoundError):
        generate_print_row(json_body, partial_files_directory)
