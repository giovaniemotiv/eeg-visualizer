from __future__ import annotations
import mne

def apply_pipeline(raw: mne.io.BaseRaw, *, notch: float|None, l_freq: float|None, h_freq: float|None,
                   resample: float|None, ref_avg: bool, interpolate: bool=False) -> mne.io.BaseRaw:
    proc = raw.copy()
    if resample and abs(proc.info["sfreq"] - resample) > 1e-6:
        proc.resample(resample)
    if notch is not None:
        proc.notch_filter(freqs=float(notch), picks="eeg", method="spectrum_fit", verbose=False)
    if l_freq is not None or h_freq is not None:
        hf = min(h_freq or (proc.info["sfreq"]/2 - 1.0), proc.info["sfreq"]/2 - 1.0)
        proc.filter(l_freq=l_freq, h_freq=hf, picks="eeg", method="fir", phase="zero",
                    fir_window="hamming", verbose=False)
    if interpolate and proc.info["bads"]:
        proc.interpolate_bads(reset_bads=False, verbose=False)
    if ref_avg:
        proc.set_eeg_reference("average", projection=False)
    return proc
