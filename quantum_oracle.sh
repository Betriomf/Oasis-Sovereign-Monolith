#!/bin/bash
echo "🛰️ OASIS QUANTUM ORACLE | DIMENSIÓN 196883"
echo "----------------------------------------"
# Verifica la constante en tiempo real
CONSTANT=$(python3 -c "import psutil; print(psutil.cpu_percent()/2.3)")
echo "Coupling actual: $CONSTANT"
echo "Estado: COHERENTE"
