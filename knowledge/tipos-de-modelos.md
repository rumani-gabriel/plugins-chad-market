# Tipos de modelos de IA: qué es cada sigla y cuál sirve en el lab

- Tipo: referencia
- Revisada: 2026-11-18
- Estado: vigente
- Relacionadas: `servir-modelos-locales`, `modelos-flash-engram`, `afinar-modelos-locales`, `rag-recuperacion-hibrida`; `models.json`; `apps/llama-cpp`

## En una línea
Una infografía de un tercero lista ocho siglas (LLM, LCM, LAM, MoE, VLM, SLM, MLM, SAM) como si fueran «ocho arquitecturas» del mismo nivel. No lo son: unas son familias de modelos, otras son una técnica interna de un modelo y una es solo un nombre de mercado. Esta nota las ordena y dice cuáles se usan o se podrían usar en la máquina del lab (RTX 3060 de 12 GB, 64 GB de RAM).

## Qué sabemos (verificado, con fuente)
**LCM (Large Concept Model).** Es una línea de investigación publicada por el equipo de Meta: «Large Concept Models: Language Modeling in a Sentence Representation Space». En vez de predecir el siguiente *token*, predice la siguiente *oración*, representada con SONAR (un codificador y decodificador de oraciones independiente del idioma). Según el repositorio oficial (`facebookresearch/large_concept_model`) hay recetas para un modelo de 1,6 B con pérdida MSE y para uno de difusión de dos torres; las versiones cuantizadas figuran como «próximamente». Un trabajo posterior (SONAR-LLM, arXiv 2508.05305) conserva la idea pero entrena con entropía cruzada por token. Fuentes consultadas el 2026-11-18: el repositorio oficial y resúmenes secundarios. Es investigación: no hay un modelo listo para correr con `llama-server`.

**MoE (mezcla de expertos).** Fuente: nuestras propias notas y `models.json` (verificado en llama.cpp al armar `apps/llama-cpp`). Es una **técnica dentro de un transformer**, no una alternativa a él: un enrutador elige unos pocos «expertos» por token y combina sus salidas, así que el modelo tiene muchos parámetros en total pero usa pocos por token. Por eso en el lab los MoE grandes son viables: con `--cpu-moe` los expertos van a la RAM y la GPU se queda con la parte que se usa siempre. Ejemplos ya anotados: Qwen3-Coder-Next (80 B en total, 3 B activos) y Qwen3.6-35B-A3B. Los MoE de 30 a 35 B no se pueden afinar con 12 GB (ver `afinar-modelos-locales`).

## Lo que dicen pero no verificamos
Todo lo que sigue es conocimiento general mío, no lo comprobé hoy contra una fuente:
- **LLM (modelo de lenguaje grande):** predice el siguiente token con capas de transformer. Es el caso base: todos los Qwen del lab.
- **LAM (modelo de acción grande):** **no es una arquitectura establecida**. Es un nombre que se usa para agentes que ejecutan acciones; por dentro suele ser un LLM con herramientas. En el lab eso es OpenCode o Pi con un Qwen: ver `apps/pi`.
- **VLM (modelo de visión y lenguaje):** un codificador de imágenes alimenta a un modelo de lenguaje. Útil para el «Jarvis» con visión y para leer capturas de pantalla. Candidato en `models.json`: Qwen3.8-27B (con visión).
- **SLM (modelo de lenguaje pequeño):** un LLM chico y cuantizado, pensado para correr en un equipo modesto. Es lo que entra entero en los 12 GB de VRAM.
- **MLM (modelo de lenguaje enmascarado):** estilo BERT, ve el contexto de los dos lados y rellena palabras tapadas. No genera texto largo; se usa para búsqueda, clasificación y reordenadores de resultados, o sea, la parte de significado del RAG híbrido (ver `rag-recuperacion-hibrida`).
- **SAM (Segment Anything):** modelo de visión que recorta objetos de una imagen según una indicación. No es de lenguaje. Podría servir para recortar fondos en video, algo que el MCP de Concat no trae de fábrica (ver `apps/concat`), pero no lo evaluamos.

## Cómo usarlo
1. **Para elegir un modelo para el lab:** pensar primero en el tamaño (qué entra en 12 GB) y en si es denso o MoE; las demás siglas casi nunca deciden.
2. **Si aparece otra infografía de «arquitecturas de IA»:** desconfiar de que pongan al mismo nivel familias (LLM, VLM), técnicas internas (MoE) y nombres de mercado (LAM).
3. **LCM:** seguirlo como investigación; no esperar un modelo utilizable en el lab todavía.
4. **Mapa rápido de lo que ya tenemos:** LLM denso → Qwen3.5-9B y Qwen3-14B (para afinar); MoE → Qwen3-Coder-Next y Qwen3.6-35B-A3B (para servir con `--cpu-moe`); VLM → Qwen3.8-27B; agente (lo que el post llama LAM) → Pi u OpenCode sobre un Qwen local.
