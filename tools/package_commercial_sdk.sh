#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

VERSION="v20.0.5"
PKG_NAME="Oasis-Capa0-Commercial-SDK-${VERSION}"
DIST_DIR="$DIR/dist/$PKG_NAME"

if grep -rn "sorry" *.lean >/dev/null 2>&1; then
    echo "❌ ERROR: Se detectó 'sorry' en teoremas formales."
    exit 1
fi

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/src_c99" "$DIST_DIR/bin_darwin_arm64" "$DIST_DIR/formal_proofs_lean4" "$DIST_DIR/legal_attestations"

clang -O3 -std=c99 -Wall -Wextra -fomit-frame-pointer \
      -o "$DIST_DIR/bin_darwin_arm64/oasis_kernel_filter" \
      tools/oasis_minkowski_filter.c

cp tools/oasis_minkowski_filter.c "$DIST_DIR/src_c99/"
cp *.lean "$DIST_DIR/formal_proofs_lean4/"
cp COMMERCIAL_LICENSE.md LICENSE AUTHORS.md "$DIST_DIR/legal_attestations/"
cp vault/bitcoin_ots_manifest.json vault/zenodo_deposition_receipt.json tools/oasis_minkowski_filter.c.ots "$DIST_DIR/legal_attestations/"

cd "$DIR/dist"
find "$PKG_NAME" -type f -exec shasum -a 256 {} + > "$PKG_NAME/SHA256SUMS.txt"
tar -czf "${PKG_NAME}.tar.gz" "$PKG_NAME"

echo "✅ SDK Comercial listo: dist/${PKG_NAME}.tar.gz"
echo "✅ SHA-256 Maestro   : $(shasum -a 256 "${PKG_NAME}.tar.gz" | awk '{print $1}')"
