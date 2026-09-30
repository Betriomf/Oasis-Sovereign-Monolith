# ⚡ Compilación de Mínima Acción y Silicio Frío (Pilar 230)

**Autor:** Mariano Panzano Caballé (<mpc.3.14@gmail.com>)  
**Entorno:** Oasis Sovereign Monolith  
**Licencia:** GNU AGPLv3 / Creative Commons Attribution 4.0 International (CC-BY-4.0)  

---

## 1. Principios de Compilación Ultraligera

* **Unity Builds:** Inclusión modular en una única unidad de traducción para evitar el parseo redundante de archivos de cabecera.
* **Operación en RAM (`-pipe` / `/tmp`):** Supresión de accesos intermedios a disco SSD, reduciendo el desgaste y la latencia.
* **Optimización Térmica:** Mantener el uso de CPU confinado para evitar el *thermal throttling* ($P \le 5.39	ext{W}$).
