"""Generación de explicaciones en lenguaje natural para las predicciones.

No depende de ningún servicio externo: el texto se arma combinando
plantillas fijas por variable con la dirección e importancia calculadas
por SHAP en `predictor.explicar_prediccion`.
"""

ETIQUETAS = {
    "PAR_C_GRUPO": {
        "jefe_hogar": "jefe(a) del hogar",
        "hijo": "hijo(a)",
        "pareja": "pareja",
        "otro_familiar": "otro familiar",
        "no_familiar_otro": "no familiar / otro",
        "trabajo_domestico_familia": "trabajo doméstico / familia",
        "no_especificado": "no especificado",
    },
    "ESCOLARIDAD_GRUPO": {
        "sin_escolaridad": "sin escolaridad",
        "preescolar": "preescolar",
        "primaria": "primaria",
        "secundaria": "secundaria",
        "media_superior": "media superior",
        "normal_tecnica": "normal / técnica",
        "profesional": "profesional",
        "posgrado": "posgrado",
        "no_sabe": "no sabe",
    },
    "INGRESO_GRUPO": {
        "sin_ingresos": "sin ingresos",
        "hasta_1_sm": "hasta 1 salario mínimo",
        "mas_1_hasta_2_sm": "más de 1 y hasta 2 salarios mínimos",
        "mas_2_hasta_3_sm": "más de 2 y hasta 3 salarios mínimos",
        "mas_3_hasta_5_sm": "más de 3 y hasta 5 salarios mínimos",
        "mas_5_sm": "más de 5 salarios mínimos",
        "no_especificado": "no especificado",
    },
    "DURACION_GRUPO": {
        "menos_15_horas": "menos de 15 horas",
        "15_a_34_horas": "15 a 34 horas",
        "35_a_48_horas": "35 a 48 horas",
        "mas_48_horas": "más de 48 horas",
        "ausente_con_vinculo": "ausencia con vínculo laboral",
        "no_especificado": "no especificado",
    },
    "TAMANO_LOCALIDAD": {
        "menos_2_500": "menos de 2,500 habitantes",
        "2_500_a_14_999": "2,500 a 14,999 habitantes",
        "15_mil_a_99_999": "15,000 a 99,999 habitantes",
        "mas_100_mil": "100,000 habitantes o más",
    },
    "ESTADO_CONYUGAL": {
        "soltero": "soltero(a)",
        "union_libre": "unión libre",
        "casado": "casado(a)",
        "separado": "separado(a)",
        "divorciado": "divorciado(a)",
        "viudo": "viudo(a)",
        "no_sabe": "no sabe",
    },
    "SEXO": {
        "hombre": "hombre",
        "mujer": "mujer",
    },
    "ENTIDAD": {
        "01": "Aguascalientes", "02": "Baja California", "03": "Baja California Sur",
        "04": "Campeche", "05": "Coahuila", "06": "Colima", "07": "Chiapas",
        "08": "Chihuahua", "09": "Ciudad de México", "10": "Durango",
        "11": "Guanajuato", "12": "Guerrero", "13": "Hidalgo", "14": "Jalisco",
        "15": "Estado de México", "16": "Michoacán", "17": "Morelos",
        "18": "Nayarit", "19": "Nuevo León", "20": "Oaxaca", "21": "Puebla",
        "22": "Querétaro", "23": "Quintana Roo", "24": "San Luis Potosí",
        "25": "Sinaloa", "26": "Sonora", "27": "Tabasco", "28": "Tamaulipas",
        "29": "Tlaxcala", "30": "Veracruz", "31": "Yucatán", "32": "Zacatecas",
    },
}


def _frase_eda(valor):
    return f"tu edad ({valor} años)" if valor is not None else "tu edad"


def _frase_antiguedad(valor):
    if valor is None:
        return "no contar con antigüedad registrada en el empleo actual"
    return f"tu antigüedad de {valor:g} años en el empleo actual"


def _frase_categorica(variable, articulo_descripcion):
    def frase(valor):
        etiqueta = ETIQUETAS[variable].get(str(valor), str(valor))
        return f"{articulo_descripcion} ({etiqueta})"
    return frase


def _frase_busqueda_empleo(valor):
    if valor == "busco_otro_empleo":
        return "que actualmente buscas otro empleo"
    if valor == "no_busco":
        return "que actualmente no buscas otro empleo"
    return "tu situación de búsqueda de otro empleo"


def _frase_tiene_jefe(valor):
    if valor == "si":
        return "que tienes un jefe o superior directo"
    if valor == "no":
        return "que no tienes un jefe o superior directo"
    return "si tienes o no un jefe o superior directo"


def _frase_sexo(valor):
    etiqueta = ETIQUETAS["SEXO"].get(str(valor), str(valor))
    return f"ser {etiqueta}"


def _frase_entidad(valor):
    etiqueta = ETIQUETAS["ENTIDAD"].get(str(valor), str(valor))
    return f"vivir en {etiqueta}"


FRASES_VARIABLE = {
    "EDA": _frase_eda,
    "ANTIGUEDAD": _frase_antiguedad,
    "PAR_C_GRUPO": _frase_categorica("PAR_C_GRUPO", "tu relación con el jefe del hogar"),
    "ESCOLARIDAD_GRUPO": _frase_categorica("ESCOLARIDAD_GRUPO", "tu nivel de escolaridad"),
    "INGRESO_GRUPO": _frase_categorica("INGRESO_GRUPO", "tu nivel de ingreso laboral"),
    "DURACION_GRUPO": _frase_categorica("DURACION_GRUPO", "tu jornada laboral"),
    "TAMANO_LOCALIDAD": _frase_categorica("TAMANO_LOCALIDAD", "el tamaño de la localidad donde vives"),
    "ESTADO_CONYUGAL": _frase_categorica("ESTADO_CONYUGAL", "tu estado conyugal"),
    "BUSQUEDA_OTRO_EMPLEO": _frase_busqueda_empleo,
    "TIENE_JEFE": _frase_tiene_jefe,
    "SEXO": _frase_sexo,
    "ENTIDAD": _frase_entidad,
}


def _describir_factor(factor: dict) -> str:
    generador = FRASES_VARIABLE.get(factor["variable"])

    if generador is None:
        return str(factor["variable"])

    return generador(factor["valor"])


def _unir_frases(frases: list[str]) -> str:
    if len(frases) == 1:
        return frases[0]

    return ", ".join(frases[:-1]) + " y " + frases[-1]


def generar_explicacion(prediccion: dict) -> str:
    """Arma un párrafo en español que interpreta la predicción para
    una persona sin conocimientos técnicos, usando solo los datos que
    ya vienen en `prediccion` (probabilidad, nivel de riesgo y factores).
    """

    probabilidad = prediccion["probabilidad_informalidad"]
    nivel = prediccion["nivel_riesgo"]
    factores = prediccion["factores_principales"]

    porcentaje = round(probabilidad * 100)

    calificativo_nivel = {
        "alto": "un nivel de riesgo alto",
        "medio": "un nivel de riesgo medio",
        "bajo": "un nivel de riesgo bajo",
    }[nivel]

    apertura = (
        f"Con las características que proporcionaste, el modelo estima "
        f"una probabilidad de {porcentaje}% de que el empleo sea "
        f"informal, lo que corresponde a {calificativo_nivel}."
    )

    aumentan = [f for f in factores if f["direccion"] == "aumenta"]
    reducen = [f for f in factores if f["direccion"] == "reduce"]

    partes = [apertura]

    if aumentan:
        frases = [_describir_factor(f) for f in aumentan[:3]]
        verbo = "eleva" if len(frases) == 1 else "elevan"
        partes.append(
            f"Lo que más {verbo} esta estimación es {_unir_frases(frases)}."
        )

    if reducen:
        frases = [_describir_factor(f) for f in reducen[:3]]
        verbo = "ayuda" if len(frases) == 1 else "ayudan"
        conector = "Por otro lado, lo" if aumentan else "Lo"
        partes.append(
            f"{conector} que más {verbo} a reducirla es {_unir_frases(frases)}."
        )

    if not aumentan and not reducen:
        partes.append(
            "Ninguna de tus características tuvo un peso relevante en "
            "esta estimación."
        )

    partes.append(
        "Estos factores reflejan patrones estadísticos que el modelo "
        "encontró en los datos de la ENOE, no relaciones de causa y "
        "efecto sobre tu situación particular."
    )

    return " ".join(partes)
