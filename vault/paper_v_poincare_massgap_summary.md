# Nota Metodológica — Enlace de Síntesis y Cota Condicional (Lean 4.36.0)

## Alcance y Honestidad Científica
- Este registro documenta la formalización en **Lean 4.36.0 puro** (`0 errors, 0 warnings, 0 sorry`, sin axiomas personalizados) de la consistencia lógica de cotas escaladas (`10⁻³`) al enlazar el certificado de síntesis de las Sub-fases 1–5 con la deducción condicional de cota de decaimiento a partir de una cota inferior de brecha/Poincaré (`formal_proofs/Subphase6_Poincare_MassGap_Bridge.lean` y `formal_proofs/poincare_to_massgap.lean`).
- **Qué queda demostrado en Lean:** la implicación deductiva entre hipótesis explícitas de cotas y las cotas resultantes de positividad, decaimiento acotado y separación frente al baseline gaussiano libre (`0`).
- **Qué queda como trabajo analítico abierto (fuera del alcance de estas pruebas):** la demostración incondicional de desigualdades funcionales de Poincaré/log-Sobolev en el continuo, la compacidad/tightness en espacios de distribuciones sobre $\mathbb{R}^4$ y la existencia rigurosa con brecha de masa $\Delta > 0$ para Yang–Mills.

## Archivos Verificados en Este Enlace
- `formal_proofs/poincare_to_massgap.lean`
- `formal_proofs/Subphase5_Global_Synthesis_Spec.lean`
- `formal_proofs/Subphase6_Poincare_MassGap_Bridge.lean`
