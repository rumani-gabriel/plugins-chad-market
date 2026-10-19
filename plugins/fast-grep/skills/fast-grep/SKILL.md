---
name: fast-grep
description: Búsqueda de texto/regex acelerada en repos grandes, sobre el motor open-source tgrep (Microsoft, MIT) indexado por trigramas -- hasta 50x más rápido que grep/ripgrep en codebases masivos. Activá esta skill cuando el usuario pida buscar un patrón/string en un repo grande, o cuando ya exista un índice (.tgrep/) construido.
---

# fast-grep (búsqueda indexada, local y verificada)

Usa el motor open-source **[tgrep](https://github.com/microsoft/tgrep)** (Microsoft, MIT) para acelerar búsquedas de texto/regex en el repo actual. No reemplaza a `graph-explorer` (ese entiende relaciones semánticas del código — qué llama a qué); `tgrep` solo acelera la búsqueda de un patrón literal o una regex, sin entender nada del código.

## Qué NO hace (a diferencia de grep normal)

- No necesita red ni API key — 100% local, binario nativo.
- No manda telemetría.
- No requiere un servidor corriendo: opera directo sobre el índice en disco (`.tgrep/`).

## 1. Construir el índice (una vez, o cuando el código cambió mucho)

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" index "<ruta>"
```

La primera invocación en la máquina descarga el binario (versión pineada,
verificado por SHA256 contra el release oficial — ver `tools/ensure_tgrep.py`)
a `~/.cache/tgrep/`, persistente entre proyectos y updates del plugin.
Las siguientes invocaciones usan el binario cacheado, sin descargar de nuevo.

## 2. Buscar

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" "<patrón-regex>" "<ruta>"        # búsqueda básica
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" -F "<string literal>" "<ruta>"   # literal, sin regex
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" "<patrón>" "<ruta>" -l           # solo nombres de archivo
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" "<patrón>" "<ruta>" -c           # conteo por archivo
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" "<patrón>" "<ruta>" -A 3 -B 2    # contexto
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" "<patrón>" "<ruta>" --json       # salida JSON (compatible ripgrep)
```

Mismos flags y sintaxis de patrones que grep/ripgrep — no hace falta
aprender nada nuevo.

## Cuándo preferirlo sobre grep/Grep nativo

Si ya existe `.tgrep/` en el repo (índice construido), preferí `tgrep` sobre
`grep`/`rg`/`findstr` para cualquier búsqueda de texto/regex, especialmente
en repos grandes. Si es una búsqueda única y puntual que no vale la pena
indexar, seguí con grep normal.

Si no existe índice todavía, corré `/tgrep-index` primero, o seguí con grep
normal si es una búsqueda única y no vale la pena indexar.

## Relación con graph-explorer

Son complementarios, no se pisan:
- **`graph-explorer`**: "¿qué conecta con qué?", arquitectura, dependencias — entiende el código.
- **`fast-grep`**: "¿dónde aparece este string/patrón?" — no entiende nada, solo busca rápido.

Si el repo tiene ambos índices construidos, para preguntas de arquitectura
andá al grafo (`/graph-query`); para un string/patrón puntual, a `tgrep`.
