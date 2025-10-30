"""Channel selection and management component."""

from __future__ import annotations
import streamlit as st
import mne
from typing import List, Tuple
from ..config import EEG14


class ChannelSelectionComponent:
    """Handles channel selection, bad channel marking, and channel information display."""
    
    def __init__(self):
        self.kept_channels = []
        self.bad_channels = []
    
    def render_channel_selection(self, raw: mne.io.BaseRaw) -> Tuple[List[str], List[str]]:
        """Render channel selection interface.
        
        Args:
            raw: MNE Raw object with loaded EEG data
            
        Returns:
            Tuple of (kept_channels, bad_channels)
        """
        st.header("📡 Channels")
        
        # Show channel information
        self._display_channel_info(raw)
        
        # Determine default channels to keep
        present_eeg14 = [ch for ch in EEG14 if ch in raw.ch_names]
        default_kept = present_eeg14 if present_eeg14 else raw.ch_names
        
        # Channel selection interface
        col1, col2 = st.columns(2)
        
        with col1:
            kept = st.multiselect(
                "Channels to keep",
                options=raw.ch_names,
                default=default_kept,
                help="Select which channels to include in analysis"
            )
            
        with col2:
            bads = st.multiselect(
                "Mark bad channels",
                options=kept,
                default=[],
                help="Mark channels as bad (they will be excluded from analysis)"
            )
        
        # Show selection summary
        self._display_selection_summary(raw, kept, bads)
        
        return kept, bads
    
    def _display_channel_info(self, raw: mne.io.BaseRaw) -> None:
        """Display information about the loaded channels."""
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.metric("Total Channels", len(raw.ch_names))
            
        with info_col2:
            eeg_channels = len([ch for ch in raw.ch_names if ch.upper() in [e.upper() for e in EEG14]])
            st.metric("Standard EEG Channels", eeg_channels)
            
        with info_col3:
            st.metric("Sampling Rate", f"{raw.info['sfreq']:.0f} Hz")
    
    def _display_selection_summary(self, raw: mne.io.BaseRaw, kept: List[str], bads: List[str]) -> None:
        """Display summary of channel selection."""
        total_channels = len(raw.ch_names)
        kept_count = len(kept)
        bad_count = len(bads)
        active_count = kept_count - bad_count
        
        st.info(
            f"📊 **Channel Summary:** "
            f"{active_count} active, {bad_count} bad, {kept_count} total selected "
            f"(out of {total_channels} available)"
        )
        
        if bad_count > 0:
            st.warning(f"⚠️ Bad channels will be excluded: {', '.join(bads)}")
            
        # Show which standard channels are missing
        missing_standard = [ch for ch in EEG14 if ch not in kept]
        if missing_standard and len(missing_standard) < len(EEG14):
            st.warning(f"🔍 Missing standard channels: {', '.join(missing_standard)}")
    
    def apply_channel_selection(self, raw: mne.io.BaseRaw, kept: List[str], bads: List[str]) -> None:
        """Apply channel selection and bad channel marking to raw data.
        
        Args:
            raw: MNE Raw object to modify
            kept: List of channels to keep
            bads: List of channels to mark as bad
        """
        # Pick only the selected channels
        if set(kept) != set(raw.ch_names):
            raw.pick(kept)
        
        # Mark bad channels
        raw.info["bads"] = list(bads)
        
        self.kept_channels = kept
        self.bad_channels = bads