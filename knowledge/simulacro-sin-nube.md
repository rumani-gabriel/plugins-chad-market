# Simulacro sin nube: cuánto puede hacer el agente local sin internet

- Tipo: guía
- Revisada: 2026-11-16
- Estado: vigente (propuesta, sin ejecutar)
- Relacionadas: `servir-modelos-locales`, `modelos-flash-engram`, `contexto-en-agentes`; `apps/llama-cpp`, `apps/pi`, `models.json`

## En una línea
Una prueba simple y repetible: levantar el modelo local y un agente, cortar la conexión y anotar qué tareas siguen funcionando. Sirve para saber con datos cuánto del trabajo depende de la nube y qué falta en el laboratorio.

## Qué sabemos (verificado, con fuente)
- La idea sale de un post que propone el mismo stack que este repo: llama.cpp (cualquier hardware, hasta carga desde SSD), un modelo cuantizado que entre en la máquina, el agente Pi con herramientas y conocimiento locales, y luego apagar internet para ver qué queda. Ese stack ya está armado en `apps/llama-cpp` y `apps/pi` (recetas sin ejecutar).
- Un comentario del post señala el riesgo que importa: Pi trae por defecto herramientas de ejecución de comandos y no pide aprobación; darle esos permisos a un modelo local flojo es arriesgado. Por eso el simulacro va en una carpeta de prueba (ver la precaución de `apps/pi`).

## Lo que dicen pero no verificamos
- «Si apagás internet, tu IA sigue haciendo mucho»: depende del modelo y de las tareas. El dato de un comentario (9 de 30 tareas de repositorio con un Flash alojado contra 16 de Claude Sonnet 5.5, medido por un proveedor de enrutamiento) apunta a que un modelo local rendirá menos que eso; sin medición propia no sabemos cuánto.

## Cómo usarlo
1. **Preparar con internet:** modelo y servidor (`apps/llama-cpp`), el agente (`apps/pi` u OpenCode) y lo que el agente necesita a mano: documentación guardada, el repositorio de prueba, las dependencias ya instaladas.
2. **Elegir 6 tareas reales y chicas:** leer y resumir un archivo, editar una función, escribir una prueba, correr un comando y arreglar el error, buscar algo en el repositorio, responder una duda sobre una librería con su documentación local.
3. **Cortar la conexión** (modo avión o desconectar la red) y correr las 6 tareas con el modelo local.
4. **Anotar por tarea:** terminada sin ayuda sí o no, llamadas a herramientas fallidas, tokens por segundo, cuánto contexto se llenó y qué faltó (una descarga, una búsqueda web, un paquete).
5. **Repetir con otro modelo** (por ejemplo Qwen3.6-35B-A3B contra Qwen3-Coder-Next) y guardar la tabla en la nota del modelo en `models.json`.
6. Lo que falló por falta de internet es la lista de lo que hay que traer al laboratorio: documentación, paquetes en caché, un índice local.
