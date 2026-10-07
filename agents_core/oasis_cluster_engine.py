#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — VIRTUAL MICROVM SWARM ORCHESTRATOR v4.0
Simula N nodos con huella física SMBIOS independiente y latido Gossip.
"""
import sys
import time
import uuid
import hashlib
import threading
import urllib.request
import json

RENDER_URL = "https://oasis-sovereign-gateway.onrender.com"
ACTIVE_CLUSTERS = {}

def simulate_node(node_idx):
    node_id = f"virtual_node_{node_idx}"
    # Generación determinista de huella de hardware por nodo
    raw_sig = f"OASIS-VIRTUAL-SILICON-CORE-{node_idx}-{uuid.uuid4().hex[:6]}"
    hw_key = "OASIS-HW-" + hashlib.sha256(raw_sig.encode()).hexdigest()[:12].upper()
    
    print(f"  🟢 [Lanzando Nodo #{node_idx}] ID: {node_id} | HW: {hw_key}")
    
    while ACTIVE_CLUSTERS.get(node_idx, True):
        try:
            payload = json.dumps({
                "hw_key": hw_key,
                "role": "MICROVM_WORKER",
                "status": "IDLE",
                "model": "oasis-microvm:qemu"
            }).encode()

            req = urllib.request.Request(
                f"{RENDER_URL}/v1/swarm/heartbeat",
                data=payload,
                headers={"Content-Type": "application/json", "x-hw-key": hw_key},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                pass
        except Exception:
            pass
        time.sleep(2.0)

def start_swarm(num_nodes=3):
    print(f"🚀 [OASIS v4.0] Desplegando enjambre de {num_nodes} MicroVMs simuladas...")
    threads = []
    for i in range(1, num_nodes + 1):
        ACTIVE_CLUSTERS[i] = True
        t = threading.Thread(target=simulate_node, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    
    print(f"✨ Enjambre activo con {num_nodes} nodos transmitiendo latidos Gossip a Render.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Apagando enjambre virtual...")
        for k in ACTIVE_CLUSTERS:
            ACTIVE_CLUSTERS[k] = False

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    start_swarm(n)
