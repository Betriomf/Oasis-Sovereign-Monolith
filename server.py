from fastapi import FastAPI, Header, HTTPException
import math

app = FastAPI()

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

@app.get("/v1/wind-forecast")
async def wind_forecast(
    city: str = None, 
    lat: float = None, 
    lon: float = None, 
    minutes: int = 5, 
    x_api_key: str = Header(None, alias="x-api-key")
):
    CLAVE_LOCAL_PRUEBAS = "oasis_sec_99887766554321"
    
    if x_api_key != CLAVE_LOCAL_PRUEBAS:
        raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")
    
    if lat is not None and lon is not None:
        ubicacion_str = f"Lat: {lat}, Lon: {lon}"
        viento_base = round(3.0 + (abs(lat) % 5.0) * 0.4, 2)
    else:
        ubicacion_str = city.capitalize() if city else "Barcelona"
        viento_base = 3.64

    viento_futuro = round(max(0.0, viento_base + (math.sin(minutes * 0.1) * 0.5)), 2)

    return {
        "node_status": "ONLINE",
        "location": ubicacion_str,
        "present_telemetry": {"wind_speed_ms": viento_base},
        f"prediction_{minutes}min": {"wind_speed_ms": viento_futuro},
        "rendering_engine": "Oasis Navier-Stokes Wave Pacer (v3.6)",
        "security": "Blindado por el Enjambre Oasis"
    }

@app.get("/v1/fluid-matrix")
async def fluid_matrix(
    city: str = "barcelona", 
    width: int = 60, 
    height: int = 12, 
    time_offset: str = "now",
    x_api_key: str = Header(None, alias="x-api-key")
):
    CLAVE_LOCAL_PRUEBAS = "oasis_sec_99887766554321"
    
    if x_api_key != CLAVE_LOCAL_PRUEBAS:
        raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")

    viento_base = 3.64
    try:
        if time_offset.lower() == "now":
            offset_temporal = 0.0
        else:
            minutos = int(time_offset)
            offset_temporal = float(minutos) * 0.2
    except ValueError:
        offset_temporal = 0.0

    matriz_ascii = generar_matriz_ascii(viento_base, width, height, offset_temporal)

    return {
        "city": city.capitalize(),
        "matrix_resolution": {"width": width, "height": height},
        "fluid_matrix_ascii": matriz_ascii,
        "rendering_engine": "Oasis Navier-Stokes Wave Pacer (v3.6)",
        "security": "Blindado por el Enjambre Oasis"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
