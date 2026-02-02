import datetime
import logging
import os
from pathlib import Path
import json

import numpy as np
import pandas as pd

log = logging.getLogger("transform.public_transform")

NIVEL_ACADEMICO_ORDEN = {
    "PRIMARIA": 1,
    "SECUNDARIA": 2,
    "BACHILLERATO": 3,
    "LICENCIATURA": 4,
    "ESPECIALIDAD": 5,
    "MAESTRIA": 6,
    "DOCTORADO": 7,
}


def dated_folder(base_output_dir: str) -> str:
    fecha_actual = datetime.datetime.now()
    nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
    ruta = os.path.join(base_output_dir, nombre_carpeta)
    Path(ruta).mkdir(parents=True, exist_ok=True)
    return ruta


def convert_to_dict(val):
    if isinstance(val, str):
        val = val.replace('"', "$")
        val = val.replace("'", '"')
        val = val.replace("$", "'")
        val = val.replace("None", "null")
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return np.nan
    return val


def get_persona_type(x):
    if isinstance(x, list):
        for dic in x:
            transmisores = dic.get("transmisores", [])
            if any(item.get("tipoPersona") == "PERSONA_MORAL" for item in transmisores):
                return "PERSONA_MORAL"
        return "PERSONA_FISICA" if any(dic.get("transmisores") for dic in x) else np.nan
    return np.nan


def get_domicilio_extranjero(x):
    if isinstance(x, list):
        for dic in x:
            domicilio = dic.get("domicilio", {}).get("domicilioExtranjero")
            if domicilio is not None:
                return "SI"
        return "NO"
    return np.nan


def get_area_adscripcion(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get("areaAdscripcion", np.nan)
    return np.nan


def get_empleo_cargo_comision(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get("empleoCargoComision", np.nan)
    return np.nan


def get_fecha_encargo(x):
    if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
        return x[0].get("fechaEncargo", np.nan)
    return np.nan


def get_max_nivel_academico(x):
    if isinstance(x, list):
        max_nivel = 0
        max_nivel_nombre = np.nan
        for dic in x:
            nivel = dic.get("nivel", {}).get("valor")
            if nivel and nivel in NIVEL_ACADEMICO_ORDEN and NIVEL_ACADEMICO_ORDEN[nivel] > max_nivel:
                max_nivel = NIVEL_ACADEMICO_ORDEN[nivel]
                max_nivel_nombre = nivel
        return max_nivel_nombre
    return np.nan


def convertir_a_si_no(valor):
    try:
        return "SI" if float(valor) != 0 else "NO"
    except Exception:
        return "NO"


def transform_csv_to_public(csv_in_path: str, output_base_dir: str, csv_out_name: str = "declaraciones_publicas.csv") -> str:
    df = pd.read_csv(csv_in_path)

    # Convert nested stringified JSON columns
    if "declaracion_bienesInmuebles_bienesInmuebles" in df.columns:
        df["declaracion_bienesInmuebles_bienesInmuebles"] = df["declaracion_bienesInmuebles_bienesInmuebles"].apply(convert_to_dict)
        df["moral_o_fisica"] = df["declaracion_bienesInmuebles_bienesInmuebles"].apply(get_persona_type)
        df["domicilioExtranjero"] = df["declaracion_bienesInmuebles_bienesInmuebles"].apply(get_domicilio_extranjero)
        df.drop(columns=["declaracion_bienesInmuebles_bienesInmuebles"], inplace=True)

    if "declaracion_datosEmpleoCargoComision_empleoCargoComision" in df.columns:
        df["declaracion_datosEmpleoCargoComision_empleoCargoComision"] = df["declaracion_datosEmpleoCargoComision_empleoCargoComision"].apply(convert_to_dict)
        df["areaAdscripcion"] = df["declaracion_datosEmpleoCargoComision_empleoCargoComision"].apply(get_area_adscripcion)
        df["empleoCargoComision"] = df["declaracion_datosEmpleoCargoComision_empleoCargoComision"].apply(get_empleo_cargo_comision)
        df["fechaEncargo"] = df["declaracion_datosEmpleoCargoComision_empleoCargoComision"].apply(get_fecha_encargo)
        df.drop(columns=["declaracion_datosEmpleoCargoComision_empleoCargoComision"], inplace=True)

    if "declaracion_datosCurricularesDeclarante_escolaridad" in df.columns:
        df["declaracion_datosCurricularesDeclarante_escolaridad"] = df["declaracion_datosCurricularesDeclarante_escolaridad"].apply(convert_to_dict)
        df["max_nivel_academico"] = df["declaracion_datosCurricularesDeclarante_escolaridad"].apply(get_max_nivel_academico)
        df.drop(columns=["declaracion_datosCurricularesDeclarante_escolaridad"], inplace=True)

    # Privacy conversions
    if "declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto" in df.columns:
        df["declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto"] = df[
            "declaracion_ingresos_ingresoNetoParejaDependiente_remuneracion_monto"
        ].apply(convertir_a_si_no)

    if "declaracion_ingresos_otrosIngresosTotal_monto" in df.columns:
        df["declaracion_ingresos_otrosIngresosTotal_monto"] = df["declaracion_ingresos_otrosIngresosTotal_monto"].apply(convertir_a_si_no)

    out_dir = dated_folder(output_base_dir)
    out_path = os.path.join(out_dir, csv_out_name)
    df.to_csv(out_path, index=False)

    log.info("Public CSV exported to: %s (rows=%s)", out_path, len(df))
    return out_path
