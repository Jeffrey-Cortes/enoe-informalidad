from typing import Literal

from pydantic import BaseModel, Field


class PersonaInput(BaseModel):
    EDA: int = Field(ge=15, le=97)

    ANTIGUEDAD: float | None = Field(
        default=None,
        ge=0
    )

    PAR_C_GRUPO: Literal[
        "jefe_hogar",
        "hijo",
        "pareja",
        "otro_familiar",
        "no_familiar_otro",
        "trabajo_domestico_familia",
        "no_especificado",
    ]

    ESCOLARIDAD_GRUPO: Literal[
        "sin_escolaridad",
        "preescolar",
        "primaria",
        "secundaria",
        "media_superior",
        "normal_tecnica",
        "profesional",
        "posgrado",
        "no_sabe",
    ]

    INGRESO_GRUPO: Literal[
        "sin_ingresos",
        "hasta_1_sm",
        "mas_1_hasta_2_sm",
        "mas_2_hasta_3_sm",
        "mas_3_hasta_5_sm",
        "mas_5_sm",
        "no_especificado",
    ]

    DURACION_GRUPO: Literal[
        "menos_15_horas",
        "15_a_34_horas",
        "35_a_48_horas",
        "mas_48_horas",
        "ausente_con_vinculo",
        "no_especificado",
    ]

    TAMANO_LOCALIDAD: Literal[
        "menos_2_500",
        "2_500_a_14_999",
        "15_mil_a_99_999",
        "mas_100_mil",
    ]

    ESTADO_CONYUGAL: Literal[
        "soltero",
        "union_libre",
        "casado",
        "separado",
        "divorciado",
        "viudo",
        "no_sabe",
    ]

    BUSQUEDA_OTRO_EMPLEO: Literal[
        "no_busco",
        "busco_otro_empleo",
        "no_especificado",
    ]

    TIENE_JEFE: Literal[
        "si",
        "no",
    ]

    SEXO: Literal[
        "hombre",
        "mujer",
    ]

    ENTIDAD: str
    

class FactorExplicativo(BaseModel):
    variable: str
    valor: str | int | float | None
    direccion: Literal[
        "aumenta",
        "reduce",
        "neutral",
    ]
    contribucion: float


class PrediccionOutput(BaseModel):
    probabilidad_informalidad: float
    nivel_riesgo: Literal[
        "bajo",
        "medio",
        "alto",
    ]

    factores_principales: list[FactorExplicativo]