from fastapi.testclient import TestClient
import pytest
from api.main import app


client = TestClient(app)


PERSONA_VALIDA = {
    "EDA": 15,
    "ANTIGUEDAD": 1.0,
    "PAR_C_GRUPO": "otro_familiar",
    "ESCOLARIDAD_GRUPO": "secundaria",
    "INGRESO_GRUPO": "sin_ingresos",
    "DURACION_GRUPO": "menos_15_horas",
    "TAMANO_LOCALIDAD": "menos_2_500",
    "ESTADO_CONYUGAL": "soltero",
    "BUSQUEDA_OTRO_EMPLEO": "no_busco",
    "TIENE_JEFE": "si",
    "SEXO": "mujer",
    "ENTIDAD": "Veracruz",
}


def test_inicio():
    response = client.get("/")

    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_prediccion_valida():
    response = client.post(
        "/predecir",
        json=PERSONA_VALIDA
    )

    assert response.status_code == 200

    data = response.json()

    assert "probabilidad_informalidad" in data
    assert "nivel_riesgo" in data
    assert "factores_principales" in data

    assert 0 <= data["probabilidad_informalidad"] <= 1

    assert data["nivel_riesgo"] in [
        "bajo",
        "medio",
        "alto",
    ]

    assert len(data["factores_principales"]) == 5


def test_edad_fuera_de_rango():
    persona = PERSONA_VALIDA.copy()
    persona["EDA"] = 99

    response = client.post(
        "/predecir",
        json=persona
    )

    assert response.status_code == 422


def test_categoria_invalida():
    persona = PERSONA_VALIDA.copy()
    persona["ESCOLARIDAD_GRUPO"] = "doctorado"

    response = client.post(
        "/predecir",
        json=persona
    )

    assert response.status_code == 422


def test_variable_faltante():
    persona = PERSONA_VALIDA.copy()
    persona.pop("INGRESO_GRUPO")

    response = client.post(
        "/predecir",
        json=persona
    )

    assert response.status_code == 422
    
def test_probabilidad_perfil_conocido():
    response = client.post(
        "/predecir",
        json=PERSONA_VALIDA
    )

    assert response.status_code == 200

    probabilidad = response.json()["probabilidad_informalidad"]

    assert probabilidad == pytest.approx(
        0.9996042262570055,
        abs=1e-10
    )