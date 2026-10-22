# plugins-chad-market

Caja de herramientas para un agente en **OpenCode** (modelos locales o remotos). La idea: si el agente necesita algo, lo busca acá; si está, lo toma; si no está, lo arma desde un plano de este mismo repo.

| Tipo | Qué es | Cuántas |
|---|---|---|
| `plugin` | skills y comandos listos para instalar | 4 |
| `app` | herramienta externa (MCP, librería, CLI) con una receta paso a paso | 4 |
| plano | esqueletos para armar skills, comandos, subagentes, tools y MCP | `blueprints/` |

Todo está en [`catalog.json`](catalog.json), con tags por capacidad y un nivel de verificación honesto (`executed`, `discovery` o `docs`).

## Plugins
| Plugin | Qué hace |
|---|---|
| `lean-code` | Escribir el mínimo código que resuelve el problema (`/lean`, `/lean-audit`) |
| `graph-explorer` | Grafo de conocimiento de un repo, local (`/graph-build`, `/graph-query`) |
| `harness-creator` | Armar y auditar el harness de un agente de código |
| `fast-grep` | Búsqueda de texto/regex indexada, hasta 50x más rápida que grep (`/tgrep-index`) |

## Apps
`rea` (ingeniería inversa por MCP), `cocoindex` (indexado incremental para RAG), `kittentts` (texto a voz local), `open-code-review` (code review con IA y plugin nativo para OpenCode). Cada una tiene su receta en `apps/<nombre>/recipe.json`.

## Instalar un plugin
Requiere Python 3 (solo stdlib).

```bash
python install.py all --project /ruta/a/tu/proyecto     # o --global
opencode debug skill                                    # verificar
```

Cómo tomar una app, cómo armar lo que falta y las reglas del repo: [`AGENTS.md`](AGENTS.md) y [`blueprints/BUILDING.md`](blueprints/BUILDING.md). Lo que está bloqueado por ahora vive en [`backlog.json`](backlog.json).

## Probado con
OpenCode 1.18.33 en Windows: instalación limpia e idempotente de los 4 plugins, y descubrimiento por `opencode debug skill` / `opencode debug config`. `fast-grep` y `harness-creator` se ejecutaron de punta a punta. Las recetas de apps están armadas desde la documentación de cada proyecto y no se ejecutaron.
