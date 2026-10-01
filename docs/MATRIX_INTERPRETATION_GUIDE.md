# 🌊 Oasis Sovereign Fluid Matrix: Guía Oficial de Interpretación

Esta documentación está diseñada para ingenieros, operadores de drones, centros de control urbano y desarrolladores que consumen el endpoint `/v1/fluid-matrix` de la **Oasis Sovereign Wind & Fluid API**.

---

## 1. ¿Qué es la Matriz ASCII de Fluidos?
La matriz ASCII es una representación discreta 2D del **campo de vorticidad y densidad de velocidad del viento** ($60 \text{ columnas} \times 12 \text{ filas}$) calculada para nodos urbanos (como Barcelona) mediante el modelado de ondas de Navier-Stokes acopladas a la constante áurea ($\phi$) y el atractor decádico ($\kappa \approx 2.302585$).

## 2. La Escala de Intensidad (Gradiente de Energía)
Los caracteres de la matriz no son decorativos; representan la densidad de energía rotacional y fricción del aire de menor a mayor intensidad:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **[Espacios] y `.` (Puntos):** Zonas de calma, baja intensidad o núcleo de baja presión (mínima fricción).
* **`-` y `=`:** Zonas de transición laminar o flujo constante.
* **`+` y `*`:** Zonas de gradiente activo y aceleración del viento.
* **`#` y `%`:** Zonas de máxima vorticidad, cizalladura o energía cinética concentrada.

## 3. Topología Física de la Matriz
Al analizar las 12 filas devueltas por la API, se identifican tres estructuras físicas clave:
1. **Ojo del Vórtice / Zona de Calma:** Áreas centrales despejadas rodeadas por bordes de alta densidad (`%%%%` y `######`), simulando núcleos estables en capas atmosféricas.
2. **Frentes de Fase (Líneas de Corte):** Líneas continuas de `=` que representan frentes de onda horizontales con potencial de velocidad constante.
3. **Vórtice de Taylor-Green Cerrado:** Núcleos concentrados de `%` rodeados simétricamente por `#`, `*`, `+` y `=`, indicando dónde la energía del viento alcanza su pico local antes de disiparse.
