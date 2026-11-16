#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 06]: CALCULADORA FISCAL PRIVADA (LOCAL-FIRST / RAM ONLY)
- 0 conexiones externas (nunca conecta con AEAT ni terceros).
- 0 almacenamiento en servidor (los datos viven solo en la sesión E2EE del usuario).
- Calcula estimaciones orientativas de IVA (Mod. 303, 21%) e IRPF (Mod. 130, 20%).
"""
import re
import sys

def fiscal_process(prompt: str = "") -> str:
    txt = prompt.strip()
    # Extraer ingresos y gastos si el usuario los pasa (ej: "fiscal ingresos 3000 gastos 500")
    m_ing = re.search(r"ingresos?\s*[:=]?\s*(\d+(?:[.,]\d+)?)", txt, re.I)
    m_gas = re.search(r"gastos?\s*[:=]?\s*(\d+(?:[.,]\d+)?)", txt, re.I)

    if not m_ing:
        nums = re.findall(r"\d+(?:[.,]\d+)?", txt)
        ingresos = float(nums[0].replace(",", ".")) if len(nums) >= 1 else 2500.0
        gastos = float(nums[1].replace(",", ".")) if len(nums) >= 2 else 400.0
    else:
        ingresos = float(m_ing.group(1).replace(",", "."))
        gastos = float(m_gas.group(1).replace(",", ".")) if m_gas else 0.0

    iva_repercutido = round(ingresos * 0.21, 2)
    iva_soportado = round(gastos * 0.21, 2)
    resultado_303 = round(iva_repercutido - iva_soportado, 2)

    rendimiento_neto = max(0.0, ingresos - gastos)
    pago_130 = round(rendimiento_neto * 0.20, 2)
    liquido_disponible = round(ingresos - gastos - max(0.0, resultado_303) - pago_130, 2)

    return (
        "════════════════════════════════════════════════════════════════\n"
        "🔒 [SIMULADOR FISCAL PRIVADO — MÓDULO 06 (SOLO EN TU RAM)]\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• Base Ingresos Trimestre : {ingresos:,.2f} €\n"
        f"• Base Gastos Deducibles  : {gastos:,.2f} €\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• IVA Repercutido (21%)   : +{iva_repercutido:,.2f} €\n"
        f"• IVA Soportado (21%)     : -{iva_soportado:,.2f} €\n"
        f"👉 Estimación Mod. 303    : {resultado_303:,.2f} €\n"
        f"👉 Estimación Mod. 130    : {pago_130:,.2f} € (20% s/ {rendimiento_neto:,.2f} €)\n"
        f"💰 Liquidez Neta Estimada : {liquido_disponible:,.2f} €\n"
        "────────────────────────────────────────────────────────────────\n"
        "🛡️ PRIVACIDAD: Cálculo volátil 100% offline. Ningún dato se guarda\n"
        "   en servidor ni se envía a Hacienda. Uso: 'fiscal 4200 650'\n"
        "════════════════════════════════════════════════════════════════"
    )

if __name__ == "__main__":
    print(fiscal_process(" ".join(sys.argv[1:])))
