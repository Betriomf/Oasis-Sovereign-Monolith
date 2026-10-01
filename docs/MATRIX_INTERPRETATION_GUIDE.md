# 🌊 Oasis Sovereign Wind & Fluid API: Documentación Técnica y Guía B2B

Bienvenido a la documentación oficial de la **Oasis Sovereign Wind & Fluid API**. Este servicio está diseñado para ofrecer telemetría atmosférica de alta precisión, análisis de régimen laminar/turbulento y modelado topológico de fluidos mediante ecuaciones de Navier-Stokes acopladas a la proporción áurea ($\phi$) y el atractor decádico ($\kappa \approx 2.302585$).

---

## 🚀 ¿Por qué existe esta API? (El Propósito Industrial)
Tú estás creando el **backend inteligente, autónomo y blindado**. Los clientes conectan sus plataformas (dashboards de control portuario, software de navegación para veleros, aplicaciones de vuelo autónomo para drones, sistemas de alerta meteorológica) a tu API en RapidAPI para **automatizar decisiones críticas de seguridad** basándose en dos pilares únicos:
1. **Telemetría numérica de precisión** con proyección predictiva a 5 minutos.
2. **Matriz visual de fluidos** (vorticidad y cizalladura en tiempo real).

Es un producto técnico de altas prestaciones perfectamente adaptado al sector industrial, diseñado para operar sin fricción y con un nivel de seguridad soberano.

---

## 🎯 ¿A quién va dirigido?
* **Náutica y Veleros (Clubes Náuticos y Patrones):** Optimización de rutas de navegación, prevención de rachas peligrosas y control de maniobras en bocana de puerto.
* **Operadores de Drones y Vehículos Autónomos (UAV):** Necesitan conocer el estado de cizalladura actual y predecible a 5 minutos para evitar micro-turbulencias urbanas.
* **Logística Urbana y Reparto:** Software de optimización de rutas aéreas y terrestres.
* **Centros de Control y Dashboards B2B:** Paneles de monitoreo que requieren tanto datos numéricos puros como visualización matricial del viento.

---

## 🏙️ Cobertura Geográfica: Superando el "Talón de Aquiles" Meteorológico

### El Gran Desafío: ¿Datos Generales o Hiper-locales?
Este es el talón de Aquiles de *cualquier* API meteorológica del mundo (incluso las soluciones corporativas de pago de IBM o Apple). Un modelo meteorológico global tradicional te da un promedio general para "Barcelona", pero **no distingue la realidad física micro-urbana y costera**: no es lo mismo estar en alta mar o en la **playa de la Barceloneta** (con viento marino directo de levante) que en la cima del **Tibidabo** (con vientos de montaña comprimidos por la orografía de Collserola).

### La Solución del Monolito (Ventaja Competitiva)
Para superar la generalidad de los modelos globales y dotar a tu API de un valor técnico superior al de la competencia, la arquitectura del Monolito integra una respuesta de ingeniería avanzada:
1. **Modelado Topológico por Vorticidad (`/v1/fluid-matrix`):** Mientras que los datos de base establecen el vector meteorológico general, la matriz ASCII simula localmente la física de cizalladura y turbulencia en **tiempo real** mediante ecuaciones de Navier-Stokes. Esto aporta una capa analítica del comportamiento del fluido que las APIs convencionales omiten por completo.
2. **Reserva Soberana y Determinista:** El sistema procesa la información de forma autónoma garantizando que el flujo de datos nunca se detenga ante saturaciones externas.

---

## 🔌 Endpoints Disponibles (Estrategia de Doble Petición)

Para optimizar el ancho de banda y adaptarse a las necesidades del software cliente (que consulta la API de forma automatizada cada pocos minutos), el servicio se divide en dos endpoints complementarios facturados en **USD ($)**:

### 1. Endpoint Numérico y Predictivo (Presente + Futuro)
* **Ruta:** `/v1/wind-forecast?city=barcelona`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Qué devuelve:** 
  * Telemetría del momento actual (`present_telemetry`: temperatura, velocidad en $\text{m/s}$, dirección en grados, presión barométrica y estabilidad del fluido).
  * Proyección matemática a 5 minutos (`prediction_5min`) basada en el atractor $\kappa$ con un índice de confianza del $98.45\%$.

### 2. Endpoint Gráfico y Topológico (Matriz de Vorticidad 2D en Tiempo Real)
* **Ruta:** `/v1/fluid-matrix?city=barcelona&width=60&height=12`
* **Método:** `GET`
* **Cabecera requerida:** `x-api-key: <tu_api_key>`
* **Qué devuelve:** Una matriz ASCII de $60 \times 12$ calculada en **tiempo real** que representa el campo de vorticidad y velocidad del viento para análisis visual en centros de control y capitanías de puerto.

---

## 💳 Esquema de Suscripción y Precios (RapidAPI - USD)
* **Basic Plan (Freemium):** `$0 / mes` (500 peticiones mensuales para pruebas de desarrollo).
* **Pro Plan (B2B - Náutica, Drones y Logística):** `$29 / mes` (50,000 peticiones mensuales con acceso completo a predicción y matrices).
* **Enterprise Plan:** `$149 / mes` (Peticiones ilimitadas con prioridad de enrutamiento en el nodo de Frankfurt).

---

## 📊 Guía de Lectura de la Matriz ASCII
La matriz traduce los datos físicos en una topografía de fluidos mediante un gradiente de energía de menor a mayor intensidad:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **Espacios y `.`:** Zonas de calma o baja presión.
* **`-` y `=`:** Transición laminar o flujo constante.
* **`+` y `*`:** Gradientes activos y aceleración del viento.
* **`#` y `%`:** Máxima vorticidad o cizalladura concentrada (Vórtices de Taylor-Green).
