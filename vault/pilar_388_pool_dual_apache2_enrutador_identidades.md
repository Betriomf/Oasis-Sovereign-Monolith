# PILAR 388: POOL DUAL APACHE 2.0 Y ENRUTADOR DETERMINISTA DE IDENTIDADES

## 1. Arquitectura de Consolidación (Metodología Wafer Sort / KGD)
- **Problema resuelto:** 31 etiquetas en Ollama consumían ~45 GB de SSD (99% de capacidad) y provocaban timeouts por paginación (swap) en 8 GB de RAM.
- **Solución:** Consolidación en dos modelos base bajo licencia **Apache 2.0** (`1.38 GB` totales en disco, `15 GB` libres recuperados):
  1. `oasis-flash:0.5b` (397 MB): Absorbe `velazquez`, `qwen:flash`, `freebuff`, `lincos`, `traductor`, `auditor` y `juez-binario` (`num_ctx=512`, `repeat_penalty=1.2`, 12.9–39.1 tok/s).
  2. `oasis-sovereign:1.5b` (986 MB): Absorbe `edge`, `laminar`, `aether-soup`, `fibonacci` y `riona` (`num_ctx=1024`, `temperature=0.618`, 8.0–9.0 tok/s).

## 2. Preservación de Personalidades y Enrutamiento
- Todas las definiciones previas quedan respaldadas en `vault/qwen25_agents_backup.md` y mapeadas en `vault/oasis_agent_roles.json`.
- El Gateway (`agents_core/oasis_render_gateway.py`) inspecciona etiquetas `@agente` y palabras clave (`c99`, `rizin`, `lean 4`) para despachar cada consulta al modelo óptimo en silicio frío (<= 2.58 W).
