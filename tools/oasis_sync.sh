#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🛸 [OASIS SYNC]: 1. Saneando entorno físico y Bóveda..."
[ -f vault ] && rm -f vault
mkdir -p vault data/models

echo "🛸 [OASIS SYNC]: 2. Ejecutando Suite Determinista ./verify..."
./verify

echo "🛸 [OASIS SYNC]: 3. Consolidando artefactos en Git..."
git add vault/ tools/ agents_core/ data/models/ .gitignore 2>/dev/null || true
git commit -m "chore(sync): automated deterministic checkpoint [$(date -u +'%Y-%m-%d %H:%M:%SZ')]" || true

echo "🛸 [OASIS SYNC]: 4. Sincronizando con repositorio remoto (rebase)..."
git pull --rebase origin main

echo "🛸 [OASIS SYNC]: 5. Desplegando a Render bajo auditoría Lean 4..."
git push origin main
echo "✅ Pipeline completado: Sistema 100% estable, certificado y desplegado."
