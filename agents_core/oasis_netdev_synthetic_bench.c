#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

// 1. Invariante OGSP en O(1)
static inline int xdp_oasis_filter(uint32_t signatures, uint32_t degree) {
    return signatures > ((degree * degree) >> 2);
}

// 2. Simulación de procesamiento clásico (Naive Flood)
static inline int naive_flood_process(uint32_t signatures) {
    int sum = 0;
    for (uint32_t i = 0; i < signatures; i++) {
        sum += (i ^ 0xA5); // Simula coste de parseo y firma
    }
    return sum;
}

int main(int argc, char *argv[]) {
    uint32_t total_packets = (argc > 1) ? atoi(argv[1]) : 10000000;
    uint32_t degree = 6;
    uint32_t dropped = 0, forwarded = 0;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (uint32_t i = 0; i < total_packets; i++) {
        uint32_t sigs = i % 16;
        if (xdp_oasis_filter(sigs, degree)) {
            naive_flood_process(sigs);
            forwarded++;
        } else {
            dropped++; // Descarte inmediato en cable O(1)
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;
    double mpps = (total_packets / (elapsed_ms / 1000.0)) / 1000000.0;

    printf("===============================================================\n");
    printf("🐧 [NETDEV KERNEL BENCHMARK] - Synthetic Saturation Test\n");
    printf("===============================================================\n");
    printf("📦 Total Packets Injected : %u\n", total_packets);
    printf("🚀 Throughput             : %.2f Mpps (Million packets/sec)\n", mpps);
    printf("⏱️ Total Execution Time   : %.2f ms\n", elapsed_ms);
    printf("⚡ Avg Latency per Packet : %.2f ns\n", (elapsed_ms / total_packets) * 1000000.0);
    printf("🚫 Wire-Level Drop Rate   : %.2f%% (Spam / Echo Suppression)\n", (dropped * 100.0) / total_packets);
    printf("===============================================================\n");
    return 0;
}
