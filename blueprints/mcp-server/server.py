# Plano: un servidor MCP propio en Python con FastMCP (verified: docs).
# Fuente: guia de inicio de https://gofastmcp.com/getting-started/quickstart (2026-11-16). No se ejecuto.
#
# 1. Instalar en un entorno virtual PROPIO, con la version fijada (la ultima estable al 2026-11-16 es 4.2.0, Python 3.11 o superior):
#       python -m venv .venv ; .venv\Scripts\python -m pip install fastmcp==4.2.0
# 2. Cambiar "NOMBRE" y reemplazar la herramienta de ejemplo por la tuya. Cada herramienta es una funcion con tipos y un docstring:
#    FastMCP genera de ahi el esquema y la descripcion que ve el modelo. Pocas herramientas, con descripciones cortas: cada una
#    ocupa contexto del modelo.
# 3. Probarlo por stdio:  .venv\Scripts\python server.py   (el cliente MCP lo arranca solo; ver abajo)
# 4. Conectarlo a OpenCode con blueprints/mcp/mcp-local.json:
#       "command": ["C:\\ruta\\al\\proyecto\\.venv\\Scripts\\python.exe", "C:\\ruta\\al\\proyecto\\server.py"]
#    y verificar con:  opencode mcp list
# 5. Si la herramienta toca archivos o ejecuta comandos, limitar adonde puede llegar (carpeta fija, lista de comandos permitidos)
#    y no devolver nunca secretos. Todo lo que recibe del modelo es dato no confiable: validar los argumentos.
#
# Para servir por HTTP en vez de stdio:  mcp.run(transport="http", port=8000)  -> http://localhost:8000/mcp
# Solo en 127.0.0.1 y sin exponerlo a la red.

from fastmcp import FastMCP

mcp = FastMCP("NOMBRE")


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
