---
name: lide-social-media
description: Publicar, programar, republicar y amplificar posts de El Quantificador y LIDE en Instagram, Facebook, LinkedIn y X (artes, textos, colaboraciones, likes y reposts entre cuentas). Usar cuando Daniel pida un arte para redes, programar o publicar un post, corregir uno ya publicado, o dar likes y reposts desde las otras cuentas.
---

# Redes sociales de El Quantificador y LIDE

Responde en español, con tuteo y sin rayas largas (em dashes). Daniel suele
delegar todo ("ya sabes todo tú"). Decide los detalles, haz el trabajo y
reporta al final.

## 1. Cuentas

| Red | Cuenta que publica | Otras cuentas del ecosistema |
|---|---|---|
| Instagram | elquantificador | laboratoriolide, newdimensions_ec. Están en el mismo inicio de sesión. Cambia con Más > Switch accounts. |
| Facebook | Página El Quantificador (id 101766768141723) | CM Lide (perfil que administra las páginas), página LIDE ("Laboratorio de Investigación para el Desarrollo del Ecuador"), New Dimensions, Bridges to the Future |
| LinkedIn | Página El Quantificador (company 65035345) | LIDE Community Management (perfil), Ecuadorian Development Research Lab (LIDE) (página), New Dimensions, Bridges to the Future |
| X | @ElQuantificador | LIDE es @laboratoriolide |

El Quantificador también tiene Threads (@elquantificador) y Bluesky
(elquantificador.bsky.social). Úsalos solo si Daniel los pide.

Otros datos fijos:

- Meta business_id: 1285696443612615.
- Correo de becas: capacitaciones@laboratoriolide.org.
- Página de cursos: elquantificador.org/talleres.
- Donaciones: Givebutter. El enlace está en la página del curso en el repo `quantificador`.

## 2. Dónde y cómo se publica

- Publica siempre desde El Quantificador, nunca desde LIDE.
- Instagram: publica desde El Quantificador con laboratoriolide como
  colaborador. Después entra como laboratoriolide y acepta la invitación.
  Aparece como aviso "Review" sobre el post o en Notificaciones.
- Facebook: solo El Quantificador, sin colaborador.
- LinkedIn: sube el carrusel como PDF (documento). Una página no puede hacer
  una colaboración formal con un documento. Por eso menciona a LIDE con @ en
  el texto (autocompletar "Ecuadorian Development Research Lab (LIDE)"). No
  uses el editor colaborativo del feed: al adjuntar un documento cambia el
  autor a la cuenta personal.
- X: hasta 4 imágenes y un texto de 280 caracteres o menos. Menciona a
  @laboratoriolide.
- Si piden publicar "mañana" sin hora, usa las 12:30, hora de Quito.

## 3. Likes y reposts después de publicar

Este es el patrón de los posts anteriores. Si hay duda, abre un post viejo y
mira quién reaccionó y quién compartió.

| Red | Like y repost (o compartir) | Solo like |
|---|---|---|
| LinkedIn | LIDE Community Management, página LIDE, New Dimensions | Bridges to the Future |
| Facebook | Página LIDE, New Dimensions, CM Lide ("Share now") | El Quantificador (su propio post), Bridges to the Future |
| Instagram | newdimensions_ec | laboratoriolide (además acepta la colaboración) |

Al terminar, deja otra vez a El Quantificador como identidad activa en cada
red.

## 4. Artes

- Hazlos en Claude Design (artifact de tipo Design), no en Canva. Daniel
  encontró que los de Canva se ven "muy AI".
- Carrusel de 3 artes en 1080 × 1350.
- Colores de El Quantificador: azul #006b8f (oscuro #00566f), rojo de
  categoría #a8363d. Colores del logo: cian #00a1cb, rojo #d54d54, naranja
  #ef9f4e, pizarra #647a8f. Letra Open Sans.
- Fondo blanco con letras azules. Mayúscula solo al inicio de la frase. Sin
  emoji.
- El nombre del curso va grande, en una sola línea si cabe. Horarios, fechas
  y "clases en vivo" también van grandes. Los logos de El Quantificador y LIDE
  van grandes. La regla de Alonso: todo lo importante se tiene que leer en un
  teléfono.
- En un calendario pon el mes bajo cada número ("Dic"), no "Clase 1".
- Exporta cada arte a JPG 1080 × 1350 con Playwright desde el HTML del board.
  Cambia las rutas `/_blob/` por rutas locales. Une los JPG en un PDF con PIL
  para LinkedIn.
- Si Daniel quiere las imágenes en el iPhone, mándale los JPG con
  SendUserFile.

## 5. Texto base para cursos

```
¿<Gancho en forma de pregunta>? Abrimos una nueva edición del curso gratuito de El Quantificador y LIDE.

Del <fechas>, de 19:30 a 20:30 (hora de Quito, Lima y Bogotá). Son <n> clases en vivo por YouTube para <objetivo>.

Si está dentro de tus posibilidades, apoya esta iniciativa con una donación voluntaria desde $5 y accede a las grabaciones, a las clases por Teams y al certificado. Si no puedes donar, pide una beca escribiendo a capacitaciones@laboratoriolide.org.

Inscríbete gratis: <enlace de Luma>
Más información: elquantificador.org/talleres

#AnalíticaDeDatos #CursoGratuito #Ecuador #ElQuantificador #LaboratorioLIDE
```

- LinkedIn: el mismo texto, con la mención @LIDE, el enlace completo
  https://elquantificador.org/talleres y sin hashtags.
- Menciona siempre la donación desde $5. Alonso lo pidió para que nadie
  piense que tiene que pagar mucho.
- Después de escribir en Meta, revisa que el último hashtag no se haya
  cortado.

## 6. Navegador (Claude in Chrome)

- Hay varios Chrome conectados. El que tiene las sesiones de X, Meta,
  LinkedIn e Instagram ha sido "Browser 2". Si hay duda, pregunta cuál usar.
  No elijas solo. No hay forma de mandar un aviso de verificación al
  navegador.
- No hagas clic en "Add photo" o "Add a document" sin antes cambiar el
  comportamiento del campo de archivo. Si no, se abre el selector de archivos
  del sistema y la pestaña se congela. Ejecuta esto en la página:

  ```js
  if(!window.__claudeFilePatch){const P=HTMLInputElement.prototype;const orig=P.click;P.click=function(){if(this.type==='file'){if(!this.isConnected)document.body.appendChild(this);this.setAttribute('aria-label','claude media input');this.style.cssText='display:block!important;opacity:1!important;visibility:visible!important;position:fixed!important;top:5px;left:5px;width:220px;height:30px;z-index:2147483647';return;}return orig.call(this)};if(P.showPicker){P.showPicker=function(){}};window.__claudeFilePatch=true;}
  ```

  Luego haz clic en el botón, busca "claude media input" con `find` y sube
  los archivos con `file_upload`.
- En Meta, escribir un texto largo puede dar timeout pero igual termina.
  Revisa el texto con `innerText` del campo editable.
- LinkedIn: adjunta el documento antes de escribir. Una vista previa de
  enlace oculta la barra de archivos. Para reaccionar como otra cuenta, usa
  el botón "Open menu for switching identity" del post (búscalo por
  `data-urn`), elige la cuenta y pulsa Save.
- Facebook: cambia de perfil con el avatar de arriba a la derecha > See all
  profiles. Confirma la identidad con el texto "Comment as ..." del campo de
  comentarios.
- X: si aparece la verificación de Cloudflare o un código QR para
  "confirm you are human", detente y pide a Daniel que la resuelva. Nunca
  resuelvas captchas.
- Cierra las pestañas que abriste.

## 7. Corregir un post ya programado o publicado

1. Corrige el board en Claude Design. Exporta otra vez los JPG y el PDF.
2. LinkedIn programado: Edit post > quita el documento > Add a document >
   sube el PDF nuevo con su título > Schedule. Si piden publicar ya, en la
   lista de posts programados elige "Post now".
3. Meta programado: borra los posts de Facebook e Instagram (Posts & reels >
   Scheduled > ... > Manage post > Delete). Crea uno nuevo y pulsa Publish con
   "Set date and time" apagado.
4. X publicado: no se pueden cambiar las imágenes. Borra el tweet y publica
   otro.
5. Repite los likes y reposts.

## 8. Actualizar el sitio web

El repo `adminlide/quantificador` guarda datos que dependen de los posts:

- Página de cada curso (`content/talleres/<curso>/index.md`): la lista
  `participation_social_posts` tiene los enlaces a las publicaciones oficiales
  que los participantes deben compartir. Cuando publiques una edición nueva,
  propón actualizar esos enlaces.
- Visualizaciones: el catálogo de `graficos-el-quantificador` necesita el
  enlace real del post de LinkedIn (`LinkedIn Link`) antes de marcar un
  gráfico como `published`.

Sigue el `AGENTS.md` de ese repo para cualquier cambio.

## 9. Reporte final

Una línea por red: qué quedó publicado, quién tiene que aceptar algo (la
colaboración de Instagram) y qué no se pudo hacer y por qué.
