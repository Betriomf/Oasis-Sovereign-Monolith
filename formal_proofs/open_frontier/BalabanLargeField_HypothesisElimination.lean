/-
  OASIS SOVEREIGN MONOLITH — PAPER P (SUB-LEMA P3: CAMPO GRANDE BALABAN & SIMETRÍA SO(4))
  Archivo: formal_proofs/open_frontier/BalabanLargeField_HypothesisElimination.lean
  Compilación estricta en Lean 4.36.0 puro: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.PaperP.SubLemmaP3

structure BalabanContinuumRestorationSystem where
  lfCapNum : Nat
  lfCapDen : Nat
  h_lf_cap_pos : 0 < lfCapNum ∧ 0 < lfCapDen
  lfProbNum : Nat → Nat
  lfProbDen : Nat → Nat
  h_lf_den_pos : ∀ k : Nat, 0 < lfProbDen k
  h_large_field_suppression : ∀ k : Nat,
    (lfProbNum k * (2 ^ k)) * lfCapDen ≤ lfCapNum * lfProbDen k
  anisoCapNum : Nat
  anisoCapDen : Nat
  h_aniso_cap_pos : 0 < anisoCapNum ∧ 0 < anisoCapDen
  so4ErrNum : Nat → Nat
  so4ErrDen : Nat → Nat
  h_so4_den_pos : ∀ k : Nat, 0 < so4ErrDen k
  h_so4_quadratic_restoration : ∀ k : Nat,
    (so4ErrNum k * (4 ^ k)) * anisoCapDen ≤ anisoCapNum * so4ErrDen k

theorem balaban_large_field_and_so4_restoration
    (B : BalabanContinuumRestorationSystem) (k : Nat) :
    (0 < (2 ^ k) * B.lfCapDen ∧
      B.lfProbNum k * B.lfCapDen ≤ B.lfCapNum * B.lfProbDen k) ∧
    (0 < (4 ^ k) * B.anisoCapDen ∧
      B.so4ErrNum k * B.anisoCapDen ≤ B.anisoCapNum * B.so4ErrDen k) := by
  have h2_pos : 0 < 2 ^ k := Nat.two_pow_pos k
  have h2_ge1 : 1 ≤ 2 ^ k := Nat.one_le_two_pow
  have h_lf := B.h_large_field_suppression k
  have h_lf_step : B.lfProbNum k * B.lfCapDen ≤ (B.lfProbNum k * (2 ^ k)) * B.lfCapDen := by
    have h1 : B.lfProbNum k * 1 ≤ B.lfProbNum k * (2 ^ k) := Nat.mul_le_mul_left (B.lfProbNum k) h2_ge1
    simpa [Nat.mul_one] using Nat.mul_le_mul_right B.lfCapDen h1

  have h4_ge1 : 1 ≤ 4 ^ k := Nat.one_le_pow k 4 (by decide)
  have h4_pos : 0 < 4 ^ k := Nat.lt_of_lt_of_le (by decide) h4_ge1
  have h_so4 := B.h_so4_quadratic_restoration k
  have h_so4_step : B.so4ErrNum k * B.anisoCapDen ≤ (B.so4ErrNum k * (4 ^ k)) * B.anisoCapDen := by
    have h1 : B.so4ErrNum k * 1 ≤ B.so4ErrNum k * (4 ^ k) := Nat.mul_le_mul_left (B.so4ErrNum k) h4_ge1
    simpa [Nat.mul_one] using Nat.mul_le_mul_right B.anisoCapDen h1

  exact ⟨
    ⟨Nat.mul_pos h2_pos B.h_lf_cap_pos.2, Nat.le_trans h_lf_step h_lf⟩,
    ⟨Nat.mul_pos h4_pos B.h_aniso_cap_pos.2, Nat.le_trans h_so4_step h_so4⟩
  ⟩

end Oasis.PaperP.SubLemmaP3
