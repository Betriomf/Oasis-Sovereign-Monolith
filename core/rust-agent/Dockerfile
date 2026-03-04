# =====================================================================
# 🏛️ OASIS SOBERANO: DOCKERFILE FRACTAL (Optimización Landauer)
# =====================================================================

# --- ETAPA 1: EL REACTOR (Compilación en Alpine) ---
FROM rust:alpine AS builder
RUN apk add --no-cache musl-dev build-base
WORKDIR /app

# Copiamos los archivos del proyecto Rust que ya tenemos
COPY Cargo.toml ./
# Si no existe la carpeta src, el comando dará error, asegúrate de estar en core/rust-agent
COPY src ./src

# Compilación estática pura (musl)
RUN RUSTFLAGS='-C target-feature=+crt-static' cargo build --release --target x86_64-unknown-linux-musl

# --- ETAPA 2: EL VACÍO CUÁNTICO (Imagen Final) ---
FROM scratch

# Constantes físicas de la Bóveda Oasis
ENV OASIS_PHI_INCREMENT="1.6180339887"
ENV OASIS_REYNOLDS_ATTRACTOR="2.3"
ENV OASIS_BLACK_CIRCLE_SIGMA="5.67e-8"

# Traemos el binario puro. Pesará ~5MB.
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/oasis-dc-agent /oasis-daemon

ENTRYPOINT ["/oasis-daemon"]
