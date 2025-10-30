from __future__ import annotations
import matplotlib.pyplot as plt

def psd_multi(freqs, psd_data, ch_names, show_legend=False):
    fig, ax = plt.subplots(figsize=(7,4), dpi=140)
    for ch_idx, ch_name in enumerate(ch_names):
        ax.plot(freqs, psd_data[ch_idx], alpha=0.7, label=ch_name)
    ax.set_xlabel("Hz"); ax.set_ylabel("PSD"); ax.grid(alpha=0.3)
    ax.set_title("Welch PSD per channel")
    if show_legend: ax.legend(ncol=2, fontsize=8)
    fig.tight_layout()
    return fig
