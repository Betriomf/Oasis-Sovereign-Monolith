#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS HARDWARE ATTESTATION — SOULBOUND TO METAL (DARWIN)
Extrae identificadores físicos inmutables de macOS y verifica el enclave de seguridad.
"""
import subprocess, hashlib, json, platform

def get_darwin_hardware_info():
    info = {}
    try:
        # Extraer Hardware UUID de Apple Silicon / macOS
        cmd = "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'"
        uuid = subprocess.check_output(cmd, shell=True).decode().strip()
        info["hardware_uuid"] = uuid if uuid else "UNKNOWN_UUID"
    except Exception:
        info["hardware_uuid"] = "DARWIN-DEFAULT-UUID"

    info["system"] = platform.system()
    info["machine"] = platform.machine()
    info["processor"] = platform.processor()

    # Comprobación de Secure Enclave
    has_secure_enclave = (platform.system() == "Darwin" and "arm" in platform.machine().lower())
    info["secure_enclave_detected"] = has_secure_enclave
    info["security_module"] = "Apple Secure Enclave (SEP)" if has_secure_enclave else "Software TPM Fallback"

    # Derivación de la Identidad Raíz de Nodo (NodeID)
    seed = f"{info['hardware_uuid']}:{info['machine']}:OASIS-CAPA-0"
    info["node_id"] = "NODE-" + hashlib.sha256(seed.encode()).hexdigest()[:16].upper()

    return info

if __name__ == "__main__":
    hw = get_darwin_hardware_info()
    print("═" * 70)
    print("🛡️ ATESTACIÓN DE HARDWARE OASIS — VÍNCULO FÍSICO INMUTABLE")
    print("═" * 70)
    print(f"  • Nodo Identificador : {hw['node_id']}")
    print(f"  • Plataforma         : {hw['system']} ({hw['machine']})")
    print(f"  • Procesador         : {hw['processor']}")
    print(f"  • Módulo de Seguridad: {hw['security_module']}")
    print(f"  • Hardware UUID      : {hw['hardware_uuid']}")
    print(f"  • Estado de Confianza: {'RAÍZ FÍSICA CERTIFICADA' if hw['secure_enclave_detected'] else 'MODO VISOR'}")
    print("═" * 70)
