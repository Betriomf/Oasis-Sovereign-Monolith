import os
import glob
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Oasis Sovereign Reasoning Engine", version="1.1.0")

OLLAMA_ENDPOINT = "http://127.0.0.1:11434/api/generate"
MONOLITH_DIR = os.path.expanduser("~/Oasis-Sovereign-Monolith")

class ScienceQuery(BaseModel):
    pilar_num: int
    question: str
    model: str = "oasis-phi3-laminar:latest"

def fetch_pilar_context(pilar_num: int) -> str:
    truth_file = os.path.join(MONOLITH_DIR, "VERDAD_OASIS.txt")
    pilar_summary = ""
    if os.path.exists(truth_file):
        with open(truth_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip().startswith(f"{pilar_num}."):
                    pilar_summary = line.strip()
                    break

    pilar_str = f"{pilar_num:03d}" if pilar_num < 1000 else str(pilar_num)
    docs = glob.glob(os.path.join(MONOLITH_DIR, f"docs/*PILAR_{pilar_str}*.md"))
    doc_content = ""
    if docs:
        with open(docs[0], "r", encoding="utf-8", errors="ignore") as f:
            doc_content = f.read()[:2000]

    return f"Axioma: {pilar_summary}\nDetalle:\n{doc_content}"

@app.post("/v1/science/ask")
async def query_sovereign_kernel(query: ScienceQuery):
    context = fetch_pilar_context(query.pilar_num)
    system_instruction = (
        "SYSTEM: Eres ÆTHER de Oasis Capa 0. Responde en LaTeX conciso sin saludos.\n"
        f"Contexto Inyectado:\n{context}\n"
    )

    full_prompt = f"{system_instruction}\nPregunta: {query.question}"

    payload = {
        "model": query.model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.23,
            "num_predict": 384,
            "num_thread": 2
        }
    }

    # Timeout extendido a 300 segundos para dar margen en carga de pesos
    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, read=300.0)) as client:
        try:
            res = await client.post(OLLAMA_ENDPOINT, json=payload)
            if res.status_code != 200:
                return {
                    "error": "Ollama Error",
                    "status_code": res.status_code,
                    "raw": res.text
                }
            data = res.json()
            return {
                "pilar": query.pilar_num,
                "model_used": query.model,
                "context_bytes": len(context),
                "analysis_latex": data.get("response", "").strip()
            }
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="Tiempo de inferencia agotado (RAM ocupada)")
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Ollama no está iniciado en 127.0.0.1:11434")
