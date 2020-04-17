import argparse
import csv
import json
import operator
import os
import shutil
import string
import uuid
from datetime import datetime
import random
from random import randint

import pandas as pd
from csvsort import csvsort


from app.constants import PrintTemplate
from app.rabbit_context import RabbitContext
from config import Config

ADDRESS1 = ['', 'Flat', 'Cell', 'Room', 'Alley', 'Villa', 'Palace']
ORGNAME = ['Smiths', 'AnOrg', 'TheOrg', 'Prison', 'BowlingClub', 'OldFolks', 'Anything', 'IdeasLacking']

ONE_GB_FILE = "./1GbFile.csv"
ONE_HUNDRED_MB_FILE = "./100mbFile.csv"
FIFTY_MB_FILE = "./50mbFile.csv"
ONE_AND_HALF_GB_FILE = "./1_5_GBFile.csv"
TWO_GB_FILE = "./2GBFile.csv"
THREE_GB_FILE = "./3GbFile.csv"


def _string_gen(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Make them related always, with magic
def get_random_cord_and_field():
    field_cord_id = randint(1000000, 1000010)
    field_officer_id = field_cord_id + randint(10, 20)

    return f'{field_cord_id}|{field_officer_id}'


def get_random_address_line():
    random_number = random.randint(1, 10)
    random_add = ADDRESS1[random.randint(0, len(ADDRESS1) - 1)]

    return f'{random_add}{random_number}'


def get_random_org():
    random_org1 = ORGNAME[randint(0, len(ORGNAME) - 1)]
    random_org2 = ORGNAME[randint(0, len(ORGNAME) - 1)]

    return f'{random_org1} {random_org2}'


def _create_test_print_file_to_sort(file_name, row_count):
    print('creating random unsorted print file', file_name)
    start = datetime.utcnow()

    with open(file_name, 'w') as out_file:
        # out_file.write('CordOfficerId|FieldOfficerId|OrgName|AddressLine1|AddresLine2|AddressLine3\n')
        for i in range(0, row_count):
            row = f'{get_random_cord_and_field()}|{get_random_org()}|{get_random_address_line()}|a road|an area\n'
            out_file.write(row)

    end = datetime.utcnow()

    print('Print file creation took: ', (end - start).total_seconds())


def get_file_size_in_mb(file_path):
    """ Get size of file at given path in bytes"""
    size = os.path.getsize(file_path)
    return (size / 1024) / 1024


def test_file_sorting(file_to_sort, sorting_function, sorting_key):
    print("----------------")

    print(f"Sort attempt on {file_to_sort}, actual_size {get_file_size_in_mb(file_to_sort)}")
    sorted_file = "./sorted.csv"

    print('Starting sort on ', file_to_sort)
    start = datetime.utcnow()
    sorting_function(file_to_sort, sorted_file, sorting_key)
    end = datetime.utcnow()

    print('Sorting took: ', (end - start).total_seconds())


def csvsort_lib(file_to_sort, out_file, sorting_key):
    shutil.copyfile(file_to_sort, out_file)
    print('Sorting print file')
    # This can take headers/true false, and column names instead or index.
    # https://bitbucket.org/richardpenman/csvsort/src/default/__init__.py

    csvsort(out_file, sorting_key, delimiter='|',
            has_header=True, max_size=200, show_progress=True)

    # Max size is mb to load at once, not rows! interesting to tweak and see on 1Gb files
    # csvsort(file_to_sort, ["CordOfficerId", "FieldOfficerId", "OrgName", "AddressLine1"], delimiter='|',
    #         has_header=True, max_size=500)


def sort_file_in_memory_by_column_index(file_to_sort, out_file, sorting_key):
    data = csv.reader(open(file_to_sort), delimiter='|')

    sortedlist = sorted(data, key=operator.itemgetter(0, 1, 2, 3))

    w = csv.writer(open(out_file, "w"), delimiter='|')
    for d in sortedlist:
        w.writerow(d)


def sort_file_in_memory_by_column_name(file_to_sort, out_file):
    with open(file_to_sort, 'r', newline='') as f_input:
        csv_input = csv.DictReader(f_input, delimiter='|')
        data = sorted(csv_input, key=lambda row: (row['CordOfficerId'], row['FieldOfficerId'],
                                                  row["OrgName"], row["AddressLine1"]))

    with open(out_file, 'w', newline='') as f_output:
        csv_output = csv.DictWriter(f_output, fieldnames=csv_input.fieldnames, delimiter='|')
        csv_output.writeheader()
        csv_output.writerows(data)


def panda_sort(file_to_sort, out_file, sorting_key):
    data = pd.read_csv(file_to_sort, delimiter='|', header=None)
    # sort_key = ["CordOfficerId", "FieldOfficerId", "OrgName", "AddressLine1"]

    sorted_data = data.sort_values([data.columns[0], data.columns[1], data.columns[2], data.columns[3]])

    sorted_data.to_csv(file_to_sort, index=False, header=None, sep='|')


def test_sorting_with(sorting_function, sorting_key, file_to_sort):
    print("\n_______________________________________________________\n")
    print(f"Testing {sorting_function.__name__}")
    # p = psutil.Process(os.getpid())
    # print(f"Memory usage before: {(p.memory_info().rss/ 1024)/1024}mb")
    test_file_sorting(file_to_sort, sorting_function, sorting_key)
    # print(f"Memory usage after:  {(p.memory_info().rss/ 1024)/1024}mb")
    print("\n_______________________________________________________\n")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Test sorting of csv printfile')
    parser.add_argument('--create_files',
                        default=False,
                        required=False)
    parser.add_argument('--file_name',
                        default=FIFTY_MB_FILE, required=False)
    parser.add_argument('--sorting_function',
                        default='', required=True)
    parser.add_argument('--send_msgs', default=0, required=False)
    return parser.parse_args()


def process(create_files, file_name, sorting_function):
    if create_files == 'True':
        _create_test_print_file_to_sort(FIFTY_MB_FILE, 1000000)
        _create_test_print_file_to_sort(ONE_HUNDRED_MB_FILE, 2000000)
        _create_test_print_file_to_sort(ONE_GB_FILE, 20000000)
        # _create_test_print_file_to_sort(ONE_AND_HALF_GB_FILE, 30000000)
        # _create_test_print_file_to_sort(TWO_GB_FILE, 40000000)
        exit(0)

    sorting_func = None
    if sorting_function == "panda":
        sorting_func = panda_sort
    elif sorting_function == "csvsort":
        sorting_func = csvsort_lib
    elif sorting_function == "inmem":
        sorting_func = sort_file_in_memory_by_column_index
    else:
        print("No sorting function: ", args.sorting_function)
        exit(1)

    print(f"About to sort {file_name} with {sorting_function}")

    sort_key = ["CordOfficerId", "FieldOfficerId", "OrgName", "AddressLine1"]

    test_sorting_with(sorting_func, sort_key, file_name)


def send_messages(sc):
    send_msgs_count = int(sc)
    print(f'Will send {send_msgs_count} msgs to be consumed')

    home_on = range(send_msgs_count)
    batch_id = str(uuid.uuid4())

    for n in home_on:
        field_cord_id = randint(1000000, 1000010)
        field_officer_id = field_cord_id + randint(10, 20)

        json_body = json.dumps({
            "actionType": "ICL1E",
            "batchId": batch_id,
            "batchQuantity": send_msgs_count,
            "uac": str(uuid.uuid4()),
            "caseRef": field_cord_id,
            "title": field_officer_id,
            "forename": get_random_org(),
            "surname": get_random_address_line(),
            "addressLine1": "123 Fake Street",
            "addressLine2": "Duffryn",
            "townName": "Newport",
            "postcode": "NPXXXX",
            "packCode": "P_IC_ICL1"
        }).encode()

        if n % 5000 == 0:
            print(f'{n} msgs sent')

        with RabbitContext(exchange=Config.RABBIT_EXCHANGE) as rabbit:
            rabbit.publish_message(
                message=json_body,
                content_type='application/json')

    exit(0)


if __name__ == '__main__':
    args = parse_arguments()

    print(f'Send Msg count {args.send_msgs}')

    if args.send_msgs != 0:
        send_messages(args.send_msgs)

    process(args.create_files, args.file_name, args.sorting_function)
