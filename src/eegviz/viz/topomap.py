from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib as mpl
import mne
from ..config import SPHERE

def topomap_from_bandpower(bp, info, *, vmin=None, vmax=None, cmap="RdBu_r", title=None):
    if vmin is None or vmax is None or vmin >= vmax:
        vmin = float(bp.min()); vmax = float(bp.max())
        if vmin == vmax:
            vmin -= 1e-12; vmax += 1e-12
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    fig, ax = plt.subplots(figsize=(4.2, 4.6), dpi=140)
    mne.viz.plot_topomap(bp, info, ch_type='eeg',
                         sphere=SPHERE, outlines='head', contours=6,
                         cmap=cmap, cnorm=norm, sensors=False, axes=ax)
    if title:
        ax.set_title(title)
    return fig
