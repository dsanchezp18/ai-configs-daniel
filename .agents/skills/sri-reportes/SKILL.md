---
name: sri-reportes
description: Completar las descargas de mcp-sri-descargas, verificar los pares XML/PDF contra el TXT del SRI y generar los reportes locales de facturas y retenciones en Excel con el formato de XML_Manager. Usar para estos entregables mensuales; no modifica conexiones ni configura el MCP.
---

# Reportes mensuales del SRI

El MCP descarga. Esta skill verifica los archivos y genera Excel localmente. Usa los
scripts incluidos: no reescribas el cálculo en cada corrida ni ejecutes las macros de
XML_Manager. El alcance actual es facturas y retenciones, recibidas o emitidas.

## 1. Confirmar el alcance

Identifica la carpeta de la empresa, RUC, año, mes, dirección y tipos solicitados.
Si la persona pidió completar un mes en la conversación, conserva ese alcance.
Nunca muestres credenciales. El MCP lee el `.env`; el generador no lo necesita.
Lee el `AGENTS.md` actual de mcp-sri-descargas antes de consultar el portal.

## 2. Completar los archivos con el MCP

Usa `descargar_reporte` primero para cada tipo solicitado. Luego `descargar_mes`,
con `pdf="local"`, si hay faltantes. Una descarga por RUC a la vez. Si las herramientas
no están expuestas, llama al mismo servidor por un cliente MCP stdio, como indica
su AGENTS.md. Mantén la conexión, el perfil y las opciones de Chrome existentes.

Ante un error, espera que termine la llamada y reintenta sin pedir confirmación:
30 segundos, luego 60 y después pausas más largas. **Ante `Captcha incorrecta`,
deja el portal sin consultas 10 minutos y prueba una sola vez `descargar_reporte`.**
Si vuelve a fallar, aumenta la pausa y revisa el diagnóstico antes de la siguiente
prueba. No consultes otro mes o tipo durante la pausa. Conserva los 30 segundos que
el MCP espera antes de cada consulta.

Tres fallos no son una razón suficiente para terminar. Evalúa cada resultado y
conserva lo descargado. No programes un bucle de reintentos ilimitado. Si aparece
un CAPTCHA visible, avisa y espera que la persona lo resuelva; no lo resuelvas ni
lo evadas. Detente ante credenciales rechazadas, `.env` faltante, bloqueo anunciado
por el portal, perfil usado por otro proceso o un fallo reproducible que impida
avanzar. Explica la evidencia. `bloqueado: true` por sí solo no prueba un bloqueo
del SRI. La extensión está reemplazada: no la uses. No uses descargas antiguas ni
importaciones para sustituir una descarga pendiente del MCP. Solo importa archivos
cuando la persona los suministra y pide expresamente importarlos.

Un tipo está completo cuando las claves únicas de su TXT tienen el XML descargado y
PDF válido, no quedan faltantes ni errores sin explicar y la última respuesta no
trae `bloqueado: true`. Verifica los archivos, no solo los contadores de la respuesta.
Si el portal confirmó cero comprobantes pero no dejó un TXT, documenta ese resultado;
el generador necesita un TXT con encabezados para producir una tabla vacía.

## 3. Generar los reportes locales

Si el mes ya está completo y verificado, no consultes otra vez el portal para hacer Excel.
Para referencias suministradas expresamente por la persona, también puedes probar
el generador sin abrir el MCP. Usa una carpeta nueva de salida fuera de los repositorios.
El generador comprueba estructura y correspondencia de archivos. No verifica firmas
digitales, identidad del emisor ni autorización del SRI. Dilo al entregar los reportes;
no presentes la etiqueta `AUTORIZADO` o una clave coincidente como prueba de autenticidad.
Para XML suministrados expresamente, añade `--desde-xml`: incluye todos los pares del
tipo, RUC y mes, y avisa que no comprueba cobertura del TXT ni del portal. Este modo
no autoriza reutilizar archivos antiguos para sustituir una descarga solicitada.

En Codex, localiza Python y Node con `load_workspace_dependencies`. El script utiliza
el runtime de documentos de Codex; no instala paquetes. Antes de crear los Excel,
aplica la skill de spreadsheets disponible, incluido su registro de inicio de operación.
En otras sesiones, esos mismos ejecutables locales funcionan si el runtime está instalado.

```powershell
# Cambia las rutas y el alcance por los de la empresa y mes solicitados.
$skill_dir = Join-Path $HOME '.codex\skills\sri-reportes'
$runtime_dir = Join-Path $HOME '.cache\codex-runtimes\codex-primary-runtime\dependencies'
& "$runtime_dir\python\python.exe" "$skill_dir\scripts\generar_reportes.py" `
  --carpeta-mes 'C:\carpeta-de-la-empresa\09 Septiembre' `
  --anio 2026 --mes 9 --ruc '<RUC>' --direccion recibidos `
  --tipos facturas retenciones --salida 'C:\entregables\2026-09' `
  --runtime $runtime_dir
```

Para solo facturas, usa `--tipos facturas`. En Claude, cambia la raíz de la skill a
`~/.claude/skills/sri-reportes`. El script lee exclusivamente las carpetas de los tipos
solicitados bajo la carpeta mensual. No busca archivos por todo Downloads.

Los archivos finales son `Reporte facturas.xlsx` y `Reporte retenciones.xlsx`, cada
uno con la hoja `XML_Reporte`. Sus columnas conservan el orden y los nombres de los
ejemplos. También se generan vistas PNG para revisar identificación e importes.
No reemplaza un Excel existente: elige otra carpeta para una nueva corrida.

## 4. Verificar y entregar

Reabre los Excel con una herramienta de lectura. Compara encabezados, claves y
cantidades con los XML/TXT; una retención puede aportar varias filas. Compara los
importes con los campos XML, mantén las claves y ceros iniciales como texto y mira
las vistas PNG. No declares equivalencia por haber creado el archivo.

Entrega los dos Excel solicitados y la ruta de los XML/PDF. Informa número de
comprobantes, filas y cualquier limitación concreta. No entregues un reporte parcial
como completo. Lee [la guía de campos y cálculo](references/campos.md) cuando debas
explicar los importes, interpretar `varios` o revisar un XML distinto a los ejemplos.
