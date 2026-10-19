---
description: Construye (o actualiza) el grafo de conocimiento del repo en modo local seguro. Uso: /graph-build [ruta]
---

Activá la skill `graph-explorer`. Construí el grafo de **$ARGUMENTS** (si no se pasa ruta, usá `.`).

```bash
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" "${ARGUMENTS:-.}"
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" cluster-only "${ARGUMENTS:-.}" --no-label
"${CLAUDE_PLUGIN_ROOT}/bin/run-python" "${CLAUDE_PLUGIN_ROOT}/tools/theme/apply_theme.py" "${ARGUMENTS:-.}/graphify-out/graph.html"
```

El primer paso extrae el código (`graph.json`); el segundo genera `graph.html` y `GRAPH_REPORT.md`. **Siempre pasá `--no-label`**: sin eso, `cluster-only` puede auto-detectar un backend LLM externo (vía `GOOGLE_API_KEY` u otra env var que exista en la máquina) para nombrar comunidades — `--no-label` lo evita y deja placeholders `Community N`, coherente con el modo local endurecido del plugin. El tercer paso le da a `graph.html` la estética "neuronal" del plugin (glow en nodos/aristas + animación de pulso al seleccionar un nodo) sin tocar el motor vendorizado — es idempotente (no rompe si `graph.html` ya la tiene) y falla en silencio sin bloquear el build si el archivo no matchea el formato esperado.

- Modo **local**: la extracción de código no hace red ni usa API key.
- **No** uses `--mcp`, `--neo4j`, `--falkordb` ni backends LLM externos.
- Si el repo tiene PDFs/imágenes/docs relevantes, leelos **vos** (no un LLM externo) y sumalos al reporte.

Al terminar, resumí el `GRAPH_REPORT.md` (comunidades/nodos clave) sin volcar el JSON. Las salidas quedan en `graphify-out/`.
