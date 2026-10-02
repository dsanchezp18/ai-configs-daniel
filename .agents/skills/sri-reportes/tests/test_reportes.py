# ============================================================
# Pruebas del generador de reportes SRI
# Author: Daniel Sanchez
# Purpose: Comprobar bases, líneas de retención y cobertura de archivos
# Inputs: XML/TXT/PDF sintéticos, sin datos privados
# Outputs: Resultado de unittest
# ============================================================

# %% 0. Setup
import importlib.util
import tempfile
import unittest
from pathlib import Path

from lxml import etree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/generar_reportes.py"
SPEC = importlib.util.spec_from_file_location("reportes", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
REPORTES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORTES)
KEY = "0109202601" + "0" * 39
ISSUER = f"""<infoTributaria><ruc>0000000000001</ruc>
<claveAcceso>{KEY}</claveAcceso><razonSocial>Empresa</razonSocial>
<estab>001</estab><ptoEmi>002</ptoEmi><secuencial>000000003</secuencial>
</infoTributaria>"""
INVOICE = f"""<factura>{ISSUER}<infoFactura><fechaEmision>01/09/2026</fechaEmision>
<tipoIdentificacionComprador>04</tipoIdentificacionComprador>
<identificacionComprador>0000000000002</identificacionComprador>
<razonSocialComprador>Comprador</razonSocialComprador><importeTotal>115</importeTotal>
<totalDescuento>0</totalDescuento><propina>0</propina><totalConImpuestos>
<totalImpuesto><codigo>2</codigo><codigoPorcentaje>4</codigoPorcentaje>
<baseImponible>100</baseImponible><valor>15</valor></totalImpuesto>
</totalConImpuestos></infoFactura><detalles><detalle><impuestos><impuesto>
<codigo>2</codigo><codigoPorcentaje>4</codigoPorcentaje><tarifa>15</tarifa>
</impuesto></impuestos></detalle></detalles></factura>"""
RETENTION_INFO = """<infoCompRetencion><fechaEmision>01/09/2026</fechaEmision>
<tipoIdentificacionSujetoRetenido>04</tipoIdentificacionSujetoRetenido>
<identificacionSujetoRetenido>0000000000002</identificacionSujetoRetenido>
<razonSocialSujetoRetenido>Sujeto</razonSocialSujetoRetenido>
<periodoFiscal>09/2026</periodoFiscal></infoCompRetencion>"""
TAX = """<codigo>1</codigo><codigoRetencion>001</codigoRetencion>
<baseImponible>100</baseImponible><porcentajeRetener>2</porcentajeRetener>
<valorRetenido>2</valorRetenido>"""
SUPPORT = """<codDocSustento>01</codDocSustento>
<numDocSustento>001002000000003</numDocSustento>
<fechaEmisionDocSustento>01/09/2026</fechaEmisionDocSustento>"""


# %% 1. Test calculations and document coverage
class TestReportes(unittest.TestCase):
    def test_invoice_preserves_amount_and_text_identifiers(self) -> None:
        row = REPORTES.invoice_row(ET.fromstring(INVOICE), KEY)
        self.assertEqual(len(row), 27)
        self.assertEqual(row[8:12], ["001", "002", "000000003", KEY])
        self.assertEqual(row[13:22], [0, 0, 0, 100, 0.15, 15, 0, 0, 115])
        self.assertEqual(row[22:24], [None, None])

    def test_zero_base_second_code_means_varios(self) -> None:
        xml = INVOICE.replace(
            "</totalConImpuestos>",
            """<totalImpuesto>
<codigo>2</codigo><codigoPorcentaje>5</codigoPorcentaje>
<baseImponible>0</baseImponible><valor>0</valor></totalImpuesto>
</totalConImpuestos>""",
        )
        self.assertEqual(REPORTES.invoice_row(ET.fromstring(xml), KEY)[17], "varios")

    def test_missing_rate_is_not_inferred(self) -> None:
        xml = INVOICE.replace("<tarifa>15</tarifa>", "")
        row = REPORTES.invoice_row(ET.fromstring(xml), KEY)
        self.assertIsNone(row[17])
        self.assertIn("Tarifa IVA no indicada", row[26])

    def test_payment_entries_are_not_lost(self) -> None:
        xml = INVOICE.replace(
            "</infoFactura>",
            """<pagos>
<pago><formaPago>01</formaPago></pago><pago><formaPago>19</formaPago></pago>
</pagos></infoFactura>""",
        )
        row = REPORTES.invoice_row(ET.fromstring(xml), KEY)
        self.assertEqual(row[25], "01-Sin utilización del sistema financiero")
        self.assertIn("19-Tarjeta de crédito", row[26])

    def test_withholding_v2_keeps_every_tax_and_support(self) -> None:
        support = (
            f"<docSustento>{SUPPORT}<retenciones><retencion>{TAX}</retencion>"
            f"<retencion>{TAX.replace('001', '002')}</retencion>"
            "</retenciones></docSustento>"
        )
        xml = (
            f"<comprobanteRetencion>{ISSUER}{RETENTION_INFO}<docsSustento>{support}"
            f"{support.replace('000000003', '000000004')}"
            "</docsSustento></comprobanteRetencion>"
        )
        rows = REPORTES.withholding_rows(ET.fromstring(xml), KEY)
        self.assertEqual(len(rows), 4)
        self.assertEqual(
            [row[16] for row in rows],
            ["000000003", "000000003", "000000004", "000000004"],
        )
        self.assertEqual(rows[0][19:23], ["001", 100, 2, 2])

    def test_withholding_v1_keeps_every_tax(self) -> None:
        xml = (
            f"<comprobanteRetencion>{ISSUER}{RETENTION_INFO}<impuestos>"
            f"<impuesto>{TAX}{SUPPORT}</impuesto>"
            f"<impuesto>{TAX}{SUPPORT}</impuesto>"
            "</impuestos></comprobanteRetencion>"
        )
        rows = REPORTES.withholding_rows(ET.fromstring(xml), KEY)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][13:17], ["01-Factura", "001", "002", "000000003"])

    def test_duplicate_xml_missing_pdf_and_wrong_month(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            kind = root / "Recibidos/Facturas"
            folder = kind / "0000000000002-Recibidos"
            folder.mkdir(parents=True)
            (kind / "0000000000002_Recibidos.txt").write_text(
                "CLAVE_ACCESO\n" + KEY + "\n"
            )
            for name in ("uno", "copia"):
                (folder / f"{name}.xml").write_text(INVOICE)
                (folder / f"{name}.pdf").write_bytes(b"%PDF-1.7\n")
            documents = REPORTES.read_month(
                root, "recibidos", "0000000000002", "facturas", 2026, 9
            )
            self.assertEqual(len(documents), 1)
            with self.assertRaisesRegex(ValueError, "fuera del mes"):
                REPORTES.read_month(
                    root, "recibidos", "0000000000002", "facturas", 2026, 8
                )
            (folder / "uno.pdf").unlink()
            with self.assertRaises(FileNotFoundError):
                REPORTES.read_month(
                    root, "recibidos", "0000000000002", "facturas", 2026, 9
                )

    def test_txt_key_without_xml_is_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            kind = root / "Recibidos/Facturas"
            kind.mkdir(parents=True)
            (kind / "0000000000002_Recibidos.txt").write_text(
                "CLAVE_ACCESO\n" + KEY + "\n"
            )
            with self.assertRaisesRegex(ValueError, "faltan 1 XML"):
                REPORTES.read_month(
                    root, "recibidos", "0000000000002", "facturas", 2026, 9
                )


if __name__ == "__main__":
    unittest.main()
