---
name: r-investigacion-clara
description: Escribir, reproducir, adaptar o modificar análisis de investigación en R con tidyverse, scripts lineales y código fácil de leer. Usar para procesar datos, construir indicadores, estimar resultados, replicar tablas o figuras y trabajar con encuestas complejas cuando se solicite código R claro y sin sobreingeniería.
---

# Investigación clara en R

Escribir código de investigación que un colega pueda leer, ejecutar y modificar sin depender de un asistente. Mostrar los cálculos en el orden en que ocurren. Aplicar las instrucciones del usuario y las convenciones específicas del proyecto cuando correspondan. No reemplazar la metodología por una versión más cómoda ni copiar errores de un script de referencia.

## Antes de escribir

1. Leer el encargo, las instrucciones del repositorio y los scripts cercanos pertinentes. Identificar qué se debe crear, modificar o reproducir.
2. Identificar insumos, unidad de observación, variables, población, transformaciones, estimador, salidas y dependencias. Para una réplica, localizar además el resultado de referencia y su metodología.
3. Consultar diccionarios y sintaxis oficiales cuando las definiciones o códigos no sean evidentes. No inventar ponderadores, denominadores ni tratamientos de valores ausentes.
4. Mantener el alcance solicitado. Si falta un dato esencial, avanzar con lo verificable y comunicar la limitación concreta; no fabricar resultados.

## Estructura y ejecución

Organizar cada script en una secuencia visible: paquetes y configuración; lectura; preparación y uniones; diseño muestral si corresponde; estimación; tablas y figuras; exportación. Omitir secciones que no se necesiten. Dividir un proyecto en varios scripts solo cuando los insumos, tiempos de ejecución o productos lo justifiquen, no por formalismo.

Usar encabezados breves y consistentes como `# Variables de ingreso`. Mantener juntas la selección de la población y la estimación correspondiente. Crear objetos intermedios cuando aclaren una transformación o permitan reutilizar un resultado, sin guardar cada paso trivial.

Usar rutas relativas a la raíz del proyecto y documentar los archivos de entrada y salida en un encabezado corto. No modificar datos crudos ni instalar paquetes automáticamente. Si la tarea requiere obtener datos, permitir una descarga reproducible desde una fuente identificada y guardarla en datos crudos conforme a las convenciones del proyecto. No incluir rutas personales. Cargar al comienzo solo los paquetes necesarios; usar `source()` únicamente para una dependencia real y hacer explícito qué aporta. Seguir la convención del proyecto para carpetas y paquetes.

## Estilo

- Priorizar `tidyverse`: `mutate()`, `case_when()`, `filter()`, `group_by()`, `summarise()`, `join` y `pivot_*()` cuando expresen el cálculo de forma clara.
- Usar `<-`, nombres descriptivos en `snake_case` y `TRUE`/`FALSE` completos. Conservar los nombres originales de variables y categorías cuando sea necesario para leer las fuentes o respetar contratos existentes.
- Se permite usar `janitor::clean_names()` para normalizar los nombres de columnas al leer datos; aplicarlo cuando la convención del proyecto lo requiera o facilite el análisis. Tener en cuenta los nombres resultantes en las referencias posteriores y conservar los códigos y etiquetas de las variables.
- En código nuevo usar español en nombres, comentarios y etiquetas, salvo que el usuario, la interfaz existente o el proyecto requieran otra convención. Usar la tubería nativa `|>`; seguir las instrucciones explícitas del proyecto o usuario si requieren otra.
- Aplicar una misma operación a varias columnas con `across()` cuando resulte más claro. Preferir operaciones vectorizadas a `rowwise()` si preservan la semántica. Separar cálculos largos en bloques legibles.
- Usar `is.na()` y `!is.na()` para detectar ausentes. No convertir ausentes, no respuesta o códigos especiales en cero sin respaldo en el diccionario. Usar `na.rm = TRUE` solo cuando esa exclusión sea metodológicamente apropiada.
- Identificar el tipo y la clave de cada unión. No usar `distinct()` o `slice(1)` para ocultar duplicados sin entender la unidad de análisis y explicar la elección.
- Escribir comentarios en español claros y naturales, salvo que el usuario indique otro idioma. Comentar la lógica de un bloque completo antes de su código: qué se busca calcular, qué población o unidad se utiliza y por qué se toman decisiones que afectan el resultado. Explicar códigos especiales y supuestos cuando haga falta. Un comentario debe ayudar a un colega a seguir el análisis sin leer cada instrucción por separado; no comentar línea por línea ni repetir nombres de funciones. Evitar prosa genérica, frases automáticas y explicaciones largas que oscurezcan el cálculo.

## Simplicidad frente a abstracción

No añadir clases, fábricas, marcos de configuración, registros, manifiestos, sistemas de alertas ni funciones que envuelvan una sola línea. No extraer una función solo para evitar repetir un bloque pequeño. Para pocos cálculos similares, mostrar cada uno de forma explícita si así se entienden mejor las diferencias de población o método. Crear una función con nombre cuando un bloque que varía en 1–3 parámetros se repita seis o más veces, conforme a las convenciones; usar `purrr::map()` cuando haga el flujo más claro. Dar nombres claros a entradas y salidas. No ocultar la definición de un indicador tras metaprogramación, `!!sym()` o selección dinámica innecesaria.

No añadir secciones de validación de entradas o resultados, aserciones, controles automáticos, infraestructura de pruebas, manifiestos ni rechazos automáticos no solicitados. Una comprobación ausente no es, por sí misma, un defecto. Si se considera necesaria una verificación adicional, explicarla en la conversación en lugar de incorporarla al script; agregarla solo cuando el usuario la solicite. Mantener las comprobaciones existentes que formen parte del análisis, salvo instrucción o necesidad concreta de modificarlas. No introducir silenciosamente `tryCatch()` o valores predeterminados que oculten fallos.

## Encuestas y estimaciones

Cuando se utilicen encuestas complejas:

1. Identificar para cada indicador la unidad, población, ronda, módulo, ponderador, estrato y unidad primaria de muestreo en la documentación correspondiente.
2. Construir el diseño completo y estimar dominios desde ese diseño cuando corresponda. Usar `srvyr` para operaciones tabulares claras y `survey` cuando resulte necesario o para replicar la metodología original.
3. Respetar las definiciones oficiales y documentar toda diferencia, incluidas las reglas de valores ausentes y los intervalos de confianza. No asumir que varios módulos usan el mismo factor de expansión.
4. Diferenciar tamaño muestral sin ponderar, estimación ponderada y población expandida. Mantener precisión durante el cálculo y redondear solo para presentación. Distinguir proporciones, porcentajes, cambios porcentuales y puntos porcentuales.
5. No recalcular una clasificación oficial existente por costumbre. Si se debe reconstruir un quintil o indicador, explicitar población, unidad, variables y ponderación; no garantizar equivalencia sin compararla.

## Tablas, gráficos y mapas

Preparar una tabla de resultados legible antes de graficar. Usar `ggplot2`, y `sf` para datos espaciales cuando corresponda. Identificar fuente, población, período y unidades. Para comparaciones entre períodos, mantener cada estimación identificable y expresar la diferencia de forma explícita. En mapas, preferir códigos geográficos documentados y comprobar que la concordancia usada sea apropiada. Guardar con `ggsave()` indicando objeto, dimensiones y unidades. Crear únicamente los productos necesarios para la tarea.

## Reproducir resultados

Si se pide replicar, leer primero el código de origen y las definiciones de la cifra, tabla o figura objetivo. Ejecutar el flujo con los insumos y dependencias disponibles. Comparar resultados concretos y rastrear las discrepancias a población, denominador, ponderación, reglas de ausentes, métodos de estimación o redondeo. Verificar la sintaxis y ejecutar la parte afectada cuando sea posible. Hacer estas verificaciones durante el trabajo, fuera del script entregado, salvo que el usuario pida incorporarlas. No confundir un script que ejecuta con una réplica validada. Si faltan datos o dependencias, indicar cuáles y qué parte no se pudo verificar; no inventar cifras ni declarar éxito.

## Entrega

Entregar el código solicitado y explicar brevemente qué calcula, qué insumos necesita, cómo ejecutarlo, qué produce y qué se verificó. Identificar diferencias metodológicas relevantes y limitaciones reales. No incluir una revisión o informe independiente salvo que se haya solicitado.
