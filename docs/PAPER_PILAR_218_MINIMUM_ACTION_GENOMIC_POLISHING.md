# 🧬 Principio de Mínima Acción en Faseo Genómico y Pulido Diploide (Pilar 218)

**Autor:** Mariano Panzano Caballé (<mpc.3.14@gmail.com>)  
**Entorno:** Oasis Sovereign Monolith  
**Licencia:** GNU AGPLv3 / Creative Commons Attribution 4.0 International (CC-BY-4.0)  

---

## 1. El Colapso de Falsa Homocigosidad como Mínimo Local

En regiones con identidad >99%, lecturas cortas (<25kb) colapsan ambos alelos en una secuencia homocigota artificial:
$$\Delta L_{\text{lectura}} < L_{\text{duplicación}} \implies \text{Colapso de Fase en Grafo}$$

---

## 2. Resolución por Mínima Acción con PHARAOH y UL-ONT

El uso de lecturas ultra-largas (>100kb) restablece la frontera de fase flanqueante:
$$S_{\text{óptimo}} = \min_{H \in \{H_1, H_2\}} \int \mathcal{D}_{\text{Edlib}}(R_{\text{HiFi}}, H) \, ds$$
Permite a DeepPolisher corregir errores residuales invisibles para análisis convencionales de $k$-mers (Merqury) a $P \le 5.39\text{W}$.
