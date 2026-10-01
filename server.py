import os
import time
import json
import urllib.request
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Oasis Sovereign Wind API", version="1.0")

SOVEREIGN_API_KEY = os.environ.get("SOVEREIGN_API_KEY", "llave-maestra-por-defecto")

@app.get("/v1/wind-forecast")
def get_wind_data(city: str = "barcelona", x_api_key: str = Header(None)):
    if x_api_key != SOVEREIGN_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: Nodo no autorizado o firma de silicio inválida."
        )

    coords = {
        "barcelona": {"lat": 41.3879, "lon": 2.1699},
        "madrid": {"lat": 40.4168, "lon": -3.7038},
        "londres": {"lat": 51.5074, "lon": -0.1278}
    }
    
    city_lower = city.lower().strip()
    if city_lower not in coords:
        raise HTTPException(status_code=404, detail="Objetivo geográfico no registrado en el enjambre.")

    loc = coords[city_lower]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current=temperature_2m,wind_speed_10m,surface_pressure"

    try:
        # Cabecera robusta simulando un cliente corporativo legítimo
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Compatible; OasisSovereignNode/2.6; +https://oasis.network)'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())['current']
            viento = data['wind_speed_10m']

            estado = "LAMINAR (Estable)" if viento < 10.0 else "TURBULENTO (Alerta de Cizalladura)"

            return {
                "city": city.capitalize(),
                "temperature_c": data['temperature_2m'],
                "wind_speed_ms": viento,
                "surface_pressure_hpa": data['surface_pressure'],
                "oasis_fluid_status": estado,
                "attractor_kappa": 2.302585,
                "security": "Protegido por el Enjambre Oasis"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en la pasarela de red: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
