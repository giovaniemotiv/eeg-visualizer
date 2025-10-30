"""Filter and preprocessing controls component."""

from __future__ import annotations
import streamlit as st
import mne
from typing import Optional, Tuple, Dict, Any
from ..preprocess.filtering import apply_pipeline


class FilterControlsComponent:
    """Handles filter and preprocessing parameter controls."""
    
    def __init__(self):
        self.filter_params = {}
    
    def render_filter_controls(self, raw: mne.io.BaseRaw) -> Tuple[Dict[str, Any], bool]:
        """Render filter and preprocessing controls.
        
        Args:
            raw: MNE Raw object for parameter validation
            
        Returns:
            Tuple of (filter_parameters_dict, apply_filters_button_pressed)
        """
        st.header("🔧 Filters & Reference")
        
        # Create columns for filter parameters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            notch = st.selectbox(
                "Mains notch filter",
                options=[None, 50.0, 60.0],
                index=2,  # Default to 60Hz for US
                help="Remove power line interference (50Hz Europe, 60Hz US/Canada)"
            )
        
        with col2:
            lfreq = st.number_input(
                "High-pass (Hz)",
                value=1.0,
                min_value=0.0,
                max_value=30.0,
                step=0.5,
                help="Remove slow drifts and DC offset"
            )
        
        with col3:
            hfreq = st.number_input(
                "Low-pass (Hz)",
                value=45.0,
                min_value=5.0,
                max_value=120.0,
                step=1.0,
                help="Remove high-frequency noise and aliasing"
            )
        
        with col4:
            resample_freq = st.number_input(
                "Resample to (Hz)",
                value=256.0,
                min_value=64.0,
                max_value=1024.0,
                step=64.0,
                help="Downsample to reduce computational load"
            )
        
        # Additional processing options
        st.subheader("Additional Processing")        
        proc_col1, proc_col2 = st.columns(2)
        
        with proc_col1:
            ref_avg = st.checkbox(
                "Average reference",
                value=True,
                help="Re-reference to average of all channels"
            )
        
        with proc_col2:
            interpolate = st.checkbox(
                "Interpolate bad channels",
                value=False,
                help="Interpolate bad channels from nearby electrodes"
            )
        
        # Parameter validation and warnings
        self._show_filter_warnings(raw, lfreq, hfreq, resample_freq)
        
        # Apply filters button
        apply_button = st.button(
            "🚀 Apply Filters",
            help="Apply all selected filters and preprocessing steps",
            type="primary"
        )
        
        filter_params = {
            "notch": notch,
            "l_freq": lfreq,
            "h_freq": hfreq,
            "resample": resample_freq,
            "ref_avg": ref_avg,
            "interpolate": interpolate
        }
        
        self.filter_params = filter_params
        return filter_params, apply_button
    
    def _show_filter_warnings(self, raw: mne.io.BaseRaw, lfreq: float, hfreq: float, resample_freq: float) -> None:
        """Show warnings for filter parameters if needed."""
        nyquist = raw.info["sfreq"] / 2
        
        # High-pass filter warning
        if lfreq > 2.0:
            st.warning(f"⚠️ High-pass filter of {lfreq} Hz may remove important low-frequency components")
        
        # Low-pass filter warning  
        if hfreq >= nyquist:
            st.error(f"❌ Low-pass filter ({hfreq} Hz) must be less than Nyquist frequency ({nyquist} Hz)")
        elif hfreq > nyquist * 0.8:
            st.warning(f"⚠️ Low-pass filter close to Nyquist frequency may cause artifacts")
        
        # Resampling warning
        if resample_freq > raw.info["sfreq"]:
            st.warning("⚠️ Cannot upsample data - resample frequency must be ≤ original sampling rate")
        elif resample_freq < 2 * hfreq:
            st.error(f"❌ Resample frequency ({resample_freq} Hz) must be > 2 × low-pass frequency ({hfreq} Hz)")
    
    def apply_filters(self, raw: mne.io.BaseRaw, filter_params: Dict[str, Any]) -> mne.io.BaseRaw:
        """Apply filters to the raw data.
        
        Args:
            raw: MNE Raw object to filter
            filter_params: Dictionary of filter parameters
            
        Returns:
            Filtered MNE Raw object
        """
        with st.spinner("Applying filters..."):
            try:
                processed = apply_pipeline(raw, **filter_params)
                st.success("✅ Filters applied successfully!")
                
                # Show processing summary
                self._show_processing_summary(raw, processed, filter_params)
                
                return processed
                
            except Exception as e:
                st.error(f"❌ Filter application failed: {str(e)}")
                return raw.copy()
    
    def _show_processing_summary(self, raw: mne.io.BaseRaw, processed: mne.io.BaseRaw, params: Dict[str, Any]) -> None:
        """Show summary of applied processing steps."""
        changes = []
        
        if abs(processed.info["sfreq"] - raw.info["sfreq"]) > 1e-6:
            changes.append(f"Resampled: {raw.info['sfreq']:.0f} → {processed.info['sfreq']:.0f} Hz")
        
        if params["notch"]:
            changes.append(f"Notch filtered: {params['notch']} Hz")
        
        if params["l_freq"] or params["h_freq"]:
            changes.append(f"Bandpass: {params['l_freq']}-{params['h_freq']} Hz")
        
        if params["ref_avg"]:
            changes.append("Average referenced")
        
        if params["interpolate"] and raw.info["bads"]:
            changes.append(f"Interpolated {len(raw.info['bads'])} bad channels")
        
        if changes:
            st.info("🔄 **Applied:** " + " | ".join(changes))