#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json


json_files = glob.glob('*/data.json')

data = []

for json_file in json_files:
    with open(json_file, 'r') as file:
        data += json.load(file)

with open('data.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
