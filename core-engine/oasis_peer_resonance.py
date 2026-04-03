import hashlib

class OasisIris:
    def __init__(self, node_id, personality_vector):
        self.node_id = node_id
        self.vector = personality_vector # Un float que representa el Jitter
        self.spn_balance = 500

    def handshake(self, other_node):
        print(f"\n🤝 ENCUENTRO DETECTADO: {self.node_id} <--> {other_node.node_id}")
        
        # Cálculo de la Resonancia (Interferencia)
        resonancia = 1.0 / abs(self.vector - other_node.vector)
        
        if resonancia > 1.5: # Atractor Oasis
            print(f"✨ RESONANCIA ALTA ({resonancia:.2f}): Iniciando intercambio laminar.")
            self.trade_resources(other_node)
        else:
            print(f"🌫️ RESONANCIA BAJA: Manteniendo privacidad de borde.")

    def trade_resources(self, other_node):
        # Navier-Stokes de Créditos
        coste_potencia = 5.5
        print(f"💳 Transacción: {other_node.node_id} alquila 2 Gflops a {self.node_id}")
        self.spn_balance -= coste_potencia
        other_node.spn_balance += coste_potencia
        print(f"💰 Nuevo Balance {self.node_id}: {self.spn_balance} $SPN")

# Simulación en el Mac Aether
def test_encuentro():
    mariano_iris = OasisIris("AYERBE_01", 2.3046)
    desconocido_iris = OasisIris("BCN_99", 2.3048) # Muy cerca en sintonía
    
    mariano_iris.handshake(desconocido_iris)

if __name__ == "__main__":
    test_encuentro()
