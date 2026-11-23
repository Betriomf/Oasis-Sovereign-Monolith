/-
  OASIS SOVEREIGN MONOLITH — BOUNDED MULTI-PROJECTION STABILITY SPEC
  Archivo: formal_proofs/UnifiedTheory_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.UnifiedSynthesis

/-- Proyecciones discretas escaladas (en unidades de 10^-3 nats):
    gauge/retículo, gradiente de red y métrica espectral. -/
structure BoundedProjections where
  gaugeMetric : Nat
  latticeMetric : Nat
  spectralMetric : Nat
  deriving DecidableEq, Repr

/-- Si cada proyección está acotada por `bound`, el máximo conjunto no supera `bound`. -/
theorem joint_projections_bounded
    (p : BoundedProjections) (bound : Nat)
    (h_gauge : p.gaugeMetric ≤ bound)
    (h_lat : p.latticeMetric ≤ bound)
    (h_spec : p.spectralMetric ≤ bound) :
    Nat.max p.gaugeMetric (Nat.max p.latticeMetric p.spectralMetric) ≤ bound := by
  exact Nat.max_le.mpr ⟨h_gauge, Nat.max_le.mpr ⟨h_lat, h_spec⟩⟩

end Oasis.UnifiedSynthesis
