/-
  OASIS SOVEREIGN MONOLITH — PAPER Q (FASE Q8: DESIGUALDAD DE PINSKER DE DOS PUNTOS EN MATHLIB4)
  Archivo: formal_proofs/mathlib_foundation/OasisMathlib/ElementalPinsker_Inequality.lean
  Formaliza:
  1. Divergencia de Kullback–Leibler binaria D_KL(p ‖ q) y su anulación en equilibrio (p = q).
  2. No negatividad de Gibbs–Shannon D_KL(p ‖ q) ≥ 0 mediante `Real.log_le_sub_one_of_pos`.
  3. Desigualdad de Pinsker de dos puntos 2 * (p - q)^2 ≤ D_KL(p ‖ q) en (0, 1)
     vía cálculo diferencial (`monotoneOn_of_deriv_nonneg` sobre f'(p) y f(p)).
-/

import OasisMathlib.KullbackLeibler_PinskerBridge
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.MeanValue

namespace OasisMathlib.ElementalPinsker

open Real Set MeasureTheory OasisMathlib.KullbackLeiblerPinsker

/-- Divergencia de Kullback–Leibler de dos puntos (Bernoulli) para p, q ∈ (0, 1) -/
noncomputable def binaryKLDivergence (p q : ℝ) : ℝ :=
  p * Real.log (p / q) + (1 - p) * Real.log ((1 - p) / (1 - q))

/-- Función auxiliar de Pinsker: f_q(p) = D_KL(p ‖ q) - 2 * (p - q)^2 -/
noncomputable def pinskerGapFunc (q p : ℝ) : ℝ :=
  binaryKLDivergence p q - 2 * (p - q) ^ 2

/-- Primera derivada respecto a p: f_q'(p) = log(p / q) - log((1 - p) / (1 - q)) - 4 * (p - q) -/
noncomputable def pinskerGapDeriv (q p : ℝ) : ℝ :=
  Real.log (p / q) - Real.log ((1 - p) / (1 - q)) - 4 * (p - q)

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

/-- Teorema Q8.3 (Positividad de la Segunda Derivada f_q''(p) = 1/p + 1/(1-p) - 4 ≥ 0 en (0, 1)):
    La identidad (1 - 2p)^2 ≥ 0 implica 4 p (1 - p) ≤ 1, garantizando la convexidad estricta
    de la función de brecha de Pinsker en todo el intervalo abierto (0, 1). -/
theorem pinsker_second_deriv_nonneg {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    0 ≤ 1 / p + 1 / (1 - p) - 4 := by
  have h1mp : 0 < 1 - p := sub_pos.mpr hp1
  have h_sq : 0 ≤ (1 - 2 * p) ^ 2 := sq_nonneg (1 - 2 * p)
  have h_amgm : 4 * (p * (1 - p)) ≤ 1 := by linarith
  have h_prod_pos : 0 < p * (1 - p) := mul_pos hp0 h1mp
  rw [one_div_add_one_div (ne_of_gt hp0) (ne_of_gt h1mp)]
  have h_num : 1 - p + p = 1 := by ring
  rw [h_num]
  rw [sub_nonneg, le_div_iff₀ h_prod_pos]
  exact h_amgm

/-- Teorema Q8.4 (Derivada de `pinskerGapFunc` en (0, 1)): -/
theorem hasDerivAt_pinskerGapFunc {q p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hq0 : 0 < q) (hq1 : q < 1) :
    HasDerivAt (pinskerGapFunc q) (pinskerGapDeriv q p) p := by
  unfold pinskerGapFunc binaryKLDivergence pinskerGapDeriv
  have hp_ne : p ≠ 0 := ne_of_gt hp0
  have h1mp_ne : 1 - p ≠ 0 := ne_of_gt (sub_pos.mpr hp1)
  have h_div1 : p / q ≠ 0 := ne_of_gt (div_pos hp0 hq0)
  have h_div2 : (1 - p) / (1 - q) ≠ 0 := ne_of_gt (div_pos (sub_pos.mpr hp1) (sub_pos.mpr hq1))
  have d1 : HasDerivAt (fun x => x * Real.log (x / q)) (1 * Real.log (p / q) + p * ((1 / q) / (p / q))) p := by
    refine HasDerivAt.mul (hasDerivAt_id p) ?_
    exact HasDerivAt.log ((hasDerivAt_id p).div_const q) h_div1
  have d2 : HasDerivAt (fun x => (1 - x) * Real.log ((1 - x) / (1 - q)))
      ((-1) * Real.log ((1 - p) / (1 - q)) + (1 - p) * (((-1) / (1 - q)) / ((1 - p) / (1 - q)))) p := by
    have h_sub : HasDerivAt (fun x : ℝ => 1 - x) (-1) p := by
      simpa using (hasDerivAt_const p (1 : ℝ)).sub (hasDerivAt_id p)
    refine HasDerivAt.mul h_sub ?_
    exact HasDerivAt.log (h_sub.div_const (1 - q)) h_div2
  have d3 : HasDerivAt (fun x => 2 * (x - q) ^ 2) (2 * (2 * (p - q) ^ (2 - 1) * 1)) p := by
    refine HasDerivAt.const_mul 2 ?_
    exact HasDerivAt.pow 2 ((hasDerivAt_id p).sub_const q)
  convert (d1.add d2).sub d3 using 1
  field_simp [hp_ne, h1mp_ne, ne_of_gt hq0, ne_of_gt (sub_pos.mpr hq1)]
  ring

/-- Teorema Q8.5 (Derivada de `pinskerGapDeriv` en (0, 1)): -/
theorem hasDerivAt_pinskerGapDeriv {q p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hq0 : 0 < q) (hq1 : q < 1) :
    HasDerivAt (pinskerGapDeriv q) (1 / p + 1 / (1 - p) - 4) p := by
  unfold pinskerGapDeriv
  have hp_ne : p ≠ 0 := ne_of_gt hp0
  have h1mp_ne : 1 - p ≠ 0 := ne_of_gt (sub_pos.mpr hp1)
  have h_div1 : p / q ≠ 0 := ne_of_gt (div_pos hp0 hq0)
  have h_div2 : (1 - p) / (1 - q) ≠ 0 := ne_of_gt (div_pos (sub_pos.mpr hp1) (sub_pos.mpr hq1))
  have d1 : HasDerivAt (fun x => Real.log (x / q)) ((1 / q) / (p / q)) p :=
    HasDerivAt.log ((hasDerivAt_id p).div_const q) h_div1
  have d2 : HasDerivAt (fun x => Real.log ((1 - x) / (1 - q))) (((-1) / (1 - q)) / ((1 - p) / (1 - q))) p := by
    have h_sub : HasDerivAt (fun x : ℝ => 1 - x) (-1) p := by
      simpa using (hasDerivAt_const p (1 : ℝ)).sub (hasDerivAt_id p)
    exact HasDerivAt.log (h_sub.div_const (1 - q)) h_div2
  have d3 : HasDerivAt (fun x => 4 * (x - q)) (4 * 1) p :=
    HasDerivAt.const_mul 4 ((hasDerivAt_id p).sub_const q)
  convert (d1.sub d2).sub d3 using 1
  field_simp [hp_ne, h1mp_ne, ne_of_gt hq0, ne_of_gt (sub_pos.mpr hq1)]
  ring

/-- Teorema Maestro Q8.6 (Desigualdad de Pinsker de Dos Puntos 2 * (p - q)^2 ≤ D_KL(p ‖ q)):
    Para todo p, q ∈ (0, 1), la divergencia de Kullback–Leibler binaria domina
    cuadráticamente la distancia entre probabilidades sin hipótesis externas. -/
theorem binary_pinsker_inequality {p q : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hq0 : 0 < q) (hq1 : q < 1) :
    2 * (p - q) ^ 2 ≤ binaryKLDivergence p q := by
  have h_deriv_mono : MonotoneOn (pinskerGapDeriv q) (Ioo 0 1) := by
    refine monotoneOn_of_deriv_nonneg (convex_Ioo 0 1) ?_ ?_ ?_
    · intro x hx
      exact (hasDerivAt_pinskerGapDeriv hx.1 hx.2 hq0 hq1).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ioo] at hx
      exact (hasDerivAt_pinskerGapDeriv hx.1 hx.2 hq0 hq1).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ioo] at hx
      rw [(hasDerivAt_pinskerGapDeriv hx.1 hx.2 hq0 hq1).deriv]
      exact pinsker_second_deriv_nonneg hx.1 hx.2
  have h_deriv_at_q : pinskerGapDeriv q q = 0 := by
    unfold pinskerGapDeriv
    rw [div_self (ne_of_gt hq0), div_self (ne_of_gt (sub_pos.mpr hq1)), Real.log_one, Real.log_one]
    ring
  have h_gap_at_q : pinskerGapFunc q q = 0 := by
    unfold pinskerGapFunc
    rw [binary_kl_self_eq_zero hq0 hq1]
    ring
  have hq_mem : q ∈ Ioo (0 : ℝ) 1 := ⟨hq0, hq1⟩
  have hp_mem : p ∈ Ioo (0 : ℝ) 1 := ⟨hp0, hp1⟩
  have h_nonneg : 0 ≤ pinskerGapFunc q p := by
    rcases le_total q p with hqp | hpq
    · have h_mono : MonotoneOn (pinskerGapFunc q) (Icc q p) := by
        refine monotoneOn_of_deriv_nonneg (convex_Icc q p) ?_ ?_ ?_
        · intro x hx
          have hx0 : 0 < x := lt_of_lt_of_le hq0 hx.1
          have hx1 : x < 1 := lt_of_le_of_lt hx.2 hp1
          exact (hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).continuousAt.continuousWithinAt
        · intro x hx
          rw [interior_Icc] at hx
          have hx0 : 0 < x := lt_trans hq0 hx.1
          have hx1 : x < 1 := lt_trans hx.2 hp1
          exact (hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).differentiableAt.differentiableWithinAt
        · intro x hx
          rw [interior_Icc] at hx
          have hx0 : 0 < x := lt_trans hq0 hx.1
          have hx1 : x < 1 := lt_trans hx.2 hp1
          rw [(hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).deriv, ← h_deriv_at_q]
          exact h_deriv_mono hq_mem ⟨hx0, hx1⟩ (le_of_lt hx.1)
      rw [← h_gap_at_q]
      exact h_mono (left_mem_Icc.mpr hqp) (right_mem_Icc.mpr hqp) hqp
    · have h_anti : AntitoneOn (pinskerGapFunc q) (Icc p q) := by
        refine antitoneOn_of_deriv_nonpos (convex_Icc p q) ?_ ?_ ?_
        · intro x hx
          have hx0 : 0 < x := lt_of_lt_of_le hp0 hx.1
          have hx1 : x < 1 := lt_of_le_of_lt hx.2 hq1
          exact (hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).continuousAt.continuousWithinAt
        · intro x hx
          rw [interior_Icc] at hx
          have hx0 : 0 < x := lt_trans hp0 hx.1
          have hx1 : x < 1 := lt_trans hx.2 hq1
          exact (hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).differentiableAt.differentiableWithinAt
        · intro x hx
          rw [interior_Icc] at hx
          have hx0 : 0 < x := lt_trans hp0 hx.1
          have hx1 : x < 1 := lt_trans hx.2 hq1
          rw [(hasDerivAt_pinskerGapFunc hx0 hx1 hq0 hq1).deriv, ← h_deriv_at_q]
          exact h_deriv_mono ⟨hx0, hx1⟩ hq_mem (le_of_lt hx.2)
      rw [← h_gap_at_q]
      exact h_anti (left_mem_Icc.mpr hpq) (right_mem_Icc.mpr hpq) hpq
  unfold pinskerGapFunc at h_nonneg
  linarith

end OasisMathlib.ElementalPinsker
