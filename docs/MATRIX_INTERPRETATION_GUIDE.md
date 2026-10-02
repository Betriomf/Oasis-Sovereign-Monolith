# 🌐 Oasis Sovereign Wind & Fluid API - Official Documentation

## 🚀 Overview
The **Oasis Sovereign Wind & Fluid API** is a high-performance, deterministic fluid dynamics engine deployed on Render and integrated with global meteorological mesh networks (NOAA, ECMWF, Met Office via Open-Meteo). It combines real-world ground truth telemetry with Navier-Stokes mathematical attractors ($\kappa \approx 2.302585$, $\phi = 1.6180339$).

---

## 🛰️ Core Endpoints

### 1. Global Advanced Forecast (`/v1/advanced-forecast`)
* **Method:** `GET`
* **Parameters:** `lat` (float), `lon` (float), `minutes` (int, default: 15), `width` (int), `height` (int)
* **Headers:** `x-api-key: oasis_sec_99887766554321`
* **Description:** Queries real-time meteorological data for **any exact coordinates on Earth**, runs the Navier-Stokes wave pacer, and returns **dual vertical ASCII matrix visualizations** (Current Reality stacked above Future Prediction) alongside strict numerical telemetry.

### 2. Fluid Vorticity Matrix (`/v1/fluid-matrix`)
* **Method:** `GET`
* **Parameters:** `city` (string), `width` (int), `height` (int), `time_offset` (string/int)
* **Headers:** `x-api-key: oasis_sec_99887766554321`
* **Description:** Generates custom topology matrices representing wind shear and rotational energy fields in real-time or arbitrary time offsets.

### 3. Classic Telemetry (`/v1/wind-forecast`)
* **Method:** `GET`
* **Parameters:** `city` (string), `minutes` (int)
* **Headers:** `x-api-key: oasis_sec_99887766554321`
* **Description:** Standard lightweight telemetry endpoint for urban centers with confidence scoring.

---

## 📊 ASCII Matrix Energy Gradient Guide
The matrices translate physical wind vectors into an energy-intensity ASCII topology:

$$[ ] \longrightarrow \mathbf{.} \longrightarrow \mathbf{:} \longrightarrow \mathbf{-} \longrightarrow \mathbf{=} \longrightarrow \mathbf{+} \longrightarrow \mathbf{*} \longrightarrow \mathbf{\#} \longrightarrow \mathbf{\%}$$

* **Spaces & `.`:** Calm zones or low-pressure cores.
* **`-` & `=`:** Laminar flow or constant velocity transitions.
* **`+` & `*`:** Active gradients and wind acceleration zones.
* **`#` & `%`:** Maximum vorticity, shear, or concentrated kinetic energy (Taylor-Green vortices).

---

## 💳 Subscription & Pricing Tiers (RapidAPI - USD)
* **Basic Plan (Freemium):** `$0 / mes` (500 monthly requests for development).
* **Pro Plan (B2B - Drones, Maritime & Logistics):** `$29 / mes` (50,000 monthly requests with full access to global coordinates and dual ASCII projections).
* **Enterprise Plan:** `$149 / mes` (Unlimited requests with Frankfurt edge routing priority).
