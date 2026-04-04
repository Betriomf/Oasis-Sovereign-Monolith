import hashlib
import math

class OasisNode:
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance
        self.phi = (1 + 5**0.5) / 2
        self.local_key = hashlib.sha256(f"{name}_{self.phi}".encode()).hexdigest()

    def encrypt_data(self, data):
        # El dato se sintoniza con la frecuencia local
        return hashlib.sha256(f"{data}_{self.local_key}".encode()).hexdigest()

    def contribute_power(self, amount):
        # Navier-Stokes: El flujo de energía genera recompensa
        recompensa = amount * 2.3
        self.balance += recompensa
        return recompensa

def simular_red_mesh():
    print("🌐 OASIS ARPANET: MESH SOBERANO ACTIVO")
    print("=" * 50)

    # 1. Inicializar Nodos (Ayerbe y Barcelona)
    mariano_node = OasisNode("MacBook_Mariano")
    swarm_node = OasisNode("External_Peer_1")

    # 2. Guardar dato en Blockchain Privada (Solo local)
    dato_original = "Mi_Genoma_Privado_2026"
    hash_holografico = mariano_node.encrypt_data(dato_original)
    
    print(f"1. [BORDE] Hash de sintonía generado en local: {hash_holografico[:16]}...")
    print(f"2. [VOLUMEN] Datos fragmentados y dispersos en Swarm_Node.")

    # 3. Intento de acceso externo (Fallo)
    print(f"3. [ATAQUE] Peer_1 intenta reconstruir el dato...")
    if swarm_node.local_key == mariano_node.local_key:
        print("   ACCESO CONCEDIDO")
    else:
        print("   ❌ ERROR: Solo el Nodo Origen tiene la fase pi/phi correcta.")

    # 4. Pago por Recursos
    potencia_pedida = 10 # Gflops
    pago = mariano_node.contribute_power(potencia_pedida)
    print(f"\n4. [ECONOMÍA] Recompensa por potencia: {pago} $SPN (Atractor 2.3)")
    print(f"   Balance de Mariano: {mariano_node.balance} $SPN")

if __name__ == "__main__":
    simular_red_mesh()
