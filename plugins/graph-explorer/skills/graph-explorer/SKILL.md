---
name: graph-explorer
description: Convierte un repo/carpeta en un grafo de conocimiento consultable y responde preguntas sobre la arquitectura y las relaciones del código (qué conecta con qué, qué llama a qué, caminos entre componentes). Activá esta skill cuando el usuario quiera entender un codebase grande, mapear dependencias/arquitectura, o consultar un grafo ya construido en graphify-out/. Corre en modo LOCAL endurecido — sin red, sin API key, sin telemetría.
---

# Graph Explorer (grafo de conocimiento, local y seguro)

Usa el motor open-source **Graphify** (paquete pip `graphifyy`, MIT) para construir un grafo del repo y consultarlo. Postura de seguridad **innegociable** en este plugin: **todo local, nada de red ni backends LLM externos.**

## Reglas de seguridad (siempre)

En **todos** los comandos, exportá estas variables para endurecer el motor:

```bash
export GRAPHIFY_QUERY_LOG_DISABLE=1     # no guardar el log de queries en ~/.cache
```

- **Nunca** configures ni pases `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` ni ningún backend LLM externo.
- **Nunca** uses los flags `--mcp`, `--neo4j`, `--neo4j-push`, `--falkordb`, `--falkordb-push` (red / daemons).
- **No** instales git-hooks de graphify. El grafo se arma solo cuando el usuario lo pide.
- El grafo y sus salidas quedan en `graphify-out/` del proyecto (local).

## 1. Asegurar el motor

`bin/run-graphify` resuelve esto solo: si hay `uv`, instala `graphifyy==0.9.9` como **uv tool persistente** la primera vez (no hace falta reinstalar por proyecto) y reusa esa instalación en cada llamada; sin `uv`, cae a `pip install -r requirements.txt` + `python -m graphify` (comportamiento previo). No hace falta ningún paso manual antes de los comandos de abajo.

## 2. Construir el grafo del código (100% local, sin LLM)

La extracción de **código** es totalmente local (tree-sitter + NetworkX): no llama a ninguna API. Son **dos pasos** (el motor separa extracción de clustering/reporte):

```bash
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" "<ruta>"                       # extrae: graphify-out/graph.json
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" cluster-only "<ruta>" --no-label   # genera graph.html y GRAPH_REPORT.md
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" update "<ruta>"                # incremental: solo archivos nuevos/cambiados (correr cluster-only después si querés el reporte actualizado)
```

**Siempre pasá `--no-label`** en `cluster-only`: sin eso, el motor puede auto-detectar un backend LLM externo (por una env var como `GOOGLE_API_KEY` que exista en la máquina) para nombrar comunidades — rompería la postura "todo local". Con `--no-label` quedan como placeholders `Community N`, que alcanza para navegar el grafo.

Después de `cluster-only`, aplicá el tema visual del plugin sobre el `graph.html` recién generado (no toca el motor vendorizado, solo post-procesa el HTML de salida):

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/run-python" "${CLAUDE_PLUGIN_ROOT}/tools/theme/apply_theme.py" "<ruta>/graphify-out/graph.html"
```

Presentá un resumen limpio del reporte; no vuelques el JSON crudo.

## 3. Consultar el grafo

```bash
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" query "<pregunta>"     # contexto amplio (BFS)
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" path "ModuloA" "ModuloB"   # camino más corto entre dos componentes
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" explain "NombreDeNodo"      # explicación de un nodo
```

Si ya existe `graphify-out/graph.json` y el usuario hace una pregunta sobre el código, andá directo a `query` (no reconstruyas).

## Preferí el grafo sobre grep cuando ya existe

Si `graphify-out/graph.json` ya está construido, para preguntas de arquitectura o dependencias usá `/graph-query` (o `query`/`path`/`explain`) antes de recurrir a `grep`/`rg`: en proyectos grandes suele ser más preciso y más barato en tokens. Si es una búsqueda de un string literal puntual que el grafo no cubre, usá grep normalmente.

## 4. PDF / imágenes / documentos — los leés VOS, no un LLM externo

El motor original mandaría PDFs/imágenes a un backend LLM externo. **Acá no.** Cuando el material no sea código:

1. **Leelo vos mismo** con la herramienta de lectura del asistente (los PDFs por páginas, las imágenes visualmente).
2. Extraé los conceptos/relaciones y sumalos al análisis o al `GRAPH_REPORT.md` como sección aparte.
3. Así el contenido **nunca sale a un tercero**: se procesa dentro de tu sesión ya autenticada.

## Qué NO hace

- No sube nada a la nube, no manda telemetría, no abre daemons.
- No edita el código del repo: solo lo lee y genera el grafo en `graphify-out/`.
