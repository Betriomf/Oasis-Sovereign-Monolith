/-
  OASIS SOVEREIGN MONOLITH — SUB-FASE 5: SÍNTESIS DE COTAS DE SUB-FASES 1 A 4
  Archivo: formal_proofs/Subphase5_Global_Synthesis_Spec.lean
  Compilación estricta en Lean 4.36.0 puro: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Nota de alcance: Reúne en un certificado de cotas las condiciones verificables de las
  Sub-fases 1 a 4 bajo hipótesis explícitas. No afirma una prueba analítica incondicional
  de existencia o brecha de masa en ℝ⁴ ni resuelve compacidad en dimensión infinita.
-/

namespace Oasis.YangMills.Subphase5GlobalSynthesis

def freeGaussianCumulantMillionths : Nat := 0

/-- Certificado conjunto de cotas escaladas para las Sub-fases 2, 3 y 4 en el paso `step`. -/
structure SubphasesSynthesisCertificate where
  step : Nat
  roughnessPermille : Nat
  momentPermille : Nat
  tailPermille : Nat
  spectralGapPermille : Nat
  connectedCumulantMillionths : Nat

/-- Hipótesis explícitas uniformes para el certificado de síntesis en el paso `step`. -/
structure SynthesisAssumptions
    (cert : SubphasesSynthesisCertificate)
    (roughnessCap momentCap tailCap : Nat) where
  h_roughness : cert.roughnessPermille ≤ roughnessCap
  h_moment : cert.momentPermille ≤ momentCap
  h_tail : cert.tailPermille ≤ tailCap
  h_gap_floor : 1 ≤ cert.spectralGapPermille
  h_nontrivial_floor : 1 ≤ cert.connectedCumulantMillionths

/-- Teorema de síntesis: bajo hipótesis explícitas, se conservan simultáneamente
    las cotas de suavizado, momento y cola, junto con brecha positiva y separación
    frente al caso gaussiano libre (`0`). -/
theorem subphases_synthesis_preserves_bounds
    (cert : SubphasesSynthesisCertificate)
    (roughnessCap momentCap tailCap : Nat)
    (assump : SynthesisAssumptions cert roughnessCap momentCap tailCap) :
    cert.roughnessPermille ≤ roughnessCap ∧
    cert.momentPermille ≤ momentCap ∧
    cert.tailPermille ≤ tailCap ∧
    0 < cert.spectralGapPermille ∧
    freeGaussianCumulantMillionths < cert.connectedCumulantMillionths := by
  exact ⟨
    assump.h_roughness,
    assump.h_moment,
    assump.h_tail,
    Nat.lt_of_lt_of_le (by decide) assump.h_gap_floor,
    Nat.lt_of_lt_of_le (by decide) assump.h_nontrivial_floor
  ⟩

end Oasis.YangMills.Subphase5GlobalSynthesis
