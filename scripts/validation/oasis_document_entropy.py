import os
import math

def calculate_entropy(file_path):
    if not os.path.exists(file_path): return 0
    with open(file_path, 'rb') as f:
        data = f.read()
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

print("🏛️ OASIS INFORMATION DENSITY ANALYZER")
print("="*45)
papers = ["MANIFESTO_KAPPA_2_3.md", "README.md"]
for p in papers:
    e = calculate_entropy(p)
    print(f"📄 Documento: {p} | Entropía: {e:.4f} bits/byte")
    print(f"🛡️  Ajuste κ=2.3: {e/2.3:.4f} (Eficiencia Oasis)")
