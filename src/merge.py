#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re  # split, sub
import glob
import json


def clean(string, is_phone=False):
    # Remove newline control character
    remove_newline = ' '.join(re.split('\n', string))

    if is_phone is True:
        replace_area_code = remove_newline.replace('++49', '').replace('+49', '')
        remove_non_digits = re.sub('\D', '', replace_area_code)

        return remove_non_digits

    # Remove multiple whitespaces within string
    clean = ' '.join(remove_newline.split())

    return clean.replace('\"', '\'').strip()


def process(item):
    node = {}

    node['Kategorie'] = ''
    node['Anrede'] = ''
    node['Vorname'] = ''
    node['Nachname'] = ''
    node['Institution'] = ''
    node['Namenszusatz-1'] = ''
    node['Namenszusatz-2'] = ''
    node['Straße'] = ''
    node['PLZ'] = ''
    node['Ort'] = ''
    node['Telefon-1'] = ''
    node['Telefon-2'] = ''
    node['Fax'] = ''
    node['Email'] = ''
    node['Webseite'] = ''
    node['Notiz'] = ''

    # Source: data
    if 'title' in item:
        node['Institution'] = clean(item['title'])

    if 'street' in item:
        node['Straße'] = clean(item['street'])

    if 'postal' in item:
        node['PLZ'] = clean(item['postal'])

    if 'city' in item:
        node['Ort'] = clean(item['city'])

    if 'phone' in item:
        node['Telefon-1'] = clean(item['phone'], True)

    if 'fax' in item:
        node['Fax'] = clean(item['fax'], True)

    if 'mail' in item:
        node['Email'] = clean(item['mail']).lower()

    if 'web' in item:
        node['Webseite'] = clean(item['web']).lower().replace('://www.', '://')


    # Source: offline
    if 'Kategorie' in item:
        node['Kategorie'] = clean(item['Kategorie'])

    if 'Anrede' in item:
        value = item['Anrede']
        node['Anrede'] = clean(value)

    if 'Titel' in item:
        value = ' '.join([item['Anrede'], item['Titel']])
        node['Anrede'] = clean(value)

    if 'Dr.-Titel' in item:
        value = ' '.join([item['Anrede'], item['Dr.-Titel']])
        node['Anrede'] = clean(value)

    if 'Titel' in item and 'Dr.-Titel' in item:
        value = ' '.join([item['Anrede'], item['Titel'], item['Dr.-Titel']])
        node['Anrede'] = clean(value)

    if 'Vorname' in item:
        node['Vorname'] = clean(item['Vorname'])

    if 'Nachname' in item:
        node['Nachname'] = clean(item['Nachname'])

    if 'Institution' in item:
        node['Institution'] = clean(item['Institution'])

    if 'Namenszusatz-1' in item:
        node['Namenszusatz-1'] = clean(item['Namenszusatz-1'])

    if 'Namenszusatz-2' in item:
        node['Namenszusatz-2'] = clean(item['Namenszusatz-2'])

    if 'Straße' in item:
        node['Straße'] = clean(item['Straße'])

    if 'PLZ' in item:
        node['PLZ'] = clean(item['PLZ'])

    if 'Ort' in item:
        node['Ort'] = clean(item['Ort'])

    if 'Telefon-1' in item:
        node['Telefon-1'] = clean(item['Telefon-1'], True)

    if 'Telefon-2' in item:
        node['Telefon-2'] = clean(item['Telefon-2'], True)

    if 'Fax' in item:
        node['Fax'] = clean(item['Fax'], True)

    if 'Email' in item:
        node['Email'] = clean(item['Email']).lower()

    if 'Webseite' in item:
        node['Webseite'] = clean(item['Webseite']).lower().replace('://www.', '://')

    if 'Notiz' in item:
        node['Notiz'] = clean(item['Notiz'])


    # No category present
    if node['Kategorie'] == '':
        # Pre-school
        pre_school = [
            'kinder',
            'krippe',
            'krabbel',
            'kiga',
            'kita',
            'hort',
            'spiel',
            'wald',
        ]

        for term in pre_school:
            if term in node['Vorname'].lower() or term in node['Nachname'].lower() or term in node['Institution'].lower() or term in node['Namenszusatz-1'].lower() or term in node['Namenszusatz-2'].lower():
                node['Kategorie'] = 'Kindertagesstätte'

        # Libraries
        libraries = [
            'bibliothek',
            'bbliothek',
            'bücherei',
            'library',
        ]

        for term in libraries:
            if term in node['Vorname'].lower() or term in node['Nachname'].lower() or term in node['Institution'].lower() or term in node['Namenszusatz-1'].lower() or term in node['Namenszusatz-2'].lower():
                node['Kategorie'] = 'Bücherei / Bibliothek'

        # Culture
        culture = [
            'museen',
            'museum',
            'theater',
            'literaturhaus',
        ]

        for term in culture:
            if term in node['Vorname'].lower() or term in node['Nachname'].lower() or term in node['Institution'].lower() or term in node['Namenszusatz-1'].lower() or term in node['Namenszusatz-2'].lower():
                node['Kategorie'] = 'Kunst / Kultur'

        # Schools
        schools = {
            'grundschule': 'Grundschule',
            'grund- und hauptschule': 'Grund- und Hauptschule',
            'hauptschule': 'Hauptschule',
            'realschule': 'Real- / Gesamtschule',
            'gesamtschule': 'Real- / Gesamtschule',
            'gymnasium': 'Gymnasium',
        }

        for term, category in schools.items():
            if term in node['Vorname'].lower() or term in node['Nachname'].lower() or term in node['Institution'].lower() or term in node['Namenszusatz-1'].lower() or term in node['Namenszusatz-2'].lower():
                node['Kategorie'] = category

    # Category present, but wrong one
    wrong_categories = {
        'Kindergarten': 'Kindertagesstätte',
        'Bibliothek': 'Bücherei / Bibliothek',
        'Realschule': 'Real- / Gesamtschule',
    }

    if node['Kategorie'] == '':
        node['Kategorie'] = 'Unsortiert'


if __name__ == "__main__":
    # Init
    json_files = glob.glob('*/data.json')

    raw = []

    # Load
    for json_file in json_files:
        with open(json_file, 'r') as file:
            raw += json.load(file)

    # Process
    data = []

    for item in raw:
        node = process(item)
        data.append(node)

    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
