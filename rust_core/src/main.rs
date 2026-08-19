use std::time::Instant;

#[inline(always)]
fn validar_golod(r: i32, d: i32) -> bool {
    r > ((d * d) >> 2)
}

fn main() {
    let total: usize = 1_000_000;
    let d = 6;
    let mut aprobados = 0;

    let start = Instant::now();
    for i in 0..total {
        let r = (i % 16) as i32;
        if validar_golod(r, d) {
            aprobados += 1;
        }
    }
    let duration = start.elapsed();

    println!("===============================================================");
    println!("🦀 [OASIS RUST NATIVE CORE] - Zero-Cost Abstraction Benchmark");
    println!("===============================================================");
    println!("📦 Paquetes evaluados   : {}", total);
    println!("✅ Paquetes válidos (r>=10): {} ({:.2}%)", aprobados, (aprobados as f64 * 100.0) / total as f64);
    println!("⏱️ Tiempo total          : {:?}", duration);
    println!("⚡ Latencia por paquete  : {:.2} ns", (duration.as_nanos() as f64) / total as f64);
    println!("===============================================================");
}
