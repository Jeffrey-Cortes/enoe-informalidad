from pathlib import Path

import joblib
import pandas as pd
import shap


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "modelo_final.joblib"
)

modelo = joblib.load(MODEL_PATH)

preprocesador = modelo.named_steps["preprocesador"]
hgb = modelo.named_steps["modelo"]

nombres_features = preprocesador.get_feature_names_out()

explainer = shap.TreeExplainer(hgb)


VARIABLES_MODELO = [
    "EDA",
    "ANTIGUEDAD",
    "PAR_C_GRUPO",
    "ESCOLARIDAD_GRUPO",
    "INGRESO_GRUPO",
    "DURACION_GRUPO",
    "TAMANO_LOCALIDAD",
    "ESTADO_CONYUGAL",
    "BUSQUEDA_OTRO_EMPLEO",
    "TIENE_JEFE",
    "SEXO",
    "ENTIDAD",
]


def clasificar_riesgo(probabilidad: float) -> str:
    if probabilidad < 0.33:
        return "bajo"
    elif probabilidad < 0.66:
        return "medio"
    return "alto"


def obtener_columnas_variable(variable: str) -> list[str]:

    if variable == "EDA":
        return [
            "numericas__EDA"
        ]

    if variable == "ANTIGUEDAD":
        return [
            columna
            for columna in nombres_features
            if columna in [
                "numericas__ANTIGUEDAD",
                "numericas__missingindicator_ANTIGUEDAD",
            ]
        ]

    prefijo = f"categoricas__{variable}_"

    return [
        columna
        for columna in nombres_features
        if columna.startswith(prefijo)
    ]


def explicar_prediccion(
    df_persona: pd.DataFrame,
    top_n: int = 5
) -> list[dict]:

    # Aplicar exactamente el preprocesamiento del pipeline
    X_transformado = preprocesador.transform(df_persona)

    # Calcular SHAP para la observación
    valores_shap = explainer(X_transformado).values[0]

    df_shap = pd.Series(
        valores_shap,
        index=nombres_features
    )

    contribuciones = []

    for variable in VARIABLES_MODELO:

        columnas = obtener_columnas_variable(variable)

        contribucion = float(
            df_shap[columnas].sum()
        )

        valor_original = df_persona.iloc[0][variable]

        # Convertir NaN a None para JSON
        if pd.isna(valor_original):
            valor_original = None

        contribuciones.append({
            "variable": variable,
            "valor": valor_original,
            "direccion": (
                "aumenta"
                if contribucion > 0
                else "reduce"
                if contribucion < 0
                else "neutral"
            ),
            "contribucion": contribucion,
        })

    contribuciones.sort(
        key=lambda x: abs(x["contribucion"]),
        reverse=True
    )

    return contribuciones[:top_n]


def predecir(datos_persona: dict) -> dict:

    faltantes = [
        variable
        for variable in VARIABLES_MODELO
        if variable not in datos_persona
    ]

    if faltantes:
        raise ValueError(
            f"Faltan variables requeridas: {faltantes}"
        )

    df_persona = pd.DataFrame([
        {
            variable: datos_persona[variable]
            for variable in VARIABLES_MODELO
        }
    ])

    probabilidad = float(
        modelo.predict_proba(df_persona)[0, 1]
    )

    factores = explicar_prediccion(
        df_persona,
        top_n=5
    )

    return {
        "probabilidad_informalidad": probabilidad,
        "nivel_riesgo": clasificar_riesgo(probabilidad),
        "factores_principales": factores,
    }