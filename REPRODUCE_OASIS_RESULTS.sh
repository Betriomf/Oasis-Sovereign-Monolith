#!/bin/bash
echo "===================================================="
echo "    OASIS INDEPENDENT REPRODUCIBILITY PROTOCOL"
echo "===================================================="
echo " FASE I: Verificando Constante κ ≈ 2.3..."
python3 scripts/validation/oasis_document_entropy.py
echo " FASE II: Validando Convergencia de Hubble..."
python3 hubble_oasis_unifier.py
echo " FASE III: Test de Inmunidad al Jitter..."
python3 hubble_euclid_stress_test.py
echo "===================================================="
