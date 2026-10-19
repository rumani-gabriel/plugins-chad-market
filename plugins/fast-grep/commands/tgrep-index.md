---
description: Construye o actualiza el índice de tgrep para búsquedas de texto/regex instantáneas. Uso: /tgrep-index [ruta]
---

Construí/actualizá el índice de **$ARGUMENTS** (si no se pasa ruta, usá `.`).

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/run-tgrep" index "${ARGUMENTS:-.}"
```

La primera vez que se corre esto en la máquina, descarga el binario de
`tgrep` (versión pineada, verificada por SHA256 contra el release oficial
de `microsoft/tgrep`) a un cache persistente (`~/.cache/tgrep/`) — no
hace falta reinstalar por proyecto ni por plugin actualizado.

El índice queda en `<ruta>/.tgrep/` (formato binario propio de tgrep,
regenerable). Sumalo a tu `.gitignore` si no está ya — no tiene sentido
versionarlo.

No vuelvas a correr esto en cada búsqueda: solo hace falta reconstruir el
índice cuando el código cambió significativamente desde la última vez. Para
buscar, invocá `tgrep` directo (ver skill `fast-grep`).
