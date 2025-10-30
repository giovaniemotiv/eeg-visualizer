from __future__ import annotations
import numpy as np

REGIONS = {
    "Frontal":      ["AF3","AF4","F3","F4","F7","F8"],
    "Frontocentral":["FC5","FC6"],
    "Temporal":     ["T7","T8"],
    "Parietal":     ["P7","P8"],
    "Occipital":    ["O1","O2"],
}

def region_means(ch_names, values):
    name_to_idx = {ch:i for i,ch in enumerate(ch_names)}
    out = []
    for reg,chs in REGIONS.items():
        idxs = [name_to_idx[c] for c in chs if c in name_to_idx]
        if idxs:
            out.append((reg, float(np.mean([values[i] for i in idxs]))))
    return sorted(out, key=lambda x: x[0])
