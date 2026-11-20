# Lista de 20 repositorios «para sacarle más a Claude Code»: triaje

- Tipo: referencia
- Revisada: 2026-11-20
- Estado: vigente
- Relacionadas: `contexto-en-agentes`, `memoria-de-agentes`, `sandbox-para-agentes`, `rag-recuperacion-hibrida`; `backlog.json`: `claude-mem`, `serena`, `markitdown`, `superpowers`, `rtk`; `catalog.json`: `graph-explorer`

## En una línea
Un post de LinkedIn lista 20 repositorios populares alrededor de Claude Code. Verifiqué en GitHub que los 17 que no teníamos existen y sus datos (estrellas, licencia, última actividad), y los ordené según el lab (agentes locales: OpenCode o Pi sobre Qwen, Windows, RTX 3060 de 12 GB) y según la prioridad de gestionar el contexto. Tres pasaron al backlog; el resto queda aquí como mapa para no volver a evaluarlos desde cero.

## Qué sabemos (verificado, con fuente)
Datos de la API de GitHub el 2026-11-20 (estrellas / licencia / último push). La descripción de una línea es la del repositorio. **Lo que no leí en profundidad está marcado «solo ficha»**: para esos solo comprobé que existen, la licencia y que están activos.

| Repositorio | Estrellas | Licencia | Qué es (según el repo) | Veredicto para el lab |
|---|---:|---|---|---|
| `upstash/context7` | 65 mil | MIT | Documentación al día de bibliotecas para agentes, por servidor MCP | **Referencia.** El servidor público es un servicio en la nube (`mcp.context7.com`); el backend, el rastreador y el motor de análisis son privados. Cada consulta sale a un tercero. Se puede correr el servidor MCP local, pero sin el backend no es lo mismo |
| `obra/superpowers` | 322 mil | MIT | Metodología de desarrollo con skills | **Ya evaluado** (backlog: costo de contexto a medir) |
| `rtk-ai/rtk` | 84 mil | Apache-2.0 / BUSL-1.1 | Recorta la salida de comandos | **Ya evaluado** (backlog; un benchmark independiente no halló ahorro asegurado) |
| `BloopAI/vibe-kanban` | 29 mil | Apache-2.0 | Tablero kanban donde cada tarjeta es un agente | **No.** Solo ficha. Más agentes en paralelo es más tokens, lo contrario de lo que se busca |
| `oraios/serena` | 32 mil | GPL-3.0-or-later (la parte SolidLSP, MIT) | Herramientas MCP de búsqueda y edición semántica de código por servidor de lenguaje (LSP, más de 40 lenguajes) | **Candidato** (backlog). Funciona con OpenCode |
| `slopus/happy` | 25 mil | MIT | Controlar Claude, Codex y otros desde el celular | **No.** Solo ficha. Controlar un agente desde el teléfono implica un servicio intermedio que no revisé |
| `github/spec-kit` | 151 mil | MIT | Desarrollo guiado por especificación | **Referencia.** Solo ficha. Mismo espacio que otras metodologías ya evaluadas |
| `thedotmack/claude-mem` | 119 mil | Apache-2.0 | Memoria persistente entre sesiones: captura lo que hace el agente, lo comprime con IA y lo reinyecta | **Candidato** (backlog). Declara soporte para OpenCode y Pi |
| `pbakaus/impeccable` | 114 mil | Apache-2.0 | Un skill de gusto de diseño para interfaces | **No.** Solo ficha. Es de diseño visual, no del lab |
| `dagger/container-use` | 4 mil | Apache-2.0 | Un contenedor y una rama de git por agente | **Referencia.** Su README se declara «experimental» y «en desarrollo temprano». Necesita Docker. Para aislar un agente en el lab ya está `apps/opensandbox` |
| `ryoppippi/ccusage` | 20 mil | MIT | Muestra tokens y costo de tus sesiones (`npx ccusage`) | **No para el lab.** Solo ficha: por el post, lee los registros de Claude Code; no mide un `llama-server`. Ver también la nota sobre `latidos` en `referencia.json` |
| Graphify | n/d | n/d | Grafo consultable del código | **Ya lo tenemos** (`graph-explorer` en el catálogo) |
| `farion1231/cc-switch` | 156 mil | MIT | Aplicación de escritorio para cambiar entre agentes y proveedores | **No.** Solo ficha. Maneja claves de varios proveedores |
| `steveyegge/beads` | 29 mil | MIT | Un gestor de tareas propio del agente para proyectos largos | **Referencia.** Solo ficha. Cae en el mismo terreno que la nota de memoria de agentes |
| `Yeachan-Heo/oh-my-claudecode` | 41 mil | MIT | Equipos de varios agentes dentro de Claude Code | **No.** Solo ficha. Varios agentes revisándose entre sí es el patrón que más tokens quema |
| `microsoft/markitdown` | 197 mil | MIT | Convierte PDF, Word, Excel y otros a Markdown | **Candidato** (backlog). Pasar documentos a texto antes de dárselos al agente evita que lea binarios o formatos pesados |
| `musistudio/claude-code-router` | 38 mil | MIT | Ruteador local que manda cada pedido a otro modelo | **No.** Solo ficha. Para rutear modelos en el lab ya está Pi con modelos virtuales (`apps/pi`) |
| `coleam00/Archon` | 24 mil | MIT | Flujos de trabajo de código repetibles | **Referencia.** Solo ficha |
| `sirmalloc/ccstatusline` | 14 mil | MIT | Línea de estado de la sesión | **No.** Solo ficha; es cosmético |
| `automazeio/ccpm` | 8 mil | MIT | Convierte issues de GitHub en tareas que agentes hacen en paralelo | **No.** Solo ficha. Más agentes en paralelo |

**Por qué pasaron tres al backlog.** `claude-mem` toca directo el dolor de la memoria y el contexto entre sesiones, y declara soporte para OpenCode y Pi. `serena` evita leer archivos enteros al buscar por significado. `markitdown` reduce lo que cuesta leer documentos. Las tres se pueden probar en una máquina Windows con un modelo local, y hay que medirlas, no creerles.

## Lo que dicen pero no verificamos
- El post agrupa todo bajo «sacarle más a Claude Code»; para el lab lo que cuenta es qué funciona con OpenCode y Pi sobre un modelo local, y eso solo lo declaran algunos (`serena`, `claude-mem`).
- Las frases de cada tarjeta («Claude deja de escribir para la API del año pasado», «recuerda lo de ayer») son del autor del post y de los repositorios; no las medí.
- Las estrellas altas reflejan popularidad, no calidad ni seguridad: varios repositorios de esta lista tienen más de 100 mil estrellas y menos de 18 meses de vida.

## Cómo usarlo
1. **No instalar la lista entera.** Cada pieza que se agrega ocupa contexto (hooks, skills, servidores MCP) o suma agentes que gastan tokens.
2. **Orden razonable de pruebas en el lab:** primero medir tokens totales por tarea terminada (criterio en `contexto-en-agentes`), después una pieza a la vez: `markitdown` (sin servicios externos), `serena` y `claude-mem`.
3. **Antes de instalar `claude-mem`:** apagar la analítica anónima (`npx claude-mem telemetry disable`, según su README) y revisar con qué proveedor comprime la memoria; si usa uno externo, el código y las acciones del agente salen de la máquina.
4. **Serena es GPL-3.0-or-later:** correrlo como herramienta aparte por MCP no obliga a nada, pero no copiar su código dentro de otro proyecto sin leer la licencia.
