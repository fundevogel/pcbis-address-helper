#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unicodedata

from bs4 import BeautifulSoup as bs


def clean(string):
    # python-notes
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python#19016117
    return "".join(character for character in string if unicodedata.category(character)[0]!="C")


# Receive HTML response
with open('raw.html', 'r') as file:
    raw = bs(file, 'lxml')

# Fetch table rows, cut first one (header)
rows = raw.find('tbody', {'id': 'ResultTableBody'}).find_all('tr')

data = []

for row in rows:
    info = row.find('div', {'class': 'infoKundeKurz'}).text
    info_list = info.splitlines()
    clean_list = [clean(item).strip() for item in info_list if clean(item).strip()]

    node = {}

    node['Anrede'] = ''
    node['Vorname'] = ''
    node['Nachname'] = clean_list[0]
    node['Namenszusatz-1'] = ''
    node['Namenszusatz-2'] = ''
    node['Straße'] = ' '.join(clean_list[1:2])
    node['PLZ'] = ' '.join(clean_list[2:]).split(' ')[0]
    node['Ort'] = ' '.join(' '.join(clean_list[2:]).split(' ')[1:])
    node['Telefon-1'] = ''
    node['Telefon-2'] = ''
    node['Fax'] = ''
    node['Email'] = ''
    node['Notiz'] = ''

    if len(clean_list) == 2:
        node['Straße'] = ''
        node['PLZ'] = ' '.join(clean_list[1:]).split()[0]
        node['Ort'] = ' '.join(' '.join(clean_list[1:]).split()[1:])

    if node['Ort'] == 'Freiburg i. Brsg.' or node['Ort'] == 'Freiburg im Breisgau' or node['Ort'] == 'Freiburg (Brsg)':
        node['Ort'] = 'Freiburg'

    if node['Ort'] == 'Staufen i. Breisgau':
        node['Ort'] = 'Staufen'

    if node['Nachname'] == None:
        node['Nachname'] = ''

    if node['Straße'] == None:
        node['Straße'] = ''

    if node['PLZ'] == None:
        node['PLZ'] = ''

    if node['Ort'] == None:
        node['Ort'] = ''

    data.append(node)

with open('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
