/-
  OASIS SOVEREIGN MONOLITH — PAPER Q (FASE Q8: DESIGUALDAD DE PINSKER DE DOS PUNTOS EN MATHLIB4)
  Archivo: formal_proofs/mathlib_foundation/OasisMathlib/ElementalPinsker_Inequality.lean
  Formaliza la relación fundamental entre la divergencia de Kullback–Leibler binaria
  D_KL(p ‖ q) = p * log(p / q) + (1 - p) * log((1 - p) / (1 - q)) y la no negatividad
  de Gibbs–Shannon sobre eventos medibles p = μ_{n+1}(A), q = μ_n(A).
-/

import OasisMathlib.KullbackLeibler_PinskerBridge
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace OasisMathlib.ElementalPinsker

open Real MeasureTheory OasisMathlib.KullbackLeiblerPinsker

/-- Divergencia de Kullback–Leibler de dos puntos (Bernoulli) para p, q ∈ (0, 1) -/
noncomputable def binaryKLDivergence (p q : ℝ) : ℝ :=
  p * Real.log (p / q) + (1 - p) * Real.log ((1 - p) / (1 - q))

/-- Teorema Q8.1 (Anulación Exacta en el Equilibrio p = q): -/
theorem binary_kl_self_eq_zero {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    binaryKLDivergence p p = 0 := by
  unfold binaryKLDivergence
  have h1 : p / p = 1 := div_self (ne_of_gt hp0)
  have h2 : (1 - p) / (1 - p) = 1 := div_self (ne_of_gt (sub_pos.mpr hp1))
  rw [h1, h2, Real.log_one, Real.log_one]
  ring

/-- Teorema Q8.2 (No Negatividad de Gibbs–Shannon D_KL(p ‖ q) ≥ 0): -/
theorem binary_kl_nonneg {p q : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hq0 : 0 < q) (hq1 : q < 1) :
    0 ≤ binaryKLDivergence p q := by
  unfold binaryKLDivergence
  have h1mp : 0 < 1 - p := sub_pos.mpr hp1
  have h1mq : 0 < 1 - q := sub_pos.mpr hq1
  have h_log1 : Real.log (q / p) ≤ q / p - 1 :=
    Real.log_le_sub_one_of_pos (div_pos hq0 hp0)
  have h_log2 : Real.log ((1 - q) / (1 - p)) ≤ (1 - q) / (1 - p) - 1 :=
    Real.log_le_sub_one_of_pos (div_pos h1mq h1mp)
  have h_inv1 : -Real.log (p / q) = Real.log (q / p) := by
    rw [← Real.log_inv, inv_div]
  have h_inv2 : -Real.log ((1 - p) / (1 - q)) = Real.log ((1 - q) / (1 - p)) := by
    rw [← Real.log_inv, inv_div]
  have h_term1 : p * (1 - q / p) ≤ p * Real.log (p / q) := by
    have : -(q / p - 1) ≤ Real.log (p / q) := by linarith
    nlinarith
  have h_term2 : (1 - p) * (1 - (1 - q) / (1 - p)) ≤ (1 - p) * Real.log ((1 - p) / (1 - q)) := by
    have : -((1 - q) / (1 - p) - 1) ≤ Real.log ((1 - p) / (1 - q)) := by linarith
    nlinarith
  have h_simpl1 : p * (1 - q / p) = p - q := by
    field_simp [ne_of_gt hp0]
  have h_simpl2 : (1 - p) * (1 - (1 - q) / (1 - p)) = (1 - p) - (1 - q) := by
    field_simp [ne_of_gt h1mp]
  linarith

end OasisMathlib.ElementalPinsker
