#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv  # ??

from hashlib import md5
from operator import itemgetter

from csv_diff import load_csv, compare


def sort_data(data):
    data = sorted(data, key=itemgetter("PLZ", "Straße", "Ort"))

    return data


def remove_duplicates(data):
    unique_data = []
    identifiers = set()

    for item in data:
        hash_digest = md5(str(item).encode("utf-8")).hexdigest()

        if hash_digest not in identifiers:
            identifiers.add(hash_digest)
            unique_data.append(item)

    return unique_data


def compare_csv(file1, file2):
    diff = compare(
        load_csv(open(file1), key="Name"), load_csv(open(file2), key="Name"),
    )

    return diff


def apply_changes(data, diff):
    added = diff["added"]
    removed = diff["removed"]
    changed = diff["changed"]

    # Check if items were added
    if len(added) > 0:
        print("Added:")

        for item in added:
            print(item["Name"])

            # Check if dictionary
            for k, v in item.items():
                if "; " in v and ": " in v:
                    d2 = dict(x.split(": ") for x in v.split("; "))
                    for k2, v2 in d2.items():
                        if k2 in ["Schüler", "Lehrer", "Klassen"]:
                            d2[k2] = int(v2)

                    item[k] = d2

                # Check if list
                if ", " in v:
                    item[k] = v.split(", ")

            data.append(item)

    # Check if items were removed
    if len(removed) > 0:
        print("\nRemoved:")

        for item in removed:
            print(item["Name"])

            # Remove from data
            data = [node for node in data if not (node["Name"] == item["Name"])]

    # Check if items were changed
    if len(changed) > 0:
        print("\nChanged:")
        print(json.dumps(changed, ensure_ascii=False, indent=4))

    return data


def prepare_item(item):
    for k, v in item.items():
        if type(v) == list:
            item[k] = ", ".join(v)

        if type(v) == dict:
            array = []

            for k2, v2 in v.items():
                array.append(": ".join([k2, str(v2)]))

            item[k] = "; ".join(array)

        return item


def print_row(data, file):
    csv_file = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)

    csv_file.writerow(data[0].keys())

    for item in data:
        node = prepare_item(item)

        csv_file.writerow(node.values())
