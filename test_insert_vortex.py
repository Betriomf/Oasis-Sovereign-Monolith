import math
import psycopg2

DB_URI = "postgresql://postgres:JWbuYNu8l51E6TIC@db.opzddoqcvsqzdhulacei.supabase.co:5432/postgres"

# Cálculo analítico del vórtice (kappa = ln 10)
kappa = math.log(10)
x, y, z, t = 1.0, 0.5, 2.0, 0.1
r = math.sqrt(x*x + y*y) + 1e-6
decay = math.exp(-0.1 * t)
enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))

u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
u_z = round( math.cos(kappa * r) * decay, 4)

vector_sql = f"[{u_x},{u_y},{u_z}]"

try:
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO game_fluid_states (session_id, helicity, enstrophy_bound, state_vector)
        VALUES (%s, %s, %s, %s)
        RETURNING id, session_id, state_vector;
    """, ("partida_madrid_001", 1.0, round(enstrophy_limit, 4), vector_sql))
    
    fila = cur.fetchone()
    conn.commit()
    print("🚀 Vórtice guardado en la base de datos:")
    print(f"ID: {fila[0]} | Sesión: {fila[1]} | Vector: {fila[2]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error al guardar en base de datos: {e}")
