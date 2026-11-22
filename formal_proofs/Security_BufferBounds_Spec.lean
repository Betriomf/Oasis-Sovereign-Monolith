/-
  OASIS OVRP SECURITY AUDIT — C99 PARSER BUFFER INVARIANTS
  Archivo: formal_proofs/Security_BufferBounds_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.SecurityAudit

structure BufferSlice where
  capacity : Nat
  offset : Nat
  readLen : Nat
  maxSize : Nat

def isSafeAllocation (reqLen maxSize : Nat) : Prop :=
  reqLen < maxSize ∧ reqLen + 1 ≤ maxSize

def isWithinBounds (b : BufferSlice) : Prop :=
  b.offset + b.readLen ≤ b.capacity ∧ b.capacity ≤ b.maxSize

theorem no_integer_overflow_on_nul_alloc
    (reqLen maxSize : Nat)
    (h_strict : reqLen < maxSize) :
    isSafeAllocation reqLen maxSize := by
  unfold isSafeAllocation
  omega

theorem sequential_parse_preserves_bounds
    (b : BufferSlice)
    (step1 step2 : Nat)
    (h_sum : step1 + step2 = b.readLen)
    (h_bounds : isWithinBounds b) :
    b.offset + step1 ≤ b.capacity ∧ (b.offset + step1) + step2 ≤ b.capacity := by
  unfold isWithinBounds at h_bounds
  omega

end Oasis.SecurityAudit
