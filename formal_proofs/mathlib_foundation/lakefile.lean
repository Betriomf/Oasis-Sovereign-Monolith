import Lake
open Lake DSL

package «oasis_mathlib_foundation» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.36.0"

@[default_target]
lean_lib «OasisMathlib» where
  globs := #[.submodules `OasisMathlib]
