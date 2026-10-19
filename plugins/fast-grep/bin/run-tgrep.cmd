@echo off
REM Resuelve (descargando y verificando por sha256 si hace falta) el binario
REM de tgrep y lo ejecuta con los argumentos recibidos. Ver tools/ensure_tgrep.py.
"%~dp0run-python.cmd" "%~dp0..\tools\ensure_tgrep.py" %*
