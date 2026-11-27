# Servir modelos locales: llama.cpp, vLLM, SGLang o Magnitude

- Tipo: criterio
- Revisada: 2026-11-27
- Estado: vigente
- Relacionadas: `contexto-en-agentes`, `modelos-flash-engram`; `apps/llama-cpp`; `apps/pi`; `models.json`; `backlog.json`: `magnitude`

## En una línea
Para un laboratorio de **un solo usuario** con una RTX 3060 de 12 GB, 64 GB de RAM y Windows, el candidato de base sigue siendo llama.cpp (receta `apps/llama-cpp`). vLLM y SGLang están pensados para atender a muchos usuarios a la vez en GPU con mucha memoria; el motivo para mirarlos sería el caché de prefijos, y llama.cpp ya tiene el suyo. Desde el 2026-11-27 hay un cuarto candidato que sí apunta directo al caso del lab: **Magnitude** (`backlog.json`), que automatiza el mismo reparto GPU/RAM/SSD que hoy se hace a mano con `--cpu-moe`.

## Qué sabemos (verificado, con fuente)
- **vLLM** (`vllm-project/vllm`): 97.028 estrellas, Apache-2.0, con commits de hoy (API de GitHub, 2026-11-16). Su documentación de instalación dice que **no soporta Windows de forma nativa**: hay que usar WSL con una distribución Linux o un fork mantenido por la comunidad. Tiene batching continuo y caché de prefijos.
- **SGLang** (`sgl-project/sglang`): 38.942 estrellas, Apache-2.0, con commits de hoy. Su README lista tarjetas NVIDIA RTX serie 30, 40 y 50 entre el hardware soportado; no verifiqué si corre en Windows nativo.
- **llama.cpp** (`llama-server`), según el README de su servidor: el caché de prompt viene **activado por defecto** (`--cache-prompt`): si un pedido comparte el comienzo con el anterior, solo se procesa la parte que cambió. Además tiene `--cache-reuse` (reutilizar fragmentos por desplazamiento de KV; por defecto 0, desactivado), `--cache-ram` (tamaño máximo del caché, por defecto 8192 MiB) y varios *slots* en paralelo (`-np`). Los MoE con los expertos en la RAM (`--cpu-moe`) son justo el caso de la receta `apps/llama-cpp`.
- Según el post: vLLM nació con PagedAttention (memoria en bloques, mucho soporte de modelos y hardware); SGLang con RadixAttention (guarda los pedidos pasados en un árbol y reutiliza el trabajo cuando varios pedidos empiezan igual: mismo prompt de sistema o mismo historial). Es una descripción general, coincide con lo que documentan los proyectos.
- **Magnitude** (`magnitudedev/magnitude`, Apache-2.0, Rust, 9.073 estrellas, creado 2026-06-12; README leído completo el 2026-11-27): motor de inferencia que reparte un modelo en tres niveles (VRAM para las capas compartidas y los expertos más usados, RAM para el siguiente nivel, SSD para el resto) y, según su README, predice y precarga los expertos de un MoE antes de que la GPU los necesite, además de afinar los kernels automáticamente para el chip detectado. Corre nativo en Windows (instalador o solo CLI), usa modelos GGUF de Hugging Face —el mismo formato de `apps/llama-cpp`— y se conecta con un clic a Pi y a OpenCode. Dice ser "más del doble de rápido que Ollama" (su propia comparación, con gráficos en su web, no verificados en texto); **no compara contra llama.cpp**, que es lo que ya usa el lab.

## Lo que dicen pero no verificamos
- Un comentario afirma que RadixAttention solo rinde por encima de ~30% de aciertos de prefijo y que por debajo es más lento que PagedAttention. Es una cifra sin fuente.
- Que «SGLang gana en agentes y RAG»: depende de cuánto prefijo se repite. Con fragmentos recuperados distintos en cada pedido, la ventaja baja.

## Cómo usarlo
1. **Quedarse con llama.cpp** mientras el uso sea de una persona y de un agente a la vez. vLLM en Windows exige WSL, y estos motores apuntan a servir muchos pedidos con modelos que caben en la GPU; no verifiqué si repartir los expertos MoE con la RAM funciona en ellos tan bien como en llama.cpp.
2. **Aprovechar el caché que ya existe.** Un agente manda en cada vuelta el mismo prompt de sistema y casi el mismo historial: ahí el caché de prefijo ahorra mucho tiempo de procesamiento. Probar `--cache-reuse` (empezar con un valor como 256, a medir) y vigilar `--cache-ram`.
3. **Medir en el log de `llama-server`**, con el tráfico real del agente: cuántos tokens del pedido se reutilizaron y cuánto tarda el primer token en la segunda vuelta de una tarea. Es la medición del consejo central del post: no elegir por el gráfico de otro, correr el propio tráfico.
4. **Cambiar de modelo a mitad de una tarea rompe el caché:** el modelo nuevo tiene que reprocesar todo el historial. Es la duda abierta de los modelos virtuales de Pi (`apps/pi`).
5. **vLLM o SGLang solo tendrían sentido** si algún día se sirve un modelo a varias personas desde una GPU con memoria suficiente. No hay acción pendiente para el laboratorio ni para un uso en equipo por ese lado.
6. **Magnitude sí tiene una acción pendiente concreta:** instalarlo en el lab y correr el mismo modelo MoE que ya está en `models.json` (Qwen3-Coder-Next o Qwen3.6-35B-A3B) contra la receta actual de `apps/llama-cpp` con `--cpu-moe`, midiendo tokens por segundo, uso de RAM/VRAM y latencia del primer token en las mismas tareas. Es la única comparación que falta, porque la del propio proyecto es contra Ollama, no contra lo que el lab usa hoy.

**Cache de prefijo en un cluster (referencia).** llm-d (Apache-2.0, 5 mil estrellas, v1.0; README leído el 2026-11-20) muestra por qué el cache de prefijo importa: con varias réplicas detrás de un reparto por turnos el ahorro se pierde, porque la réplica que atiende casi nunca vio el prefijo, y el proyecto lo resuelve enrutando según qué réplica ya lo tiene. Sus cifras (3x de rendimiento, 13,9x con descarga a CPU) son de socios, en hardware de centro de datos, y no aplican a una sola máquina. En el lab la lección es otra: un agente que reenvía casi el mismo historial se beneficia de `--cache-prompt` de llama-server solo si el historial no se reescribe entre vueltas (ver lo anotado sobre compresores de contexto en `contexto-en-agentes`).
