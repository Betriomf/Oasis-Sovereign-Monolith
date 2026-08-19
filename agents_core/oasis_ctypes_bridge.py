#!/usr/bin/env python3
import ctypes
import os
import sys
import time

lib_path = os.path.join(os.path.dirname(__file__), "..", "bin", "liboasis_golod.dylib")
if not os.path.exists(lib_path):
    lib_path = os.path.join(os.path.dirname(__file__), "..", "bin", "liboasis_golod.so")

c_lib = ctypes.CDLL(lib_path)
c_lib.validar_golod_c.argtypes = [ctypes.c_int32, ctypes.c_int32]
c_lib.validar_golod_c.restype = ctypes.c_int32

def test_ctypes_benchmark(total=1_000_000):
    print("=" * 70)
    print("🛰️ [OASIS CTYPES BRIDGE] - Invocando Binario C Nativo desde Python")
    print("=" * 70)
    
    t0 = time.perf_counter()
    aprobados = 0
    for i in range(total):
        r = i % 16
        if c_lib.validar_golod_c(r, 6):
            aprobados += 1
            
    dt = (time.perf_counter() - t0) * 1000.0
    print(f"📦 Paquetes evaluados : {total:,}")
    print(f"✅ Válidos (r>=10)    : {aprobados:,} ({(aprobados/total)*100:.2f}%)")
    print(f"⏱️ Tiempo total       : {dt:.2f} ms")
    print(f"⚡ Latencia ctypes    : {(dt/total)*1000.0:.4f} µs por llamada")
    print("=" * 70)

if __name__ == "__main__":
    test_ctypes_benchmark()
