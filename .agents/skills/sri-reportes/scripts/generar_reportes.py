# ============================================================
# Reportes de facturas y retenciones del SRI
# Author: Daniel Sanchez
# Purpose: Convertir XML autorizados en los dos reportes de Excel
# Inputs: Carpeta mensual, TXT del SRI y pares XML/PDF completos
# Outputs: Reporte facturas.xlsx y Reporte retenciones.xlsx
# ============================================================

# %% 0. Setup
import argparse
import csv
import html
import json
import logging
import subprocess
import tempfile
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from lxml import etree as ET

SCRIPT_DIR = Path(__file__).resolve().parent
RUNTIME = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies"
LOGGER = logging.getLogger(__name__)
IDENTIFICATIONS = {"04": "04-Ruc", "05": "05-Cédula", "06": "06-Pasaporte"}
PAYMENTS = {
    "01": "01-Sin utilización del sistema financiero",
    "15": "15-Compensación de deudas",
    "16": "16-Tarjeta de débito",
    "17": "17-Dinero electrónico",
    "18": "18-Tarjeta prepago",
    "19": "19-Tarjeta de crédito",
    "20": "20-Otros con utilización del sistema financiero",
    "21": "21-Endoso de títulos",
}
TAXES = {"1": "1-RENTA", "2": "2-IVA", "3": "3-ICE", "5": "5-IRBPNR", "6": "6-ISD"}


# %% 1. Read inputs
def read_document(path: Path) -> tuple[ET._Element, str]:
    """Leer el comprobante, tanto autorizado como XML sin envoltura."""
    xml_parser = ET.XMLParser(resolve_entities=False, no_network=True)
    outer = ET.parse(str(path), xml_parser).getroot()
    if outer.tag == "autorizacion":
        if outer.findtext("estado") != "AUTORIZADO":
            raise ValueError(f"XML sin autorización: {path.name}")
        body = ET.fromstring((outer.findtext("comprobante") or "").encode(), xml_parser)
        key = outer.findtext("numeroAutorizacion") or ""
    else:
        body = outer
        key = body.findtext("infoTributaria/claveAcceso") or ""
    body_key = body.findtext("infoTributaria/claveAcceso") or ""
    if len(key) != 49 or not key.isdigit() or key != body_key:
        raise ValueError(
            f"Clave de autorización inválida o distinta del XML: {path.name}"
        )
    return body, key


def read_month(
    month_dir: Path,
    direction: str,
    ruc: str,
    kind: str,
    year: int,
    month: int,
    from_xml: bool = False,
) -> list[tuple[ET._Element, str]]:
    """Comprobar el alcance y cada par de archivos contra el TXT del SRI."""
    type_dir = month_dir / direction.capitalize() / kind.capitalize()
    report_path = type_dir / f"{ruc}_{direction.capitalize()}.txt"
    expected = None
    if not from_xml:
        try:
            text = report_path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            text = report_path.read_text(encoding="latin-1")
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        if "CLAVE_ACCESO" not in (reader.fieldnames or []):
            raise ValueError(f"TXT sin la columna CLAVE_ACCESO: {report_path.name}")
        records = list(reader)
        expected = {record["CLAVE_ACCESO"].strip() for record in records}
        if len(expected) != len(records):
            raise ValueError(f"Claves repetidas en {report_path.name}; revisar el TXT")
    documents: dict[str, tuple[ET._Element, str]] = {}
    excluded = 0
    xml_dir = type_dir / f"{ruc}-{direction.capitalize()}"
    if from_xml and not xml_dir.is_dir():
        raise FileNotFoundError(f"Carpeta XML ausente: {xml_dir}")
    for path in sorted(xml_dir.glob("*.xml")):
        body, key = read_document(path)
        if expected is not None and key not in expected:
            excluded += 1
            continue
        date_path = (
            "infoFactura/fechaEmision"
            if kind == "facturas"
            else "infoCompRetencion/fechaEmision"
        )
        date = datetime.strptime(body.findtext(date_path) or "", "%d/%m/%Y")
        taxpayer_path = (
            (
                "infoFactura/identificacionComprador"
                if kind == "facturas"
                else "infoCompRetencion/identificacionSujetoRetenido"
            )
            if direction == "recibidos"
            else "infoTributaria/ruc"
        )
        if (date.year, date.month) != (year, month) or body.findtext(
            taxpayer_path
        ) != ruc:
            raise ValueError(f"XML fuera del mes o del RUC solicitado: {path.name}")
        expected_tag = "factura" if kind == "facturas" else "comprobanteRetencion"
        if body.tag != expected_tag:
            raise ValueError(f"Tipo de comprobante inesperado: {path.name}")
        pdf_path = path.with_suffix(".pdf")
        with pdf_path.open("rb") as pdf:
            if pdf.read(5) != b"%PDF-":
                raise ValueError(f"PDF vacío o inválido: {pdf_path.name}")
        if key in documents:
            previous = documents[key][0]
            if ET.tostring(body) != ET.tostring(previous):
                raise ValueError(f"Dos XML distintos para la misma clave: {path.name}")
        documents[key] = (body, key)
    missing = expected - documents.keys() if expected is not None else set()
    if missing:
        raise ValueError(
            f"{kind}: faltan {len(missing)} XML del TXT; completar con el MCP"
        )
    LOGGER.warning(
        "%s: se comprobaron estructura y alcance de %s XML; no se verifica la "
        "firma digital, la identidad del emisor ni la autorizacion del SRI",
        kind,
        len(documents),
    )
    LOGGER.info("%s: %s pares XML/PDF con estructura comprobada", kind, len(documents))
    if excluded:
        LOGGER.warning(
            "%s: %s XML excluidos porque no figuran en el TXT", kind, excluded
        )
    if from_xml:
        LOGGER.warning(
            "%s: origen XML suministrado; no acredita una descarga completa del portal",
            kind,
        )
    return list(documents.values())


# %% 2. Prepare data and amounts
def invoice_row(body: ET._Element, key: str) -> list[Any]:
    """Una fila por factura; las bases y los importes vienen del XML."""
    issuer = body.find("infoTributaria")
    info = body.find("infoFactura")
    if issuer is None or info is None:
        raise ValueError(f"Factura sin información tributaria: {key}")
    totals = info.findall("totalConImpuestos/totalImpuesto")
    iva = [tax for tax in totals if tax.findtext("codigo") == "2"]
    bases = {"6": Decimal(0), "7": Decimal(0), "0": Decimal(0), "gravada": Decimal(0)}
    for tax in iva:
        code = tax.findtext("codigoPorcentaje") or ""
        category = code if code in bases else "gravada"
        bases[category] += Decimal(tax.findtext("baseImponible") or "0")
    iva_codes = {tax.findtext("codigoPorcentaje") for tax in iva}
    detail_taxes = body.findall("detalles/detalle/impuestos/impuesto")
    iva_rates = {
        Decimal(tax.findtext("tarifa") or "0") / 100
        for tax in detail_taxes
        if tax.findtext("codigo") == "2"
        and tax.findtext("tarifa") is not None
        and tax.findtext("codigoPorcentaje") in iva_codes
    }
    rate: float | str | None = None
    if len(iva_codes) > 1 or len(iva_rates) > 1:
        rate = "varios"
    elif iva_rates:
        rate = float(next(iter(iva_rates)))
    elif iva_codes <= {"0", "6", "7"} and iva_codes:
        rate = 0.0
    ice = [tax for tax in totals if tax.findtext("codigo") == "3"]
    ice_rates = {
        Decimal(tax.findtext("tarifa") or "0") / 100
        for tax in detail_taxes
        if tax.findtext("codigo") == "3" and tax.findtext("tarifa") is not None
    }
    ice_rate: float | str | None = None
    if len(ice_rates) > 1:
        ice_rate = "varios"
    elif ice_rates:
        ice_rate = float(next(iter(ice_rates)))
    payments = [
        payment.findtext("formaPago") or "" for payment in info.findall("pagos/pago")
    ]
    observations = []
    if len(payments) > 1:
        observations.append(
            "Otras formas de pago: "
            + ", ".join(PAYMENTS.get(code, code) for code in payments[1:])
        )
    if iva_codes and rate is None:
        observations.append(
            "Tarifa IVA no indicada en el XML; códigos: "
            + ", ".join(sorted(str(code) for code in iva_codes))
        )
    return [
        issuer.findtext("ruc"),
        "01-Ruc",
        " ".join(html.unescape(issuer.findtext("razonSocial") or "").split()),
        issuer.findtext("contribuyenteRimpe"),
        info.findtext("identificacionComprador"),
        IDENTIFICATIONS.get(
            info.findtext("tipoIdentificacionComprador") or "",
            info.findtext("tipoIdentificacionComprador"),
        ),
        " ".join(html.unescape(info.findtext("razonSocialComprador") or "").split()),
        "01-Factura ",
        issuer.findtext("estab"),
        issuer.findtext("ptoEmi"),
        issuer.findtext("secuencial"),
        key,
        datetime.strptime(info.findtext("fechaEmision") or "", "%d/%m/%Y")
        .date()
        .isoformat(),
        *(float(bases[category]) for category in ("6", "7", "0", "gravada")),
        rate,
        float(sum((Decimal(tax.findtext("valor") or "0") for tax in iva), Decimal(0))),
        float(
            sum(
                (
                    Decimal(tax.findtext("valor") or "0")
                    for tax in totals
                    if tax.findtext("codigo") == "5"
                ),
                Decimal(0),
            )
        ),
        float(Decimal(info.findtext("propina") or "0")),
        float(Decimal(info.findtext("importeTotal") or "")),
        ice_rate,
        float(sum((Decimal(tax.findtext("valor") or "0") for tax in ice), Decimal(0)))
        if ice
        else None,
        float(Decimal(info.findtext("totalDescuento") or "0")),
        PAYMENTS.get(payments[0], payments[0]) if payments else None,
        "; ".join(observations) or None,
    ]


def withholding_rows(body: ET._Element, key: str) -> list[list[Any]]:
    """Una fila por retención y documento de sustento, versiones 1 y 2."""
    issuer = body.find("infoTributaria")
    info = body.find("infoCompRetencion")
    if issuer is None or info is None:
        raise ValueError(f"Retención sin información tributaria: {key}")
    common: list[Any] = [
        issuer.findtext("ruc"),
        "01-Ruc",
        " ".join(html.unescape(issuer.findtext("razonSocial") or "").split()),
        info.findtext("identificacionSujetoRetenido"),
        IDENTIFICATIONS.get(
            info.findtext("tipoIdentificacionSujetoRetenido") or "",
            info.findtext("tipoIdentificacionSujetoRetenido"),
        ),
        " ".join(
            html.unescape(info.findtext("razonSocialSujetoRetenido") or "").split()
        ),
        "07-Comprobante de Retención",
        issuer.findtext("estab"),
        issuer.findtext("ptoEmi"),
        issuer.findtext("secuencial"),
        key,
        datetime.strptime(info.findtext("fechaEmision") or "", "%d/%m/%Y")
        .date()
        .isoformat(),
        info.findtext("periodoFiscal"),
    ]
    supports = body.findall("docsSustento/docSustento")
    entries = [
        (support, tax)
        for support in supports
        for tax in support.findall("retenciones/retencion")
    ]
    if not supports:
        entries = [(tax, tax) for tax in body.findall("impuestos/impuesto")]
    rows = []
    for support, tax in entries:
        number = support.findtext("numDocSustento") or ""
        number = number.replace("-", "")
        support_code = support.findtext("codDocSustento") or ""
        support_date = support.findtext("fechaEmisionDocSustento")
        rows.append(
            common
            + [
                "01-Factura" if support_code == "01" else support_code,
                number[:3] or None,
                number[3:6] or None,
                number[6:] or None,
                datetime.strptime(support_date, "%d/%m/%Y").date().isoformat()
                if support_date
                else None,
                TAXES.get(tax.findtext("codigo") or "", tax.findtext("codigo")),
                tax.findtext("codigoRetencion"),
                float(Decimal(tax.findtext("baseImponible") or "")),
                float(Decimal(tax.findtext("porcentajeRetener") or "")),
                float(Decimal(tax.findtext("valorRetenido") or "")),
            ]
        )
    if not rows:
        raise ValueError(f"Comprobante de retención sin líneas: {key}")
    return rows


# %% 3. Write outputs
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generar los dos reportes desde un mes completo del MCP."
    )
    parser.add_argument("--carpeta-mes", type=Path, required=True)
    parser.add_argument("--anio", type=int, required=True)
    parser.add_argument("--mes", type=int, required=True, choices=range(1, 13))
    parser.add_argument("--ruc", required=True)
    parser.add_argument(
        "--direccion", choices=("recibidos", "emitidos"), default="recibidos"
    )
    parser.add_argument(
        "--tipos",
        nargs="+",
        choices=("facturas", "retenciones"),
        default=["facturas", "retenciones"],
    )
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--runtime", type=Path, default=RUNTIME)
    parser.add_argument(
        "--desde-xml",
        action="store_true",
        help="Reportar XML suministrados, sin afirmar cobertura del TXT/portal",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    reports = []
    schema = json.loads(
        (SCRIPT_DIR.parent / "assets/reportes.json").read_text(encoding="utf-8")
    )
    for kind in dict.fromkeys(args.tipos):
        documents = read_month(
            args.carpeta_mes,
            args.direccion,
            args.ruc,
            kind,
            args.anio,
            args.mes,
            args.desde_xml,
        )
        rows = (
            [invoice_row(body, key) for body, key in documents]
            if kind == "facturas"
            else [row for body, key in documents for row in withholding_rows(body, key)]
        )
        reports.append({"kind": kind, "schema": schema[kind], "rows": rows})
        LOGGER.info("%s: %s filas para Excel", kind, len(rows))
    # Los datos intermedios viven en una carpeta temporal, nunca en el repositorio.
    args.salida.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="sri-reportes-", dir=args.salida.resolve()
    ) as temp_dir:
        data_path = Path(temp_dir) / "reportes.json"
        data_path.write_text(json.dumps(reports, ensure_ascii=False), encoding="utf-8")
        node = args.runtime / "node/bin/node.exe"
        if not node.exists():
            node = args.runtime / "node/bin/node"
        subprocess.run(  # noqa: S603 — argumentos separados de un ejecutable local
            [
                str(node),
                str(SCRIPT_DIR / "generar_excel.mjs"),
                str(data_path),
                str(args.salida.resolve()),
                str(args.runtime / "node/node_modules"),
            ],
            check=True,
        )  # noqa: S603 — rutas locales y argumentos separados, sin shell
    for report in reports:
        kind = report["kind"]
        amount_index = 21 if kind == "facturas" else 22
        total = sum(
            (Decimal(str(row[amount_index])) for row in report["rows"]), Decimal(0)
        )
        counts = Counter(
            row[11 if kind == "facturas" else 10] for row in report["rows"]
        )
        LOGGER.info(
            "%s: %s comprobantes, %s filas, total %s",
            kind,
            len(counts),
            len(report["rows"]),
            total,
        )


if __name__ == "__main__":
    main()
