# 🛰️ Sistema Operativo con Kernel Linux e Init de IA Autoejecutable (Pilar 225)

**Autor:** Mariano Panzano Caballé (<mpc.3.14@gmail.com>)  
**Entorno:** Oasis Sovereign Monolith  
**Licencia:** GNU AGPLv3 / Creative Commons Attribution 4.0 International (CC-BY-4.0)  

---

## 1. Arquitectura del Sistema

* **Kernel Base:** Linux LTS estándar para compatibilidad de controladores gráficos y periféricos.
* **Capa 0 en Kernel (eBPF):** Filtrado de paquetes de red y supresión de colisiones en tiempo $O(1)$ sin recompilar el núcleo.
* **Init con IA (PID 1):** Proceso de arranque ligero que carga un modelo de lenguaje local para la gestión de recursos y optimización de juegos en hardware frío ($P \le 5.39\text{W}$).
