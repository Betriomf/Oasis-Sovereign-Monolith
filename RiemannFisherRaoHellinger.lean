import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

namespace Oasis.FisherRao

/-- Pointwise identity behind the Bhattacharyya-Hellinger regularization p_j = q_j^2. -/
theorem hellinger_simplex_identity_real (q dq : ℝ) :
    (2 * q * dq) * (2 * q * dq) = 4 * (q * q) * (dq * dq) := by
  ring

/-- Nonnegativity of the pointwise Fisher-Rao speed term in q-coordinates. -/
theorem fisher_rao_speed_nonneg (q dq : ℝ) :
    0 ≤ 2 * |q * dq| := by
  positivity

end Oasis.FisherRao
