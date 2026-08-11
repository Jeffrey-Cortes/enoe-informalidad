import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

const opciones = {
  PAR_C_GRUPO: [
    ["jefe_hogar", "Jefe(a) del hogar"],
    ["hijo", "Hijo(a)"],
    ["pareja", "Pareja"],
    ["otro_familiar", "Otro familiar"],
    ["no_familiar_otro", "No familiar / otro"],
    ["trabajo_domestico_familia", "Trabajo doméstico / familia"],
    ["no_especificado", "No especificado"],
  ],

  ESCOLARIDAD_GRUPO: [
    ["sin_escolaridad", "Sin escolaridad"],
    ["preescolar", "Preescolar"],
    ["primaria", "Primaria"],
    ["secundaria", "Secundaria"],
    ["media_superior", "Media superior"],
    ["normal_tecnica", "Normal / técnica"],
    ["profesional", "Profesional"],
    ["posgrado", "Posgrado"],
    ["no_sabe", "No sabe"],
  ],

  INGRESO_GRUPO: [
    ["sin_ingresos", "Sin ingresos"],
    ["hasta_1_sm", "Hasta 1 salario mínimo"],
    ["mas_1_hasta_2_sm", "Más de 1 y hasta 2 salarios mínimos"],
    ["mas_2_hasta_3_sm", "Más de 2 y hasta 3 salarios mínimos"],
    ["mas_3_hasta_5_sm", "Más de 3 y hasta 5 salarios mínimos"],
    ["mas_5_sm", "Más de 5 salarios mínimos"],
    ["no_especificado", "No especificado"],
  ],

  DURACION_GRUPO: [
    ["menos_15_horas", "Menos de 15 horas"],
    ["15_a_34_horas", "15 a 34 horas"],
    ["35_a_48_horas", "35 a 48 horas"],
    ["mas_48_horas", "Más de 48 horas"],
    ["ausente_con_vinculo", "Ausente con vínculo laboral"],
    ["no_especificado", "No especificado"],
  ],

  TAMANO_LOCALIDAD: [
    ["menos_2_500", "Menos de 2,500 habitantes"],
    ["2_500_a_14_999", "2,500 a 14,999 habitantes"],
    ["15_mil_a_99_999", "15,000 a 99,999 habitantes"],
    ["mas_100_mil", "100,000 habitantes o más"],
  ],

  ESTADO_CONYUGAL: [
    ["soltero", "Soltero(a)"],
    ["union_libre", "Unión libre"],
    ["casado", "Casado(a)"],
    ["separado", "Separado(a)"],
    ["divorciado", "Divorciado(a)"],
    ["viudo", "Viudo(a)"],
    ["no_sabe", "No sabe"],
  ],

  BUSQUEDA_OTRO_EMPLEO: [
    ["no_busco", "No buscó otro empleo"],
    ["busco_otro_empleo", "Buscó otro empleo"],
    ["no_especificado", "No especificado"],
  ],

  TIENE_JEFE: [
    ["si", "Sí"],
    ["no", "No"],
  ],

  SEXO: [
    ["hombre", "Hombre"],
    ["mujer", "Mujer"],
  ],

  ENTIDAD: [
    ["01", "Aguascalientes"],
    ["02", "Baja California"],
    ["03", "Baja California Sur"],
    ["04", "Campeche"],
    ["05", "Coahuila"],
    ["06", "Colima"],
    ["07", "Chiapas"],
    ["08", "Chihuahua"],
    ["09", "Ciudad de México"],
    ["10", "Durango"],
    ["11", "Guanajuato"],
    ["12", "Guerrero"],
    ["13", "Hidalgo"],
    ["14", "Jalisco"],
    ["15", "Estado de México"],
    ["16", "Michoacán"],
    ["17", "Morelos"],
    ["18", "Nayarit"],
    ["19", "Nuevo León"],
    ["20", "Oaxaca"],
    ["21", "Puebla"],
    ["22", "Querétaro"],
    ["23", "Quintana Roo"],
    ["24", "San Luis Potosí"],
    ["25", "Sinaloa"],
    ["26", "Sonora"],
    ["27", "Tabasco"],
    ["28", "Tamaulipas"],
    ["29", "Tlaxcala"],
    ["30", "Veracruz"],
    ["31", "Yucatán"],
    ["32", "Zacatecas"],
  ],
};

const nombresVariables = {
  EDA: "Edad",
  ANTIGUEDAD: "Antigüedad laboral",
  PAR_C_GRUPO: "Relación en el hogar",
  ESCOLARIDAD_GRUPO: "Escolaridad",
  INGRESO_GRUPO: "Ingreso laboral",
  DURACION_GRUPO: "Jornada laboral",
  TAMANO_LOCALIDAD: "Tamaño de localidad",
  ESTADO_CONYUGAL: "Estado conyugal",
  BUSQUEDA_OTRO_EMPLEO: "Búsqueda de otro empleo",
  TIENE_JEFE: "Tiene jefe o superior",
  SEXO: "Sexo",
  ENTIDAD: "Entidad federativa",
};

function obtenerEtiqueta(variable, valor) {
  if (variable === "EDA") {
    return `${valor} años`;
  }

  if (variable === "ANTIGUEDAD") {
    return `${valor} años`;
  }

  const lista = opciones[variable];

  if (!lista) {
    return String(valor);
  }

  const opcion = lista.find(([value]) => value === String(valor));

  return opcion ? opcion[1] : String(valor);
}

function SelectCampo({ nombre, etiqueta, valor, onChange }) {
  return (
    <div className="campo">
      <label htmlFor={nombre}>{etiqueta}</label>

      <select
        id={nombre}
        name={nombre}
        value={valor}
        onChange={onChange}
        required
      >
        <option value="">Selecciona una opción</option>

        {opciones[nombre].map(([value, label]) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
}

function Resultado({ resultado }) {
  const porcentaje = (
    resultado.probabilidad_informalidad * 100
  ).toFixed(1);

  const nivel = resultado.nivel_riesgo.toLowerCase();

  return (
    <section className="resultado" aria-live="polite">
      <p className="resultado-etiqueta">
        Probabilidad estimada de informalidad
      </p>

      <div className="probabilidad">{porcentaje}%</div>

      <div className={`nivel nivel-${nivel}`}>
        Riesgo {nivel}
      </div>

      <div className="separador" />

      <h2>Factores principales</h2>

      <p className="resultado-descripcion">
        Características que más influyeron en esta estimación.
      </p>

      <div className="factores">
        {resultado.factores_principales.map((factor, index) => {
          const aumenta = factor.direccion === "aumenta";

          return (
            <div className="factor" key={`${factor.variable}-${index}`}>
              <div className="factor-contenido">
                <span className="factor-variable">
                  {nombresVariables[factor.variable] ?? factor.variable}
                </span>

                <span className="factor-valor">
                  {obtenerEtiqueta(factor.variable, factor.valor)}
                </span>
              </div>

              <span
                className={
                  aumenta
                    ? "direccion aumenta"
                    : "direccion reduce"
                }
              >
                {aumenta ? "↑ Aumenta" : "↓ Reduce"}
              </span>
            </div>
          );
        })}
      </div>

      <p className="nota">
        Los factores describen cómo el modelo construyó esta predicción.
        No representan relaciones causales.
      </p>
    </section>
  );
}

function App() {
  const [formulario, setFormulario] = useState({
    EDA: "",
    ANTIGUEDAD: "",
    PAR_C_GRUPO: "",
    ESCOLARIDAD_GRUPO: "",
    INGRESO_GRUPO: "",
    DURACION_GRUPO: "",
    TAMANO_LOCALIDAD: "",
    ESTADO_CONYUGAL: "",
    BUSQUEDA_OTRO_EMPLEO: "",
    TIENE_JEFE: "",
    SEXO: "",
    ENTIDAD: "",
  });

  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  function manejarCambio(event) {
    const { name, value } = event.target;

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }));
  }

  async function manejarEnvio(event) {
    event.preventDefault();

    setCargando(true);
    setError(null);
    setResultado(null);

    const datos = {
      ...formulario,
      EDA: Number(formulario.EDA),
      ANTIGUEDAD:
        formulario.ANTIGUEDAD === ""
          ? null
          : Number(formulario.ANTIGUEDAD),
    };

    try {
            const respuesta = await fetch(
        `${API_URL}/predecir`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(datos),
        }
      );

      if (!respuesta.ok) {
        throw new Error(`Error HTTP: ${respuesta.status}`);
      }

      const resultadoApi = await respuesta.json();
      setResultado(resultadoApi);
    } catch (error) {
      console.error(error);

      setError(
        "No fue posible obtener la estimación. Intenta nuevamente."
      );
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="pagina">
      <header className="encabezado">
        <span className="proyecto">ENOE · México</span>

        <h1>Estimador de informalidad laboral</h1>

        <p>
          Explora la probabilidad estimada de empleo informal a partir
          de características sociodemográficas y laborales.
        </p>
      </header>

      <main
        className={`contenido ${
          resultado ? "contenido-con-resultado" : ""
        }`}
      >
        <section className="panel-formulario">
          <div className="titulo-seccion">
            <h2>Características de la persona</h2>
            <p>Completa los campos para generar una estimación.</p>
          </div>

          <form onSubmit={manejarEnvio}>
            <div className="grid-formulario">
              <div className="campo">
                <label htmlFor="EDA">Edad</label>

                <input
                  id="EDA"
                  name="EDA"
                  type="number"
                  min="15"
                  max="97"
                  placeholder="Ej. 35"
                  value={formulario.EDA}
                  onChange={manejarCambio}
                  required
                />
              </div>

              <div className="campo">
                <label htmlFor="ANTIGUEDAD">
                  Antigüedad en el empleo actual
                </label>

                <input
                  id="ANTIGUEDAD"
                  name="ANTIGUEDAD"
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="Años"
                  value={formulario.ANTIGUEDAD}
                  onChange={manejarCambio}
                />
              </div>

              <SelectCampo
                nombre="PAR_C_GRUPO"
                etiqueta="Relación con el jefe del hogar"
                valor={formulario.PAR_C_GRUPO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="ESCOLARIDAD_GRUPO"
                etiqueta="Escolaridad"
                valor={formulario.ESCOLARIDAD_GRUPO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="INGRESO_GRUPO"
                etiqueta="Ingreso laboral"
                valor={formulario.INGRESO_GRUPO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="DURACION_GRUPO"
                etiqueta="Duración de la jornada"
                valor={formulario.DURACION_GRUPO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="TAMANO_LOCALIDAD"
                etiqueta="Tamaño de localidad"
                valor={formulario.TAMANO_LOCALIDAD}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="ESTADO_CONYUGAL"
                etiqueta="Estado conyugal"
                valor={formulario.ESTADO_CONYUGAL}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="BUSQUEDA_OTRO_EMPLEO"
                etiqueta="Búsqueda de otro empleo"
                valor={formulario.BUSQUEDA_OTRO_EMPLEO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="TIENE_JEFE"
                etiqueta="¿Tiene jefe o superior?"
                valor={formulario.TIENE_JEFE}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="SEXO"
                etiqueta="Sexo"
                valor={formulario.SEXO}
                onChange={manejarCambio}
              />

              <SelectCampo
                nombre="ENTIDAD"
                etiqueta="Entidad federativa"
                valor={formulario.ENTIDAD}
                onChange={manejarCambio}
              />
            </div>

            <button
              className="boton-estimar"
              type="submit"
              disabled={cargando}
            >
              {cargando
                ? "Calculando..."
                : "Estimar probabilidad"}
            </button>

            {error && (
              <p className="mensaje-error" role="alert">
                {error}
              </p>
            )}
          </form>
        </section>

        {resultado && <Resultado resultado={resultado} />}
      </main>

      <footer>
        Modelo desarrollado con datos de la ENOE · 1.er trimestre de 2026
      </footer>
    </div>
  );
}

export default App;