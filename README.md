# KNV Address Organizer

## What
This project serves as an example workflow for organizing addresses generated from [KNV](https://www.knv-zeitfracht.de) (german wholesale book distributor) and saving them in [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). It's possible to convert exported contacts from within [`pcbis.de`](https://pcbis.de) (called *Stammadressen*) as well as extracting them from invoices.


## Why
We needed a solution that's flexible enough for all employees to work with while being easily maintainable through the [CLI](https://en.wikipedia.org/wiki/Command-line_interface).


## Getting started

### TL;DR
Simply run `bash setup.bash` and you're set.

### Manual setup
Create a virtual environment with `python3` and activate it:

```text
    virtualenv -p python3 .venv
    source .venv/bin/activate
```

Now, install all python packages with `pip install -r requirements.txt` - or just [`doit`](https://pydoit.org) as its the only dependency at the moment: `pip install doit`.


## Usage
With `doit list` you'll be presented with available tasks:

```text
$ doit list
backup    Backs up main file
filter    Filters uniques out of main file
merge     Merges lists into main file
print     Prints CSV tables from main file
restore   Restores main file
sort      Sorts main file
split     Splits main file into lists
```

## Roadmap
Currently, the initial database was created *before* the decision to release this was made - so this is somewhat incomplete. Address organization already works the way it should ..  but these features are planned:

- [] Additional comments
- [] Data extraction for `pcbis.de`
- [] Tutorial on downloading invoices from `pcbis.de`
- [] Diffing CSV files from employees, adding changes automagically

:copyright: Fundevogel Kinder- und Jugendbuchhandlung
