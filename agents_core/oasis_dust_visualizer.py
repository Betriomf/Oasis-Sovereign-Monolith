#!/usr/bin/env python3
"""
OASIS DUST VISUALIZER ENGINE (Pilar 150)
Visualizador Jerárquico de Espacio en Disco estilo 'dust' (bootandy/dust)
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import os
import sys
from pathlib import Path

def calcular_tamano_nodo(ruta: Path) -> int:
    if not ruta.exists():
        return 0
    if ruta.is_file() or ruta.is_symlink():
        try:
            return ruta.stat().st_size
        except Exception:
            return 0
    total = 0
    for root, _, files in os.walk(ruta):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except Exception:
                pass
    return total

def formatear_tamano(bytes_cant: int) -> str:
    if bytes_cant >= 1024 * 1024 * 1024:
        return f"{bytes_cant / (1024**3):>6.2f} GB"
    elif bytes_cant >= 1024 * 1024:
        return f"{bytes_cant / (1024**2):>6.1f} MB"
    elif bytes_cant >= 1024:
        return f"{bytes_cant / 1024:>6.1f} KB"
    return f"{bytes_cant:>6} B"

def render_dust(ruta_base: Path, profundidad_max: int = 2):
    print("=" * 75)
    print(f"🌌 [OASIS DUST VISUALIZER]: Mapeo Topológico de Disco en '{ruta_base}'")
    print("=" * 75)

    tamano_raiz = calcular_tamano_nodo(ruta_base)
    if tamano_raiz == 0:
        print("Carpeta vacía o sin permisos de lectura.")
        return

    elementos = []
    try:
        for item in ruta_base.iterdir():
            sz = calcular_tamano_nodo(item)
            if sz > 1024 * 1024:  # Filtrar entradas mayores a 1 MB
                elementos.append((item, sz))
    except Exception as e:
        print(f"Error al listar: {e}")
        return

    elementos.sort(key=lambda x: x[1], reverse=False)

    for item, sz in elementos:
        porcentaje = (sz / tamano_raiz) * 100
        ancho_barra = int((porcentaje / 100) * 25)
        barra = "█" * ancho_barra + "░" * (25 - ancho_barra)
        print(f"{formatear_tamano(sz)} | {barra} | {porcentaje:>5.1f}% | 📂 {item.name}")

    print("-" * 75)
    print(f"📦 VOLUMEN TOTAL: {formatear_tamano(tamano_raiz)} | Nodos analizados: {len(elementos)}")
    print("=" * 75)

if __name__ == "__main__":
    target = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path(".")
    render_dust(target)
