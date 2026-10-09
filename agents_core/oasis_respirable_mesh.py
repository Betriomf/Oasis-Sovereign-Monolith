#!/usr/bin/env python3
"""
OASIS RESPIRABLE MESH DAEMON (AXCAN ARCHITECTURE) v1.0
Migración elástica de tareas entre Darwin (Mac) y Alpine (iPhone).
"""
import os
import sys
import time
import math
import json
import socket
import threading
import subprocess

REPO_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")
sys.path.insert(0, REPO_DIR)

from agents_core.oasis_bitmask_os import verify_capability, CAP_P2P_MESH, CAP_VORTEX_RUN
from agents_core.oasis_landauer_guard import LandauerGuard

PORT_MESH = 9091
CAP_REQ = CAP_P2P_MESH | CAP_VORTEX_RUN  # 0x0024

class RespirableMeshCoordinator:
    def __init__(self):
        self.guard = LandauerGuard()
        self.active_slab = {
            "slab_id": 3,
            "z_range": [-0.5, 0.0],
            "step": 1040,
            "enstrophy": 5.2910,
            "tensor": [0.5501, -0.3940, -0.9026],
            "owner": "DARWIN_MAC"
        }
        self.peer_conn = None
        self.peer_addr = None
        self.simulated_battery = False

    def get_power_source(self):
        """Consulta el estado del hardware en macOS mediante pmset nativo."""
        if self.simulated_battery:
            return "BATTERY_SIMULATED"
        try:
            out = subprocess.check_output(["pmset", "-g", "batt"]).decode()
            if "Battery Power" in out:
                return "BATTERY"
            elif "AC Power" in out:
                return "AC"
        except Exception:
            pass
        return "AC"

    def serialize_slab(self):
        """Empaqueta el estado en una micro-trama conforme de π-KB."""
        payload = json.dumps({
            "action": "TASK_MIGRATE_INCOMING",
            "caps": hex(CAP_REQ),
            "slab": self.active_slab,
            "timestamp": time.time()
        }).encode("utf-8")
        return self.guard.sanitize_pi_frame(payload)

    def start_server(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('0.0.0.0', PORT_MESH))
        srv.listen(2)

        print("="*65)
        print("🌬️  OASIS RESPIRABLE MESH (AXCAN RUNTIME MIGRATION)")
        print(f"📍 Puerto P2P Local : {PORT_MESH}")
        print(f"⚡ Permiso Requerido: 0x{CAP_REQ:04X} (P2P_MESH | VORTEX_RUN)")
        print("="*65)
        print("Esperando conexión del worker iPhone (Alpine / iSH)...")

        threading.Thread(target=self._monitor_power_loop, daemon=True).start()

        while True:
            try:
                conn, addr = srv.accept()
                self.peer_conn = conn
                self.peer_addr = addr
                print(f"\n🔗 [PEER CONECTADO]: Nodo iPhone detectado desde {addr}")
                self._handle_peer(conn)
            except KeyboardInterrupt:
                print("\n🛑 Mesh respirable detenido.")
                break
            except Exception as e:
                print(f"⚠️ Error de enlace: {e}")

    def _handle_peer(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                msg = json.loads(data.decode("utf-8"))
                action = msg.get("action")

                if action == "WORKER_READY":
                    print(f"📱 [IPHONE READY]: Worker en línea. Propietario actual: {self.active_slab['owner']}")
                    conn.sendall(json.dumps({"status": "REGISTERED", "owner": self.active_slab["owner"]}).encode())

                elif action == "TASK_RETURN":
                    # El iPhone devuelve el slab calculado tras la reconexión a CA
                    returned_slab = msg.get("slab", {})
                    t_recv = time.perf_counter()
                    dt = (time.time() - msg.get("timestamp", time.time())) * 1000
                    self.active_slab = returned_slab
                    self.active_slab["owner"] = "DARWIN_MAC"
                    print(f"🍏 [SLAB REABSORBIDO EN MAC]: Paso {self.active_slab.get('step')} | Latencia retorno: {dt:.2f} ms")
                    conn.sendall(json.dumps({"status": "REABSORBED_OK"}).encode())

            except Exception:
                break
        self.peer_conn = None
        print("🔌 Peer desconectado.")

    def _monitor_power_loop(self):
        """Bucle que vigila el estado de batería para gatillar la migración."""
        last_power = "AC"
        while True:
            time.sleep(1.5)
            power = self.get_power_source()

            if power != last_power:
                print(f"\n⚡ [CAMBIO TÉRMICO / ENERGÍA]: {last_power} ➔ {power}")
                if "BATTERY" in power and self.peer_conn and self.active_slab["owner"] == "DARWIN_MAC":
                    # MIGRAR TAREA HACIA EL IPHONE
                    t0 = time.perf_counter()
                    self.active_slab["owner"] = "IPHONE_NODE"
                    frame = self.serialize_slab()
                    try:
                        self.peer_conn.sendall(frame)
                        lat_ms = (time.perf_counter() - t0) * 1000
                        print(f"🚀 [MIGRACIÓN EN CALIENTE DISPARADA]: Slab 3 enviado al iPhone ({len(frame)} bytes) en {lat_ms:.2f} ms")
                        print("❄️  MacBook Air entrando en modo Reposo Térmico (0 W cómputo)...")
                    except Exception as e:
                        print(f"❌ Error al migrar: {e}")

                elif "AC" in power and self.peer_conn and self.active_slab["owner"] == "IPHONE_NODE":
                    # RECLAMAR TAREA DE VUELTA
                    print("⚡ Corriente AC restablecida. Reclamando cómputo del iPhone...")
                    try:
                        req = json.dumps({"action": "REQUEST_RECLAIM"}).encode()
                        self.peer_conn.sendall(req)
                    except Exception as e:
                        print(f"❌ Error al reclamar: {e}")

                last_power = power

if __name__ == "__main__":
    coordinator = RespirableMeshCoordinator()
    coordinator.start_server()
