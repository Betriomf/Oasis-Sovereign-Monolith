#!/usr/bin/env python3
"""
OASIS APFS SNAPSHOT & PURGABLE SPACE RECLAIMER (Pilar 164)
Eliminación determinista de snapshots locales de Time Machine y purga APFS
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import re

def purgar_apfs():
    print("=" * 65)
    print("🧹 [OASIS APFS RECLAIMER]: Purgando snapshots locales y espacio ciego...")
    print("=" * 65)

    # 1. Listar snapshots locales
    res = subprocess.run(["tmutil", "listlocalsnapshots", "/"], capture_output=True, text=True)
    snapshots = re.findall(r"com\.apple\.TimeMachine\.[\d\-]+", res.stdout)

    if snapshots:
        print(f"📸 Snapshots detectados: {len(snapshots)}")
        for snap in snapshots:
            fecha = snap.split(".")[-1]
            print(f"  • Purgando snapshot: {snap}...")
            subprocess.run(["tmutil", "deletelocalsnapshots", fecha], capture_output=True)
        print("✅ Snapshots locales eliminados.")
    else:
        print("ℹ️ No se detectaron snapshots locales retenidos.")

    # 2. Auditar espacio final disponible en Data
    df_out = subprocess.getoutput("df -H /System/Volumes/Data | tail -n 1").split()
    if len(df_out) >= 4:
        total, usado, libre = df_out[1], df_out[2], df_out[3]
        print("-" * 65)
        print(f"📊 [CAPACIDAD REAL DATA]: Total: {total} | Usado: {usado} | Libre Real: {libre}")
    print("=" * 65)

if __name__ == "__main__":
    purgar_apfs()
