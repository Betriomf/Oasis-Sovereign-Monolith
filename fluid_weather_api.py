import urllib.request
import json
import math
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Atmospheric Fluid Dynamics & Turbulence API",
    description="Real-time Navier-Stokes shear, vorticity, and turbulence metrics for UAVs and wind energy.",
    version="1.0.0"
)

class FluidMetrics(BaseModel):
    latitud: float
    longitud: float
    temperatura_c: float
    viento_base_kmh: float
    viento_rafaga_kmh: float
    cizalladura_vertical_s1: float
    estimacion_enstrofia: float
    indice_turbulencia: str
    uav_flight_risk_score: float

def calcular_fluidos_atmosfericos(v_base, v_gust, temp):
    u0 = v_base / 3.6
    u_gust = v_gust / 3.6
    delta_z = 10.0  # Medición a 10 metros de superficie
    
    # Gradiente vertical de velocidad (Cizalladura aproximada du/dz)
    shear_rate = abs(u_gust - u0) / delta_z
    
    # Viscosidad cinemática del aire ajustada por temperatura (Sutherland simplificada)
    nu = 1.5e-5 * ((temp + 273.15) / 293.15) ** 1.5
    
    # Enstrofia local aproximada (0.5 * omega^2)
    vorticidad_estimada = shear_rate * 1.4142
    enstrofia = 0.5 * (vorticidad_estimada ** 2)
    
    # Puntuación de riesgo de 0 a 100
    risk = min(100.0, (shear_rate * 40.0) + (enstrofia * 20.0))
    
    if risk < 25:
        categoria = "Laminar / Seguro"
    elif risk < 60:
        categoria = "Cizalladura Moderada"
    else:
        categoria = "Turbulencia Severa / Riesgo Blow-up"
        
    return round(shear_rate, 4), round(enstrofia, 4), categoria, round(risk, 2)

@app.get("/v1/turbulence", response_model=FluidMetrics)
def get_turbulence(
    lat: float = Query(41.3888, description="Latitud (ej. Barcelona: 41.3888)"),
    lon: float = Query(2.1590, description="Longitud (ej. Barcelona: 2.1590)")
):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    req = urllib.request.Request(url, headers={"User-Agent": "OasisFluid/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            current = data.get("current_weather", {})
            temp = current.get("temperature", 20.0)
            viento = current.get("windspeed", 10.0)
            # Ráfaga estimada si no está presente
            rafaga = viento * 1.35
    except Exception:
        raise HTTPException(status_code=502, detail="Error al consultar datos atmosféricos")

    shear, enstrophy, estado, riesgo = calcular_fluidos_atmosfericos(viento, rafaga, temp)
    
    return FluidMetrics(
        latitud=lat,
        longitud=lon,
        temperatura_c=temp,
        viento_base_kmh=viento,
        viento_rafaga_kmh=round(rafaga, 1),
        cizalladura_vertical_s1=shear,
        estimacion_enstrofia=enstrophy,
        indice_turbulencia=estado,
        uav_flight_risk_score=riesgo
    )
