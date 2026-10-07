export class BlackCircleScheduler {
  private static readonly SIGMA = 5.67e-8;
  private static readonly EXPONENT = -2.5;

  static getFractalTaskSize(minMB: number, maxMB: number): number {
    const r = Math.random();
    return parseFloat((minMB + (maxMB - minMB) * Math.pow(1 - r, 1 / (this.EXPONENT + 1))).toFixed(2));
  }

  static calculateBarrierCost(loadMB: number, totalMB: number): number {
    const r = loadMB / totalMB;
    const dist = 1.0 - r;
    return dist <= 0.001 ? Infinity : parseFloat((1.0 / dist).toFixed(4));
  }

  static schedule(loadMB: number, totalMB: number, tempC: number) {
    if (tempC > 80.0) return { status: "THROTTLED", reason: "THERMAL_LIMIT_EXCEEDED" };
    const barrier = this.calculateBarrierCost(loadMB, totalMB);
    if (!isFinite(barrier)) return { status: "BLOCKED", reason: "COULOMB_BARRIER_BREACH" };
    return { status: "ALLOCATED", taskSizeMB: this.getFractalTaskSize(0.1, totalMB * 0.2), barrierCost: barrier };
  }
}
