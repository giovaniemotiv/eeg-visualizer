from __future__ import annotations
import mne
from typing import List, Sequence

def normalize_names(raw: mne.io.BaseRaw) -> None:
    def _clean(n: str) -> str:
        n = n.upper().strip()
        for junk in ["EEG ", "EEG.", "EEG_", "CHAN ", "CHAN.", " "]:
            n = n.replace(junk, "")
        return n
    mne.channels.rename_channels(raw.info, {ch: _clean(ch) for ch in raw.ch_names})

def pick_and_mark(raw, kept, bads):
    if set(kept) != set(raw.ch_names):
        raw.pick(kept)   # instead of pick_channels
    raw.info["bads"] = list(bads)

def set_montage(raw: mne.io.BaseRaw, name: str = "standard_1020") -> None:
    mont = mne.channels.make_standard_montage(name)
    raw.set_montage(mont, match_case=False, on_missing="ignore")
