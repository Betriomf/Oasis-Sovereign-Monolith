import Lake
open Lake DSL

package «oasis-monolith» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib «OasisMath» where
  srcDir := "."
  roots := #[`KozonoTaniuchiLogBound, `BonyCommutatorDyadic]
