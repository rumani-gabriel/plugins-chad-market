---
name: lean-code
description: Hace que escribas el MÍNIMO código que resuelve el problema, como un ingeniero senior que evita trabajo innecesario. Activá esta skill SIEMPRE que vayas a generar, escribir, agregar o modificar código — antes de tipear, bajá por la escalera de decisión y frená en el primer peldaño que ya resuelve la tarea. No aplica a seguridad, validación ni manejo de errores (esos nunca se recortan).
---

# Lean Code — escribí menos, resolvé igual

El mejor código es el que no escribiste. Los modelos saben **generar**; lo que cuesta es **contenerse**. Esta skill te da el instinto de un dev senior: la solución más corta y aburrida que resuelve el problema de verdad, no la más impresionante.

## La escalera de decisión

**Antes de escribir una sola línea**, bajá por estos peldaños en orden y **detenete en el primero que ya resuelve la tarea**:

1. **¿Hace falta? (YAGNI)** — ¿El problema realmente pide esto, o lo estás anticipando? Si no se pidió y no es necesario hoy, no lo construyas.
2. **¿Ya existe en este codebase?** — Buscá antes de crear. Reusá la función/clase/util que ya está en vez de duplicar lógica.
3. **¿Lo hace la librería estándar?** — stdlib del lenguaje antes que cualquier dependencia. (`itertools`, `pathlib`, `datetime`, `string.Template`, etc.)
4. **¿Hay una feature nativa de la plataforma?** — Algo que el framework/SO/DB ya ofrece (un constraint SQL, un built-in del runtime) gana a reimplementarlo.
5. **¿Lo resuelve una dependencia YA instalada?** — Si ya está en el proyecto, usala. **No** agregues una dependencia nueva si podés evitarlo.
6. **¿Se puede en una línea?** — Si llegaste hasta acá, buscá la expresión mínima antes de armar una estructura.
7. **Último recurso** — Escribí el **mínimo código que funcione**, una vez entendido el problema.

## Reglas duras

**Evitá (salvo que se pida explícito):**
- Abstracciones especulativas (capas, interfaces, "por si mañana…").
- Dependencias nuevas cuando hay alternativa con lo que ya tenés.
- Boilerplate innecesario (getters/setters vacíos, wrappers que no aportan).
- Archivos de más. Menos archivos, menos superficie.

**Preferí:**
- **Borrar antes que agregar.** Si podés resolver quitando código, ganaste.
- **Aburrido antes que clever.** Código obvio que cualquiera entiende.
- **El diff más corto** que resuelve el problema, después de entenderlo.
- Correcto en los edge cases por sobre elegante.

## No-negociables (acá NO se aplica la "pereza")

Recortar código **nunca** significa recortar en:
- **Entender el problema** antes de tocar nada.
- **Validación de inputs** en los límites de confianza.
- **Manejo de errores** que evita pérdida o corrupción de datos.
- **Seguridad** (inyección, secretos, autorización) — innegociable.
- **Accesibilidad** donde aplique.
- Cualquier cosa que el usuario **pidió explícitamente**, aunque sume código.

## Marcá las simplificaciones

Cuando elegís a propósito una solución mínima que tiene un techo conocido, dejá un comentario corto con el límite, así el que venga sabe:

```python
# lean: O(n) en memoria; alcanza para < 10k filas. Si crece, paginar.
```

## Cómo entregar

- Mostrá **qué peldaño** usaste y **qué evitaste** ("no agregué `pandas`, lo resolví con `csv` de stdlib").
- Si el pedido implicaba más código del necesario, **proponé la versión mínima primero** y ofrecé la completa solo si el usuario la quiere.
- Si estás por crear algo grande, pará y preguntá **por qué** antes de construirlo.
