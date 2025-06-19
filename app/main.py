from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
import os
from .google_sheets_db import GoogleSheet
from datetime import datetime
from dotenv import load_dotenv

# Sólo carga .env en local
if os.getenv("ENV") == "development":
    load_dotenv()

google = GoogleSheet(
    file_name=os.getenv("GOOGLE_CREDENTIALS"),  
    document=os.getenv("GOOGLE_SHEET_ID", "RegistroAccesos"),
    sheet_name=os.getenv("SHEET_NAME", "Sheet1")
)

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class EnvioDatos:
    def __init__(self, rut: str):
        now = datetime.now()
        self.fecha = now.strftime("%d/%m/%Y")
        self.hora  = now.strftime("%H:%M:%S")
        self.rut   = rut

    def to_row(self):
        return [self.fecha, self.hora, self.rut]

class RegistroRequest(BaseModel):
    rut: str

@app.post("/registro")
def registro_acceso(request: RegistroRequest):
    rut = request.rut
    if not rut:
        raise HTTPException(400, "RUT no recibido")

    fila = EnvioDatos(rut).to_row()
    if any(not v for v in fila):
        raise HTTPException(422, "Datos inválidos")

    rango = google.get_last_row_range()
    google.write_data(rango, [fila])
    logging.info(f"RUT {rut} registrado a las {fila[0]} {fila[1]}")
    return JSONResponse({"message": "RUT registrado con éxito"}, 200)

@app.get("/")
def read_root():
    return {"message": "API de Registro de Accesos en Google Sheets"}
