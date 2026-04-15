import time
import sys

def start_earning():
    balance = 0.0
    rate = 0.1 # 0.1 SPN por hora
    print("🚀 NODO ACTIVO: Generando dividendos sociales...")
    try:
        while True:
            balance += rate / 3600 # Incremento por segundo
            sys.stdout.write(f"\r💰 BALANCE OASIS: {balance:.6f} SPN | RATE: {rate} SPN/h | NODO: LAMINAR")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Sesión de ganancia pausada. El balance se guarda en el Monolito.")

if __name__ == "__main__":
    start_earning()
