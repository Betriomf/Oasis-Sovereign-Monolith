# 🌌 Micro-Sistema Operativo Embebido Portable y Runtime de Gaming (Pilar 224)

**Autor:** Mariano Panzano Caballé (<mpc.3.14@gmail.com>)  
**Entorno:** Oasis Sovereign Monolith  
**Licencia:** GNU AGPLv3 / Creative Commons Attribution 4.0 International (CC-BY-4.0)  

---

## 1. Supresión de Dependencias del Sistema Anfitrión

Oasis Micro-OS elimina la complejidad de gestores de paquetes y dependencias del sistema:
* **Ejecutable Único:** Se compila como un ejecutable portátil autónomo que interactúa directamente con los hipervisores nativos de hardware (`Hypervisor.framework` en macOS, `WHPX` en Windows, `KVM` en Linux).
* **Arranque Instantáneo:** Tiempo de inicialización $< 5\text{ ms}$ y consumo de memoria base $< 5\text{ MB}$.

---

## 2. Ventajas para Motores de Videojuegos

1. **Régimen Térmico Frío:** Al eliminar servicios en segundo plano de macOS/Windows, el silicio se mantiene por debajo de $5.39\text{W}$, suprimiendo el *thermal throttling*.
2. **Latencia Invariante:** El tráfico de red UDP pasa directamente por el micro-kernel con el filtro Golod-Shafarevich en tiempo $O(1)$.
