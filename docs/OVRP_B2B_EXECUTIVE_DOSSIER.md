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
- **Recuperación en Grafo (`Graphity`):** Consulta de dependencias y evidencias en `< 2 ms` sin invocar modelos pesados.
- **Verificación Formal (`Lean 4.36.0`):** Certificación mecánica de invariantes y teoremas con `0 errors, 0 warnings, 0 sorry, 0 custom axioms`.
- **Ejecución Determinista (`C99`):** Motores numéricos y sanitizadores de memoria (`ASan`/`UBSan`) capaces de auditar 100 paquetes en `0.6420 ms` (`6.42 µs`/paquete) en hardware ligero (`≤ 2.58 W`).
- **Notarización Criptográfica Dual:** Huellas `SHA-256`, anclaje temporal en Bitcoin (`OpenTimestamps`) y archivo permanente con DOI del CERN (Zenodo).

## 3. Evidencia Empírica Publicada (7 DOIs en Zenodo)
- **Serie Física Matemática (`SU(3)` Lattice Gauge Theory):** DOIs `24383187`, `24383399`, `24383530`, `24442236`, `24442403`.
- **Arquitectura OVRP:** DOI `24443531`.
- **Termodinámica Informacional Acotada y Silicio Frío:** DOI `24443786`.

## 4. Servicios y Modelos de Licenciamiento Comercial
1. **Auditoría Formal de Invariantes y Código Crítico (C99 / Rust / Algoritmos):** Entrega de especificación verificada en Lean 4 + batería C99 + certificado SHA-256/OTS.
2. **Despliegue de Nodos Soberanos On-Premise:** Instalación de tuberías de verificación locales sin fuga de datos a la nube.
3. **Licencia Comercial OVRP:** Cesión de uso comercial sobre la arquitectura publicada bajo `CC-BY-NC-4.0`.
