# plugins-chad-market

Catálogo de plugins empaquetados para **OpenCode** (modelos locales o remotos). Cada plugin conserva su layout y se instala con un script de una línea; OpenCode descubre solo los skills y comandos.

Estado: piloto con 2 plugins.

| Plugin | Qué hace | Red / API keys |
|---|---|---|
| `lean-code` | Escribir el mínimo código que resuelve el problema (`/lean`, `/lean-audit`, skill `lean-code`) | No / No |
| `graph-explorer` | Grafo de conocimiento de un repo, local (`/graph-build`, `/graph-query`, skill `graph-explorer`) | Solo para instalar el motor / No |

## Instalar
Requiere Python 3 (solo stdlib).

```bash
python install.py all --project /ruta/a/tu/proyecto     # o --global
opencode debug skill                                    # verificar
```

Detalles, convenciones y cómo sumar un plugin: [`AGENTS.md`](AGENTS.md). Índice legible por máquina: [`catalog.json`](catalog.json).

## Probado con
OpenCode 1.18.33 en Windows: instalación limpia e idempotente, 2 skills y 4 comandos descubiertos por `opencode debug skill` / `opencode debug config`. La ejecución real de los comandos con un modelo no está probada todavía.
