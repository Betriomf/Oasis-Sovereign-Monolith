FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Instalar dependencias esenciales, ttyd, Nginx y Python
RUN apt-get update && apt-get install -y \
    ttyd \
    nginx \
    python3 \
    python3-pip \
    bash \
    git \
    curl \
    htop \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el código del repositorio
COPY . /app

# Copiar configuración de Nginx y script de entrada
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

CMD ["/app/entrypoint.sh"]
