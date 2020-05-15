import json

import pytest

from app.exceptions import MalformedMessageError
from app.print_file_builder import generate_print_row


def test_generate_print_row_valid_ICL1E(cleanup_test_files):
    # Given
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
        "packCode": "P_IC_ICL1",
        "qid": "",
        "organisationName": "",
        "fieldCoordinatorId": "",
        "fieldOfficerId": ""
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('ICL1E.P_IC_ICL1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|P_IC_ICL1||||\n')


def test_generate_print_row_valid_ICHHQE(cleanup_test_files):
    # Given
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
        "packCode": "P_IC_H1",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('ICHHQE.P_IC_H1.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id|'
        '|||123 Fake Street|Duffryn||Newport|NPXXXX|P_IC_H1|ONS|012345678\n')


def test_generate_print_row_valid_CE1_IC01(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE1_IC01",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_CE1A_ICLCR1",
        "qid": "31000000000093",
        "organisationName": "ONS",
        "fieldCoordinatorId": "123456789",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE1_IC01.D_CE1A_ICLCR1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|D_CE1A_ICLCR1|31000000000093'
                                                '|ONS|123456789|012345678\n')


def test_generate_print_row_valid_CE_IC03_1(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE_IC03_1",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_ICA_ICLR1",
        "qid": "21000000001234",
        "organisationName": "ONS",
        "fieldCoordinatorId": "123456789",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE_IC03_1.D_ICA_ICLR1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|D_ICA_ICLR1|21000000001234'
                                                '|ONS|123456789|012345678\n')


def test_generate_print_row_valid_CE_IC05(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE_IC05",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_CE4A_ICLR4",
        "qid": "31000000000093",
        "organisationName": "ONS",
        "fieldCoordinatorId": "123456789",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE_IC05.D_CE4A_ICLR4.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|D_CE4A_ICLR4|31000000000093'
                                                '|ONS|123456789|012345678\n')


def test_generate_print_row_valid_CE_IC08(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE_IC08",
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
        "packCode": "D_FDCE_I4",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE_IC08.D_FDCE_I4.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id||||123 Fake Street|Duffryn||Newport'
        '|NPXXXX|D_FDCE_I4|ONS|012345678\n')


def test_generate_print_row_valid_CE_IC09(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE_IC09",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "fieldCoordinatorId": "test_qm_coordinator_id",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_FDCE_I1",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE_IC09.D_FDCE_I1.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id||||123 Fake Street|Duffryn||Newport'
        '|NPXXXX|D_FDCE_I1|ONS|012345678\n')


def test_generate_print_row_valid_CE_IC10(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "CE_IC10",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "fieldCoordinatorId": "test_qm_coordinator_id",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_FDCE_I2",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('CE_IC10.D_FDCE_I2.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id||||123 Fake Street|Duffryn||Newport'
        '|NPXXXX|D_FDCE_I2|ONS|012345678\n')


def test_generate_print_row_valid_SPG_IC11(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "SPG_IC11",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "P_ICCE_ICL1",
        "qid": "21000000005678",
        "organisationName": "ONS",
        "fieldCoordinatorId": "123456789",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('SPG_IC11.P_ICCE_ICL1.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|P_ICCE_ICL1|21000000005678'
                                                '|ONS|123456789|012345678\n')


def test_generate_print_row_valid_SPG_IC12(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "SPG_IC12",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "caseRef": "test_caseref",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "P_ICCE_ICL2B",
        "qid": "21000000005555",
        "organisationName": "ONS",
        "fieldCoordinatorId": "123456789",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('SPG_IC12.P_ICCE_ICL2B.1.3')
    assert generated_print_file.read_text() == ('test_uac|test_caseref||||123 Fake Street'
                                                '|Duffryn||Newport|NPXXXX|P_ICCE_ICL2B|21000000005555'
                                                '|ONS|123456789|012345678\n')


def test_generate_print_row_valid_SPG_IC13(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "SPG_IC13",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "fieldCoordinatorId": "test_qm_coordinator_id",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_FDCE_H1",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('SPG_IC13.D_FDCE_H1.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id||||123 Fake Street|Duffryn||Newport'
        '|NPXXXX|D_FDCE_H1|ONS|012345678\n')


def test_generate_print_row_valid_SPG_IC14(cleanup_test_files):
    # Given
    json_body = json.dumps({
        "actionType": "SPG_IC14",
        "batchId": "1",
        "batchQuantity": 3,
        "uac": "test_uac",
        "qid": "test_qid",
        "uacWales": "test_wales_uac",
        "qidWales": "test_wales_qid",
        "fieldCoordinatorId": "test_qm_coordinator_id",
        "addressLine1": "123 Fake Street",
        "addressLine2": "Duffryn",
        "townName": "Newport",
        "postcode": "NPXXXX",
        "packCode": "D_FDCE_H2",
        "organisationName": "ONS",
        "fieldOfficerId": "012345678"
    })

    # When
    generate_print_row(json_body, cleanup_test_files.partial_files)

    # Then
    generated_print_file = cleanup_test_files.partial_files.joinpath('SPG_IC14.D_FDCE_H2.1.3')
    assert generated_print_file.read_text() == (
        'test_uac|test_qid|test_wales_uac|test_wales_qid|test_qm_coordinator_id||||123 Fake Street|Duffryn||Newport'
        '|NPXXXX|D_FDCE_H2|ONS|012345678\n')


def test_generate_print_row_invalid_action_type(cleanup_test_files):
    # Given
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
    with pytest.raises(MalformedMessageError):
        generate_print_row(json_body, cleanup_test_files.partial_files)
