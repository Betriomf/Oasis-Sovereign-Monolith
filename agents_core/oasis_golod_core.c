#include <stdint.h>

// Función exportada en C puro para ctypes
int32_t validar_golod_c(int32_t r, int32_t d) {
    return (r > ((d * d) >> 2)) ? 1 : 0;
}
