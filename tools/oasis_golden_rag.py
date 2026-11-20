import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(".")
DATASET = ROOT / "vault/datasets/oasis_crm_sft_dataset.jsonl"
SNAPSHOT = ROOT / "vault/OASIS_AI_CONTEXT_SNAPSHOT.md"

# Presupuesto total de caracteres (~1000 tokens) repartido en 61.8% / 38.2%
TOTAL_BUDGET = 3800
PRIMARY_BUDGET = int(round(TOTAL_BUDGET * 0.6180339887))   # ~2349 chars
CONTEXT_BUDGET = TOTAL_BUDGET - PRIMARY_BUDGET             # ~1451 chars

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ\^\-]+", text.lower()))

def retrieve_golden_context(query: str) -> str:
    q_tokens = tokenize(query)
    scored = []

    if DATASET.exists():
        for line in DATASET.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            blob = f"{row.get('instruction', '')} {row.get('output', '')}"
            tokens = tokenize(blob)
            overlap = len(q_tokens & tokens)
            if overlap > 0:
                score = overlap / math.sqrt(max(len(tokens), 1))
                scored.append((score, row))

    scored.sort(key=lambda x: x[0], reverse=True)

    primary_chunks = []
    used_primary = 0
    for _, row in scored:
        entry = f"- [{row.get('source', 'crm')}] {row['instruction']} -> {row['output']}"
        if used_primary + len(entry) + 1 > PRIMARY_BUDGET:
            break
        primary_chunks.append(entry)
        used_primary += len(entry) + 1

    # Parte secundaria (38.2%): últimas líneas más recientes del snapshot
    recent_tail = ""
    if SNAPSHOT.exists():
        lines = SNAPSHOT.read_text(encoding="utf-8").splitlines()
        tail_lines = []
        used_ctx = 0
        for ln in reversed(lines):
            if used_ctx + len(ln) + 1 > CONTEXT_BUDGET:
                break
            tail_lines.append(ln)
            used_ctx += len(ln) + 1
        recent_tail = "\n".join(reversed(tail_lines))

    return (
        "=== EVIDENCIA RECUPERADA (61.8% RAG ÁUREO) ===\n"
        + ("\n".join(primary_chunks) if primary_chunks else "(Sin coincidencias exactas en JSONL)")
        + "\n\n=== ESTADO RECIENTE DEL REPOSITORIO (38.2%) ===\n"
        + recent_tail
    )

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() or "Paper Y L=2^4 L=3^4 Lean 4"
    print(retrieve_golden_context(q))
