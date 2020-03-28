#!/bin/bash

# (1) Generates `data.json` file for each directory
# (2) Merges them into single `data.json` file

cd src || exit

for directory in *
do
    if [ -d "$directory" ]; then
        cd "${directory}" || exit

        if [ -f main.py ]; then
            python main.py
        fi

        cd ..
    fi
done

python merge.py
