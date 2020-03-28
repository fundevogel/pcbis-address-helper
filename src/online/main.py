#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


with open('raw.json', 'r') as file:
    raw = json.load(file)

data = []

for item in raw:
    node = {}
    node['Anrede'] = item['rechnungaddresstitle']
    node['Vorname'] = item['rechnungaddressfirstname']
    node['Nachname'] = item['rechnungaddresslastname']
    node['Namenszusatz-1'] = item['Firma']
    node['Namenszusatz-2'] = ''
    node['Straße'] = ''
    node['PLZ'] = str(item['rechnungaddresszipcode'])[:-2]
    node['Ort'] = item['rechnungaddresscity']
    node['Telefon-1'] = item['rechnungaddressphonenumber']
    node['Telefon-2'] = ''
    node['Fax'] = ''
    node['Email'] = item['rechnungaddressemail']
    node['Notiz'] = ''

    if item['rechnungaddressstreet'] != None:
        node['Straße'] = ' '.join([item['rechnungaddressstreet'], item['rechnungaddresshousenumber']])

    for k, v in node.items():
        if v == None:
            node[k] = ''

    data.append(node)

with open('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
