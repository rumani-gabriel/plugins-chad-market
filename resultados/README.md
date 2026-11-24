# resultados/ — lo que se midió en el laboratorio

Acá van las notas de las pruebas hechas en la máquina del laboratorio. Una nota por prueba, con nombre `AAAA-MM-DD-<tema>.md`. Mientras no haya notas, **nada de lo investigado está probado**: las cifras de los proyectos son de sus autores.

## Plantilla

```markdown
# <Tema de la prueba>

- Fecha: AAAA-MM-DD
- Entrada probada: <nombre en backlog.json, models.json o apps/>
- Máquina: <GPU, RAM, sistema operativo>
- Modelo y configuración: <modelo, cuantización, contexto, arnés (OpenCode o Pi), versión>
- Veredicto: sirve | sirve en parte | no sirve

## Qué se hizo
<tareas concretas y cuántas veces se repitieron>

## Qué se midió
| Medida | Sin la herramienta | Con la herramienta |
|---|---|---|
| Tokens totales por tarea terminada | | |
| Pasos o vueltas | | |
| Tiempo | | |
| Aciertos | | |

## Qué falló o sorprendió
<errores, límites, cosas que el README no decía>

## Qué hay que cambiar en el repo
<entrada que pasa a ejecutada, se mueve a referencia.json o se corrige>
```

## Reglas
- Si no se pudo medir algo, dejar la celda vacía y decirlo: no estimar.
- Anotar versión exacta de lo probado y fecha.
- Sin nombres de empresas, usuarios ni datos de trabajo.
