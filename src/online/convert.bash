#!/usr/bash

iconv --from-code=ISO8859-1 --to-code=UTF-8 Orders_*.csv > raw.csv
csvjson -d ";" raw.csv > raw.json
