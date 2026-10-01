# 🌊 Oasis Sovereign Wind & Fluid API: Documentación Técnica y Guía B2B

Bienvenido a la documentación oficial de la **Oasis Sovereign Wind & Fluid API**. Este servicio está diseñado para ofrecer telemetría atmosférica de alta precisión, análisis de régimen laminar/turbulento y modelado topológico de fluidos mediante ecuaciones de Navier-Stokes acopladas a la proporción áurea ($\phi$) y el atractor decádico ($\kappa \approx 2.302585$).

---

## 🚀 ¿Por qué existe esta API? (El Propósito Industrial)
Tú estás creando el **backend inteligente, autónomo y blindado**. Los clientes conectan sus plataformas (dashboards de control portuario, software de navegación para veleros, aplicaciones de vuelo autónomo para drones, sistemas de alerta meteorológica) a tu API en RapidAPI para **automatizar decisiones críticas de seguridad** basándose en dos pilares únicos:
1. **Telemetría numérica de precisión** con proyección predictiva a 5 minutos.
2. **Matriz visual de fluidos en tiempo real y proyectada a minutos arbitrarios** (vorticidad y cizalladura).

---

## 🔌 Endpoints Disponibles y Cómo Consumirlos

### 1. Endpoint Numérico y Predictivo (Presente + Futuro)
* **Ruta:** `/v1/wind-forecast?city=barcelona&minutes=5`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Cómo usarlo:** El cliente puede cambiar el parámetro `minutes` (ej. `minutes=15`) para obtener la proyección matemática exacta calculada por el atractor $\kappa$.

### 2. Endpoint Gráfico y Topológico (Matriz ASCII con Desfase Temporal)
* **Ruta:** `/v1/fluid-matrix?city=barcelona&width=60&height=12&time_offset=now`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Cómo usarlo (Muy fácil para el cliente):**
  * Para ver la matriz del **presente (ahora)**: 
    `.../v1/fluid-matrix?city=barcelona&time_offset=now` (o `time_offset=0`)
  * Para ver la proyección de la matriz a **cualquier número de minutos en el futuro**: El cliente solo tiene que escribir los minutos deseados en el parámetro. Por ejemplo, para ver el viento de dentro de 15 minutos:
    `.../v1/fluid-matrix?city=barcelona&time_offset=15`
    O para ver dentro de 1 hora:
    `.../v1/fluid-matrix?city=barcelona&time_offset=60`

---

## 💳 Esquema de Suscripción y Precios (RapidAPI - USD)
* **Basic Plan (Freemium):** `$0 / mes` (500 peticiones mensuales).
* **Pro Plan (B2B - Náutica, Drones y Logística):** `$29 / mes` (50,000 peticiones mensuales con acceso a predicción y matrices arbitrarias).
* **Enterprise Plan:** `$149 / mes` (Peticiones ilimitadas con prioridad de enrutamiento en Frankfurt).

---

## 📊 Guía de Lectura de la Matriz ASCII
La matriz traduce los datos físicos en una topografía de fluidos mediante un gradiente de energía de menor a mayor intensidad:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **Espacios y `.`:** Zonas de calma o baja presión.
* **`-` y `=`:** Transición laminar o flujo constante.
* **`+` y `*`:** Gradientes activos y aceleración del viento.
* **`#` y `%`:** Máxima vorticidad o cizalladura concentrada (Vórtices de Taylor-Green).
