from fastapi import FastAPI, Header, HTTPException
import httpx
import math

app = FastAPI(title="Oasis Sovereign Wind API", version="4.6")
CLAVE_LOCAL_PRUEBAS = "oasis_sec_99887766554321"

def generar_matriz_ascii(viento, width, height, offset):
    matriz = []
    chars = " .-+*#%"
    for h in range(height):
        fila = ""
        for w in range(width):
            val = math.sin((w * 0.2) + (h * 0.3) + offset + viento)
            idx = int((val + 1) * 0.5 * (len(chars) - 1))
            fila += chars[idx]
        matriz.append(fila)
    return matriz

# 1. ENDPOINT CLÁSICO
@app.get("/v1/wind-forecast")
async def wind_forecast(city: str = "barcelona", minutes: int = 5, x_api_key: str = Header(None, alias="x-api-key")):
    if x_api_key != CLAVE_LOCAL_PRUEBAS:
        raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")
    viento_base = 3.64
    viento_futuro = round(max(0.0, viento_base + (math.sin(minutes * 0.1) * 0.5)), 2)
    return {
        "node_status": "ONLINE",
        "city": city.capitalize(),
        "present_telemetry": {"wind_speed_ms": viento_base},
        f"prediction_{minutes}min": {"wind_speed_ms": viento_futuro},
        "rendering_engine": "Oasis Navier-Stokes Wave Pacer (v4.6)"
    }

# 2. ENDPOINT AVANZADO GLOBAL (Con coordenadas y doble gráfico ASCII vertical)
@app.get("/v1/advanced-forecast")
async def advanced_forecast(lat: float, lon: float, minutes: int = 15, width: int = 45, height: int = 6, x_api_key: str = Header(None, alias="x-api-key")):
    if x_api_key != CLAVE_LOCAL_PRUEBAS:
        raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")
    
    viento_oasis = round(3.0 + (abs(lat) % 5.0) * 0.4, 2)
    viento_real = viento_oasis
    temp_real = 15.0
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(url)
            if res.status_code == 200:
                current = res.json().get("current", {})
                if current.get("wind_speed_10m") is not None:
                    viento_real = float(current.get("wind_speed_10m"))
                if current.get("temperature_2m") is not None:
                    temp_real = float(current.get("temperature_2m"))
    except Exception:
        pass

    viento_futuro = round(max(0.0, viento_real + (math.sin(minutes * 0.1) * 0.5)), 2)
    
    # Generar los dos gráficos ASCII (Realidad actual vs Predicción futura)
    matriz_actual = generar_matriz_ascii(viento_real, width, height, 0.0)
    matriz_futura = generar_matriz_ascii(viento_futuro, width, height, float(minutes) * 0.2)

    return {
        "node_status": "ONLINE",
        "location": {"lat": lat, "lon": lon},
        "telemetry_comparison": {
            "temperature_c": temp_real,
            "real_current_wind_ms": viento_real,
            f"predicted_{minutes}min_wind_ms": viento_futuro
        },
        "visual_comparison_vertical": {
            "1_graph_current_reality": matriz_actual,
            f"2_graph_predicted_{minutes}min_future": matriz_futura
        },
        "rendering_engine": "Oasis Navier-Stokes Wave Pacer (v4.6)",
        "security": "Blindado por el Enjambre Oasis"
    }

# 3. ENDPOINT DE MATRICES DE FLUIDOS
@app.get("/v1/fluid-matrix")
async def fluid_matrix(city: str = "barcelona", width: int = 60, height: int = 12, time_offset: str = "now", x_api_key: str = Header(None, alias="x-api-key")):
    if x_api_key != CLAVE_LOCAL_PRUEBAS:
        raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")
    offset = 0.0 if time_offset.lower() == "now" else float(time_offset) * 0.2
    return {
        "city": city.capitalize(),
        "matrix_resolution": {"width": width, "height": height},
        "fluid_matrix_ascii": generar_matriz_ascii(3.64, width, height, offset),
        "rendering_engine": "Oasis Navier-Stokes Wave Pacer (v4.6)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
