#! /usr/bin/python
# ~*~ coding=utf-8 ~*~

###
# IMPORTS (START)
#

from doit import get_var
from doit.tools import run_once

# TODO: Import only what is needed
import csv  # ??
import glob  # glob
import json  # dump, load

from os import path  # > isfile, getctime
from datetime import datetime  # now
from hashlib import md5
from operator import itemgetter

from csv_diff import load_csv, compare

from helpers import process

#
# IMPORTS (END)
###


###
# CONFIG (START)
#

DOIT_CONFIG = {
    'action_string_formatting': 'old',
}

#
# CONFIG (END)
###


###
# VARIABLES (START)
#

# Time
now = datetime.now()
timestamp = str(now.timestamp()).replace('.', '')

# Directories
backup_dir = 'backups/'
src = 'src/'
customers_dir = src + 'customers/'
invoices_dir = src + 'invoices/'

dist = 'dist/'
list_dir = dist + 'json/'
tables_dir = dist + 'csv/'

# Files
base_file = src + 'data.json'
main_file = dist + 'main.json'
backup_file = backup_dir + timestamp + '.json'

customers_file = customers_dir + 'Stammadressen.xls'
customers_temp = customers_dir + 'raw.xls'
customers_json = customers_dir + 'raw.json'

invoices_file = invoices_dir + 'Fakturierung.html'

backups = backup_dir + '*.json'
lists = list_dir + '*.json'
tables = tables_dir + '*.csv'
comparisons = src + 'changed/*.csv'

backup_files = glob.glob(backups)
list_files = glob.glob(lists)

comparison_files = glob.glob(comparisons)

#
# VARIABLES (END)
###


###
# FUNCTIONS (START)
#

# TODO: Remove unqiue from JSON dumps or move to write_json function
def unique(data):
    """
    Removes duplicates from main file
    """
    unique_data = []
    identifiers = set()

    for item in data:
        hash_digest = md5(str(item).encode('utf-8')).hexdigest()

        if hash_digest not in identifiers:
            identifiers.add(hash_digest)
            unique_data.append(item)

    return unique_data

#
# FUNCTIONS (END)
###


###
# GROUPS (START)
#

def task_import():
    """
    Imports changes to CSV files into main file
    """
    return {
        'actions': None,
        'task_dep': [
            'diff',
            'merge',
            'sort',
        ]
    }

#
# GROUPS (END)
###


###
# TASKS (START)
#

def task_diff():
    """
    Processes changes made to CSV files
    """
    def _diff(file1, file2):
        diff = compare(
            load_csv(open(file1), key="Name"),
            load_csv(open(file2), key="Name"),
        )

        return diff

    def diff():
        for comparison_file in comparison_files:
            current_file = comparison_file.replace('src/changed', 'dist/csv')
            json_file = current_file.replace('csv', 'json')

            with open(json_file, 'r') as input_file:
                data = json.load(input_file)

            diff = _diff(current_file, comparison_file)
            added = diff['added']
            removed = diff['removed']
            changed = diff['changed']


            # Check if items were added
            if len(added) > 0:
                print('Added:')

                for item in added:
                    print(item['Name'])

                    # Check if dictionary
                    for k, v in item.items():
                        if '; ' in v and ': ' in v:
                            d2 = dict(x.split(': ') for x in v.split('; '))
                            for k2, v2 in d2.items():
                                if k2 in ['Schüler', 'Lehrer', 'Klassen']:
                                    d2[k2] = int(v2)

                            item[k] = d2

                        # Check if list
                        if ', ' in v:
                            item[k] = v.split(', ')

                    data.append(item)


            # Check if items were removed
            if len(removed) > 0:
                print('\nRemoved:')

                for item in removed:
                    print(item['Name'])

                    # Remove from data
                    data = [node for node in data if not (node['Name'] == item['Name'])]


            # Check if items were changed
            if len(changed) > 0:
                print('\nChanged:')
                print(json.dumps(changed, ensure_ascii=False, indent=4))

            # Write to disk
            with open(json_file, 'w') as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)

    return {
        'actions': [
            diff,
            'rm ' + comparisons
        ],
        'verbosity': 2,
    }


def task_count():
    """
    Counts entries in main file
    """
    def count():
        with open(main_file, 'r') as file:
            data = json.load(file)

        print('Database holds %s entries.' % len(data))

    return {
        'actions': [count],
        'verbosity': 2,
    }


def task_backup():
    """
    Backs up main file
    """
    return {
        'actions': [
            'mkdir -p backups',
            'cp ' + main_file + ' %(targets)s 2>/dev/null || :',
        ],
        'targets': [backup_file],
    }


def task_restore():
    """
    Restores main file
    """
    recent_backup = max(backup_files, key=path.getctime)

    return {
        'file_dep': [recent_backup],
        'actions': ['cp %(dependencies)s ' + main_file],
    }


def task_extract():
    """
    Extracts addresses from source files
    """
    def extract_data():
        with open(base_file, 'r') as file:
            raw = json.load(file)

        # Process
        data = []

        for item in raw:
            node = process(item)
            data.append(node)

        with open(main_file, 'w') as file:
            json.dump(unique(data), file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'file_dep': [
            customers_file,
            invoices_file,
        ],
        'actions': [
            'bash src/main.bash',
            extract_data,
        ],
        'targets': [main_file],
        'uptodate': [run_once],
    }


def task_merge():
    """
    Merges lists into main file
    """
    def merge_json():
        data = []

        for list_file in list_files:
            with open(list_file, 'r') as file:
                data += json.load(file)

        with open(main_file, 'w') as file:
            json.dump(unique(data), file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [merge_json],
    }


# TODO: Sort by given key(s)
def task_sort():
    """
    Sorts main file
    """
    def sort(data):
        data = sorted(
            data,
            key=itemgetter(
                'PLZ',
                'Straße',
                'Ort'
            )
        )

        return data

    def sort_data():
        with open(main_file, 'r') as input_file:
            data = json.load(input_file)

        with open(main_file, 'w') as output_file:
            json.dump(sort(data), output_file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [sort_data],
        'verbosity': 2,
    }


def task_filter():
    """
    Filters uniques out of main file
    """
    def filter_uniques():
        with open(main_file, 'r') as input_file:
            data = json.load(input_file)

        with open(main_file, 'w') as output_file:
            json.dump(unique(data), output_file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [filter_uniques],
    }


def task_split():
    """
    Splits main file into lists
    """
    def split_json():
        with open(main_file, 'r') as file:
            raw = json.load(file)

        for item in raw:
            # Build filename
            stripped = item['Kategorie'].replace('/', '').replace('-', '')
            category = '-'.join(stripped.split()).lower()
            file_name = list_dir + category + '.json'

            data = []

            if path.isfile(file_name):
                with open(file_name, 'r') as file:
                    data = json.load(file)

            data.append(item)

            with open(file_name, 'w') as file:
                json.dump(unique(data), file, ensure_ascii=False, indent=4)

    return {
        'actions': ['rm -f ' + lists, split_json],
        'targets': list_files,
    }


def task_print():
    """
    Prints CSV tables from main file
    """
    def _print(data, file):
        csv_file = csv.writer(
            file,
            quoting=csv.QUOTE_NONNUMERIC
        )

        csv_file.writerow(data[0].keys())

        for item in data:
            for k, v in item.items():
                if type(v) == list:
                    item[k] = ', '.join(v)

                if type(v) == dict:
                    array = []

                    for k2, v2 in v.items():
                        array.append(': '.join([k2, str(v2)]))

                    item[k] = '; '.join(array)

            csv_file.writerow(item.values())

    def print_tables():
        # Load
        for list_file in list_files:
            with open(list_file, 'r') as input_file:
                data = json.load(input_file)

            # Run
            with open(list_file.replace('json', 'csv'), 'w') as output_file:
                _print(data, output_file)

    return {
        'file_dep': list_files,
        'actions': ['rm  -f ' + tables, print_tables],
    }

#
# TASKS (END)
###
