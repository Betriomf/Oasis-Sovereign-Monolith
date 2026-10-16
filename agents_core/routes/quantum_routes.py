# -*- coding: utf-8 -*-
import json
from handlers.quantum_engine import enqueue_circuit, get_circuit_status

def handle_quantum_get(path: str):
    if path.startswith("/v1/quantum/status"):
        task_id = path.split("task_id=")[-1] if "task_id=" in path else ""
        return (200, "application/json", json.dumps(get_circuit_status(task_id)).encode("utf-8"))
    return None

def handle_quantum_post(path: str, body: dict):
    if path == "/v1/quantum/run":
        c_type = body.get("circuit", "bell")
        shots = body.get("shots", 1024)
        node_id = body.get("node_id", "ANON")
        task_id = enqueue_circuit(c_type, shots, node_id)
        return (200, "application/json", json.dumps({"status": "QUEUED", "task_id": task_id}).encode("utf-8"))
    return None
