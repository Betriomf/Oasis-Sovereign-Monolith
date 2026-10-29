# CONTRATO DE SOBERANÍA Y CONFIGURACIÓN DEL NODO OASIS

**Licencia de Código:** GNU AGPLv3 / MIT Open Infrastructure  
**Doctrina Legal:** Mero Conducto (Mere Conduit — Directiva 2000/31/CE & DMCA 512)  
**Hardware Vinculado:** `OASIS-HW-MAC-87B34287C3` (Soulbound to Metal)  
**Cota Termodinámica:** Sub-Landauer (<= 3.78 W / Flujo Laminar)  

---

### 1. Software Libre e Infraestructura Neutra
Oasis Sovereign OS actúa exclusivamente bajo la doctrina del Mero Conducto: es una red P2P neutra y descentralizada que transporta y almacena fragmentos binarios matemáticamente ofuscados sin inspección central ni intermediarios comerciales.

### 2. Soberanía y Custodia Criptográfica Radical
El operador del nodo es el único custodio de su par de claves (Ed25519) y frases semilla. No existen puertas traseras ni servidores centrales de recuperación; la clave privada reside sellada en el enclave de silicio local.

### 3. Filtro de Cuarentena en RAM y DenyList Ciega
Todo archivo procesado en el buzón P2P pasa por un escáner heurístico aislado en memoria volátil (`quarantine_pass: true`) y contraste de hashes ciegos contra listas de denegación axiomática antes de permitir su persistencia o fragmentación en la malla.

### 4. Aislamiento en Espacio de Usuario (Círculo Negro)
Los complementos analíticos y procesos de IA operan confinados en sandboxes WASM sin permisos de superusuario, imposibilitando la alteración o vulneración del sistema operativo anfitrión.
