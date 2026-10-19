@echo off
REM Resuelve y ejecuta el CLI de graphify (graphifyy==0.9.9), priorizando una
REM instalacion PERSISTENTE via "uv tool" (no se re-resuelve el entorno en
REM cada llamada, a diferencia de "uv run --with-requirements").
set PIN=graphifyy==0.9.9
where uv >nul 2>nul
if %errorlevel%==0 (
  uv tool list 2>nul | findstr /x "graphifyy v0.9.9" >nul || uv tool install --quiet "%PIN%" >nul 2>nul
  uv tool run --from "%PIN%" graphify %*
) else (
  "%~dp0run-python.cmd" -c "import graphify" 2>nul || "%~dp0run-python.cmd" -m pip install -q -r "%~dp0..\requirements.txt"
  "%~dp0run-python.cmd" -m graphify %*
)
