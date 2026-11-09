#!/usr/bin/env python3
"""
OASIS LINCOS COMPACT RADIO CODEC (v1.1)
Empaqueta telemetría cardiovascular SOAP y GPS en exactamente 21 bytes binarios (<= 32 bytes).
Diseñado para enlaces LoRa SX1262 (868 MHz) y mallas Bitchat BLE.
"""
import struct
import zlib
import sys
import json

MAGIC_LINCOS = 0xAA

def pack_lincos_frame(node_id: str, lat: float, lon: float, triage_level: int,
                       pas: int, pad: int, fc: int, spo2: int, wss: float, enstrophy: float) -> bytes:
    # 1. Identidad de nodo: Hash 4 bytes
    node_hash = zlib.crc32(node_id.encode("utf-8")) & 0xFFFFFFFF
    
    # 2. GPS empaquetado en enteros de 24 bits (6 bytes en total)
    lat_i = int((lat + 90.0) * 100000) & 0xFFFFFF
    lon_i = int((lon + 180.0) * 100000) & 0xFFFFFF
    gps_bytes = struct.pack(">I", lat_i)[1:] + struct.pack(">I", lon_i)[1:]

    # 3. Triaje y constantes hemodinámicas escaladas
    status_flags = 0x01  # Bit 0: Silicio Frío Activo (<= 3.78 W)
    wss_scaled = int(min(max(wss, 0.0), 15.0) * 10) & 0xFF
    omega_residual = int(max(enstrophy - 5.2900, 0.0) * 10000) & 0xFF
    
    # Payload = 1 (Magic) + 4 (Hash) + 6 (GPS) + 8 (Bytes individuales) = 19 bytes
    payload = struct.pack(
        ">BI6sBBBBBBBB",
        MAGIC_LINCOS,
        node_hash,
        gps_bytes,
        status_flags,
        triage_level & 0xFF,
        pas & 0xFF,
        pad & 0xFF,
        fc & 0xFF,
        spo2 & 0xFF,
        wss_scaled,
        omega_residual
    )
    
    # 4. Checksum CRC16 (2 bytes) -> Total trama: 19 + 2 = 21 bytes
    crc16 = zlib.crc32(payload) & 0xFFFF
    full_frame = payload + struct.pack(">H", crc16)
    return full_frame

def unpack_lincos_frame(frame: bytes) -> dict:
    if len(frame) != 21:
        raise ValueError(f"Longitud de trama inválida: {len(frame)} bytes (esperados 21)")
    
    magic, node_hash, gps_raw, status_flags, triage_lvl, pas, pad, fc, spo2, wss_scaled, omega_res, crc16 = struct.unpack(
        ">BI6sBBBBBBBBH", frame
    )
    
    if magic != MAGIC_LINCOS:
        raise ValueError("Cabecera LINCOS inválida")
        
    calc_crc = zlib.crc32(frame[:19]) & 0xFFFF
    if calc_crc != crc16:
        raise ValueError("Fallo de integridad CRC16 en radioenlace")

    lat_i = struct.unpack(">I", b'\x00' + gps_raw[:3])[0]
    lon_i = struct.unpack(">I", b'\x00' + gps_raw[3:])[0]
    lat = round((lat_i / 100000.0) - 90.0, 5)
    lon = round((lon_i / 100000.0) - 180.0, 5)

    wss = round(wss_scaled / 10.0, 2)
    enstrophy = round(5.2900 + (omega_res / 10000.0), 4)

    triage_map = {
        1: "NIVEL 1 - CRÍTICO",
        2: "NIVEL 2 - URGENCIA",
        3: "NIVEL 3 - PRECAUCIÓN",
        4: "NIVEL 4 - ESTABLE"
    }

    return {
        "bytes_total": len(frame),
        "node_hash": f"0x{node_hash:08x}",
        "status_cold_silicon": bool(status_flags & 0x01),
        "gps": {"lat": lat, "lon": lon},
        "triage": triage_map.get(triage_lvl, "DESCONOCIDO"),
        "telemetry": {
            "pas": pas,
            "pad": pad,
            "fc": fc,
            "spo2": spo2,
            "wss_pa": wss,
            "enstrophy_omega": enstrophy,
            "confinement": enstrophy <= 5.3019
        }
    }

if __name__ == "__main__":
    packed = pack_lincos_frame(
        node_id="did:key:zOasisBadalona01",
        lat=41.4469,
        lon=2.2458,
        triage_level=2,
        pas=142,
        pad=91,
        fc=82,
        spo2=97,
        wss=4.52,
        enstrophy=5.2967
    )
    
    hex_repr = packed.hex()
    unpacked = unpack_lincos_frame(packed)

    print("════════════════════════════════════════════════════════════════")
    print("📡 [CÓDEC LINCOS OFF-GRID]: TELEMETRÍA ULTRA-COMPRIMIDA")
    print("────────────────────────────────────────────────────────────────")
    print(f"• Tamaño de Trama Binaria      : {len(packed)} bytes (Límite: <= 32 bytes)")
    print(f"• Trama Hexadecimal (Radio TX) : {hex_repr}")
    print(f"• Carga Útil Decodificada      :")
    print(json.dumps(unpacked, indent=2, ensure_ascii=False))
    print("════════════════════════════════════════════════════════════════")
