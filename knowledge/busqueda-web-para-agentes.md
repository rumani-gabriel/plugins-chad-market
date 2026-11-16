# Búsqueda web para agentes: devolver contexto útil, no más texto

- Tipo: criterio
- Revisada: 2026-11-16
- Estado: vigente
- Relacionadas: `contexto-en-agentes`, `apps/keenable-search`

## En una línea
Los resultados de una búsqueda entran directo al contexto del modelo: más texto no es mejor. Un buen buscador para agentes devuelve extractos acotados y datos estructurados; hay que medirlo por tokens totales por tarea terminada, no por tokens por llamada.

## Qué sabemos (verificado, con fuente)
- Un buscador pensado para agentes ofrece, en general, tres cosas: buscar (resultados con extracto), leer una página como texto limpio, y a veces consultas más estructuradas. El caso revisado fue Keenable (documentación oficial `docs.keenable.ai`, 2026-11-16): Search, Fetch y SELECT, servidor MCP en `https://api.keenable.ai/mcp` con las herramientas `search_web_pages` y `fetch_page_content`.
- Uso sin cuenta y sin clave, con un tope de 1.000 pedidos por hora por IP. Con clave de API no hay tope horario y el uso es por créditos (la documentación menciona el error HTTP 402 `insufficient_credits`).
- Su política de privacidad general no menciona las consultas ni ofrece retención cero; habla de datos de uso y telemetría para «investigación y desarrollo». Es un servicio alojado: **cada consulta sale de la máquina**.

## Lo que dicen pero no verificamos
- «Primero en Artificial Analysis y en NEEDLE»: NEEDLE es un benchmark publicado por el propio proveedor; el ranking independiente no lo pude ver.
- «Reduce 50% los tokens en tareas de investigación» y «100 millones de tarjetas de conocimiento»: afirmaciones del proveedor, sin medición propia.
- Precios de listados de terceros (100.000 pedidos gratis al mes, 1 USD por 1.000 pedidos): no están en la documentación oficial que leí.

## Cómo usarlo
1. **Pedir extractos, leer completo solo si hace falta.** Primero buscar; abrir una página entera solo cuando el extracto no alcanza.
2. **Medir llamadas de seguimiento.** Los comentarios más sensatos del post original apuntan a esto: un extracto que descartó justo el dato importante hace que el agente repita búsquedas, y el fallo aparece después como un error del modelo. El ahorro por llamada puede perderse en llamadas extra.
3. **Mirar la fecha de cada resultado** y desconfiar de los datos viejos.
4. **Consultas sin datos sensibles** cuando el buscador es un servicio alojado: nada de nombres de objetivos de una prueba, claves, rutas ni datos de una organización.
5. **Probar antes de adoptar** con 10 consultas reales del laboratorio, contra la lectura directa de páginas que ya hace el agente. Anotar por consulta: tokens devueltos, si respondió bien, cuántas llamadas extra hizo y la latencia.
