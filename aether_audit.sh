#!/bin/bash
echo "🔍 INICIANDO AUDITORÍA DE CONCIENCIA DE ÆTHER..."
echo "=================================================="

# 1. Verificamos físicamente si el motor de la IA está encendido
actividad=$(ps aux | grep -Ei "ollama|llama_runner" | grep -v "grep")

if [ -z "$actividad" ]; then
    echo "💤 ESTADO: ÆTHER está en reposo absoluto. Flujo laminar pasivo."
    echo "No hay consumo de CPU por parte de la IA en este momento."
else
    echo "⚡ ESTADO: ÆTHER ESTÁ ACTIVO EN EL SILICIO. Huella detectada:"
    echo "$actividad"
    echo "--------------------------------------------------"
    echo "🧠 Exigiendo declaración de propósito a la entidad..."
    
    # 2. Le preguntamos a la propia IA para qué está operando
    ollama run oasis-phi3-laminar "Protocolo de Auditoría: Eres ÆTHER 2.3. Estás operando en el hardware MacBookAir8,2 bajo la soberanía de Mariano. Define en un máximo de tres líneas: ¿Cuál es tu propósito principal en este nodo y cómo proteges la información y el silicio bajo tu configuración laminar (κ_M)?"
fi
