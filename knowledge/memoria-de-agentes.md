# Memoria persistente de agentes: opciones evaluadas y cómo elegir

- Tipo: estrategia
- Revisada: 2026-11-16
- Estado: vigente (se actualiza con cada opción nueva)
- Relacionadas: `contexto-en-agentes`, `rag-recuperacion-hibrida`, `mcp-servidor-y-skills`; `backlog.json` o `referencia.json`: `relate`, `auto-ontology-mcp`, `okf-agent-memory`, `omnigraph`, `txtai`, `memorilla`, `context-mode`, `llm-wiki`

## En una línea
La memoria de un agente es lo que sobrevive entre sesiones y le evita releer y repetir. Todas las opciones evaluadas hasta ahora son jóvenes y ninguna tiene una prueba propia; con un modelo local chico importa más que la interfaz sea simple (pocas herramientas, ninguna consulta escrita a mano) que el motor que haya debajo.

## Qué sabemos (verificado, con fuente)
Opciones revisadas, con lo que cada una guarda y cómo se consulta (todas siguen en el backlog del repositorio, sin probar):

| Opción | Dónde vive la memoria | Cómo la consulta el agente | Observación verificada |
|---|---|---|---|
| `okf-agent-memory` | archivos markdown versionados en el repositorio | MCP con búsqueda BM25 embebida | distingue «escrito por agente» de «verificado por una persona» |
| `auto-ontology-mcp` | tablas tipadas en archivos SQLite locales | MCP; el modelo del cliente hace los pasos de lenguaje, SQL sobre los datos | repositorio de pocos días, no figura Databricks |
| `txtai` | base de embeddings (denso, disperso, grafo y SQL) | API web con MCP opcional | madura (2020), hay que escribir la configuración |
| `relate` | un grafo en un archivo `.rl`, en memoria con registro durable | lenguaje Cypher 25, por CLI, Python o servidor MCP opcional | proyecto de 12 días (versión 1.0.2): ver más abajo |
| `omnigraph` | grafo compartido entre agentes con ramas y fusiones | MCP | para varios agentes |
| `context-mode` | SQLite con búsqueda de texto | resume lo que guardó | licencia Elastic 2.0; cifras de ahorro del propio autor |
| `memorilla` | embeddings latentes entrenados para un Qwen3-8B | no accesible desde `llama-server` | investigación, no herramienta |

- **`relate`** (Neo4j Labs, API de GitHub 2026-11-16): 292 estrellas, Apache-2.0, creado el 2026-11-04. Es un grafo embebido en Rust que vive en un solo archivo y no necesita servidor. Según su propia documentación, **todo el grafo debe caber en memoria, hay un solo proceso dueño del almacén y un solo usuario o agente por proceso**, y la cantidad de bases es fija. Ofrece instalador firmado (clave pública fijada en el script, falla si la firma no coincide) y también la opción de leer el script antes de ejecutarlo.
- **Riesgo de proyecto que se abandona:** el motor de grafo embebido Kùzu, citado en un comentario del post, figura **archivado** en GitHub desde el 2025-10-10 (API de GitHub): una base de datos embebida joven puede quedarse sin mantenimiento.

## Lo que dicen pero no verificamos
- Un comentario de alguien que contribuye a un competidor (declarado) midió `relate` con un conjunto de pruebas tipo LDBC: casi todas las respuestas correctas pero consultas de triángulos de 1,3 s contra 2 a 3 ms de dos rivales, de 4 a 6 veces más memoria, y falla por memoria en conjuntos grandes con 64 GB. No es una medición independiente ni de un uso de agente; para una memoria de pocos miles de nodos probablemente no importa.
- «La memoria de un agente no necesita servidor»: plausible para un solo agente local; no resuelve varios agentes a la vez (un comentario del post lo plantea: ¿grafos separados o escrituras en serie?).

## Cómo elegir (criterios)
1. **¿Qué tiene que recordar?** Hechos con campos (fechas, totales, estados): tablas tipadas con SQL. Relaciones entre cosas (qué depende de qué): grafo. Notas y decisiones en prosa: archivos de texto con búsqueda por palabras clave más significado (`rag-recuperacion-hibrida`).
2. **Qué tan fácil le queda a un modelo chico:** que el agente tenga que **escribir Cypher o SQL** es una fuente de errores con un Qwen local. Preferir una memoria con herramientas simples (guardar, buscar, listar) y pocas.
3. **Quién es dueño del archivo:** un solo proceso. Si varios agentes escriben, serializar a través de un único servidor o separar un almacén por agente.
4. **Que se pueda leer sin la herramienta:** markdown o SQLite se abren con cualquier cosa; un formato propio depende de que el proyecto siga vivo (ver Kùzu).
5. **Medir con una tarea real:** una tarea larga cortada a la mitad, retomada en una sesión nueva con y sin memoria. Anotar tokens totales hasta terminar, si recordó lo decidido y si repitió trabajo.

## Cómo usarlo
Empezar por lo más simple que cubra la necesidad (markdown con búsqueda: `okf-agent-memory`, o SQLite con `auto-ontology-mcp`) y recién después un grafo. `relate` no se prueba hasta que un caso concreto necesite relaciones y pase de la etapa de proyecto de dos semanas.
