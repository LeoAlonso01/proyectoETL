# Declaranet Public ETL Pipeline (Python)

Real-world ETL pipeline that extracts nested declaration records from MongoDB,
normalizes and applies privacy rules, and generates public-ready outputs.

## What it does
1) **Extract** (MongoDB Aggregation Pipeline) → raw CSV  
2) **Transform** (data normalization + privacy rules) → public CSV  
3) **Load** (document automation) → DOCX + PDF outputs

## Why it matters
Organizations often store nested JSON documents that are not ready for reporting.
This project automates:
- Flattening nested data
- Enforcing business rules (YES/NO masking, derived fields)
- Exporting consistent, auditable outputs
- Automated document generation from templates

## Tech Stack
- Python, Pandas, PyMongo
- MongoDB Aggregation Pipeline
- python-docx, docx2pdf

> Note: `docx2pdf` usually requires Windows + Microsoft Word installed.

## Highlights
- Processes nested MongoDB documents using an Aggregation Pipeline
- Flattens JSON structures into tabular datasets
- Applies business rules for public disclosure (YES/NO masking)
- Generates public-ready DOCX and PDF reports from templates
- Output is organized by execution date for auditing


## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your Mongo credentials
python -m app.main --all

## Setup (Windows)

### PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m app.main --all

### CMD
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.main --all
