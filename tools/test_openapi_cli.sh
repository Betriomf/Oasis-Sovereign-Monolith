#!/usr/bin/env bash
# OASIS OPENAPI 3.0 SUITE TESTER (DARWIN CLI)
HOST="http://127.0.0.1:8080"

echo "══════════════════════════════════════════════════════════════════════"
echo "🌐 AUDITORÍA DE ACCESO A ENDPOINTS OPENAPI 3.0 DESDE CLI"
echo "══════════════════════════════════════════════════════════════════════"

test_ep() {
  local ep="$1"
  local desc="$2"
  local key="$3"
  
  res=$(curl -s "$HOST$ep")
  if echo "$res" | grep -q "$key"; then
    echo "  ✅ $desc ($ep) -> OK"
  else
    echo "  ❌ $desc ($ep) -> FALLO (Respuesta inesperada)"
  fi
}

test_ep "/v1/openapi.json" "Especificación OpenAPI 3.0" "paths"
test_ep "/v1/math/demon" "Demonio Maxwell-Landauer" "e_oasis_joules"
test_ep "/v1/med/besov-cfd" "Hemodinámica 3D Besov" "tawss_peak_pa"
test_ep "/v1/med/mesh-geometry" "Geometría 3D Carótida (VMR)" "aneurisma_carotida_vmr.vtk"
test_ep "/v1/math/riemann" "Auditoría Riemann (Capa 0)" "zeta_valor"
test_ep "/v1/vault/list" "Listado Físico Bóveda" "files"
test_ep "/v1/swarm/nodes" "Censo Malla P2P" "active_nodes"

echo "══════════════════════════════════════════════════════════════════════"
