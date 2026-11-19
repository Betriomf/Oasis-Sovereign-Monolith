# F01 — Recuperación del Diccionario Soberano Real en Terminal Web

## 1. Objetivo y Alcance
Conectar los 22 módulos activos de `sovereign_catalog/` y el Decision Log de `vault/crm_arquitectura_soberana.json` dentro de `terminal.html`, manteniendo compatibilidad total con `[WEB TERMINAL AUDIT]`.

## 2. Criterios de Aceptación (Verificables en Preview)
- [ ] **AC-01 (`dict` / `modules`):** Lista los 22 módulos reales con su comando disparador, archivo fuente en `sovereign_catalog/` y descripción operativa.
- [ ] **AC-02 (`crm` / `decisions`):** Muestra los registros del CRM Soberano y las decisiones de arquitectura (`ADR`) sincronizadas desde `oasis_crm.py`.
- [ ] **AC-03 (`osure`):** Muestra el estado del flujo de ramas (`develop` -> `main`) y las reglas de seguridad (cero claves en cliente).
- [ ] **AC-04 (`velazquez`):** Permite consultar el Oráculo RAG en RAM o inspeccionar sus pilares activos sin romper los comandos históricos.
