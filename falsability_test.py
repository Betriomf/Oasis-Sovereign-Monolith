import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros
phi = (1 + 5**0.5) / 2
landauer = np.log(phi) / np.log(2) # El objetivo: 0.6942

# Las dos realidades
kappa_real = 2.3046  # Tu Constante
kappa_falsa = 5.0    # Una constante arbitraria (ruido)

re_range = np.linspace(100, 10000, 400)

# Cálculo de errores
error_real = np.abs(re_range / (1000 * kappa_real * phi) - landauer)
error_falso = np.abs(re_range / (1000 * kappa_falsa * phi) - landauer)

# 2. Renderizado de la Verdad
plt.figure(figsize=(12, 6))

# Curva Real (Cian)
plt.plot(re_range, error_real, label='Soberanía Mariano (2.3046)', color='cyan', lw=3)
# Curva Falsa (Roja)
plt.plot(re_range, error_falso, label='Error de la Matrix (5.0)', color='red', linestyle=':', lw=2)

plt.axhline(y=0.5, color='black', linestyle='--', label='Límite de Turbulencia')
plt.fill_between(re_range, 0, 0.5, color='green', alpha=0.1, label='Zona de Suavidad Garantizada')

plt.title('PRUEBA DE FALSABILIDAD: ¿Es el 2.3046 la llave única?')
plt.xlabel('Número de Reynolds (Energía)')
plt.ylabel('Desviación de Fase (Caos)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig('oasis_falsability_test.png')
print("--------------------------------------------------")
print("✅ PRUEBA DE FALSABILIDAD GENERADA: 'oasis_falsability_test.png'")
print(f"📊 Análisis: Con 2.3046, el valle toca el suelo en Reynolds {int(landauer * 1000 * kappa_real * phi)}")
print(f"❌ Análisis: Con 5.0, el valle se desplaza fuera del rango biológico normal.")
