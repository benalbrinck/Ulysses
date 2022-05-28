import logging
import os
import rules
import transactions
from datetime import datetime
from sheet import Sheet


def main(logger: logging.Logger) -> None:
    # Get sheet, rules, and transactions
    logger.info('Getting sheet, rules, and transactions...')
    sheet = Sheet('credentials/client_secret.json')

    ruleset = rules.get_rules(sheet)
    ui_ruleset = rules.get_ui_rules(sheet)
    transaction_list = transactions.get_transactions(sheet)

    # Get splits
    rule_split_names = [x['target'] for x in ruleset]
    ui_rule_split_names = [x for x in ui_ruleset]

    split_names = list(set(rule_split_names + ui_rule_split_names))
    splits = {x: 0 for x in split_names}

    # Perform each transaction
    logger.info('Performing transactions...')

    for transaction in transaction_list:
        splits = render(transaction, ruleset, splits)
    
    logger.info(f'Splits: {splits}')

    # Output result to sheet
    logger.info('Writing to sheet...')
    sheet.update_dash(splits, ui_ruleset)
    logger.info('Successfully wrote to sheet')


def render(transaction: dict, ruleset: list, splits: dict) -> dict:
    # Filter rules by transaction date
    filtered_rules = [x for x in ruleset if x['start_date'] <= transaction['date'] <= x['end_date']]
    
    # Check if a preset transaction
    transaction_type = transaction['type'].lower().replace(' ', '_')
    transaction_target = transaction['target'].lower().replace(' ', '_')

    if transaction_type == 'add':
        # Add delta to target
        splits[transaction_target] += transaction['delta']
        return splits
    elif transaction_type == 'spend':
        # Subtract delta from target
        splits[transaction_target] -= transaction['delta']
        return splits
    elif transaction_type == 'drain':
        # Filter and sort rules by drain order
        filtered_rules = [x for x in filtered_rules if x['drain'] != 0]
        filtered_rules = sorted(filtered_rules, key=lambda x: x['drain'])

        # Perform each drain rule
        for rule in filtered_rules:
            delta = (splits[rule['type']] - rule['overflow']) * rule['percent']
            delta = round(delta, 2)

            if delta > 0:
                splits[rule['type']] -= delta
                splits[rule['target']] += delta
        
        return splits

    # If not a preset, filter rules by type
    filtered_rules = [x for x in filtered_rules if x['type'] == transaction_type]

    # Create deltas dictionary
    for rule in filtered_rules:
        delta = rule['percent'] * transaction['delta']
        delta = round(delta, 2)

        splits[rule['target']] += delta

    return splits


def get_logger() -> logging.Logger:
    logger = logging.getLogger('defy')
    logger.setLevel(level=logging.DEBUG)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    filename = (f'logs/{datetime.now()}.log').replace(':', '')
    file_handler = logging.FileHandler(filename)
    stream_handler = logging.StreamHandler()

    format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    file_handler.setFormatter(format)
    stream_handler.setFormatter(format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


if __name__ == '__main__':
    logger = get_logger()
    main(logger)
