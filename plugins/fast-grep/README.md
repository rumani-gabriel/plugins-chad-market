# fast-grep

Búsqueda de texto/regex acelerada en repos grandes, sobre el motor open-source [tgrep](https://github.com/microsoft/tgrep) (Microsoft, MIT) — indexado por trigramas, hasta **50x más rápido que grep/ripgrep** en codebases masivos. GitHub Copilot CLI ya lo usa internamente.

## Qué hace
- Indexa una vez (`/tgrep-index`), busca al instante después — misma sintaxis de patrones que grep/ripgrep.
- 100% local: sin red, sin API key, sin telemetría. El único tráfico de red es la descarga única del binario.
- No reemplaza a `graph-explorer` (ese entiende relaciones semánticas del código) — son complementarios.

## Cómo se resuelve el binario (y por qué es seguro)
`tgrep` es un binario nativo (Rust), no un paquete de Python. `tools/ensure_tgrep.py` lo resuelve en este orden:
1. Si ya está en el PATH (instalación propia), se usa tal cual.
2. Si no, se busca en un cache persistente (`~/.cache/tgrep/<versión>/`).
3. Si no está en ningún lado, se descarga el asset correcto para tu SO/arquitectura desde el release oficial de GitHub (`microsoft/tgrep`), **se verifica su SHA256 antes de extraer o ejecutar nada** — si no coincide, aborta sin tocar el binario.

Los 4 assets de Linux/macOS traen checksum publicado por el proyecto (`checksums.txt` del release); los 2 de Windows no — se calcularon a mano una vez y quedaron pineados en el propio script. Versión pineada (1.0.10), no se auto-actualiza sola.

## Uso
```
/tgrep-index [ruta]   # construye/actualiza el índice
```
Para buscar, invocá `tgrep` directo vía Bash (ver skill `fast-grep`) una vez que hay índice construido.

## Requisitos
Python (solo stdlib, sin dependencias de terceros) para resolver/verificar el binario. Sin red salvo la descarga única inicial.
