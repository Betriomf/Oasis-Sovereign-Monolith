/-
  OASIS SOVEREIGN MONOLITH — PHASE 5 COMPOSITE BOUNDED PROJECTION THEOREM
  Archivo: formal_proofs/UnifiedTheory_Master.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Combina tres métricas escaladas acotadas (retículo, capa entrópica y espectral)
  frente a una cota superior común `capPermille`.
-/

namespace Oasis.UnifiedPhase5

/-- Triplete de métricas discretas escaladas (en milésimas de unidad). -/
structure CompositeMetrics where
  latticePermille : Nat
  layerPermille : Nat
  spectralPermille : Nat
  deriving DecidableEq, Repr

/-- Todas las métricas del triplete respetan la cota superior `capPermille`. -/
def allBounded (m : CompositeMetrics) (capPermille : Nat) : Prop :=
  m.latticePermille ≤ capPermille ∧
  m.layerPermille ≤ capPermille ∧
  m.spectralPermille ≤ capPermille

/-- El máximo conjunto de las tres métricas no supera `capPermille` cuando todas están acotadas. -/
theorem master_max_bounded
    (m : CompositeMetrics) (capPermille : Nat)
    (h_all : allBounded m capPermille) :
    Nat.max m.latticePermille (Nat.max m.layerPermille m.spectralPermille) ≤ capPermille := by
  simp only [allBounded] at h_all
  exact Nat.max_le.mpr ⟨h_all.1, Nat.max_le.mpr ⟨h_all.2.1, h_all.2.2⟩⟩

end Oasis.UnifiedPhase5
