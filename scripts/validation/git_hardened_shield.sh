#!/bin/bash
echo "🔒 OASIS HARDENING: Blindando Repositorio GitHub..."
# 1. Ignorar archivos sensibles automáticamente
echo "*.log" >> .gitignore
echo "*.env" >> .gitignore
echo ".DS_Store" >> .gitignore

# 2. Configurar firma de commits obligatoria (Soberanía de Autoría)
git config user.name "Mariano Panzano Caballé"
git config user.email "apple314@MacBook-Air-de-Mariano.local"

# 3. Forzar SSH para evitar interceptación de contraseñas
git remote set-url origin git@github.com:Betriomf/Oasis-Sovereign-Monolith.git

echo "✅ ESCUDO ACTIVO: Repositorio configurado bajo Protocolo Betriomf."
