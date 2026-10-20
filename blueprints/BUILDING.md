# Armar lo que falta

Para cuando necesitás una herramienta y el catálogo no la tiene. Seguí estos pasos en orden.

## 1. Buscá antes de armar
Leé `catalog.json`: cada entrada tiene `tags` por capacidad (por ejemplo `search`, `reverse-engineering`, `rag`, `memory`). Si algo ya cubre la necesidad, usalo.

## 2. Elegí el tipo de pieza

| Necesito... | Tipo | Blueprint | Va en (dentro de `.opencode/`) |
|---|---|---|---|
| Un procedimiento o criterio que el modelo sigue cuando corresponde | skill | `blueprints/skill/SKILL.md` | `skills/<nombre>/SKILL.md` |
| Un atajo que recibe argumentos | command | `blueprints/command/command.md` | `commands/<nombre>.md` |
| Un rol con permisos acotados | subagente | `blueprints/subagent/agent.md` | `agents/<nombre>.md` |
| Ejecutar código determinístico con argumentos tipados | custom tool | `blueprints/custom-tool/tool.ts` | `tools/<nombre>.ts` |
| Una herramienta externa que habla MCP | mcp | `blueprints/mcp/mcp-local.json` o `mcp-remote.json` | clave `mcp` de `opencode.json` |
| Una herramienta externa sin MCP (CLI, librería, servicio) | app | copiá una receta de `apps/*/recipe.json` | no se copia: se ejecuta paso a paso |

Para instrucciones de proyecto (el `AGENTS.md` de un repo) usá la skill `harness-creator` de este market.

## 3. Copiá el blueprint y reemplazá `NOMBRE`
- El `name` de una skill debe coincidir con su carpeta y cumplir `^[a-z0-9]+(-[a-z0-9]+)*$` (máximo 64).
- OpenCode **descarta en silencio** un comando cuyo frontmatter no es YAML válido. Si agregás claves con `[...]` o `: ` en el valor, ponelas entre comillas.
- Guardá los archivos en **UTF-8 sin BOM**. Un BOM antes del `---` inicial hace que OpenCode ignore la skill sin avisar (probado). En Windows PowerShell 5.1, `Set-Content -Encoding UTF8` y `Out-File` agregan BOM; usá `[System.IO.File]::WriteAllText(ruta, texto, (New-Object System.Text.UTF8Encoding($false)))` o una herramienta de edición de archivos.
- No pongas credenciales en un blueprint MCP: usá `{env:VARIABLE}`. Fijá siempre una versión (`paquete@1.2.3`), nunca `latest`.

## 4. Probalo
- skill: `opencode debug skill`
- comando: `opencode debug config` (sección `command`)
- subagente: `opencode debug agent <nombre>`
- mcp: `opencode mcp list` y `opencode debug config`
- custom tool: no hay comando de listado documentado; pedile al modelo que la use y verificá el resultado.

## 5. Si vale la pena compartirlo
1. Carpeta `plugins/<nombre>/` (o `apps/<nombre>/recipe.json`) con el mismo layout que los existentes.
2. Entrada en `catalog.json` con `kind`, `summary`, `tags`, `path` y un `verified` honesto: `executed` (lo corriste de punta a punta), `discovery` (OpenCode lo descubre pero no corriste su lógica) o `docs` (armado desde la documentación, sin ejecutar).
3. Probá `python install.py <nombre> --project <dir temporal>` y `opencode debug skill`.
4. Sin secretos, sin datos de ninguna organización y declarando con honestidad si necesita red o API keys.
