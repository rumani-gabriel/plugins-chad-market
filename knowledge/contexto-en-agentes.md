# Gestión de contexto en agentes: lo investigado hasta ahora

- Tipo: estrategia
- Revisada: 2026-11-16
- Estado: vigente (se actualiza cada vez que se evalúa algo del tema)
- Relacionadas: `busqueda-web-para-agentes`, `rag-visual-vs-texto`; entradas de `backlog.json`: `context-mode`, `rtk`, `txtai`, `floorplan`, `memorilla`, `pi-coding-agent` (ahora `apps/pi`); `catalog.json`: `graph-explorer`, `fast-grep`, `cocoindex`, `llama-cpp`

## En una línea
El contexto es el recurso escaso de un agente, sobre todo con un modelo local de contexto corto. El gasto grande no es una sola lectura sino el agente que **relee** y repite; hay siete familias de soluciones y ninguna tiene todavía una medición propia en este laboratorio.

## Qué sabemos (verificado, con fuente)
Por familia, con el estado real de cada hallazgo:

1. **Recortar la salida de las herramientas antes de que entre al modelo.** `context-mode` (licencia Elastic 2.0) y `rtk`. Un benchmark independiente de JetBrains sobre `rtk` 0.43 encontró 7,6% *más* costo a esfuerzo de razonamiento bajo y casi ningún ahorro a esfuerzo alto: no asumir ahorro. Estado: backlog, sin medir.
2. **Consultar un índice en vez de releer archivos.** `fast-grep` (búsqueda indexada, en el catálogo), `cocoindex` (indexado incremental, receta) y `txtai` (base de embeddings con servidor MCP, en backlog para probar).
3. **Un mapa del código en vez de leerlo entero.** `graph-explorer` (grafo local del repo, en el catálogo) y `floorplan` (mapa con nombres en lenguaje llano, en backlog; ojo: su descripción puede quedar vieja si solo cambia el cuerpo de una función).
4. **Memoria que no ocupa el contexto.** `memorilla` (Stanford) comprime documentos en 16 embeddings que entran al modelo; es investigación, está entrenada para un Qwen3-8B concreto y no funciona detrás de `llama-server` ni de OpenCode. Referencia, no herramienta.
5. **Enrutar por tarea.** Pi (`apps/pi`) permite un modelo virtual que manda lo simple al Qwen local y lo difícil a un modelo remoto; duda abierta: cambiar de modelo a mitad de una tarea obliga a reprocesar el contexto.
6. **Búsqueda web que devuelve extractos.** Ver la nota `busqueda-web-para-agentes`.
7. **Indexar páginas como imagen en vez de texto** (`pixelrag`, en backlog): evita la pérdida del parser, pero una imagen también gasta contexto y hace falta un modelo con visión. Ver la nota `rag-visual-vs-texto`.

## Lo que dicen pero no verificamos
- Todas las cifras de ahorro de los autores (98%, 84%, 50%, 4.212 veces menos tokens): son de quien vende o publica la herramienta, sobre sus propios casos.

## Cómo usarlo
- **Qué medir:** tokens totales por tarea *terminada* y la calidad del resultado, con y sin la herramienta, con la versión fijada y las mismas tareas. Contar también las llamadas repetidas.
- **Orden sugerido para el lab:** primero lo que no agrega piezas (acotar lecturas, `fast-grep`, `graph-explorer`), después un índice (`txtai`), y solo al final recortar salidas (`context-mode`), porque es la familia con peor evidencia independiente.
- **Contexto corto:** con un modelo local, cada herramienta nueva suma descripciones al contexto; preferir pocas herramientas simples. Si un servidor MCP trae muchas (Concat: 45), ver `mcp-servidor-y-skills` por la idea de un proxy que oculte las que no se usan (sin probar).
