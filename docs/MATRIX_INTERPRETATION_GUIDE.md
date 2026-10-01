# 🌊 Oasis Sovereign Wind & Fluid API: Documentación Técnica y Guía B2B

Bienvenido a la documentación oficial de la **Oasis Sovereign Wind & Fluid API**. Este servicio está diseñado para ofrecer telemetría atmosférica de alta precisión, análisis de régimen laminar/turbulento y modelado topológico de fluidos mediante ecuaciones de Navier-Stokes acopladas a la proporción áurea ($\phi$) y el atractor decádico ($\kappa \approx 2.302585$).

---

## 🎯 ¿A quién va dirigido?
* **Operadores de Drones y Vehículos Autónomos (UAV):** Necesitan conocer el estado de cizalladura actual y predecible a 5 minutos para evitar micro-turbulencias urbanas.
* **Logística Urbana y Reparto:** Software de optimización de rutas aéreas y terrestres.
* **Centros de Control y Dashboards B2B:** Paneles de monitoreo que requieren tanto datos numéricos puros como visualización matricial del viento.

---

## 🏙️ Cobertura Geográfica: Barcelona y Área Metropolitana
La API evalúa nodos geolocalizados clave. Es importante destacar que **el viento no es homogéneo**:
* **Efecto Costa / Litoral:** Frentes marinos con mayor componente direccional abierta.
* **Efecto Valle y Collserola:** Obstáculos orográficos que comprimen las líneas de corriente, generando aceleraciones locales de cizalladura respecto al llano de la ciudad.
El nodo central procesa el vector representativo del sector metropolitano optimizado para las coordenadas de Barcelona ($41.3879^\circ\text{ N}, 2.1699^\circ\text{ E}$).

---

## 🔌 Endpoints Disponibles (Estrategia de Doble Petición)

Para optimizar el ancho de banda, la API se divide en dos endpoints complementarios que los clientes pueden consumir según sus necesidades:

### 1. Endpoint Numérico y Predictivo (Presente + Futuro)
* **Ruta:** `/v1/wind-forecast?city=barcelona`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Qué devuelve:** 
  * Telemetría del momento actual (`present_telemetry`: temperatura, velocidad en $\text{m/s}$, dirección en grados, presión barométrica y estabilidad del fluido).
  * Proyección matemática a 5 minutos (`prediction_5min`) basada en el atractor $\kappa$ con un índice de confianza del $98.45\%$.
  * Metadatos físicos del Monolito y guía de interpretación.

### 2. Endpoint Gráfico y Topológico (Matriz de Vorticidad 2D)
* **Ruta:** `/v1/fluid-matrix?city=barcelona&width=60&height=12`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Qué devuelve:** Una matriz ASCII de $60 \times 12$ que representa el campo de vorticidad y velocidad del viento en tiempo real.

---

## 📊 Guía de Lectura de la Matriz ASCII
La matriz traduce los datos físicos en una topografía de fluidos mediante un gradiente de energía de menor a mayor intensidad:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **Espacios y `.`:** Zonas de calma o baja presión.
* **`-` y `=`:** Transición laminar o flujo constante.
* **`+` y `*`:** Gradientes activos y aceleración del viento.
* **`#` y `%`:** Máxima vorticidad o cizalladura concentrada (Vórtices de Taylor-Green).
