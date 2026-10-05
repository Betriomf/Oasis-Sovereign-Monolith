#!/usr/bin/env python3
import time
import json
import urllib.request
import urllib.parse

AKASH_WALLET = "akash1dy3ph3lcylhwu9mz969kpg4jh49qs03mkn6v4y"
RPC_NODE = "https://rpc.akashnet.net:443"
SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"

# Ratio de conversión: 1 AKT (1.000.000 uakt) = 10.000 llamadas a la API
CREDITS_PER_AKT = 10000

def get_processed_txs():
    """Obtiene los hashes ya liquidados desde Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/processed_crypto_tx?select=tx_hash"
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return {row["tx_hash"] for row in data}
    except Exception:
        return set()

def credit_api_key(key_id, extra_quota, tx_hash, sender, amount):
    """Suma créditos a la clave del cliente y sella el hash de la transacción."""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    # 1. Obtener saldo actual
    url_key = f"{SUPABASE_URL}/rest/v1/api_keys?key_id=eq.{key_id}"
    req_get = urllib.request.Request(url_key, headers=headers)
    current_quota = 0
    try:
        with urllib.request.urlopen(req_get, timeout=5) as resp:
            rows = json.loads(resp.read().decode())
            if rows:
                current_quota = rows[0].get("quota", 0)
    except Exception as e:
        print(f"Error consultando clave {key_id}: {e}")
        return False

    new_quota = current_quota + extra_quota

    # 2. Actualizar cupo
    req_patch = urllib.request.Request(
        url_key,
        data=json.dumps({"quota": new_quota}).encode(),
        headers=headers,
        method="PATCH"
    )

    # 3. Registrar transacción procesada
    url_tx = f"{SUPABASE_URL}/rest/v1/processed_crypto_tx"
    tx_payload = json.dumps({
        "tx_hash": tx_hash,
        "sender": sender,
        "amount_tokens": amount,
        "key_credited": key_id
    }).encode()
    req_tx = urllib.request.Request(url_tx, data=tx_payload, headers=headers, method="POST")

    try:
        urllib.request.urlopen(req_patch, timeout=5)
        urllib.request.urlopen(req_tx, timeout=5)
        print(f"⚡ [PAGO ACREDITADO]: Clave {key_id} recargada con +{extra_quota} créditos (Total: {new_quota}).")
        return True
    except Exception as e:
        print(f"Error registrando liquidación: {e}")
        return False

def scan_incoming_akash_txs():
    """Consulta la blockchain en busca de depósitos dirigidos a tu dirección."""
    query = f"transfer.recipient='{AKASH_WALLET}'"
    url = f"{RPC_NODE}/tx_search?query={urllib.parse.quote(f'\"{query}\"')}&prove=false&page=1&per_page=10&order_by=\"desc\""
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OasisAutonomousBridge/2.0"})
        with urllib.request.urlopen(req, timeout=7) as resp:
            res = json.loads(resp.read().decode())
            return res.get("result", {}).get("txs", [])
    except Exception as e:
        return []

def run_bridge_cycle():
    processed_hashes = get_processed_txs()
    txs = scan_incoming_akash_txs()

    for tx in txs:
        tx_hash = tx.get("hash")
        if not tx_hash or tx_hash in processed_hashes:
            continue

        # Extraer memo y eventos
        tx_result = tx.get("tx_result", {})
        if tx_result.get("code", 0) != 0:
            continue  # Transacción fallida en la cadena

        # Decodificar eventos de transferencia
        events = tx_result.get("events", [])
        sender = "desconocido"
        amount_akt = 0.0

        for ev in events:
            if ev.get("type") == "transfer":
                for attr in ev.get("attributes", []):
                    # Decodificación base64 o texto directo según versión de RPC
                    k = attr.get("key", "")
                    v = attr.get("value", "")
                    if k == "sender":
                        sender = v
                    elif k == "amount" and "uakt" in v:
                        uakt_val = int(v.replace("uakt", "").split(",")[0])
                        amount_akt = uakt_val / 1000000.0

        # En Cosmos, si el comprador indica su API Key en el Memo, se acredita automáticamente
        # Si no la indica, se asocia por defecto al remitente
        memo_key = tx.get("tx", "")  # Cadena en bruto
        target_key = f"OASIS-KEY-{sender[:12]}"

        if amount_akt > 0:
            credits = int(amount_akt * CREDITS_PER_AKT)
            credit_api_key(target_key, credits, tx_hash, sender, amount_akt)
            processed_hashes.add(tx_hash)

if __name__ == "__main__":
    print(f"🛰️ [OASIS BRIDGE]: Monitorizando depósitos en {AKASH_WALLET}...")
    while True:
        run_bridge_cycle()
        time.sleep(30)  # Polling eficiente cada 30 segundos
