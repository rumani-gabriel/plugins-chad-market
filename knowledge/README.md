# Baúl de conocimiento

Notas con estrategias, criterios y hallazgos que **no son una herramienta** (esas van en `plugins/`, `apps/` o `blueprints/`) pero conviene tener a mano: cómo gestionar el contexto de un agente, cómo evaluar un buscador para agentes, estrategias de RAG, etc.

Si sos un agente: leé `INDEX.json`, elegí las notas por `tags` y leé solo esas. No cargues todo el baúl en el contexto.

## Formato de una nota
Archivo `knowledge/<id>.md`, con un encabezado fijo y secciones cortas:

```text
# Título
- Tipo: estrategia | criterio | referencia | guía
- Revisada: AAAA-MM-DD
- Estado: vigente | a revisar | superada
- Relacionadas: ids de otras notas, y entradas de catalog.json o backlog.json

## En una línea
## Qué sabemos (verificado, con fuente)
## Lo que dicen pero no verificamos
## Cómo usarlo
```

## Reglas
- **Separar lo verificado de lo que afirma el autor.** Una cifra de un proveedor sobre su propio producto va en «Lo que dicen pero no verificamos».
- **Con fecha.** Los datos de estrellas, precios, versiones y rankings cambian: cada nota lleva su fecha de revisión.
- **Sin datos de ninguna organización**: ni correos, ni URLs internas, ni nombres de equipos o clientes.
- **Una nota por tema.** Si un hallazgo cambia una nota existente, se edita esa nota y se sube su fecha; no se duplica.
- Si una nota termina en una herramienta que se puede tomar, enlazarla desde `Relacionadas` (receta en `apps/`, plugin o entrada del backlog).
