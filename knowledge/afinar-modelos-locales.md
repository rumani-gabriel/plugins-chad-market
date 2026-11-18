# Afinar (fine-tuning) modelos locales para tareas propias

- Tipo: guía
- Revisada: 2026-11-16
- Estado: a revisar (nada se ejecutó; las cifras de memoria son mínimos publicados por Unsloth)
- Relacionadas: `servir-modelos-locales`, `contexto-en-agentes`, `simulacro-sin-nube`; `apps/unsloth`; `apps/llama-cpp`; `models.json`; `backlog.json` o `referencia.json`: `minimind`, `train-llm-from-scratch`

## En una línea
**MiniMind no es el entrenador que buscás:** entrena un modelo propio diminuto (64 millones de parámetros) desde cero con fines didácticos; no afina Qwen ni ningún modelo que ya uses. Lo que sí sirve para afinar tus modelos locales en una RTX 3060 de 12 GB es **Unsloth** (receta `apps/unsloth`), con límites claros de tamaño y una condición previa: tener datos y una forma de medir si mejoró.

## Qué sabemos (verificado, con fuente)
### MiniMind (`jingyaogong/minimind`)
- API de GitHub, 2026-11-16: 65.550 estrellas, licencia Apache-2.0, creado el 2024-07-27, último commit 2026-10-27.
- Según su README: un modelo de ~64 M de parámetros (1/2700 de GPT-3) con todo el recorrido de entrenamiento escrito en PyTorch puro: limpieza de datos, preentrenamiento, SFT, LoRA, DPO, PPO, GRPO y CISPO, uso de herramientas y RL de agentes, destilación; hay variantes de visión, multimodal y de difusión.
- Aclaración del propio README: las «2 horas» son **una época de la etapa de SFT** en una RTX 3090, no todo el recorrido; y los «3 yuanes» son el costo de alquiler de esa tarjeta.
- Qué es: una herramienta para aprender cómo se hace un LLM. Qué no es: un modelo útil como agente ni una forma de especializar tus Qwen.

### Unsloth (`unslothai/unsloth`), la vía real
- API de GitHub y documentación oficial: 79.611 estrellas, licencia Apache-2.0 en el paquete base (los componentes opcionales, como la interfaz Studio, son AGPL-3.0), commits de hoy; versiones casi diarias (la última, v0.1.918-beta del 2026-11-16).
- Se usa de tres formas: la aplicación de escritorio, la interfaz web Studio y la biblioteca. **Funciona en Windows de forma nativa** (Windows 10 u 11 de 64 bits, NVIDIA con controladores, Python 3.11 a 3.13) y exige capacidad de cómputo CUDA 7.0 o superior (la 3060 es Ampere: la cumple).
- Memoria mínima publicada para entrenar (QLoRA de 4 bits / LoRA de 16 bits): 7B 5 GB / 19 GB; 8B 6 GB / 22 GB; 14B 8,5 GB / 33 GB; 27B 22 GB / 64 GB; 32B 26 GB / 76 GB. Son mínimos absolutos: contexto largo y lotes grandes necesitan más; la guía recomienda lotes de 1 a 3 si falta memoria.
- Flujo de Studio según su documentación: cargar un modelo, importar datos (PDF, CSV o JSONL, o armarlos con «Data Recipes»), entrenar con valores recomendados o propios, ver la pérdida y el uso de GPU en vivo, **chatear con el modelo afinado y compararlo con el base**, y exportar a safetensors o **GGUF** (para llama.cpp, Ollama, LM Studio). Dice que corre «100% sin conexión y en local» y que no recoge telemetría de uso, solo datos mínimos de hardware; no aclara qué descargas necesita (los modelos vienen de Hugging Face).
- Modelos base candidatos que entran en 12 GB (fichas de Hugging Face, Apache-2.0): **Qwen3.5-9B** (9,65 B, 2026-02-27), **Qwen3-14B** (14,77 B), Qwen3-8B (8,19 B) y Qwen3-4B (4,02 B).

## Lo que no cabe (y por qué importa)
- **El Qwen3-30B-A3B de la receta `apps/llama-cpp` y los MoE grandes (Qwen3.6-35B-A3B, Qwen3-Coder-Next) no se afinan en esta máquina.** Para un MoE de 35B, un artículo de terceros cita unos 74 GB de VRAM en bf16, y la documentación de Unsloth sobre Qwen3.6 no da ninguna cifra de entrenamiento (solo de inferencia). No lo verifiqué en la fuente oficial: tomarlo como probable, no como confirmado. Lo que sí se afina en 12 GB es un modelo **denso de 8 a 14 B**.
- Un modelo afinado de ese tamaño **no se acerca a Sonnet u Opus** en razonamiento general: aprende formato, estilo, vocabulario y patrones de tu trabajo, no capacidad que el modelo base no tiene.

## Lo que dicen pero no verificamos
- «Entrena 2 veces más rápido con 70% menos de VRAM» (lema de Unsloth): cifra suya, sin medición propia. Los mínimos de la tabla son la parte más comprobable.
- Que afinar permita internalizar un prompt de sistema o una skill larga y así gastar menos contexto por tarea: hipótesis razonable para un modelo local de contexto corto; no está medida.

## Cuándo conviene afinar (y cuándo no)
**Primero probar lo barato:** un mejor prompt, una skill, un índice de búsqueda (`rag-recuperacion-hibrida`), otro modelo (`models.json`). Afinar tiene sentido cuando:
- el modelo falla **siempre igual** en una tarea repetida (formato de salida, llamadas a herramientas con un esquema propio, un dialecto de comandos, un estilo de revisión);
- tenés **entre cientos y pocos miles de ejemplos buenos** de esa tarea (entrada y salida correctas), de tu propio trabajo;
- podés **medir** el antes y el después con un conjunto aparte de ejemplos.

No conviene afinar para «que sepa más» (para eso, recuperación de datos) ni sin datos.

## Cómo usarlo
1. **Medir la base primero:** elegir una tarea, juntar 20 ejemplos de evaluación que **no entren al entrenamiento** y anotar cuántos resuelve el modelo base (mismo servidor, mismo contexto).
2. **Armar los datos:** 100 a 500 ejemplos reales de esa tarea, revisados a mano. Calidad antes que cantidad.
3. **Afinar con QLoRA** un modelo denso de 8 a 14 B (`apps/unsloth`), con el servidor de llama.cpp apagado: la VRAM es de uno u otro.
4. **Comparar contra el base** con los 20 ejemplos apartados (la propia interfaz permite chatear con ambos), y recién entonces exportar a GGUF y servirlo con llama.cpp.
5. **Guardar el resultado con fecha** en `models.json`: modelo base, datos usados, cuántos de 20 resuelve antes y después. Si no mejora o empeora otras tareas, descartarlo; el modelo base no se toca.

## Precauciones
- **Datos de entrenamiento:** usá tus propios ejemplos o salidas de modelos de licencia abierta. Los términos de uso de varios proveedores de modelos alojados (Anthropic y OpenAI entre ellos) limitan usar sus salidas para entrenar modelos que compitan con ellos: leer los términos vigentes antes de usar esas salidas como datos.
- **Datos sensibles:** nada de una organización ni de terceros en el conjunto de datos; si el modelo se publica, esos datos pueden salir.
- **Olvido:** un modelo afinado en una tarea puede empeorar en otras. Por eso se guarda el base y se mide fuera del conjunto de entrenamiento.
- **Costo de tiempo:** en una 3060 un afinado de un modelo de 8 B con pocos ejemplos puede llevar horas; no se midió.
