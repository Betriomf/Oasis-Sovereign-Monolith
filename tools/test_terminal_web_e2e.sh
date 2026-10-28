#!/usr/bin/env bash
# OASIS TERMINAL WEB E2E TESTER (DARWIN CLI)
# Simula las peticiones de la terminal web y valida la respuesta.

BASE="http://127.0.0.1:8080"
EXIT_CODE=0

echo "══════════════════════════════════════════════════════════════════════"
echo "🧪 SIMULADOR E2E DE COMANDOS TERMINAL WEB (VÍA CURL)"
echo "══════════════════════════════════════════════════════════════════════"

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
    echo "     Recibido: '${res:0:80}...'"
    EXIT_CODE=1
  fi
}

# 1. Simulación de comando 'hemo' (Biomarcadores)
run_test "hemo (Biomarcadores)" "/v1/med/besov-cfd" "GET" "" "tawss_peak_pa"

# 2. Simulación de comando 'mesh3d' (Geometría carotídea)
run_test "mesh3d (VMR Carótida)" "/v1/med/mesh-geometry" "GET" "" "aneurisma_carotida_vmr.vtk"

# 3. Simulación de comando 'ai' (Inferencia local)
run_test "ai explica la cota de landauer" "/v1/ai/chat" "POST" '{"prompt":"explica la cota de landauer"}' "Sub-Landauer"
run_test "ai capital de españa?" "/v1/ai/chat" "POST" '{"prompt":"capital de españa?"}' "Madrid"

# 4. Simulación de comandos de sistema
run_test "cat AUTHORS.md" "/v1/darwin/exec" "POST" '{"command":"cat AUTHORS.md"}' "AUTORÍA"
run_test "KAPPA_MARIANO.txt" "/v1/darwin/exec" "POST" '{"command":"KAPPA_MARIANO.txt"}' "MARIANO"

# 5. Simulación de auto-registro P2P
run_test "Swarm Heartbeat" "/v1/swarm/heartbeat" "POST" '{"node_id":"NODE-SIMULATED-DARWIN","device":"CLI Tester"}' "ACK"

echo "══════════════════════════════════════════════════════════════════════"
if [ $EXIT_CODE -eq 0 ]; then
  echo "🏆 TODOS LOS COMANDOS SIMULADOS DESDE DARWIN HAN RESPONDIDO AL 100%"
else
  echo "🚨 SE DETECTARON FALLOS EN LA SIMULACIÓN DE LA TERMINAL WEB"
fi
echo "══════════════════════════════════════════════════════════════════════"

exit $EXIT_CODE
