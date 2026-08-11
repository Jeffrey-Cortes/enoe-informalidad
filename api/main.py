from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.predictor import predecir
from src.schemas import PersonaInput, PrediccionOutput


app = FastAPI(
    title="API de predicción de informalidad laboral",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "http://localhost:5173",
            "http://localhost:4173",
        ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de predicción de informalidad laboral activa"
    }


@app.post(
    "/predecir",
    response_model=PrediccionOutput
)
def predecir_informalidad(persona: PersonaInput):

    datos = persona.model_dump()

    resultado = predecir(datos)

    return resultado