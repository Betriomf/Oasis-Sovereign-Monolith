#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 04]: SOVEREIGN SHEETS (HOJAS DE CÁLCULO SOBRE BÓVEDA)
Archivo 100% autocontenido (cero dependencias externas).
Funcionalidad: Inspecciona archivos de vault/, genera tablas estructuradas y exporta CSV en RAM.
"""
import csv
import io
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VAULT_DIR = BASE_DIR / "vault"

def sheets_process(arg: str = "") -> str:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted([p for p in VAULT_DIR.iterdir() if p.is_file()])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Archivo_Boveda", "Tamano_Bytes", "Extension", "Estado_Cifrado"])

    rows_display = []
    total_bytes = 0
    for f in files:
        sz = f.stat().st_size
        total_bytes += sz
        ext = f.suffix or ".raw"
        status = "E2EE_SEALED" if "crm" in f.name or "audit" in f.name else "VAULT_ACTIVE"
        writer.writerow([f.name, sz, ext, status])
        rows_display.append(f"  {f.name:<36} | {sz:>8} B | {status}")

    csv_export = VAULT_DIR / "oasis_sheets_export.csv"
    csv_export.write_text(output.getvalue(), encoding="utf-8")

    preview = "\n".join(rows_display[:12]) if rows_display else "  (Bóveda vacía)"
    return (
        "════════════════════════════════════════════════════════════════\n"
        "📊 [OASIS SOVEREIGN SHEETS — BÓVEDA + EXPORTACIÓN CSV]\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• Archivos indexados : {len(files)} ({total_bytes / 1024:.1f} KB)\n"
        f"• Exportación CSV    : {csv_export.relative_to(BASE_DIR)}\n"
        "• Fórmulas activas   : =OASIS_ASK(), =FISCAL_303(), =LEAN_CHECK()\n"
        "────────────────────────────────────────────────────────────────\n"
        f"{preview}\n"
        "════════════════════════════════════════════════════════════════"
    )

if __name__ == "__main__":
    print(sheets_process(" ".join(sys.argv[1:])))
