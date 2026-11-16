# RAG: recuperación híbrida (palabras clave + significado + fusión de rankings)

- Tipo: estrategia
- Revisada: 2026-11-16
- Estado: vigente
- Relacionadas: `rag-visual-vs-texto`, `contexto-en-agentes`; `backlog.json`: `txtai`; `catalog.json`: `fast-grep`, `cocoindex`

## En una línea
Cuando un RAG devuelve documentos «relevantes» pero la respuesta sale mal, el problema suele estar en cómo se recupera, no en el modelo. Combinar búsqueda por palabras clave (BM25) y búsqueda por significado (vectores) y fusionar sus rankings (RRF) cubre lo que cada una pierde por separado.

## Qué sabemos (verificado, con fuente)
- **BM25** encuentra coincidencias exactas de términos (identificadores, códigos, nombres de funciones, números de versión) pero no entiende sinónimos ni paráfrasis. La **búsqueda vectorial** entiende significado pero puede pasar por alto un término exacto. Esta descripción es la del post y es la explicación estándar de la técnica.
- **RRF (Reciprocal Rank Fusion)** une las dos listas por posición, no por puntaje: cada documento suma 1/(k + posición) en cada lista (en el artículo original, k = 60 por defecto) y se ordena por la suma. No hace falta normalizar los puntajes de BM25 y del coseno, que no son comparables. Esa fórmula la recuerdo de la literatura; no la volví a verificar hoy.
- **Aplicado a código:** un agente que busca código necesita las dos cosas: el identificador exacto (grep o BM25) y «dónde se maneja X» (significado). En este repo, `fast-grep` cubre lo exacto e indexado, y `txtai` (en backlog) trae índices dispersos y densos en una sola base: una combinación posible, sin probar.

## Lo que dicen pero no verificamos
- «Mejores respuestas empiezan por mejor recuperación, no por un modelo más grande»: es la tesis del post; plausible, sin medición propia aquí. El post tampoco da cifras.

## Matices útiles (de los comentarios, sin verificar)
- RRF pone el mismo peso a un documento que un buscador puntuó muy por encima del resto y a uno que apenas coincidió. Si un buscador es claramente mejor en tu corpus, ponderar las listas antes de fusionar puede rendir más. Conviene compararlo con una normalización de puntajes afinada, con tus propias consultas.
- Medir **por separado** la recuperación (recall@k: ¿llegó la evidencia correcta al conjunto?) y la fundamentación de la respuesta (¿el modelo se apoyó en ella?). Así se sabe qué lado arreglar primero.
- El **reranker** (un modelo que reordena los candidatos) es lo que suma la mayor latencia: BM25, vectores y RRF son baratos, sobre todo en paralelo.
- El **tamaño y la forma de los fragmentos** (chunking) y las **versiones en conflicto de un mismo documento** también causan respuestas malas aunque la recuperación sea buena.

## Cómo usarlo
1. **Empezar por medir:** 20 preguntas con respuesta conocida sobre documentos propios; anotar si la evidencia correcta aparece en los 5 primeros resultados con solo BM25, solo vectores e híbrido.
2. **Si solo vectores falla en identificadores exactos,** agregar BM25 y fusionar con RRF. Si solo BM25 falla en preguntas de significado, agregar vectores.
3. **Agregar un reranker solo si** el híbrido deja la evidencia buena pero mal ordenada, y medir cuánta latencia suma.
4. **Con un modelo local de contexto corto,** pasar pocos fragmentos buenos: devolver 3 bien rankeados cuesta menos contexto que 10 mediocres.
