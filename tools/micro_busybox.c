#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("🐧 [OASIS MICRO-BOX C99]: Comandos disponibles: uname, free, ls, cat\n");
        return 0;
    }
    if (strcmp(argv[1], "uname") == 0) {
        printf("Linux oasis-hurd 6.1.0-tinycore-wasm #1 SMP PREEMPT C99 i486 GNU/Linux\n");
    } else if (strcmp(argv[1], "free") == 0) {
        printf("              total        used        free      shared  buff/cache   available\n");
        printf("Mem:          64000        8420       55580           0        1200       54380\n");
        printf("Swap:             0           0           0\n");
    } else if (strcmp(argv[1], "cat") == 0 && argc > 2) {
        FILE *f = fopen(argv[2], "r");
        if (!f) { perror("cat"); return 1; }
        char buf[256];
        while (fgets(buf, sizeof(buf), f)) printf("%s", buf);
        fclose(f);
    } else {
        printf("microbox: comando '%s' reconocido en Capa 0.\n", argv[1]);
    }
    return 0;
}
