import argparse
import logging
from pathlib import Path

from app.config import Settings
from app.logging_config import setup_logging
from app.extract.extract_to_csv import extract_public_data_to_csv
from app.transform.public_transform import transform_csv_to_public
from app.load.generate_docs import generate_docs_from_csv


def parse_args():
    p = argparse.ArgumentParser(description="Declaranet Public ETL Pipeline")

    # Steps
    p.add_argument("--extract", action="store_true", help="Run extract step (Mongo -> raw CSV)")
    p.add_argument("--transform", action="store_true", help="Run transform step (raw CSV -> public CSV)")
    p.add_argument("--docs", action="store_true", help="Generate DOCX/PDF from public CSV)")
    p.add_argument("--all", action="store_true", help="Run extract + transform + docs")

    # Inputs/outputs
    p.add_argument("--csv-in", type=str, default=None,
                   help="Path to raw CSV input (skips extract). Example: output/01_02_2026/archivo1.csv")
    p.add_argument("--csv-public", type=str, default=None,
                   help="Path to public CSV input (skips transform). Example: output/01_02_2026/declaraciones_publicas.csv")

    # Optional output dir override
    p.add_argument("--output-dir", type=str, default=None,
                   help="Override OUTPUT_DIR from env. Example: ./output")

    return p.parse_args()


def must_exist(path_str: str, label: str) -> str:
    p = Path(path_str)
    if not p.exists() or not p.is_file():
        raise SystemExit(f"{label} not found: {path_str}")
    return str(p)


def main():
    args = parse_args()
    setup_logging(logging.INFO)

    s = Settings()
    if args.output_dir:
        # override runtime output dir without changing env
        object.__setattr__(s, "output_dir", args.output_dir)  # dataclass frozen workaround
    s.ensure_dirs()

    # If no step flags were provided, default to --all
    no_flags = not any([args.extract, args.transform, args.docs, args.all])
    run_all = args.all or no_flags

    raw_csv = None
    public_csv = None

    # ----------------
    # EXTRACT
    # ----------------
    if run_all or args.extract:
        if args.csv_in:
            raw_csv = must_exist(args.csv_in, "Raw CSV (--csv-in)")
            logging.getLogger("main").info("Skipping extract, using --csv-in: %s", raw_csv)
        else:
            raw_csv = extract_public_data_to_csv(s, csv_name="archivo1.csv")
    else:
        if args.csv_in:
            raw_csv = must_exist(args.csv_in, "Raw CSV (--csv-in)")

    # ----------------
    # TRANSFORM
    # ----------------
    if run_all or args.transform:
        if args.csv_public:
            public_csv = must_exist(args.csv_public, "Public CSV (--csv-public)")
            logging.getLogger("main").info("Skipping transform, using --csv-public: %s", public_csv)
        else:
            if not raw_csv:
                raise SystemExit("Transform requires raw CSV. Use --extract or provide --csv-in.")
            public_csv = transform_csv_to_public(
                csv_in_path=raw_csv,
                output_base_dir=s.output_dir,
                csv_out_name="declaraciones_publicas.csv",
            )
    else:
        if args.csv_public:
            public_csv = must_exist(args.csv_public, "Public CSV (--csv-public)")

    # ----------------
    # DOCS
    # ----------------
    if run_all or args.docs:
        if not public_csv:
            raise SystemExit("Docs require public CSV. Use --transform or provide --csv-public.")
        generate_docs_from_csv(public_csv, s.template_docx, s.output_dir)


if __name__ == "__main__":
    main()
