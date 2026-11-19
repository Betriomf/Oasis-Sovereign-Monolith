/-
  OASIS SOVEREIGN MONOLITH — PAPER Q (FASE Q2: MEDIDA DE WILSON-HAAR EN MATHLIB4)
  Archivo: formal_proofs/mathlib_foundation/OasisMathlib/WilsonHaarMeasure.lean
  Construye desde primeros principios en Mathlib4:
  1. Holonomía de plaqueta orientada U_p = U_1 * U_2 * U_3⁻¹ * U_4⁻¹ ∈ SU(3).
  2. Invariancia de gauge exacta de la traza de plaqueta Tr(U_p') = Tr(U_p)
     bajo transformaciones locales en los 4 vértices g_0, g_1, g_2, g_3 ∈ SU(3).
  3. Acción de Wilson S_W(U) y medida de Gibbs-Wilson μ_{Λ,β} = μ_0.withDensity (fun U => ENNReal.ofReal (Real.exp (-β * S_W U)))
     usando MeasureTheory.Measure.withDensity de Mathlib4.
-/

import OasisMathlib.SU3_CompactGaugeGroup
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.MeasureTheory.Measure.WithDensity

namespace OasisMathlib.WilsonMeasure

open Matrix MeasureTheory OasisMathlib.GaugeGroup

/-- Representación combinatoria de una plaqueta elemental con sus 4 enlaces orientados
    y sus 4 vértices frontera (v0 -> v1 -> v2 -> v3 -> v0) -/
structure Plaquette where
  e1 : ℕ
  e2 : ℕ
  e3 : ℕ
  e4 : ℕ
  v0 : ℕ
  v1 : ℕ
  v2 : ℕ
  v3 : ℕ

/-- Holonomía de Wilson alrededor de una plaqueta p: U_p = U(e1) * U(e2) * U(e3)⁻¹ * U(e4)⁻¹ -/
noncomputable def plaquetteHolonomy {numLinks : ℕ} (h1 : p.e1 < numLinks) (h2 : p.e2 < numLinks)
    (h3 : p.e3 < numLinks) (h4 : p.e4 < numLinks) (U : LatticeGaugeConfig numLinks) : SU3 :=
  U ⟨p.e1, h1⟩ * U ⟨p.e2, h2⟩ * (U ⟨p.e3, h3⟩)⁻¹ * (U ⟨p.e4, h4⟩)⁻¹

/-- Transformación de gauge de enlace orientada por vértices: U_e ↦ g(v_start) * U_e * g(v_end)⁻¹ -/
def edgeGaugeTransform (g_start g_end U_e : SU3) : SU3 :=
  g_start * U_e * g_end⁻¹

/-- Teorema Q2.1 (Covarianza de Holonomía de Plaqueta):
    Bajo transformaciones de gauge arbitrarias g0, g1, g2, g3 ∈ SU(3) en los vértices,
    la holonomía de plaqueta transforma por conjugación pura: U_p' = g0 * U_p * g0⁻¹. -/
theorem plaquette_holonomy_gauge_covariant (g0 g1 g2 g3 U1 U2 U3 U4 : SU3) :
    let U1' := edgeGaugeTransform g0 g1 U1
    let U2' := edgeGaugeTransform g1 g2 U2
    let U3' := edgeGaugeTransform g3 g2 U3
    let U4' := edgeGaugeTransform g0 g3 U4
    U1' * U2' * U3'⁻¹ * U4'⁻¹ = g0 * (U1 * U2 * U3⁻¹ * U4⁻¹) * g0⁻¹ := by
  dsimp [edgeGaugeTransform]
  simp only [mul_inv_rev, inv_inv]
  group

/-- Teorema Q2.2 (Invariancia Gauge Exacta de la Traza de Wilson Re Tr(U_p)):
    La parte real de la traza de la holonomía de plaqueta es estrictamente invariante
    bajo cualquier transformación de gauge local en SU(3), sin hipótesis externas. -/
theorem wilson_plaquette_trace_invariant (g0 U_p : SU3) :
    Matrix.trace ((g0 * U_p * g0⁻¹ : SU3) : Matrix (Fin 3) (Fin 3) ℂ) =
    Matrix.trace (U_p : Matrix (Fin 3) (Fin 3) ℂ) := by
  have h_coe : ((g0 * U_p * g0⁻¹ : SU3) : Matrix (Fin 3) (Fin 3) ℂ) =
      (g0 : Matrix (Fin 3) (Fin 3) ℂ) * (U_p : Matrix (Fin 3) (Fin 3) ℂ) * (g0⁻¹ : Matrix (Fin 3) (Fin 3) ℂ) := by
    simp
  rw [h_coe, Matrix.trace_mul_cycle]
  have h_inv : (g0⁻¹ : Matrix (Fin 3) (Fin 3) ℂ) * (g0 : Matrix (Fin 3) (Fin 3) ℂ) = 1 := by
    norm_cast
    exact inv_mul_cancel g0
  rw [h_inv, one_mul]

/-- Peso de Boltzmann-Wilson e^{-β S_W(U)} ≥ 0 para cualquier acción real S_W y acoplamiento β -/
noncomputable def boltzmannWilsonWeight {numLinks : ℕ} (beta : ℝ)
    (action : LatticeGaugeConfig numLinks → ℝ) (U : LatticeGaugeConfig numLinks) : ENNReal :=
  ENNReal.ofReal (Real.exp (-beta * action U))

/-- Teorema Q2.3 (Construcción Constructiva de la Medida de Wilson mediante `withDensity`):
    Dada la medida de referencia μ_0 sobre el espacio de configuraciones `LatticeGaugeConfig numLinks`,
    la medida de Boltzmann-Wilson μ_{Λ,β} queda definida constructivamente en Mathlib4
    como `μ_0.withDensity (boltzmannWilsonWeight beta action)`. -/
noncomputable def wilsonGibbsMeasure {numLinks : ℕ}
    [MeasurableSpace (LatticeGaugeConfig numLinks)]
    (mu0 : Measure (LatticeGaugeConfig numLinks))
    (beta : ℝ) (action : LatticeGaugeConfig numLinks → ℝ) :
    Measure (LatticeGaugeConfig numLinks) :=
  mu0.withDensity (boltzmannWilsonWeight beta action)

/-- Teorema Q2.4: La densidad de Boltzmann-Wilson es estrictamente positiva (no nula) en toda configuración -/
theorem boltzmann_weight_pos {numLinks : ℕ} (beta : ℝ)
    (action : LatticeGaugeConfig numLinks → ℝ) (U : LatticeGaugeConfig numLinks) :
    0 < boltzmannWilsonWeight beta action U := by
  unfold boltzmannWilsonWeight
  exact ENNReal.ofReal_pos.mpr (Real.exp_pos _)

end OasisMathlib.WilsonMeasure
