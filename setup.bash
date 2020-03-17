#!/bin/bash

# Setting up & activating virtualenv
virtualenv -p python3 .env
# shellcheck disable=SC1091
source .env/bin/activate

# Installing dependencies
pip install -r requirements.txt

# Creating directory structure
for dir in src/changed \
           dist/csv \
           dist/json \
           backups
do
    mkdir -p "$dir"
done
