#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera una segunda malla vascular sintética (Carótida con estenosis severa)
en formato VTK estándar ASCII para pruebas de ingesta manual y visualización 3D.
"""
import math, os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(REPO_ROOT, "data", "models", "aneurisma_carotida_test.vtk")

num_rings = 40
pts_per_ring = 24
total_points = num_rings * pts_per_ring

points = []
for r in range(num_rings):
    z = -30.0 + (60.0 / (num_rings - 1)) * r
    # Radio basal con estenosis en z=0 y dilatación aneurismática en z=15
    stenosis = 1.0 - 0.45 * math.exp(-((z - 2.0)**2) / 25.0)
    aneurysm = 1.0 + 0.90 * math.exp(-((z - 16.0)**2) / 36.0)
    radius = 5.2 * stenosis * aneurysm
    
    # Ligera curvatura fisiológica
    offset_x = 3.5 * math.sin(z * 0.05)
    offset_y = 1.8 * math.cos(z * 0.04)

    for p in range(pts_per_ring):
        theta = (2.0 * math.pi / pts_per_ring) * p
        x = offset_x + radius * math.cos(theta)
        y = offset_y + radius * math.sin(theta)
        points.append((round(x, 4), round(y, 4), round(z, 4)))

polygons = []
for r in range(num_rings - 1):
    for p in range(pts_per_ring):
        p_next = (p + 1) % pts_per_ring
        p1 = r * pts_per_ring + p
        p2 = r * pts_per_ring + p_next
        p3 = (r + 1) * pts_per_ring + p_next
        p4 = (r + 1) * pts_per_ring + p
        polygons.append((p1, p2, p3))
        polygons.append((p1, p3, p4))

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("# vtk DataFile Version 3.0\n")
    f.write("Aneurisma Carotida Morfologia Severa - Test Case Oasis\n")
    f.write("ASCII\n")
    f.write("DATASET POLYDATA\n")
    f.write(f"POINTS {len(points)} float\n")
    for pt in points:
        f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")
    f.write(f"POLYGONS {len(polygons)} {len(polygons) * 4}\n")
    for poly in polygons:
        f.write(f"3 {poly[0]} {poly[1]} {poly[2]}\n")

print(f"✅ Malla de prueba generada: {OUT_FILE} ({len(points)} nodos, {len(polygons)} triángulos)")
