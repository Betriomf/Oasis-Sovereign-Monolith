/-
  OASIS SOVEREIGN MONOLITH — YM UV/IR COMPATIBILITY WINDOW SPECIFICATION
  Archivo: formal_proofs/YM_UV_IR_Window_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.YangMillsWindow

/-- Parámetros escalados (en milésimas, ‰) de una ventana de control UV/IR. -/
structure UVIRWindow where
  uvFluctuationPermille : Nat
  irGapMarginPermille : Nat
  deriving DecidableEq, Repr

/-- Condición de ventana válida: la fluctuación UV no supera el margen IR disponible. -/
def isCompatible (w : UVIRWindow) : Prop :=
  w.uvFluctuationPermille ≤ w.irGapMarginPermille

/-- Si una ventana es compatible y el margen IR se incrementa,
    la compatibilidad se preserva. -/
theorem compatible_monotone_ir
    (w : UVIRWindow) (deltaIR : Nat)
    (h_compat : isCompatible w) :
    isCompatible { w with irGapMarginPermille := w.irGapMarginPermille + deltaIR } := by
  simp only [isCompatible] at h_compat ⊢
  omega

/-- Si una ventana es compatible y la fluctuación UV se reduce o mantiene por debajo de `uvNew`,
    la compatibilidad se preserva. -/
theorem compatible_monotone_uv
    (w : UVIRWindow) (uvNew : Nat)
    (h_compat : isCompatible w)
    (h_le : uvNew ≤ w.uvFluctuationPermille) :
    isCompatible { w with uvFluctuationPermille := uvNew } := by
  simp only [isCompatible] at h_compat ⊢
  omega

/-- Encadenamiento de dos ventanas sucesivas: si `w₁` es compatible y `w₂` mejora
    simultáneamente (menor o igual fluctuación UV y mayor o igual margen IR), `w₂` es compatible. -/
theorem compatible_chain_step
    (w₁ w₂ : UVIRWindow)
    (h_compat₁ : isCompatible w₁)
    (h_uv_step : w₂.uvFluctuationPermille ≤ w₁.uvFluctuationPermille)
    (h_ir_step : w₁.irGapMarginPermille ≤ w₂.irGapMarginPermille) :
    isCompatible w₂ := by
  simp only [isCompatible] at h_compat₁ ⊢
  omega

end Oasis.YangMillsWindow
