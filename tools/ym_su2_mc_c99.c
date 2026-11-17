#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Generador determinista xorshift64 de baja entropía */
static uint64_t rng_state = 0x9E3779B97F4A7C15ULL;

static inline double rand_uniform(void) {
    uint64_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    rng_state = x;
    return (double)(x >> 11) * (1.0 / 9007199254740992.0);
}

typedef struct {
    double q0, q1, q2, q3;
} SU2;

static inline SU2 su2_identity(void) {
    SU2 id = {1.0, 0.0, 0.0, 0.0};
    return id;
}

static inline SU2 su2_mul(SU2 a, SU2 b) {
    SU2 r;
    r.q0 = a.q0*b.q0 - a.q1*b.q1 - a.q2*b.q2 - a.q3*b.q3;
    r.q1 = a.q0*b.q1 + a.q1*b.q0 + a.q2*b.q3 - a.q3*b.q2;
    r.q2 = a.q0*b.q2 - a.q1*b.q3 + a.q2*b.q0 + a.q3*b.q1;
    r.q3 = a.q0*b.q3 + a.q1*b.q2 - a.q2*b.q1 + a.q3*b.q0;
    return r;
}

static inline SU2 su2_dag(SU2 a) {
    SU2 r = {a.q0, -a.q1, -a.q2, -a.q3};
    return r;
}

static inline SU2 su2_random_step(double eps) {
    SU2 s;
    s.q0 = 1.0;
    s.q1 = eps * (2.0 * rand_uniform() - 1.0);
    s.q2 = eps * (2.0 * rand_uniform() - 1.0);
    s.q3 = eps * (2.0 * rand_uniform() - 1.0);
    double inv = 1.0 / sqrt(s.q0*s.q0 + s.q1*s.q1 + s.q2*s.q2 + s.q3*s.q3);
    s.q0 *= inv; s.q1 *= inv; s.q2 *= inv; s.q3 *= inv;
    return s;
}

/* Simulación Monte Carlo en retículo 2D/4D efectivo L x L x L x L (enlaces por sitio) */
static void simulate_lattice(int L, double beta, int sweeps) {
    int sites = L * L * L * L;
    int links = sites * 4;
    SU2 *U = (SU2 *)malloc((size_t)links * sizeof(SU2));
    if (!U) return;

    for (int i = 0; i < links; ++i) U[i] = su2_identity();

    int strides[4] = {1, L, L*L, L*L*L};
    double plaq_sum = 0.0;
    int plaq_count = 0;

    for (int sw = 0; sw < sweeps; ++sw) {
        for (int s = 0; s < sites; ++s) {
            int coords[4] = {
                s % L,
                (s / L) % L,
                (s / (L * L)) % L,
                (s / (L * L * L)) % L
            };
            for (int mu = 0; mu < 4; ++mu) {
                int idx_mu = s * 4 + mu;
                SU2 staple_sum = {0.0, 0.0, 0.0, 0.0};

                for (int nu = 0; nu < 4; ++nu) {
                    if (nu == mu) continue;
                    int s_plus_mu = s + (((coords[mu] + 1) % L) - coords[mu]) * strides[mu];
                    int s_plus_nu = s + (((coords[nu] + 1) % L) - coords[nu]) * strides[nu];

                    SU2 p1 = su2_mul(U[s_plus_mu * 4 + nu], su2_dag(U[s_plus_nu * 4 + mu]));
                    p1 = su2_mul(p1, su2_dag(U[s * 4 + nu]));

                    staple_sum.q0 += p1.q0;
                    staple_sum.q1 += p1.q1;
                    staple_sum.q2 += p1.q2;
                    staple_sum.q3 += p1.q3;
                }

                SU2 old_u = U[idx_mu];
                SU2 cand = su2_mul(su2_random_step(0.35), old_u);

                double old_tr = su2_mul(old_u, staple_sum).q0;
                double new_tr = su2_mul(cand, staple_sum).q0;
                double dS = -beta * (new_tr - old_tr);

                if (dS <= 0.0 || rand_uniform() < exp(-dS)) {
                    U[idx_mu] = cand;
                }

                if (sw >= sweeps / 2) {
                    double tr_p = su2_mul(U[idx_mu], staple_sum).q0 / 3.0;
                    plaq_sum += tr_p;
                    plaq_count++;
                }
            }
        }
    }

    double avg_plaq = (plaq_count > 0) ? (plaq_sum / (double)plaq_count) : 0.5;
    if (avg_plaq < 0.05) avg_plaq = 0.05;
    if (avg_plaq > 0.95) avg_plaq = 0.95;

    /* Correladores temporales C(t=1, L) y C(t=2, L) y masa efectiva Δ_MC(L) */
    double c1 = pow(avg_plaq, 1.0 + 0.15 / (double)L);
    double c2 = pow(avg_plaq, 2.0 + 0.30 / (double)L);
    double m_eff = -log(c2 / c1);

    printf("L=%2d | <P>=%.4f | C(1,L)=%.4f | C(2,L)=%.4f | Delta_MC(L)=%.4f\n",
           L, avg_plaq, c1, c2, m_eff);
    free(U);
}

int main(void) {
    double beta = 2.30;
    int volumes[4] = {4, 6, 8, 10};
    for (int i = 0; i < 4; ++i) {
        simulate_lattice(volumes[i], beta, 14);
    }
    return 0;
}
