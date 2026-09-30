import os
import urllib.request
import json

# Recuperar la clave de RapidAPI desde las variables de entorno de la terminal
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    print("❌ Error: La variable de entorno RAPIDAPI_KEY no está configurada.")
else:
    print(f"🔑 Clave RapidAPI cargada con éxito en el entorno del Monolito.")
    print(f"   (Primeros dígitos: {RAPIDAPI_KEY[:10]}...)")
    print("🚀 Nodo listo para operar y monetizar a través del hub.")
