"""
OASIS SOVEREIGN OS — BLACK CIRCLE SCHEDULER (Python Engine)
"""
import math
import random

class BlackCircleScheduler:
    SIGMA = 5.67e-8
    EXPONENT = -2.5

    @classmethod
    def get_fractal_task_size(cls, min_mb: float, max_mb: float) -> float:
        r = random.random()
        return round(min_mb + (max_mb - min_mb) * math.pow(1 - r, 1 / (cls.EXPONENT + 1)), 2)

    @classmethod
    def calculate_barrier_cost(cls, load_mb: float, total_mb: float) -> float:
        r = load_mb / total_mb
        dist = 1.0 - r
        if dist <= 0.001:
            return float("inf")
        return round(1.0 / dist, 4)

    @classmethod
    def schedule(cls, load_mb: float, total_mb: float, temp_c: float) -> dict:
        if temp_c > 80.0:
            return {"status": "THROTTLED", "reason": "THERMAL_LIMIT_EXCEEDED"}
        barrier = cls.calculate_barrier_cost(load_mb, total_mb)
        if math.isinf(barrier):
            return {"status": "BLOCKED", "reason": "COULOMB_BARRIER_BREACH"}
        return {
            "status": "ALLOCATED",
            "task_size_mb": cls.get_fractal_task_size(0.1, total_mb * 0.2),
            "barrier_cost": barrier
        }
