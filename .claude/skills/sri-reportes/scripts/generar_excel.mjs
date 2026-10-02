// ============================================================
// Exportar reportes del SRI a Excel
// Author: Daniel Sanchez
// Inputs: JSON preparado por generar_reportes.py
// Outputs: Excel y vistas PNG de cada reporte
// ============================================================
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const [dataPath, outputDir, modulesDir] = process.argv.slice(2);
const require = createRequire(path.join(modulesDir, '..', 'package.json'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const reports = JSON.parse(await fs.readFile(dataPath, 'utf8'));

for (const report of reports) {
  const { schema, rows } = report;
  const filePath = path.join(outputDir, schema.filename);
  // No reemplazar un reporte anterior sin una decisión explícita del usuario.
  try {
    await fs.access(filePath);
    throw new Error(`Ya existe ${filePath}; use otra carpeta de salida.`);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add('XML_Reporte');
  const lastRow = rows.length + 1;
  const matrix = rows.map(row => row.map((value, index) => {
    if (value === null) return null;
    if (schema.date_columns.includes(index)) return new Date(`${value}T00:00:00Z`);
    if (typeof value === 'string' && value.startsWith('=')) return `'${value}`;
    return value;
  }));
  const area = sheet.getRange(`A1:${schema.last_column}${lastRow}`);
  area.values = [schema.headers, ...matrix];
  area.format.font = { name: 'Aptos Narrow', size: 11 };
  const header = sheet.getRange(`A1:${schema.last_column}1`);
  header.format = { fill: '#D6DCE4', font: { name: 'Aptos Narrow', size: 11, bold: true }, wrapText: true, rowHeight: 34 };
  for (let index = 0; index < schema.headers.length; index++) {
    let n = index + 1;
    let column = '';
    while (n > 0) { n--; column = String.fromCharCode(65 + n % 26) + column; n = Math.floor(n / 26); }
    sheet.getRange(`${column}1:${column}${lastRow}`).format.columnWidth = schema.widths[index];
    if (lastRow > 1) {
      const range = sheet.getRange(`${column}2:${column}${lastRow}`);
      if (schema.text_columns.includes(index)) range.setNumberFormat('@');
      if (schema.date_columns.includes(index)) range.setNumberFormat('dd/mm/yyyy');
      if (schema.money_columns.includes(index)) range.setNumberFormat('#,##0.00');
      if (schema.rate_columns.includes(index)) range.setNumberFormat('0.00%');
    }
  }
  sheet.freezePanes.freezeRows(1);
  workbook.recalculate();
  const exported = await SpreadsheetFile.exportXlsx(workbook);
  await exported.save(filePath);
  // El renderizador trata textos numéricos como números. Solo para las vistas,
  // mostrar sus dígitos completos; el Excel ya exportado conserva texto y formato @.
  for (let rowIndex = 0; rowIndex < rows.length; rowIndex++) {
    for (const columnIndex of schema.text_columns) {
      const value = rows[rowIndex][columnIndex];
      if (typeof value === 'string' && /^\d{1,15}$/.test(value)) {
        let n = columnIndex + 1;
        let column = '';
        while (n > 0) { n--; column = String.fromCharCode(65 + n % 26) + column; n = Math.floor(n / 26); }
        sheet.getRange(`${column}${rowIndex + 2}`).setNumberFormat('0'.repeat(value.length));
      }
    }
  }
  // Dos vistas cubren también los importes, que están al final de estas tablas anchas.
  for (const [label, start, end] of schema.previews) {
    const preview = await workbook.render({ sheetName: 'XML_Reporte', range: `${start}1:${end}${Math.min(lastRow, 6)}`, scale: 1.5, format: 'png' });
    await fs.writeFile(path.join(outputDir, `${report.kind}-${label}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  console.log(filePath);
}
