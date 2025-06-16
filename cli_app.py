from google_sheets_db import GoogleSheet
from datetime import date
import uuid

file_name_gs = "informaticaxrobotica-credenciales.json"
google_sheet = "RegistroAccesos"
sheet_name = "Sheet1"


# --------------------------------------


def generate_uid():
    # Generate a UUID
    unique_id = uuid.uuid4()
    # Convert the UUID to a string
    unique_id_str = str(unique_id)
    return unique_id_str


# Generate uid
uid = generate_uid()
# Init
google = GoogleSheet(file_name_gs, google_sheet, sheet_name)

date = date.today()
value = [[uid, "test", "test", "test"]]
range = google.get_last_row_range()
google.write_data(range, value)
