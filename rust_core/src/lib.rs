#[inline(always)]
pub fn validar_golod(r: i32, d: i32) -> bool {
    r > ((d * d) >> 2)
}

#[no_mangle]
pub extern "C" fn validar_golod_rust(r: i32, d: i32) -> i32 {
    if validar_golod(r, d) { 1 } else { 0 }
}
