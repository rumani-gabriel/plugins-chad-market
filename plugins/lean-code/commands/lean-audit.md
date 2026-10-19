---
description: Audita código YA escrito (diff local, un commit, o un path) contra la escalera lean — señala abstracciones especulativas, lógica duplicada, dependencias evitables y boilerplate. Solo lectura. Útil para revisar el trabajo de alguien que no usó el hook. Uso: /lean-audit [--staged] [--diff <ref>] [<path>]
argument-hint: [--staged] [--diff <ref>] [<path>]
---

Activá la skill `lean-code`. Acción: auditoría retroactiva (no vas a escribir código, solo a revisarlo).

## Resolver el alcance

- **`--staged`**: `git diff --staged`.
- **`--diff <ref>`**: `git diff <ref>` (ej. `--diff main`, `--diff HEAD~3`).
- **`<path>`**: si se pasó un archivo o carpeta sin flags de diff, leé ese contenido directo (no hay diff de git de referencia).
- **Sin nada**: `git diff` (working tree vs. último commit). Si no hay repo git o el diff está vacío, avisá y no sigas.

## Qué revisar en cada bloque de código nuevo/modificado

Recorré la [escalera de decisión](../skills/lean-code/SKILL.md) al revés de cómo se escribe: para cada pieza de lógica agregada, preguntate si un peldaño anterior ya la resolvía.

- **YAGNI**: ¿hay código para un caso que no se pidió ni existe hoy (parámetros sin uso, flags "por si mañana", capas de más)?
- **Reuso**: ¿duplica una función/util que ya existe en el codebase? (buscá antes de asumir que no existe)
- **Librería estándar / dependencia ya instalada**: ¿reimplementa algo que la stdlib o una dependencia ya presente en el proyecto ya resuelve?
- **Boilerplate**: getters/setters vacíos, wrappers sin valor agregado, archivos de más para algo chico.
- **Diff innecesariamente largo**: ¿la misma tarea se resolvía con menos líneas sin perder claridad?

**No marques como hallazgo** nada que sea validación de inputs, manejo de errores, seguridad, o algo que el usuario pidió explícito — eso nunca se recorta y no es "exceso".

## Reporte

```markdown
# Auditoría lean — <alcance: staged | diff <ref> | <path> | working tree>
Archivos revisados: N · Hallazgos: N

## Hallazgos
### 🟠 Evitable (recortaría código sin perder funcionalidad)
- `archivo:línea` — <qué está de más> → <peldaño de la escalera que ya lo resolvía> — sugerencia: <diff mínimo>

### 🟡 Mejorable (no urgente, pero es más código del necesario)
- ...

## Sin hallazgos en
- <archivos que ya están lean>
```

Si no hay hallazgos, decilo directo — no inventes hallazgos menores para llenar el reporte.

**No apliques cambios.** Esto es solo lectura. Si el usuario pide *"aplicá las simplificaciones"*, recién ahí editá, archivo por archivo, mostrando el diff.
