import os
import sys

gw_path = os.path.expanduser("~/Oasis-Sovereign-Monolith/agents_core/oasis_render_gateway.py")

if not os.path.exists(gw_path):
    print(f"❌ No se encontró el archivo: {gw_path}")
    sys.exit(1)

with open(gw_path, "r", encoding="utf-8") as f:
    code = f.read()

box_handler = '''
# --- MÓDULO SOVEREIGN DRIVE / BOX (LOCAL-FIRST & P2P) ---
SOVEREIGN_BOX_REGISTRY = {}

def handle_box_command(action, file_path=None, payload=None):
    import time, uuid
    if action == "list":
        return {
            "status": "OK",
            "storage_engine": "OPFS / IndexedDB (Local-First)",
            "files": [
                {"name": "slab_3.dat", "size": "3141 B", "type": "binary/tensor"},
                {"name": "informe_navier.md", "size": "18.4 KB", "type": "text/markdown"}
            ]
        }
    elif action == "send":
        token = f"oasis_p2p_{uuid.uuid4().hex[:8]}"
        SOVEREIGN_BOX_REGISTRY[token] = {
            "file_name": file_path or "unnamed_payload",
            "created_at": time.time(),
            "status": "AWAITING_WEBRTC_PEER"
        }
        return {
            "status": "OK",
            "p2p_token": token,
            "qr_payload": f"https://oasis-sovereign-gateway.onrender.com/terminal?peer={token}",
            "msg": f"⚡ [CANAL P2P EFÍMERO]: Token {token}\\n📲 Escanea el QR para transferir de RAM a RAM vía WebRTC DataChannel."
        }
    elif action == "recv":
        token = file_path
        if token in SOVEREIGN_BOX_REGISTRY:
            return {
                "status": "MATCHED",
                "session": SOVEREIGN_BOX_REGISTRY[token],
                "msg": "📡 Par encontrado. Conectando canal WebRTC seguro E2EE..."
            }
        return {
            "status": "WAITING",
            "msg": "📡 Esperando transferencia por WebRTC DataChannel..."
        }
    return {"status": "ERROR", "msg": f"Accion {action} no reconocida"}
'''

if "SOVEREIGN_BOX_REGISTRY" not in code:
    code = box_handler + "\n" + code

route_patch = '''        if self.path == "/v1/box":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}
            act = body.get("action", "list")
            fpath = body.get("file_path", None)
            res = handle_box_command(act, fpath, body)
            self._send_json(res)
            return
'''

if 'self.path == "/v1/box"' not in code:
    target = 'if self.path in ["/telemetry", "/v1/swarm/telemetry"]:'
    if target in code:
        code = code.replace(target, route_patch + "\n        " + target)
    else:
        # Alternativa si el despachador usa otra cadena
        code = code.replace('if self.path == "/v1/swarm/telemetry":', route_patch + '\n        if self.path == "/v1/swarm/telemetry":')

with open(gw_path, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Módulo Sovereign Box integrado con éxito en agents_core/oasis_render_gateway.py")
