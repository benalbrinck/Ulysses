import yaml
from datetime import datetime
from sheet import Sheet


def get_transactions(sheet: Sheet) -> list:
    # Get Rules worksheet values
    with open('setup/config.yml') as file:
        config = yaml.safe_load(file)

    transactions_name = config['transactions_name']
    column_names, worksheet_values = sheet.get_worksheet_values(transactions_name)

    # Load rows into dictionaries
    rules = []

    for row in worksheet_values:
        rule = {}

        for i, name in enumerate(column_names):
            if name == 'delta':
                # If delta column, parse value as float
                rule[name] = float(row[i].strip('$')) if row[i] != '' else 0
            elif name == 'date':
                # If date column, parse value as datetime
                rule[name] = datetime.strptime(row[i], '%m/%d/%y') if row[i] != '' else datetime.min
            else:
                # Otherwise, keep value as string
                rule[name] = row[i]
        
        rules.append(rule)
    
    return rules


if __name__ == '__main__':
    # Testing
    sheet = Sheet('credentials/client_secret.json')
    print(get_transactions(sheet))
