/**
 * OASIS BIOMEDICAL 3D MESH VIEWER (Three.js WebGL Module)
 * Componente Desacoplado: Renderizado 3D de Carótida, Streamlines y TAWSS/OSI.
 * Autor: Mariano Panzano Caballé | Licencia AGPLv3 / CC-BY-4.0
 */

(function(window) {
  let scene, camera, renderer, meshObject, meshMaterial, particleSystem;
  let isDragging = false, prevMouseX = 0, prevMouseY = 0;
  let cachedGeometry = null;
  let currentMode = "tawss";
  let showParticles = true;

  function resize() {
    const container = document.getElementById("webgl-canvas-box");
    if (!container || !renderer || !camera) return;
    const w = container.clientWidth || 880;
    const h = container.clientHeight || 520;
    if (w > 0 && h > 0) {
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
  }

  function applyColors() {
    if (!cachedGeometry || !meshObject) return;
    const geom = meshObject.geometry;
    const colors = [];
    const numPts = cachedGeometry.num_nodes;
    const vals = currentMode === "tawss" ? cachedGeometry.tawss : cachedGeometry.osi;
    const minVal = currentMode === "tawss" ? 1.8 : 0.02;
    const maxVal = currentMode === "tawss" ? 9.159 : 0.45;

    for (let i = 0; i < numPts; i++) {
      const val = vals[i] !== undefined ? vals[i] : minVal;
      const norm = Math.max(0, Math.min(1, (val - minVal) / (maxVal - minVal + 1e-6)));
      const col = new THREE.Color();
      if (currentMode === "tawss") {
        col.setHSL((1.0 - norm) * 0.65, 1.0, 0.5); // Azul -> Verde -> Rojo
      } else {
        col.setHSL(0.55 + norm * 0.35, 1.0, 0.45 + norm * 0.15); // Cian -> Violeta
      }
      colors.push(col.r, col.g, col.b);
    }
    geom.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    geom.attributes.color.needsUpdate = true;
  }

  function init() {
    const container = document.getElementById("webgl-canvas-box");
    if (!container || !window.THREE) return;

    if (!renderer) {
      container.innerHTML = "";
      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x020408);

      const w = container.clientWidth || 880;
      const h = container.clientHeight || 520;

      camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
      camera.position.set(0, 20, 85);

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
      renderer.setSize(w, h);
      renderer.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer.domElement);

      // Iluminación
      scene.add(new THREE.AmbientLight(0xffffff, 0.70));
      const dirLight = new THREE.DirectionalLight(0xffffff, 0.90);
      dirLight.position.set(30, 60, 50);
      scene.add(dirLight);

      const pointLight = new THREE.PointLight(0x00e5ff, 1.2, 100);
      pointLight.position.set(-20, 10, 30);
      scene.add(pointLight);

      // Interacción de rotación táctil / ratón
      container.addEventListener("pointerdown", (e) => {
        isDragging = true;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
      });
      window.addEventListener("pointerup", () => isDragging = false);
      window.addEventListener("pointermove", (e) => {
        if (!isDragging || !meshObject) return;
        meshObject.rotation.y += (e.clientX - prevMouseX) * 0.008;
        meshObject.rotation.x += (e.clientY - prevMouseY) * 0.008;
        if (particleSystem) {
          particleSystem.rotation.y = meshObject.rotation.y;
          particleSystem.rotation.x = meshObject.rotation.x;
        }
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
      });

      // Partículas animadas de sangre (Streamlines)
      const pCount = 750;
      const pGeom = new THREE.BufferGeometry();
      const pPos = new Float32Array(pCount * 3);
      const pSpeeds = new Float32Array(pCount);
      for (let i = 0; i < pCount; i++) {
        pPos[i*3] = (Math.random() - 0.5) * 4.5;
        pPos[i*3+1] = (Math.random() - 0.5) * 4.5;
        pPos[i*3+2] = (Math.random() * 60.0) - 30.0;
        pSpeeds[i] = 0.22 + Math.random() * 0.28;
      }
      pGeom.setAttribute("position", new THREE.BufferAttribute(pPos, 3));
      particleSystem = new THREE.Points(
        pGeom,
        new THREE.PointsMaterial({ color: 0x00ffff, size: 1.5, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending })
      );
      scene.add(particleSystem);

      function animate() {
        requestAnimationFrame(animate);
        if (meshObject && !isDragging) {
          meshObject.rotation.y += 0.0025;
          if (particleSystem) particleSystem.rotation.y = meshObject.rotation.y;
        }
        if (particleSystem && showParticles) {
          const arr = particleSystem.geometry.attributes.position.array;
          for (let i = 0; i < pCount; i++) {
            arr[i*3+2] += pSpeeds[i];
            if (arr[i*3+2] > 30.0) arr[i*3+2] = -30.0;
          }
          particleSystem.geometry.attributes.position.needsUpdate = true;
        }
        renderer.render(scene, camera);
      }
      animate();
      window.addEventListener("resize", resize);
    }

    // Cargar geometría VMR desde el backend
    document.getElementById("mesh3d-status").innerText = "Cargando geometría vascular VMR...";
    fetch("/v1/med/mesh-geometry")
      .then(r => r.json())
      .then(d => {
        cachedGeometry = d;
        if (meshObject) scene.remove(meshObject);

        const geom = new THREE.BufferGeometry();
        geom.setAttribute("position", new THREE.BufferAttribute(new Float32Array(d.points), 3));
        geom.setIndex(new THREE.BufferAttribute(new Uint32Array(d.indices), 1));
        geom.computeVertexNormals();
        geom.center();

        meshMaterial = new THREE.MeshPhongMaterial({
          vertexColors: true,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.90,
          shininess: 50
        });

        meshObject = new THREE.Mesh(geom, meshMaterial);
        scene.add(meshObject);
        applyColors();
        resize();
        document.getElementById("mesh3d-status").innerText = `${d.file} (${d.num_nodes} nodos | ${d.num_triangles} triángulos)`;
      })
      .catch(e => {
        document.getElementById("mesh3d-status").innerText = "Error: " + e;
      });
  }

  // Exportar API global limpia
  window.Oasis3D = {
    open: function() {
      const m = document.getElementById("mesh3d-modal");
      if (!m) return;
      m.style.display = "flex";
      init();
      setTimeout(resize, 60);
      setTimeout(resize, 250);
    },
    close: function() {
      const m = document.getElementById("mesh3d-modal");
      if (m) m.style.display = "none";
    },
    setMode: function(m) {
      currentMode = m;
      applyColors();
    },
    toggleWireframe: function() {
      if (meshMaterial) meshMaterial.wireframe = !meshMaterial.wireframe;
    },
    toggleStreamlines: function() {
      showParticles = !showParticles;
      if (particleSystem) particleSystem.visible = showParticles;
      const b = document.getElementById("btn-streamlines");
      if (b) b.innerText = showParticles ? "🌊 STREAMLINES [ON]" : "🌊 STREAMLINES [OFF]";
    },
    loadGeometry: function(geoData) {
      cachedGeometry = geoData;
      if (meshObject && scene) scene.remove(meshObject);
      const geom = new THREE.BufferGeometry();
      geom.setAttribute("position", new THREE.BufferAttribute(new Float32Array(geoData.points), 3));
      geom.setIndex(new THREE.BufferAttribute(new Uint32Array(geoData.indices), 1));
      geom.computeVertexNormals();
      geom.center();
      meshMaterial = new THREE.MeshPhongMaterial({ vertexColors: true, side: THREE.DoubleSide, transparent: true, opacity: 0.90 });
      meshObject = new THREE.Mesh(geom, meshMaterial);
      scene.add(meshObject);
      applyColors();
      resize();
      document.getElementById("mesh3d-status").innerText = `${geoData.file} (${geoData.num_nodes} nodos)`;
    }
  };
})(window);
