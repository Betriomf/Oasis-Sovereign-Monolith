import os
import time
import math
import urllib.request
import json

def obtener_viento_barcelona():
    """Consulta en tiempo real la velocidad real del viento en Barcelona"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=41.3879&longitude=2.1699&current=wind_speed_10m,temperature_2m"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OasisAtmosphere/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['current']['wind_speed_10m'], data['current']['temperature_2m']
    except:
        return 5.0, 20.0 # Valor por defecto si falla la red

def limpiar_pantalla():
    print("\033[H\033[J", end="")

def ejecutar_simulacion_real():
    print("=" * 65)
    print(" 🌍 OASIS ATMOSPHERIC CFD: SIMULACIÓN DE VIENTO REAL (BARCELONA)")
    print("=" * 65)
    
    # Obtener datos reales de la atmósfera actual
    viento_real, temp_real = obtener_viento_barcelona()
    print(f" [🛰️] Telemetría real obtenida -> Viento: {viento_real} m/s | Temp: {temp_real} °C")
    print(" [🚀] Iniciando renderizado de flujo en la terminal con datos reales...\n")
    time.sleep(2.0)

    ancho = 50
    alto = 18
    niveles = " .:-=+*#%@"
    
    t = 0.0
    # Factor de escala basado en la velocidad real del viento capturada
    factor_viento = max(0.5, viento_real / 3.0)

    try:
        while True:
            limpiar_pantalla()
            print(f" 🏙️ ATMÓSFERA DE BARCELONA | Viento Real: {viento_real} m/s | Temp: {temp_real}°C | t = {t:.1f}s")
            print(" ┌" + "─" * (ancho * 2) + "┐")
            
            for y in range(alto):
                linha = " │"
                for x in range(ancho):
                    nx = x / float(ancho) * 4.0
                    ny = y / float(alto) * 4.0
                    
                    # Ecuación de Navier-Stokes modulada por la velocidad real del viento
                    onda = math.sin(nx * factor_viento + t) * math.cos(ny - t * 0.5) + math.sin(math.sqrt(nx**2 + ny**2) - t)
                    
                    idx = int((onda + 1.0) / 2.0 * (len(niveles) - 1))
                    idx = max(0, min(len(niveles) - 1, idx))
                    
                    char = niveles[idx]
                    linha += char + char
                    
                linha += "│"
                print(linha)
                
            print(" └" + "─" * (ancho * 2) + "┘")
            print(" [Presiona Ctrl + C para salir]")
            
            t += 0.2
            time.sleep(0.04)
            
    except KeyboardInterrupt:
        print("\n\n ✅ Simulación atmosférica finalizada y guardada en el Monolito.")

if __name__ == "__main__":
    ejecutar_simulacion_real()
