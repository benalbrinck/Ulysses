"""Gets the Google Sheet for Ulysses to use."""

import gspread
import yaml
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    """A class to represent a Google Sheet using gspread."""

    def __init__(self, creds_path: str) -> None:
        """Initialization method.
        
        Parameters:
            creds_path (str): the path to the credentials JSON file that is used to get the sheet.
        """

        # Use creds to create a client to interact with the Google Drive API
        scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        # Get sheet
        with open('setup/config.yml') as file:
            config = yaml.safe_load(file)

        sheet_name = config['sheet_name']
        self._sheet = client.open(sheet_name)
    
    def get_worksheet_values(self, worksheet_name: str) -> tuple[list, list]:
        """Get all values from a worksheet.

        Parameters:
            worksheet_name (str): the name of the worksheet to get values from.
        
        Returns:
            column_names (list): the column names of the worksheet.
            worksheet_values (list): a two-dimensional list of all the values of the sheet, excluding the first row.
        """

         # Get worksheet and column values
        worksheet = self._sheet.worksheet(worksheet_name)
        worksheet_values = worksheet.get_all_values()
        
        column_names = worksheet_values[0]
        worksheet_values = worksheet_values[1:]

        # Format column names
        column_names = [name.lower().replace(' ', '_') for name in column_names]

        return column_names, worksheet_values
    
    def update_dash(self, splits: dict, ui_ruleset: dict) -> None:
        """Update the Dash worksheet.

        Parameters:
            splits (dict): 
            ui_ruleset (dict): 
        """

        # Get dashboard name and worksheet
        with open('setup/config.yml') as file:
            config = yaml.safe_load(file)

        dashboard_name = config['dashboard_name']
        worksheet = self._sheet.worksheet(dashboard_name)

        # Write split values to cells specified in UI rules
        for split_name in ui_ruleset:
            split_value = splits[split_name]
            cell = ui_ruleset[split_name]

            worksheet.update(cell, split_value)
