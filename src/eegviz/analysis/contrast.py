from __future__ import annotations
import numpy as np
import mne
from .psd import bandpower_segment

def mean_band_over_intervals(raw: mne.io.BaseRaw, intervals, fmin: float, fmax: float, picks=None):
    vals = []
    for o, d in intervals:
        seg = raw.copy().crop(tmin=o, tmax=o+d)
        vals.append(bandpower_segment(seg, fmin, fmax, picks))
    if not vals:
        return None
    return np.mean(np.vstack(vals), axis=0)

def contrast_db(Pb: np.ndarray, Pa: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10((Pb + 1e-20) / (Pa + 1e-20))
