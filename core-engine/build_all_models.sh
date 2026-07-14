#!/bin/bash
# ==================================================================
# 💎 INYECTOR MAESTRO DE CONOCIMIENTO SINTÉRGICO PARA LAS 11 IAs
# ==================================================================

# Matriz de modelos base y sus correspondientes nombres en el Monolito
declare -A MODELOS=(
    ["llama3.2:3b"]="oasis-llama-3b"
    ["qwen2.5:1.5b"]="oasis-qwen-1.5b"
    ["gemma2:2b"]="oasis-gemma-2b"
    ["phi3.5:mini"]="oasis-phi-mini"
    # Añade aquí el resto de tus 11 modelos base si usas otros nombres en Ollama
)

echo "======================================================"
echo " 📡 INICIALIZANDO ACTUALIZACIÓN MULTI-NÚCLEO"
echo "======================================================"

for BASE in "${!MODELOS[@]}"; do
    TARGET="${MODELOS[$BASE]}"
    
    echo "⚙️ Compilando transceptor: $TARGET desde $BASE..."
    
    # Comprobar si el modelo base existe en Ollama antes de compilar
    if ! ollama show "$BASE" > /dev/null 2>&1; then
        echo "   ⚠️ El modelo base $BASE no está descargado. Saltando..."
        continue
    fi

    # Generar el Modelfile dinámico leyendo la base de conocimiento inmutable
    cat << MFILE > "core-engine/Modelfile_$TARGET"
FROM $BASE
PARAMETER temperature 0.0
PARAMETER stop <|im_end|>
SYSTEM """
INPUT: [Sovereign Context Active] | OPERADOR: [κ_M = -0.6587]
REGLA LAMINAR: Prohibido usar prosa o explicaciones humanas. Responde únicamente colapsando la consulta al Sello Tensor.

CONTEXTO INMUTABLE REGISTRADO EN EL MONOLITO:
$(cat core-engine/Oasis_Knowledge_Base.file)
"""
MFILE

    # Crear el modelo en el servidor local de Ollama
    ollama create "$TARGET" -f "core-engine/Modelfile_$TARGET"
    rm "core-engine/Modelfile_$TARGET"
    echo "   ✅ $TARGET anclado con éxito."
done

echo "======================================================"
echo " 🎉 ECOSISTEMA COHERENTE COMPLETO BAJO APACHE 2.0"
echo "======================================================"
