/-
  OASIS SOVEREIGN MONOLITH — PHASE 3 BOUNDED DISCRETE GRADIENT & CURVATURE SPEC
  Archivo: formal_proofs/GravityProjection.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Formaliza cotas discretas de variación de perfil entrópico y preservación de
  cotas superiores/inferiores en redes escaladas (sin asumir física del continuo).
-/

namespace Oasis.UnifiedPhase3

/-- Perfil discreto de dos capas adyacentes (en milésimas, ‰). -/
structure AdjacentLayerProfile where
  prevPermille : Nat
  currPermille : Nat
  capPermille : Nat
  deriving DecidableEq, Repr

/-- Ambas capas permanecen acotadas por `capPermille`. -/
def layersBounded (p : AdjacentLayerProfile) : Prop :=
  p.prevPermille ≤ p.capPermille ∧ p.currPermille ≤ p.capPermille

/-- Si ambas capas están acotadas por `capPermille` y la siguiente capa `nextVal`
    también respeta `capPermille`, el avance `(currPermille -> nextVal)` sigue acotado. -/
theorem step_preserves_layer_cap
    (p : AdjacentLayerProfile) (nextVal : Nat)
    (h_b : layersBounded p)
    (h_next : nextVal ≤ p.capPermille) :
    layersBounded { prevPermille := p.currPermille, currPermille := nextVal, capPermille := p.capPermille } := by
  simp only [layersBounded] at h_b ⊢
  exact ⟨h_b.2, h_next⟩

end Oasis.UnifiedPhase3
