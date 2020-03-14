#!/bin/bash

# (1) Generates `data.json` file for each directory
# (2) Merges them into single `data.json` file

cd src || exit

for directory in *
do
    if [ -d "$directory" ]; then
        cd "${directory}" || exit
        python main.py && cd ..
    fi
done

python merge.py
