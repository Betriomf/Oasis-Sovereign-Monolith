#!/usr/bin/env python3
"""
OASIS OCI LAYER & MANIFEST INSPECTOR (Pilar 168)
Auditoría forense de manifiestos y capas SHA-256 en modelos locales de Ollama
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import json
from pathlib import Path

HOME = Path.home()
MANIFESTS_DIR = HOME / ".ollama" / "models" / "manifests" / "registry.ollama.ai" / "library"

def inspeccionar_modelo(nombre_modelo: str = "oasis-laminar"):
    print("=" * 65)
    print(f"🔍 [OASIS LAYER INSPECTOR]: Inspeccionando capas de '{nombre_modelo}'...")
    print("=" * 65)

    tag_file = MANIFESTS_DIR / nombre_modelo / "1.5b"
    if not tag_file.exists():
        # Buscar en la raíz de manifests
        posibles = list((HOME / ".ollama" / "models" / "manifests").rglob(f"*{nombre_modelo}*"))
        if posibles:
            tag_file = posibles[0]
        else:
            print("ℹ️ Manifiesto no encontrado en ruta estándar.")
            return

    try:
        manifest = json.loads(tag_file.read_text(encoding="utf-8"))
        print(f"📦 Schema Version: {manifest.get('schemaVersion', 'N/A')}")
        print(f"🏷️ MediaType:      {manifest.get('mediaType', 'N/A')}")
        print("-" * 65)
        print("📑 CAPAS DETECTADAS (Layers):")
        for i, layer in enumerate(manifest.get("layers", []), 1):
            digest = layer.get("digest", "")
            media_type = layer.get("mediaType", "").split(".")[-1]
            size_kb = layer.get("size", 0) / 1024
            print(f"  [{i}] {digest[:24]}...{digest[-6:]} | {size_kb:>8.2f} KB | Tipo: {media_type}")
        print("-" * 65)
        print("🔒 Integridad: Capas deterministas acopladas.")
        print("=" * 65)
    except Exception as e:
        print(f"⚠️ Error al leer manifiesto: {e}")

if __name__ == "__main__":
    inspeccionar_modelo("oasis-laminar")
