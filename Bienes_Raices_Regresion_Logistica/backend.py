import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def precio_casas():
    datos = {
        "metros_cuadrados": [50, 60, 70, 80, 90, 100],
        "habitaciones": [1, 2, 2, 3, 3, 4],
        "antiguedad": [5, 10, 15, 20, 25, 30],
        "precio": [100000, 120000, 140000, 160000, 180000, 200000]
    }

    df = pd.DataFrame(datos)
    print("Datos historicos cargasdos correctamente")

    X = df[["metros_cuadrados", "habitaciones", "antiguedad"]]
    y = df["precio"]

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo_inmobiliario = LinearRegression()
    modelo_inmobiliario.fit(x_train, y_train)
    print("Modelo de predicción entrenado correctamente")

    casa_nueva = pd.DataFrame({
        "metros_cuadrados": [75],
        "habitaciones": [3],
        "antiguedad": [10]
    })

    precio_estimado = modelo_inmobiliario.predict(casa_nueva)

    print("--- Predicción para la Nueva Casa ---")
    print(
        f"El precio de venta sugerido por el modelo es: ${precio_estimado[0]:,.2f}"
        " dólares"
    )

    # Opcional: Ver el valor del Sesgo (Intercepto) o cuánto aporta cada metro cuadrado
    print(
        "\nPrecio base (Sesgo / Intercepto):"
        f" ${modelo_inmobiliario.intercept_:,.2f}"
    )
    print(
        "Impacto por metro cuadrado (Coeficiente):"
        f" ${modelo_inmobiliario.coef_[0]:,.2f} por m²"
    )

precio_casas()