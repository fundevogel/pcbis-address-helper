#! /usr/bin/python
# ~*~ coding=utf-8 ~*~

###
# IMPORTS (START)
#

from doit import get_var
from doit.tools import run_once

# TODO: Import only what is needed
import glob  # glob
import json  # dump, load

from os import path  # > isfile, getctime
from datetime import datetime  # now

from helpers import sort_data, remove_duplicates, compare_csv, apply_changes, print_row

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
            'dedupe',
            'sort',
        ]
    }


def task_export():
    """
    Exports all data from main file to CSV files
    """
    return {
        'actions': None,
        'task_dep': [
            'dedupe',
            'sort',
            'print',
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
    def diff():
        for comparison_file in comparison_files:
            current_file = comparison_file.replace('src/changed', 'dist/csv')
            json_file = current_file.replace('csv', 'json')

            with open(json_file, 'r') as input_file:
                data = json.load(input_file)

            diff = compare_csv(current_file, comparison_file)
            node = apply_changes(data, diff)

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


def task_merge():
    """
    Merges lists into main file
    """
    def merge():
        data = []

        for list_file in list_files:
            with open(list_file, 'r') as file:
                data += json.load(file)

        with open(main_file, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [merge],
    }


# TODO: Sort by given key(s)
def task_sort():
    """
    Sorts main file
    """
    def sort():
        with open(main_file, 'r') as input_file:
            data = json.load(input_file)

        with open(main_file, 'w') as output_file:
            json.dump(sort_data(data), output_file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [sort],
    }


def task_dedupe():
    """
    Removes duplicates from main file
    """
    def dedupe():
        with open(main_file, 'r') as input_file:
            data = json.load(input_file)

        unqiue_data = remove_duplicates(data)

        with open(main_file, 'w') as output_file:
            json.dump(unqiue_data, output_file, ensure_ascii=False, indent=4)

    return {
        'task_dep': ['backup'],
        'actions': [dedupe],
    }


def task_split():
    """
    Splits main file into lists
    """
    def split_data():
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
                json.dump(data, file, ensure_ascii=False, indent=4)

    return {
        'actions': ['rm -f ' + lists, split_data],
    }


def task_print():
    """
    Prints CSV tables from main file
    """
    def print_tables():
        # Load
        for list_file in list_files:
            with open(list_file, 'r') as input_file:
                data = json.load(input_file)

            # Run
            with open(list_file.replace('json', 'csv'), 'w') as output_file:
                print_row(data, output_file)

    return {
        'task_dep': ['split'],
        'actions': ['rm  -f ' + tables, print_tables],
    }

#
# TASKS (END)
###
