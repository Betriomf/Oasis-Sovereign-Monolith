# -*- coding: utf-8 -*-
import os
import sys
import ast
import time
import shutil
import hashlib
import threading

def read_source(target_file: str) -> dict:
    safe_name = os.path.basename(target_file)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = target_file if os.path.exists(target_file) else os.path.join(base_dir, safe_name)
    if not os.path.exists(full_path):
        return {"error": f"Archivo '{target_file}' no encontrado"}
    with open(full_path, "r", encoding="utf-8") as f:
        return {"file": target_file, "content": f.read()}

def apply_patch(target_file: str, new_content: str, hot_reload: bool = True) -> dict:
    safe_name = os.path.basename(target_file)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = target_file if os.path.exists(target_file) else os.path.join(base_dir, safe_name)

    if full_path.endswith(".py"):
        try:
            ast.parse(new_content)
        except SyntaxError as err:
            return {"success": False, "status": "ERROR_SYNTAX", "detail": f"Línea {err.lineno}: {err.msg}"}

    if os.path.exists(full_path):
        try:
            shutil.copyfile(full_path, f"{full_path}.bak")
        except Exception:
            pass

    tmp_path = f"{full_path}.tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, full_path)
    except Exception as err:
        return {"success": False, "status": "ERROR_WRITE", "detail": str(err)}

    sha256 = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

    if hot_reload:
        def _reboot():
            time.sleep(0.5)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        threading.Thread(target=_reboot, daemon=True).start()

    return {"success": True, "status": "SUCCESS_REBOOTING", "file": full_path, "sha256": sha256}
