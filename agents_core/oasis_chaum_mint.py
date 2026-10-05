#!/usr/bin/env python3
import secrets
import hashlib

def generate_simple_keys():
    # Par RSA demostrativo para Capa 0 (e, d, N)
    # En producción se usan primos de 2048 bits
    p = 61
    q = 53
    N = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = pow(e, -1, phi)
    return (e, N), (d, N)

class ChaumianMint:
    def __init__(self):
        # Claves del emisor
        self.public_key, self._private_key = generate_simple_keys()
        self.spent_nullifiers = set()

    def blind_sign(self, blinded_message: int) -> int:
        """Paso 3: El servidor firma el sobre sin ver el contenido."""
        d, N = self._private_key
        return pow(blinded_message, d, N)

    def verify_and_spend(self, serial_m: int, signature_s: int) -> bool:
        """Paso 5: Validación matemática y prevención de doble gasto."""
        e, N = self.public_key
        # Verificar firma: s^e mod N == m mod N
        if pow(signature_s, e, N) != (serial_m % N):
            return False
        
        # Comprobar si ya fue gastado
        nullifier = hashlib.sha256(str(serial_m).encode("utf-8")).hexdigest()
        if nullifier in self.spent_nullifiers:
            return False
        
        self.spent_nullifiers.add(nullifier)
        return True

class ChaumianClient:
    def __init__(self, public_key):
        self.e, self.N = public_key

    def create_blinded_token(self):
        """Paso 2: Generar billete y factor de cegado r."""
        # Generar número de serie del token
        self.m = secrets.randbelow(self.N - 2) + 2
        # Generar factor de cegado coprimo con N
        while True:
            self.r = secrets.randbelow(self.N - 2) + 2
            if math_gcd(self.r, self.N) == 1:
                break
        
        # m' = (m * r^e) mod N
        blinded_m = (self.m * pow(self.r, self.e, self.N)) % self.N
        return blinded_m

    def unblind_signature(self, blind_sig: int):
        """Paso 4: Extraer la firma limpia eliminando el factor r."""
        r_inv = pow(self.r, -1, self.N)
        # s = (s' * r^-1) mod N
        self.s = (blind_sig * r_inv) % self.N
        return self.m, self.s

def math_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    mint = ChaumianMint()
    client = ChaumianClient(mint.public_key)

    print("🔐 [TEST CHAUM 1982]: Iniciando ciclo de privacidad absoluta...")
    
    # 1. El cliente ciega su token
    m_prime = client.create_blinded_token()
    print(f"1. Token cegado enviado al servidor: {m_prime}")

    # 2. El servidor firma el token a ciegas tras recibir 0.01 AKT
    s_prime = mint.blind_sign(m_prime)
    print(f"2. Firma ciega emitida por el servidor: {s_prime}")

    # 3. El cliente descega y obtiene su billete anónimo (m, s)
    serial, sig = client.unblind_signature(s_prime)
    print(f"3. Billete final listo para usar: Serie={serial} | Firma={sig}")

    # 4. Redención anónima en la API
    valido = mint.verify_and_spend(serial, sig)
    print(f"4. Primera llamada a la API con el billete: {'✅ AUTORIZADA' if valido else '❌ DENEGADA'}")

    # 5. Intento de reutilización (Doble gasto)
    reintento = mint.verify_and_spend(serial, sig)
    print(f"5. Intento de reutilizar el mismo billete: {'❌ BLOQUEADO (Doble gasto)' if not reintento else 'ERROR'}")
