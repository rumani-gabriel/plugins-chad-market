# Aislar lo que ejecuta un agente (sandbox)

- Tipo: criterio
- Revisada: 2026-11-16
- Estado: vigente
- Relacionadas: `simulacro-sin-nube`, `mcp-servidor-y-skills`; `apps/opensandbox`; `apps/pi`; `apps/concat`

## En una línea
Un agente que ejecuta comandos y código generado por un modelo necesita una frontera que no dependa de que el modelo se porte bien. Hay cuatro niveles de aislamiento y la receta `apps/opensandbox` cubre los dos más accesibles; en una máquina Windows con Docker solo se alcanza el más débil, y eso hay que saberlo.

## Qué sabemos (verificado, con fuente)
**OpenSandbox** (`alibaba/OpenSandbox`, ahora en `opensandbox-group/OpenSandbox`; API de GitHub y PyPI, 2026-11-16): 17.351 estrellas, 1.655 forks, licencia Apache-2.0, creado el 2025-12-17, versión estable 1.2.1 (2026-11-13) y una 1.3.0-rc.1 de hoy. Es una API de ciclo de vida para crear entornos aislados donde un agente ejecuta comandos, maneja archivos y opera navegadores o escritorios. Se usa con Docker en local o con Kubernetes. Trae SDK en Python, Java/Kotlin, TypeScript, C# y Go, una CLI (`osb`) y un servidor MCP (`opensandbox-mcp`) con herramientas para crear, conectar y matar sandboxes, ejecutar comandos y manejar archivos de texto. Sus ejemplos incluyen correr **OpenCode, Claude Code, Codex CLI y Gemini CLI dentro de un sandbox**.

Niveles de aislamiento (según su guía de runtimes seguros):

| Nivel | Qué lo aísla | Dónde se puede usar |
|---|---|---|
| Sin aislamiento | nada: el agente corre en tu cuenta | cualquier lado (es el caso de Pi y OpenCode sin sandbox) |
| Contenedor común (runc, el valor por defecto) | procesos y cgroups; comparte el núcleo con el anfitrión | Docker, incluido Docker en Windows; la guía lo recomienda para «cargas de confianza y desarrollo local» |
| gVisor | núcleo en espacio de usuario que intercepta llamadas al sistema | Docker en un anfitrión **Linux** con `runsc` instalado |
| Kata (QEMU, Firecracker, Cloud Hypervisor) | una microVM por sandbox, con núcleo propio | anfitrión Linux con el runtime instalado (Docker o Kubernetes); requiere virtualización |

- **Red:** cada sandbox puede llevar una política de salida (`egress`): por defecto se puede negar todo y permitir solo dominios concretos; se aplica dentro del sandbox, con una capa de DNS y, en el modo `dns+nft`, reglas del filtro de paquetes. Límite documentado: solo TCP (no UDP). La guía de seguridad de red está escrita para administradores de clústeres de Kubernetes.
- **Credenciales (Credential Vault):** las claves reales quedan en el proceso lateral de salida y el sandbox solo ve valores falsos; exige el modo `dns+nft` y una política con negar por defecto.
- **Acceso entrante autenticado (`secureAccess`):** solo existe en Kubernetes; Docker lo rechaza.

## Lo que dicen pero no verificamos
- «Crea sandboxes con Firecracker en 64 ms»: cifra del propio proyecto (P50 en serie, 125,4 ms P99 con 10 en paralelo), de su runtime de Kubernetes; no aplica a Docker en tu máquina.
- «Ejecuta de forma aislada y protege claves»: depende del nivel que se configure. Con el contenedor común la frontera es la de un contenedor Docker, no la de una máquina virtual.
- No verifiqué si la política de salida con `dns+nft` funciona en Docker Desktop sobre Windows ni si hace falta alguna capacidad especial del contenedor.

## Cómo usarlo
1. **Decidir qué se aísla.** Dos formas: (a) **correr el arnés completo dentro del sandbox** (hay un ejemplo oficial con OpenCode): lo más seguro, pero el modelo local tiene que ser alcanzable desde el contenedor; (b) **darle al agente una herramienta MCP que ejecuta dentro del sandbox** y quitarle la ejecución de comandos en el anfitrión: menos aislamiento total, mucho más fácil de adoptar.
2. **En Windows con Docker Desktop el aislamiento es el de un contenedor común.** Es un avance frente a ejecutar en tu cuenta, pero no una frontera fuerte contra código hostil. Para algo hostil (malware, un modelo sin censura, pruebas ofensivas) usar una máquina virtual descartable o un anfitrión Linux con gVisor o Kata.
3. **Red cerrada por defecto:** crear los sandboxes con la política de negar todo y abrir solo lo que la tarea necesita (por ejemplo el registro de paquetes). Sin salida a internet el agente no puede filtrar datos.
4. **Nada de claves reales dentro del sandbox**; usar Credential Vault solo si se cumplen sus requisitos, o no darle credenciales.
5. **Fijar la versión** de los paquetes y de las imágenes (la guía del propio proyecto pide fijar por digest y avisa que la firma de sus lanzamientos agrupados todavía está en seguimiento).
6. **Medir el costo:** tiempo de creación en esta máquina y cuánta RAM y VRAM deja libres para el modelo.

7. **Ocultar una herramienta no es denegarla.** Omnigraph (fuente: notas de cambios de su version 0.15, 2026-11-09) tenia un flag que escondia las herramientas MCP de escritura mientras la misma credencial podia escribir por HTTP; lo quitaron y ahora decide solo la politica Cedar del lado del servidor. Criterio para el lab: el permiso se aplica donde esta el dato (politica de la credencial), no en la lista de herramientas que ve el modelo; al actualizar una herramienta con permisos, comparar lo que cada agente podia hacer antes y despues.

8. **Claves fuera del sandbox: evita el robo, no el uso indebido.** Agent Substrate (Apache-2.0, 8 mil estrellas, versión 1.0.1; README y guía de seguridad leídos el 2026-11-20) y el Credential Vault de OpenSandbox hacen lo mismo: la clave real vive en una puerta de salida que la agrega a las peticiones permitidas, y el sandbox nunca la ve ni queda en una instantánea. Eso impide filtrarla, pero un agente con una inyección de prompt puede pedirle a esa puerta que use la clave contra un destino permitido; las reglas de salida suelen distinguir solo servidor y puerto. La capa que falta es una política más fina (qué ruta, qué método) o una compuerta de decisión antes de la llamada (ver `modelos-de-decision`). Agent Substrate en sí exige Kubernetes y no sirve para una sola máquina Windows: queda en `referencia.json`.
9. **Separar quién decide de dónde se ejecuta.** Google AX (`referencia.json`: `google-ax`) es el plano de control que corre *arriba* de Agent Substrate: declara qué tarea corre, con qué modelo y qué permiso de red, y delega todo el aislamiento real al runtime de abajo. Los dos proyectos se describen a sí mismos como «ortogonales». Es el mismo principio que separar `apps/pi` (qué modelo atiende cada tarea) de `apps/opensandbox` (dónde se ejecuta lo que ese modelo pide), aunque a una escala mucho menor: ninguna herramienta del lab necesita reinventar un plano de control de Kubernetes para aplicar la idea.
