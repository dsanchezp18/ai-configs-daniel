---
name: quantificador-viz-publishing
description: Publicar en el sitio quantificador la última visualización del catálogo de graficos-el-quantificador. Sincroniza solo esa entrada, la vuelve interactiva con Observable Plot, regenera su miniatura, verifica SEO y abre el pull request. Usar cuando el catálogo tiene una fila nueva `published` que aún no está en el sitio, o cuando una visualización publicada necesita datos o miniatura nuevos.
metadata:
  short-description: Publicar una visualización en el sitio
---

# Publicación de visualizaciones en el sitio

Usa esta skill dentro del repositorio `quantificador` cuando una fila del
catálogo de `graficos-el-quantificador` ya está `published` y falta su página en
el sitio, o cuando una visualización publicada necesita datos o miniatura
nuevos. Producir el gráfico (R, PNG, catálogo) es trabajo de
`quantificador-chart-production`. El copy editorial no se redacta aquí.

Las reglas completas están en el `AGENTS.md` del sitio, en las secciones
`Visualizaciones Workflow`, `Observable visualizations`, `Publishing One
Visualization, Step by Step` y `Lessons Learned from the Observable Charts`. Si
esta skill y el `AGENTS.md` difieren, manda el `AGENTS.md`. Esta skill es el
orden de trabajo y las trampas ya conocidas.

## Antes de empezar

- Lee el `AGENTS.md` del sitio completo.
- Trabaja en una rama nueva desde `origin/main` (`git fetch origin`, luego
  `git switch -c visualizacion-NN origin/main`). No trabajes sobre un `main`
  local atrasado ni sobre cambios que no sean tuyos. Si el árbol tiene trabajo
  ajeno, aíslalo en un worktree.
- Herramientas: Hugo 0.163 o más nuevo en el PATH (el 0.157 no compila
  `layouts/index.xml`), Python 3 con Playwright (miniaturas) y PyYAML, y R con
  los paquetes del script de exportación.
- No hagas commit, push ni merge si el usuario no lo pidió. El resultado normal
  es una rama con un pull request abierto.

## Flujo

1. **Repositorio de gráficos al día.** Un checkout sin actualizar puede ocultar
   gráficos ya publicados. Desde `graficos-el-quantificador`:

   ```powershell
   git fetch origin
   git status -sb
   git merge --ff-only origin/main        # solo si el árbol está limpio
   python scripts/validate_chart_catalog.py
   ```

   La fila debe estar `published`, con fecha, enlace de LinkedIn, imagen y
   `Description`. Si falta algo, repórtalo y detente: no inventes esos campos.

2. **Comprueba el enlace de LinkedIn.** Abre
   `https://www.linkedin.com/embed/feed/update/urn:li:<activity|share|ugcPost>:<id>`
   con el identificador del enlace del catálogo. Debe responder 200. Un enlace
   `feed/update/...?actorCompanyId=...` puede ser solo para administradores y
   dar 404 a cualquier lector. Corrige la fila en el repo de gráficos, no solo la
   página del sitio. Un enlace genérico de empresa no sirve.

3. **Sincroniza solo la última entrada.** Por defecto el script escribe
   únicamente el grupo con la última fila publicada del catálogo y no borra
   nada:

   ```powershell
   python scripts/sync_visualizaciones.py `
     --catalog-path ../graficos-el-quantificador/outputs/chart_catalog/chart_catalog.csv `
     --image-source-dir ../graficos-el-quantificador/outputs/figures
   ```

   Luego `git status --short`. Solo deben aparecer la página nueva y sus
   imágenes. Si aparece otra página, no la reviertas a mano: hay un fallo del
   script y se corrige en el script. `--all` reescribe todo y es una decisión
   explícita, no un atajo.

4. **Edita la página nueva.**
   - Sustituye las imágenes del cuerpo por el shortcode
     `{{< observable-chart id="..." fallback="/img/visualizaciones/....png" title="..." alt="..." >}}`,
     uno por gráfico, con texto alternativo que describa lo que muestra.
   - Agrega entre 1 y 4 `tags` del vocabulario existente.
   - Conserva `link` (LinkedIn) y `github`.
   - Cumple las reglas editoriales del sitio: tuteo, sentence case, cero em
     dashes y ninguna fórmula de contraste artificial. No cambies el texto del
     autor.

5. **Escribe los datos del gráfico.** Crea
   `static/data/visualizaciones/<id>.json` con `id`, `kind`, `config`,
   `source_script` y `data`, a partir de un script R en `scripts/` que lea los
   `data/processed/*.rds` del repo de gráficos. Imita
   `scripts/export_observable_56_57.R`: la raíz del repo de gráficos entra como
   primer argumento. Toma los colores del PNG publicado y verifica que valores,
   unidades, etiquetas y notas coincidan con el PNG y el catálogo. Tipos
   disponibles en `static/js/observable/observable-viz.js`: `bar` (con
   `callout`), `horizontal-bar` (`hide_legend`, `x_decimals`), `line`,
   `line-events` (`bands`, `reference_y`, `point_label`), `province-map` y `map`
   (`bins`, `colors`). Si hace falta un tipo nuevo, extiende el renderizador y
   revisa que no cambie los gráficos que ya existen.

6. **Regenera la miniatura.** Con un servidor de Hugo en el puerto 1318 (el que
   usa el script por defecto) y solo para el gráfico nuevo:

   ```powershell
   python scripts/export_observable_thumbnails.py --update-front-matter --chart-id <id>
   ```

   Sin `--chart-id` reescribe todas las miniaturas y llena el diff de ruido
   binario. Cuando corrijas los datos de un gráfico antiguo, regenera su
   miniatura: una más vieja que su JSON muestra un gráfico desactualizado en la
   portada y en el listado. Detén tu servidor al terminar y no mates procesos de
   Hugo que no iniciaste.

7. **Verifica.**

   ```powershell
   python -m unittest discover -s tests -p "test_*.py"
   hugo --minify --gc
   python scripts/check_seo.py public
   python scripts/check_llms_index.py public
   ```

   Después abre la página en el navegador, en escritorio y con un viewport de
   375 px: el gráfico debe dibujarse (no el PNG de respaldo), sin desborde
   horizontal, con leyendas y etiquetas legibles y sin errores en la consola.

8. **Pull request.** Rama, commit en inglés imperativo, push y PR con título y
   cuerpo en español. Cuando Netlify publique la vista previa, comprueba ahí el
   título, la descripción, el canónico, el H1, `og:image` y que la página salga
   en `sitemap.xml`. No mergees sin que el usuario lo pida, y no lo hagas con una
   revisión de CI que falle.

9. **Después del merge.** `git switch main` y `git pull --ff-only origin main`
   en el sitio y en el repo de gráficos. Borra tu rama local ya fusionada.

## Trampas conocidas

- **Miniaturas viejas.** El script de sincronización nunca cambia la
  `thumbnail` de una página publicada. Sin el paso 6, la tarjeta muestra el PNG
  estático o un gráfico anterior a la corrección de datos.
- **Leyendas estiradas.** `.observable-viz__canvas svg { width: 100%; height: auto }`
  estiraba la leyenda SVG de Observable Plot y deformaba el mapa. El mapa dibuja
  su propia leyenda y limita su ancho. Revisa cada leyenda nueva en escritorio y
  en móvil.
- **Etiquetas de bandas en móvil.** En `line-events`, las etiquetas largas se
  superponen en pantallas angostas. Usa `label_compact` y `label_rotate`.
- **`data/` rompe la compilación.** Hugo carga toda la carpeta `data/`, con el
  `.xlsx` de las becas, en cuanto una plantilla lee `site.Data`, y falla. El JSON
  que necesiten las plantillas va en `static/data/` y se lee con `os.ReadFile`.
- **Reescritura de páginas antiguas.** El sync asociaba cada página con su
  primera imagen, así que los gráficos de las páginas con varios gráficos
  recibían redirecciones inventadas, y conservaba PNG en caché desactualizados.
  Ya está corregido y el modo por defecto toca solo la última entrada. Cualquier
  otra página en `git status` es un fallo.
- **Archivos bloqueados en Windows.** Un servidor de Hugo abierto mantiene los
  archivos de `static/`. Detenlo antes de reemplazar PDF o imágenes.
- **Datos sin verificar.** No publiques un JSON cuyo valor, unidad o nota no
  coincida con el PNG y el catálogo. Compara antes del pull request.

## Entrega

Reporta, separado, lo que verificaste (pruebas, compilación, SEO, vista en
escritorio y móvil, consola) y lo que no pudiste verificar, junto con el enlace
del pull request y el estado de su CI. No presentes la página como terminada si
el gráfico interactivo o su respaldo no funcionan.
