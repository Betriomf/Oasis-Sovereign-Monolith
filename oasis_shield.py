import json
import time
import urllib.request
from typing import List, Tuple

DEFAULT_ENDPOINT = "https://oasis-sovereign-gateway.onrender.com/v1/shield/entropy-score"

class OasisShield:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT, timeout_sec: float = 0.35):
        self.endpoint = endpoint
        self.timeout_sec = timeout_sec

    def verify_traffic(self, intervals_ms: List[float], target_id: str = "anon") -> Tuple[bool, dict]:
        """
        Retorna (is_human, metadata).
        Aplica fail-open seguro: si hay timeout, no bloquea al usuario.
        """
        payload = json.dumps({
            "target_id": target_id,
            "intervals_ms": intervals_ms
        }).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-client-time": str(time.time())
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return (not data.get("is_bot", False)), data
        except Exception as e:
            # Tolerancia a fallos: fallback grácil para mantener disponibilidad
            return True, {"fallback": True, "error": str(e), "verdict": "BYPASS_FAIL_OPEN"}

if __name__ == "__main__":
    shield = OasisShield()
    humano, audit = shield.verify_traffic([150.2, 420.5, 210.1, 890.3, 310.0], "user_test")
    print(f"✅ Validación Humana: {humano} | Score: {audit.get('entropy_score')}")
    
    bot, audit_bot = shield.verify_traffic([50.0, 50.0, 50.0, 50.0, 50.0], "bot_test")
    print(f"🤖 Detección de Bot: {not bot} | Veredicto: {audit_bot.get('verdict')}")
