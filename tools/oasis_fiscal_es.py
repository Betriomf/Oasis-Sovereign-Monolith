#!/usr/bin/env python3
"""Módulo Fiscal Soberano (España): Libro Registro de Ingresos, IVA (Mod. 303) e IRPF (Mod. 130)."""
import json, sys
from datetime import datetime
from pathlib import Path

LEDGER = Path("vault/libro_fiscal_es.json")

def load_ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"titular": "Mariano Panzano Caballé", "iban": "ES36 0182 1756 1802 0152 9233", "movimientos": []}

def add_entry(concepto: str, base_imponible: float, canal: str = "Bizum/SEPA", tipo: str = "INGRESO"):
    data = load_ledger()
    iva = round(base_imponible * 0.21, 2)
    total = round(base_imponible + iva, 2)
    entry = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tipo": tipo.upper(),
        "concepto": concepto,
        "canal": canal,
        "base_eur": round(base_imponible, 2),
        "iva_21_eur": iva,
        "total_eur": total
    }
    data["movimientos"].append(entry)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return entry

def summary_report() -> str:
    data = load_ledger()
    movs = data.get("movimientos", [])
    ing_base = sum(m["base_eur"] for m in movs if m["tipo"] == "INGRESO")
    ing_iva  = sum(m["iva_21_eur"] for m in movs if m["tipo"] == "INGRESO")
    gas_base = sum(m["base_eur"] for m in movs if m["tipo"] == "GASTO")
    gas_iva  = sum(m["iva_21_eur"] for m in movs if m["tipo"] == "GASTO")

    rend_neto = round(ing_base - gas_base, 2)
    mod_303 = round(ing_iva - gas_iva, 2)
    mod_130 = round(max(0.0, rend_neto * 0.20), 2)

    return (
        "════════════════════════════════════════════════════════════════\n"
        "🧾 [OASIS FISCAL ENGINE — ESPAÑA (MOD. 303 IVA + MOD. 130 IRPF)]\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• Titular / IBAN   : {data['titular']} | {data['iban']}\n"
        f"• Operaciones reg. : {len(movs)} asientos en vault/libro_fiscal_es.json\n"
        f"• Base Ingresos    : {ing_base:.2f} € | Base Gastos Deducibles: {gas_base:.2f} €\n"
        f"• Rendimiento Neto : {rend_neto:.2f} €\n"
        f"• Modelo 303 (IVA) : {mod_303:.2f} € (Repercutido {ing_iva:.2f} € - Soportado {gas_iva:.2f} €)\n"
        f"• Modelo 130 (IRPF): {mod_130:.2f} € (20% s/ Rendimiento Neto acumulado)\n"
        "════════════════════════════════════════════════════════════════"
    )

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] in ("ingreso", "gasto"):
        e = add_entry(sys.argv[3], float(sys.argv[2]), sys.argv[4] if len(sys.argv) > 4 else "Bizum/SEPA", sys.argv[1].upper())
        print(f"✅ Asiento registrado: {e}")
    print(summary_report())
