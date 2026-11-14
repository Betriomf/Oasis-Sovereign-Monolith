FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=2 \
    PORT=7860

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && \
    gcc -O3 -std=c99 -fomit-frame-pointer tools/oasis_minkowski_filter.c -o tools/oasis_kernel_filter || true && \
    apt-get purge -y gcc libc6-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

EXPOSE 7860 8080
CMD ["python3", "-u", "agents_core/oasis_render_gateway.py"]
