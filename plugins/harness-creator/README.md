# harness-creator

Skill para construir, auditar y mejorar el "harness" que rodea a un agente de código: archivo de instrucciones (`AGENTS.md`/`CLAUDE.md`), seguimiento de estado/features, comandos de verificación, límites de alcance y traspaso de sesión. Útil cuando un agente olvida contexto entre sesiones, se sale de alcance, o dice "listo" antes de que pasen los tests.

## Qué incluye
- `skills/harness-creator/SKILL.md`: el modelo de 5 subsistemas (instrucciones, estado, verificación, alcance, ciclo de vida) y cuándo usar cada script.
- `scripts/`: `create-harness.mjs` (arma un harness mínimo), `validate-harness.mjs` (lo audita y puntúa), `render-assessment-html.mjs` / `run-benchmark.mjs` (reporte). Solo Node.js core, sin dependencias de npm.
- `references/`: patrones de memoria persistente, multi-agente, registro de tools, context budget, bootstrap/lifecycle y gotchas conocidos.
- `templates/`: `agents.md`, `feature-list.json` (+ schema), `progress.md`, `session-handoff.md`, `init.sh`.

## Requisitos
Node.js (sin dependencias de npm — los scripts usan solo `node:fs`, `node:path`, `node:child_process`, `node:util`, `node:os`, `node:url`).

## Nota de empaquetado
Los scripts se autolocalizan (`import.meta.url`), así que funcionan igual instalados con `--project` o `--global`. El `SKILL.md` original traía la ruta de invocación hardcodeada a la estructura del curso (`skills/harness-creator/scripts/...`); acá se reemplazó por `${SKILL_ROOT}`, que `install.py` resuelve a la carpeta real donde quedó instalada la skill.

## Origen
Extraído de [`walkinglabs/learn-harness-engineering`](https://github.com/walkinglabs/learn-harness-engineering) (MIT), un curso de 14 lecciones sobre harness engineering. Solo se tomó la skill `harness-creator`, no el curso completo.
