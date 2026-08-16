#!/usr/bin/env python3
"""
OASIS AUTONOMOUS SENTINEL DAEMON
Mantenimiento autónomo en segundo plano a cero fricción
Autor: Mariano Panzano Caballé (@Betriomf)
Licencia: GNU AGPLv3
"""

import subprocess
import time
from pathlib import Path

REPO = Path.home() / "Oasis-Sovereign-Monolith"

def ciclo_mantenimiento():
    # 1. Purgar cachés internas pesadas
    subprocess.run(["python3", str(REPO / "agents_core" / "oasis_appsupport_purger.py")], capture_output=True)
    # 2. Purgar residuos huérfanos de runtimes
    subprocess.run(["python3", str(REPO / "agents_core" / "oasis_nvm_rust_pruner.py")], capture_output=True)
    # 3. Compactar histórico
    subprocess.run(["python3", str(REPO / "agents_core" / "oasis_holographic_sweep.py")], capture_output=True)

if __name__ == "__main__":
    ciclo_mantenimiento()
