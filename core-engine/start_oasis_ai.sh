#!/bin/bash
# 🏛️ OASIS AI - VON NEUMANN CORE
# IA Optimizada para Balística y Ecuaciones Diferenciales

MODEL="../llama.cpp/models/soberano.gguf"

# Lanzamos con limitación de hilos para mantener flujo laminar
../llama.cpp/main -m $MODEL -n 128 --threads 2 -p "### Instrucción: Escribe una ecuación diferencial para calcular la trayectoria de un proceso viscoso que supera kappa=2.3 y dame el código en FORTRAN para resolverlo. ### Respuesta:"
