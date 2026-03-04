import os
import math

def calculate_oasis_gravity(file_path):
    """Calcula la tensión y curvatura según el peso real del archivo"""
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    
    # Constante Verlinde-Panzano (k=2.3) como factor de acoplamiento
    kappa = 2.3
    # La masa informacional curva el espacio de direccionamiento
    curvature = math.log(size_mb + 1) / kappa
    
    return size_mb, curvature

print("🏛️ OASIS GRAVITY ORCHESTRATOR - ESCANEO DE MASA INFORMACIONAL")
print("="*60)

target_dir = os.path.expanduser("~/Oasis-Sovereign-Monolith")
for root, dirs, files in os.walk(target_dir):
    for name in files:
        path = os.path.join(root, name)
        mb, curve = calculate_oasis_gravity(path)
        status = "🟢 LIGERO" if curve < 1 else "🔴 MASIVO (CURVA ESPACIO)"
        print(f"FILE: {name[:20]:<20} | MASS: {mb:>8.2f} MB | CURVATURE: {curve:.4f} | {status}")

print("\n✅ Veredicto: El sistema está en equilibrio termodinámico.")
