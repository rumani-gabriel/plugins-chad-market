@echo off
REM Resuelve el interprete Python disponible. Este plugin no tiene dependencias
REM de terceros (solo stdlib) -- no hace falta pip install para nada.
where python >nul 2>nul
if %errorlevel%==0 (
  python %*
) else (
  python3 %*
)
