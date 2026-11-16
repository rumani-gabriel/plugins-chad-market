# Servidores MCP propios y skills servidas por el servidor (FastMCP)

- Tipo: criterio
- Revisada: 2026-11-16
- Estado: a revisar (la función de skills es experimental)
- Relacionadas: `contexto-en-agentes`; `blueprints/mcp-server/server.py`; `blueprints/mcp/mcp-local.json`; `apps/concat`

## En una línea
FastMCP es el framework estándar para escribir servidores MCP en Python, y la herramienta natural para construir en el laboratorio un servidor que falte. Servir la skill desde el mismo servidor que las herramientas evita copias viejas, pero es experimental y abre un canal por el que un servidor puede escribir instrucciones en tu agente.

## Qué sabemos (verificado, con fuente)
- **El proyecto** (`PrefectHQ/fastmcp`, API de GitHub y PyPI, 2026-11-16): 28.581 estrellas, licencia Apache-2.0, creado el 2024-11-30, versión 4.2.0 del 2026-11-13, Python 3.11 o superior, commits de hoy. Su README ofrece además un producto de pago, «FastMCP Gateway», del mismo equipo.
- **Servidor mínimo** (guía de inicio oficial): una función con `@mcp.tool` y `mcp.run()`; por defecto usa stdio, y con `transport="http"` queda en `http://localhost:8000/mcp`. El esquema y la descripción se generan de los tipos y del docstring. Plano listo en `blueprints/mcp-server/server.py`.
- **Skills desde el servidor** (documentación `servers/providers/skills`, marcada «experimental»): se sirven como recursos `skill://<nombre>/SKILL.md`, con un manifiesto por skill. El cliente (`SkillsClientExtension`) baja los archivos, verifica tamaños y SHA-256 (límites: 512 archivos y 16 MiB) y los escribe en una carpeta con `skill.to_directory(path, overwrite=True)`. La documentación **no** trae un comando de sincronización: el bucle se escribe en Python. Los ejemplos usan `~/.claude/skills`; no menciona las carpetas de Codex ni de OpenCode.
- **Versionado:** las skills cargadas son inmutables y las actualizaciones llegan al desplegar; la documentación no describe un campo de versión ni cómo fijar una.
- **Notas de la versión 4.2.0** (GitHub, 2026-11-13): la función es nueva y **cambia rápido**: la API de skills de la 4.1 queda deprecada y **se elimina en la 4.3**, y el nombre `Skill` pasó a ser la clase para crearlas (el modelo del protocolo se llama ahora `MCPSkill`). Las skills por el protocolo dependen de una extensión **experimental** (propuesta SEP-2640 de MCP) que, dice la propia versión, pocos clientes soportan todavía; cualquier cliente sí puede leer los archivos de una skill como recursos normales. Hay comandos nuevos como `fastmcp list --skills`. Moraleja práctica: fijar la versión exacta de FastMCP.
- **Proxy:** `create_proxy()` puede envolver otro servidor y `proxy.disable(names={...})` oculta herramientas. La documentación no muestra el caso de envolver un ejecutable por stdio con argumentos ni renombrar o acortar descripciones, y no menciona OpenCode.

## Lo que dicen pero no verificamos
- «Un solo despliegue actualiza el servidor y la skill en todos los clientes»: depende de que cada cliente ejecute la sincronización; un comentario del post pregunta si FastMCP avisa de copias viejas y la documentación no lo cubre.
- Dos preguntas de un segundo post sobre lo mismo siguen sin respuesta en la documentación leída: si hay **reversión** cuando se publica una skill mala (no está descrita; las skills cargadas son inmutables y se actualizan al desplegar) y si el cliente trae las skills nuevas **al conectar** o solo al ejecutar la sincronización (la sincronización es código del cliente).
- Comentarios de usuarios (sin verificar): al cambiar la descripción de una herramienta hay que desconectar y reconectar el servidor en el cliente para que el modelo vea el cambio.

## Riesgos
- **Las skills son instrucciones para el agente.** Un cliente que las baja y las sobrescribe solo (`overwrite=True`) confía en el servidor: si el servidor se compromete, escribe instrucciones en la carpeta de skills de todos. El hash comprueba que los archivos coinciden con lo que el servidor declara, no que el servidor sea de fiar. Usarlo solo con servidores propios, locales o internos, y con una revisión humana de lo que cambia.
- Un servidor MCP con muchas herramientas gasta contexto: es el caso de Concat (45 herramientas). Un servidor intermedio de FastMCP que oculte las que no se usan (`disable`) podría adelgazar esa lista; no está verificado que funcione envolviendo un ejecutable por stdio.

## Cómo usarlo
1. **Para construir una pieza que falte:** partir de `blueprints/mcp-server/server.py`, fijar `fastmcp==4.2.0` en un entorno virtual propio y conectarlo con `blueprints/mcp/mcp-local.json`. Pocas herramientas, descripciones cortas.
2. **No adoptar todavía** las skills servidas por MCP: esperar a que dejen de ser experimentales y a que documenten el versionado.
3. **Probar el adelgazado:** crear un proxy sobre un servidor con muchas herramientas, ocultar las innecesarias y medir cuántos tokens menos ocupa la lista de herramientas.
