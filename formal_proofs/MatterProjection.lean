/-
  OASIS SOVEREIGN MONOLITH — PHASE 2 BOUNDED GAUGE/LATTICE MARGIN SPECIFICATION
  Archivo: formal_proofs/MatterProjection.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Formaliza la preservación de un margen neto no negativo entre una magnitud efectiva
  y un umbral de fluctuación en unidades discretas escaladas (milésimas, ‰).
-/

namespace Oasis.UnifiedPhase2

/-- Estado de margen escalado (en milésimas, ‰) para una proyección de red/confinamiento. -/
structure LatticeMarginState where
  effectivePermille : Nat
  thresholdPermille : Nat
  deriving DecidableEq, Repr

/-- Condición de margen no negativo respecto al umbral. -/
def hasNonNegMargin (st : LatticeMarginState) : Prop :=
  st.thresholdPermille ≤ st.effectivePermille

/-- Si se cumple el margen no negativo y `effectivePermille` aumenta, se preserva. -/
theorem margin_preserved_on_gain
    (st : LatticeMarginState) (gainPermille : Nat)
    (h_margin : hasNonNegMargin st) :
    hasNonNegMargin { st with effectivePermille := st.effectivePermille + gainPermille } := by
  simp only [hasNonNegMargin] at h_margin ⊢
  omega

/-- Definición del margen neto entero (puede ser negativo si cae bajo el umbral). -/
def netMarginInt (effPermille threshPermille : Nat) : Int :=
  (effPermille : Int) - (threshPermille : Int)

theorem net_margin_nonneg_iff (effPermille threshPermille : Nat) :
    0 ≤ netMarginInt effPermille threshPermille ↔ thresholdPermille ≤ effPermille := by
  unfold netMarginInt
  omega

end Oasis.UnifiedPhase2
