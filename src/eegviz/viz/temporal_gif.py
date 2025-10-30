from __future__ import annotations
import io
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import matplotlib as mpl
import mne
import numpy as np
from ..config import SPHERE
from ..preprocess.windows import sliding_windows
from ..analysis.psd import bandpower_segment

def build_frames(raw, fmin, fmax, picks, start, end, win_len, step, pmin=5, pmax=95):
    vals, meta = [], []
    if end - start < 0.25:
        return None, None, None
    wins = list(sliding_windows(start, end, win_len, step)) or [(start, end)]
    for a, b in wins:
        seg = raw.copy().crop(tmin=a, tmax=b)
        nfft = int(min(512, seg.n_times))
        if nfft < 32: 
            continue
        bp = bandpower_segment(seg, fmin, fmax, picks)
        if not np.isfinite(bp).all():
            continue
        vals.append(bp); meta.append((a,b))
    if not vals:
        return None, None, None
    frames = np.vstack(vals)
    vmin = float(np.percentile(frames, pmin)); vmax = float(np.percentile(frames, pmax))
    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin >= vmax:
        vmin, vmax = float(frames.min()), float(frames.max())
        if vmin == vmax: vmin -= 1e-12; vmax += 1e-12
    return frames, meta, (vmin, vmax)

def render_gif(raw, frames, meta, vmin, vmax, cmap="RdBu_r", fps=12):
    images = []
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    for (a,b), data in zip(meta, frames):
        fig, ax = plt.subplots(figsize=(3.2, 3.6), dpi=140)
        mne.viz.plot_topomap(data, raw.info, ch_type='eeg',
                             sphere=SPHERE, outlines='head', contours=6,
                             cmap=cmap, cnorm=norm, sensors=False, axes=ax)
        ax.set_title(f"{a:.1f}–{b:.1f}s", fontsize=10)
        fig.tight_layout(pad=0.2)
        buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=140); plt.close(fig); buf.seek(0)
        images.append(imageio.imread(buf)); buf.close()
    gif_buf = io.BytesIO()
    imageio.mimsave(gif_buf, images, duration=1.0/max(1,fps))
    gif_buf.seek(0)
    return gif_buf.getvalue()
