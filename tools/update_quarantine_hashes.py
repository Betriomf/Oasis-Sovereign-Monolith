#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — SINCRONIZADOR DE CUARENTENA Y FIRMAS (PILAR 50 / 66)
Actualiza hashes SHA-256 de amenazas mediante feeds públicos abiertos y catálogo local.
"""
import urllib.request
import json
import os

QUARANTINE_FILE = os.path.expanduser("~/Oasis-Sovereign-Monolith/vault/quarantine_hashes.json")

# Catálogo base permanente de hashes de prueba y malware crítico conocido
CURATED_BLOCKED_HASHES = {
    # 1. EICAR Standard Antivirus Test File (SHA-256)
    "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
    # 2. WannaCry Ransomware dropper (SHA-256)
    "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
    # 3. NotPetya Wiper / Ransomware (SHA-256)
    "0277328961a94fa77bd5c3b120ce0fff4253414f4c6e5942ffaaebc60f73d740",
    # 4. LockBit 3.0 Encryptor (SHA-256)
    "d64f0b2f1e29c8e8d5f3d45cf5443217b9b78037a5491104eec4d57c5a0fb7b2",
    # 5. Emotet Trojan Loader (SHA-256)
    "7a1e0c50d32bb5e64883907a3c3c73489fe0000a8c2f5815cf6980d220808cf0"
}

def fetch_public_threat_feed():
    """Descarga firmas desde el feed JSON público y sin autenticación de URLhaus."""
    url = "https://urlhaus.abuse.ch/downloads/json_recent/"
    found = set()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Oasis-Quarantine-Node/19.5"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for entry in list(data.values())[:300]:
                if isinstance(entry, list):
                    for item in entry:
                        sha = item.get("payload_sha256")
                        if sha: found.add(sha.lower())
    except Exception as e:
        print(f"ℹ️ [FEED EXTERNO]: Conexión en reposo o modo estasis ({e}). Usando catálogo soberano.")
    return found

def update_database():
    os.makedirs(os.path.dirname(QUARANTINE_FILE), exist_ok=True)
    all_hashes = set(CURATED_BLOCKED_HASHES)

    if os.path.exists(QUARANTINE_FILE):
        try:
            with open(QUARANTINE_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                all_hashes.update(d.get("blocked_hashes", []))
        except Exception:
            pass

    print("🛰️ Consultando feed público de firmas...")
    external_hashes = fetch_public_threat_feed()
    all_hashes.update(external_hashes)

    output = {
        "network": "OASIS-QUARANTINE-FEED",
        "last_sync": "2026-11-03",
        "total_signatures": len(all_hashes),
        "blocked_hashes": sorted(list(all_hashes))
    }

    with open(QUARANTINE_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Base de datos de Cuarentena actualizada: {len(all_hashes)} hashes vetados en {QUARANTINE_FILE}.")

if __name__ == "__main__":
    update_database()
