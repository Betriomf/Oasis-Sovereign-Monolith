-- OASIS SOVEREIGN MONOLITH — SUPABASE PGVECTOR SCHEMA (Fase 4)
-- Habilita la extensión vectorial en PostgreSQL
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla de tramas Lincos con embedding vectorial de baja entropía
CREATE TABLE IF NOT EXISTS lincos_vectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lincos_header TEXT NOT NULL,
    source_label TEXT NOT NULL,
    payload TEXT NOT NULL,
    landauer_entropy FLOAT NOT NULL,
    target_kb FLOAT DEFAULT 3.14159265,
    embedding VECTOR(384), -- Dimensiones para embeddings ligeros
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice IVFFlat para búsquedas en tiempo real en régimen laminar
CREATE INDEX IF NOT EXISTS lincos_vectors_embedding_idx 
ON lincos_vectors USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
