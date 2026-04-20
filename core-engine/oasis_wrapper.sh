#!/bin/bash
# 🌀 OASIS EXECUTION WRAPPER
# Lanza procesos forzando el estado laminar

riona "Iniciando proceso en modo adiabático. Sintonizando registros RAX y RCX."

# Forzamos que el proceso use solo 1 hilo (evita colisiones térmicas)
# y le damos la prioridad máxima de tiempo real
export OLLAMA_NUM_THREAD=1
nice -n -20 "$@" 

riona "Proceso finalizado. Energía reciclada."
