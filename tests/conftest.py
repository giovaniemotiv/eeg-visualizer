import numpy as np
import mne
import pytest

@pytest.fixture
def make_raw_sine():
    def _mk(freq=10.0, sfreq=256.0, secs=5.0, n_ch=6):
        t = np.arange(int(sfreq*secs)) / sfreq
        data = np.array([np.sin(2*np.pi*freq*t) for _ in range(n_ch)])
        info = mne.create_info([f"CH{i+1}" for i in range(n_ch)], sfreq, ch_types="eeg")
        raw = mne.io.RawArray(data, info)
        return raw
    return _mk
