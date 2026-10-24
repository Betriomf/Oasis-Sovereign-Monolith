#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS OS — AUDITORÍA, MARCA DE AGUA Y SELLADO CRIPTOGRÁFICO DE DATASET
Inyecta canarios de datos, verifica la estructura y genera la firma SHA-256.
"""

import os
import json
import hashlib
import time

def process_dataset():
    base_dir = os.path.expanduser("~/Oasis-Sovereign-Monolith")
    input_file = os.path.join(base_dir, "datasets_lean/oasis_lean4_formal_reasoning.jsonl")
    output_file = os.path.join(base_dir, "datasets_lean/oasis_lean4_watermarked.jsonl")
    manifest_file = os.path.join(base_dir, "MANIFIESTO_DATASET_LEAN4.sha256")

    if not os.path.exists(input_file):
        print(f"🚨 Error: No se encuentra el archivo {input_file}")
        return

    author_signature = "Mariano Panzano Caballé (@Betriomf) | Oasis Sovereign Monolith"
    valid_count = 0
    watermarked_records = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            
            # 1. Inyectar marca de agua en metadatos y sistema
            data["metadata"]["author"] = author_signature
            data["metadata"]["watermark_id"] = hashlib.sha256(f"{data['metadata']['pilar']}:{author_signature}".encode()).hexdigest()[:16]
            data["metadata"]["timestamp"] = int(time.time())
            
            watermarked_records.append(data)
            valid_count += 1

    # 2. Guardar dataset protegido
    with open(output_file, "w", encoding="utf-8") as f:
        for record in watermarked_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 3. Calcular Hash SHA-256 del paquete completo
    with open(output_file, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # 4. Generar Manifiesto de Integridad
    manifest_content = (
        f"==========================================================\n"
        f"🌌 OASIS SOVEREIGN OS — MANIFIESTO CRIPTOGRÁFICO DE DATASET\n"
        f"==========================================================\n"
        f"• Archivo Dataset : datasets_lean/oasis_lean4_watermarked.jsonl\n"
        f"• Total Teoremas  : {valid_count}\n"
        f"• Firma Autoría   : {author_signature}\n"
        f"• Billetera Akash : akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y\n"
        f"• Hash SHA-256    : {file_hash}\n"
        f"• Licencia        : Dual Open-Core (AGPLv3) / Comercial B2B\n"
        f"==========================================================\n"
    )

    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write(manifest_content)

    print(manifest_content)
    print(f"✅ Dataset protegido con marca de agua guardado en: {output_file}")
    print(f"🔒 Manifiesto sellado en: {manifest_file}")

if __name__ == "__main__":
    process_dataset()
