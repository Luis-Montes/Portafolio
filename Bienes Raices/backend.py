# Prepara el registro de errores del servidor.
import logging
# Importa utilidades para guardar la fecha y la hora del cálculo.
from datetime import datetime, timezone
# Permite reutilizar el modelo ya entrenado.
from functools import lru_cache
# Identifica errores al interpretar el JSON recibido.
from json import JSONDecodeError
# Permite comprobar que los números no sean infinitos ni inválidos.
from math import isfinite
# Permite localizar los archivos de la aplicación.
from pathlib import Path
# Permite tipar valores JSON de distintos tipos.
from typing import Any

# Importa pandas para preparar los datos del modelo.
import pandas as pd
# Importa el modelo de regresión lineal usado para estimar precios.
from sklearn.linear_model import LinearRegression
# Importa la separación de los datos para conservar el entrenamiento original.
from sklearn.model_selection import train_test_split
# Importa el framework que expone la aplicación web.
from starlette.applications import Starlette
# Define la función que atiende una solicitud HTTP.
from starlette.requests import Request
# Importa la respuesta que sirve un archivo al navegador.
from starlette.responses import FileResponse, JSONResponse
# Importa la herramienta para asociar rutas y funciones.
from starlette.routing import Route


# Prepara el registro de errores del servidor.
logger = logging.getLogger(__name__)

# Define los seis ejemplos que usa el modelo; los precios están expresados en dólares.
DATOS_HISTORICOS = {
    # Registra las superficies de los ejemplos históricos.
    "metros_cuadrados": [50, 60, 70, 80, 90, 100],
    # Registra las habitaciones de los ejemplos históricos.
    "habitaciones": [1, 2, 2, 3, 3, 4],
    # Registra la antigüedad de los ejemplos históricos.
    "antiguedad": [5, 10, 15, 20, 25, 30],
    # Registra los precios de los ejemplos históricos en dólares.
    "precio": [100000, 120000, 140000, 160000, 180000, 200000],
# Cierra la estructura abierta en las líneas anteriores.
}
# Indica qué columnas utiliza el modelo como variables de entrada.
CARACTERISTICAS = ["metros_cuadrados", "habitaciones", "antiguedad"]


# Reutiliza en memoria el modelo para evitar reentrenarlo por solicitud.
@lru_cache(maxsize=1)
# Importa el modelo de regresión lineal usado para estimar precios.
def obtener_modelo() -> LinearRegression:
    # Convierte el conjunto de ejemplos a una tabla de pandas.
    datos = pd.DataFrame(DATOS_HISTORICOS)
    # Indica qué columnas utiliza el modelo como variables de entrada.
    caracteristicas = datos[CARACTERISTICAS]
    # Selecciona la columna de precios que el modelo debe aprender.
    precios = datos["precio"]
    # Separa los ejemplos conservando el tamaño y la semilla originales.
    x_train, _, y_train, _ = train_test_split(
        # Divide las entradas y los precios para entrenar el modelo.
        caracteristicas, precios, test_size=0.2, random_state=42
    # Cierra la estructura abierta en las líneas anteriores.
    )
    # Importa el modelo de regresión lineal usado para estimar precios.
    modelo = LinearRegression()
    # Ajusta la regresión lineal con los datos de entrenamiento.
    modelo.fit(x_train, y_train)
    # Devuelve el modelo entrenado para que pueda calcular estimaciones.
    return modelo


# Declara el cálculo reutilizable que aplica el modelo a una propiedad.
def calcular_precio(
    # Completa la instrucción que implementa la operación actual.
    metros_cuadrados: float, habitaciones: int, antiguedad: int
# Cierra la estructura abierta en las líneas anteriores.
) -> float:
    # Agrupa las entradas para validar que sean valores numéricos finitos.
    valores = (metros_cuadrados, habitaciones, antiguedad)
    # Permite comprobar que los números no sean infinitos ni inválidos.
    if any(isinstance(value, bool) or not isfinite(value) for value in valores):
        # Completa la instrucción que implementa la operación actual.
        raise ValueError("Las características deben ser números finitos.")
    # Valida que la superficie sea mayor que cero.
    if metros_cuadrados <= 0:
        # Completa la instrucción que implementa la operación actual.
        raise ValueError("La superficie debe ser mayor que cero.")
    # Valida que las habitaciones sean un entero no negativo.
    if habitaciones < 0 or not float(habitaciones).is_integer():
        # Completa la instrucción que implementa la operación actual.
        raise ValueError("Las habitaciones deben ser un entero de cero o más.")
    # Valida que la antigüedad sea un entero no negativo.
    if antiguedad < 0 or not float(antiguedad).is_integer():
        # Completa la instrucción que implementa la operación actual.
        raise ValueError("La antigüedad debe ser un entero de cero o más.")

    # Prepara las características de la propiedad en el formato esperado por pandas.
    propiedad = pd.DataFrame(
        # Abre una estructura cuyos datos se especifican en las líneas siguientes.
        [{
            # Declara el campo de datos correspondiente.
            "metros_cuadrados": metros_cuadrados,
            # Declara el campo de datos correspondiente.
            "habitaciones": habitaciones,
            # Declara el campo de datos correspondiente.
            "antiguedad": antiguedad,
        # Cierra la estructura abierta en las líneas anteriores.
        }],
        # Indica qué columnas utiliza el modelo como variables de entrada.
        columns=CARACTERISTICAS,
    # Cierra la estructura abierta en las líneas anteriores.
    )
    # Obtiene del modelo la predicción para la propiedad y la convierte a número.
    precio = float(obtener_modelo().predict(propiedad)[0])
    # Permite comprobar que los números no sean infinitos ni inválidos.
    if not isfinite(precio):
        # Completa la instrucción que implementa la operación actual.
        raise ValueError("El modelo no produjo una estimación válida.")
    # Devuelve el precio calculado por el modelo.
    return precio


# Conserva la demostración de consola que traía el archivo original.
def precio_casas() -> None:
    # Declara el campo de datos correspondiente.
    """Conserva la demostración de consola que incluía el archivo original."""
    # Calcula el precio con las características recibidas y ya validadas.
    precio_estimado = calcular_precio(75, 3, 10)
    # Recupera el modelo entrenado y almacenado en caché.
    modelo = obtener_modelo()
    # Imprime el valor informativo de la demostración.
    print("Datos historicos cargasdos correctamente")
    # Imprime el valor informativo de la demostración.
    print("Modelo de predicción entrenado correctamente")
    # Imprime el valor informativo de la demostración.
    print("--- Predicción para la Nueva Casa ---")
    # Imprime el valor informativo de la demostración.
    print(
        # Completa la instrucción que implementa la operación actual.
        f"El precio de venta sugerido por el modelo es: "
        # Completa la instrucción que implementa la operación actual.
        f"${precio_estimado:,.2f} dólares"
    # Cierra la estructura abierta en las líneas anteriores.
    )
    # Imprime el valor informativo de la demostración.
    print("\nPrecio base (Sesgo / Intercepto):")
    # Imprime el valor informativo de la demostración.
    print(f" ${modelo.intercept_:,.2f}")
    # Imprime el valor informativo de la demostración.
    print("Impacto por metro cuadrado (Coeficiente):")
    # Imprime el valor informativo de la demostración.
    print(f" ${modelo.coef_[0]:,.2f} por m²")


# Define la ruta que sirve la página principal.
async def pagina_inicio(_: Request) -> FileResponse:
    # Envía el documento HTML solicitado al navegador.
    return FileResponse(Path(__file__).with_name("index.html"))


# Define una ruta que confirma que el servicio está activo.
async def estado_api(_: Request) -> JSONResponse:
    # Devuelve una respuesta HTTP codificada como JSON.
    return JSONResponse({"status": "ok"})


# Define una función auxiliar para validar valores numéricos del JSON.
def numero_requerido(payload: dict[str, Any], campo: str) -> float | None:
    # Lee el valor solicitado del cuerpo JSON.
    valor = payload.get(campo)
    # Rechaza valores que no sean números JSON válidos.
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        # Señala que el dato no es válido y no debe entrar al modelo.
        return None
    # Inicia un bloque protegido para manejar errores de esta operación.
    try:
        # Convierte la entrada validada a número decimal.
        numero = float(valor)
    # Maneja valores numéricos que no pueden convertirse.
    except (OverflowError, ValueError):
        # Señala que el dato no es válido y no debe entrar al modelo.
        return None
    # Permite comprobar que los números no sean infinitos ni inválidos.
    return numero if isfinite(numero) else None


# Define la función que atiende una solicitud HTTP.
async def estimar_precio_endpoint(request: Request) -> JSONResponse:
    # Inicia un bloque protegido para manejar errores de esta operación.
    try:
        # Lee el cuerpo JSON de la solicitud HTTP.
        payload = await request.json()
    # Identifica errores al interpretar el JSON recibido.
    except (JSONDecodeError, UnicodeDecodeError):
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse({"detail": "El cuerpo de la solicitud debe ser JSON válido."}, status_code=400)

    # Asegura que el JSON recibido sea un objeto con campos.
    if not isinstance(payload, dict):
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse({"detail": "Envía las características de una propiedad."}, status_code=422)

    # Obtiene y valida la superficie requerida por el modelo.
    metros_cuadrados = numero_requerido(payload, "metros_cuadrados")
    # Obtiene y valida el número de habitaciones.
    habitaciones = numero_requerido(payload, "habitaciones")
    # Obtiene y valida los años de antigüedad.
    antiguedad = numero_requerido(payload, "antiguedad")
    # Valida que la superficie sea mayor que cero.
    if metros_cuadrados is None or habitaciones is None or antiguedad is None:
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse(
            # Abre una estructura cuyos datos se especifican en las líneas siguientes.
            {
                # Define el mensaje de error seguro que recibirá el navegador.
                "detail": (
                    # Inicia el mensaje que explica cuáles valores faltan o son inválidos.
                    "Indica metros_cuadrados, habitaciones y antiguedad "
                    # Completa el mensaje de validación para los datos de entrada.
                    "con valores numéricos válidos."
                # Cierra la estructura abierta en las líneas anteriores.
                )
            # Cierra la estructura abierta en las líneas anteriores.
            },
            # Establece el código HTTP que describe el resultado.
            status_code=422,
        # Cierra la estructura abierta en las líneas anteriores.
        )
    # Valida que la superficie sea mayor que cero.
    if metros_cuadrados <= 0:
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse(
            # Define el mensaje de error seguro que recibirá el navegador.
            {"detail": "Los metros cuadrados deben ser mayores que cero."},
            # Establece el código HTTP que describe el resultado.
            status_code=422,
        # Cierra la estructura abierta en las líneas anteriores.
        )
    # Valida que las habitaciones sean un entero no negativo.
    if habitaciones < 0 or not habitaciones.is_integer():
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse(
            # Define el mensaje de error seguro que recibirá el navegador.
            {"detail": "Las habitaciones deben ser un entero de cero o más."},
            # Establece el código HTTP que describe el resultado.
            status_code=422,
        # Cierra la estructura abierta en las líneas anteriores.
        )
    # Valida que la antigüedad sea un entero no negativo.
    if antiguedad < 0 or not antiguedad.is_integer():
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse(
            # Define el mensaje de error seguro que recibirá el navegador.
            {"detail": "La antigüedad debe ser un entero de cero o más."},
            # Establece el código HTTP que describe el resultado.
            status_code=422,
        # Cierra la estructura abierta en las líneas anteriores.
        )

    # Inicia un bloque protegido para manejar errores de esta operación.
    try:
        # Calcula el precio con las características recibidas y ya validadas.
        precio_estimado = calcular_precio(
            # Completa la instrucción que implementa la operación actual.
            metros_cuadrados, int(habitaciones), int(antiguedad)
        # Cierra la estructura abierta en las líneas anteriores.
        )
    # Registra el fallo interno y devuelve un mensaje sin detalles sensibles.
    except Exception:
        # Guarda los detalles técnicos del error solo en los registros del servidor.
        logger.exception("Falló el cálculo del precio estimado.")
        # Devuelve una respuesta HTTP codificada como JSON.
        return JSONResponse(
            # Define el mensaje de error seguro que recibirá el navegador.
            {"detail": "No fue posible calcular la estimación. Inténtalo de nuevo."},
            # Establece el código HTTP que describe el resultado.
            status_code=500,
        # Cierra la estructura abierta en las líneas anteriores.
        )

    # Devuelve una respuesta HTTP codificada como JSON.
    return JSONResponse(
        # Abre una estructura cuyos datos se especifican en las líneas siguientes.
        {
            # Incluye el precio calculado por el modelo.
            "precio_estimado": precio_estimado,
            # Indica la moneda en que están expresados los datos de entrenamiento.
            "moneda": "USD",
            # Importa utilidades para guardar la fecha y la hora del cálculo.
            "calculado_en": datetime.now(timezone.utc).isoformat(),
        # Cierra la estructura abierta en las líneas anteriores.
        }
    # Cierra la estructura abierta en las líneas anteriores.
    )


# Crea la aplicación web y registra las rutas que puede atender.
app = Starlette(
    # Evita exponer información interna mediante errores de depuración.
    debug=False,
    # Reúne las rutas públicas de la aplicación.
    routes=[
        # Registra un endpoint y el método HTTP que acepta.
        Route("/", pagina_inicio, methods=["GET"]),
        # Registra un endpoint y el método HTTP que acepta.
        Route("/api/health", estado_api, methods=["GET"]),
        # Registra un endpoint y el método HTTP que acepta.
        Route("/api/estimate", estimar_precio_endpoint, methods=["POST"]),
    # Cierra la estructura abierta en las líneas anteriores.
    ],
# Cierra la estructura abierta en las líneas anteriores.
)


# Ejecuta la demostración solo al iniciar este archivo directamente.
if __name__ == "__main__":
    # Lanza la demostración original de predicción por consola.
    precio_casas()
