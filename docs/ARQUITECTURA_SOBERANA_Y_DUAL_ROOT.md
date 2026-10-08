# 🏛️ OASIS SOVEREIGN OS — ARQUITECTURA DUAL-ROOT Y MANIFIESTO TÉCNICO

> **Versión del Kernel:** v4.8.1 (DriverMesh & Universal Ephemeral Root)  
> **Arquitectura de Cómputo:** Malla Híbrida Darwin (Apple Silicon / Metal) + Capa 0 Cloud (Frankfurt)  
> **Aislamiento Teórico:** SafeOS Círculo Negro ($k = -2.5$) & Límite Termodinámico de Landauer ($k_B T \ln \phi$)

---

## 1. El Paradigma Dual-Plane Root (Soberanía vs. Centralización)

La informática corporativa tradicional confina al usuario final a una condición subalterna: entornos sin permisos administrativos, telemetría extractiva opaca y dependencia de nubes cerradas. Oasis Sovereign OS reestructura el acceso mediante un **Doble Plano de Superusuario Desacoplado**: ---

## 2. Pila de Controladores en Espacio de Usuario (Universal Userspace Drivers)

En los kernels monolíticos (Linux, Windows NT, XNU/Darwin), los controladores de hardware residen en el espacio más privilegiado del procesador (**Ring 0**). Esta decisión acarrea una fragilidad estructural: cualquier excepción no capturada en un driver de vídeo o red desencadena un *Kernel Panic* o Pantallazo Azul.

Oasis adopta el paradigma de **micronúcleo y traductores de GNU Hurd / VirtIO**, trasladando todos los controladores a procesos aislados en espacio de usuario (**Ring 3**): ### Especificación de los 4 Drivers Clave

#### A. Driver Gráfico (Oasis-DRM / KMS Translator)
* **Nodo de Dispositivo:** `/dev/dri/card0`
* **Mecanismo:** Implementa el estándar DRM 1.4 respondiendo a `DRM_IOCTL_VERSION`, `DRM_IOCTL_MODE_CREATE_DUMB` y `DRM_IOCTL_MODE_MAP_DUMB`.
* **Memoria Lineal:** Asigna un *Dumb Buffer* en RAM contigua (1024×768 píxeles a 32 bpp = 3.145.728 bytes). 
* **Proyección Visual:** En lugar de depender de registros de GPU propietarios, la memoria se exporta a través de WebAssembly/WebGL hacia el Canvas de la terminal web, logrando 60 FPS con un consumo de 0 W en GPU dedicada.
* **Modelo GNU Hurd:** En Mach/Hurd se asocia mediante `settrans -c /dev/dri/card0 /hurd/oasis_drm`, sirviendo peticiones vía Mach IPC RPCs sin tocar el micronúcleo.

#### B. Driver de Entrada (Virtual Evdev / WebHID Multiplexer)
* **Nodo de Dispositivo:** `/dev/input/event0`
* **Mecanismo:** Captura eventos de puntero, toques en pantalla y pulsaciones de teclado en el DOM/Canvas y los serializa en estructuras binarias estándar de Linux `struct input_event` (tiempo, tipo, código, valor).
* **Compatibilidad:** Los binarios de Linux, Android (ReDroid) y Wine leen `/dev/input/event0` creyendo interactuar con un teclado USB o pantalla táctil física.

#### C. Driver de Almacenamiento (VirtIO-Block / VFS Desacoplado)
* **Nodo de Dispositivo:** `/dev/vda1`
* **Mecanismo:** Traduce llamadas POSIX de lectura/escritura (`read`, `write`, `sync`) a transacciones asíncronas sobre IndexedDB en el navegador del cliente.
* **Soberanía:** Los datos residen en el silicio del propio usuario. Para persistencia permanente del anfitrión, los bloques se sincronizan cifrados vía REST con PostgreSQL en Supabase.

#### D. Driver de Red (VirtIO-Net / WebSocket Bridge)
* **Nodo de Dispositivo:** `/dev/net/tun0`
* **Mecanismo:** Encapsula paquetes Ethernet/IP en tramas atómicas $\pi$-KB (máximo 3141 bytes) transmitidas sobre túneles seguros WebSocket/QUIC hacia el gateway en Render, brindando salida de red a los entornos sin requerir privilegios de superusuario (`CAP_NET_ADMIN`) en la máquina anfitriona.

---


## 2.1. Arquitectura de Almacenamiento Inmutable (SteamOS A/B Pattern)

Siguiendo el principio de **particionado inmutable de SteamOS 3.x**, Oasis desacopla el núcleo del sistema del espacio mutable del usuario mediante **Dual-Slot A/B con OverlayFS**:
* **Slot A / Slot B:** Dos particiones idénticas de solo lectura con verificación criptográfica dm-verity. Las actualizaciones del sistema se aplican en la ranura inactiva en segundo plano.
* **OverlayFS:** Los cambios, configuraciones y datos de usuario se almacenan en una capa superior mutable aislada, permitiendo conmutar o restaurar versiones de kernel sin pérdida de datos.


## 2.2. Matriz de Integración Científica en el Ecosistema Oasis

| Paper | Concepto Clave | Aplicación en el Modelo | Comando en la Terminal |
| :--- | :--- | :--- | :--- |
| **[1] Drifting Elliptic** | Vórtice elíptico con cizalla $\mu(\rho)$ | Dinámica en torbellinos reales acotada por $\ln 10$ | `vortex --elliptic <x> <y> <z>` |
| **[2] Existence & Smoothness** | Criterio BKM y regularidad 3D | Cota global sin blow-up para preprints | `bkm` o `lean check bkm` |
| **[3] Stability Transition** | Espacios críticos de Besov | Robustez del atractor frente a ruido entrópico | `shield` o `/v1/shield/status` |


## 2.3. Ecosistema de Proyectos Abiertos Embebidos en Oasis

| Proyecto | Naturaleza Tecnológica | Integración en la Arquitectura Oasis | Comando Web / CLI |
| :--- | :--- | :--- | :--- |
| **Conformal Gamescope** | Micro-compositor Wayland con Pacing Áureo | Superficie aislada de 640×480 reescalada a 1024×768 sin aliasing | `gamescope launch` |
| **Sunshine + Moonlight** | Streaming WebRTC de latencia $<15\text{ ms}$ | Decodificación H.264 acelerada en el navegador sin carga en la nube | `moonlight` |
| **v86 (Copy.sh)** | Emulador de PC x86 completo en WebAssembly | Arranque en caliente de FreeDOS, Alpine y sistemas clásicos en cliente | `v86 [alpine\|freedos]` |
| **JS-DOS / Dosbox** | Runtime de emulación DOS para navegador | Ejecución instantánea de videojuegos clásicos con soporte de teclado | `game [doom\|prince]` |
| **Box64 + FEX-Emu** | Traductores de instrucciones x86_64 a ARM64 | Ejecución de binarios x86 de Windows en nodos ARM económicos | `box64` o `fex` |

## 3. ¿Qué puede hacer el Visitante en el Plano 2 (Ephemeral Guest Root)?

El visitante no es un usuario limitado: dentro de su sesión disfruta de facultades completas de superusuario en su propio sandbox:

1. **Gestión de Archivos Persistente (VFS MS-DOS 2.0 & Unix):**  
   Comandos `DIR`, `SAVE`, `TYPE`, `COPY`, `DEL`, `CLS` junto a `ls`, `cat`, `touch`, `write`, `rm`. Los archivos se conservan en su propio navegador sin visibilidad para terceros.
2. **Estudio de Código en Pantalla (`edit <archivo>`):**  
   Editor interactivo superpuesto con atajo de guardado `Ctrl + S`.
3. **Inspección de Hardware y Drivers (`drivers` y `drm test`):**  
   Comprobación del bus de dispositivos y renderizado de la carta de ajuste con simulación de fluidos directamente en su Canvas WebGL.
4. **Virtualización x86 y Juegos en WASM (`v86`, `doom`, `retrotick`):**  
   Arranque de imágenes de PC x86 (FreeDOS / Alpine) y ejecución de binarios clásicos a 60 FPS dentro del navegador.
5. **Cálculo Científico Navier-Stokes (`vortex`) y Lean 4 (`lean`):**  
   Resolución de tensores de enstrofia acotados por $\kappa = \ln 10$ y verificación formal interactiva de lemas matemáticos (`elliptic`, `bkm`, `besov`, `landauer`).
6. **Enclaves de Compatibilidad (`wine` y `android`):**  
   Pruebas de binarios Win32 y paquetes APK bajo el aislamiento del Círculo Negro.

---

## 4. El Manifiesto Estratégico: Las 4 Dimensiones

### I. Privacidad (Soberanía frente a Extractivismo)
En el modelo hegemónico de computación en la nube, los datos del usuario son monetizados y analizados de forma centralizada. Oasis revierte este flujo:
* **Confinamiento en silicio:** Toda operación vive en la memoria volátil del usuario o en su almacenamiento local cifrado.
* **Telemetría no invasiva:** Las únicas señales transmitidas corresponden a magnitudes físicas y energéticas ($k_B T \ln \phi$, micro-tramas $\pi$-KB de 3141 bytes), garantizando neutralidad frente a datos personales.

### II. Seguridad (Micronúcleo Axiomático)
Los núcleos monolíticos concentran millones de líneas de código en Ring 0 con alta superficie de ataque.
* Al trasladar el **DRM, el VFS y la entrada a espacio de usuario**, cada subsistema opera como un proceso aislado. Un fallo gráfico no genera un fallo del sistema (*kernel panic*): el traductor se reinicia de manera transparente.
* La acotación analítica $\kappa = \ln 10$ formalizada en **Lean 4** sustituye la estimación empírica por demostraciones lógicas verificadas por máquina.

### III. Transformación (La Computación del Sur Global y la Descentralización Real)
Frente a infraestructuras de inteligencia artificial que concentran altos consumos eléctricos y modelos de suscripción cerrados:
* Oasis demuestra que dispositivos estándar, equipos reacondicionados y hardware ligero pueden sostener sistemas operativos funcionales y análisis científico si se optimizan bajo **silicio frío**.
* La arquitectura de red P2P transforma al usuario en un participante activo de la malla de cómputo en lugar de un consumidor dependiente.

### IV. Vida (Régimen Laminar y Tiempo Humano)
El diseño tecnológico dominante suele sobrecargar procesadores y mantener al usuario en continua reactividad.
* El principio del **silicio frío** traslada a la computación el concepto de **régimen laminar**: operar de forma fluida, estable y sin fricciones destructivas.
* Concebir sistemas que minimicen el estrés térmico del silicio protege tanto la durabilidad del hardware como la autonomía de quien lo utiliza.
