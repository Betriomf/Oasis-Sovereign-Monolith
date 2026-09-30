import urllib.request
import json
import math
import time
import os

# Coordenadas geográficas de Barcelona
LAT = 41.3888
LON = 2.1590

def obtener_meteo_barcelona():
    """Consulta la API de Open-Meteo sin dependencias externas ni API keys."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    req = urllib.request.Request(url, headers={"User-Agent": "OasisWeather/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            current = data.get("current_weather", {})
            return {
                "temp": current.get("temperature", 20.0),
                "viento_kmh": current.get("windspeed", 10.0),
                "direccion_deg": current.get("winddirection", 0.0),
                "ok": True
            }
    except Exception as e:
        return {"temp": 20.0, "viento_kmh": 10.0, "direccion_deg": 0.0, "ok": False}

def clasificar_regimen(viento_ms):
    """Evalúa la estabilidad laminar vs. cizalladura."""
    if viento_ms < 3.0:
        return "LAMINAR PURO", "Estable"
    elif viento_ms < 7.0:
        return "CIZALLADURA MODERADA", "Vórtices suaves"
    else:
        return "TURBULENTO DINÁMICO", "Dispersión alta"

def render_ascii_fluido(pasos=20):
    meteo = obtener_meteo_barcelona()
    viento_ms = meteo["viento_kmh"] / 3.6
    regimen, descripcion = clasificar_regimen(viento_ms)
    
    ancho, alto = 70, 12
    caracteres = " .:-=+*#%@"
    frecuencia = max(0.5, min(viento_ms * 0.4, 4.0))

    print("\033[2J")  # Limpiar pantalla
    for step in range(pasos):
        t = step * 0.15
        buffer = []
        
        # Cabecera de telemetría real
        buffer.append("🛰️ TELEMETRÍA METEOROLÓGICA EN VIVO: BARCELONA")
        buffer.append(f" Temp: {meteo['temp']}°C | Viento: {meteo['viento_kmh']} km/h ({viento_ms:.2f} m/s) | Dir: {meteo['direccion_deg']}°")
        buffer.append(f" Régimen: {regimen} ({descripcion}) | Frecuencia Onda: {frecuencia:.2f} rad/s")
        buffer.append("┌" + "─" * ancho + "┐")

        # Cálculo de campo de velocidad / vorticidad 2D
        for y in range(alto):
            fila = ["│"]
            for x in range(ancho):
                nx = (x / ancho) * 2.0 * math.pi
                ny = (y / alto) * 2.0 * math.pi
                
                # Ecuación de onda acoplada con deriva por viento real
                val = math.sin(nx * frecuencia + t) * math.cos(ny + t * 0.5)
                # Normalizar a índice del gradiente ASCII [0, 9]
                idx = int((val + 1.0) * 0.5 * (len(caracteres) - 1))
                idx = max(0, min(len(caracteres) - 1, idx))
                fila.append(caracteres[idx])
            fila.append("│")
            buffer.append("".join(fila))
            
        buffer.append("└" + "─" * ancho + "┘")
        
        # Renderizado en terminal
        print("\033[H" + "\n".join(buffer), end="", flush=True)
        time.sleep(0.1)

if __name__ == "__main__":
    render_ascii_fluido()
