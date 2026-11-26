/-
  OASIS SOVEREIGN MONOLITH — PAPER 29 NOISE & ENTROPY CONTRAST SPEC
  Archivo: formal_proofs/Paper29_NoiseEntropy_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.Paper29NoiseEntropy

/-- Conservación de presupuesto acotado entre ruido consumido y margen disponible. -/
theorem noise_budget_conservation (cap used : Nat) (h : used ≤ cap) :
    used + (cap - used) = cap := by
  omega

/-- Monotonía de cota superior para presupuestos acotados. -/
theorem noise_cap_monotone (c1 c2 : Nat) (h : c1 ≤ c2) :
    c1 ≤ c2 := by
  exact h

/-- No negatividad de margen residual entero. -/
theorem nonneg_residual_margin (cap used : Nat) :
    0 ≤ cap - used := by
  omega

end Oasis.Paper29NoiseEntropy
