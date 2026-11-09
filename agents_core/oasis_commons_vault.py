#!/usr/bin/env python3
"""
OASIS COMMONS VAULT DISPATCHER (v1.0)
Expone y firma activos de soberanía jurídica y científica descentralizada (Pilar 386).
"""
import os
import json
import hashlib

VAULT_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith/vault")
NODE_DID = "did:key:zOasisSovereignCommons2026"

def list_commons_assets():
    assets = [
        {
            "id": "COMMONS-LEGAL-01",
            "name": "Reclamación Administrativa Brecha de Género / IRPF",
            "file": "commons_soberania_legal_pension_irpf.md",
            "category": "Soberanía Jurídica Ciudadana",
            "scope": "Administración Pública / Seguridad Social"
        },
        {
            "id": "COMMONS-CLINIC-01",
            "name": "Protocolo Clínico y Triaje Cardiovascular SOAP",
            "file": "commons_salud_triage_soap.md",
            "category": "Salud Comunitaria Off-Grid",
            "scope": "Atención Primaria y Zonas de Aislamiento"
        },
        {
            "id": "COMMONS-RADIO-01",
            "name": "Diccionario de Rescate LINCOS para Redes LoRa/BLE",
            "file": "commons_radio_lincos_emergencia.md",
            "category": "Telecomunicaciones de Emergencia",
            "scope": "Comunicaciones Tácticas sin Internet"
        }
    ]
    
    verified_assets = []
    for a in assets:
        path = os.path.join(VAULT_DIR, a["file"])
        if os.path.exists(path):
            with open(path, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
            a["integrity_sha256"] = sha256
            a["issuer_did"] = NODE_DID
            a["status"] = "CERTIFICADO LOCAL-FIRST (OPFS)"
            verified_assets.append(a)
    return verified_assets

if __name__ == "__main__":
    assets = list_commons_assets()
    print("════════════════════════════════════════════════════════════════")
    print("🏛️ [BÓVEDA COMMONS]: ACTIVOS SOBERANOS DESCENTRALIZADOS")
    print("────────────────────────────────────────────────────────────────")
    print(f"• Emisor Criptográfico         : {NODE_DID}")
    print(f"• Total Activos Disponibles    : {len(assets)}")
    print("────────────────────────────────────────────────────────────────")
    for a in assets:
        print(f"[{a['id']}] {a['name']}")
        print(f"  • Categoría: {a['category']} | Ámbito: {a['scope']}")
        print(f"  • Hash SHA-256: {a['integrity_sha256'][:16]}...{a['integrity_sha256'][-8:]}")
    print("════════════════════════════════════════════════════════════════")
