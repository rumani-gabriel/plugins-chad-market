# RAG visual o de texto: dónde se pierde la información

- Tipo: estrategia
- Revisada: 2026-11-16
- Estado: a revisar (idea con respaldo de un solo grupo y sin prueba propia)
- Relacionadas: `contexto-en-agentes`, `busqueda-web-para-agentes`; `backlog.json` o `referencia.json`: `pixelrag`; `models.json`: `Qwen3.8-27B` (el candidato con visión)

## En una línea
En un RAG de páginas web o de documentos, el punto donde más se pierde información suele ser el *parser* que convierte HTML o PDF en texto (tablas, gráficos y diseño se aplanan o se descartan). PixelRAG propone indexar la página como imagen (capturas en mosaicos) y que un modelo con visión la lea.

## Qué sabemos (verificado, con fuente)
- El proyecto existe y es abierto: `StarTrail-org/PixelRAG`, licencia Apache-2.0, 10.950 estrellas, creado el 2026-05-29, versión v0.4.0 (2026-07-16), con commits hasta 2026-11-11 (API de GitHub, 2026-11-16). El artículo asociado figura como arXiv 2606.28344 (no lo leí).
- Cómo funciona, según su README: renderiza páginas web, PDF o imágenes a mosaicos de captura; los embebe con `Qwen3-VL-Embedding` (la receta de ejemplo usa la variante de 2B); arma un índice FAISS y lo expone con una API de búsqueda. El lector es un modelo con visión.
- Además trae una pieza independiente y más simple, `pixelshot`: captura una URL, un HTML local, un PDF o una imagen con Playwright/Chromium en la propia máquina y devuelve las rutas de los mosaicos para que el agente los lea con su herramienta de lectura. Hay una skill para Claude Code (`pixelbrowse`) y un plugin de OpenCode en npm (`@startrail/pixelbrowse` 0.1.0, Apache-2.0).
- Para correr el índice completo el README menciona Linux con CUDA y macOS con Apple Silicon; Windows no aparece.

## Lo que dicen pero no verificamos
- «Un parser de HTML a texto puede perder más del 40% de una página» y «cambiar de parser mueve la exactitud unos 10 puntos»: cifras del post, sin fuente a la vista. Un comentario del propio post lo cuestiona con razón: depende del parser y de las páginas elegidas.
- «Supera en 18,1% al mejor RAG de texto en preguntas de solo texto» sobre 30 millones de capturas de Wikipedia: cifra de los autores; no sé qué base de comparación ni cuántas preguntas usaron.
- Que un lector más fuerte mejora la respuesta sin reindexar es cierto por construcción (el índice son píxeles), pero el costo de volver a procesar imágenes con cada lector no está medido.

## Cómo usarlo
1. **No cambiar un RAG por esto sin medir con documentos propios.** Tomar 20 documentos con tablas o gráficos y 20 preguntas con respuesta conocida; compararlas con el pipeline de texto actual y con el visual. Anotar aciertos, tokens que consume cada imagen o tramo de texto y latencia.
2. **Antes de acusar al retriever, revisar el parser:** probar dos parsers distintos sobre los mismos documentos. Si la exactitud cambia mucho, el problema es el parser, no el modelo.
3. **Una imagen no es gratis en contexto.** Un mosaico consume tokens de visión; para una página larga pueden ser varios mosaicos. Es una hipótesis a medir, no un ahorro asegurado frente al texto extraído.
4. **Con modelos locales hace falta un modelo con visión** y, con llama.cpp, el archivo de proyección de imagen que lo acompañe. El Qwen3-30B-A3B de la receta `apps/llama-cpp` es solo de texto: no puede leer los mosaicos.
5. **Las capturas de páginas ajenas son datos, no instrucciones:** una página puede esconder texto dirigido al agente. La propia skill de `pixelbrowse` lo advierte.
