---
description: Activa el modo minimalista — escribí el mínimo código que resuelve el problema (escalera de decisión estilo dev senior).
---

Activá la skill `lean-code` y aplicá el modo minimalista a lo que sigue: **$ARGUMENTS**

Antes de escribir código, bajá por la escalera de decisión y frená en el primer peldaño que resuelve la tarea:

1. YAGNI — ¿hace falta?
2. ¿Ya existe en el codebase?
3. ¿Lo hace la librería estándar?
4. ¿Feature nativa de la plataforma?
5. ¿Dependencia ya instalada?
6. ¿Una línea?
7. Último recurso: mínimo código que funcione.

Entregá el **diff más corto** que resuelve el problema y contá qué evitaste. **No recortes** en validación, manejo de errores, seguridad ni en lo que el usuario pidió explícito.

Si no se pasó nada en `$ARGUMENTS`, aplicá este criterio al pedido actual de la conversación.
