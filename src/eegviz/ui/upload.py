"""File upload component for EEG files and markers."""

from __future__ import annotations
from pathlib import Path
import streamlit as st
from typing import Optional, Tuple


class FileUploadComponent:
    """Handles file upload UI and validation for EDF files and marker files."""
    
    def __init__(self):
        self.edf_file = None
        self.csv_file = None 
        self.json_file = None
    
    def render_upload_sidebar(self) -> Tuple[Optional[object], Optional[object], Optional[object]]:
        """Render the file upload sidebar.
        
        Returns:
            Tuple of (edf_file, csv_file, json_file) uploaded file objects
        """
        with st.sidebar:
            st.header("Upload")
            
            # EDF file upload
            edf_file = st.file_uploader(
                "EDF/EDF+ file", 
                type=["edf", "bdf"],
                help="Upload your EEG data file in EDF or BDF format"
            )
            
            # Optional marker files
            csv_file = st.file_uploader(
                "Markers CSV (optional)", 
                type=["csv"],
                help="CSV file with columns: latency, duration, type"
            )
            
            json_file = st.file_uploader(
                "Markers JSON (optional)", 
                type=["json"],
                help="JSON file with Markers array containing startDatetime, endDatetime, label"
            )
            
            if edf_file:
                st.success(f"✅ EDF file loaded: {edf_file.name}")
                st.info(f"File size: {len(edf_file.getvalue()) / 1024 / 1024:.1f} MB")
            
            if csv_file:
                st.success(f"✅ CSV markers: {csv_file.name}")
                
            if json_file:
                st.success(f"✅ JSON markers: {json_file.name}")
        
        return edf_file, csv_file, json_file
    
    def validate_edf_file(self, edf_file) -> bool:
        """Validate the uploaded EDF file.
        
        Args:
            edf_file: Streamlit file upload object
            
        Returns:
            True if file is valid, False otherwise
        """
        if not edf_file:
            return False
            
        # Check file size (warn if > 100MB)
        file_size_mb = len(edf_file.getvalue()) / 1024 / 1024
        if file_size_mb > 100:
            st.warning(f"⚠️ Large file detected ({file_size_mb:.1f} MB). Processing may be slow.")
        
        # Check file extension
        if not edf_file.name.lower().endswith(('.edf', '.bdf')):
            st.error("❌ Invalid file type. Please upload an EDF or BDF file.")
            return False
            
        return True
    
    def save_uploaded_file(self, uploaded_file, tmpdir: Path) -> Path:
        """Save uploaded file to temporary directory.
        
        Args:
            uploaded_file: Streamlit file upload object
            tmpdir: Temporary directory path
            
        Returns:
            Path to saved file
        """
        file_path = tmpdir / uploaded_file.name
        file_path.write_bytes(uploaded_file.getvalue())
        return file_path