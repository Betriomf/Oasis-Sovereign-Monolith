# Oasis Verifiable Research Pipeline (OVRP) — Dossier Ejecutivo B2B

**Autor y Titular de PI:** Mariano Panzano Caballé (Barcelona, España)  
**Publicación Canónica:** [DOI: 10.5281/zenodo.24443531](https://doi.org/10.5281/zenodo.24443531) (Licencia `CC-BY-NC-4.0`)

## 1. Problema que Resuelve
Las organizaciones que adoptan inteligencia artificial y modelos cuantitativos complejos enfrentan tres riesgos críticos:
1. **Alucinaciones deductivas y errores silenciosos** en código C/C++, modelos financieros y sistemas de control.
2. **Falta de trazabilidad y auditoría legal** sobre qué datos, hipótesis y versiones produjeron un resultado.
3. **Costes energéticos y computacionales desorbitados** por depender de grandes clústeres GPU.

## 2. Solución Tecnológica (Arquitectura OVRP)
OVRP desacopla la generación asistida por IA de la certificación determinista en cinco capas auditables:
- **Recuperación en Grafo (`Graphity`):** Consulta de dependencias y evidencias en `1.36 ms` sin invocar modelos pesados.
- **Verificación Formal (`Lean 4.36.0`):** Certificación mecánica de invariantes y teoremas con `0 errors, 0 warnings, 0 sorry, 0 custom axioms`.
- **Ejecución Determinista (`C99`):** Motores numéricos y sanitizadores de memoria (`ASan`/`UBSan`) validados con más de `75.000` mutaciones en RAM (`libcurl` + `SQLite`) con `0 crashes` en hardware ligero (`≤ 2.58 W`).
- **Notarización Criptográfica Dual:** Huellas `SHA-256`, anclaje temporal en Bitcoin (`OpenTimestamps`) y archivo permanente con DOI del CERN (Zenodo).

## 3. Evidencia Empírica Publicada (11 DOIs Oficiales en Zenodo — `CC-BY-NC-4.0`)
1. **Paper V (Poincaré–MassGap Bridge):** `10.5281/zenodo.24383187`
2. **Paper W (Bakry–Émery → Poincaré):** `10.5281/zenodo.24383399`
3. **Paper X (Uniform Curvature Continuum Reduction):** `10.5281/zenodo.24383530`
4. **Paper Y (Curvature–Entropy Margin & C99 Wilson Bridge, Pilar 389):** `10.5281/zenodo.24442236`
5. **Paper Z (Discrete Ricci–Entropic Evolution & Series T–Z Closure):** `10.5281/zenodo.24442403`
6. **Paper OVRP (Oasis Verifiable Research Pipeline & Methodology):** `10.5281/zenodo.24443531`
7. **Paper Informational Thermodynamics (Laws 0–3 & Cold Silicon):** `10.5281/zenodo.24443786`
8. **Paper String Spectrum & Regge Bounds (Lean 4 & C99):** `10.5281/zenodo.24448235`
9. **Paper OVRP Audit of RH Lean 4 & Critical-Line Scan:** `10.5281/zenodo.24463308`
10. **Paper Discrete Entropic Gravity Model (Lean 4 & C99):** `10.5281/zenodo.24464014`
11. **Paper Entropic Gradient Inversion & Repulsive Lattice Dynamics (Lean 4 & C99):** `10.5281/zenodo.24464245`

## 4. Servicios y Modelos de Licenciamiento Comercial
1. **Auditoría Formal de Invariantes y Código Crítico (C99 / Rust / Algoritmos):** Entrega de especificación verificada en Lean 4 + batería C99 ASan/UBSan + certificado SHA-256/OTS.
2. **Despliegue de Nodos Soberanos On-Premise:** Instalación de tuberías de verificación locales sin fuga de datos a la nube.
3. **Licencia Comercial OVRP:** Cesión de uso comercial sobre la arquitectura y corpus publicados bajo `CC-BY-NC-4.0`.
