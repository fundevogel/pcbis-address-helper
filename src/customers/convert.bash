#!/usr/bash

iconv --from-code=ISO-8859-1 --to-code=UTF-8 Stammadressen.xls > raw.xls
csvjson raw.xls > raw.json
