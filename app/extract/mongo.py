import json
import logging
from pathlib import Path
from pymongo import MongoClient

log = logging.getLogger("extract.mongo")


def build_mongo_uri(host: str, port: int, db: str, user: str, password: str) -> str:
    # Si no hay user/pass, conecta sin auth
    if user and password:
        return f"mongodb://{user}:{password}@{host}:{port}/{db}"
    return f"mongodb://{host}:{port}/{db}"


def load_pipeline(pipeline_path: str):
    data = Path(pipeline_path).read_text(encoding="utf-8")
    return json.loads(data)


def run_aggregation(uri: str, db_name: str, collection_name: str, pipeline: list):
    client = MongoClient(uri)
    db = client[db_name]
    col = db[collection_name]
    log.info("Running aggregation on %s.%s ...", db_name, collection_name)
    cursor = col.aggregate(pipeline, allowDiskUse=True)
    return list(cursor)
