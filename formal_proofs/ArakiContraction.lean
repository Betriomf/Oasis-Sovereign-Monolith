/-
  OASIS SOVEREIGN MONOLITH — PROTOCOLO PUENTE ARAKI-ESPECTRAL (FASE 2: EL MURO DE ARAKI)
  Objetivo: Aislar formalmente el operador de contracción basado en la entropía relativa de Araki
  y demostrar (0 sorry, 0 admit, 0 axiomas personalizados) que:
  1. Bajo monotonía de Araki, la divergencia entre estados cuánticos nunca aumenta.
  2. La iteración n-ésima comprime exponencialmente el ruido por inducción.
  3. Un canal contractivo fiel preserva la distinguibilidad (no destruye información en tiempo finito).
-/

namespace Oasis.ArakiSpectralBridge.Fase2

structure ArakiDivergenceSpace (State : Type) where
  relEntropy : State → State → Nat
  zero_iff_eq : ∀ ρ σ : State, relEntropy ρ σ = 0 ↔ ρ = σ

structure ArakiContractionChannel (State : Type) (S : ArakiDivergenceSpace State) where
  step : State → State
  contractNum : Nat
  fidelityNum : Nat
  denom : Nat
  h_denom_pos : 0 < denom
  h_fidelity_pos : 0 < fidelityNum
  h_ordered : fidelityNum ≤ contractNum
  h_contractive : contractNum ≤ denom
  h_araki_monotonicity : ∀ ρ σ : State,
    S.relEntropy (step ρ) (step σ) * denom ≤ S.relEntropy ρ σ * contractNum
  h_faithful_lower : ∀ ρ σ : State,
    S.relEntropy ρ σ * fidelityNum ≤ S.relEntropy (step ρ) (step σ) * denom

def iterateStep {State : Type} {S : ArakiDivergenceSpace State}
    (Φ : ArakiContractionChannel State S) : Nat → State → State
  | 0, ρ => ρ
  | n + 1, ρ => Φ.step (iterateStep Φ n ρ)

/-- Teorema 1 (No-Expansividad de Araki) -/
theorem araki_monotone_non_expansive {State : Type} {S : ArakiDivergenceSpace State}
    (Φ : ArakiContractionChannel State S) (ρ σ : State) :
    S.relEntropy (Φ.step ρ) (Φ.step σ) ≤ S.relEntropy ρ σ := by
  have h1 := Φ.h_araki_monotonicity ρ σ
  have h2 : S.relEntropy ρ σ * Φ.contractNum ≤ S.relEntropy ρ σ * Φ.denom :=
    Nat.mul_le_mul_left (S.relEntropy ρ σ) Φ.h_contractive
  have h3 : S.relEntropy (Φ.step ρ) (Φ.step σ) * Φ.denom ≤ S.relEntropy ρ σ * Φ.denom :=
    Nat.le_trans h1 h2
  exact Nat.le_of_mul_le_mul_right h3 Φ.h_denom_pos

/-- Teorema 2 (Contracción Iterada en n pasos por inducción) -/
theorem araki_iterated_contraction {State : Type} {S : ArakiDivergenceSpace State}
    (Φ : ArakiContractionChannel State S) (n : Nat) (ρ σ : State) :
    S.relEntropy (iterateStep Φ n ρ) (iterateStep Φ n σ) * (Φ.denom ^ n) ≤
      S.relEntropy ρ σ * (Φ.contractNum ^ n) := by
  induction n with
  | zero =>
      simp [iterateStep]
  | succ k ih =>
      have h_step := Φ.h_araki_monotonicity (iterateStep Φ k ρ) (iterateStep Φ k σ)
      have h_mul1 :
          S.relEntropy (iterateStep Φ (k + 1) ρ) (iterateStep Φ (k + 1) σ) * (Φ.denom ^ (k + 1)) =
          (S.relEntropy (Φ.step (iterateStep Φ k ρ)) (Φ.step (iterateStep Φ k σ)) * Φ.denom) * (Φ.denom ^ k) := by
        simp [iterateStep, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      have h_mul2 :
          (S.relEntropy (Φ.step (iterateStep Φ k ρ)) (Φ.step (iterateStep Φ k σ)) * Φ.denom) * (Φ.denom ^ k) ≤
          (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * Φ.contractNum) * (Φ.denom ^ k) :=
        Nat.mul_le_mul_right (Φ.denom ^ k) h_step
      have h_reassoc :
          (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * Φ.contractNum) * (Φ.denom ^ k) =
          (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * (Φ.denom ^ k)) * Φ.contractNum := by
        simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      have h_mul3 :
          (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * (Φ.denom ^ k)) * Φ.contractNum ≤
          (S.relEntropy ρ σ * (Φ.contractNum ^ k)) * Φ.contractNum :=
        Nat.mul_le_mul_right Φ.contractNum ih
      have h_rhs :
          (S.relEntropy ρ σ * (Φ.contractNum ^ k)) * Φ.contractNum =
          S.relEntropy ρ σ * (Φ.contractNum ^ (k + 1)) := by
        simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      rw [h_mul1]
      exact Nat.le_trans h_mul2 (by rw [h_reassoc, h_rhs]; exact h_mul3)

/-- Teorema 3 (Preservación de Información / No-Colapso en Tiempo Finito) -/
theorem araki_contraction_preserves_information {State : Type} {S : ArakiDivergenceSpace State}
    (Φ : ArakiContractionChannel State S) (n : Nat) (ρ σ : State)
    (h_distinct : ρ ≠ σ) :
    iterateStep Φ n ρ ≠ iterateStep Φ n σ := by
  have h_pos : 0 < S.relEntropy ρ σ := by
    have h_ne : S.relEntropy ρ σ ≠ 0 := by
      intro h_z
      exact h_distinct ((S.zero_iff_eq ρ σ).mp h_z)
    exact Nat.pos_of_ne_zero h_ne
  have h_lower : ∀ m : Nat,
      S.relEntropy ρ σ * (Φ.fidelityNum ^ m) ≤
      S.relEntropy (iterateStep Φ m ρ) (iterateStep Φ m σ) * (Φ.denom ^ m) := by
    intro m
    induction m with
    | zero =>
        simp [iterateStep]
    | succ k ih =>
        have h_f := Φ.h_faithful_lower (iterateStep Φ k ρ) (iterateStep Φ k σ)
        have h1 :
            S.relEntropy ρ σ * (Φ.fidelityNum ^ (k + 1)) =
            (S.relEntropy ρ σ * (Φ.fidelityNum ^ k)) * Φ.fidelityNum := by
          simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        have h2 :
            (S.relEntropy ρ σ * (Φ.fidelityNum ^ k)) * Φ.fidelityNum ≤
            (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * (Φ.denom ^ k)) * Φ.fidelityNum :=
          Nat.mul_le_mul_right Φ.fidelityNum ih
        have h3 :
            (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * (Φ.denom ^ k)) * Φ.fidelityNum =
            (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * Φ.fidelityNum) * (Φ.denom ^ k) := by
          simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        have h4 :
            (S.relEntropy (iterateStep Φ k ρ) (iterateStep Φ k σ) * Φ.fidelityNum) * (Φ.denom ^ k) ≤
            (S.relEntropy (iterateStep Φ (k + 1) ρ) (iterateStep Φ (k + 1) σ) * Φ.denom) * (Φ.denom ^ k) :=
          Nat.mul_le_mul_right (Φ.denom ^ k) h_f
        have h5 :
            (S.relEntropy (iterateStep Φ (k + 1) ρ) (iterateStep Φ (k + 1) σ) * Φ.denom) * (Φ.denom ^ k) =
            S.relEntropy (iterateStep Φ (k + 1) ρ) (iterateStep Φ (k + 1) σ) * (Φ.denom ^ (k + 1)) := by
          simp [iterateStep, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        rw [h1]
        exact Nat.le_trans h2 (by rw [h3, ← h5]; exact h4)
  have h_fid_pow_pos : 0 < Φ.fidelityNum ^ n := Nat.pow_pos Φ.h_fidelity_pos
  have h_lhs_pos : 0 < S.relEntropy ρ σ * (Φ.fidelityNum ^ n) :=
    Nat.mul_pos h_pos h_fid_pow_pos
  have h_rhs_pos : 0 < S.relEntropy (iterateStep Φ n ρ) (iterateStep Φ n σ) * (Φ.denom ^ n) :=
    Nat.lt_of_lt_of_le h_lhs_pos (h_lower n)
  intro h_eq_n
  have h_zero_n : S.relEntropy (iterateStep Φ n ρ) (iterateStep Φ n σ) = 0 :=
    (S.zero_iff_eq _ _).mpr h_eq_n
  rw [h_zero_n, Nat.zero_mul] at h_rhs_pos
  exact Nat.lt_irrefl 0 h_rhs_pos

/-- Teorema 4 (Estabilidad del Punto Fijo de Equilibrio) -/
theorem araki_equilibrium_attraction {State : Type} {S : ArakiDivergenceSpace State}
    (Φ : ArakiContractionChannel State S) (ρ ω : State) (h_fix : Φ.step ω = ω) :
    S.relEntropy (Φ.step ρ) ω ≤ S.relEntropy ρ ω := by
  have h := araki_monotone_non_expansive Φ ρ ω
  rw [h_fix] at h
  exact h

end Oasis.ArakiSpectralBridge.Fase2
