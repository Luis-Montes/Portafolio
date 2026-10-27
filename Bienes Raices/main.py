from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from database.connection import engine
from models.train_models import entrenar_modelos

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CSV_PATH = "realtor-data.csv"

modelo_lineal = None
modelo_logistico = None

if os.path.exists(CSV_PATH):
    modelo_lineal, modelo_logistico, mediana = entrenar_modelos(CSV_PATH)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"resultado": None})

@app.post("/predecir_y_guardar", response_class=HTMLResponse)
async def predecir_y_guardar(
    request: Request,
    bed: float = Form(...),
    bath: float = Form(...),
    house_size: float = Form(...),
    city: str = Form(...),
    state: str = Form(...),
):
    global modelo_lineal, modelo_logistico

    if modelo_lineal is None:
        return templates.TemplateResponse(request, "index.html", {
            "request": request,
            "error": "Primero debes colocar el archivo CSV y entrenar los modelos.",
        })

    entrada_df = pd.DataFrame([[bed, bath, house_size]], columns=['bed', 'bath', 'house_size'])
    precio_estimado = modelo_lineal.predict(entrada_df)[0]

    clase_estimada = modelo_logistico.predict(entrada_df)[0]
    categoria_texto = "Propiedad de Lujo / Alta Gama" if clase_estimada == 1 else "Propiedad de Gama Estándar"

    query = f"""
    INSERT INTO viviendas (bed, bath, house_size, city, state, precio_estimado)
    VALUES ({bed}, {bath}, {house_size}, '{city}', '{state}', {precio_estimado})
    """

    try:
        with engine.begin() as conn:
            conn.exec_driver_sql(query)
        db_status = "¡Vivienda guardada exitosamente en SQL Server!"
    except Exception as e:
        db_status = f"Nota: Datos calculados, pero error al guardar en BD (verifica la tabla): {str(e)}"

    return templates.TemplateResponse(request, "index.html", {
        "precio": round(precio_estimado, 2),
        "categoria": categoria_texto,
        "db_status": db_status,
        "bed": bed,
        "bath": bath,
        "house_size": house_size
    })