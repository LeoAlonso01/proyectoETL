@echo off
setlocal

REM Create venv if not exists
if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate

pip install -r requirements.txt

REM Copy .env.example to .env (first time)
if not exist .env (
  copy .env.example .env
  echo Created .env from .env.example - please edit credentials before running.
  exit /b 0
)

python -m app.main --all
endlocal
