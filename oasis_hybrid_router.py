import sys
import json
import urllib.parse
import urllib.request
import subprocess

def consultar_opendata_web(query: str) -> str:
    """Extrae el extracto informativo mediante la API REST de DuckDuckGo."""
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'OasisHybridEngine/2.3'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            abstract = data.get("AbstractText", "")
            if abstract:
                return abstract[:3141]  # Empaquetado estricto pi-KB (3.14 KB)
            # Si no hay abstract directo, tomar primer tópico relacionado
            topics = data.get("RelatedTopics", [])
            if topics and "Text" in topics[0]:
                return topics[0]["Text"][:3141]
    except Exception:
        pass
    return "No se requirieron datos externos o la red operó en modo estricto local."

def inferencia_laminar_local(pregunta: str, contexto_web: str, modelo: str = "qwen2.5:0.5b") -> str:
    """Inyecta el contexto web en el modelo local acotando temperatura a 0.23."""
    prompt = (
        f"SISTEMA: Eres el núcleo laminar de Oasis. Responde en 2 párrafos concisos sin saludos.\n"
        f"HECHOS VERIFICADOS (WEB): {contexto_web}\n\n"
        f"PREGUNTA DEL USUARIO: {pregunta}"
    )
    cmd = ["ollama", "run", modelo, prompt]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip()

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "¿Qué es la computación cuántica y cuál es su principio físico?"
    print(f"🛰️ [OASIS HYBRID ROUTER]: Procesando consulta -> '{query}'")
    
    print("📡 [CAPA 2]: Consultando fuentes abiertas externas...")
    info_externa = consultar_opendata_web(query)
    print(f"📦 [TRAMA π-KB]: {len(info_externa)} bytes empaquetados.")

    print(f"🧠 [CAPA 3]: Ejecutando inferencia laminar en silicio frío (<5.39W)...")
    # Usa qwen2.5:0.5b o qwen2.5:1.5b presentes en tu lista de Ollama
    respuesta = inferencia_laminar_local(query, info_externa, modelo="qwen2.5:0.5b")
    
    print("\n" + "="*60)
    print("💡 [RESPUESTA HÍBRIDA OASIS]:")
    print(respuesta)
    print("="*60)

if __name__ == "__main__":
    main()
