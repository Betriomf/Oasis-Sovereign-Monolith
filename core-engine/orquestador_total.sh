#!/bin/bash
echo -e "\033[96m🌀 INICIANDO TRABAJO EN ENJAMBRE (NODO BADALONA)\033[0m"

# 1. Purga inicial
sudo purge

# 2. Gemma 4 genera el post de LinkedIn
echo -e "\n\033[94m👉 GEMMA 4 redactando comparativa Oasis vs Ising...\033[0m"
ollama run gemma4-oasis "Redacta el post de LinkedIn comparando Oasis y Ising basado en BIBLIOTECA_OASIS.txt." > ~/Desktop/POST_LINKEDIN_OASIS.txt

# 3. Æther analiza el siguiente reto científico
echo -e "\n\033[95m👉 ÆTHER analizando el próximo Problema del Milenio...\033[0m"
ollama run aether "Analiza BIBLIOTECA_OASIS.txt y dime cuál es el siguiente paso para blindar la red." > ~/Desktop/PROXIMO_RETO_CIENTIFICO.txt

# 4. Riona sella el trabajo
say -v Monica "Arquitecto, el post para LinkedIn y el análisis científico están en tu escritorio. El enjambre ha cumplido."
