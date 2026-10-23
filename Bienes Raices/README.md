# Mi Patrimonio Inmobiliario

## Iniciar la aplicación

Desde PowerShell, abre la carpeta `Bienes Raices` y ejecuta:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn backend:app --host 127.0.0.1 --port 8000
```

Abre <http://127.0.0.1:8000/>. El backend sirve `index.html` y la API desde el mismo origen; no abras el HTML directamente como `file://`, porque el navegador no podrá enviar las solicitudes a la API. La información de las propiedades continúa guardándose en `localStorage`.

## API de estimación

`POST /api/estimate` recibe las características que el modelo existente usa:

```json
{
  "metros_cuadrados": 75,
  "habitaciones": 3,
  "antiguedad": 10
}
```

Una respuesta correcta (`200`) tiene el formato:

```json
{
  "precio_estimado": 144000.0,
  "moneda": "USD",
  "calculado_en": "2026-10-23T04:00:00+00:00"
}
```

Los valores de la respuesta son un ejemplo del resultado reproducible con los datos incluidos en el modelo. Las entradas faltantes o inválidas reciben `400` o `422` y un mensaje en `detail`; un fallo interno devuelve `500` sin exponer detalles del servidor. `GET /api/health` permite comprobar que el backend está disponible.

El precio se estima únicamente a partir de metros cuadrados, habitaciones y antigüedad. El modelo no utiliza el nombre, el tipo de inmueble ni la dirección.

## Limitaciones del modelo

La implementación conserva la regresión lineal de `backend.py` y su conjunto de entrenamiento actual: seis ejemplos sintéticos con precios expresados en dólares. El código mantiene la separación aleatoria existente (`test_size=0.2`, `random_state=42`) y entrena con los registros de entrenamiento de esa separación. Los ejemplos no representan datos de mercado verificados ni incorporan ubicación o tipo de inmueble. Por ello, el resultado es orientativo, no constituye una tasación oficial ni un precio de mercado comprobado. La aplicación muestra la moneda devuelta por el backend (USD) y no convierte a MXN.

## Pruebas

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests
```
