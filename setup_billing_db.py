import urllib.request
import json

SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"

# Esquema relacional: 'api_keys' y 'processed_crypto_tx'
sql_payload = """
CREATE TABLE IF NOT EXISTS api_keys (
    key_id TEXT PRIMARY KEY,
    owner TEXT NOT NULL,
    quota BIGINT NOT NULL DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS processed_crypto_tx (
    tx_hash TEXT PRIMARY KEY,
    sender TEXT NOT NULL,
    amount_tokens FLOAT NOT NULL,
    key_credited TEXT NOT NULL,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

print("📦 Configurando tablas de facturación en Supabase...")
# Inserción inicial de tu Clave Maestra en la base de datos
url = f"{SUPABASE_URL}/rest/v1/api_keys"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

master_payload = json.dumps({
    "key_id": "OASIS-SOVEREIGN-MARIANO-2026",
    "owner": "sovereign_root",
    "quota": 999999999
}).encode("utf-8")

req = urllib.request.Request(url, data=master_payload, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print("✅ Clave Maestra Soberana registrada en Supabase.")
except Exception as e:
    print(f"ℹ️ Registro en Supabase: {e}")
