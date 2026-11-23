/-
  OASIS SOVEREIGN MONOLITH — DISCRETE ENTROPIC GRAVITY BOUND SPECIFICATION
  Archivo: formal_proofs/EntropicGravity_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.EntropicGravity

/-- Variación no negativa de entropía entre capas discretas (en unidades escaladas). -/
def discreteEntropyGradient (s_curr s_next : Nat) : Nat :=
  s_next - s_curr

/-- Si la entropía entre capas es no decreciente y su incremento está acotado por `gradCap`,
    entonces `s_curr ≤ s_next` y el gradiente discreto no supera `gradCap`. -/
theorem entropy_gradient_bounded
    (s_curr s_next gradCap : Nat)
    (h_nondec : s_curr ≤ s_next)
    (h_cap : s_next - s_curr ≤ gradCap) :
    s_curr ≤ s_next ∧ discreteEntropyGradient s_curr s_next ≤ gradCap := by
  unfold discreteEntropyGradient
  exact ⟨h_nondec, h_cap⟩

end Oasis.EntropicGravity
