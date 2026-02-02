import datetime
import logging
import os
from pathlib import Path

import pandas as pd

from app.config import Settings
from app.extract.mongo import build_mongo_uri, load_pipeline, run_aggregation
from app.transform.flatten import flatten_dict

log = logging.getLogger("extract.extract_to_csv")


def dated_folder(base_output_dir: str) -> str:
    fecha_actual = datetime.datetime.now()
    nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
    ruta = os.path.join(base_output_dir, nombre_carpeta)
    Path(ruta).mkdir(parents=True, exist_ok=True)
    return ruta


def extract_public_data_to_csv(settings: Settings, csv_name: str = "archivo1.csv") -> str:
    settings.ensure_dirs()

    uri = build_mongo_uri(
        host=settings.mongo_host,
        port=settings.mongo_port,
        db=settings.mongo_db,
        user=settings.mongo_user,
        password=settings.mongo_password,
    )

    pipeline = load_pipeline(settings.pipeline_json)
    rows = run_aggregation(uri, settings.mongo_db, settings.mongo_collection, pipeline)

    df = pd.DataFrame(rows)
    if "declaracion" in df.columns:
        df_flat = df["declaracion"].apply(lambda x: flatten_dict(x)).apply(pd.Series)
        df = pd.concat([df.drop(["declaracion"], axis=1), df_flat], axis=1)

    out_dir = dated_folder(settings.output_dir)
    out_path = os.path.join(out_dir, csv_name)
    df.to_csv(out_path, index=False)

    log.info("CSV exported to: %s (rows=%s, cols=%s)", out_path, len(df), len(df.columns))
    return out_path
