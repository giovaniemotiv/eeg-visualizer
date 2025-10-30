"""Comprehensive visualization panel component with all visualization types."""

from __future__ import annotations
import streamlit as st
import mne
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import io
from typing import Optional, List, Dict, Any, Tuple
from mne.time_frequency import tfr_morlet

from ..config import BANDS, SPHERE
from ..core.epochs import EpochManager
from ..analysis.bands import bandpower_mean
from ..analysis.contrast import mean_band_over_intervals, contrast_db
from ..viz.topomap import topomap_from_bandpower
from ..viz.psd_plot import psd_multi
from ..viz.temporal_gif import build_frames, render_gif
from ..viz.regional import region_means
from ..preprocess.windows import restrict_interval


class VisualizationPanelComponent:
    """Manages all visualization types in a unified interface."""
    
    def __init__(self):
        self.epoch_manager = EpochManager()
        self.current_visualization = None
    
    def render_visualization_panel(
        self, 
        processed_raw: mne.io.BaseRaw, 
        start_sec: float, 
        end_sec: float,
        picks
    ) -> None:
        """Render the main visualization panel.
        
        Args:
            processed_raw: Processed MNE Raw object
            start_sec: Start time of current window
            end_sec: End time of current window
            picks: Channel picks for analysis
        """
        st.header("📊 Visualizations")
        
        # Get available annotation labels
        labels = sorted(set(processed_raw.annotations.description)) if len(processed_raw.annotations) else []
        
        # Visualization type selection
        vis_type = st.selectbox(
            "Choose visualization type",
            options=[
                "Topomap (single frame)",
                "Contrast (dB) between conditions", 
                "Temporal GIF animation",
                "Regional bar charts",
                "Power Spectral Density (PSD)",
                "Raw time series preview",
                "Event-Related Potentials (ERP)",
                "Time-Frequency Analysis (TFR)",
            ],
            index=0,
            help="Select the type of visualization to generate"
        )
        
        # Render the selected visualization
        if vis_type == "Topomap (single frame)":
            fig = self._render_topomap(processed_raw, start_sec, end_sec, picks)
        elif vis_type == "Contrast (dB) between conditions":
            fig = self._render_contrast(processed_raw, start_sec, end_sec, picks, labels)
        elif vis_type == "Temporal GIF animation":
            fig = self._render_temporal_gif(processed_raw, start_sec, end_sec, picks)
        elif vis_type == "Regional bar charts":
            fig = self._render_regional_bars(processed_raw, start_sec, end_sec, picks)
        elif vis_type == "Power Spectral Density (PSD)":
            fig = self._render_psd(processed_raw, start_sec, end_sec, picks)
        elif vis_type == "Raw time series preview":
            fig = self._render_raw_preview(processed_raw, start_sec, end_sec)
        elif vis_type == "Event-Related Potentials (ERP)":
            fig = self._render_erp(processed_raw, labels, picks)
        elif vis_type == "Time-Frequency Analysis (TFR)":
            fig = self._render_tfr(processed_raw, labels, picks)
        else:
            fig = None
            st.info("Select a visualization type to begin")
        
        # Store current visualization for potential download
        self.current_visualization = {"type": vis_type, "figure": fig}
    
    def _render_topomap(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> Optional[plt.Figure]:
        """Render single-frame topomap visualization."""
        st.subheader("🗺️ Topomap Visualization")
        
        # Parameters
        col1, col2 = st.columns(2)
        with col1:
            band_name = st.selectbox("Frequency band", list(BANDS.keys()), index=2, key="topo_band")
        with col2:
            center = st.slider(
                "Center time (s)",
                start_sec, end_sec,
                value=start_sec + (end_sec - start_sec) / 2,
                step=0.1,
                key="topo_center"
            )
        
        # Calculate window around center
        window_size = st.slider("Window size (s)", 0.5, 5.0, 2.0, 0.5, key="topo_window")
        a = max(start_sec, center - window_size/2)
        b = min(end_sec, center + window_size/2)
        
        try:
            # Extract data and compute band power
            fmin, fmax = BANDS[band_name]
            seg = raw.copy().crop(tmin=a, tmax=b)
            bp = bandpower_mean(seg, fmin, fmax, picks=picks)
            
            # Create topomap
            vmin = float(np.percentile(bp, 5))
            vmax = float(np.percentile(bp, 95))
            if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin >= vmax:
                vmin, vmax = float(bp.min()), float(bp.max())
                if vmin == vmax:
                    vmin -= 1e-12
                    vmax += 1e-12
            
            fig = topomap_from_bandpower(
                bp, raw.info,
                vmin=vmin, vmax=vmax,
                title=f"{band_name} Power ({a:.1f}-{b:.1f}s)"
            )
            
            st.pyplot(fig)
            return fig
            
        except Exception as e:
            st.error(f"Failed to create topomap: {str(e)}")
            return None
    
    def _render_contrast(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks, labels: List[str]) -> Optional[plt.Figure]:
        """Render contrast analysis between two conditions."""
        st.subheader("⚖️ Condition Contrast Analysis")
        
        if len(labels) < 2:
            st.warning("Need at least 2 annotation labels for contrast analysis")
            st.info("Contrast analysis compares band power between different experimental conditions")
            return None
        
        # Parameters
        col1, col2, col3 = st.columns(3)
        with col1:
            band_name = st.selectbox("Frequency band", list(BANDS.keys()), index=2, key="contrast_band")
        with col2:
            condition_a = st.selectbox("Condition A", labels, key="condition_a")
        with col3:
            condition_b = st.selectbox("Condition B", [l for l in labels if l != condition_a], key="condition_b")
        
        try:
            fmin, fmax = BANDS[band_name]
            
            # Collect intervals for each condition within the selected time window
            intervals_a, intervals_b = [], []
            for onset, duration, label in zip(raw.annotations.onset, raw.annotations.duration, raw.annotations.description):
                start, end = float(onset), float(onset + duration)
                
                # Skip if outside time window
                if end <= start_sec or start >= end_sec:
                    continue
                
                # Clip to time window
                start = max(start, start_sec)
                end = min(end, end_sec)
                
                if end - start <= 0:
                    continue
                
                if label == condition_a:
                    intervals_a.append((start, end - start))
                elif label == condition_b:
                    intervals_b.append((start, end - start))
            
            # Calculate mean band power for each condition
            power_a = mean_band_over_intervals(raw, intervals_a, fmin, fmax, picks=picks) if intervals_a else None
            power_b = mean_band_over_intervals(raw, intervals_b, fmin, fmax, picks=picks) if intervals_b else None
            
            if power_a is None or power_b is None:
                st.error("Could not compute band power for one or both conditions")
                st.info(f"Condition A intervals: {len(intervals_a)}, Condition B intervals: {len(intervals_b)}")
                return None
            
            # Calculate contrast in dB
            contrast = contrast_db(power_b, power_a)
            
            # Create contrast topomap
            vmax = float(np.max(np.abs(contrast)))
            vmin = -vmax if vmax > 0 else -1e-12
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
            
            fig, ax = plt.subplots(figsize=(5, 5), dpi=140)
            mne.viz.plot_topomap(
                contrast, raw.info, ch_type="eeg",
                sphere=SPHERE, outlines="head", contours=6,
                cmap="RdBu_r", cnorm=norm, sensors=False, axes=ax
            )
            ax.set_title(f"Contrast (dB): {condition_b} - {condition_a}\n{band_name} band")
            
            st.pyplot(fig)
            
            # Show statistics
            st.info(f"📊 Condition A ({condition_a}): {len(intervals_a)} intervals")
            st.info(f"📊 Condition B ({condition_b}): {len(intervals_b)} intervals")
            st.info(f"📊 Max contrast: ±{vmax:.2f} dB")
            
            return fig
            
        except Exception as e:
            st.error(f"Failed to create contrast analysis: {str(e)}")
            return None
    
    def _render_temporal_gif(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> Optional[bytes]:
        """Render temporal GIF animation."""
        st.subheader("🎬 Temporal Animation")
        
        # Parameters
        col1, col2, col3 = st.columns(3)
        with col1:
            band_name = st.selectbox("Frequency band", list(BANDS.keys()), index=2, key="gif_band")
            win_len = st.number_input("Window length (s)", 0.5, 10.0, 2.0, 0.5, key="gif_window")
        with col2:
            step_size = st.number_input("Step size (s)", 0.1, 5.0, 0.5, 0.1, key="gif_step")
            fps = st.slider("Animation FPS", 2, 30, 10, key="gif_fps")
        with col3:
            pmin = st.slider("Color min percentile", 0, 20, 5, key="gif_pmin")
            pmax = st.slider("Color max percentile", 80, 100, 95, key="gif_pmax")
        
        colormap = st.selectbox("Colormap", ["RdBu_r", "viridis", "plasma", "magma"], key="gif_cmap")
        
        if st.button("🎬 Generate Animation", key="generate_gif"):
            try:
                fmin, fmax = BANDS[band_name]
                
                with st.spinner("Generating animation frames..."):
                    frames, meta, vm = build_frames(raw, fmin, fmax, picks, start_sec, end_sec, win_len, step_size, pmin, pmax)
                
                if frames is None:
                    st.error("Failed to generate frames. Try adjusting window/step parameters.")
                    return None
                
                with st.spinner("Rendering GIF..."):
                    vmin_all, vmax_all = vm
                    gif_bytes = render_gif(raw, frames, meta, vmin_all, vmax_all, cmap=colormap, fps=fps)
                
                st.success(f"✅ Generated {len(frames)} frames")
                st.image(gif_bytes, caption=f"{band_name} band temporal evolution")
                
                # Download button
                st.download_button(
                    "📥 Download GIF",
                    data=gif_bytes,
                    file_name=f"eeg_temporal_{band_name.lower()}_{start_sec:.0f}s-{end_sec:.0f}s.gif",
                    mime="image/gif"
                )
                
                return gif_bytes
                
            except Exception as e:
                st.error(f"Failed to generate temporal GIF: {str(e)}")
                return None
        
        return None
    
    def _render_regional_bars(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> Optional[plt.Figure]:
        """Render regional bar chart."""
        st.subheader("🏛️ Regional Analysis")
        
        band_name = st.selectbox("Frequency band", list(BANDS.keys()), index=2, key="regional_band")
        
        try:
            fmin, fmax = BANDS[band_name]
            seg = raw.copy().crop(tmin=start_sec, tmax=end_sec)
            bp = bandpower_mean(seg, fmin, fmax, picks=picks)
            
            # Aggregate by brain region
            bars = region_means(seg.ch_names, bp)
            
            if not bars:
                st.warning("No brain regions matched the current channel selection")
                return None
            
            # Create bar chart
            regions = [b[0] for b in bars]
            powers = [b[1] for b in bars]
            
            fig, ax = plt.subplots(figsize=(8, 5), dpi=140)
            bars_plot = ax.bar(regions, powers, color='steelblue', alpha=0.7)
            ax.set_ylabel("Mean Band Power")
            ax.set_title(f"{band_name} Power by Brain Region ({start_sec:.1f}-{end_sec:.1f}s)")
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for bar, power in zip(bars_plot, powers):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(powers)*0.01,
                       f'{power:.2e}', ha='center', va='bottom', fontsize=9)
            
            fig.tight_layout()
            st.pyplot(fig)
            
            # Show regional summary
            st.info(f"📊 Analyzed {len(bars)} brain regions from {len([ch for ch in seg.ch_names if ch in raw.ch_names])} channels")
            
            return fig
            
        except Exception as e:
            st.error(f"Failed to create regional analysis: {str(e)}")
            return None
    
    def _render_psd(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> Optional[plt.Figure]:
        """Render Power Spectral Density plot."""
        st.subheader("📈 Power Spectral Density")
        
        # Parameters
        fmax_show = st.number_input(
            "Maximum frequency (Hz)",
            value=60.0,
            min_value=5.0,
            max_value=float(raw.info["sfreq"] / 2),
            step=5.0,
            key="psd_fmax"
        )
        
        show_legend = st.checkbox("Show channel legend", value=False, key="psd_legend")
        
        try:
            seg = raw.copy().crop(tmin=start_sec, tmax=end_sec)
            psd = seg.compute_psd(fmax=fmax_show, picks=picks, reject_by_annotation="omit", verbose=False)
            
            freqs = psd.freqs
            data = psd.get_data()
            channel_names = [seg.ch_names[i] for i in picks]
            
            fig = psd_multi(freqs, data, channel_names, show_legend=show_legend)
            st.pyplot(fig)
            
            # Show PSD statistics
            mean_power = np.mean(data)
            peak_freq = freqs[np.argmax(np.mean(data, axis=0))]
            st.info(f"📊 Mean power: {mean_power:.2e} | Peak frequency: {peak_freq:.1f} Hz")
            
            return fig
            
        except Exception as e:
            st.error(f"Failed to create PSD plot: {str(e)}")
            return None
    
    def _render_raw_preview(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float) -> Optional[plt.Figure]:
        """Render raw time series preview."""
        st.subheader("📊 Raw Time Series")
        
        n_channels_show = st.slider(
            "Channels to display", 
            4, len(raw.ch_names), 
            min(14, len(raw.ch_names)), 
            key="raw_n_channels"
        )
        
        scaling_factor = st.selectbox(
            "Amplitude scaling", 
            options=[("Auto", None), ("20 µV", 20e-6), ("50 µV", 50e-6), ("100 µV", 100e-6)],
            index=1,
            key="raw_scaling"
        )[1]
        
        try:
            duration = end_sec - start_sec
            seg = raw.copy().crop(tmin=start_sec, tmax=end_sec)
            
            scalings = {"eeg": scaling_factor} if scaling_factor else "auto"
            
            fig = seg.plot(
                n_channels=n_channels_show,
                duration=max(1.0, duration),
                start=0.0,
                show=False,
                block=False,
                scalings=scalings,
                clipping=None
            )
            
            st.pyplot(fig)
            st.info(f"📊 Showing {n_channels_show} channels over {duration:.1f} seconds")
            
            return fig
            
        except Exception as e:
            st.error(f"Failed to create raw time series: {str(e)}")
            return None
    
    def _render_erp(self, raw: mne.io.BaseRaw, labels: List[str], picks) -> Optional[List[plt.Figure]]:
        """Render Event-Related Potentials."""
        st.subheader("⚡ Event-Related Potentials (ERP)")
        
        if not labels:
            st.warning("No annotation labels found. ERPs require event markers.")
            return None
        
        # ERP parameters
        col1, col2 = st.columns(2)
        with col1:
            selected_conditions = st.multiselect(
                "Conditions to analyze",
                labels,
                default=labels[:2] if len(labels) >= 2 else labels,
                key="erp_conditions"
            )
            tmin = st.number_input("Epoch start (s)", value=-0.2, step=0.05, format="%.2f", key="erp_tmin")
            tmax = st.number_input("Epoch end (s)", value=0.8, step=0.05, format="%.2f", key="erp_tmax")
        
        with col2:
            use_baseline = st.checkbox("Baseline correction", value=True, key="erp_baseline")
            if use_baseline:
                baseline_start = st.number_input("Baseline start (s)", value=-0.2, step=0.05, format="%.2f", key="erp_bstart")
                baseline_end = st.number_input("Baseline end (s)", value=0.0, step=0.05, format="%.2f", key="erp_bend")
                baseline = (baseline_start, baseline_end)
            else:
                baseline = None
            
            decim = st.slider("Decimation factor", 1, 10, 2, key="erp_decim")
        
        if not selected_conditions:
            st.warning("Select at least one condition")
            return None
        
        try:
            # Create epochs
            epochs, event_id, error = self.epoch_manager.create_epochs_from_labels(
                raw, selected_conditions, tmin, tmax, picks, baseline, decim
            )
            
            if error:
                st.error(f"Failed to create epochs: {error}")
                return None
            
            figures = []
            
            # Create evoked responses for each condition
            for condition in selected_conditions:
                if condition in epochs.event_id:
                    evoked = epochs[condition].average()
                    
                    # Plot butterfly plot with spatial colors
                    fig = evoked.plot(spatial_colors=True, selectable=False, show=False, exclude="bads")
                    fig.suptitle(f"ERP - {condition} (n={len(epochs[condition])} epochs)")
                    st.pyplot(fig)
                    figures.append(fig)
            
            # Show epoch information
            epoch_info = self.epoch_manager.get_epochs_info(epochs)
            st.info(f"📊 Created {epoch_info['n_epochs']} epochs total")
            for condition, count in epoch_info['condition_counts'].items():
                st.info(f"  • {condition}: {count} epochs")
            
            return figures
            
        except Exception as e:
            st.error(f"Failed to create ERPs: {str(e)}")
            return None
    
    def _render_tfr(self, raw: mne.io.BaseRaw, labels: List[str], picks) -> Optional[plt.Figure]:
        """Render Time-Frequency analysis."""
        st.subheader("🌊 Time-Frequency Analysis")
        
        if not labels:
            st.warning("Time-frequency analysis requires event markers")
            return None
        
        # TFR parameters
        col1, col2 = st.columns(2)
        with col1:
            condition = st.selectbox("Condition", labels, key="tfr_condition")
            tmin = st.number_input("Epoch start (s)", value=-0.5, step=0.05, format="%.2f", key="tfr_tmin")
            tmax = st.number_input("Epoch end (s)", value=1.0, step=0.05, format="%.2f", key="tfr_tmax")
            f_min = st.number_input("Min frequency (Hz)", value=2.0, min_value=1.0, step=1.0, key="tfr_fmin")
            f_max = st.number_input("Max frequency (Hz)", value=40.0, min_value=5.0, step=1.0, key="tfr_fmax")
        
        with col2:
            n_freqs = st.slider("Number of frequencies", 10, 60, 30, key="tfr_nfreqs")
            decim = st.slider("Decimation", 1, 10, 3, key="tfr_decim")
            use_baseline = st.checkbox("Baseline correction", value=False, key="tfr_baseline")
            if use_baseline:
                baseline_start = st.number_input("Baseline start (s)", value=-0.5, step=0.05, format="%.2f", key="tfr_bstart")
                baseline_end = st.number_input("Baseline end (s)", value=0.0, step=0.05, format="%.2f", key="tfr_bend")
                baseline = (baseline_start, baseline_end)
            else:
                baseline = None
        
        # Channel selection for averaging
        channel_selection = st.multiselect(
            "Channels for averaging",
            [raw.ch_names[i] for i in picks],
            default=[raw.ch_names[i] for i in picks[:min(4, len(picks))]],
            key="tfr_channels"
        )
        
        if not channel_selection:
            st.warning("Select at least one channel")
            return None
        
        try:
            # Create epochs
            epochs, event_id, error = self.epoch_manager.create_epochs_from_labels(
                raw, [condition], tmin, tmax, picks, baseline, decim
            )
            
            if error:
                st.error(f"Failed to create epochs: {error}")
                return None
            
            # Set up frequency analysis
            freqs = np.linspace(f_min, f_max, n_freqs)
            n_cycles = freqs / 2.0  # Adaptive number of cycles
            
            with st.spinner("Computing time-frequency decomposition..."):
                # Compute TFR using Morlet wavelets
                power = tfr_morlet(
                    epochs[condition], 
                    freqs=freqs, 
                    n_cycles=n_cycles,
                    use_fft=True, 
                    return_itc=False, 
                    average=True, 
                    decim=1, 
                    n_jobs=1
                )
            
            # Average across selected channels
            ch_indices = [power.ch_names.index(ch) for ch in channel_selection if ch in power.ch_names]
            avg_power = power.data[ch_indices].mean(axis=0)
            
            # Apply baseline if requested
            if use_baseline and baseline is not None:
                times = power.times
                baseline_mask = (times >= baseline[0]) & (times <= baseline[1])
                if baseline_mask.any():
                    baseline_mean = avg_power[:, baseline_mask].mean(axis=1, keepdims=True)
                    avg_power = 10 * np.log10((avg_power + 1e-20) / (baseline_mean + 1e-20))
            
            # Create time-frequency plot
            fig, ax = plt.subplots(figsize=(10, 6), dpi=140)
            extent = [power.times[0], power.times[-1], freqs[0], freqs[-1]]
            
            im = ax.imshow(
                avg_power,
                origin="lower",
                aspect="auto", 
                extent=extent,
                interpolation="nearest",
                cmap="magma"
            )
            
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")
            ax.set_title(f"Time-Frequency Power - {condition} (avg of {len(ch_indices)} channels)")
            
            # Add colorbar
            cbar_label = "Power (dB relative to baseline)" if use_baseline else "Power"
            fig.colorbar(im, ax=ax, label=cbar_label)
            
            # Add event line at t=0
            ax.axvline(0, color='white', linestyle='--', alpha=0.8, linewidth=2)
            
            fig.tight_layout()
            st.pyplot(fig)
            
            # Show analysis info
            st.info(f"📊 Analyzed {len(epochs[condition])} epochs, {len(ch_indices)} channels")
            st.info(f"📊 Frequency range: {f_min}-{f_max} Hz, Time range: {tmin}-{tmax} s")
            
            return fig
            
        except Exception as e:
            st.error(f"Failed to create time-frequency analysis: {str(e)}")
            return None