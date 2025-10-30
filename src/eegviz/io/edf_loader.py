# src/eegviz/io/edf_loader.py
from __future__ import annotations
from pathlib import Path
import tempfile
import mne

def load_edf(edf_bytes_or_path, base_dir: Path | None = None) -> mne.io.BaseRaw:
    if hasattr(edf_bytes_or_path, "read"):
        data = edf_bytes_or_path.read()
        base = base_dir or Path(tempfile.mkdtemp(prefix="eegviz_"))
        base.mkdir(parents=True, exist_ok=True)
        p = base / "input.edf"
        p.write_bytes(data)
        return mne.io.read_raw_edf(str(p), preload=True, verbose=False)
    return mne.io.read_raw_edf(str(edf_bytes_or_path), preload=True, verbose=False)
