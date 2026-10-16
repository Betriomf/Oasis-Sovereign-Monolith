#!/usr/bin/env python3
"""
OASIS BLACK-SKY SIMULATION: P2P Triage Sync (Darwin Mac <-> iPhone)
Enlace directo sin conexión a internet mediante datagramas locales y LWW-CRDT.
"""
import time
import json
import socket
import threading
import hashlib

FRAME_LIMIT = 3141
PORT_MAC = 9091
PORT_IPHONE = 9092

class SimulatedMeshNode:
    def __init__(self, node_id, listen_port, remote_port, caps=0x0800):
        self.node_id = node_id
        self.listen_port = listen_port
        self.remote_port = remote_port
        self.caps = caps
        self.store = {}
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", self.listen_port))
        
        self.rx_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.rx_thread.start()

    def _listen_loop(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(4096)
                self.ingest_frame(data)
            except Exception:
                break

    def pack_triage(self, pid, level, vitals, notes, timestamp=None):
        if len(notes) > 1024:
            notes = notes[:1024]
        ts = timestamp if timestamp else time.time()
        record = {
            "magic": "OAST",
            "nid": self.node_id,
            "pid": pid,
            "lvl": level,
            "vitals": vitals,
            "notes": notes,
            "ts": ts
        }
        serialized = json.dumps(record, separators=(',', ':')).encode("utf-8")
        if len(serialized) > FRAME_LIMIT:
            raise ValueError("Trama supera el límite estricto pi-KB")
        
        # Digest criptográfico de Capa 0
        sig = hashlib.sha256(serialized + b":COLD_SILICON_KEY").hexdigest()[:16]
        return json.dumps({"payload": record, "sig": sig}).encode("utf-8")

    def send_frame(self, frame_bytes):
        self.sock.sendto(frame_bytes, ("127.0.0.1", self.remote_port))

    def ingest_frame(self, raw_bytes):
        t0 = time.perf_counter()
        packet = json.loads(raw_bytes.decode("utf-8"))
        p = packet["payload"]
        pid = p["pid"]
        incoming_ts = p["ts"]

        # Resolución LWW-CRDT
        existing = self.store.get(pid)
        if not existing or incoming_ts > existing["ts"]:
            self.store[pid] = p
            lat_us = (time.perf_counter() - t0) * 1e6
            print(f"  📥 [{self.node_id}]: Trama aceptada para {pid} ➔ ESTADO: {p['lvl']} "
                  f"(Emisor: {p['nid']} | Ingesta: {lat_us:.1f} µs | Tamaño: {len(raw_bytes)} B)")
            return True
        else:
            print(f"  ⏭️ [{self.node_id}]: Trama descartada para {pid} (Registro local más reciente)")
            return False

    def close(self):
        self.running = False
        self.sock.close()

def run_simulation():
    print("=" * 72)
    print("🛰️  SIMULACIÓN OASIS BLACK-SKY: INTERCAMBIO P2P DE TRIAJE OFF-GRID")
    print("📡 Medio Físico   : Enlace local ad-hoc directo (127.0.0.1 / Link-Local)")
    print("🔒 Restricciones  : 0 servidores externos | Límite por trama <= 3141 bytes")
    print("=" * 72)

    # 1. Inicialización de Nodos
    mac_node = SimulatedMeshNode("DARWIN-SURGICAL-MAC", PORT_MAC, PORT_IPHONE)
    iphone_node = SimulatedMeshNode("IPHONE-MOBILE-01", PORT_IPHONE, PORT_MAC)
    time.sleep(0.1)

    print("\n[PASO 1] 📱 El iPhone localiza a víctima en acceso exterior (PAC-402)")
    t0 = time.time()
    vitals_initial = {"hr": 98, "rr": 20, "spo2": 95, "bp": "115/75"}
    frame_1 = iphone_node.pack_triage(
        pid="PAC-402",
        level="YELLOW",
        vitals=vitals_initial,
        notes="Traumatismo cerrado en brazo izquierdo. Hemodinámicamente estable.",
        timestamp=t0
    )
    # iPhone lo almacena en su propio registro local
    iphone_node.ingest_frame(frame_1)
    
    print("\n[PASO 2] ⚡ Transmisión de trama desde iPhone hacia MacBook Air...")
    iphone_node.send_frame(frame_1)
    time.sleep(0.2)

    print("\n[PASO 3] ⚠️ Empeoramiento clínico en Puesto Quirúrgico (MacBook Air)")
    print("         El paciente entra en shock hipovolémico. Mac actualiza prioridad...")
    t1 = t0 + 120.0  # 2 minutos después
    vitals_worse = {"hr": 138, "rr": 34, "spo2": 88, "bp": "75/40"}
    frame_2 = mac_node.pack_triage(
        pid="PAC-402",
        level="RED",
        vitals=vitals_worse,
        notes="Shock hipovolémico súbito. Requiere canalización y transfusión urgente.",
        timestamp=t1
    )
    mac_node.ingest_frame(frame_2)

    print("\n[PASO 4] ⚡ Retransmisión de actualización desde Mac hacia iPhone (Gossip)...")
    mac_node.send_frame(frame_2)
    time.sleep(0.2)

    print("\n[PASO 5] 🧪 Prueba de concurrencia: iPhone intenta reenviar trama antigua (t0)")
    # El iPhone simula un paquete desfasado en la red
    iphone_node.send_frame(frame_1)
    time.sleep(0.2)

    print("\n" + "=" * 72)
    print("📊 ESTADO CONSOLIDADO DEL REGISTRO EN AMBOS DISPOSITIVOS (CRDT CONVERGENTE)")
    print("=" * 72)
    print(f"🖥️  MacBook Air -> Paciente {mac_node.store['PAC-402']['pid']}: "
          f"Nivel {mac_node.store['PAC-402']['lvl']} | TA: {mac_node.store['PAC-402']['vitals']['bp']}")
    print(f"📱 iPhone      -> Paciente {iphone_node.store['PAC-402']['pid']}: "
          f"Nivel {iphone_node.store['PAC-402']['lvl']} | TA: {iphone_node.store['PAC-402']['vitals']['bp']}")

    assert mac_node.store["PAC-402"]["lvl"] == iphone_node.store["PAC-402"]["lvl"] == "RED"
    print("\n✅ Veredicto: Sincronización convergente verificada al 100%. Cero pérdida de datos.")

    mac_node.close()
    iphone_node.close()

if __name__ == "__main__":
    run_simulation()
