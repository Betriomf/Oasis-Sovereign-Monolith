#!/usr/bin/env python3
import os
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"

import numpy as np
import time

def run_tg_dns(N, Re=1600.0, T_max=10.0, dt=0.01):
    nu = 1.0 / Re
    x = np.linspace(0, 2 * np.pi, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

    # Condición inicial Taylor-Green 3D
    u = np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)

    k1d = np.fft.fftfreq(N, d=1.0 / N)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing='ij')
    k2 = kx**2 + ky**2 + kz**2
    kmag = np.sqrt(k2)
    k2_safe = np.where(k2 == 0, 1.0, k2)

    # Filtro de dealiasing 2/3 de Orszag
    k_cut = N // 3
    dealias = (np.abs(kx) < k_cut) & (np.abs(ky) < k_cut) & (np.abs(kz) < k_cut)

    # Capas diádicas de Littlewood-Paley
    max_j = int(np.ceil(np.log2(max(N // 2, 2)))) + 1
    shells = [(kmag >= (2**(j-1) if j > 0 else 0.0)) & (kmag < 2**j) for j in range(max_j)]

    def get_spectrum_and_enstrophy(uh, vh, wh):
        # Vorticidad en Fourier
        oxh = 1j * (ky * wh - kz * vh)
        oyh = 1j * (kz * uh - kx * wh)
        ozh = 1j * (kx * vh - ky * uh)
        enstrophy = np.sum(np.abs(oxh)**2 + np.abs(oyh)**2 + np.abs(ozh)**2) / (N**6)

        e_k = np.abs(uh)**2 + np.abs(vh)**2 + np.abs(wh)**2
        p = np.array([np.sum(e_k[s]) for s in shells], dtype=np.float64)
        s_tot = np.sum(p)
        p = p / s_tot if s_tot > 0 else np.ones_like(p) / len(p)
        return p, enstrophy

    uh, vh, wh = np.fft.fftn(u), np.fft.fftn(v), np.fft.fftn(w)
    p_prev, omega_0 = get_spectrum_and_enstrophy(uh, vh, wh)
    omega_max_norm = 1.0
    L_fr = 0.0

    steps = int(T_max / dt)
    for step in range(1, steps + 1):
        # Paso Euler/RK2 simplificado con proyección de Leray
        u_r = np.fft.ifftn(uh).real
        v_r = np.fft.ifftn(vh).real
        w_r = np.fft.ifftn(wh).real

        ox = np.fft.ifftn(1j * (ky * wh - kz * vh)).real
        oy = np.fft.ifftn(1j * (kz * uh - kx * wh)).real
        oz = np.fft.ifftn(1j * (kx * vh - ky * uh)).real

        # Término rotacional u x omega
        cx = np.fft.fftn(v_r * oz - w_r * oy) * dealias
        cy = np.fft.fftn(w_r * ox - u_r * oz) * dealias
        cz = np.fft.fftn(u_r * oy - v_r * ox) * dealias

        # Proyección de Leray libre de divergencia
        k_dot_c = kx * cx + ky * cy + kz * cz
        cx -= kx * k_dot_c / k2_safe
        cy -= ky * k_dot_c / k2_safe
        cz -= kz * k_dot_c / k2_safe

        visc = np.exp(-nu * k2 * dt)
        uh = (uh + dt * cx) * visc
        vh = (vh + dt * cy) * visc
        wh = (wh + dt * cz) * visc

        if step % 10 == 0:
            p_curr, omega_t = get_spectrum_and_enstrophy(uh, vh, wh)
            omega_max_norm = max(omega_max_norm, omega_t / omega_0)
            inner = np.clip(np.sum(np.sqrt(p_prev * p_curr)), -1.0, 1.0)
            L_fr += 2.0 * np.arccos(inner)
            p_prev = p_curr

    # Tasa efectiva de decaimiento espectral logarítmico
    active = p_prev[p_prev > 1e-12]
    kappa_eff = float(-np.mean(np.diff(np.log(active)))) if len(active) > 1 else 2.30
    return L_fr, omega_max_norm, abs(kappa_eff)

print("❄️  [DNS FISHER-RAO]: Ejecutando Taylor-Green 3D (Re=1600, 2 hilos)...")
rows = []
for N in [32, 48, 64]:
    t0 = time.time()
    l_fr, om_max, kap = run_tg_dns(N, Re=1600.0, T_max=10.0, dt=0.01)
    dt_run = time.time() - t0
    print(f"  • N={N:<3} | L_FR(T=10)={l_fr:.3f} | Omega_max={om_max:.3f} | kappa_eff={kap:.3f} ({dt_run:.1f}s)")
    rows.append(f"${N}$  & ${l_fr:.3f}$ & ${om_max:.3f}$ & ${kap:.3f}$ \\\\")

# Inyectar resultados reales en papers/paper_b_millennium_regularity.tex
tex_path = "papers/paper_b_millennium_regularity.tex"
with open(tex_path, "r", encoding="utf-8") as f:
    tex = f.read()

new_table = """% DNS_TABLE_START
\\begin{center}
\\begin{tabular}{cccc}
\\toprule
$N$ & $\\mathcal{L}_{FR}(T=10)$ & $\\widetilde{\\Omega}_{\\max}$ & $\\kappa_{\\mathrm{eff}}$ \\\\
\\midrule
""" + "\n".join(rows) + """
\\bottomrule
\\end{tabular}
\\end{center}
% DNS_TABLE_END"""

import re
tex_updated = re.sub(r'% DNS_TABLE_START[\s\S]*?% DNS_TABLE_END', lambda _: new_table, tex)
with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_updated)

print("✅ Tabla DNS real inyectada en papers/paper_b_millennium_regularity.tex")
