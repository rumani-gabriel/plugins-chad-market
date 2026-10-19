# graph-explorer

Convierte un repo o carpeta en un **grafo de conocimiento consultable**: entendés la arquitectura, las dependencias y "qué conecta con qué" sin leer archivo por archivo. Usa el motor open-source Graphify en **modo local endurecido**.

## Uso
```
/graph-build [ruta]        # arma o actualiza el grafo (por defecto, el directorio actual)
/graph-query <pregunta>    # consulta el grafo ya construido
```
Las salidas quedan en `graphify-out/`: `graph.json`, `graph.html` (interactivo, con un tema visual propio aplicado por `tools/theme/apply_theme.py`, idempotente) y `GRAPH_REPORT.md`. La consulta admite lenguaje natural, camino entre dos módulos (`path`) y explicación de un nodo (`explain`).

## Modo local endurecido
La extracción de código es local (tree-sitter + NetworkX, ~40 lenguajes): sin red, sin API key.

| Riesgo del motor original | Aquí |
|---|---|
| PDF/imágenes enviados a un LLM externo | Eliminado: los lee el propio asistente en la sesión |
| Log de queries en `~/.cache` | Apagado (`GRAPHIFY_QUERY_LOG_DISABLE=1`) |
| git-hooks post-commit | No se instalan; el grafo se arma a pedido |
| MCP server / Neo4j / FalkorDB | Flags prohibidos; extras no instalados |
| `cluster-only` detecta un backend LLM por variables de entorno | Siempre `--no-label` (comunidades `Community N`) |

## Requisitos
- Python 3.10+ y [`uv`](https://docs.astral.sh/uv/) (recomendado) o `pip`.
- La primera ejecución instala el motor `graphifyy==0.9.9` (necesita red solo esa vez). Con `uv` queda como herramienta persistente.
- Los wrappers `bin/run-*` son `sh` POSIX; en Windows nativo usá los `.cmd`.

## Motor
Paquete [`graphifyy`](https://pypi.org/project/graphifyy/) **0.9.9**, licencia MIT (verificado en PyPI), pineado a propósito. Repo original: `github.com/safishamsi/graphify`, que hoy redirige a `Graphify-Labs/graphify`; el código más nuevo de ese repo declara Apache-2.0, así que revisá la licencia antes de subir de versión.
