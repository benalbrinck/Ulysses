import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheet:
    def __init__(self, creds_path: str) -> None:
        # Use creds to create a client to interact with the Google Drive API
        scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        self._sheet = client.open('Financial Suite')
    
    def get_worksheet_values(self, worksheet_name: str) -> tuple[list, list]:
         # Get worksheet and column values
        worksheet = self._sheet.worksheet(worksheet_name)
        worksheet_values = worksheet.get_all_values()
        
        column_names = worksheet_values[0]
        worksheet_values = worksheet_values[1:]

        # Format column names
        column_names = [name.lower().replace(' ', '_') for name in column_names]

        return column_names, worksheet_values
    
    def update_dash(self, splits: dict, ui_ruleset: dict) -> None:
        worksheet = self._sheet.worksheet('Dash')

        # Write split values to cells specified in UI rules
        for split_name in ui_ruleset:
            split_value = splits[split_name]
            cell = ui_ruleset[split_name]

            worksheet.update(cell, split_value)
