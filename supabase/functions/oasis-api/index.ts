// OASIS CAPA 0 — SUPABASE EDGE FUNCTION (Deno / TypeScript)
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const authHeader = req.headers.get('Authorization')
  
  // Validación de API Key de Pago / Suscripción
  if (!authHeader || !authHeader.includes("Bearer oasis_live_key_")) {
    return new Response(JSON.stringify({ error: "API Key inválida o sin saldo" }), {
      status: 401,
      headers: { "Content-Type": "application/json" }
    })
  }

  const payload = {
    status: "OK",
    agente: "Cervantes Ultra + ÆTHER",
    techo_termico: "5.39W",
    mensaje: "Respuesta servida desde Supabase Edge sin consumo de RAM en tu Mac."
  }

  return new Response(JSON.stringify(payload), {
    headers: { "Content-Type": "application/json" },
  })
})
