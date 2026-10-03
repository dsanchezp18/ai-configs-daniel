# Campos y cálculo de los reportes

## Fuentes y entregables

La fuente de cada fila es el contenido del XML leído. El generador comprueba su
estructura, clave, tipo, RUC, mes y relación con el TXT cuando está disponible. El TXT
del SRI establece qué claves pertenecen al mes y permite comprobar que no falten
comprobantes. El PDF sirve como entregable y se comprueba su encabezado; no se extraen
importes de él.

Estas comprobaciones no verifican la firma electrónica del XML ni la identidad del
emisor. Un estado `AUTORIZADO`, una clave coincidente o una firma presente no bastan
para demostrar autenticidad. El generador no establece confianza en certificados ni
confirma que el SRI autorizó el comprobante. Revisa el origen del archivo por separado;
el modo `--desde-xml` tampoco comprueba su cobertura en el portal. El generador muestra
esta limitación en el registro de cada tipo procesado.

La verificación del generador no sustituye la respuesta final del MCP ni una revisión
visual del PDF.

La estructura y los encabezados provienen de `Reporte facturas.xlsx` y
`Reporte retenciones.xlsx` del proyecto de descarga de comprobantes suministrado
por Daniel. `assets/reportes.json` conserva los encabezados, anchos y tipos de columna,
sin guardar contribuyentes, credenciales o facturas de ejemplo. No se ejecuta ni
se reproduce la aplicación `XML_Manager_v5.53.xlsm`.

Cada Excel tiene una sola hoja, `XML_Reporte`. Se conserva el encabezado gris; se
añaden fecha `dd/mm/yyyy`, importes con dos decimales y encabezado fijo para facilitar
la lectura. Los valores no cambian por ese formato. Los reportes contienen datos,
sin fórmulas ni hojas de resumen añadidas. Las razones sociales se presentan sin
espacios repetidos ni entidades HTML como `&amp;`: los caracteres se muestran legibles.

## Facturas: una fila por clave

| Columnas | Fuente o transformación |
|---|---|
| A–D | RUC y razón social de `infoTributaria`, tipo de emisor `01-Ruc`, `contribuyenteRimpe` si existe |
| E–G | Identificación, tipo y razón social del comprador de `infoFactura` |
| H–L | Tipo `01-Factura `, establecimiento, punto de emisión, secuencial y autorización |
| M | `fechaEmision`, convertida a fecha Excel |
| N–Q | Bases IVA de `totalConImpuestos`: códigos 6, 7, 0 y demás códigos, respectivamente |
| R | Tarifa IVA de los impuestos del detalle, dividida por 100; `varios` si el resumen presenta más de un código o el detalle más de una tarifa |
| S–T | Suma de `valor` del impuesto código 2 (IVA) y código 5 (IRBPNR), respectivamente |
| U–V | `propina` e `importeTotal` |
| W–X | Tarifa del ICE del detalle y suma del impuesto código 3; vacías si no hay ICE |
| Y | `totalDescuento` |
| Z | Primera `formaPago` de `pagos`; el código se acompaña con su etiqueta |
| AA | Otras formas de pago o tarifa ausente que requiere revisión; vacía si no aplica |

**Base gravada = suma de las bases IVA cuyos códigos no son 0, 6 ni 7.**
Por ejemplo, base 100 y tarifa 15 en el XML generan Base Gravada 100, Tarifa IVA
15 % y Monto IVA igual al `valor` registrado en el XML. El generador no recalcula
el impuesto multiplicando base por tarifa: respeta el importe y su redondeo original.

El ejemplo contiene facturas con códigos adicionales de base cero. También cuentan
para decidir `varios`, como ocurre en el reporte suministrado. No se eliminan esos
códigos para presentar una sola tarifa. Si falta la tarifa, no se estima dividiendo
IVA por base ni se aplica la tarifa vigente: se deja vacía y se explica en Observacion.
Las sumas usan Decimal antes de convertir los importes a números de Excel.

## Retenciones: una fila por línea de impuesto

| Columnas | Fuente o transformación |
|---|---|
| A–F | Emisor/agente y sujeto retenido, con sus identificaciones y razones sociales |
| G–K | Tipo `07-Comprobante de Retención`, establecimiento, punto, secuencial y autorización |
| L–M | Fecha de emisión y `periodoFiscal`, este último como texto |
| N–R | Tipo, número separado en establecimiento/punto/secuencial y fecha del documento de sustento |
| S–W | `codigo`, `codigoRetencion`, `baseImponible`, `porcentajeRetener` y `valorRetenido` de cada línea |

La versión 2 lee cada `docsSustento/docSustento/retenciones/retencion`. La versión 1
lee cada `impuestos/impuesto`, donde el sustento está en la propia línea. No se suma
todo un comprobante en una sola fila: dos impuestos o dos documentos de sustento
aportan sus propias filas.

**Valor retenido del reporte = `valorRetenido` de la línea XML.**
Por ejemplo, base 100, porcentaje 2 y valor retenido 2 producen tres valores 100,
2 y 2. La columna `% Ret.` contiene 2, como la referencia; no se guarda 0,02.
Para el sustento, `01` se presenta como `01-Factura`; los demás códigos se conservan
sin inventar una etiqueta. Los códigos desconocidos de identificación, pago e
impuesto se conservan como texto.

## Cobertura y límites

Las claves de autorización, RUC, establecimientos, puntos y secuenciales siempre
son texto. Una clave repetida con el mismo contenido se cuenta una vez; si hay XML
distintos para la misma clave, hace falta revisar la fuente. Los XML ajenos al TXT
no se incluyen. Cada XML incluido debe corresponder al RUC, tipo y mes solicitado
y tener un PDF con encabezado válido. Un TXT ausente no se interpreta como mes vacío.

Los importes ausentes de categorías de impuesto equivalen a cero cuando la categoría
no aparece; RIMPE, pago e ICE ausentes quedan vacíos. Un XML mal formado, no autorizado,
sin clave válida o sin sus campos de fecha impide emitir un reporte que se declare
completo. Los mensajes indican el archivo a revisar. No se interpreta una falta de
datos como exención, anulación o conclusión tributaria.

Con `--desde-xml`, la fuente es el conjunto de XML suministrado expresamente por la
persona y no el TXT. Se mantiene la comprobación de RUC, mes, tipo, autorización y
PDF, pero no se afirma cobertura del portal. Este modo sirve para referencias y
reportes de archivos que la persona entregó; no sirve para declarar completa una
descarga fallida del MCP.

## Prueba de referencia, 2026-10-02

Se probaron los XML recibidos de septiembre 2026 suministrados por Daniel: 30 facturas
y 7 retenciones, con sus PDF. Los Excel generados se reabrieron y se compararon con
los ejemplos por clave de autorización: 810 celdas de facturas y 161 de retenciones.
Encabezados, fechas, identificaciones, códigos y valores numéricos coinciden. En dos
celdas de razón social la referencia conserva entidades HTML escapadas; se normalizan
para comparar el mismo nombre. El generador muestra esos nombres legibles y limpia
los espacios repetidos de las razones sociales al leer los XML.

El TXT de facturas de esa referencia contiene 29 claves, mientras el Excel y la carpeta
XML contienen 30. El par adicional corresponde al 4 de septiembre, por 120,75. Por eso
la reproducción del ejemplo usa `--desde-xml`: no se oculta esa diferencia ni se afirma
que el TXT tenga 30 filas. El TXT de retenciones coincide con sus 7 XML.

Totales de los ejemplos reproducidos: importe de facturas 12 224,26; valor retenido
3 914,39. Las pruebas sintéticas cubren varias líneas y documentos de sustento,
retenciones de versiones 1 y 2, códigos IVA de base cero, tarifa ausente, múltiples
pagos, XML duplicados, PDF faltante, mes incorrecto y clave TXT sin XML.

La tarifa ICE se presenta como porcentaje cuando el XML incluye `tarifa`; no se
infieren tarifas específicas por unidades. No se generan reportes de notas de crédito,
débito ni liquidaciones de compra con esta skill.
