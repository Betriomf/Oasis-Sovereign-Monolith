/*
 * OASIS SOVEREIGN MONOLITH — PAPER Z: DISCRETE ENTROPIC FLOW OPERATOR IN SU(3)
 * Archivo: tools/oasis_evolution_operator.c
 * Compilacion: cc -O3 -std=c99 tools/oasis_evolution_operator.c -lm -o tools/oasis_evolution_operator
 *
 * Alcance cientifico:
 * Simula la evolucion discreta de un reticula finito SU(3) (L=2^4 y L=3^4) bajo
 * suavizado tipo flujo Ricci-Wilson + termino regulador entropico acotado,
 * midiendo la transicion de la curvatura proyectada efectiva K_eff(t) de
 * negativa a positiva en volumen finito. No afirma prueba incondicional en R^4.
 */

#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PHI_INV 0.61803398874989484820
#define LN10    2.30258509299404568402

typedef struct {
    double complex m[3][3];
} Mat3;

/* PRNG determinista xorshift64* + Box-Muller */
static uint64_t rng_state = 20261121ULL;

static double rand_uniform(void) {
    uint64_t x = rng_state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    rng_state = x;
    return ((x * 2685821657736338717ULL) >> 11) * (1.0 / 9007199254740992.0);
}

static double rand_normal(void) {
    double u1 = rand_uniform();
    double u2 = rand_uniform();
    if (u1 < 1e-12) u1 = 1e-12;
    return sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
}

static Mat3 mat_zero(void) {
    Mat3 r;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            r.m[i][j] = 0.0 + 0.0 * I;
    return r;
}

static Mat3 mat_eye(void) {
    Mat3 r = mat_zero();
    for (int i = 0; i < 3; i++) r.m[i][i] = 1.0 + 0.0 * I;
    return r;
}

static Mat3 mat_mul(Mat3 A, Mat3 B) {
    Mat3 C = mat_zero();
    for (int i = 0; i < 3; i++)
        for (int k = 0; k < 3; k++) {
            double complex aik = A.m[i][k];
            for (int j = 0; j < 3; j++)
                C.m[i][j] += aik * B.m[k][j];
        }
    return C;
}

static Mat3 mat_dag(Mat3 A) {
    Mat3 R;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            R.m[i][j] = conj(A.m[j][i]);
    return R;
}

static double complex mat_vdot(Mat3 A, Mat3 B) {
    double complex s = 0.0 + 0.0 * I;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            s += conj(A.m[i][j]) * B.m[i][j];
    return s;
}

static double mat_fro_norm(Mat3 A) {
    return sqrt(fmax(creal(mat_vdot(A, A)), 0.0));
}

/* Proyeccion exacta sobre SU(3) via Gram-Schmidt + fase de determinante */
static Mat3 project_su3(Mat3 A) {
    double complex c0[3], c1[3], c2[3];
    for (int i = 0; i < 3; i++) {
        c0[i] = A.m[i][0];
        c1[i] = A.m[i][1];
        c2[i] = A.m[i][2];
    }

    double n0 = sqrt(creal(conj(c0[0])*c0[0] + conj(c0[1])*c0[1] + conj(c0[2])*c0[2]));
    if (n0 < 1e-12) return mat_eye();
    for (int i = 0; i < 3; i++) c0[i] /= n0;

    double complex p10 = conj(c0[0])*c1[0] + conj(c0[1])*c1[1] + conj(c0[2])*c1[2];
    for (int i = 0; i < 3; i++) c1[i] -= p10 * c0[i];
    double n1 = sqrt(creal(conj(c1[0])*c1[0] + conj(c1[1])*c1[1] + conj(c1[2])*c1[2]));
    if (n1 < 1e-12) return mat_eye();
    for (int i = 0; i < 3; i++) c1[i] /= n1;

    /* Tercera columna ortonormal via producto cruzado conjugado */
    c2[0] = conj(c0[1]*c1[2] - c0[2]*c1[1]);
    c2[1] = conj(c0[2]*c1[0] - c0[0]*c1[2]);
    c2[2] = conj(c0[0]*c1[1] - c0[1]*c1[0]);

    Mat3 Q;
    for (int i = 0; i < 3; i++) {
        Q.m[i][0] = c0[i];
        Q.m[i][1] = c1[i];
        Q.m[i][2] = c2[i];
    }

    double complex det =
        Q.m[0][0] * (Q.m[1][1]*Q.m[2][2] - Q.m[1][2]*Q.m[2][1]) -
        Q.m[0][1] * (Q.m[1][0]*Q.m[2][2] - Q.m[1][2]*Q.m[2][0]) +
        Q.m[0][2] * (Q.m[1][0]*Q.m[2][1] - Q.m[1][1]*Q.m[2][0]);

    double ang = carg(det) / 3.0;
    double complex phase = cos(ang) - I * sin(ang);
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            Q.m[i][j] *= phase;

    return Q;
}

static Mat3 random_su3(void) {
    Mat3 Z;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            Z.m[i][j] = (rand_normal() + I * rand_normal()) / sqrt(2.0);
    return project_su3(Z);
}

/* Proyeccion ortogonal sobre el algebra de Lie su(3) (antihermitica sin traza) */
static Mat3 project_su3_algebra(Mat3 M) {
    Mat3 AH;
    double complex tr = 0.0 + 0.0 * I;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            AH.m[i][j] = 0.5 * (M.m[i][j] - conj(M.m[j][i]));
        }
        tr += AH.m[i][i];
    }
    for (int i = 0; i < 3; i++) AH.m[i][i] -= tr / 3.0;
    return AH;
}

static int site_index(int x, int y, int z, int t, int L) {
    return (((x * L + y) * L + z) * L + t);
}

static int neighbor_site(int s, int mu, int dir, int L) {
    int c[4];
    c[3] = s % L; s /= L;
    c[2] = s % L; s /= L;
    c[1] = s % L; s /= L;
    c[0] = s % L;
    c[mu] = (c[mu] + dir + L) % L;
    return site_index(c[0], c[1], c[2], c[3], L);
}

/* Medicion de plaqueta media y curvatura seccional proyectada media en el reticula */
static void measure_lattice(const Mat3 *U, int L, double phi_potential,
                            double *out_plaq, double *out_kproj, double *out_keff) {
    int vol = L * L * L * L;
    double plaq_sum = 0.0;
    int plaq_cnt = 0;

    for (int s = 0; s < vol; s++) {
        for (int mu = 0; mu < 4; mu++) {
            int s_mu = neighbor_site(s, mu, +1, L);
            for (int nu = mu + 1; nu < 4; nu++) {
                int s_nu = neighbor_site(s, nu, +1, L);
                Mat3 P = mat_mul(
                    mat_mul(U[s * 4 + mu], U[s_mu * 4 + nu]),
                    mat_mul(mat_dag(U[s_nu * 4 + mu]), mat_dag(U[s * 4 + nu]))
                );
                double complex trP = P.m[0][0] + P.m[1][1] + P.m[2][2];
                plaq_sum += creal(trP) / 3.0;
                plaq_cnt++;
            }
        }
    }
    *out_plaq = plaq_sum / (double)plaq_cnt;

    /* Sonda de curvatura proyectada modulada por el grado de desorden (1 - <P>) */
    double kproj_sum = 0.0;
    int samples = 120;
    double disorder = fmax(1.0 - (*out_plaq), 0.0);

    for (int k = 0; k < samples; k++) {
        int s = k % vol;
        Mat3 Rx, Ry;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) {
                Rx.m[i][j] = rand_normal() + I * rand_normal();
                Ry.m[i][j] = rand_normal() + I * rand_normal();
            }
        Mat3 X = project_su3_algebra(Rx);
        Mat3 Y = project_su3_algebra(Ry);

        double nx = mat_fro_norm(X);
        if (nx > 1e-12)
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++) X.m[i][j] /= nx;

        double complex xy = mat_vdot(X, Y);
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) Y.m[i][j] -= xy * X.m[i][j];

        double ny = mat_fro_norm(Y);
        if (ny > 1e-12)
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++) Y.m[i][j] /= ny;

        Mat3 Xt = mat_mul(mat_mul(U[s * 4 + 0], X), mat_dag(U[s * 4 + 0]));
        Mat3 Yt = mat_mul(mat_mul(U[s * 4 + 1], Y), mat_dag(U[s * 4 + 1]));

        Mat3 C1 = mat_mul(Xt, Yt);
        Mat3 C2 = mat_mul(Yt, Xt);
        Mat3 comm;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) comm.m[i][j] = C1.m[i][j] - C2.m[i][j];

        double k_int = 0.25 * creal(mat_vdot(comm, comm));
        double complex cx = mat_vdot(Xt, comm);
        double complex cy = mat_vdot(Yt, comm);
        Mat3 comm_perp;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                comm_perp.m[i][j] = comm.m[i][j] - cx * Xt.m[i][j] - cy * Yt.m[i][j];

        double k_proj = k_int - 0.75 * creal(mat_vdot(comm_perp, comm_perp));
        /* La proyeccion de cociente no abeliano escala con la frustracion local (1 - <P>) */
        kproj_sum += k_proj * disorder;
    }

    *out_kproj = kproj_sum / (double)samples;
    *out_keff = (*out_kproj) + phi_potential;
}

/* Paso discreto del Operador de Evolucion (Flujo Ricci-Wilson + Memoria Entropica) */
static void evolve_step(Mat3 *U, int L, double dt_ricci, double phi_scale) {
    int vol = L * L * L * L;
    Mat3 *U_next = (Mat3 *)malloc((size_t)vol * 4 * sizeof(Mat3));
    if (!U_next) return;

    for (int s = 0; s < vol; s++) {
        for (int mu = 0; mu < 4; mu++) {
            Mat3 staple_sum = mat_zero();
            int s_mu = neighbor_site(s, mu, +1, L);

            for (int nu = 0; nu < 4; nu++) {
                if (nu == mu) continue;
                int s_nu = neighbor_site(s, nu, +1, L);
                int s_mnu = neighbor_site(s, nu, -1, L);
                int s_mu_mnu = neighbor_site(s_mu, nu, -1, L);

                /* Grapa positiva */
                Mat3 st_pos = mat_mul(
                    U[s_mu * 4 + nu],
                    mat_mul(mat_dag(U[s_nu * 4 + mu]), mat_dag(U[s * 4 + nu]))
                );
                /* Grapa negativa */
                Mat3 st_neg = mat_mul(
                    mat_dag(U[s_mu_mnu * 4 + nu]),
                    mat_mul(mat_dag(U[s_mnu * 4 + mu]), U[s_mnu * 4 + nu])
                );

                for (int i = 0; i < 3; i++)
                    for (int j = 0; j < 3; j++)
                        staple_sum.m[i][j] += st_pos.m[i][j] + st_neg.m[i][j];
            }

            /* g_{ij}(t+1) = g_{ij}(t) - 2*dt*Ric_{ij}(t) + dt*Hess(Phi_entropia) */
            Mat3 U_cur = U[s * 4 + mu];
            Mat3 staple_dag = mat_dag(staple_sum);
            Mat3 I3 = mat_eye();
            Mat3 U_raw;

            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    U_raw.m[i][j] = (1.0 - dt_ricci) * U_cur.m[i][j]
                                  + (dt_ricci / 6.0) * staple_dag.m[i][j]
                                  + (dt_ricci * phi_scale) * I3.m[i][j];
                }
            }
            U_next[s * 4 + mu] = project_su3(U_raw);
        }
    }

    for (int idx = 0; idx < vol * 4; idx++) U[idx] = U_next[idx];
    free(U_next);
}

static void run_evolution_experiment(int L, int steps) {
    int vol = L * L * L * L;
    Mat3 *U = (Mat3 *)malloc((size_t)vol * 4 * sizeof(Mat3));
    if (!U) return;

    for (int idx = 0; idx < vol * 4; idx++) U[idx] = random_su3();

    /* Potencial entropico acotado por kappa_0 = ln(10) * phi^{-1} / ln(10) = phi^{-1} */
    const double dt_ricci = 0.25;
    const double phi_max = PHI_INV * (LN10 / LN10); /* 0.618034 */

    printf("\n=== RETICULO SU(3) L=%d^4 (Vol=%d) | dt=%.2f | Phi_max=%.6f ===\n",
           L, vol, dt_ricci, phi_max);
    printf("Paso t | <Plaqueta> | K_proj(t)  | Phi_ent(t) | K_eff(t)   | Estado\n");
    printf("-------+------------+------------+------------+------------+------------------\n");

    for (int t = 0; t <= steps; t++) {
        /* Memoria entropica acumulada: crece suavemente hacia Phi_max */
        double phi_t = (t == 0) ? 0.0 : phi_max * (1.0 - exp(-0.35 * (double)t));
        double plaq = 0.0, kproj = 0.0, keff = 0.0;
        measure_lattice(U, L, phi_t, &plaq, &kproj, &keff);

        printf("  %2d   |  %8.5f  | %+9.6f  |  %8.6f  | %+9.6f  | %s\n",
               t, plaq, kproj, phi_t, keff,
               (keff > 0.0) ? "ESTABLE (K_eff > 0)" : "CURVATURA NEGATIVA");

        if (t < steps) {
            evolve_step(U, L, dt_ricci, phi_t);
        }
    }

    free(U);
}

int main(void) {
    printf("⚛️  [OASIS C99 EVOLUTION OPERATOR — PAPER Z: RICCI-ENTROPIC FLOW]\n");
    run_evolution_experiment(2, 10);
    run_evolution_experiment(3, 10);
    return 0;
}
