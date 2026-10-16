# -*- coding: utf-8 -*-
import json
from handlers.system_patcher import read_source, apply_patch
from oasis_hybrid_router import classify_query_intent, solve_analytic_query

def handle_system_get(path: str, kernel_version: str):
    if path.startswith("/v1/system/source"):
        q_file = path.split("file=")[-1] if "file=" in path else "agents_core/oasis_render_gateway.py"
        res = read_source(q_file)
        return (404 if "error" in res else 200, "application/json", json.dumps(res).encode("utf-8"))

    elif path in ("/telemetry", "/v1/agent/status"):
        data = {
            "status": "ONLINE",
            "version": kernel_version,
            "power_watts": 4.18,
            "silicon_power": 4.18,
            "cpu_efficient_load": 12.4,
            "entropy_asymmetry": "0.00 J/K·s (Adiabático)",
            "arpanet_mesh": 23,
            "hardware_id": "OASIS-HW-468F6F695BDB"
        }
        return (200, "application/json", json.dumps(data).encode("utf-8"))
    return None

def handle_system_post(path: str, body: dict):
    if path == "/v1/system/patch":
        target = body.get("target_file", "agents_core/oasis_render_gateway.py")
        content = body.get("content", "")
        reboot = body.get("hot_reload", True)
        res = apply_patch(target, content, reboot)
        return (200 if res.get("success") else 400, "application/json", json.dumps(res).encode("utf-8"))

    elif path == "/v1/hybrid/query":
        user_query = body.get("query", "")
        intent = classify_query_intent(user_query)
        if intent == "ANALYTIC_LINCOS":
            result = solve_analytic_query(user_query)
            return (200, "application/json", json.dumps({"intent": intent, "result": result}).encode("utf-8"))
        else:
            return (200, "application/json", json.dumps({
                "intent": "SEMANTIC_ARXIV",
                "message": "Consulta bibliográfica canalizada a Ollama / RAG local."
            }).encode("utf-8"))

    return None
