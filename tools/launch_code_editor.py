#!/usr/bin/env python3
import os, sys, json
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8085
WORKSPACE = os.path.expanduser("~/Oasis-Sovereign-Monolith")

HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>⚡ OASIS CODE & TERMINAL WORKBENCH</title>
  <link rel="stylesheet" data-name="vs/editor/editor.main" href="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs/editor/editor.main.min.css">
  <style>
    body { margin: 0; background: #1e1e1e; color: #fff; font-family: -apple-system, monospace; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
    .bar { background: #252526; padding: 6px 12px; display: flex; gap: 8px; align-items: center; border-bottom: 1px solid #333; }
    select, button { background: #3c3c3c; color: #fff; border: 1px solid #555; padding: 4px 8px; border-radius: 3px; font-family: inherit; font-size: 0.78rem; }
    button:hover { background: #007acc; cursor: pointer; }
    #main-split { flex: 1; display: flex; flex-direction: column; }
    #editor-box { flex: 6; min-height: 250px; position: relative; }
    #term-box { flex: 4; border-top: 2px solid #005a36; display: flex; flex-direction: column; background: #03060a; }
    .term-bar { background: #0c1a24; padding: 4px 10px; font-size: 0.72rem; color: #00ff9d; display: flex; justify-content: space-between; align-items: center; }
    #term-iframe { width: 100%; flex: 1; border: none; }
  </style>
</head>
<body>
  <div class="bar">
    <strong style="color: #00ff9d;">⚡ OASIS WORKBENCH</strong>
    <select id="fileSelect" onchange="loadFile()">
      <option value="">Selecciona archivo para editar...</option>
      <option value="oasis-core-simulation/src/main.rs">oasis-core-simulation/src/main.rs (Rust)</option>
      <option value="agents_core/oasis_render_gateway.py">agents_core/oasis_render_gateway.py (Gateway)</option>
      <option value="VERDAD_OASIS.txt">VERDAD_OASIS.txt (Pilares)</option>
      <option value="datasets_lean/oasis_lean4_formal_reasoning.jsonl">oasis_lean4_formal_reasoning.jsonl</option>
    </select>
    <button onclick="saveFile()">💾 Guardar Archivo</button>
    <button onclick="document.getElementById('term-iframe').src='http://127.0.0.1:8080/terminal'">🔄 Recargar Terminal</button>
    <span id="status" style="font-size: 0.75rem; color: #00e5ff; margin-left: 10px;"></span>
  </div>

  <div id="main-split">
    <div id="editor-box"></div>
    <div id="term-box">
      <div class="term-bar">
        <span>📟 OASIS TERMINAL WEB (:8080) — CONEXIÓN ACTIVA</span>
        <span>Silicio Frío &lt;= 4.18W</span>
      </div>
      <iframe id="term-iframe" src="http://127.0.0.1:8080/terminal"></iframe>
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs/loader.min.js"></script>
  <script>
    let editor;
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.39.0/min/vs' }});
    require(['vs/editor/editor.main'], function() {
      editor = monaco.editor.create(document.getElementById('editor-box'), {
        value: '// Selecciona un archivo en la barra superior para comenzar a editar\\n',
        language: 'rust',
        theme: 'vs-dark',
        automaticLayout: true
      });
    });

    function loadFile() {
      const f = document.getElementById('fileSelect').value;
      if (!f) return;
      fetch('/read?file=' + encodeURIComponent(f))
        .then(r => r.json())
        .then(d => {
          editor.setValue(d.content);
          const lang = f.endsWith('.rs') ? 'rust' : (f.endsWith('.py') ? 'python' : (f.endsWith('.lean') ? 'lean' : 'markdown'));
          monaco.editor.setModelLanguage(editor.getModel(), lang);
          document.getElementById('status').innerText = 'Cargado: ' + f;
        });
    }

    function saveFile() {
      const f = document.getElementById('fileSelect').value;
      if (!f) return alert('Selecciona un archivo primero');
      fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: f, content: editor.getValue() })
      })
      .then(r => r.json())
      .then(d => {
        document.getElementById('status').innerText = '✅ Guardado: ' + new Date().toLocaleTimeString();
      });
    }
  </script>
</body>
</html>"""

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/edit"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        elif self.path.startswith("/read?"):
            fname = self.path.split("file=")[1]
            import urllib.parse
            fname = urllib.parse.unquote(fname)
            fpath = os.path.join(WORKSPACE, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f: c = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"content": c}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            fpath = os.path.join(WORKSPACE, data["file"])
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(data["content"])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "OK"}).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
