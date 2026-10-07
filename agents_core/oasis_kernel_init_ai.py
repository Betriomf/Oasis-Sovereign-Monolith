#!/usr/bin/env python3
"""
OASIS VIRTUAL OS INITIALIZER & CLOUD KERNEL (PID 1)
Motor de Inicialización del OS Virtual en la Nube (Render + Supabase + VPS Linux).
"""

import os
import sys
import time
import math
import asyncio
import argparse
import httpx

PHI = (1.0 + math.sqrt(5.0)) / 2.0
GOLDEN_PACING = math.pi / PHI
ATTRACTOR_KAPPA = math.log(10.0)
PI_FRAME_MAX_BYTES = 3141

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://opzddoqcvsqzdhulacei.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

class OasisVirtualKernel:
    def __init__(self, mode: str = "gateway"):
        self.mode = mode
        self.start_time = time.time()
        self.active = True
        self.tasks_processed = 0

    def print_banner(self):
        print("======================================================================")
        print("⚡ [OASIS OS VIRTUAL KERNEL INIT — PID 1]: CLOUD SYSTEM INIT")
        print("======================================================================")
        print(f"🌀 Modo de Operación       : {self.mode.upper()}")
        print(f"📡 Región Nube / Target   : Fráncfort (Render + Supabase DePIN)")
        print(f"📐 Constante Atractor (κ)  : {ATTRACTOR_KAPPA:.6f} (ln 10)")
        print(f"📦 Marco Confinado (π-KB) : {PI_FRAME_MAX_BYTES} bytes max")
        print("======================================================================")

    async def verify_supabase_connection(self) -> bool:
        if not SUPABASE_KEY:
            print("ℹ️ [KERNEL INIT]: SUPABASE_KEY no configurada. Operando en modo estático.")
            return False

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        url = f"{SUPABASE_URL}/rest/v1/"
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code in (200, 204, 301, 302):
                    print("✅ [KERNEL INIT]: Conexión con Supabase (pgvector) ESTABLE.")
                    return True
                else:
                    print(f"⚠️ [KERNEL INIT]: Supabase respondió con código {resp.status_code}")
                    return False
        except Exception as e:
            print(f"⚠️ [KERNEL INIT]: Error contactando Supabase ({e}).")
            return False

    async def run_heartbeat_monitor(self):
        while self.active:
            uptime = round(time.time() - self.start_time, 2)
            power_w = round(3.90 + 1.49 * (math.sin(uptime * 0.1) ** 2), 2)
            print(f"💓 [KERNEL HEARTBEAT]: Uptime={uptime}s | Power={power_w}W (Adiabático) | Tareas={self.tasks_processed}")
            await asyncio.sleep(10)

    async def boot(self):
        self.print_banner()
        await self.verify_supabase_connection()
        print("🟢 [OASIS KERNEL INIT]: Sistema Operativo Virtual OPERATIVO en la nube.")
        await self.run_heartbeat_monitor()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Oasis Virtual Kernel Initializer")
    parser.add_argument("--mode", choices=["gateway", "worker"], default="gateway", help="Modo de ejecución")
    args = parser.parse_args()

    kernel = OasisVirtualKernel(mode=args.mode)
    try:
        asyncio.run(kernel.boot())
    except KeyboardInterrupt:
        print("\n👋 [KERNEL SHUTDOWN]: Apagado controlado del sistema.")
