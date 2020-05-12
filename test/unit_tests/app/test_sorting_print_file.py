import shutil
from pathlib import Path

from app.constants import ActionType, PackCode, PrintTemplate
from app.printfile_sorting import sort_print_file_if_required, get_column_indexes_by_name_from_template
from config import TestConfig
from test.unit_tests.app.test_file_sender import resource_file_path


def test_sorting_print_file():
    # struggling with test file paths at the moment...
    from_file = resource_file_path.joinpath('file_to_sort')
    to_file = TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('tmp_file_to_sort')

    complete_file_path = Path(shutil.copyfile(from_file, to_file))
    sorted_print_file = sort_print_file_if_required(complete_file_path, PackCode.D_CE1A_ICLCR1, ActionType.ICHHQE, None)

    correct_file = resource_file_path.joinpath('correctly_sorted_file')

    assert sorted_print_file.read_text() == correct_file.read_text()


# def test_packcode_for_not_sorting_not_sorted():
#     from_file = resource_file_path.joinpath('file_to_sort')
#     to_file = TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('tmp_file_to_sort')
#
#     complete_file_path = Path(shutil.copyfile(from_file, to_file))
#     sort_print_file(complete_file_path, [3, 5])
#     correct_file = resource_file_path.joinpath('correctly_sorted_file')
#
#     assert complete_file_path.read_text() == correct_file.read_text()
#
#     assert get_sorting_key_for_printfile('P_IC_ICL1') is None

def test_get_sort_indexes_from_template():
    sorting_key = get_column_indexes_by_name_from_template(template=PrintTemplate.PPO_LETTER_TEMPLATE,
                                                           columns=['fieldOfficerId', 'organisationName'])
    assert sorting_key == [14, 12]

