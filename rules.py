import yaml
from datetime import datetime
from sheet import Sheet


def get_rules(sheet: Sheet) -> list:
    # Get Rules worksheet values
    with open('setup/config.yml') as file:
        config = yaml.safe_load(file)

    rules_name = config['rules_name']
    column_names, worksheet_values = sheet.get_worksheet_values(rules_name)

    # Load rows into dictionaries
    rules = []

    for row in worksheet_values:
        rule = {}

        for i, name in enumerate(column_names):
            if name == 'drain':
                # If drain column, parse value as int
                rule[name] = int(row[i]) if row[i] != '' else 0
            elif name == 'percent':
                # If percent column, parse as float
                rule[name] = float(row[i].strip('%')) / 100
            elif name == 'overflow':
                # If overflow column, parse value as float
                rule[name] = float(row[i].strip('$')) if row[i] != '' else 0
            elif 'date' in name:
                # If start or end date column, parse value as datetime
                rule[name] = datetime.strptime(row[i], '%m/%d/%y') if row[i] != '' else datetime.max
            else:
                # Otherwise, keep value as string
                rule[name] = row[i].lower().replace(' ', '_')
        
        rules.append(rule)
    
    return rules


def get_ui_rules(sheet: Sheet) -> dict:
    # Get UI Rules worksheet values
    with open('setup/config.yml') as file:
        config = yaml.safe_load(file)

    ui_rules_name = config['ui_rules_name']
    column_names, worksheet_values = sheet.get_worksheet_values(ui_rules_name)

    # Load rows into dictionary
    ui_rules = {}

    for row in worksheet_values:
        # Get split name and cell based on the column names
        split_name = row[0] if column_names[0] == 'split_name' else row[1]
        cell = row[1] if column_names[0] == 'split_name' else row[0]

        # Format split name and insert into dictionary
        split_name = split_name.lower().replace(' ', '_')
        ui_rules[split_name] = cell
    
    return ui_rules


if __name__ == '__main__':
    # Testing
    sheet = Sheet('credentials/client_secret.json')
    print(get_rules(sheet))
    print(get_ui_rules(sheet))
