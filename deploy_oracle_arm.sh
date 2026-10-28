#!/usr/bin/env bash
set -e

echo "🚀 [OCI PROVISIONER]: Creando instancia ARM Ampere A1 (24GB RAM)..."

# Obtener variables de entorno configuradas en oci setup
COMPARTMENT_ID=$(oci iam compartment list --query "data[0].id" --raw-output)
AD_NAME=$(oci iam availability-domain list --query "data[0].name" --raw-output)

# Imagen Ubuntu 24.04 aarch64
IMAGE_ID=$(oci compute image list --compartment-id "$COMPARTMENT_ID" \
  --operating-system "Canonical Ubuntu" \
  --operating-system-version "24.04" \
  --shape "VM.Standard.A1.Flex" \
  --query "data[0].id" --raw-output)

# Obtener primera Subnet pública de la VCN predeterminada
SUBNET_ID=$(oci network subnet list --compartment-id "$COMPARTMENT_ID" --query "data[0].id" --raw-output)

# Lanzar la máquina con 4 OCPUs y 24 GB de RAM
oci compute instance launch \
  --availability-domain "$AD_NAME" \
  --compartment-id "$COMPARTMENT_ID" \
  --shape "VM.Standard.A1.Flex" \
  --shape-config '{"ocpus": 4, "memoryInGBs": 24}' \
  --display-name "Oasis-Aether-Node-01" \
  --image-id "$IMAGE_ID" \
  --subnet-id "$SUBNET_ID" \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
  --wait-for-state RUNNING

echo "✅ Instancia desplegada con éxito."
