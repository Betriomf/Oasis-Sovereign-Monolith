import os
import shutil
import asyncio
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Oasis MovieBox Stream API", version="2.0.0")

class StreamResolution(BaseModel):
    title: str
    stream_url: str
    status: str
    engine: str

@app.get("/v1/guide/download")
async def download_architecture_guide():
    guide_path = os.path.expanduser("~/Oasis-Sovereign-Monolith/docs/MATRIX_INTERPRETATION_GUIDE.md")
    if not os.path.exists(guide_path):
        raise HTTPException(status_code=404, detail="Guía no encontrada en el repositorio")
    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"guide": "MATRIX_INTERPRETATION_GUIDE", "bytes": len(content), "payload": content}

@app.get("/v1/movies/stream", response_model=StreamResolution)
async def resolve_movie_stream(q: str = Query(..., description="Título de la película")):
    moviebox_bin = shutil.which("moviebox") or "/usr/local/bin/moviebox"
    if not os.path.exists(moviebox_bin):
        return StreamResolution(
            title=q,
            stream_url="https://mock-stream.oasis-engine.local/stream.m3u8",
            status="FALLBACK_LOCAL",
            engine="Oasis-Internal-Scraper"
        )

    proc = await asyncio.create_subprocess_exec(
        moviebox_bin, "--get-stream", q,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=502, detail="Fallo al resolver streaming")
    return StreamResolution(
        title=q,
        stream_url=stdout.decode().strip(),
        status="RESOLVED_OK",
        engine="MovieBox-Darwin-Native"
    )
