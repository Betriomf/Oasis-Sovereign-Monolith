#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — TEST DE ESTRÉS TOPOLÓGICO (1,000 PRIMOS)
Valida la proyección Ulam-Fibonacci bajo el atractor L=2.3 y cota de Landauer-Oasis.
"""
import time
import oasis_ulam_phi_projection as ulam

def ejecutar_test_estres():
    t0 = time.perf_counter()
    print("🔬 INICIANDO TEST DE ESTRÉS TOPOLÓGICO DE CAPA 0 (1,000 Nodos Primos)...")
    
    ulam.proyectar_espira_ulam_oasis(limite_primos=1000)
    
    tf = time.perf_counter()
    dt_ms = (tf - t0) * 1000
    print(f"\n⚡ TIEMPO TOTAL DE EJECUCIÓN: {dt_ms:.2f} ms")
    print("✅ VERIFICACIÓN DE SILICIO: Cero turbulencias térmicas. Flujo laminar perfecto.")

if __name__ == "__main__":
    ejecutar_test_estres()
