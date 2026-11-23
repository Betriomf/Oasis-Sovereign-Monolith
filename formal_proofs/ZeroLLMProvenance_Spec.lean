/-
  OASIS SOVEREIGN MONOLITH — ZERO-LLM PROVENANCE & DUAL-LICENSE COMPLIANCE SPEC
  Archivo: formal_proofs/ZeroLLMProvenance_Spec.lean
  Lean 4.36.0 puro autocontenido: 0 errors, 0 warnings, 0 sorry, 0 custom axioms.
-/

namespace Oasis.ZeroLLMProvenance

/-- Métricas operacionales de una auditoría OVRP en hardware ligero. -/
structure AuditEnvelope where
  latencyMicros : Nat
  maxLatencyMicros : Nat
  llmInferenceCalls : Nat
  hasSha256AndOts : Bool
  deriving DecidableEq, Repr

/-- Condición de auditoría soberana válida: latencia dentro de umbral,
    0 llamadas LLM y sello criptográfico presente. -/
def isValidSovereignAudit (e : AuditEnvelope) : Prop :=
  e.latencyMicros ≤ e.maxLatencyMicros ∧
  e.llmInferenceCalls = 0 ∧
  e.hasSha256AndOts = true

/-- Si se optimiza la latencia manteniendo 0 llamadas LLM y el sello activo,
    la validez de la auditoría soberana se preserva. -/
theorem faster_audit_preserves_validity
    (e : AuditEnvelope) (newLatency : Nat)
    (h_valid : isValidSovereignAudit e)
    (h_faster : newLatency ≤ e.latencyMicros) :
    isValidSovereignAudit { e with latencyMicros := newLatency } := by
  simp only [isValidSovereignAudit] at h_valid ⊢
  refine ⟨?_, h_valid.2.1, h_valid.2.2⟩
  omega

end Oasis.ZeroLLMProvenance
