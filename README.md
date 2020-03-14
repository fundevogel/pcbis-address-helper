# KNV Address Organizer

## What
This project serves as an example workflow for organizing addresses generated from [KNV](https://www.knv-zeitfracht.de) (german wholesale book distributor) and saving them in [CSV files](https://en.wikipedia.org/wiki/Comma-separated_values). It's possible to convert exported contacts from within [`pcbis.de -> fitbis`](https://pcbis.de) (called *Stammadressen*) as well as extracting them from invoices.


## Why
We needed a solution that's flexible enough for all employees to work with (who are using [Kubuntu](https://kubuntu.org) which helps) while being easily maintainable through the [CLI](https://en.wikipedia.org/wiki/Command-line_interface).


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
extract   Extracts addresses & formats them
filter    Filters uniques out of main file
merge     Merges lists into main file
prepare   Prepares addresses from customer data & invoices
print     Prints CSV tables from main file
restore   Restores main file
sort      Sorts main file
split     Splits main file into lists
```


## Troubleshooting
Especially when extracting outdated information, at some point or another challenges will arise:

### Scraping invoices
First of all, exporting those invoices may take some time. When we decided to do this, there were over 8000 records, going back to 2010. `fitbis` isn't of much help there, limiting us to 50 records per page ..

Along the way, we will need the help of our browser's 'Developer Tools' (which are included in [Firefox](https://developer.mozilla.org/en-US/docs/Tools) as well as [Chrome](https://developers.google.com/web/tools/chrome-devtools)).

While the whole customer database (*Stammadressen*) may be exported in one fell swoop (`Weitere Funktionen -> Stammadressen -> Anzeigen`, then `Funktionen -> Alle Stammadressen exportieren`), this doesn't apply to invoices - but were there's a will there's a way:

1. Log into `pcbis.de`, then `Fitbis -> Fakturierung -> Anzeigen` will show you the ten most recent invoices.
2. Open the dropdown for entries per page (*Einträge pro Seite*), right-click on one of those numbers (eg '50') and select `Inspect Element` (Firefox) `Inspect` (Chrome).
3. Looking at the selected `li` element's `onclick` attribute, we notice the following: `setInputFieldDynamic( 'comtitlesPerPageHeader', '50','50')`.
4. Double-click the `onclick` attribute and change both integers to something >= the total number of invoices (eg '10000').
5. Wait for it .. boom! Save the page with `CTRL + S`.

### One size doesn't fit all
We never intended to release this, so think of this project as a boilerplate to get you started.


## Roadmap
Currently, the initial database was created *before* the decision to release this was made - so this is somewhat incomplete. Address organization already works the way it should ..  but these features are planned:

- [] Additional comments
- [x] Data extraction for `pcbis.de`
- [x] Tutorial on downloading invoices from `pcbis.de`
- [] Diffing CSV files from employees, adding changes automagically
- [] More modular setup (rules about converting phone numbers, cities, wrong categories ..)

:copyright: Fundevogel Kinder- und Jugendbuchhandlung
