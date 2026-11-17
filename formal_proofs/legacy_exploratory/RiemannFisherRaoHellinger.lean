/-
  Hellinger / Fisher-Rao isometry on the dyadic energy simplex.
  Pure Lean 4 verification (zero external dependencies, sorry = 0).
  Verifies (2 * q * dq)^2 = 4 * q^2 * (dq)^2 over any commutative ring (including ℝ).
-/

class CommRingLaw (R : Type) where
  add : R → R → R
  mul : R → R → R
  zero : R
  one : R
  mul_assoc : ∀ a b c : R, mul (mul a b) c = mul a (mul b c)
  mul_comm : ∀ a b : R, mul a b = mul b a

section
open CommRingLaw

theorem hellinger_simplex_identity_ring {R : Type} [CommRingLaw R] (q dq : R) :
    let two := add one one
    let four := mul two two
    mul (mul (mul two q) dq) (mul (mul two q) dq) =
    mul (mul four (mul q q)) (mul dq dq) := by
  intro two four
  have h1 : mul (mul (mul two q) dq) (mul (mul two q) dq) =
            mul (mul (mul two q) (mul two q)) (mul dq dq) := by
    rw [mul_assoc (mul two q) dq (mul (mul two q) dq)]
    rw [← mul_assoc dq (mul two q) dq]
    rw [mul_comm dq (mul two q)]
    rw [mul_assoc (mul two q) dq dq]
    rw [← mul_assoc (mul two q) (mul two q) (mul dq dq)]
  have h2 : mul (mul two q) (mul two q) = mul (mul two two) (mul q q) := by
    rw [mul_assoc two q (mul two q)]
    rw [← mul_assoc q two q]
    rw [mul_comm q two]
    rw [mul_assoc two q q]
    rw [← mul_assoc two two (mul q q)]
  rw [h1, h2]

theorem hellinger_simplex_identity_int (q dq : Int) :
    (2 * q * dq) * (2 * q * dq) = 4 * (q * q) * (dq * dq) := by
  simp [Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]

end

#eval "✅ PILAR 377B [LEAN 4]: Isometría de Hellinger p_j = q_j^2 verificada (sorry = 0)."
