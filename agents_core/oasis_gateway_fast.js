const http = require('http');
const { spawn, exec } = require('child_process');

const PORT = process.env.PORT || 8080;
const OLLAMA_PORT = 11434;

// Asegura que Ollama esté corriendo en el puerto 11434
function ensureOllamaRunning() {
    exec('lsof -i :11434', (err, stdout) => {
        if (err || !stdout) {
            console.log('⚡ [OASIS GATEWAY]: Levantando Ollama en segundo plano...');
            const ollama = spawn('ollama', ['serve'], { detached: true, stdio: 'ignore' });
            ollama.unref();
        }
    });
}

ensureOllamaRunning();

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'OK', engine: 'Oasis Node.js Fast Gateway', port: PORT }));
        return;
    }

    if (req.url === '/api/chat' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const parsed = JSON.parse(body);
                const promptText = parsed.prompt || '';

                const ollamaReq = http.request({
                    hostname: '127.0.0.1',
                    port: OLLAMA_PORT,
                    path: '/api/generate',
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                }, (ollamaRes) => {
                    let ollamaData = '';
                    ollamaRes.on('data', chunk => { ollamaData += chunk.toString(); });
                    ollamaRes.on('end', () => {
                        try {
                            const jsonRes = JSON.parse(ollamaData);
                            res.writeHead(200, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ response: jsonRes.response }));
                        } catch (e) {
                            res.writeHead(500, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ error: 'Error al parsear respuesta de Ollama' }));
                        }
                    });
                });

                ollamaReq.on('error', () => {
                    ensureOllamaRunning();
                    res.writeHead(503, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Iniciando Ollama en segundo plano. Reintenta en 3 segundos...' }));
                });

                const payload = JSON.stringify({
                    model: 'oasis-aether-soup:1.5b',
                    prompt: `[SISTEMA OASIS OS - LEAN 4 & SILICIO FRÍO <= 4.18W]:\n${promptText}`,
                    stream: false,
                    options: { temperature: 0.05, num_predict: 1024, num_thread: 2 }
                });

                ollamaReq.write(payload);
                ollamaReq.end();

            } catch (err) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'JSON inválido' }));
            }
        });
        return;
    }

    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 - Ruta no encontrada');
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`⚡ [OASIS NODE GATEWAY]: Servidor activo en http://127.0.0.1:${PORT}`);
    console.log(`🖥️  API lista para recibir peticiones sin sobrecarga de CPU`);
});
