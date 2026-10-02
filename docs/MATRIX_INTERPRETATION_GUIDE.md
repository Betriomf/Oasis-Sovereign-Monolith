# 🌐 Oasis Sovereign Wind & Fluid API — Documentación Oficial

## 🚀 Arquitectura del Sistema
El **Oasis Sovereign Wind & Fluid API** es un motor de dinámica de fluidos de alto rendimiento desplegado en Render. Combina telemetría en tiempo real con atractores matemáticos de Navier-Stokes ($\kappa \approx 2.302585$, $\phi = 1.6180339$).

### Características Principales del Monolito:
* **Geolocalización Planetaria Real:** La API no está atada a una sola ciudad; acepta cualquier coordenada de latitud y longitud del planeta (desde Nueva York o Londres hasta la Antártida o la Playa de Icària en Barcelona).
* **Fusión Híbrida Inteligente:** Conecta en tiempo real con redes meteorológicas mundiales a través de Open-Meteo y las cruza al instante con el atractor matemático y modelos de respaldo autónomos para evitar caídas en zonas polares o remotas.
* **Doble Gráfico ASCII en Cascada Vertical:** El servidor devuelve simultáneamente dos matrices topográficas vectoriales (la realidad actual y la proyección matemática al minuto u hora que elijas), permitiendo ver la evolución del viento a simple vista en la terminal.
* **Resiliencia y Despliegue en la Nube:** Sistema automatizado, securizado con cabeceras privadas (`x-api-key`), sincronizado en GitHub y volando en producción en Render.

---

## 🛰️ Endpoints Principales

### 1. Global Advanced Forecast (`/v1/advanced-forecast`)
* **Método:** `GET`
* **Parámetros:** `lat` (float), `lon` (float), `minutes` (int, por defecto: 15), `width` (int), `height` (int)
* **Cabecera requerida:** `x-api-key: oasis_sec_99887766554321`
* **Descripción:** Consulta datos meteorológicos en tiempo real para cualquier coordenada del planeta, ejecuta el modelo de Navier-Stokes y devuelve **doble matriz ASCII en cascada vertical** (Realidad actual sobre Predicción futura) junto con la telemetría numérica y la hora local matemática.

### 2. Fluid Vorticity Matrix (`/v1/fluid-matrix`)
* **Método:** `GET`
* **Parámetros:** `city` (string), `width` (int), `height` (int), `time_offset` (string/int)
* **Cabecera requerida:** `x-api-key: oasis_sec_99887766554321`
* **Descripción:** Genera matrices topográficas personalizadas que representan el campo de vorticidad y velocidad del viento en tiempo real o con desfases temporales arbitrarios.

### 3. Classic Telemetry (`/v1/wind-forecast`)
* **Método:** `GET`
* **Parámetros:** `city` (string), `minutes` (int)
* **Cabecera requerida:** `x-api-key: oasis_sec_99887766554321`
* **Descripción:** Endpoint ligero de telemetría urbana con puntuación de confianza y metadatos físicos.

---

## 📊 Guía de Lectura de la Matriz ASCII
Las matrices traducen los vectores de viento físicos en una topografía de energía e intensidad:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **Espacios y `.`:** Zonas de calma o núcleos de baja presión.
* **`-` y `=`:** Transición laminar o flujo de velocidad constante.
* **`+` y `*`:** Gradientes activos y zonas de aceleración del viento.
* **`#` y `%`:** Máxima vorticidad, cizalladura o energía cinética concentrada (Vórtices de Taylor-Green).

---

## 💳 Esquema de Suscripción y Precios (RapidAPI - USD)
* **Basic Plan (Freemium):** `$0 / mes` (500 peticiones mensuales para desarrollo).
* **Pro Plan (B2B - Drones, Náutica y Logística):** `$29 / mes` (50,000 peticiones mensuales con acceso total a coordenadas globales y gráficos duales en cascada).
* **Enterprise Plan:** `$149 / mes` (Peticiones ilimitadas con prioridad de enrutamiento en el nodo de Frankfurt).
