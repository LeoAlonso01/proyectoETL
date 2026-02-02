@echo off

REM Activar entorno virtual
call .\pub-may\Scripts\activate

REM Ejecutar scripts de python
call python .\Creacion_De_Archivo_CSV.py
call python .\Transformacion.py
call python .\Final_Version_Publica.py

REM Desactivar entorno virtual
call deactivate
