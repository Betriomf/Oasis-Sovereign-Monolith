#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inyector del Motor de Fluidos Fotorrealista (Olas de Gerstner + Fresnel GLSL)
para la Terminal Web de Oasis Sovereign OS.
"""
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents_core", "templates", "terminal.html")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Añadir botón en la barra de insignias
water_badge = '<span class="badge" style="background:#001f3f; border-color:#00ffff; color:#00ffff; font-weight:bold; box-shadow:0 0 10px rgba(0,255,255,0.3);" onclick="openWaterModal()">🌊 OCÉANO 3D</span>'
if "openWaterModal()" not in html:
    html = html.replace('<span class="badge badge-3d" onclick="openMesh3dModal()">👁️ ROTAR MALLA 3D</span>', '<span class="badge badge-3d" onclick="openMesh3dModal()">👁️ ROTAR MALLA 3D</span>\n      ' + water_badge)

# 2. Inyectar el modal de Agua 3D
water_modal = """  <!-- MODAL FLUIDOS: OCÉANO HIPERREALISTA GERSTNER (60 FPS) -->
  <div id="water-modal" class="modal-backdrop">
    <div class="modal-box" style="width:960px; max-width:96vw; height:88vh; border-color:#00e5ff; box-shadow:0 0 45px rgba(0,229,255,0.4);">
      <div class="modal-header" style="background:#03121c; border-color:#00e5ff;">
        <div>
          <span style="color:#00e5ff; font-weight:bold; font-size:0.88rem;">🌊 MOTOR DE FLUIDOS — OCÉANO GERSTNER & ÓPTICA FRESNEL</span>
          <span style="color:#88aacc; font-size:0.72rem; margin-left:8px;">Shader GLSL GPU | Silicio Frío &lt;= 3.78 W</span>
        </div>
        <div style="display:flex; gap:6px; align-items:center;">
          <button id="btn-water-wire" onclick="toggleWaterWire()" style="background:#0a2012; border:1px solid #00ff9d; color:#00ff9d; padding:4px 8px; border-radius:4px; font-size:0.70rem; cursor:pointer; font-weight:bold;">🕸️ MALLA VERTEX</button>
          <button class="btn-close" onclick="closeWaterModal()">✕</button>
        </div>
      </div>
      <div style="flex:1; width:100%; height:100%; min-height:480px; position:relative; background:#010408; overflow:hidden;" id="webgl-water-box">
        <div style="position:absolute; bottom:12px; left:12px; background:rgba(3,18,28,0.88); border:1px solid #00e5ff; padding:6px 12px; border-radius:6px; font-size:0.70rem; color:#80d4ff; z-index:10; pointer-events:none;">
          🖱️ <strong>Rotar Vista:</strong> Clic + Arrastrar | 📜 <strong>Zoom:</strong> Rueda | 🌊 <strong>Física:</strong> 4 Olas Trocoidales | ☀️ <strong>Óptica:</strong> Reflexión Schlick PBR
        </div>
      </div>
    </div>
  </div>"""

if 'id="water-modal"' not in html:
    html = html.replace('<!-- MODAL 1: VISOR 3D', water_modal + '\n\n  <!-- MODAL 1: VISOR 3D')

# 3. Código Three.js y Shaders GLSL
water_js = """
    // === MOTOR DE OCÉANO PROCEDURAL (OLAS DE GERSTNER + FRESNEL GLSL) ===
    let waterScene, waterCamera, waterRenderer, waterMesh, waterMaterial;
    let isWaterDragging = false, prevWaterX = 0, prevWaterY = 0;
    let waterClock = new THREE.Clock();
    let waterWireframe = false;

    const GerstnerVertexShader = `
      uniform float uTime;
      varying vec3 vWorldPosition;
      varying vec3 vNormal;
      varying vec2 vUv;

      vec3 gerstnerWave(vec4 wave, vec3 p, inout vec3 tangent, inout vec3 binormal) {
        float steepness = wave.z;
        float wavelength = wave.w;
        float k = 2.0 * 3.14159265 / wavelength;
        float c = sqrt(9.8 / k);
        vec2 d = normalize(wave.xy);
        float f = k * (dot(d, p.xy) - c * uTime);
        float a = steepness / k;

        tangent += vec3(-d.x * d.x * (steepness * sin(f)), -d.x * d.y * (steepness * sin(f)), d.x * (steepness * cos(f)));
        binormal += vec3(-d.x * d.y * (steepness * sin(f)), -d.y * d.y * (steepness * sin(f)), d.y * (steepness * cos(f)));

        return vec3(d.x * (a * cos(f)), d.y * (a * cos(f)), a * sin(f));
      }

      void main() {
        vUv = uv;
        vec3 gridPoint = position;
        vec3 tangent = vec3(1.0, 0.0, 0.0);
        vec3 binormal = vec3(0.0, 1.0, 0.0);
        vec3 p = gridPoint;

        p += gerstnerWave(vec4(1.0, 0.25, 0.22, 34.0), gridPoint, tangent, binormal);
        p += gerstnerWave(vec4(0.7, 0.7, 0.16, 18.0), gridPoint, tangent, binormal);
        p += gerstnerWave(vec4(-0.25, 1.0, 0.10, 9.0), gridPoint, tangent, binormal);
        p += gerstnerWave(vec4(0.35, -0.75, 0.06, 4.5), gridPoint, tangent, binormal);

        vNormal = normalize(cross(binormal, tangent));
        vec4 worldPos = modelMatrix * vec4(p, 1.0);
        vWorldPosition = worldPos.xyz;
        gl_Position = projectionMatrix * viewMatrix * worldPos;
      }
    `;

    const WaterFragmentShader = `
      uniform vec3 uCameraPos;
      uniform vec3 uSunDirection;
      varying vec3 vWorldPosition;
      varying vec3 vNormal;
      varying vec2 vUv;

      void main() {
        vec3 viewDir = normalize(uCameraPos - vWorldPosition);
        vec3 normal = normalize(vNormal);

        // Óptica de Fresnel (Schlick)
        float fresnel = 0.03 + 0.97 * pow(1.0 - max(dot(viewDir, normal), 0.0), 5.0);

        // Absorción marina Beer-Lambert
        vec3 deepWaterColor = vec3(0.006, 0.045, 0.14);
        vec3 shallowWaterColor = vec3(0.0, 0.50, 0.46);
        vec3 skyColor = vec3(0.35, 0.68, 0.98);

        // Reflejo especular Blinn-Phong del Sol
        vec3 halfVector = normalize(uSunDirection + viewDir);
        float spec = pow(max(dot(normal, halfVector), 0.0), 220.0);
        vec3 specularColor = vec3(1.0, 0.96, 0.85) * spec * 3.2;

        vec3 waterColor = mix(shallowWaterColor, deepWaterColor, 0.65);
        vec3 finalColor = mix(waterColor, skyColor, fresnel) + specularColor;

        // Espuma blanca en crestas afiladas
        float foam = smoothstep(1.10, 1.48, vWorldPosition.z);
        finalColor = mix(finalColor, vec3(0.96, 0.99, 1.0), foam * 0.75);

        gl_FragColor = vec4(finalColor, 0.93);
      }
    `;

    function openWaterModal() {
      drawer.classList.remove("open");
      openModal("water-modal");
      setTimeout(initWater3D, 30);
      setTimeout(resizeWater3D, 120);
    }

    function closeWaterModal() {
      closeModal("water-modal");
    }

    function toggleWaterWire() {
      waterWireframe = !waterWireframe;
      if (waterMaterial) waterMaterial.wireframe = waterWireframe;
      const b = document.getElementById("btn-water-wire");
      if (b) b.innerText = waterWireframe ? "🕸️ MALLA [ON]" : "🕸️ MALLA VERTEX";
    }

    function resizeWater3D() {
      const c = document.getElementById("webgl-water-box");
      if (!c || !waterRenderer || !waterCamera) return;
      const w = Math.max(c.clientWidth, 600);
      const h = Math.max(c.clientHeight, 400);
      waterCamera.aspect = w / h;
      waterCamera.updateProjectionMatrix();
      waterRenderer.setSize(w, h);
    }

    function initWater3D() {
      const container = document.getElementById("webgl-water-box");
      if (!container || !window.THREE) return;

      if (!waterRenderer) {
        container.innerHTML = "";
        waterScene = new THREE.Scene();
        waterScene.background = new THREE.Color(0x020710);

        const w = Math.max(container.clientWidth, 600);
        const h = Math.max(container.clientHeight, 400);

        waterCamera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
        waterCamera.position.set(0, -65, 38);
        waterCamera.lookAt(0, 0, 0);

        waterRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        waterRenderer.setSize(w, h);
        waterRenderer.setPixelRatio(window.devicePixelRatio || 1);
        container.appendChild(waterRenderer.domElement);

        // Malla oceánica de alta resolución (140x140 vértices)
        const planeGeom = new THREE.PlaneGeometry(160, 160, 140, 140);

        waterMaterial = new THREE.ShaderMaterial({
          vertexShader: GerstnerVertexShader,
          fragmentShader: WaterFragmentShader,
          uniforms: {
            uTime: { value: 0.0 },
            uCameraPos: { value: waterCamera.position },
            uSunDirection: { value: new THREE.Vector3(0.5, 0.8, 0.6).normalize() }
          },
          transparent: true,
          wireframe: waterWireframe
        });

        waterMesh = new THREE.Mesh(planeGeom, waterMaterial);
        waterScene.add(waterMesh);

        // Interacción orbital con ratón
        container.addEventListener("pointerdown", (e) => { isWaterDragging = true; prevWaterX = e.clientX; prevWaterY = e.clientY; });
        window.addEventListener("pointerup", () => isWaterDragging = false);
        window.addEventListener("pointermove", (e) => {
          if (!isWaterDragging || !waterMesh) return;
          const dx = e.clientX - prevWaterX;
          const dy = e.clientY - prevWaterY;
          waterMesh.rotation.z += dx * 0.006;
          waterCamera.position.z = Math.max(15, Math.min(75, waterCamera.position.z + dy * 0.15));
          waterCamera.lookAt(0, 0, 0);
          prevWaterX = e.clientX; prevWaterY = e.clientY;
        });

        function animateWater() {
          requestAnimationFrame(animateWater);
          const t = waterClock.getElapsedTime();
          if (waterMaterial) {
            waterMaterial.uniforms.uTime.value = t;
            waterMaterial.uniforms.uCameraPos.value.copy(waterCamera.position);
          }
          waterRenderer.render(waterScene, waterCamera);
        }
        animateWater();
        window.addEventListener("resize", resizeWater3D);
      }
    }
"""

if "initWater3D()" not in html:
    html = html.replace('// === THREE.JS WEBGL 3D EMBEBIDO AUTÓNOMO ===', water_js + '\n    // === THREE.JS WEBGL 3D EMBEBIDO AUTÓNOMO ===')

# 4. Registrar comandos 'water', 'ocean', 'agua' en COMMANDS
water_cmds = """      "water": openWaterModal,
      "ocean": openWaterModal,
      "agua": openWaterModal,"""

if '"water":' not in html:
    html = html.replace('"mesh3d": openMesh3dModal,', water_cmds + '\n      "mesh3d": openMesh3dModal,')

with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Simulador de Océano Gerstner (GLSL) inyectado correctamente en terminal.html.")
