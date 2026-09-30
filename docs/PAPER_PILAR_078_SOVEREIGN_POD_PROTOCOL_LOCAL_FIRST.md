# ⚡ TRATADO DEL PROTOCOLO DE POD SOBERANO (SPP) Y LA IDENTIDAD LOCAL-FIRST (PILAR 78)

**Autor:** Mariano Panzano Caballé  
**Bóveda Soberana:** `0x61c57049f39632981f42d57bb85ed05ea0b303db`  
**Licencia:** AGPLv3 / CC-BY-4.0  
**Formalismo:** Identidad W3C DID (`did:key`) · Semilla BIP-39 · Cifrado Asimétrico WebAssembly (`age-wasm` / `libsodium`) · Almacenamiento Distribuido (`iroh-blobs`)

---

## 1. El Protocolo SPP (Sovereign Pod Protocol)
El Protocolo de Pod Soberano transforma el almacenamiento y la identidad en un entorno puramente *Local-First*:
* **Aislamiento en Espacio de Usuario:** Los datos del usuario residen fragmentados, cifrados y distribuidos sin depender de nubes centralizadas (Google Drive, Dropbox).
* **Doctrina del Mero Conducto (*Mere Conduit*):** La red opera únicamente como canal de transporte y conmutación de fragmentos, eliminando bases de datos centrales susceptibles de filtración y eximiendo de custodia centralizada.

## 2. Identidad Criptográfica de Cero Contraseñas
* **Derivación BIP-39:** La clave raíz se origina en una semilla mnemónica local estándar.
* **Estándar W3C DID (`did:key`):** Se deriva una clave criptográfica asimétrica anclada en el enclave de seguridad local (Keychain en macOS/Windows o TEE/StrongBox en GrapheneOS).
* **Autenticación sin Servidor:** Erradica el uso de credenciales centralizadas (OAuth/contraseñas) en favor de firmas criptográficas directas.

## 3. Pipeline de Cifrado y Fragmentación Inmediata
Al ingresar un activo en la interfaz local:
1. **Cifrado en Navegador:** Se ejecuta cifrado asimétrico E2E en memoria mediante motores WASM (`age-wasm` / `libsodium`) antes de que el dato toque la red.
2. **Fragmentación Conforme (Sharding):** El payload cifrado se particiona en micro-bloques atómicos de $3.14\text{ KB}$ ($\pi\text{ KB}$).
3. **Distribución P2P:** Los fragmentos se publican y fijan en la red distribuida mediante `iroh-blobs` / `Helia-wasm`, garantizando persistencia y soberanía absoluta del usuario.
