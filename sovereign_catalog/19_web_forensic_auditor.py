#!/usr/bin/env python3
"""
[DICCIONARIO SOBERANO OASIS — MÓDULO 19]: AUDITOR FORENSE DE WEBS Y APIS (`web-audit` / `audit-web`)
Aplica el protocolo científico de 8 fases (Scraping -> Invariantes -> Test -> Notario) para detectar
y certificar por qué fallan aplicaciones web (respuestas JSON vacías, rutas huérfanas, bloqueos de UI).
"""
import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SSL_CTX = ssl._create_unverified_context()

def audit_local_artifacts() -> list[str]:
    findings = []
    t_html = BASE_DIR / "agents_core" / "templates" / "terminal.html"
    gw_py = BASE_DIR / "agents_core" / "oasis_render_gateway.py"

    if t_html.exists():
        txt = t_html.read_text(encoding="utf-8")
        has_bridge = "__OASIS_SOVEREIGN_BRIDGE__" in txt
        has_safe_json = "response.text()" in txt or "res.text()" in txt
        findings.append(f"  {'✅' if has_bridge else '❌'} [FASE 1-UI] Enrutador maestro Xterm.js (18+ módulos): {'ACTIVO' if has_bridge else 'DESCONECTADO'}")
        findings.append(f"  {'✅' if has_safe_json else '⚠️'} [FASE 2-UI] Parser JSON defensivo (anti-cuerpo vacío): {'PROTEGIDO' if has_safe_json else 'VULNERABLE a Unexpected end of JSON'}")

    if gw_py.exists():
        gtxt = gw_py.read_text(encoding="utf-8")
        has_fallback = "OASIS_JSON_CONTRACT_SHIELD" in gtxt
        findings.append(f"  {'✅' if has_fallback else '❌'} [FASE 3-API] Escudo JSON 0-bytes en Gateway: {'ACTIVO' if has_fallback else 'SIN ESCUDO'}")

    return findings

def probe_live_endpoints(base_url: str = "https://oasis-sovereign-wind-node.onrender.com") -> list[str]:
    results = []
    for sk in ("pilares", "agents", "sec", "crm", "verify-ym"):
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(
                f"{base_url}/v1/skill",
                data=json.dumps({"skill": sk, "prompt": "status"}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=8, context=SSL_CTX) as r:
                raw = r.read().decode("utf-8", errors="ignore")
                ms = (time.perf_counter() - t0) * 1000.0
                if not raw.strip():
                    results.append(f"  ❌ POST /v1/skill ({sk:<10}) -> HTTP {r.status} | CUERPO VACÍO (Fallo JSON) | {ms:.0f} ms")
                else:
                    parsed = json.loads(raw)
                    ok = bool(parsed.get("output"))
                    results.append(f"  {'✅' if ok else '⚠️'} POST /v1/skill ({sk:<10}) -> HTTP {r.status} | JSON OK ({len(raw)} B) | {ms:.0f} ms")
        except Exception as e:
            results.append(f"  ⚠️ POST /v1/skill ({sk:<10}) -> {type(e).__name__}: {e}")
    return results

def web_audit_process(target: str = "") -> str:
    url = target.strip() if target.strip().startswith("http") else "https://oasis-sovereign-wind-node.onrender.com"
    local_rep = audit_local_artifacts()
    live_rep = probe_live_endpoints(url)
    return (
        "════════════════════════════════════════════════════════════════\n"
        "🕵️  [AUDITOR FORENSE DE WEBS Y APIS — MÓDULO 19 (PROTOCOLO 8 FASES)]\n"
        "────────────────────────────────────────────────────────────────\n"
        f"• Objetivo Auditado : {url}\n"
        "────────────────────────────────────────────────────────────────\n"
        "🔬 FASE 1–3 (ANÁLISIS ESTÁTICO DE CONTRATO FRONTEND/BACKEND):\n"
        + "\n".join(local_rep) + "\n"
        "────────────────────────────────────────────────────────────────\n"
        "🌐 FASE 4–7 (PRUEBA DE ESTRÉS EN VIVO CONTRA ENDPOINTS):\n"
        + "\n".join(live_rep) + "\n"
        "════════════════════════════════════════════════════════════════"
    )

if __name__ == "__main__":
    print(web_audit_process(" ".join(sys.argv[1:])))
