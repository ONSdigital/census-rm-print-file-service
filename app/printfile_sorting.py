import shutil
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
    # Leave complete_partial_file in partial_files dir
    # Run sort on that file to a new file in sort_dir  filename_sorted
    # Move back to partial directory
    # delete previous complete_partial_file
    # look at splitting code for this, is there reuable code there
    # In sorting decisions, if endswith _sorted then don't sort

    # and not str(complete_partial_file).endswith('_sorted')

    if pack_code.value in PACKCODES_TO_SORT:
        file_to_sort = copy_file_to_sorting_dir_to_sort(complete_partial_file)
        print_template = ACTION_TYPE_TO_PRINT_TEMPLATE.get(action_type)
        context_logger.info('Got print_template, change to good info logging of everything?')
        sorting_key_indexed = get_column_indexes_by_name_from_template(print_template, SORTING_KEY)

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


# Having a copy of the file here will mean that the split file sorting will be done in the /sorting dir
# if something went wrong these would never be picked up again by the service
def copy_file_to_sorting_dir_to_sort(complete_partial_file: Path):
    file_to_sort_path = Path(f'{Config.SORTING_FILES_DIRECTORY}/{complete_partial_file.name}.to_sort')
    shutil.copy(str(complete_partial_file), str(file_to_sort_path))

    return file_to_sort_path


# def make_dir_to_sort_file_in_and_move_file_there(complete_partial_file: Path, pack_code: PackCode, context_logger):
#     directory_to_sort = f'{Config.SORTING_FILES_DIRECTORY}/' \
#                         f'{pack_code.value}_{datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")}'
#     os.mkdir(directory_to_sort)
#     file_to_sort_in_dir = Path(f'{directory_to_sort}/{complete_partial_file.name}_to_sort')
#     shutil.move(str(complete_partial_file), file_to_sort_in_dir)
#
#     return file_to_sort_in_dir


def sort_print_file_to_new_file(file_to_sort: Path, sorting_column_indexes):
    sorted_file_path = f'{file_to_sort.parent}/{file_to_sort.name.replace(".to_sort", ".sorted")}'
    # if we leave complete_partial_file in partial_files and write to file in sorting_dir where do the file 'chunks'
    # get written
    csvsort(str(file_to_sort), sorting_column_indexes, output_filename=sorted_file_path,
            max_size=500, delimiter='|', has_header=False)
    return Path(sorted_file_path)


def get_column_indexes_by_name_from_template(template, columns):
    return [template.index(column) for column in columns]
