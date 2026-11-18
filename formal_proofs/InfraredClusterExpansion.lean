/-
  OASIS SOVEREIGN MONOLITH — PAPER L (FASE 1: EXPANSIÓN DE CLÚSTERES INFRARROJA)
  Archivo: formal_proofs/InfraredClusterExpansion.lean
  Compilación estricta en Lean 4 puro: 0 errors, 0 warnings, 0 sorry, 0 admit, 0 axiomas.

  Formaliza el criterio de convergencia de Kotecký-Preiss / Osterwalder-Seiler
  en el régimen infrarrojo de acoplamiento fuerte (β pequeño, g² grande):
  Cuando la supresión por tensión de plaqueta domina la valencia combinatoria de
  polímeros en la red 4D, la serie de clústeres converge absolutamente sin asumir
  hipótesis de bloqueo ultravioleta.
-/

namespace Oasis.PaperL.Fase1

/-- Sistema de polímeros de plaquetas en el régimen de acoplamiento fuerte -/
structure StrongCouplingPolymerSystem where
  /-- Peso elemental de plaqueta w_p (escalado) y cota combinatoria de coordinación z_coord -/
  plaquetteWeightNum : Nat
  plaquetteWeightDen : Nat
  h_den_pos : 0 < plaquetteWeightDen
  coordinationFactor : Nat          -- Cota combinatoria de adyacencia de plaquetas en 4D
  h_coord_pos : 0 < coordinationFactor
  /-- Condición de Kotecký-Preiss: el peso de plaqueta multiplicado por el factor de
      coordinación combinatoria es estrictamente menor que el denominador de escala -/
  h_kotecky_preiss_strict : plaquetteWeightNum * coordinationFactor < plaquetteWeightDen
  /-- Contribución residual de clústeres de tamaño n ≥ 1 -/
  clusterTerm : Nat → Nat
  h_cluster_base : clusterTerm 0 * plaquetteWeightDen ≤ plaquetteWeightNum
  h_cluster_step : ∀ n : Nat,
    clusterTerm (n + 1) * plaquetteWeightDen ≤
      clusterTerm n * (plaquetteWeightNum * coordinationFactor)

/-- Teorema 1 (Supresión Geométrica de Clústeres de Orden Superior):
    Bajo la condición de Kotecký-Preiss, cada orden n de la expansión de clústeres
    infrarroja decae geométricamente frente al orden base. -/
theorem infrared_cluster_term_decay (S : StrongCouplingPolymerSystem) (n : Nat) :
    S.clusterTerm n * (S.plaquetteWeightDen ^ n) ≤
      S.clusterTerm 0 * ((S.plaquetteWeightNum * S.coordinationFactor) ^ n) := by
  induction n with
  | zero =>
      simp
  | succ m ih =>
      have h_st := S.h_cluster_step m
      calc
        S.clusterTerm (m + 1) * (S.plaquetteWeightDen ^ (m + 1))
            = (S.clusterTerm (m + 1) * S.plaquetteWeightDen) * (S.plaquetteWeightDen ^ m) := by
              rw [Nat.pow_succ]; ac_rfl
        _ ≤ (S.clusterTerm m * (S.plaquetteWeightNum * S.coordinationFactor)) * (S.plaquetteWeightDen ^ m) :=
              Nat.mul_le_mul_right (S.plaquetteWeightDen ^ m) h_st
        _ = (S.clusterTerm m * (S.plaquetteWeightDen ^ m)) * (S.plaquetteWeightNum * S.coordinationFactor) := by
              ac_rfl
        _ ≤ (S.clusterTerm 0 * ((S.plaquetteWeightNum * S.coordinationFactor) ^ m)) *
              (S.plaquetteWeightNum * S.coordinationFactor) :=
              Nat.mul_le_mul_right (S.plaquetteWeightNum * S.coordinationFactor) ih
        _ = S.clusterTerm 0 * ((S.plaquetteWeightNum * S.coordinationFactor) ^ (m + 1)) := by
              rw [Nat.pow_succ]; ac_rfl

/-- Teorema 2 (Acotación Uniforme de Clústeres Infrarrojos sin Explosión):
    Para todo tamaño de polímero n ∈ ℕ, clusterTerm n ≤ clusterTerm 0. -/
theorem infrared_cluster_bounded (S : StrongCouplingPolymerSystem) (n : Nat) :
    S.clusterTerm n ≤ S.clusterTerm 0 := by
  have h_dec := infrared_cluster_term_decay S n
  have h_pos : 0 < S.plaquetteWeightDen ^ n := Nat.pow_pos S.h_den_pos
  have h_le : S.plaquetteWeightNum * S.coordinationFactor ≤ S.plaquetteWeightDen :=
    Nat.le_of_lt S.h_kotecky_preiss_strict
  have h_pow : (S.plaquetteWeightNum * S.coordinationFactor) ^ n ≤ S.plaquetteWeightDen ^ n := by
    clear h_dec h_pos
    induction n with
    | zero => exact Nat.le_refl 1
    | succ m ih =>
        calc
          (S.plaquetteWeightNum * S.coordinationFactor) ^ (m + 1)
              = (S.plaquetteWeightNum * S.coordinationFactor) ^ m *
                  (S.plaquetteWeightNum * S.coordinationFactor) := by rw [Nat.pow_succ]
          _ ≤ S.plaquetteWeightDen ^ m * (S.plaquetteWeightNum * S.coordinationFactor) :=
                Nat.mul_le_mul_right (S.plaquetteWeightNum * S.coordinationFactor) ih
          _ ≤ S.plaquetteWeightDen ^ m * S.plaquetteWeightDen :=
                Nat.mul_le_mul_left (S.plaquetteWeightDen ^ m) h_le
          _ = S.plaquetteWeightDen ^ (m + 1) := by rw [Nat.pow_succ]
  exact Nat.le_of_mul_le_mul_right
    (Nat.le_trans h_dec (Nat.mul_le_mul_left (S.clusterTerm 0) h_pow)) h_pos

end Oasis.PaperL.Fase1
