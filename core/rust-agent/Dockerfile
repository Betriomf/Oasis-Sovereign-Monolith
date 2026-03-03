# STAGE 1: Compilación en Acero Nuclear
FROM rust:1.75-slim as builder
WORKDIR /usr/src/oasis
COPY . .
RUN cargo build --release

# STAGE 2: Imagen Final Ultraligera (5MB)
FROM scratch
COPY --from=builder /usr/src/oasis/target/release/oasis-dc-agent /oasis-agent
ENTRYPOINT ["/oasis-agent"]
