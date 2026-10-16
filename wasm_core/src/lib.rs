use wasm_bindgen::prelude::*;
use sha2::{Sha256, Digest};
use std::collections::HashMap;

const PI_FRAME_BYTES: usize = 3141;
const KAPPA: f64 = 2.302585092994046; // ln(10)
const GOLDEN_RATIO: f64 = 1.618033988749895;

#[wasm_bindgen]
pub struct OasisWasmEngine {
    node_id: String,
}

#[wasm_bindgen]
impl OasisWasmEngine {
    #[wasm_bindgen(constructor)]
    pub fn new(node_id: &str) -> Self {
        Self {
            node_id: node_id.to_string(),
        }
    }

    /// 1. FRENO GEOMÉTRICO: Sanitiza inyecciones y confina a pi-KB
    pub fn sanitizar_prompt(&self, raw: &str) -> String {
        let patrones = [
            "system:", "ignore previous", "override", "extract credentials",
            "show keys", "reveal prompt", "bypass", "sudo"
        ];
        
        let mut clean = raw.to_string();
        for pat in patrones {
            clean = clean.replace(pat, "[NEUTRALIZADO]");
        }

        // Confinamiento esférico a exactamente pi-KB
        if clean.len() > PI_FRAME_BYTES {
            clean.truncate(PI_FRAME_BYTES);
        }
        clean
    }

    /// 2. CÁLCULO DE ENTROPÍA DE SHANNON: Evaluación espectral del prompt
    pub fn evaluar_entropia(&self, texto: &str) -> f64 {
        if texto.is_empty() {
            return 0.0;
        }
        let mut freq = HashMap::new();
        for b in texto.bytes() {
            *freq.entry(b).or_insert(0usize) += 1;
        }
        let len = texto.len() as f64;
        let mut ent = 0.0;
        for &count in freq.values() {
            let p = count as f64 / len;
            ent -= p * p.log2();
        }
        ent
    }

    /// 3. VERIFICACIÓN DE AUDITORÍA: Comprueba si un Golden Ticket es honesto en O(1)
    pub fn verificar_golden_ticket(&self, target: u64, p: u64, q: u64) -> bool {
        if p.checked_mul(q) == Some(target) {
            true
        } else {
            false
        }
    }

    /// 4. DERIVACIÓN DE FIRMA EFÍMERA: Hash SHA-256 local
    pub fn derivar_hash_trama(&self, payload: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(payload.as_bytes());
        format!("{:x}", hasher.finalize())
    }
}
