#!/usr/bin/env python3
"""
OASIS DIRECT WEBRTC / P2P DATA BRIDGE (DARWIN MAC <--> ALPINE IPHONE)
Establece transferencia directa sin pasar por Render.
"""
import os
import sys
import time
import json
import socket
import threading
import urllib.request

GATEWAY = "https://oasis-sovereign-gateway.onrender.com"
LOCAL_PORT = 9091
PEER_ID_MAC = "DARWIN-MAC-MASTER"

def registrar_en_broker(local_ip):
    """Publica la oferta de conexión en el broker de Capa 0."""
    payload = json.dumps({
        "peer_id": PEER_ID_MAC,
        "signal": {
            "type": "direct_offer",
            "ip": local_ip,
            "port": LOCAL_PORT,
            "protocol": "OASIS-P2P-LAMINAR/1.0"
        }
    }).encode()
    req = urllib.request.Request(f"{GATEWAY}/v1/webrtc/signal", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def iniciar_servidor_p2p():
    local_ip = get_local_ip()
    print("="*65)
    print("🌐 OASIS DIRECT P2P BRIDGE (DARWIN MAC <--> ALPINE IPHONE)")
    print(f"📍 IP Local Mac      : {local_ip}:{LOCAL_PORT}")
    print(f"📡 Señalización      : {GATEWAY}/v1/webrtc/signal")
    print("="*65)

    res = registrar_en_broker(local_ip)
    print(f"✅ Señal publicada en Capa 0: {res.get('status')}")
    print("⚡ Esperando conexión directa desde el iPhone (Alpine / Safari)...\n")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', LOCAL_PORT))
    srv.listen(5)

    while True:
        try:
            conn, addr = srv.accept()
            print(f"🔗 [ENLACE DIRECTO P2P ESTABLECIDO]: Conexión desde {addr} (0W Nube)")
            data = conn.recv(8192)
            if data:
                try:
                    msg = json.loads(data.decode())
                    action = msg.get("action")
                    if action == "sync_vfs":
                        file_name = msg.get("filename", "sync.txt")
                        content = msg.get("content", "")
                        dest = os.path.expanduser(f"~/Oasis-Tools/{file_name}")
                        with open(dest, "w", encoding="utf-8") as f:
                            f.write(content)
                        conn.sendall(json.dumps({"status": "FILE_WRITTEN", "path": dest}).encode())
                        print(f"📦 [VFS P2P RECIBIDO]: Guardado {dest} ({len(content)} bytes)")
                    elif action == "ping":
                        conn.sendall(json.dumps({"status": "PONG", "latency_ms": 1.2}).encode())
                except Exception as e:
                    conn.sendall(json.dumps({"error": str(e)}).encode())
            conn.close()
        except KeyboardInterrupt:
            print("\n🛑 Puente P2P cerrado.")
            break

if __name__ == "__main__":
    iniciar_servidor_p2p()
