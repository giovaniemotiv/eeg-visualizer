import json
from pathlib import Path
from dateutil import parser as dtparser
import mne

def add_json_markers(raw, json_path: Path) -> int:
    js = json.loads(json_path.read_text(encoding="utf-8"))
    marks = js.get("Markers", [])
    if not marks:
        return 0

    rows = []
    for m in marks:
        s = m.get("startDatetime") or m.get("originalStartDatetime")
        e = m.get("endDatetime") or m.get("originalEndDatetime")
        if not (s and e):
            continue
        sdt, edt = dtparser.isoparse(s), dtparser.isoparse(e)
        rows.append((m.get("label", "Marker"), sdt, edt))
    if not rows: return 0

    durations = [(e - s).total_seconds() for _, s, e in rows]
    descs = [lbl for (lbl, _, _) in rows]

    base_orig = raw.annotations.orig_time
    if base_orig is not None:
        onsets = [(s - base_orig).total_seconds() for _, s, _ in rows]
    else:
        s0 = min(s for _, s, _ in rows)
        onsets = [(s - s0).total_seconds() for _, s, _ in rows]

    T = float(raw.times[-1])
    on, du, de = [], [], []
    for o, d, lab in zip(onsets, durations, descs):
        if d <= 0 or o >= T: continue
        end = min(T, o + d); o = max(0.0, o)
        if end - o <= 0: continue
        on.append(float(o)); du.append(float(end-o)); de.append(lab)

    if not on: return 0
    ann = mne.Annotations(on, du, de, orig_time=base_orig)
    raw.set_annotations(raw.annotations + ann)
    return len(on)
