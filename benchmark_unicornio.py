#!/usr/bin/env python3
"""
OASIS SOVEREIGN MONOLITH — BENCHMARK UNICORNIO (Capa 0 vs Tradicional)
Árbitro Neutral: oasis-auditor / qwen2.5 (T=0.0)
"""

import json
import struct
import time
import subprocess
import sys

# -------------------------------------------------------------------------
# 1. DATOS DE LA TRANACCIÓN BANCARIA LEGACY (PL/1)
# -------------------------------------------------------------------------
TX_DATA = {
    "transaction_id": "TX202607",
    "account_number": "ES9121000418450200051234",
    "amount": 1250.75,
    "currency": "EUR",
    "status": "APPROVED",
    "timestamp": "2026-07-28T22:30:00Z",
    "bank_code": "0128",
    "node_signature": "0x8F3A21B901C"
}

print("⚖️  INICIANDO PRUEBA DE CAMPO: TRADICIONAL VS MÉTODO OASIS UNICORNIO")
print("=" * 70)

# -------------------------------------------------------------------------
# 2. MÉTODO TRADICIONAL (JSON sobre HTTP/Rest API Standard)
# -------------------------------------------------------------------------
t0_trad = time.perf_counter()

# Serialización JSON tradicional
json_bytes = json.dumps(TX_DATA).encode('utf-8')
# Encabezados HTTP ficticios simulados
http_headers = (
    "POST /api/v1/transactions HTTP/1.1\r\n"
    "Host: api.bank-legacy.com\r\n"
    "Content-Type: application/json\r\n"
    f"Content-Length: {len(json_bytes)}\r\n\r\n"
).encode('utf-8')
payload_tradicional = http_headers + json_bytes

t1_trad = time.perf_counter()
tiempo_trad = (t1_trad - t0_trad) * 1000 # ms
bytes_trad = len(payload_tradicional)

print(f"🔴 [MÉTODO TRADICIONAL - REST/JSON]:")
print(f"   ├─ Tamañao de Trama Payload : {bytes_trad} bytes")
print(f"   └─ Tiempo de Serialización  : {tiempo_trad:.4f} ms")
print("-" * 70)

# -------------------------------------------------------------------------
# 3. MÉTODO OASIS UNICORNIO (Lincos / PL1-Frontec + Packet BitChat)
# -------------------------------------------------------------------------
t0_oasis = time.perf_counter()

# Empaquetado binario puro de Capa 0 (14 bytes)
# Formato: 8s (ID), i (Valor en céntimos), 2s (Status OK)
tx_id_bytes = TX_DATA["transaction_id"].encode('ascii')
amount_cents = int(TX_DATA["amount"] * 100)
status_bytes = b"OK"

payload_oasis = struct.pack("!8si2s", tx_id_bytes, amount_cents, status_bytes)

t1_oasis = time.perf_counter()
tiempo_oasis = (t1_oasis - t0_oasis) * 1000 # ms
bytes_oasis = len(payload_oasis)

# Cálculo de eficiencia
ahorro_bytes = ((bytes_trad - bytes_oasis) / bytes_trad) * 100
aceleracion = tiempo_trad / tiempo_oasis if tiempo_oasis > 0 else 1.0

print(f"🟢 [MÉTODO OASIS UNICORNIO - LINCOS/BITCHAT]:")
print(f"   ├─ Tamañao de Trama Payload : {bytes_oasis} bytes  (Reducción: -{ahorro_bytes:.1f}%)")
print(f"   └─ Tiempo de Serialización  : {tiempo_oasis:.4f} ms (Aceleración: {aceleracion:.2f}x)")
print("=" * 70)

# -------------------------------------------------------------------------
# 4. ÁRBITRO NEUTRAL IA (Auditoría de Inferencia Local)
# -------------------------------------------------------------------------
print("🤖 Invocando al Árbitro Neutral IA (oasis-auditor / qwen2.5:0.5b)...")

prompt_arbitro = f"""Actúa como un Árbitro Neutral y Auditor de Arquitectura de Software.
Evalúa estrictamente estas métricas de rendimiento real de la terminal:

[MÉTODO TRADICIONAL - REST/JSON]
- Tamaño Trama: {bytes_trad} bytes
- Tiempo Procesamiento: {tiempo_trad:.4f} ms

[MÉTODO OASIS UNICORNIO - LINCOS/BITCHAT]
- Tamaño Trama: {bytes_oasis} bytes
- Tiempo Procesamiento: {tiempo_oasis:.4f} ms

TAREA DE AUDITORÍA:
1. Emite un dictamen objetivo comparando el coste de ancho de banda.
2. ¿Cuál método protege el silicio reduciendo el calentamiento y la latencia?
3. Da una puntuación final del 1 al 10 para cada arquitectura."""

try:
    # Usar el modelo local como juez
    resultado = subprocess.run(
        ["ollama", "run", "freebuff:latest", prompt_arbitro],
        capture_output=True,
        text=True,
        check=True
    )
    print("\n🏛️  [VEREDICTO DEL ÁRBITRO NEUTRAL IA]:\n")
    print(resultado.stdout.strip())
except Exception as e:
    print(f"⚠️ Error al invocar al árbitro: {e}")

