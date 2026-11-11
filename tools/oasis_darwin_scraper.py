#!/usr/bin/env python3
"""
OASIS DARWIN TERMINAL SCRAPER & GOLDEN SEARCH ENGINE (v1.0)
Recupera terminales activas y cerradas (~/.zsh_sessions) aplicando Pacing Áureo (pi/phi).
"""
import os
import sys
import glob
import time
import math
import asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
OUTPUT_MD = os.path.join(VAULT_DIR, "darwin_terminal_scrape.md")

# Constante de Pacing Áureo de Capa 0 (Pilar 14 / 385)
PHI = (1.0 + math.sqrt(5.0)) / 2.0
PI = math.pi
PACING_S = (PI / PHI) / 1000.0  # 0.0019416 s (~1.94 ms)

async def scrape_zsh_sessions(keyword=None):
    sessions_dir = os.path.expanduser("~/.zsh_sessions")
    records = []
    if not os.path.exists(sessions_dir):
        return records

    history_files = sorted(glob.glob(os.path.join(sessions_dir, "*.history")), key=os.path.getmtime, reverse=True)
    count = 0
    for hf in history_files:
        session_id = os.path.basename(hf).replace(".history", "")
        try:
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(hf)))
            with open(hf, "r", encoding="utf-8", errors="ignore") as f:
                raw_lines = [l.strip() for l in f if l.strip()]
            
            if keyword:
                raw_lines = [l for l in raw_lines if keyword.lower() in l.lower()]

            if raw_lines:
                records.append({
                    "origen": f"Zsh Session ({session_id[:8]}...)",
                    "fecha_cierre": mtime,
                    "lineas": raw_lines[-40:]
                })
        except Exception:
            pass

        count += 1
        if count % 20 == 0:
            await asyncio.sleep(PACING_S)  # Pacing pi/phi para no saturar bus I/O

    return records

async def scrape_zsh_global(keyword=None):
    hist_file = os.path.expanduser("~/.zsh_history")
    lines = []
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.readlines()
            for l in raw[-150:]:
                clean = l.strip()
                if clean.startswith(": "):
                    parts = clean.split(";", 1)
                    if len(parts) == 2:
                        clean = parts[1]
                if keyword:
                    if keyword.lower() in clean.lower():
                        lines.append(clean)
                else:
                    lines.append(clean)
        except Exception:
            pass
    return lines

async def scrape_gateway_logs(keyword=None):
    candidates = [
        "/Volumes/OasisRAM/tmp/gateway.log",
        os.path.join(BASE_DIR, "gateway.log")
    ]
    entries = []
    for log_path in candidates:
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f.readlines()[-60:]:
                        clean = line.strip()
                        if clean:
                            if keyword:
                                if keyword.lower() in clean.lower():
                                    entries.append(clean)
                            else:
                                entries.append(clean)
            except Exception:
                pass
    return entries

async def run_scraper(keyword=None):
    t0 = time.perf_counter()
    os.makedirs(VAULT_DIR, exist_ok=True)
    mode = f"FILTRADO: '{keyword}'" if keyword else "VOLCADO COMPLETO"
    print(f"🚀 [OASIS SCRAPER]: Iniciando búsqueda con Pacing Áureo (π/φ) [{mode}]...")

    sessions_data = await scrape_zsh_sessions(keyword)
    global_hist = await scrape_zsh_global(keyword)
    gateway_logs = await scrape_gateway_logs(keyword)

    with open(OUTPUT_MD, "w", encoding="utf-8") as out:
        out.write("# 🏛️ VOLCADO FORENSE DE TERMINALES DARWIN (MACOS)\n\n")
        out.write(f"- **Nodo:** MacBookAir8,2 (i5-8210Y)\n")
        out.write(f"- **Fecha:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"- **Cadencia:** Pacing Áureo $\\Delta t = \\pi/\\phi \\approx 1.9416\\text{ ms}$ (Silicio Frío $\\le 2.58\\text{ W}$)\n")
        if keyword:
            out.write(f"- **Filtro Aplicado:** `{keyword}`\n")
        out.write("\n---\n\n")

        out.write("## 1. SESIONES CERRADAS RECUPERADAS (`~/.zsh_sessions`)\n\n")
        if sessions_data:
            for s in sessions_data:
                out.write(f"### 📂 UUID: `{s['origen']}` (Cerrada: {s['fecha_cierre']})\n```bash\n")
                out.write("\n".join(s["lineas"]))
                out.write("\n```\n\n")
        else:
            out.write("No se encontraron coincidencias en `~/.zsh_sessions/`.\n\n")

        out.write("## 2. HISTORIAL GLOBAL (`~/.zsh_history`)\n\n```bash\n")
        out.write("\n".join(global_hist[-60:]) if global_hist else "# Sin entradas")
        out.write("\n```\n\n")

        out.write("## 3. LOGS RPC DEVFRAME (`gateway.log`)\n\n```text\n")
        out.write("\n".join(gateway_logs[-40:]) if gateway_logs else "# Sin entradas")
        out.write("\n```\n")

    t_total = time.perf_counter() - t0
    print(f"✅ Extracción completada en {t_total:.3f} s.")
    print(f"📁 Volcado persistido en Bóveda: {OUTPUT_MD}")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(run_scraper(query))
