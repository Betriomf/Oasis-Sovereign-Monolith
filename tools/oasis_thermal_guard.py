#!/usr/bin/env python3
import subprocess, time, sys

MAX_WATTS = 5.39

def get_combined_power():
    try:
        cmd = "sudo powermetrics -n 1 -i 500 --samplers cpu_power | grep -E 'Combined Power'"
        out = subprocess.check_output(cmd, shell=True, text=True)
        # Ejemplo: Combined Power (CPU + GPU + ANE): 3410 mW
        val_mw = float(out.split(":")[-1].replace("mW", "").strip())
        return val_mw / 1000.0
    except Exception:
        return 3.50  # Estimación basal segura

print(f"🛡️  [OASIS THERMAL GUARD]: Vigilando silicio (Cota: {MAX_WATTS} W)...")
while True:
    w = get_combined_power()
    if w > MAX_WATTS:
        print(f"⚠️  [EXCESO TÉRMICO]: {w:.2f} W > {MAX_WATTS} W. Aplicando Radiación de Hawking...")
        subprocess.run("pkill -STOP -f 'oasis_render_gateway'", shell=True)
        time.sleep(1.618)
        subprocess.run("pkill -CONT -f 'oasis_render_gateway'", shell=True)
    else:
        print(f"❄️  [LAMINAR]: {w:.2f} W | Operación Fría.", end="\r")
    time.sleep(1.938)
