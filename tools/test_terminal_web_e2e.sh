#!/usr/bin/env bash
# OASIS TERMINAL WEB E2E TESTER (DARWIN CLI)
# Simula las peticiones de fetch() enviadas por el navegador y verifica la respuesta.

BASE="http://127.0.0.1:8080"
EXIT_CODE=0

echo "═" * 70
echo "🧪 SIMULADOR E2E DE COMANDOS TERMINAL WEB (VÍA CURL)"
echo "═" * 70

run_test() {
  local name="$1"
  local url="$2"
  local method="$3"
  local data="$4"
  local expect="$5"

  if [ "$method" = "POST" ]; then
    res=$(curl -s -X POST "$BASE$url" -H "Content-Type: application/json" -d "$data")
  else
    res=$(curl -s "$BASE$url")
  fi

  if echo "$res" | grep -q "$expect"; then
    echo "  ✅ [WEB CLI] $name -> OK"
  else
    echo "  ❌ [WEB CLI] $name -> FALLO"
    echo "     Esperado: '$expect'"
    echo "     Recibido: '${res:0:90}...'"
    EXIT_CODE=1
  fi
}

# 1. Simulación de comando 'bench' / 'hemo' (APIs de datos biomecánicos)
run_test "hemo (Biomarcadores)" "/v1/med/besov-cfd" "GET" "" "tawss_peak_pa"

# 2. Simulación de comando 'mesh3d' (Carga de geometría carotídea)
run_test "mesh3d (VMR Carótida)" "/v1/med/mesh-geometry" "GET" "" "aneurisma_carotida_vmr.vtk"

# 3. Simulación de comando 'ai <pregunta>' (Inferencia RAG local)
run_test "ai explica la cota de landauer" "/v1/ai/chat" "POST" '{"prompt":"explica la cota de landauer"}' "Sub-Landauer"
run_test "ai capital de españa?" "/v1/ai/chat" "POST" '{"prompt":"capital de españa?"}' "Madrid"

# 4. Simulación de comando POSIX 'cat AUTHORS.md' (vía /v1/darwin/exec)
run_test "cat AUTHORS.md" "/v1/darwin/exec" "POST" '{"command":"cat AUTHORS.md"}' "AUTORÍA"

# 5. Simulación de comando de documento 'KAPPA_MARIANO.txt'
run_test "KAPPA_MARIANO.txt" "/v1/darwin/exec" "POST" '{"command":"KAPPA_MARIANO.txt"}' "KAPPA"

# 6. Simulación de auto-registro P2P (?peer=...)
run_test "Swarm Heartbeat (Malla)" "/v1/swarm/heartbeat" "POST" '{"node_id":"NODE-SIMULATED-DARWIN","device":"CLI Tester"}' "ACK"

echo "═" * 70
if [ $EXIT_CODE -eq 0 ]; then
  echo "🏆 TODOS LOS COMANDOS SIMULADOS DESDE DARWIN HAN RESPONDIDO AL 100%"
else
  echo "🚨 SE DETECTARON FALLOS EN LA SIMULACIÓN DE LA TERMINAL WEB"
fi
echo "═" * 70

exit $EXIT_CODE
