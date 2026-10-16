# -*- coding: utf-8 -*-
"""Módulo Atómico de Auto-Parcheo con Linter AST y Hot-Reloading."""

import os
import sys
import ast
import time
import shutil
import hashlib
import threading

def read_source_file(target_file: str) -> dict:
    safe_name = os.path.basename(target_file)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = target_file if os.path.exists(target_file) else os.path.join(base_dir, safe_name)
    if not os.path.exists(full_path):
        return {"error": f"Archivo '{target_file}' no encontrado"}
    with open(full_path, "r", encoding="utf-8") as f:
        return {"file": target_file, "content": f.read()}

def apply_code_patch(target_file: str, new_content: str, hot_reload: bool = True) -> dict:
    safe_name = os.path.basename(target_file)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = target_file if os.path.exists(target_file) else os.path.join(base_dir, safe_name)

    # 1. Validación de Sintaxis en Memoria mediante AST
    if full_path.endswith(".py"):
        try:
            ast.parse(new_content)
        except SyntaxError as err:
            return {
                "success": False,
                "status": "ERROR_SYNTAX",
                "detail": f"⛔ Error de sintaxis (Línea {err.lineno}, Col {err.offset}): {err.msg}"
            }

    # 2. Respaldo Automático (.bak)
    if os.path.exists(full_path):
        try:
            shutil.copyfile(full_path, f"{full_path}.bak")
        except Exception:
            pass

    # 3. Escritura Atómica (.tmp -> fsync -> replace)
    tmp_path = f"{full_path}.tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, full_path)
    except Exception as err:
        return {"success": False, "status": "ERROR_WRITE", "detail": str(err)}

    sha256_hash = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

    # 4. Reinicio en Caliente (Hot-Reload)
    if hot_reload:
        def trigger_restart():
            time.sleep(0.5)
            print(f"🔄 [HOT-RELOAD] Reiniciando Gateway modular ({sha256_hash[:10]})...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        threading.Thread(target=trigger_restart, daemon=True).start()

    return {
        "success": True,
        "status": "SUCCESS_REBOOTING",
        "file": full_path,
        "sha256": sha256_hash
    }
