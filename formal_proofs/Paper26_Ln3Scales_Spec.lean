/-
  OASIS SOVEREIGN MONOLITH — PAPER 26 LN(3) TERNARY SCALES SPEC
  Archivo: formal_proofs/Paper26_Ln3Scales_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.Paper26Ln3Scales

/-- Orden escalado en milésimas entre ln(2) (693), ln(3) (1099) y ln(10) (2303). -/
theorem permil_ln2_ln3_ln10_chain :
    693 ≤ 1099 ∧ 1099 ≤ 2303 := by
  decide

/-- Conservación de presupuesto de milésimas entre tramo asignado y remanente. -/
theorem permil_split_identity (u : Nat) (hu : u ≤ 1000) :
    u + (1000 - u) = 1000 := by
  omega

/-- No negatividad de residuo para cualquier cuota no negativa. -/
theorem nonneg_remainder (total used : Nat) :
    0 ≤ total - used := by
  omega

end Oasis.Paper26Ln3Scales
