#!/usr/bin/env python3
"""
OASIS SOVEREIGN SCRAPER ENGINE — SILICIO FRÍO (v2.1)
Extracción unificada sin dependencias externas:
1. Pestañas de terminal cerradas y activas (~/.zsh_sessions, ~/.zsh_history).
2. Volcado de código fuente completo con Pacing Áureo (pi/phi).
3. Exportación de la Bóveda a archivo ZIP comprimido.
"""
import os
import sys
import glob
import time
import math
import shutil
import asyncio

import re

def sanitize_sensitive_data(text):
    """Redacta tokens, claves privadas y mnemónicos usando Zero-Knowledge."""
    # 1. Claves privadas hex (64 caracteres)
    text = re.sub(r'([0-9a-fA-F]{64})', r'[ZK_REDACTED_HEX_KEY:[:6]...]', text)
    # 2. Tokens de GitHub / Bearer
    text = re.sub(r'(ghp_[a-zA-Z0-9]{36}|Bearer\s+[a-zA-Z0-9\._\-]+)', r'[ZK_REDACTED_TOKEN]', text)
    # 3. Frases mnemónicas típicas (12 palabras)
    text = re.sub(r'(mnemonic_12_words["']?\s*:\s*["'])([^"']+)(["'])', r'[ZK_REDACTED_MNEMONIC]', text)
    # 4. Claves Ed25519 selladas
    text = re.sub(r'(private_key_sealed["']?\s*:\s*["'])([^"']+)(["'])', r'[ZK_REDACTED_PRIVATE_KEY]', text)
    return text


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DIR = os.path.join(BASE_DIR, "vault")
SESSIONS_OUT = os.path.join(VAULT_DIR, "darwin_terminal_scrape.md")
CODE_OUT = os.path.join(VAULT_DIR, "OASIS_FULL_CODE.md")
ZIP_OUT = os.path.join(BASE_DIR, "oasis_vault_backup")

# Constante de Pacing Áureo (Pilar 14 / 385)
PHI = (1.0 + math.sqrt(5.0)) / 2.0
PI = math.pi
PACING_S = (PI / PHI) / 1000.0  # 1.9416 ms

# -------------------------------------------------------------
# NIVEL 1: PESTAÑAS CERRADAS Y LOGS DE TERMINAL
# -------------------------------------------------------------
async def scrape_terminal_sessions(keyword=None):
    print("🛰️  [NIVEL 1]: Escaneando sesiones cerradas e historial de Darwin...")
    sessions_dir = os.path.expanduser("~/.zsh_sessions")
    records = []

    if os.path.exists(sessions_dir):
        files = sorted(glob.glob(os.path.join(sessions_dir, "*.history")), key=os.path.getmtime, reverse=True)
        for idx, hf in enumerate(files):
            session_id = os.path.basename(hf).replace(".history", "")
            try:
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(hf)))
                with open(hf, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [sanitize_sensitive_data(l.strip()) for l in f if l.strip()]
                if keyword:
                    lines = [l for l in lines if keyword.lower() in l.lower()]
                if lines:
                    records.append({"id": session_id[:8], "mtime": mtime, "lines": lines[-30:]})
            except Exception:
                pass

            if (idx + 1) % 15 == 0:
                await asyncio.sleep(PACING_S)

    # Historial global ~/.zsh_history
    hist_lines = []
    hist_file = os.path.expanduser("~/.zsh_history")
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r", encoding="utf-8", errors="ignore") as f:
                for l in f.readlines()[-120:]:
                    clean = l.strip()
                    if clean.startswith(": "):
                        parts = clean.split(";", 1)
                        if len(parts) == 2:
                            clean = parts[1]
                    if not keyword or keyword.lower() in clean.lower():
                        hist_lines.append(sanitize_sensitive_data(clean))
        except Exception:
            pass

    # Escribir resultado en Markdown para la Bóveda
    with open(SESSIONS_OUT, "w", encoding="utf-8") as out:
        out.write("# 🏛️ REGISTRO DE TERMINALES DARWIN RECUPERADAS\n\n")
        out.write(f"- **Nodo:** MacBookAir8,2 | **Cadencia:** Pacing Áureo ($\\pi/\\phi \\approx 1.94\\text{{ ms}}$)\n")
        out.write(f"- **Fecha:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        out.write("## 1. Pestañas Cerradas (~/.zsh_sessions)\n\n")
        for r in records:
            out.write(f"### 📂 Pestaña `{r['id']}` (Cerrada: {r['mtime']})\n```bash\n")
            out.write("\n".join(r["lines"]))
            out.write("\n```\n\n")
        out.write("## 2. Historial Global Reciente (~/.zsh_history)\n\n```bash\n")
        out.write("\n".join(hist_lines[-50:]) if hist_lines else "# Sin datos")
        out.write("\n```\n")

    print(f"✅ [NIVEL 1 COMPLETADO]: Guardado en {SESSIONS_OUT}")

# -------------------------------------------------------------
# NIVEL 2: VOLCADO DE CÓDIGO CON PACING ÁUREO
# -------------------------------------------------------------
async def scrape_full_codebase():
    print(f"🚀 [NIVEL 2]: Consolidando código fuente con Pacing Áureo...")
    t0 = time.perf_counter()
    archivos_procesados = 0
    bytes_totales = 0

    ignored_dirs = {'.git', 'node_modules', '__pycache__', 'venv', 'qemu_swarm', 'dist', 'build'}
    valid_exts = ('.py', '.html', '.js', '.lean', '.c', '.h', '.md', '.json', '.sh')

    with open(CODE_OUT, "w", encoding="utf-8") as out:
        out.write("# 🏛️ OASIS SOVEREIGN OS — VOLCADO MAESTRO DE CÓDIGO FUENTE\n\n")
        out.write(f"- **Generado:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"- **Pacing Áureo:** $\\Delta t = \\pi/\\phi$ cada 50 archivos\n\n---\n\n")

        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith('.')]

            for file in sorted(files):
                if file.endswith(valid_exts):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, BASE_DIR)

                    # Evitar incluir el propio volcado generado
                    if relpath in ["vault/OASIS_FULL_CODE.md", "vault/darwin_terminal_scrape.md"]:
                        continue

                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        out.write(f"\n\n# ============================================================\n")
                        out.write(f"# ARCHIVO: {relpath}\n")
                        out.write(f"# ============================================================\n\n")
                        out.write(content)

                        archivos_procesados += 1
                        bytes_totales += len(content.encode("utf-8"))
                    except Exception:
                        pass

                    if archivos_procesados % 50 == 0:
                        await asyncio.sleep(PACING_S)

    t_total = time.perf_counter() - t0
    mb = bytes_totales / (1024 * 1024)
    print(f"✅ [NIVEL 2 COMPLETADO]: {archivos_procesados} archivos ({mb:.2f} MB) consolidados en {t_total:.2f} s.")
    print(f"📁 Guardado en Bóveda: {CODE_OUT}")

# -------------------------------------------------------------
# NIVEL 3: EMPAQUETADO COMPRIMIDO DE LA BÓVEDA
# -------------------------------------------------------------
def export_vault_zip():
    print("📦 [NIVEL 3]: Empaquetando Bóveda E2EE en archivo ZIP...")
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR, exist_ok=True)
    archive_path = shutil.make_archive(ZIP_OUT, 'zip', VAULT_DIR)
    sz_kb = os.path.getsize(archive_path) / 1024.0
    print(f"✅ [NIVEL 3 COMPLETADO]: Bóveda respaldada en {archive_path} ({sz_kb:.1f} KB)")

# -------------------------------------------------------------
# DESPACHADOR PRINCIPAL
# -------------------------------------------------------------
async def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "--all"
    query = sys.argv[2] if len(sys.argv) > 2 else None

    if mode in ["--sessions", "-s"]:
        await scrape_terminal_sessions(query)
    elif mode in ["--code", "-c"]:
        await scrape_full_codebase()
    elif mode in ["--zip", "-z"]:
        export_vault_zip()
    elif mode in ["--all", "-a"]:
        await scrape_terminal_sessions(query)
        await scrape_full_codebase()
        export_vault_zip()
    else:
        print("Uso: python3 tools/oasis_scraper_engine.py [--sessions [filtro] | --code | --zip | --all]")

if __name__ == "__main__":
    asyncio.run(main())
