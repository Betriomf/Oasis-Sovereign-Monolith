import math
from supabase import create_client

SUPABASE_URL = "https://opzddoqcvsqzdhulacei.supabase.co"
SUPABASE_KEY = "sb_publishable_oTCm3P5c_cpuRT3hN5TfBQ_G8w_C8vn"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

kappa = math.log(10)
x, y, z, t = 1.0, 0.5, 2.0, 0.1
r = math.sqrt(x*x + y*y) + 1e-6
decay = math.exp(-0.1 * t)
enstrophy_limit = min(kappa**2, 1.0 / (r * decay + 0.1))

u_x = round(-y / r * math.sin(kappa * z) * enstrophy_limit, 4)
u_y = round( x / r * math.sin(kappa * z) * enstrophy_limit, 4)
u_z = round( math.cos(kappa * r) * decay, 4)

data = {
    "session_id": "partida_madrid_002",
    "helicity": 1.0,
    "enstrophy_bound": round(enstrophy_limit, 4),
    "state_vector": [u_x, u_y, u_z]
}

res = supabase.table("game_fluid_states").insert(data).execute()
print("🚀 Vórtice guardado vía HTTPS:", res.data)
