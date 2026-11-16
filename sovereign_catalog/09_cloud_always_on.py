#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 09]: NODO PÚBLICO 24/7 (MAC CERRADO)
Comprueba el estado de los servidores gratuitos permanentes (Render + Hugging Face)
que atienden a los usuarios cuando el MacBook Air local está apagado o cerrado.
"""
import ssl
import sys
import time
import urllib.request

RENDER_URL = "https://oasis-sovereign-wind-node.onrender.com/terminal"
HF_URL = "https://huggingface.co/spaces/Betriomf/oasis-sovereign-terminal"
CTX = ssl._create_unverified_context()

def probe_endpoint(url: str) -> str:
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OasisCloudSentinel/20.8"})
        with urllib.request.urlopen(req, timeout=6, context=CTX) as r:
            ms = (time.perf_counter() - t0) * 1000
            return f"ONLINE (HTTP {r.status} | {ms:.0f} ms)"
    except Exception as e:
        return f"HIBERNANDO / DESPERTANDO ({type(e).__name__})"

def cloud_process(_arg: str = "") -> str:
    st_render = probe_endpoint(RENDER_URL)
    st_hf = probe_endpoint(HF_URL)
    return (
        "════════════════════════════════════════════════════════════════\n"
        "☁️  [OASIS ALWAYS-ON CLOUD — MÓDULO 09 (FUNCIONA CON MAC CERRADO)]\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• Nodo API + Terminal (Render) : {st_render}\n"
        f"  🔗 {RENDER_URL}\n"
        f"• Nodo Estático (Hugging Face) : {st_hf}\n"
        f"  🔗 {HF_URL}\n"
        "────────────────────────────────────────────────────────────────\n"
        "💡 Cualquier usuario puede entrar gratis a esos enlaces y usar\n"
        "   `ai`, `riona`, `qr`, `mesh`, `webgpu`, `play`, `fiscal` y `sheets`\n"
        "   24/7 sin que tu MacBook Air esté encendido.\n"
        "════════════════════════════════════════════════════════════════"
    )

if __name__ == "__main__":
    print(cloud_process())
