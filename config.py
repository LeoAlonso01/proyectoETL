import os
from dataclasses import dataclass
from pathlib import Path

try:
    # opcional (si instalas python-dotenv). Si no, no pasa nada.
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


@dataclass(frozen=True)
class Settings:
    mongo_host: str = os.getenv("MONGO_HOST", "127.0.0.1")
    mongo_port: int = int(os.getenv("MONGO_PORT", "27017"))
    mongo_db: str = os.getenv("MONGO_DB", "declaranet")
    mongo_user: str = os.getenv("MONGO_USER", "")
    mongo_password: str = os.getenv("MONGO_PASSWORD", "")
    mongo_collection: str = os.getenv("MONGO_COLLECTION", "datosPublicos100")

    pipeline_json: str = os.getenv("PIPELINE_JSON", "./pipeline/pipeline.json")
    output_dir: str = os.getenv("OUTPUT_DIR", "./output")
    template_docx: str = os.getenv("TEMPLATE_DOCX", "./templates/declaracion_publica.docx")

    def ensure_dirs(self) -> None:
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
