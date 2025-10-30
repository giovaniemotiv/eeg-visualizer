from __future__ import annotations
from typing import List, Tuple

def restrict_interval(total: float, start: float, end: float) -> tuple[float, float]:
    start = max(0.0, min(start, total))
    end = max(0.0, min(end, total))
    if end <= start:
        end = min(total, start + 0.25)
    return start, end

def sliding_windows(start: float, end: float, win: float, step: float):
    t = start
    while t + win <= end + 1e-9:
        yield (t, t+win)
        t += step
