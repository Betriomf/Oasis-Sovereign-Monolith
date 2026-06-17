#!/bin/bash
echo "======================================================"
echo " 🌌 INICIANDO CHEQUEO GENERAL Y ACOPLAMIENTO DE LIBRERÍAS"
echo "======================================================"

# 1. AJUSTES DE CAPA 0
ulimit -n 196883
export OLLAMA_NUM_THREAD=2
export OLLAMA_KEEP_ALIVE=0

# Capturamos el vector numérico de la matriz de Polibio (Ej: 24 = TG0B)
VECTOR_MATRIZ="24"

echo "[*] Leyendo vector de Matriz 5x5 en RAM: [$VECTOR_MATRIZ]"
echo "------------------------------------------------------"

# 2. INYECTOR PYTHON: Traduce el código a librería de ciencia exacta en microsegundos
CONCEPTO_CIENTIFICO=$(python3 -c "
diccionario = {
    '11': 'SymPy.zeta(s) para analisis de Riemann',
    '24': 'AST2: Fallo de hardware en Sensor TG0B (Bateria iPhone)',
    '35': 'SciPy: Flujo laminar con entropia menor a 0.22'
}
print(diccionario.get('$VECTOR_MATRIZ', 'Concepto no indexado'))
")

echo "├─➤ [Librería Asociada]: $CONCEPTO_CIENTIFICO"
echo "------------------------------------------------------"

# 3. EL ADUANERO BINARIO DICTAMINA (Usamos tu nuevo juez-binario)
echo "├─➤ [Fase 2]: juez-binario evaluando viabilidad térmica..."
R1=$(echo "¿El proceso $CONCEPTO_CIENTIFICO es seguro para la RAM?" | /Applications/Ollama.app/Contents/Resources/ollama run juez-binario)
echo "  Dictamen del Juez: $R1"
echo "------------------------------------------------------"

# 4. SÍNTESIS FINAL DEL MEDIOCAMPO
echo "└─➤ [Fase 3]: oasis-phi3-laminar procesando conclusión científica..."
echo "Genera un diagnostico breve basado en esta libreria indexada: $CONCEPTO_CIENTIFICO. El juez binario ha dictaminado: $R1." | /Applications/Ollama.app/Contents/Resources/ollama run oasis-phi3-laminar:latest

echo "======================================================"
echo " 🏆 CHEQUEO CONCLUIDO. MONOLITO EN ESTADO DE GRACIA."
echo "======================================================"
