#!/bin/bash
echo "🏦 AUDITORÍA FINANCIERA OASIS"
STRIPE_URL=$(gh api user/sponsorship_payout_settings --jq '.stripe_connect_url' 2>/dev/null)
if [ -z "$STRIPE_URL" ]; then
    echo "⚠️  ESTADO: Portal no detectado. Verifica en GitHub Sponsors."
else
    echo "✅ ESTADO: Pasarela Vinculada."
    echo "🔗 Enlace: $STRIPE_URL"
fi
echo "🏛️  IBAN: ES36...9233"
