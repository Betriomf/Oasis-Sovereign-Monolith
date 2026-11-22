/-
  OASIS SOVEREIGN MONOLITH — STRING SPECTRUM & REGGE BOUND SPECIFICATION
  Archivo: formal_proofs/StringTheory_Regge_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.StringTheory

def bosonicCriticalDim : Nat := 26
def superstringCriticalDim : Nat := 10

def openStringMassSq (level : Nat) : Int :=
  (level : Int) - 1

def closedStringMassSq (level : Nat) : Int :=
  2 * ((level : Int) - 2)

theorem critical_dimensions_relation :
    bosonicCriticalDim = superstringCriticalDim + 16 := by
  decide

theorem open_spectrum_monotone_for_positive_levels
    (n₁ n₂ : Nat)
    (_h_pos₁ : 1 ≤ n₁)
    (h_le : n₁ ≤ n₂) :
    openStringMassSq n₁ ≤ openStringMassSq n₂ := by
  unfold openStringMassSq
  omega

theorem closed_spectrum_monotone_for_levels_ge_two
    (n₁ n₂ : Nat)
    (_h_ge₂ : 2 ≤ n₁)
    (h_le : n₁ ≤ n₂) :
    closedStringMassSq n₁ ≤ closedStringMassSq n₂ := by
  unfold closedStringMassSq
  omega

end Oasis.StringTheory
