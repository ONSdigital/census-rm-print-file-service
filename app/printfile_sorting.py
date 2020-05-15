import os
import shutil
from datetime import datetime
from pathlib import Path

from csvsort import csvsort

from app.constants import PackCode, ActionType
from app.mappings import ACTION_TYPE_TO_PRINT_TEMPLATE
from config import Config

SORTING_KEY = ['fieldOfficerId', 'organisationName']
# make these enums
PACKCODES_TO_SORT = ['D_CE1A_ICLCR1', 'D_CE1A_ICLCR2B', 'D_ICA_ICLR1', 'D_ICA_ICLR1', 'D_ICA_ICLR2B',
                     'D_ICA_ICLR2B', 'D_FDCE_I1', 'D_FDCE_I2', 'D_FDCE_I4', 'D_CE4A_ICLR4', 'D_CE4A_ICLS4',
                     'D_FDCE_H1', 'D_FDCE_H2']


# Need to do this to another file?
# technically not always going to be a sorted file?
# Get this bit working simple route then deal with:

# Then call on Adam? maybe or just sit down and work it out
# 1. Do sorting in a directory, for any temp files csvsort uses - if the svc dies it's easy to clean up.
# 2. Resulting sorted file created and returned.
# 3. If print file doesn't require sorting then return the passed file? naming important

def sort_print_file_if_required(complete_partial_file: Path, pack_code: PackCode, action_type: ActionType,
                                context_logger):
    if pack_code.value in PACKCODES_TO_SORT:
        context_logger.info('Going to sort file')
        complete_partial_file = make_dir_to_sort_file_in_and_move_file_there(complete_partial_file, pack_code,
                                                                             context_logger)
        context_logger.info('Have moved file to new directory')
        print_template = ACTION_TYPE_TO_PRINT_TEMPLATE.get(action_type)
        context_logger.info('Got print_template')
        sorting_key_indexed = get_column_indexes_by_name_from_template(print_template, SORTING_KEY)
        context_logger.info('Got sorting key')

        return sort_print_file_to_new_file(complete_partial_file, sorting_key_indexed)
    else:
        return complete_partial_file


def make_dir_to_sort_file_in_and_move_file_there(complete_partial_file: Path, pack_code: PackCode, context_logger):
    directory_to_sort = f'{Config.SORTING_FILES_DIRECTORY}/' \
                        f'{pack_code.value}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}'
    os.mkdir(directory_to_sort)
    file_to_sort_in_dir = Path(f'{directory_to_sort}/{complete_partial_file.name}_to_sort')
    shutil.move(str(complete_partial_file), file_to_sort_in_dir)

    return file_to_sort_in_dir


def sort_print_file_to_new_file(complete_partial_file: Path, sorting_column_indexes):
    sorted_file_path = f'{complete_partial_file.parent}/{complete_partial_file.name.replace("_to_sort", "")}'
    # if we leave complete_partial_file in partial_files and write to file in sorting_dir where do the file 'chunks'
    # get written
    csvsort(str(complete_partial_file), sorting_column_indexes, output_filename=sorted_file_path,
            max_size=500, delimiter='|', has_header=False)
    return Path(sorted_file_path)


def get_column_indexes_by_name_from_template(template, columns):
    return [template.index(column) for column in columns]
