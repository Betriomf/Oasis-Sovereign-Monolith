-- TABLA DE GESTIÓN MODULAR DE WIDGETS OASIS OS (SUPABASE)
CREATE TABLE IF NOT EXISTS public.oasis_modules (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL DEFAULT 'v1.0.0',
    enabled BOOLEAN NOT NULL DEFAULT true,
    bundle_url TEXT,
    api_endpoint TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Habilitar lectura pública (Row Level Security)
ALTER TABLE public.oasis_modules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Access" ON public.oasis_modules FOR SELECT USING (true);

-- Insertar módulos base de Oasis
INSERT INTO public.oasis_modules (id, name, version, enabled, bundle_url, api_endpoint)
VALUES 
    ('mesh3d', 'Visor 3D WebGL VMR', 'v17.0.0', true, '/static/js/mesh_viewer_3d.js', '/v1/med/mesh-geometry'),
    ('demon', 'Demonio Maxwell-Landauer', 'v17.0.0', true, NULL, '/v1/math/demon'),
    ('hemo', 'Hemodinámica Besov 3D', 'v17.0.0', true, NULL, '/v1/med/besov-cfd'),
    ('gutenberg', 'Project Gutenberg RAG', 'v17.0.0', true, NULL, '/v1/gutenberg/book')
ON CONFLICT (id) DO UPDATE SET enabled = EXCLUDED.enabled;
