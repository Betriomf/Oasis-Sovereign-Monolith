#!/bin/bash
echo "🛡️ [OASIS SELLO DE PLOMO]: Inmutabilizando LaunchAgents parásitos..."

TARGETS=(
  "$HOME/Library/LaunchAgents/com.google.keystone.agent.plist"
  "$HOME/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist"
)

for target in "${TARGETS[@]}"; do
  if [ -f "$target" ]; then
    chmod 000 "$target"
    echo "🔒 Sello de plomo aplicado a: $(basename $target)"
  fi
done

echo "✅ Estado: Procesos zombis neutralizados a 000 (Cero CPU / Silicio Frío)."
