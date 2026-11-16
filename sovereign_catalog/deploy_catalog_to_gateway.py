#!/usr/bin/env python3
"""
Ensamblador Maestro del Diccionario Soberano:
Lee sovereign_catalog/INDEX.json, valida todos los módulos independientes
y sincroniza el enrutador unificado en agents_core/oasis_render_gateway.py.
"""
import json
import py_compile
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_DIR = BASE_DIR / "sovereign_catalog"
INDEX_FILE = CATALOG_DIR / "INDEX.json"
GATEWAY_FILE = BASE_DIR / "agents_core" / "oasis_render_gateway.py"

def verify_all_catalog_modules() -> list[dict]:
    data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    modules = data.get("modules", [])
    print(f"📚 [DICCIONARIO SOBERANO]: Auditando {len(modules)} módulos independientes...")
    for m in modules:
        mod_path = BASE_DIR / m["file"]
        if not mod_path.exists():
            print(f"  ❌ Falta el archivo del módulo {m['id']}: {mod_path}")
            sys.exit(1)
        py_compile.compile(str(mod_path), doraise=True)
        print(f"  ✅ Módulo {m['id']} ({m['command']:<28}) -> {m['file']} [OK]")
    return modules

def inject_unified_dispatcher():
    code = GATEWAY_FILE.read_text(encoding="utf-8")
    marker = "# === SOVEREIGN CATALOG UNIFIED DISPATCHER ==="
    end_marker = "# === END SOVEREIGN CATALOG DISPATCHER ==="

    dispatcher_block = f"""        {marker}
        import importlib.util as _ilu
        from pathlib import Path as _Path
        _cat_dir = _Path(__file__).resolve().parent.parent / "sovereign_catalog"
        _cat_map = {{
            "riona": ("01_riona_sentinel.py", "riona_process", True),
            "qr": ("02_qr_gossip.py", "qr_process", True),
            "mesh": ("02_qr_gossip.py", "mesh_process", False),
            "id": ("02_qr_gossip.py", "id_process", False),
            "check_hash": ("02_qr_gossip.py", "check_hash_process", True),
            "webgpu": ("03_webgpu_play.py", "webgpu_process", True),
            "play": ("03_webgpu_play.py", "play_process", True),
            "boost-gta": ("03_webgpu_play.py", "play_process", True),
            "sheets": ("04_sovereign_sheets.py", "sheets_process", True),
            "modules": ("05_modules_registry.py", "modules_process", True),
            "catalog": ("05_modules_registry.py", "modules_process", True),
            "fiscal": ("06_fiscal_local.py", "fiscal_process", True),
            "verify_bin": ("07_verify_bin_uma.py", "verify_bin_process", True),
            "soc": ("07_verify_bin_uma.py", "verify_bin_process", True),
            "ai": ("08_ai_vault_oracle.py", "ai_process", True),
            "v": ("08_ai_vault_oracle.py", "ai_process", True),
            "pilares": ("08_ai_vault_oracle.py", "ai_process", True),
            "cloud": ("09_cloud_always_on.py", "cloud_process", True),
            "always-on": ("09_cloud_always_on.py", "cloud_process", True),
            "nod": ("10_sovereign_nod_flow.py", "nod_process", True),
            "flow": ("10_sovereign_nod_flow.py", "nod_process", True),
            "edge0": ("11_edge0_1458.py", "edge0_process", True),
            "1458": ("11_edge0_1458.py", "edge0_process", True),
        }}
        if skill in _cat_map:
            _fname, _fn_name, _takes_arg = _cat_map[skill]
            _spec = _ilu.spec_from_file_location("cat_mod_" + skill, str(_cat_dir / _fname))
            _mod = _ilu.module_from_spec(_spec)
            _spec.loader.exec_module(_mod)
            _fn = getattr(_mod, _fn_name)
            _res = _fn(payload.get("prompt", "")) if _takes_arg else _fn()
            self._send_json({{"skill": skill, "output": _res, "status": "COMPLETED"}})
            return
        {end_marker}"""

    if marker in code and end_marker in code:
        start = code.find(marker) - 8
        end = code.find(end_marker) + len(end_marker)
        code = code[:start] + dispatcher_block + code[end:]
    else:
        lines = code.splitlines()
        out = []
        inserted = False
        for ln in lines:
            out.append(ln)
            if not inserted and "skill = " in ln and 'payload.get("skill"' in ln:
                out.append(dispatcher_block)
                inserted = True
        code = "\n".join(out) + "\n"

    GATEWAY_FILE.write_text(code, encoding="utf-8")
    py_compile.compile(str(GATEWAY_FILE), doraise=True)
    print("🔗 Gateway sincronizado con todo el Diccionario Soberano (0 errores de ruta).")

if __name__ == "__main__":
    verify_all_catalog_modules()
    inject_unified_dispatcher()
