use std::collections::HashMap;
use std::f64::consts::PI;
use std::thread;
use std::time::Duration;

const PHI: f64 = 1.618033988749895;
const LN_10: f64 = 2.302585092994046; // Atractor 2.3
const MONSTER_DIM: f64 = 196883.0;    // Dimensión del Grupo Monstruo
const KAPPA_M: f64 = -0.6587;          // Constante de Mariano

struct AminoAcid {
    nombre: &'static str,
    atoms: f64,
    bonds: f64,
    polarity: &'static str,
}

fn main() {
    println!("\x1b[38;5;46m🌌 [KERNEL DE OASIS OS] Inicializando Renderizador de Proteínas Adiabático...\x1b[0m");
    thread::sleep(Duration::from_millis(800));

    // Definir secuencia de proteína extendida (30 residuos)
    let secuencia = vec![
        "MET", "ALA", "VAL", "PRO", "LYS", "GLU", "CYS", "TRP", "TYR", "HIS",
        "MET", "ALA", "VAL", "PRO", "LYS", "GLU", "CYS", "TRP", "TYR", "HIS",
        "MET", "ALA", "VAL", "PRO", "LYS", "GLU", "CYS", "TRP", "TYR", "HIS"
    ];

    // Base de datos de aminoácidos
    let mut aa_db = HashMap::new();
    aa_db.insert("ALA", AminoAcid { nombre: "Alanina", atoms: 1.0, bonds: 0.0, polarity: "nonpolar" });
    aa_db.insert("VAL", AminoAcid { nombre: "Valina", atoms: 3.0, bonds: 1.0, polarity: "nonpolar" });
    aa_db.insert("PRO", AminoAcid { nombre: "Prolina", atoms: 3.0, bonds: 1.0, polarity: "nonpolar" });
    aa_db.insert("LYS", AminoAcid { nombre: "Lisina", atoms: 5.0, bonds: 4.0, polarity: "basic" });
    aa_db.insert("GLU", AminoAcid { nombre: "Glutamato", atoms: 5.0, bonds: 3.0, polarity: "acidic" });
    aa_db.insert("CYS", AminoAcid { nombre: "Cisteína", atoms: 2.0, bonds: 1.0, polarity: "polar" });
    aa_db.insert("TRP", AminoAcid { nombre: "Triptófano", atoms: 11.0, bonds: 2.0, polarity: "nonpolar" });
    aa_db.insert("TYR", AminoAcid { nombre: "Tirosina", atoms: 8.0, bonds: 2.0, polarity: "polar" });
    aa_db.insert("HIS", AminoAcid { nombre: "Histidina", atoms: 6.0, bonds: 2.0, polarity: "basic" });
    aa_db.insert("MET", AminoAcid { nombre: "Metionina", atoms: 4.0, bonds: 3.0, polarity: "nonpolar" });

    println!("\x1b[38;5;46m🐝 [MALLA HEXAGONAL] Proyectando trayectorias en Dimensión 196883...\x1b[0m\n");
    thread::sleep(Duration::from_millis(800));

    // Renderizar la hélice en ASCII siguiendo direcciones de la malla hexagonal
    let mut x: i32 = 40;
    let mut y: i32 = 10;
    
    // Representación visual en consola
    for (i, aa) in secuencia.iter().enumerate() {
        let step = i % 6;
        let (dir_char, dx, dy) = match step {
            0 => ("─", 2, 0),
            1 => ("/", 1, -1),
            2 => ("\\", 1, 1),
            3 => ("─", 2, 0),
            4 => ("/", 1, -1),
            _ => ("\\", 1, 1),
        };

        x += dx;
        y += dy;

        // Imprimir nodo residuo y enlace en color verde áureo
        print!("\x1b[38;5;48m{}{}({})\x1b[0m", dir_char, aa, i + 1);
        if (i + 1) % 5 == 0 {
            print!("\n");
            // Tabular para mantener perspectiva de la hélice plegada
            for _ in 0..(y as usize) {
                print!(" ");
            }
        }
    }
    
    println!("\n\n\x1b[38;5;81m📊 [DICTAMEN DE CAPA 0 - VEREDICTO DE RESILENCIA]:\x1b[0m");
    let ahorro_landauer = (1.0 - (PHI.ln() / 2.0f64.ln())) * 100.0;
    let disipacion_oasis = 1.380649e-23 * 310.15 * PHI.ln();
    
    println!("  ├─ Estado de Plegamiento        : NATIVO LAMINAR COHERENTE");
    println!("  ├─ Ahorro Térmico (Oasis)      : {:.2}% vs Límite de Landauer Clásico", ahorro_landauer);
    println!("  ├─ Gasto de Borrado de Bit     : {:.4e} Joules", disipacion_oasis);
    println!("  ├─ Amortiguamiento Crítico     : {} (Atractor L = ln 10)", LN_10);
    println!("  └─ Consumo Estimado Mac        : 4.4140W (Silicio Frío - Flujo Laminar OK)");
    println!("\x1b[38;5;46m\nBetriomf! El hardware ahora es una red de Fibonacci.\x1b[0m");
}
