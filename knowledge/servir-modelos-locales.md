# Servir modelos locales: llama.cpp, vLLM o SGLang

- Tipo: criterio
- Revisada: 2026-11-16
- Estado: vigente
- Relacionadas: `contexto-en-agentes`; `apps/llama-cpp`; `apps/pi`; `models.json`

## En una línea
Para un laboratorio de **un solo usuario** con una RTX 3060 de 12 GB, 64 GB de RAM y Windows, el servidor correcto es llama.cpp (receta `apps/llama-cpp`). vLLM y SGLang están pensados para atender a muchos usuarios a la vez en GPU con mucha memoria; el motivo para mirarlos sería el caché de prefijos, y llama.cpp ya tiene el suyo.

## Qué sabemos (verificado, con fuente)
- **vLLM** (`vllm-project/vllm`): 97.028 estrellas, Apache-2.0, con commits de hoy (API de GitHub, 2026-11-16). Su documentación de instalación dice que **no soporta Windows de forma nativa**: hay que usar WSL con una distribución Linux o un fork mantenido por la comunidad. Tiene batching continuo y caché de prefijos.
- **SGLang** (`sgl-project/sglang`): 38.942 estrellas, Apache-2.0, con commits de hoy. Su README lista tarjetas NVIDIA RTX serie 30, 40 y 50 entre el hardware soportado; no verifiqué si corre en Windows nativo.
- **llama.cpp** (`llama-server`), según el README de su servidor: el caché de prompt viene **activado por defecto** (`--cache-prompt`): si un pedido comparte el comienzo con el anterior, solo se procesa la parte que cambió. Además tiene `--cache-reuse` (reutilizar fragmentos por desplazamiento de KV; por defecto 0, desactivado), `--cache-ram` (tamaño máximo del caché, por defecto 8192 MiB) y varios *slots* en paralelo (`-np`). Los MoE con los expertos en la RAM (`--cpu-moe`) son justo el caso de la receta `apps/llama-cpp`.
- Según el post: vLLM nació con PagedAttention (memoria en bloques, mucho soporte de modelos y hardware); SGLang con RadixAttention (guarda los pedidos pasados en un árbol y reutiliza el trabajo cuando varios pedidos empiezan igual: mismo prompt de sistema o mismo historial). Es una descripción general, coincide con lo que documentan los proyectos.

## Lo que dicen pero no verificamos
- Un comentario afirma que RadixAttention solo rinde por encima de ~30% de aciertos de prefijo y que por debajo es más lento que PagedAttention. Es una cifra sin fuente.
- Que «SGLang gana en agentes y RAG»: depende de cuánto prefijo se repite. Con fragmentos recuperados distintos en cada pedido, la ventaja baja.

## Cómo usarlo
1. **Quedarse con llama.cpp** mientras el uso sea de una persona y de un agente a la vez. vLLM en Windows exige WSL, y estos motores apuntan a servir muchos pedidos con modelos que caben en la GPU; no verifiqué si repartir los expertos MoE con la RAM funciona en ellos tan bien como en llama.cpp.
2. **Aprovechar el caché que ya existe.** Un agente manda en cada vuelta el mismo prompt de sistema y casi el mismo historial: ahí el caché de prefijo ahorra mucho tiempo de procesamiento. Probar `--cache-reuse` (empezar con un valor como 256, a medir) y vigilar `--cache-ram`.
3. **Medir en el log de `llama-server`**, con el tráfico real del agente: cuántos tokens del pedido se reutilizaron y cuánto tarda el primer token en la segunda vuelta de una tarea. Es la medición del consejo central del post: no elegir por el gráfico de otro, correr el propio tráfico.
4. **Cambiar de modelo a mitad de una tarea rompe el caché:** el modelo nuevo tiene que reprocesar todo el historial. Es la duda abierta de los modelos virtuales de Pi (`apps/pi`).
5. **vLLM o SGLang solo tendrían sentido** si algún día se sirve un modelo a varias personas desde una GPU con memoria suficiente. No hay acción pendiente para el laboratorio ni para el marketplace del equipo.
