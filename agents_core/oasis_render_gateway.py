#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASIS SOVEREIGN OS — ENTRYPOINT PRINCIPAL
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.http_server import run_server

KERNEL_VERSION = "v16.3.0-ModularHurd"
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    run_server(PORT, KERNEL_VERSION)
