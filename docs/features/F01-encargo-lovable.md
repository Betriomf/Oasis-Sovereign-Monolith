# Encargo de Construcción F01 — Interfaz Web Oasis Sovereign OS (Para Lovable.dev)

## 1. Contexto y Arquitectura (`product-setup` / `product-builder`)
Construir el panel web interactivo de **Oasis Sovereign OS** conectado al repositorio `Betriomf/Oasis-Sovereign-Monolith` (desarrollo en rama `develop`, promoción a `main` solo por Pull Request).
- **Seguridad estricta:** Cero claves privadas, tokens o `service_role` en el cliente ni en el repositorio. Toda configuración de endpoint local (`http://127.0.0.1:8080`) se lee desde variables de entorno (`VITE_OASIS_RPC_URL`) con modo lectura autónomo desde `web_dictionary_manifest.json`.

## 2. Vistas y Funcionalidades Reales (Contra Ficha F01)
1. **Consola Unificada (Terminal Web + RPC):**
   - Mantiene todos los comandos históricos (`help`, `boveda`, `c99`, `v <pregunta>`, `crm`, `pool`, `agents`, `minkowski`, `sec`).
   - Añade comandos conectados al catálogo real: `dict` / `modules` (lista los módulos reales de `sovereign_catalog/`), `decisions` / `adr` (lee el Decision Log fusionado con `vault/crm_arquitectura_soberana.json`), `papers` (muestra los 12 DOIs de Zenodo hasta `10.5281/zenodo.24347447`) y `osure` (estado de sincronización con `osure618`).
   - El panel `DEVFRAME RPC` envía `POST /api/rpc` con manejo limpio de estado conectado/desconectado.
2. **Explorador del Diccionario Soberano (22+ Módulos):**
   - Tabla buscable generada desde `web_dictionary_manifest.json` con nombre del módulo, archivo fuente (`sovereign_catalog/01..22`), resumen operativo y botón de ejecución rápida en consola.
3. **CRM & Product-Builder Decision Log:**
   - Vista cronológica de `eras_historicas`, `hoja_de_ruta_hitos` y decisiones de arquitectura (`ADR`) con estado de verificación.
4. **Archivo Científico (12 DOIs Zenodo + Lean 4 `0 sorry`):**
   - Tarjetas con enlace directo a Zenodo (`10.5281/zenodo.24347447` y precedentes), módulos `.lean` sellados y recibos Bitcoin OpenTimestamps.
