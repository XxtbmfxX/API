from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
import os

from .google_sheets_db import GoogleSheet  # <-- Cambio aquí
from datetime import datetime
import uuid

# Cambia la ruta aquí
file_name_gs = os.path.join(os.path.dirname(__file__), "credenciales.json")
google_sheet = "RegistroAccesos"
sheet_name = "Sheet1"

google = GoogleSheet(file_name_gs, google_sheet, sheet_name)

app = FastAPI()
logging.basicConfig(level=logging.INFO)


# Clase para organizar los datos de envío
class EnvioDatos:
    def __init__(self, rut: str):
        now = datetime.now()
        self.fecha = now.strftime("%d/%m/%Y")
        self.hora = now.strftime("%H:%M:%S")
        self.rut = rut

    def to_row(self):
        return [self.fecha, self.hora, self.rut]


# Modelo Pydantic para recibir datos en formato JSON
class RegistroRequest(BaseModel):
    rut: str


# Endpoint para recibir POST con FastAPI (ahora acepta JSON)
@app.post("/registro")
def registro_acceso(request: RegistroRequest):
    try:
        rut = request.rut
        if not rut:
            logging.warning("RUT no recibido en la petición")
            raise HTTPException(status_code=400, detail="RUT no recibido")

        datos_envio = EnvioDatos(rut)
        fila = datos_envio.to_row()

        # Validación previa del formato de los datos
        if not isinstance(fila, list) or any(v is None or v == "" for v in fila):
            logging.error(f"Formato de datos inválido para Google Sheets: {fila}")
            raise HTTPException(
                status_code=422,
                detail="Formato de datos inválido para Google Sheets"
            )

        valores = [fila]
        if not isinstance(valores, list) or not all(isinstance(row, list) for row in valores):
            logging.error(f"Los datos enviados a Google Sheets deben ser lista de listas: {valores}")
            raise HTTPException(
                status_code=422,
                detail="Los datos enviados a Google Sheets deben ser lista de listas"
            )

        range = google.get_last_row_range()
        google.write_data(range, valores)

        logging.info(
            f"RUT {rut} registrado a las {datos_envio.fecha} {datos_envio.hora}"
        )
        return JSONResponse(
            content={"message": "RUT registrado con éxito"}, status_code=200
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al registrar acceso: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.get("/")
def read_root():
    return {"message": "API de Registro de Accesos en Google Sheets"}


# Si quieres testear desde localhost:8000
# uvicorn main:app --reload
def read_root():
    return {"message": "API de Registro de Accesos en Google Sheets"}


# Si quieres testear desde localhost:8000
# uvicorn main:app --reload
