/-
  OASIS SOVEREIGN MONOLITH — FASE 3: COTA TELESCÓPICA ACUMULADA Y COTA DE COLA/MOMENTO
  Archivo: formal_proofs/tightness_telescopiccauchy_fase3.lean
  Compilación estricta en Lean 4.36.0 puro: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
  Nota de alcance: Formaliza la suma telescópica y el control de cola/momento en n pasos
  (en 10⁻³); la compacidad relativa topológica completa en S'(ℝ⁴) sigue siendo un paso analítico mayor.
-/

namespace Oasis.YangMills.Fase3TelescopicCauchy

/-- Suma acumulada de diferencias entre escalas desde `i = 0` hasta `i < n`. -/
def telescopicStepSum (stepDiff : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k + 1 => telescopicStepSum stepDiff k + stepDiff k

@[simp]
theorem telescopicStepSum_zero (stepDiff : Nat → Nat) :
    telescopicStepSum stepDiff 0 = 0 := rfl

@[simp]
theorem telescopicStepSum_succ (stepDiff : Nat → Nat) (k : Nat) :
    telescopicStepSum stepDiff (k + 1) = telescopicStepSum stepDiff k + stepDiff k := rfl

/-- Si cada diferencia de paso `stepDiff i` está acotada por `perStepBound`,
    la suma telescópica en `n` pasos está acotada por `n * perStepBound`. -/
theorem telescopic_sum_le_mul
    (stepDiff : Nat → Nat)
    (perStepBound : Nat)
    (h_step : ∀ i, stepDiff i ≤ perStepBound)
    (n : Nat) :
    telescopicStepSum stepDiff n ≤ n * perStepBound := by
  induction n with
  | zero =>
    simp
  | succ k ih =>
    have h_add : telescopicStepSum stepDiff k + stepDiff k ≤ k * perStepBound + perStepBound :=
      Nat.add_le_add ih (h_step k)
    simpa [telescopicStepSum_succ, Nat.succ_mul] using h_add

/-- Si la suma telescópica en `n` pasos está dominada por una cota uniforme `uniformCap`,
    la acumulación permanece uniformemente acotada por `uniformCap`. -/
theorem telescopic_sum_uniform_cap
    (stepDiff : Nat → Nat)
    (uniformCap : Nat)
    (h_cap : ∀ n, telescopicStepSum stepDiff n ≤ uniformCap)
    (n : Nat) :
    telescopicStepSum stepDiff n ≤ uniformCap :=
  h_cap n

/-- Lema de cola/momento en el paso `n`: si el momento en la escala `n` está acotado por
    `momentCap` y la variación telescópica acumulada hasta `n` está acotada por `uniformCap`,
    ambas cotas se cumplen simultáneamente en `n` (y su suma queda acotada por `momentCap + uniformCap`). -/
theorem tail_moment_bound_at_step
    (momentAt : Nat → Nat)
    (stepDiff : Nat → Nat)
    (momentCap uniformCap n : Nat)
    (h_mom : ∀ k, momentAt k ≤ momentCap)
    (h_tel : ∀ k, telescopicStepSum stepDiff k ≤ uniformCap) :
    momentAt n ≤ momentCap ∧
    telescopicStepSum stepDiff n ≤ uniformCap ∧
    momentAt n + telescopicStepSum stepDiff n ≤ momentCap + uniformCap := by
  refine ⟨h_mom n, h_tel n, ?_⟩
  exact Nat.add_le_add (h_mom n) (h_tel n)

end Oasis.YangMills.Fase3TelescopicCauchy
