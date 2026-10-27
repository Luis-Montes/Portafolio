import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split

def entrenar_modelos(ruta_csv: str):
    df = pd.read_csv(ruta_csv)
    total_original = len(df)
    print(f"Total de registros originales: {total_original}")

    columnas_criticas = ['price', 'bed', 'bath', 'house_size']

    df = df.dropna(subset=columnas_criticas)
    total_limpio = len(df)

    print(f"Total de registros después de eliminar nulos: {total_limpio}")
    print(f"Registros eliminados: {total_original - total_limpio}")

    if total_limpio == 0:
        raise ValueError("No hay suficientes datos después de eliminar nulos.")

    X = df[['bed', 'bath', 'house_size']]
    y_precio = df['price']

    X_train, X_test, y_train_precio, y_test_precio = train_test_split(X, y_precio, test_size=0.2, random_state=42)
    modelo_lineal = LinearRegression()
    modelo_lineal.fit(X_train, y_train_precio)

    mediana_precio = df['price'].median()
    y_clase = (df['price'] > mediana_precio).astype(int)

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_clase, test_size=0.2, random_state=42)
    modelo_logistico = LogisticRegression()
    modelo_logistico.fit(X_train_c, y_train_c)

    return modelo_lineal, modelo_logistico, mediana_precio