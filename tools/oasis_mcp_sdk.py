#!/usr/bin/env python3
"""OASIS MCP & ORACLE CLIENT SDK (Zero-Dependencies, Apache 2.0 / AGPLv3)"""
import json
import sys
import urllib.request

class OasisClient:
    def __init__(self, base_url="https://oasis-sovereign-wind-node.onrender.com"):
        self.base_url = base_url.rstrip("/")

    def ask(self, query):
        req = urllib.request.Request(
            f"{self.base_url}/v1/mcp",
            data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "ask", "arguments": {"query": query}}}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as r:
            res = json.loads(r.read().decode("utf-8"))
        return res["result"]["content"][0]["text"]

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 2 else "http://127.0.0.1:8080"
    q = sys.argv[2] if len(sys.argv) > 2 else (sys.argv[1] if len(sys.argv) > 1 else "Pilar 388")
    print(OasisClient(url).ask(q))
