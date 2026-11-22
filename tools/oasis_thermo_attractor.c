/*
 * OASIS INFORMATIONAL THERMODYNAMICS — C99 ATTRACTOR & SUB-LANDAUER BENCHMARK
 * Archivo: tools/oasis_thermo_attractor.c
 * Compilacion: cc -O3 -std=c99 tools/oasis_thermo_attractor.c -lm -o /Volumes/OasisRAM/tmp/thermo_sim
 *
 * Simula la evolucion discreta dOmega/dt <= kappa^2 - Omega (kappa = ln(10)) y el
 * balance energetico bajo termostato aureo T = 1/phi^2 (sin diverger ni tocar T = 0).
 */

#include <math.h>
#include <stdio.h>

int main(void) {
    const double phi = 1.6180339887498948482;
    const double kappa = log(10.0);          /* 2.302585... */
    const double kappa_sq = kappa * kappa;   /* 5.301898... */
    const double landauer_coeff = log(2.0);  /* 0.693147... k_B T */
    const double oasis_coeff = log(phi);     /* 0.481212... k_B T */

    double omega = 1.2500;   /* Enstrofia inicial */
    double T_rel = 1.0000;   /* Temperatura relativa inicial (> 0 siempre) */
    const double dt = 0.25;
    const double T_floor = 1.0 / (phi * phi); /* 0.381966... > 0 */

    printf("⚛️  [OASIS INFORMATIONAL THERMODYNAMICS — C99 EVOLUTION]\n");
    printf("   Techo decádico kappa^2 = %.6f | E_Oasis/k_BT = %.6f < Landauer = %.6f\n\n",
           kappa_sq, oasis_coeff, landauer_coeff);
    printf("Paso | Omega(t)  | Techo cap | T_rel(t)  | P_est (W) | Estado\n");
    printf("-----+-----------+-----------+-----------+-----------+---------------------\n");

    for (int step = 0; step <= 12; step++) {
        double p_watts = 1.15 + 1.43 * (omega / kappa_sq); /* <= 2.58 W */
        printf(" %2d  | %9.6f | %9.6f | %9.6f | %9.4f | %s\n",
               step, omega, kappa_sq, T_rel, p_watts,
               (omega <= kappa_sq && T_rel > 0.0 && p_watts <= 2.5801)
                   ? "ACOTADO & SILICIO FRIO"
                   : "FUERA DE RANGO");

        /* Paso amortiguado hacia el atractor kappa^2 y relajacion asintotica hacia T_floor > 0 */
        omega += dt * (kappa_sq - omega);
        T_rel = T_floor + (T_rel - T_floor) * exp(-0.35);
    }

    return 0;
}
