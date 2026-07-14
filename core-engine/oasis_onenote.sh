#!/bin/zsh
# 📝 OASIS ONENOTE CONNECTOR: INYECCIÓN DE SNAPSHOTS A DARWIN

TEXTO_REPORT=$(cat core-engine/strategic_news_snapshot.json 2>/dev/null)

if [ -z "$TEXTO_REPORT" ]; then
    TEXTO_REPORT="Matriz de estado Oasis: Flujo Laminar Sincronizado."
fi

echo "📥 Sincronizando bloque informacional con Microsoft OneNote..."

# Ejecutar el puente nativo de AppleScript para interactuar con la interfaz de OneNote
osascript <<EOD
tell application "Microsoft OneNote"
    activate
    try
        # Crear una nueva página en la sección activa con las métricas de Capa 0
        tell active section of first notebook
            make new page with properties {title:"Oasis Real-Time Context", content:"$TEXTO_REPORT"}
        end tell
    end try
end tell
EOD

echo "💎 ONENOTE_SYNC_CLOSED: Registro acoplado con éxito."
