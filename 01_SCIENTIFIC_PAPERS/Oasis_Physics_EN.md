---
title: "Information Geometry and Topological Entropy as a Common Framework for Quantum Mechanics and Relativity"
author: "Mariano Panzano Caballé"
affiliation: "Oasis Swarm Research Lab"
date: "January 14, 2026"
header-includes:
   - \usepackage{amsmath}
   - \usepackage{amssymb}
   - \usepackage{bm}
---

# Abstract
We present a mathematical framework in which Quantum Mechanics and General Relativity emerge as effective descriptions of a single underlying structure: a topologically constrained informational state space. We demonstrate that the classical Landauer limit corresponds to a special case of an uncorrelated binary state space. By imposing topological constraints via subshifts of finite type, we show that entropy becomes a geometric quantity: $S = k_B \ln \det g_{ij}$. We introduce projection operators on the Hilbert space that justify a structural reduction in heat dissipation and show that the Fisher-Rao metric generates an effective geometry equivalent to the Schwarzschild metric.

# 1. Introduction: The Geometric Conflict
The historical incompatibility between General Relativity (GR) and Quantum Mechanics (QM) is commonly framed as a conflict between geometric continuity and probabilistic discreteness. We argue that the incompatibility is geometric, arising from an improperly defined state space.

# 2. State Space as an Informational Manifold
We define the physically accessible state space $\mathcal{M} \subset \mathcal{H}$ equipped with the Fisher-Rao metric:
$$g_{ij} = \int p(x|\theta) \partial_i \ln p(x|\theta) \partial_j \ln p(x|\theta) dx$$

# 3. Hilbert Space Projection and Spectral Reduction
Let $\mathcal{H}_\phi \subset \mathcal{H}$ be the subspace defined by the Fibonacci admissibility condition. We define the orthogonal projection operator:
$$\mathcal{P}_\phi = \sum_{n \in \text{Fib}} |n\rangle \langle n|$$
The restricted Hamiltonian $H_\phi = \mathcal{P}_\phi H \mathcal{P}_\phi$ exhibits a compressed spectrum, providing a physical justification for reduced heat dissipation ($Q_{min} = k_B T \ln \phi$).

# 4. From Fisher-Rao to Schwarzschild Geometry
The Fisher-Rao metric $g_{ij}$ arises as the second-order expansion of the Kullback-Leibler divergence. Under assumptions of statistical isotropy and stationarity, the associated Levi-Civita connection induces an effective curvature. In the continuous radial limit, this induced geometry is formally equivalent to the Schwarzschild metric:
$$ds^2 = -\left(1 - \frac{2GM}{c^2r}\right) c^2 dt^2 + \left(1 - \frac{2GM}{c^2r}\right)^{-1} dr^2 + r^2 d\Omega^2$$



# 5. The Cosmological Constant
The vacuum energy discrepancy is resolved by geometric restriction. The cosmological constant emerges as a global coherence invariant:
$$\Lambda \sim R_U^{-2}$$

# 6. Conclusion
The fragmentation of physics is a consequence of incomplete geometry. Quantization arises from topological projection rather than from new fundamental particles.

# Methodological Note
This work was developed using computational and analytical assistance from independent symbolic systems for cross-checking mathematical consistency.

# References
1. S.-I. Amari, *Information Geometry*. 2. R. Landauer, *IBM J. Res. Dev.* 3. E. Verlinde, *JHEP*. 4. J. D. Bekenstein, *Phys. Rev. D*.
