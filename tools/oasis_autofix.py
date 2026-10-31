#!/usr/bin/env python3
"""
OASIS SOVEREIGN OS — AUTO-CORRECTOR DE CÓDIGO
Supervisado por Aether 1.5B con validación formal previa (sorry = 0).
"""
import sys
import os
import json
import urllib.request
import subprocess

def test_file_syntax(filepath):
    res = subprocess.run([sys.executable, "-m", "py_compile", filepath], capture_output=True, text=True)
    return res.returncode == 0, res.stderr

def request_fix_from_aether(file_content, error_log):
    prompt = (
        f"Corrige el siguiente error sintáctico de Python de forma limpia y devuelve EXCLUSIVAMENTE "
        f"el bloque de código corregido sin explicaciones ni markdown:\n"
        f"ERROR DETECTADO:\n{error_log}\n\n"
        f"CÓDIGO ORIGINAL:\n{file_content[:2500]}"
    )
    payload = json.dumps({
        "model": "aether:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 400}
    }).encode("utf-8")

    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode())
        return data.get("response", "").replace("```python", "").replace("```", "").strip()

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tools/oasis_autofix.py <archivo.py>")
        sys.exit(1)

    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"❌ Archivo no encontrado: {target_file}")
        sys.exit(1)

    ok, err = test_file_syntax(target_file)
    if ok:
        print(f"✅ El archivo {target_file} ya compila con 0 errores sintácticos.")
        sys.exit(0)

    print(f"⚠️ Error detectado en {target_file}:\n{err}")
    print("🧠 Consultando a Aether 1.5B para generar parche...")

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        fixed_code = request_fix_from_aether(content, err)
        temp_file = target_file + ".autofix_test"
        with open(temp_file, "w", encoding="utf-8") as tf:
            tf.write(fixed_code)

        valid, new_err = test_file_syntax(temp_file)
        if valid:
            os.replace(temp_file, target_file)
            print(f"🎉 [AUTOCORRECCIÓN EXITOSA]: {target_file} reparado y validado con 0 errores.")
        else:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"🛑 [RECHAZO]: El parche propuesto no superó la compilación sintáctica.")
    except Exception as e:
        print(f"❌ Error durante el proceso de reparación: {e}")

if __name__ == "__main__":
    main()
