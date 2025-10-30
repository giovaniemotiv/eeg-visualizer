"""Session state management for the EEG Visualizer application."""

from __future__ import annotations
import tempfile
import streamlit as st
from pathlib import Path
from typing import Optional, Any, Dict
import mne


class SessionManager:
    """Manages session state, temporary files, and application data persistence."""
    
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize session state variables if they don't exist."""
        if "eegviz_tmpdir" not in st.session_state:
            st.session_state["eegviz_tmpdir"] = tempfile.mkdtemp(prefix="eegviz_")
        
        if "eegviz_raw_data" not in st.session_state:
            st.session_state["eegviz_raw_data"] = None
            
        if "eegviz_processed_data" not in st.session_state:
            st.session_state["eegviz_processed_data"] = None
        
        if "eegviz_filter_applied" not in st.session_state:
            st.session_state["eegviz_filter_applied"] = False
            
        if "eegviz_user_preferences" not in st.session_state:
            st.session_state["eegviz_user_preferences"] = self._get_default_preferences()
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default user preferences."""
        return {
            "default_time_window": 30.0,
            "default_band": "Alpha",
            "preferred_colormap": "RdBu_r",
            "auto_apply_filters": False,
            "show_advanced_options": False,
        }
    
    @property
    def temp_dir(self) -> Path:
        """Get the temporary directory for this session."""
        return Path(st.session_state["eegviz_tmpdir"])
    
    @property
    def raw_data(self) -> Optional[mne.io.BaseRaw]:
        """Get the current raw EEG data."""
        return st.session_state.get("eegviz_raw_data")
    
    @raw_data.setter
    def raw_data(self, value: Optional[mne.io.BaseRaw]) -> None:
        """Set the raw EEG data."""
        st.session_state["eegviz_raw_data"] = value
        # Clear processed data when raw data changes
        if value is not None:
            self.processed_data = None
            self.filter_applied = False
    
    @property
    def processed_data(self) -> Optional[mne.io.BaseRaw]:
        """Get the processed EEG data."""
        return st.session_state.get("eegviz_processed_data")
    
    @processed_data.setter
    def processed_data(self, value: Optional[mne.io.BaseRaw]) -> None:
        """Set the processed EEG data."""
        st.session_state["eegviz_processed_data"] = value
    
    @property
    def filter_applied(self) -> bool:
        """Check if filters have been applied."""
        return st.session_state.get("eegviz_filter_applied", False)
    
    @filter_applied.setter
    def filter_applied(self, value: bool) -> None:
        """Set filter applied status."""
        st.session_state["eegviz_filter_applied"] = value
    
    @property
    def preferences(self) -> Dict[str, Any]:
        """Get user preferences."""
        return st.session_state.get("eegviz_user_preferences", self._get_default_preferences())
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update a user preference."""
        prefs = self.preferences.copy()
        prefs[key] = value
        st.session_state["eegviz_user_preferences"] = prefs
    
    def get_current_data(self) -> Optional[mne.io.BaseRaw]:
        """Get the current data to use (processed if available, otherwise raw)."""
        return self.processed_data if self.processed_data is not None else self.raw_data
    
    def clear_session(self) -> None:
        """Clear all session data."""
        keys_to_clear = [
            "eegviz_raw_data",
            "eegviz_processed_data", 
            "eegviz_filter_applied",
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def save_uploaded_file(self, uploaded_file, filename: Optional[str] = None) -> Path:
        """Save an uploaded file to the temporary directory.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            filename: Optional custom filename
            
        Returns:
            Path to the saved file
        """
        if filename is None:
            filename = uploaded_file.name
            
        file_path = self.temp_dir / filename
        file_path.write_bytes(uploaded_file.getvalue())
        return file_path
    
    def display_session_info(self) -> None:
        """Display session information in an expander (for debugging)."""
        with st.expander("🔍 Session Info (Debug)", expanded=False):
            st.write("**Temporary Directory:**", str(self.temp_dir))
            st.write("**Raw Data Loaded:**", self.raw_data is not None)
            st.write("**Processed Data Available:**", self.processed_data is not None)
            st.write("**Filters Applied:**", self.filter_applied)
            
            if self.raw_data is not None:
                st.write("**Raw Data Info:**")
                st.write(f"- Channels: {len(self.raw_data.ch_names)}")
                st.write(f"- Sampling Rate: {self.raw_data.info['sfreq']:.0f} Hz")
                st.write(f"- Duration: {len(self.raw_data.times) / self.raw_data.info['sfreq']:.1f} seconds")
                st.write(f"- Annotations: {len(self.raw_data.annotations)}")
            
            st.write("**User Preferences:**")
            for key, value in self.preferences.items():
                st.write(f"- {key}: {value}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of the current data state.
        
        Returns:
            Dictionary with data summary information
        """
        current_data = self.get_current_data()
        
        if current_data is None:
            return {"status": "no_data"}
        
        return {
            "status": "data_loaded",
            "n_channels": len(current_data.ch_names),
            "n_bad_channels": len(current_data.info["bads"]),
            "sampling_rate": current_data.info["sfreq"],
            "duration_sec": len(current_data.times) / current_data.info["sfreq"],
            "n_annotations": len(current_data.annotations),
            "filter_applied": self.filter_applied,
            "data_type": "processed" if self.processed_data is not None else "raw"
        }