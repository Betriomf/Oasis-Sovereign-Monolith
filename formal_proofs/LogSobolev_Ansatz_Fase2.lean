namespace Oasis.Ruta0001.Fase2

structure RenormalizationLogSobolevBlock where
  lsiNum : Nat
  lsiDen : Nat
  h_lsi_pos : 0 < lsiNum
  h_lsi_den_pos : 0 < lsiDen
  uvErrorTerm : Nat → Nat
  relEntropyScale : Nat → Nat
  h_uv_dominated_by_entropy : ∀ k : Nat, uvErrorTerm k ≤ relEntropyScale k
  h_log_sobolev_ansatz : ∀ k : Nat,
    relEntropyScale (k + 1) * (lsiDen + lsiNum) ≤ relEntropyScale k * lsiDen

theorem log_sobolev_prevents_uv_blowup (B : RenormalizationLogSobolevBlock) (k : Nat) :
    B.relEntropyScale (k + 1) ≤ B.relEntropyScale k := by
  have h1 := B.h_log_sobolev_ansatz k
  have h2 : B.relEntropyScale k * B.lsiDen ≤ B.relEntropyScale k * (B.lsiDen + B.lsiNum) :=
    Nat.mul_le_mul_left (B.relEntropyScale k) (Nat.le_add_right B.lsiDen B.lsiNum)
  have h3 : B.relEntropyScale (k + 1) * (B.lsiDen + B.lsiNum) ≤
            B.relEntropyScale k * (B.lsiDen + B.lsiNum) :=
    Nat.le_trans h1 h2
  have h_pos : 0 < B.lsiDen + B.lsiNum := Nat.add_pos_left B.h_lsi_den_pos B.lsiNum
  exact Nat.le_of_mul_le_mul_right h3 h_pos

theorem uv_residual_bounded_across_all_scales (B : RenormalizationLogSobolevBlock) :
    ∀ k : Nat, B.uvErrorTerm k ≤ B.relEntropyScale 0 := by
  intro k
  have h_uv : B.uvErrorTerm k ≤ B.relEntropyScale k := B.h_uv_dominated_by_entropy k
  have h_dec : B.relEntropyScale k ≤ B.relEntropyScale 0 := by
    clear h_uv
    induction k with
    | zero => exact Nat.le_refl _
    | succ m ih => exact Nat.le_trans (log_sobolev_prevents_uv_blowup B m) ih
  exact Nat.le_trans h_uv h_dec

theorem log_sobolev_dissipation_gap_positive (B : RenormalizationLogSobolevBlock) :
    B.lsiDen < B.lsiDen + B.lsiNum := by
  exact Nat.lt_add_of_pos_right B.h_lsi_pos

end Oasis.Ruta0001.Fase2
