/-
  OASIS SOVEREIGN MONOLITH — PAPER Y CONDITIONAL MARGIN SPEC
  Archivo: formal_proofs/PaperY_Entropy_Curvature_Margin.lean
  Lean 4.36.0 puro: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Alcance: Formaliza de forma condicional que si un margen efectivo acotado
  compensa una pérdida de curvatura en milésimas (10^-3), se obtiene un
  margen neto positivo. No afirma prueba incondicional en ℝ⁴ ni en S'(ℝ⁴).
-/

namespace Oasis.YangMills.PaperY

/-! ### 1. DEFINICIONES -/

structure CurvatureMarginState where
  intrinsicPermille : Nat
  quotientLossPermille : Nat
  entropyMarginPermille : Nat

def netEffectiveMargin (s : CurvatureMarginState) : Int :=
  (s.intrinsicPermille : Int) + (s.entropyMarginPermille : Int) - (s.quotientLossPermille : Int)

/-! ### 2. HIPÓTESIS EXPLÍCITAS -/

structure StabilizedMarginAssumptions (s : CurvatureMarginState) where
  h_compensated : s.quotientLossPermille ≤ s.intrinsicPermille + s.entropyMarginPermille
  h_strict_pos : s.quotientLossPermille < s.intrinsicPermille + s.entropyMarginPermille

/-! ### 3. TEOREMAS DEMOSTRADOS -/

theorem stabilized_margin_strictly_positive
    (s : CurvatureMarginState)
    (h : StabilizedMarginAssumptions s) :
    0 < netEffectiveMargin s := by
  have hlt :
      (s.quotientLossPermille : Int) <
        (s.intrinsicPermille : Int) + (s.entropyMarginPermille : Int) :=
    Int.ofNat_lt.mpr h.h_strict_pos
  unfold netEffectiveMargin
  omega

/-- Instancia ilustrativa escalada en milésimas (K_SU3 ~ 220‰, pérdida ~ 661‰, margen ~ 500‰ -> +59‰). -/
def sampleSU3Margin : CurvatureMarginState :=
  { intrinsicPermille := 220
    quotientLossPermille := 661
    entropyMarginPermille := 500 }

theorem sampleSU3Margin_positive :
    0 < netEffectiveMargin sampleSU3Margin :=
  stabilized_margin_strictly_positive sampleSU3Margin
    { h_compensated := by decide
      h_strict_pos := by decide }

end Oasis.YangMills.PaperY
