from __future__ import annotations
import numpy as np
import mne

def bandpower_mean(raw: mne.io.BaseRaw, fmin: float, fmax: float, picks=None) -> np.ndarray:
    nfft = int(min(512, raw.n_times)); nfft = max(nfft, 64)
    nover = int(max(0, nfft // 2))
    psd = raw.compute_psd(fmin=fmin, fmax=fmax, picks=picks,
                          n_fft=nfft, n_overlap=nover,
                          reject_by_annotation='omit', verbose=False)
    return psd.get_data().mean(axis=1)
