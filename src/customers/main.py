#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def clean(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary

    return dict((key, clean(value)) for key, value in dictionary.items() if value is not None)


with open('raw.json', 'r') as file:
    raw = json.load(file)

data = []

# TODO: Replace with loop
for item in raw:
    if item['Anrede'] == None:
        item['Anrede'] = ''

    if item['Vorname'] == None:
        item['Vorname'] = ''

    if item['Nachname'] == None:
        item['Nachname'] = ''

    if item['Namenszusatz-1'] == None:
        item['Namenszusatz-1'] = ''

    if item['Namenszusatz-2'] == None:
        item['Namenszusatz-2'] = ''

    if item['Straße'] == None:
        item['Straße'] = ''

    if item['PLZ'] == None:
        item['PLZ'] = ''

    if item['Ort'] == None:
        item['Ort'] = ''

    if item['Telefon-1'] == None:
        item['Telefon-1'] = ''

    if item['Telefon-2'] == None:
        item['Telefon-2'] = ''

    if item['Fax'] == None:
        item['Fax'] = ''

    if item['Email'] == None:
        item['Email'] = ''

    if item['Notiz'] == None:
        item['Notiz'] = ''

    delete = [
        'Kundenland-ISO',
        'Benachrichtigung',
        'Rabatt',
        'Rechnungsart',
    ]

    for element in delete:
        del item[element]

    data.append(clean(item))

with open('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
