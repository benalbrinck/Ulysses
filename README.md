# Ulysses

A Python program to manage finances.

This is the program that I use personally to manage my finances. It tracks transactions, where income is distributed, and where to move money at the end of the month by splitting the money into separate virtual accounts. Ulysses uses Google Sheets to track transactions, the rules about how to distribute money, and how to display this information.

## Table of Contents

- [Ulysses](#ulysses)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Setup](#setup)
  - [Usage](#usage)
    - [Transactions](#transactions)
    - [Rules](#rules)
    - [UI Rules](#ui-rules)
    - [Dashboard](#dashboard)
  - [Configuration](#configuration)
  - [Maintainers](#maintainers)
  - [License](#license)

## Installation

Install the requirements for the project:

```sh
pip install requirements.txt
```

## Setup

Ulysses has an ```example_setup``` folder that should be renamed to ```setup```.

This project uses [gspread](https://github.com/burnash/gspread), so a service account needs to be created from the [Google API Console](http://gspread.readthedocs.org/en/latest/oauth2.html). After downloading the credentials JSON file, it should be moved to ```Ulysses/setup``` and renamed to ```client_secret.json```, overriding the empty file.

In the ```setup``` folder, there is an example Excel sheet that should be imported into Google Drive and made into a Google Sheet. This sheet should be shared with ```client_email``` in ```client_secret.json``` and should be given full edit permissions.

## Usage

The sheet and the worksheets in the sheet can be renamed. More details can be found in the [Configuration](#configuration) section.

Once ```ulysses.py``` is run, it will gather all transactions and rules from the sheet, calculate the totals for each split, and write them to the dashboard worksheet using the UI rules.

### Transactions

Ulysses uses different virtual accounts called splits that transactions move money into, out of, and between. A transaction consists of a name, type, delta, target, and date. The name is the description of the transaction, and the date is the day that the transaction took place.

Under the Transactions worksheet of the example Excel sheet, there are some example transactions. The four types of transactions are:

- Add: add money to the target split
- Spend: remove money from the target split
- Drain: this moves money between accounts, usually at the end of a month. This is configured in the Rules worksheet. See the below [Rules](#rules) section for more details.
- Custom transactions: these are created in the Rules worksheet. See the below [Rules](###rules) section for more details.

The Add and Spend transactions require a target, and the drain does not require either a target or a delta.

### Rules

This worksheet includes how custom transactions are performed and how a drain is performed. Examples of this can be found in the Rules worksheet of the example Excel sheet. Each rule consists of the transaction name, target, percent, start date, and end date.

- ```Start Date and End Date```: the start and end dates of the rule. If the transaction date is within these dates, the rule will be in effect. This allows changing rules over time without having to reset the entire Ulysses system. The End Date can be left empty.
- ```Type```: the name of the transaction that the rule is for.
- ```Target```: where to move the delta of the transaction to. This money will be split between each of the targets based on the percentage.
- ```Percent```: the percentage of the delta to move to the target.
- ```Overflow and Drain```: overflow can be left blank and drain can be set to 0 for normal rules.

Drain rules include these elements with slight differences as well as a drain number and an overflow.

- ```Drain``` number is what order to perform the drain rules in. If this is set to a number other than 0, then this rule is a drain rule.
- ```Type```: where to move money from.
- ```Target```: where to move money to.
- ```Percent```: what percentage of ```Type``` to move to ```Target```. This is the percentage of what is remaining after the previous drain rules have been performed. For example, if you want to move 90% of your leftover gas money at the end of the month to savings and 10% to the investing account, then the first drain rule will be 90% and the second 100%.
- ```Overflow```: what amount to keep in the ```Type``` before moving the ```Percent``` of the remaning money to the ```Target```.
- ```Start Date and End Date```: are the same as normal rules.

### UI Rules

These are what cells to display split amounts in the Dashboard. All available split names are determined by combining all ```Target``` names in the Rules worksheet. Examples can be found in the ```UI Rules``` worksheet in the example Excel sheet.

### Dashboard

This is where split totals will be displayed after Ulysses is run. This worksheet can be formatted however you want, but the UI Rules have to be updated if any changes are made to the location of a split. A very basic example can be found in the ```Dash``` worksheet in the example.

## Configuration

Beyond changing Rules and UI Rules, there are more configuration options. These can be found in ```config.yml```. The Google Sheet can be renamed in here, as well as each sheet.

The formats of each worksheet can also be changed. The names of the columns are unable to be changed, and the currency format has to remove commas and include two decimal places, though.

## Maintainers
- Ben Albrinck (https://github.com/benalbrinck)

## License

MIT License. Copyright (c) 2022 Ben Albrinck