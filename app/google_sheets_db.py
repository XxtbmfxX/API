import gspread
import pandas as pd

from google.auth import default
from googleapiclient.discovery import build


class GoogleSheet:
    def __init__(self, cred_path, sheet_id, sheet_name):
        if cred_path:
            creds = service_account.Credentials.from_service_account_file(
                cred_path, scopes=[...]
            )
        else:
            creds, _ = default(scopes=["https://www.googleapis.com/auth/spreadsheets"])
        self.service = build("sheets", "v4", credentials=creds)
        self.sheet = sheet_id
        self.sheet_name = sheet_name

    def read_data(
        self, range
    ):  # range = "A1:E1". Data devolvera un array de la fila 1 desde la columna A hasta la E
        data = self.sheet.get(range)
        return data

    def read_data_by_uid(self, uid):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        print(df)
        filtered_data = df[df["uid"] == uid]
        return filtered_data  # devuelve un data frame de una tabla, de dos filas siendo la primera las cabeceras de las columnas y la segunda los valores filtrados para acceder a un valor en concreto df["nombre"].to_string()

    def write_data(
        self, range, values
    ):  # range ej "A1:V1". values must be a list of list
        self.sheet.update(range, values)

    def write_data_by_uid(self, uid, values):
        # Find the row index based on the UID
        cell = self.sheet.find(uid)
        row_index = cell.row
        # Update the row with the specified values
        self.sheet.update(f"A{row_index}:E{row_index}", values)

    def get_last_row_range(self):
        last_row = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{last_row}"
        range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row}"
        return f"{range_start}:{range_end}"

    def get_all_values(self):
        # self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
        return (
            self.sheet.get_all_records()
        )  # this return a list of dictioraies so the key is the name column and the value is the value for that particular column
