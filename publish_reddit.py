#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import base64
import sys

# Credenciales de tu app en reddit.com/prefs/apps
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"
REDDIT_USER = "TU_USUARIO_REDDIT"
REDDIT_PASS = "TU_CONTRASEÑA_REDDIT"

SUBREDDIT = "webdev"  # O gamedev, netsec
TITLE = "[Show HN / Launch] Oasis Shield: Zero-PII Anti-Bot & 16-Byte Netcode Stream"

# Leer el contenido del markdown desde el archivo del anuncio
with open("README.md", "r", encoding="utf-8") as f:
    MARKDOWN_BODY = f.read()

def get_reddit_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    url = "https://www.reddit.com/api/v1/access_token"
    data = urllib.parse.urlencode({
        "grant_type": "password",
        "username": REDDIT_USER,
        "password": REDDIT_PASS
    }).encode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "User-Agent": "OasisPublisher/1.0 by " + REDDIT_USER
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode()).get("access_token")

def submit_post(token):
    url = "https://oauth.reddit.com/api/submit"
    payload = urllib.parse.urlencode({
        "sr": SUBREDDIT,
        "kind": "self",
        "title": TITLE,
        "text": MARKDOWN_BODY,
        "api_type": "json"
    }).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "OasisPublisher/1.0 by " + REDDIT_USER
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print("✅ Respuesta de Reddit:", data)

if __name__ == "__main__":
    if CLIENT_ID == "TU_CLIENT_ID":
        print("⚠️ Introduce tus credenciales en publish_reddit.py antes de ejecutar.")
        sys.exit(1)
    token = get_reddit_token()
    submit_post(token)
