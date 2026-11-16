# Concat: copia del código fuente (vendor/concat)

La carpeta `vendor/concat/` es una **copia exacta, sin modificar**, del código fuente de Concat, un editor de video local que un agente puede manejar por MCP. Receta de uso: `apps/concat/recipe.json`.

| | |
|---|---|
| Proyecto | Concat, de Jareer Abdullah (`jub0t`) |
| Origen | https://github.com/jub0t/Concat |
| Versión | `v0.2.11` (2026-11-13), beta |
| Commit | `6584d34971ae5e168f12cb475bdf58055b67d780` (2026-11-12) |
| Copiada el | 2026-11-16, con `git archive` de ese commit (sin el historial de git) |
| Licencia | **AGPL-3.0-or-later** (archivo `vendor/concat/LICENSE`). Existe también una licencia comercial aparte, ver `vendor/concat/LICENSING.md` |
| Tamaño | 1.348 archivos, unos 53 MB; no incluye instaladores ni modelos |

## Qué no está copiado
- **Los instaladores** (Windows, macOS, Linux, Android): se bajan de la página oficial de releases, con el hash SHA-256 que figura en `apps/concat/recipe.json`.
- **Los modelos** de subtítulos, voz y recorte de fondo (más de 1 GB): el programa no los trae; se bajan la primera vez que una función los pide. Su lista con el hash de cada uno está en `vendor/concat/models/manifest.toml`.

## Condiciones de la licencia que hay que respetar
- Se conservan el `LICENSE`, `LICENSING.md`, `THIRD_PARTY_NOTICES.md` y los avisos de derechos de autor de cada archivo. **No se editan archivos de `vendor/concat/`.** Si hace falta un cambio, se hace en una copia aparte y se declara qué se cambió y cuándo (AGPL, sección 5).
- Quien distribuya Concat, o una obra basada en él, o deje usar una versión modificada por red, debe ofrecer su código fuente completo bajo la misma licencia. Usarlo en una máquina propia, sin modificar ni distribuir, no activa esa obligación.
- La licencia no concede derechos sobre las patentes de los formatos multimedia (H.264, HEVC, AV1): leer la sección «Codec patents» de `LICENSING.md`.
- La carpeta `vendor/concat/.claude/` es configuración de desarrollo del autor (una skill para compilar el proyecto, con rutas de su máquina). No se aplica a este laboratorio y no hay que cargarla.
- Los nombres y logos de Concat tienen su propia política: `vendor/concat/TRADEMARK.md`.

## Aclaración
La licencia de los archivos de `vendor/` es la de su autor, no la del resto de este repositorio. Los escaneos de este repositorio buscan datos propios; los textos de terceros dentro de `vendor/` (por ejemplo, enlaces a sitios de otros proyectos en sus avisos) no son datos nuestros.
