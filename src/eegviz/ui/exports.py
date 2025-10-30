"""Export functionality component."""

from __future__ import annotations
import streamlit as st
import mne
import io
from typing import Dict, Any
from ..config import BANDS
from ..analysis.bands import bandpower_mean
from ..export.annotations import annotations_to_csv_bytes
from ..export.bandpower_csv import bandpower_to_csv_bytes
from ..export.save_raw import save_fif_bytes, save_edf_bytes


class ExportComponent:
    """Handles data export functionality."""
    
    def __init__(self):
        pass
    
    def render_export_section(self, processed_raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> None:
        """Render the export section with download options.
        
        Args:
            processed_raw: Processed MNE Raw object
            start_sec: Start time of current window
            end_sec: End time of current window  
            picks: Channel picks for analysis
        """
        st.header("💾 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_annotations_export(processed_raw)
        
        with col2:
            self._render_bandpower_export(processed_raw, start_sec, end_sec, picks)
        
        with col3:
            self._render_raw_data_export(processed_raw)
    
    def _render_annotations_export(self, raw: mne.io.BaseRaw) -> None:
        """Render annotations export section."""
        st.subheader("📋 Annotations")
        
        if len(raw.annotations) > 0:
            st.info(f"Found {len(raw.annotations)} annotations")
            
            # Preview annotations
            if st.checkbox("Preview annotations", key="preview_annotations"):
                import pandas as pd
                df = pd.DataFrame({
                    "onset_s": raw.annotations.onset,
                    "duration_s": raw.annotations.duration,
                    "label": raw.annotations.description,
                })
                st.dataframe(df.head(10), use_container_width=True)
                if len(df) > 10:
                    st.caption(f"Showing first 10 of {len(df)} annotations")
            
            # Download button
            st.download_button(
                "📥 Download Annotations CSV",
                data=annotations_to_csv_bytes(raw.annotations),
                file_name="annotations.csv",
                mime="text/csv",
                help="Export all annotations as CSV file"
            )
        else:
            st.warning("No annotations to export")
    
    def _render_bandpower_export(self, raw: mne.io.BaseRaw, start_sec: float, end_sec: float, picks) -> None:
        """Render band power export section."""
        st.subheader("⚡ Band Power")
        
        # Band selection for export
        band_name = st.selectbox(
            "Frequency band",
            options=list(BANDS.keys()),
            index=2,  # Default to Alpha
            key="export_band",
            help="Select frequency band for power analysis"
        )
        
        fmin, fmax = BANDS[band_name]
        
        # Calculate band power for current window
        try:
            seg = raw.copy().crop(tmin=start_sec, tmax=end_sec)
            bp = bandpower_mean(seg, fmin, fmax, picks=picks)
            
            st.info(f"Band: {band_name} ({fmin}-{fmax} Hz)")
            st.info(f"Window: {start_sec:.1f}-{end_sec:.1f}s ({end_sec-start_sec:.1f}s duration)")
            
            # Show statistics
            if len(bp) > 0:
                col_stats1, col_stats2 = st.columns(2)
                with col_stats1:
                    st.metric("Mean Power", f"{bp.mean():.2e}")
                with col_stats2:
                    st.metric("Max Power", f"{bp.max():.2e}")
            
            # Download button
            st.download_button(
                "📥 Download Band Power CSV",
                data=bandpower_to_csv_bytes([raw.ch_names[i] for i in picks], band_name, bp),
                file_name=f"band_power_{band_name.lower()}_{start_sec:.0f}s-{end_sec:.0f}s.csv",
                mime="text/csv",
                help=f"Export {band_name} band power for each channel"
            )
            
        except Exception as e:
            st.error(f"Error calculating band power: {str(e)}")
    
    def _render_raw_data_export(self, raw: mne.io.BaseRaw) -> None:
        """Render raw data export section."""
        st.subheader("🗂️ Processed Data")
        
        # Show data info
        duration_min = len(raw.times) / raw.info["sfreq"] / 60
        data_size_mb = raw.get_data().nbytes / 1024 / 1024
        
        st.info(f"Duration: {duration_min:.1f} minutes")
        st.info(f"Size: ~{data_size_mb:.1f} MB")
        
        # Format selection
        export_format = st.selectbox(
            "Export format",
            options=["FIF (MNE native)", "EDF (universal)"],
            help="FIF: Best for MNE-Python. EDF: Universal format for other software"
        )
        
        # Export button with processing
        if st.button("🚀 Prepare Download", key="export_raw"):
            try:
                if "FIF" in export_format:
                    with st.spinner("Preparing FIF file..."):
                        file_data = save_fif_bytes(raw)
                        file_name = "processed_eeg_data.fif"
                        mime_type = "application/octet-stream"
                else:
                    with st.spinner("Preparing EDF file..."):
                        file_data = save_edf_bytes(raw)
                        file_name = "processed_eeg_data.edf"
                        mime_type = "application/octet-stream"
                
                # Show download button
                st.download_button(
                    "📥 Download Processed Data",
                    data=file_data,
                    file_name=file_name,
                    mime=mime_type,
                    help="Download the processed EEG data file"
                )
                st.success("✅ File ready for download!")
                
            except Exception as e:
                st.error(f"❌ Export failed: {str(e)}")
                if "EDF" in export_format:
                    st.info("💡 Try FIF format if EDF export fails")
    
    def render_visualization_downloads(self, fig, vis_type: str) -> None:
        """Render download options for visualization figures.
        
        Args:
            fig: Matplotlib figure object
            vis_type: Type of visualization for filename
        """
        if fig is not None:
            # Create download button for PNG
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            
            st.download_button(
                f"📥 Download {vis_type} PNG",
                data=buf.getvalue(),
                file_name=f"{vis_type.lower().replace(' ', '_')}.png",
                mime="image/png",
                help=f"Download {vis_type} as high-resolution PNG"
            )