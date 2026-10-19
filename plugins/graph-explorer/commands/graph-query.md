---
description: Consulta el grafo de conocimiento ya construido (arquitectura, relaciones, caminos). Uso: /graph-query <pregunta>
---

Activá la skill `graph-explorer`. Respondé la consulta sobre el código usando el grafo: **$ARGUMENTS**

Si no existe `graphify-out/graph.json`, avisá que primero hay que correr `/graph-build`.

```bash
GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" query "$ARGUMENTS"
# o, según lo que se pida:
# GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" path "ComponenteA" "ComponenteB"
# GRAPHIFY_QUERY_LOG_DISABLE=1 "${CLAUDE_PLUGIN_ROOT}/bin/run-graphify" explain "NombreDeNodo"
```

Todo local, sin red. Presentá la respuesta en lenguaje claro (qué conecta con qué, el camino, el rol del nodo), citando los componentes del grafo.
