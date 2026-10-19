@echo off
REM Resuelve el interprete Python disponible y ejecuta con sus dependencias:
REM   1) uv (si esta disponible): instala/cachea las deps de requirements.txt
REM      al vuelo -- no hace falta pip install manual.
REM   2) python / python3 (fallback): asume que ya corriste
REM      "pip install -r requirements.txt".
where uv >nul 2>nul
if %errorlevel%==0 (
  uv run --with-requirements "%~dp0..\requirements.txt" python %*
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python %*
  ) else (
    python3 %*
  )
)
