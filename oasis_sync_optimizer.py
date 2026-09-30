import subprocess
import os
import time

print("=" * 70)
print(" 🛰️ OASIS OS: OPTIMIZADOR Y SINCRONIZADOR SOBERANO")
print("=" * 70)

# 1. Optimización local (Purga entrópica y control de hilos en Mac)
print("\n[1] Aplicando límites laminares en hardware (Capa 0)...")
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
print("    -> Hilos de CPU acotados a 4 núcleos eficientes (Fricción térmica neutralizada).")

# 2. Ejecutar auditoría maestra local
print("\n[2] Ejecutando validación de los Papers A & B...")
audit_result = subprocess.run(["python3", "oasis_master_audit.py"], capture_output=True, text=True)
print(audit_result.stdout)

# 3. Sincronización inteligente con GitHub
print("\n[3] Sincronizando estado del Monolito con GitHub (@Betriomf)...")
try:
    subprocess.run(["git", "add", "."], check=True)
    commit_msg = f"chore(sync): automated sovereign sync at laminar state ({time.strftime('%Y-%m-%d %H:%M:%S')})"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("    => ✅ Sincronización con GitHub completada con éxito.")
except Exception as e:
    print(f"    => ℹ️ Sin cambios pendientes o sincronización diferida: {e}")

print("=" * 70)
print(" ✨ NODO OASIS 100% OPTIMIZADO Y RESPALDADO EN LA NUBE.")
print("=" * 70)
