# lean-code

Skill y comandos para que el agente escriba el **mínimo código** que resuelve el problema, como un ingeniero senior que evita trabajo innecesario. Menos código generado: menos tokens, menos superficie de bugs.

## La escalera de decisión
Antes de escribir código, el agente baja por estos peldaños y frena en el primero que ya resuelve la tarea:

1. **YAGNI**: ¿hace falta construirlo?
2. **Reusar**: ¿ya existe en el codebase?
3. **Librería estándar**: ¿lo hace la stdlib?
4. **Feature nativa**: ¿lo cubre la plataforma?
5. **Dependencia ya instalada**: ¿algo que ya está en el proyecto?
6. **Una línea**: ¿se puede resolver en una?
7. **Último recurso**: el mínimo código que funcione.

Prefiere borrar a agregar, lo aburrido a lo ingenioso y el diff más corto. Lo que **nunca** recorta: entender el problema, validar inputs, manejar errores, seguridad y accesibilidad.

## Qué incluye
- Skill `lean-code`: el modelo la carga cuando va a escribir o modificar código.
- `/lean <tarea>`: fuerza el modo minimalista sobre una tarea puntual.
- `/lean-audit [--staged] [--diff <ref>] [<path>]`: audita código ya escrito contra la escalera. Solo lectura, no aplica cambios.

## Requisitos
Ninguno. Sin red y sin API keys. `git` solo para `/lean-audit` sobre diffs.

## Créditos
Inspirado en el enfoque de [Ponytail](https://github.com/DietrichGebert/ponytail) (MIT). Redacción propia.
