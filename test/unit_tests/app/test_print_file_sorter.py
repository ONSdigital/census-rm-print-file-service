import shutil
from pathlib import Path
from unittest.mock import Mock

from app.constants import ActionType, PackCode, PrintTemplate
from app.print_file_sorter import sort_print_file_if_required, get_column_indexes_by_name_from_template
from config import TestConfig
from test.unit_tests import RESOURCE_FILE_PATH


def test_sorting_print_file(cleanup_test_files):
    complete_file_path = Path(shutil.copyfile(RESOURCE_FILE_PATH.joinpath('file_to_sort'),
                                              TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('tmp_file_to_sort')))

    context_logger = Mock()
    sorted_print_file = sort_print_file_if_required(complete_file_path, PackCode.D_CE1A_ICLCR1, ActionType.ICHHQE,
                                                    context_logger)

    correct_file = RESOURCE_FILE_PATH.joinpath('correctly_sorted_file')

    assert sorted_print_file.read_text() == correct_file.read_text()


def test_packcode_for_not_sorting_not_sorted(cleanup_test_files):
    from_file = RESOURCE_FILE_PATH.joinpath('file_to_sort')
    to_file = TestConfig.PARTIAL_FILES_DIRECTORY.joinpath('tmp_file_to_sort')

    complete_file_path = Path(shutil.copyfile(from_file, to_file))
    unsorted_print_file = sort_print_file_if_required(complete_file_path, PackCode.P_IC_ICL1, ActionType.ICHHQE, None)

    assert unsorted_print_file.read_text() == from_file.read_text()


def test_get_sort_indexes_from_template():
    sorting_key = get_column_indexes_by_name_from_template(template=PrintTemplate.PPO_LETTER_TEMPLATE,
                                                           columns=['fieldOfficerId', 'organisationName'])
    assert sorting_key == [14, 12]
