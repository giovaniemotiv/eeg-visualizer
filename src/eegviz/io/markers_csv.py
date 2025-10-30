import pandas as pd
import mne
from pathlib import Path

def add_csv_markers(raw, csv_path: Path) -> int:
    df = pd.read_csv(csv_path)
    if not {"latency","duration","type"}.issubset(df.columns):
        return 0

    on, du, de = [], [], []
    T = float(raw.times[-1])
    for o, d, lab in zip(df["latency"], df["duration"], df["type"]):
        if d <= 0 or o >= T:
            continue
        end = min(T, o + d); o = max(0.0, o)
        if end - o <= 0:
            continue
        on.append(float(o)); du.append(float(end - o)); de.append(str(lab))

    if not on: return 0
    ann = mne.Annotations(on, du, de, orig_time=raw.annotations.orig_time)
    raw.set_annotations(raw.annotations + ann)
    return len(on)
