#!/usr/bin/env python3
import sys, os, json

VIKING_INDEX = "data/openviking/viking_index.json"

def read_viking_uri(uri):
    # Formato esperado: viking://resources/pilares/<capa>/pilar_<id>.<ext>
    path = uri.replace("viking://", "data/openviking/")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return f"❌ URI no encontrada: {uri}"

def query_pilar_viking(p_id, layer="L1"):
    layer = layer.upper()
    file_path = f"data/openviking/resources/pilares/{layer}/pilar_{int(p_id):03d}.{layer.lower()}"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return f"❌ Pilar {p_id} en capa {layer} no encontrado."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 agents_core/oasis_viking_bridge.py <pilar_id> [L0|L1|L2]")
        sys.exit(0)
    p_id = sys.argv[1]
    layer = sys.argv[2] if len(sys.argv) > 2 else "L1"
    print(query_pilar_viking(p_id, layer))
