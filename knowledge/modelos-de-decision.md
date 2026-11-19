# Modelos de decisión: clasificadores que devuelven probabilidades en vez de texto

- Tipo: criterio
- Revisada: 2026-11-19
- Estado: vigente
- Relacionadas: `sandbox-para-agentes`, `contexto-en-agentes`, `rag-recuperacion-hibrida`, `servir-modelos-locales`, `tipos-de-modelos`; `models.json`: `JevK5`; `apps/llama-cpp`, `apps/pi`

## En una línea
Un modelo de decisión no escribe una respuesta: lee un estado (texto, JSON o imágenes) y una pregunta cerrada declarada en código (sí o no, elegir entre opciones, un puntaje) y devuelve **la probabilidad de cada opción**, sin explicación. Sirve como pieza barata y repetible dentro de un agente, para decidir y no para conversar.

## Qué sabemos (verificado, con fuente)
**El concepto** (artículo «Nine places to use decision models in agentic RAG systems», newsletter de SwirlAI, 2026-11-19): el autor usa una API alojada de TypeSafe AI en todos los ejemplos y nombra también una «OpenAI Decisions API». El artículo no da tamaños, latencias ni costos, y no dice si algún modelo corre en local. Los umbrales viven en tu código y hay que calibrarlos con tu propio tráfico.

**Los nueve usos que propone, y su cuidado principal:**
1. **Enrutar modelos:** una pregunta de opciones elige el nivel (barato para consultas, caro para lo que no podés fallar); por debajo de un umbral calibrado se cae a un modelo seguro.
2. **Guardias:** una pregunta de sí/no *por cada riesgo* (inyección, datos personales, fuera de política), antes del modelo y sobre su borrador. Una sola pregunta combinada obliga a tolerar lo mismo para todo.
3. **Suficiencia de la recuperación:** ¿lo recuperado alcanza para responder o hay que buscar de nuevo?
4. **Filtrar y reordenar pasajes:** una llamada por pasaje; el costo crece con la cantidad de pasajes.
5. **Verificar citas:** apoya, contradice o no trata el tema. Extraer el fragmento sigue necesitando un modelo generativo.
6. **Compuerta de herramientas:** permitir, preguntar o negar por llamada, con preguntas separadas («¿está intencionado?», «¿es irreversible?») y no un «¿es seguro?» único.
7. **Terminar bucles:** una llamada por criterio de aceptación; los criterios fallidos se devuelven al agente como contexto.
8. **Compactar contexto:** puntuar cada trozo y descartar lo viejo en vez de resumirlo.
9. **Evaluaciones:** reemplazar un juez LLM por una pregunta por criterio, más barata, con confianza.

**Modelos abiertos que lo hacen (Hugging Face, 2026-11-19):** Jev, el modelo de TypeSafe, **no es abierto** (solo servicio alojado). La alternativa abierta e independiente más concreta es **JevK5** (Apache-2.0, base Qwen3.5-4B, también 2B y 9B), con versiones GGUF para llama.cpp (4B Q5_K_M: 3,07 GB; 9B Q5_K_M: 6,47 GB). Según su ficha, el 4B v0.3 acierta 0,784 en el nivel difícil de JevBench y 0,944 en el estándar, y lo cuantizado a Q8_0 da la misma respuesta que el modelo completo en 229 de 231 casos. Son cifras autoinformadas; detalle y pruebas pendientes en `models.json`.

**Cómo funciona por dentro (ficha de JevK5):** la «lectura» es un softmax sobre los logits de las letras de respuesta en el siguiente token, dividido por una temperatura de calibración. No genera texto.

**Llama.cpp ya expone lo necesario para imitarlo:** el servidor devuelve las probabilidades de los mejores tokens (`n_probs`, documentado en el README del servidor). Se puede pedir a un Qwen común que responda una letra y leer su probabilidad. Falta la calibración que traen los modelos de decisión.

## Lo que dicen pero no verificamos
- **«Gemini Decision 1» de Google:** según blogs secundarios, un endpoint lanzado el 2026-11-11, con latencia de 150 a 250 ms y 0,10 USD por millón de tokens de entrada. No lo contrasté con la documentación de Google; es un servicio alojado, no sirve para el lab.
- **Seguridad:** un trabajo académico (arXiv 2610.12292, leído solo por su resumen en buscadores) dice que usar este tipo de modelos como guardias de agentes se puede burlar con texto que controla el atacante. Probado en modelos abiertos, no en Gemini. Tratarlo como advertencia: **una compuerta de decisión no es una barrera de seguridad.**
- Cualquier cifra de calibración depende de que los umbrales se midan con casos propios; el artículo y las fichas coinciden en eso.

## Cómo usarlo
1. **Pensarlo como un clasificador barato**, no como un modelo más inteligente. No reemplaza al agente; le pone una pregunta cerrada en un punto concreto.
2. **Para el lab, el primer uso con sentido es la compuerta de herramientas** de Pi u OpenCode: «¿este comando está intencionado?» y «¿es irreversible?», con umbrales distintos. Va *antes* de la ejecución, y **además** del aislamiento (`sandbox-para-agentes`), no en su lugar.
3. **Segundo uso: terminar bucles por criterio**, para que el agente no se pare antes de tiempo ni siga de más. Un comentario del propio post pide tope duro de iteraciones y de tokens al lado, por si el clasificador duda siempre.
4. **Medir antes de confiar:** armar de 50 a 100 casos propios etiquetados a mano, fijar umbrales y revisar precisión y falsos rechazos cada vez que se mueve un umbral (un umbral mal puesto falla sin hacer ruido).
5. **Idioma:** JevK5 está documentado solo en inglés; probar con español antes de usarlo.
6. **Cuidado con el contexto:** cada decisión es una llamada más; en pasajes o criterios la cantidad de llamadas crece y se come el tiempo que se quería ahorrar.
