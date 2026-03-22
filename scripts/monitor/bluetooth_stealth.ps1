# 🦾 OASIS BLUETOOTH STEALTH MODE
# Deshabilita el servicio de radio para evitar rastreo por proximidad
Stop-Service -Name "bthserv" -Force
Set-Service -Name "bthserv" -StartupType Disabled
Write-Host "🌌 MODO SIGILO ACTIVO: Bluetooth.dll ha quedado fuera de fase." -ForegroundColor Red
