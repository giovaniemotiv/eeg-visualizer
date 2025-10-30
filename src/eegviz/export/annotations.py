from __future__ import annotations
import pandas as pd
import mne

def annotations_to_csv_bytes(ann: mne.Annotations) -> bytes:
    if len(ann) == 0:
        return b""
    df = pd.DataFrame({
        "onset_s": ann.onset,
        "duration_s": ann.duration,
        "label": ann.description,
    })
    return df.to_csv(index=False).encode("utf-8")
