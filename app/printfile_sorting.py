import shutil
from pathlib import Path

from csvsort import csvsort

from app.constants import PackCode, ActionType
from app.mappings import ACTION_TYPE_TO_PRINT_TEMPLATE
from config import Config

SORTING_KEY = ['fieldOfficerId', 'organisationName']
PACKCODES_TO_SORT = [PackCode.D_CE1A_ICLCR1, PackCode.D_CE1A_ICLCR2B, PackCode.D_ICA_ICLR1, PackCode.D_ICA_ICLR1,
                     PackCode.D_ICA_ICLR2B, PackCode.D_ICA_ICLR2B, PackCode.D_FDCE_I1, PackCode.D_FDCE_I2,
                     PackCode.D_FDCE_I4, PackCode.D_CE4A_ICLR4, PackCode.D_CE4A_ICLS4,
                     PackCode.D_FDCE_H1, PackCode.D_FDCE_H2]


def sort_print_file_if_required(complete_partial_file: Path, pack_code: PackCode, action_type: ActionType,
                                context_logger):
    if pack_code in PACKCODES_TO_SORT:
        file_to_sort = copy_file_to_sorting_dir_to_sort(complete_partial_file)
        print_template = ACTION_TYPE_TO_PRINT_TEMPLATE.get(action_type)
        sorting_key_indexed = get_column_indexes_by_name_from_template(print_template, SORTING_KEY)
        context_logger.info("About to sort file: ", file_to_sort=file_to_sort)

        sorted_file = sort_print_file_to_new_file(file_to_sort, sorting_key_indexed)
        return move_sorted_file_to_partial_files_and_delete_old(sorted_file, complete_partial_file, file_to_sort)
    else:
        return complete_partial_file


def move_sorted_file_to_partial_files_and_delete_old(sorted_file: Path, complete_partial_file: Path,
                                                     file_to_sort: Path):

    new_sorted_file_path = Path(f'{Config.PARTIAL_FILES_DIRECTORY}/{sorted_file.name}')
    shutil.move(str(sorted_file), str(new_sorted_file_path))
    # the sorted file is now in the /partial_files dir, ready to be processed and would be picked up on restart
    # time to remove the unrequired files
    complete_partial_file.unlink()
    file_to_sort.unlink()

    return new_sorted_file_path


def copy_file_to_sorting_dir_to_sort(complete_partial_file: Path):
    # Having a copy of the file here will mean that the split file sorting will be done in the /sorting dir
    # if something went wrong these would never be picked up again by the service
    file_to_sort_path = Path(f'{Config.SORTING_FILES_DIRECTORY}/{complete_partial_file.name}.to_sort')
    shutil.copy(str(complete_partial_file), str(file_to_sort_path))

    return file_to_sort_path


def sort_print_file_to_new_file(file_to_sort: Path, sorting_column_indexes):
    sorted_file_path = f'{file_to_sort.parent}/{file_to_sort.name.replace(".to_sort", ".sorted")}'
    csvsort(str(file_to_sort), sorting_column_indexes, output_filename=sorted_file_path,
            max_size=500, delimiter='|', has_header=False)
    return Path(sorted_file_path)


def get_column_indexes_by_name_from_template(template, columns):
    return [template.index(column) for column in columns]
