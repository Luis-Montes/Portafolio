# Importa el ejecutor asíncrono usado para probar los endpoints.
import asyncio
# Importa la conversión de objetos Python a JSON en las pruebas.
import json
# Importa las herramientas estándar para definir y ejecutar pruebas.
import unittest

# Define la función que atiende una solicitud HTTP.
from starlette.requests import Request

# Carga las funciones y la aplicación backend que se van a probar.
import backend


# Define una utilidad que construye solicitudes para las pruebas.
def make_request(body: bytes) -> Request:
    # Registra si el cuerpo de la solicitud ya fue enviado.
    sent = False

    # Simula el canal asíncrono que entrega el cuerpo HTTP a Starlette.
    async def receive() -> dict[str, object]:
        # Permite actualizar la variable sent del ámbito exterior.
        nonlocal sent
        # Indica a Starlette que no hay más contenido por recibir.
        if sent:
            # Entrega al cliente la respuesta simulada de la solicitud.
            return {"type": "http.disconnect"}
        # Registra si el cuerpo de la solicitud ya fue enviado.
        sent = True
        # Entrega al cliente la respuesta simulada de la solicitud.
        return {"type": "http.request", "body": body, "more_body": False}

    # Define la información ASGI básica de la solicitud simulada.
    scope = {
        # Identifica esta estructura como una solicitud HTTP ASGI.
        "type": "http",
        # Especifica el método HTTP usado por la prueba.
        "method": "POST",
        # Indica la ruta del endpoint que se está probando.
        "path": "/api/estimate",
        # Declara que el cuerpo enviado está codificado como JSON.
        "headers": [(b"content-type", b"application/json")],
    # Cierra la estructura abierta en las líneas anteriores.
    }
    # Define la función que atiende una solicitud HTTP.
    return Request(scope, receive)


# Agrupa las pruebas unitarias de la función de predicción.
class PriceCalculationTests(unittest.TestCase):
    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_existing_demo_input_uses_the_existing_model(self) -> None:
        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(backend.calcular_precio(75, 3, 10), 144000.0)

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_calculation_rejects_non_positive_area(self) -> None:
        # Comprueba que la entrada inválida genera la excepción esperada.
        with self.assertRaises(ValueError):
            # Completa la instrucción que implementa la operación actual.
            backend.calcular_precio(0, 3, 10)

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_calculation_rejects_negative_or_fractional_counts(self) -> None:
        # Comprueba que la entrada inválida genera la excepción esperada.
        with self.assertRaises(ValueError):
            # Completa la instrucción que implementa la operación actual.
            backend.calcular_precio(75, -1, 10)
        # Comprueba que la entrada inválida genera la excepción esperada.
        with self.assertRaises(ValueError):
            # Completa la instrucción que implementa la operación actual.
            backend.calcular_precio(75, 2.5, 10)
        # Comprueba que la entrada inválida genera la excepción esperada.
        with self.assertRaises(ValueError):
            # Completa la instrucción que implementa la operación actual.
            backend.calcular_precio(75, 3, -1)


# Agrupa las pruebas del endpoint HTTP de estimación.
class EstimateEndpointTests(unittest.TestCase):
    # Envía un cuerpo al endpoint durante las pruebas.
    def post(self, body: bytes):
        # Ejecuta el endpoint asíncrono dentro de la prueba síncrona.
        return asyncio.run(backend.estimar_precio_endpoint(make_request(body)))

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_valid_request_returns_price_currency_and_timestamp(self) -> None:
        # Guarda la respuesta del endpoint para comprobarla.
        response = self.post(json.dumps({
            # Declara el campo de datos correspondiente.
            "metros_cuadrados": 75,
            # Declara el campo de datos correspondiente.
            "habitaciones": 3,
            # Declara el campo de datos correspondiente.
            "antiguedad": 10,
        # Cierra la estructura abierta en las líneas anteriores.
        }).encode())

        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(response.status_code, 200)
        # Asigna o declara el valor utilizado por la operación actual.
        result = json.loads(response.body)
        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(result["precio_estimado"], 144000.0)
        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(result["moneda"], "USD")
        # Comprueba que el valor devuelto representa una condición verdadera.
        self.assertTrue(result["calculado_en"])

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_missing_features_are_rejected(self) -> None:
        # Guarda la respuesta del endpoint para comprobarla.
        response = self.post(b'{"metros_cuadrados": 75}')

        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(response.status_code, 422)
        # Comprueba que la respuesta contiene el campo indicado.
        self.assertIn("detail", json.loads(response.body))

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_invalid_numbers_are_rejected_without_prediction(self) -> None:
        # Prueba varias combinaciones inválidas de forma parametrizada.
        for payload in (
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": 0, "habitaciones": 3, "antiguedad": 10},
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": 75, "habitaciones": -1, "antiguedad": 10},
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": 75, "habitaciones": 3.5, "antiguedad": 10},
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": 75, "habitaciones": 3, "antiguedad": -1},
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": True, "habitaciones": 3, "antiguedad": 10},
            # Completa la instrucción que implementa la operación actual.
            {"metros_cuadrados": 10**400, "habitaciones": 3, "antiguedad": 10},
        # Cierra la estructura abierta en las líneas anteriores.
        ):
            # Identifica qué conjunto de datos produjo un fallo de prueba.
            with self.subTest(payload=payload):
                # Guarda la respuesta del endpoint para comprobarla.
                response = self.post(json.dumps(payload).encode())
                # Comprueba que el resultado coincide con el valor esperado.
                self.assertEqual(response.status_code, 422)
                # Comprueba que una solicitud inválida no devuelve un precio.
                self.assertNotIn("precio_estimado", json.loads(response.body))

    # Define una prueba que verifica un comportamiento esperado del backend.
    def test_invalid_json_is_rejected(self) -> None:
        # Guarda la respuesta del endpoint para comprobarla.
        response = self.post(b"{")

        # Comprueba que el resultado coincide con el valor esperado.
        self.assertEqual(response.status_code, 400)
        # Comprueba que la respuesta contiene el campo indicado.
        self.assertIn("detail", json.loads(response.body))


# Ejecuta la demostración solo al iniciar este archivo directamente.
if __name__ == "__main__":
    # Completa la instrucción que implementa la operación actual.
    unittest.main()
