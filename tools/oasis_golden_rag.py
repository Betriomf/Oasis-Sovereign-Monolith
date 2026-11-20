import json
import math
import re
import sys
from pathlib import Path

DATASET = Path("vault/datasets/oasis_crm_sft_dataset.jsonl")
MAX_CHARS = 750  # ~200 tokens: prefill casi instantáneo en CPU

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_áéíóúñ\^\-]+", text.lower()))

def retrieve_fast(query: str) -> str:
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
                scored.append((overlap / math.sqrt(max(len(tokens), 1)), row))

    scored.sort(key=lambda x: x[0], reverse=True)
    out, used = [], 0
    for _, row in scored[:4]:
        chunk = f"- {row['output']}"
        if used + len(chunk) + 1 > MAX_CHARS:
            break
        out.append(chunk)
        used += len(chunk) + 1
    return "\n".join(out) if out else "- Sin coincidencias directas en el CRM."

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip() or "Paper Y Lean 4"
    print(retrieve_fast(q))
