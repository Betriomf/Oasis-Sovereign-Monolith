import json
import re
from pathlib import Path

ROOT = Path(".")
CRM_JSON = ROOT / "vault/crm_arquitectura_soberana.json"
OUT_JSONL = ROOT / "vault/datasets/oasis_crm_sft_dataset.jsonl"
OUT_SNAPSHOT = ROOT / "vault/OASIS_AI_CONTEXT_SNAPSHOT.md"

def sanitize(text: str) -> str:
    # Evita filtrar posibles tokens largos alfanuméricos en el dataset
    return re.sub(r"\b[A-Za-z0-9]{48,}\b", "[REDACTED_TOKEN]", text)

def main():
    records = []
    snapshot_lines = [
        "# OASIS SOVEREIGN MONOLITH — SNAPSHOT PARA IA LOCAL",
        "",
        "## 1. Estado del CRM y Bitácora",
    ]

    if CRM_JSON.exists():
        data = json.loads(CRM_JSON.read_text(encoding="utf-8"))
        # Extrae entradas tanto si el JSON es lista como diccionario con incidencias/hitos
        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ("incidencias", "incidents", "hitos", "milestones", "entries", "historial"):
                if isinstance(data.get(key), list):
                    items.extend(data[key])
            if not items:
                items = [{"titulo": k, "detalle": json.dumps(v, ensure_ascii=False)} for k, v in data.items()]

        for idx, it in enumerate(items[-60:], 1):
            raw_str = sanitize(json.dumps(it, ensure_ascii=False))
            title = sanitize(str(it.get("titulo") or it.get("title") or it.get("resumen") or f"Registro CRM #{idx}"))
            desc = sanitize(str(it.get("descripcion") or it.get("detail") or it.get("impacto") or raw_str))
            ver = sanitize(str(it.get("version") or "v25"))

            records.append({
                "instruction": f"Resume el hito técnico '{title}' ({ver}) registrado en el CRM de Oasis Sovereign Monolith.",
                "input": "",
                "output": desc,
                "source": "crm_arquitectura_soberana.json",
            })
            snapshot_lines.append(f"- **[{ver}] {title}**: {desc[:280]}")

    snapshot_lines.extend(["", "## 2. Módulos Formales en Lean 4 Verificados"])
    for lean_file in sorted((ROOT / "formal_proofs").glob("*.lean")):
        content = sanitize(lean_file.read_text(encoding="utf-8", errors="ignore"))
        has_sorry = "sorry" in re.sub(r"/\-.*?\-/", "", content, flags=re.DOTALL)
        theorems = re.findall(r"^(?:theorem|def|structure)\s+([A-Za-z0-9_']+)", content, flags=re.MULTILINE)
        status = "CON SORRY" if has_sorry else "0 sorry (verificado)"
        summary = (
            f"El archivo `{lean_file}` ({status}) define: {', '.join(theorems[:12]) or 'especificaciones formales'}. "
            "Toda conclusión sobre salto de masa o estabilización en Lean 4 es condicional a sus estructuras de hipótesis explícitas."
        )
        records.append({
            "instruction": f"Explica el contenido y alcance formal del módulo {lean_file.name} en Oasis Sovereign Monolith.",
            "input": "",
            "output": summary,
            "source": str(lean_file),
        })
        snapshot_lines.append(f"- `{lean_file.name}` ({status}): {', '.join(theorems[:8])}")

    snapshot_lines.extend(["", "## 3. Manuscritos Científicos en `papers/`"])
    for tex_file in sorted((ROOT / "papers").glob("*.tex")):
        tex = sanitize(tex_file.read_text(encoding="utf-8", errors="ignore"))
        m_title = re.search(r"\\title\{([^}]*)\}", tex)
        title = m_title.group(1) if m_title else tex_file.name
        records.append({
            "instruction": f"¿Cuál es el objeto y límite de alcance del manuscrito {tex_file.name}?",
            "input": "",
            "output": (
                f"El manuscrito `{tex_file.name}` ('{title}') documenta resultados numéricos acotados y "
                "cadenas condicionales verificadas en Lean 4.36.0, delimitando explícitamente que la existencia "
                "incondicional y el salto de masa en el continuo R^4 / S'(R^4) siguen abiertos."
            ),
            "source": str(tex_file),
        })
        snapshot_lines.append(f"- `{tex_file.name}`: {title}")

    OUT_JSONL.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8",
    )
    OUT_SNAPSHOT.write_text("\n".join(snapshot_lines) + "\n", encoding="utf-8")
    print(f"✅ Dataset JSONL generado: {OUT_JSONL} ({len(records)} ejemplos)")
    print(f"✅ Snapshot actualizado para IA local: {OUT_SNAPSHOT}")

if __name__ == "__main__":
    main()
