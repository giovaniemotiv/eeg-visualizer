from __future__ import annotations
from pathlib import Path
import mne

def save_fif_bytes(raw: mne.io.BaseRaw) -> bytes:
    tmp = Path(mne.utils._TempDir()) / "proc_raw.fif"  # type: ignore
    raw.save(str(tmp), overwrite=True)
    return tmp.read_bytes()

def save_edf_bytes(raw: mne.io.BaseRaw) -> bytes:
    try:
        from mne.export import export_raw
        tmp = Path(mne.utils._TempDir()) / "proc_raw.edf"  # type: ignore
        export_raw(str(tmp), raw, fmt="edf", overwrite=True)
        return tmp.read_bytes()
    except Exception as e:
        raise RuntimeError(f"EDF export failed: {e}")
