#!/usr/bin/env bash
# 📱 OASIS ANDROID / TERMUX BUILDER
set -e

echo "==============================================================="
echo "📱 [OASIS ANDROID/TERMUX ENGINE] - Compilación Nativa"
echo "==============================================================="

mkdir -p bin
if command -v clang &> /dev/null; then
    clang -O3 agents_core/oasis_golod_core.c -o bin/oasis_golod_android_standalone -Wall
    echo "✅ Binario nativo para Termux/Android generado en: bin/oasis_golod_android_standalone"
    ./bin/oasis_golod_android_standalone 2>/dev/null || true
else
    echo "⚠️ Clang no está instalado. Ejecuta: pkg install clang -y (en Termux)"
fi
