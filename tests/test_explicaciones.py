from src.explicaciones import generar_explicacion


def _factor(variable, valor, direccion, contribucion):
    return {
        "variable": variable,
        "valor": valor,
        "direccion": direccion,
        "contribucion": contribucion,
    }


def test_solo_factores_que_aumentan():
    prediccion = {
        "probabilidad_informalidad": 0.9,
        "nivel_riesgo": "alto",
        "factores_principales": [
            _factor("INGRESO_GRUPO", "sin_ingresos", "aumenta", 0.3),
            _factor("TIENE_JEFE", "no", "aumenta", 0.2),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "90%" in texto
    assert "riesgo alto" in texto
    assert "elevan esta estimación" in texto
    assert "reducirla" not in texto


def test_solo_factores_que_reducen():
    prediccion = {
        "probabilidad_informalidad": 0.1,
        "nivel_riesgo": "bajo",
        "factores_principales": [
            _factor("ESCOLARIDAD_GRUPO", "profesional", "reduce", -0.2),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "10%" in texto
    assert "riesgo bajo" in texto
    assert "ayuda a reducirla" in texto
    assert "eleva" not in texto


def test_factores_mixtos_usan_plural_y_conector():
    prediccion = {
        "probabilidad_informalidad": 0.5,
        "nivel_riesgo": "medio",
        "factores_principales": [
            _factor("INGRESO_GRUPO", "sin_ingresos", "aumenta", 0.3),
            _factor("TIENE_JEFE", "no", "aumenta", 0.2),
            _factor("ESCOLARIDAD_GRUPO", "profesional", "reduce", -0.15),
            _factor("EDA", 45, "reduce", -0.05),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "elevan esta estimación" in texto
    assert "Por otro lado, lo que más ayudan a reducirla" in texto
    assert " y " in texto


def test_todo_neutral_no_menciona_factores():
    prediccion = {
        "probabilidad_informalidad": 0.4,
        "nivel_riesgo": "medio",
        "factores_principales": [
            _factor("SEXO", "hombre", "neutral", 0.0),
            _factor("ANTIGUEDAD", 3.0, "neutral", 0.0),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "Lo que más" not in texto
    assert "reducirla" not in texto
    assert "Ninguna de tus características tuvo un peso relevante" in texto


def test_valor_none_en_antiguedad():
    prediccion = {
        "probabilidad_informalidad": 0.6,
        "nivel_riesgo": "medio",
        "factores_principales": [
            _factor("ANTIGUEDAD", None, "aumenta", 0.1),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "no contar con antigüedad registrada en el empleo actual" in texto


def test_lista_de_un_solo_factor_no_usa_coma():
    prediccion = {
        "probabilidad_informalidad": 0.7,
        "nivel_riesgo": "alto",
        "factores_principales": [
            _factor("ENTIDAD", "09", "aumenta", 0.4),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "vivir en Ciudad de México" in texto
    assert "eleva esta estimación" in texto


def test_variable_desconocida_no_rompe():
    prediccion = {
        "probabilidad_informalidad": 0.55,
        "nivel_riesgo": "medio",
        "factores_principales": [
            _factor("VARIABLE_NUEVA_NO_MAPEADA", "x", "aumenta", 0.1),
        ],
    }

    texto = generar_explicacion(prediccion)

    assert "VARIABLE_NUEVA_NO_MAPEADA" in texto
