from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/github-pay', methods=['POST'])
def handle_payment():
    data = request.json
    # Verificamos que sea una suscripción comercial ODSC v1.0
    if data.get('action') == 'created' and 'tier' in data.get('sponsorship', {}):
        tier_name = data['sponsorship']['tier']['name']
        client_id = data['sender']['login']
        
        print(f"💰 PAGO DETECTADO: {client_id} en Tier: {tier_name}")
        
        # Ejecutamos tu motor de concesión holográfica
        result = subprocess.run(
            ['python3', 'scripts/validation/holographic_lease_engine.py'],
            capture_output=True, text=True
        )
        
        return jsonify({"status": "License Issued", "client": client_id}), 200
    return jsonify({"status": "Ignored"}), 400

if __name__ == '__main__':
    app.run(port=5000)
