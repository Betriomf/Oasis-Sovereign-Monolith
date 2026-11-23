/-
  OASIS SOVEREIGN MONOLITH — YM UV/IR COMPATIBILITY WINDOW SPECIFICATION
  Archivo: formal_proofs/YM_UV_IR_Window_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Modela explícitamente una ventana de compatibilidad entre cota UV (ruido/fluctuación)
  y cota IR (brecha/margen mínimo) sin asumir el límite continuo incondicional.
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

end Oasis.YangMillsWindow
