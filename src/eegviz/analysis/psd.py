from __future__ import annotations
import mne
import numpy as np

def bandpower_segment(raw_seg: mne.io.BaseRaw, fmin: float, fmax: float, picks=None):
    nfft = int(min(512, raw_seg.n_times)); nfft = max(nfft, 64)
    nover = int(max(0, nfft // 2))
    psd = raw_seg.compute_psd(fmin=fmin, fmax=fmax, picks=picks,
                              n_fft=nfft, n_overlap=nover,
                              reject_by_annotation='omit', verbose=False)
    return psd.get_data().mean(axis=1)
