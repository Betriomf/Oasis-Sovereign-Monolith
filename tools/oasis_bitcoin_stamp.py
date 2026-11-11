#!/usr/bin/env python3
"""
OASIS BITCOIN OPENTIMESTAMPS SEALER (tools/oasis_bitcoin_stamp.py)
Genera manifiestos criptográficos SHA-256 de Capa 0 y gestiona el sellado
inmutable en la cadena de bloques de Bitcoin.
"""
import os
import hashlib
import time
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
MANIFEST_FILE = os.path.join(VAULT_DIR, "bitcoin_ots_manifest.json")

TARGET_FILES = [
    "AUTHORS.md",
    "LICENSE",
    "VERDAD_OASIS.txt",
    "vault/crm_arquitectura_soberana.json",
    "vault/bitacora_arquitectura_crm.md",
    "vault/oasis_tech_index.json",
    "tools/oasis_crm.py"
]

def calculate_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("════════════════════════════════════════════════════════════════")
    print("₿ [OASIS BITCOIN OTS]: GENERANDO SELLADO CRIPTOGRÁFICO...")
    print("────────────────────────────────────────────────────────────────")

    manifest = {
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "author": "Mariano Panzano Caballé",
        "did_key": "did:key:zOasisClinicalNode01",
        "files_sealed": {}
    }

    raw_hashes_to_stamp = []

    for rel_path in TARGET_FILES:
        full_p = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(full_p):
            f_hash = calculate_sha256(full_p)
            manifest["files_sealed"][rel_path] = f_hash
            raw_hashes_to_stamp.append(f"{f_hash}  {rel_path}")
            print(f"• SHA-256: {f_hash[:16]}... | {rel_path}")

    # Guardar manifiesto en la Bóveda
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    ots_txt = os.path.join(VAULT_DIR, "hashes_for_bitcoin.txt")
    with open(ots_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(raw_hashes_to_stamp) + "\n")

    print("────────────────────────────────────────────────────────────────")
    print(f"✅ Manifiesto generado en: {MANIFEST_FILE}")
    print(f"📄 Hashes listos para OTS en: {ots_txt}")

    # Comprobar si 'ots' está instalado en Darwin
    try:
        subprocess.run(["ots", "--version"], capture_output=True, check=True)
        print("⚡ Ejecutando sellado directo en Bitcoin Calendar Servers...")
        subprocess.run(["ots", "stamp", ots_txt], check=True)
        print(f"🏆 Sellado completado: {ots_txt}.ots listo para verificar en Bitcoin.")
    except Exception:
        print("ℹ️ Herramienta 'ots' CLI no detectada.")
        print(f"  Para completar el anclaje a Bitcoin ejecuta:")
        print(f"    pip install opentimestamps-client")
        print(f"    ots stamp {ots_txt}")

    print("════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()
