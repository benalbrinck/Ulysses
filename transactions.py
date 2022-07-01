"""Gets transactions from the Google Sheet."""

import yaml
from datetime import datetime
from sheet import Sheet


def get_transactions(sheet: Sheet) -> list:
    """Get transactions from the Transactions worksheet.

    Parameters:
        sheet (Sheet): the sheet to get transactions from.
    
    Returns:
        transactions (list): a list of transactions. Each transaction is a dictionary with the columns as the keys.
    """

    # Get Transaction worksheet values
    with open('setup/config.yml') as file:
        config = yaml.safe_load(file)

    transactions_name = config['transactions_name']
    column_names, worksheet_values = sheet.get_worksheet_values(transactions_name)

    # Load rows into dictionaries
    transactions = []

    for row in worksheet_values:
        transaction = {}

        for i, name in enumerate(column_names):
            if name == 'delta':
                # If delta column, parse value as float
                transaction[name] = float(row[i].strip('$')) if row[i] != '' else 0
            elif name == 'date':
                # If date column, parse value as datetime
                transaction[name] = datetime.strptime(row[i], '%m/%d/%y') if row[i] != '' else datetime.min
            else:
                # Otherwise, keep value as string
                transaction[name] = row[i]
        
        transactions.append(transaction)
    
    return transactions


if __name__ == '__main__':
    # Testing
    sheet = Sheet('credentials/client_secret.json')
    print(get_transactions(sheet))
