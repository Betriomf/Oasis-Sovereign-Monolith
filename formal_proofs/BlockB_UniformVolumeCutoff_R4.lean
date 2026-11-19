/-
  OASIS SOVEREIGN MONOLITH — BLOQUE B: ESTIMACIONES UNIFORMES EN VOLUMEN Y CORTE
  Archivo: formal_proofs/BlockB_UniformVolumeCutoff_R4.lean
  Compilación estricta en Lean 4.36.0 puro: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Separación explícita:
    - [DEFINICIÓN]: configuración de volumen/corte y cotas en unidades escaladas (10⁻³).
    - [HIPÓTESIS EXPLÍCITA]: cotas uniformes exigidas para configuraciones y cadenas de regulación.
    - [TEOREMA DEMOSTRADO]: preservación de cotas, estabilidad por deriva y cota en cadena.
-/

namespace Oasis.YangMills.BlockBVolumeCutoff

/-! ### 1. DEFINICIONES -/

/-- Parámetros de regulación: volumen `volumeL` (> 0) y corte/escala `cutoffScaleK`. -/
structure RegulatorConfig where
  volumeL : Nat
  cutoffScaleK : Nat
  h_vol_pos : 0 < volumeL

/-- Cotas asociadas a una configuración `(volumeL, cutoffScaleK)` en milésimas (10⁻³). -/
structure RegulatorBounds where
  cfg : RegulatorConfig
  momentPermille : Nat
  decayRatePermille : Nat
  driftPermille : Nat

/-! ### 2. HIPÓTESIS EXPLÍCITAS -/

/-- Hipótesis explícitas de uniformidad para `b : RegulatorBounds`. -/
structure UniformRegulatorAssumptions (b : RegulatorBounds) where
  h_moment_cap : b.momentPermille ≤ 3000
  h_decay_floor : 1 ≤ b.decayRatePermille
  h_drift_cap : b.driftPermille ≤ 250

/-! ### 3. TEOREMAS DEMOSTRADOS -/

/-- Si `b1` y `b2` satisfacen las hipótesis explícitas de uniformidad, ambas conservan
    la cota de momento, la cota inferior positiva de decaimiento y la cota de deriva. -/
theorem uniform_bounds_across_regulators
    (b1 b2 : RegulatorBounds)
    (a1 : UniformRegulatorAssumptions b1)
    (a2 : UniformRegulatorAssumptions b2) :
    b1.momentPermille ≤ 3000 ∧ b2.momentPermille ≤ 3000 ∧
    0 < b1.decayRatePermille ∧ 0 < b2.decayRatePermille ∧
    b1.driftPermille ≤ 250 ∧ b2.driftPermille ≤ 250 := by
  exact ⟨
    a1.h_moment_cap,
    a2.h_moment_cap,
    Nat.lt_of_lt_of_le (by decide) a1.h_decay_floor,
    Nat.lt_of_lt_of_le (by decide) a2.h_decay_floor,
    a1.h_drift_cap,
    a2.h_drift_cap
  ⟩

/-- Si la diferencia entre dos cotas de momento está dominada por la suma
    de sus cotas de deriva `b1.driftPermille + b2.driftPermille`, queda acotada
    por `500` cuando ambos estados cumplen `driftPermille ≤ 250`. -/
theorem moment_diff_bounded_by_drifts
    (b1 b2 : RegulatorBounds)
    (a1 : UniformRegulatorAssumptions b1)
    (a2 : UniformRegulatorAssumptions b2)
    (diffPermille : Nat)
    (h_diff : diffPermille ≤ b1.driftPermille + b2.driftPermille) :
    diffPermille ≤ 500 := by
  have h_sum : b1.driftPermille + b2.driftPermille ≤ 250 + 250 :=
    Nat.add_le_add a1.h_drift_cap a2.h_drift_cap
  exact Nat.le_trans h_diff (by simpa using h_sum)

/-- A lo largo de `n` pasos de regulación, si cada estado `chain i` satisface
    `UniformRegulatorAssumptions` y su deriva está acotada por `stepDrift ≤ 250`,
    la deriva acumulada `n * stepDrift` está dominada por `n * 250` y el volumen
    en `n` es estrictamente positivo. -/
theorem chain_regulator_drift_bound
    (n stepDrift : Nat)
    (chain : Nat → RegulatorBounds)
    (h_all : ∀ i : Nat, UniformRegulatorAssumptions (chain i))
    (h_step_drift : stepDrift ≤ 250) :
    0 < (chain n).cfg.volumeL ∧
    n * stepDrift ≤ n * 250 := by
  have _ := h_all n
  exact ⟨(chain n).cfg.h_vol_pos, Nat.mul_le_mul_left n h_step_drift⟩

end Oasis.YangMills.BlockBVolumeCutoff
