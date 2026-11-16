# Modelos «Flash» con Engram: tablas en SSD en vez de RAM

- Tipo: referencia
- Revisada: 2026-11-16
- Estado: a revisar (tecnología nueva; las guías son de un tercero y de hace pocos días)
- Relacionadas: `servir-modelos-locales`, `contexto-en-agentes`; `models.json`: `Qwen3.8-Flash-Next`, `Qwen3-Coder-Next`

## En una línea
Algunos modelos nuevos (Qwen3.8-Flash-Next, DeepSeek-V4.1-Flash) llevan una parte de sus parámetros en tablas de búsqueda («Engram» o n-gram por capa) que se consultan por posición y pueden quedar en el SSD, con lo que sobra menos para la RAM y la VRAM. Es una vía real para correr un modelo mayor con tu máquina, pero con los números disponibles hoy **no es una apuesta segura**.

## Qué sabemos (verificado, con fuente)
- **Qué es Engram:** un módulo de memoria condicional que recupera vectores de tablas hash de n-gramas. Como los índices de la próxima consulta se conocen en cuanto se conocen los tokens, las filas se pueden pedir con anticipación y esconder la latencia del SSD (resumen de guías de Unsloth y de artículos académicos, por ejemplo arXiv 2601.07372 y 2607.07388; no los leí enteros).
- **Qwen3.8-Flash-Next** (ficha oficial en Hugging Face): 125 B de parámetros con 6 B activos, más 51 B de tablas n-gram y 4 B de MTP (180 B en total), contexto de 256K, publicado el 2026-08-24. Licencia **Qwen Community License 1.0** (leí el texto): permite usar, copiar, modificar y desplegar libremente; las condiciones solo aplican a productos comerciales con más de 100 millones de usuarios activos o 20 millones de dólares de ingresos mensuales (mostrar el nombre del modelo) y a quien ofrezca un servicio de modelos o un asistente de IA para programar u oficina como negocio (licencia aparte), con una excepción para el uso interno. Para un laboratorio personal no es un obstáculo.
- **Cómo se corre** (guía de Unsloth, `unsloth.ai/docs/models/qwen3.8-next`, 2026-11-16): llama.cpp **b12233 o posterior** con la opción `--ple <archivo de la tabla Engram>`; la tabla puede ir a SSD con mmap. Tamaños de archivo según esa guía: IQ1_S 72,5 GB, Q2_K_XL 78,9 GB, IQ3_XXS 82,0 GB, Q3_K_XL 90,0 GB, Q4_K_XL 111,3 GB; la tabla Engram aparte pesa de 28,8 GB (IQ4_NL) a 102,4 GB (BF16). Sacar el fragmento de Engram del Q4_K_XL ahorra 28,8 GB.
- **DeepSeek-V4.1-Flash:** según Unsloth, 552 B de red principal más 196 B de Engram. La red principal sola no entra en 64 GB de RAM: descartado para este laboratorio.
- La receta `apps/llama-cpp` fija el build **b12040**, anterior al b12233: para un modelo con Engram habría que subir el build y volver a verificar hashes.

## Lo que dicen pero no verificamos
- Las cifras de memoria de la guía de Unsloth **se contradicen entre sí**: una tabla dice «4 bits: 64 GB» y a la vez el archivo Q4_K_XL pesa 111,3 GB; otra frase pide «al menos 75 GB». No se puede afirmar que algún cuantizado entre en 64 GB de RAM más 12 GB de VRAM sin probarlo.
- La velocidad (MTP «1,3 a 1,7 veces más rápido», 170 tokens por segundo en una RTX 6000 PRO) es de una tarjeta de otra categoría: no dice nada de una 3060 con RAM DDR.
- Un artículo de un tercero advierte que «Engram no permite correr un modelo de 1 billón de parámetros en local»: las ganancias son reales pero más acotadas que el entusiasmo.
- Un comentario del post ofrece un dato de CodeRouter (quien lo publica declara que vende ese servicio): Claude Code con DeepSeek V4.1 Flash resolvió 9 de 30 tareas de repositorio reales contra 16 de Claude Sonnet 5.5, con un costo por tarea de menos de un cuarto, ambos por API alojada. Sirve de cota superior para un Flash local, no como medición propia.
- Del post original, «CLM»: no pude identificar a qué proyecto se refiere. No hay nada anotado.

## Cómo usarlo
1. **Orden de prueba en el lab:** Qwen3.6-35B-A3B (cambio de menor riesgo) y Qwen3-Coder-Next (48,4 GB a Q4, el más cercano que entra en 64 GB) primero. Qwen3.8-Flash-Next solo después, y a 1 o 2 bits, donde se pierde calidad.
2. **Antes de bajar nada:** confirmar cuánto pesa realmente el fragmento de Engram del cuantizado elegido, y medir RAM, VRAM y velocidad con un contexto chico.
3. **SSD:** una tabla en SSD se lee por mmap de forma aleatoria: conviene un NVMe y no un disco mecánico ni uno lento. No está verificado el efecto en esta máquina.
4. Anotar los resultados en `models.json` y subir la fecha de esta nota.
