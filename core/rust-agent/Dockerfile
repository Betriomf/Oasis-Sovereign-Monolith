# ETAPA 1: Compilación (The Forge)
FROM rust:1.75-slim as builder
WORKDIR /usr/src/oasis
COPY . .
RUN cargo build --release

# ETAPA 2: Binario Puro (The Projectile)
# Usamos 'scratch' para que la imagen pese ~5MB
FROM scratch
COPY --from=builder /usr/src/oasis/target/release/oasis-dc-agent /oasis-agent
ENTRYPOINT ["/oasis-agent"]
