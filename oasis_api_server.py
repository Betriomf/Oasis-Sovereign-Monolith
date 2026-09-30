from fastapi import FastAPI, HTTPException
import urllib.request
import json

app = FastAPI(title="Oasis Sovereign Fluid & Weather API", version="1.0")

@app.get("/v1/forecast")
def get_fluid_forecast(city: str = "barcelona"):
    city_lower = city.lower().strip()
    
    # Coordenadas de prueba
    coords = {
        "barcelona": {"lat": 41.3879, "lon": 2.1699},
        "madrid": {"lat": 40.4168, "lon": -3.7038},
        "londres": {"lat": 51.5074, "lon": -0.1278}
    }
    
    if city_lower not in coords:
        raise HTTPException(status_code=404, detail="Ciudad no soportada en el nodo actual.")
        
    loc = coords[city_lower]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current=temperature_2m,wind_speed_10m,surface_pressure"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OasisAPIGateway/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())['current']
            viento = data['wind_speed_10m']
            
            # Aplicar la lógica del Monolito (Atractor decádico y estabilidad)
            estado = "LAMINAR (Estable)" if viento < 10.0 else "TURBULENTO (Alerta cizalladura)"
            
            return {
                "city": city.capitalize(),
                "temperature_c": data['temperature_2m'],
                "wind_speed_ms": viento,
                "surface_pressure_hpa": data['surface_pressure'],
                "oasis_fluid_status": estado,
                "attractor_kappa": 2.302585,
                "node_power_watts": 3.81
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
