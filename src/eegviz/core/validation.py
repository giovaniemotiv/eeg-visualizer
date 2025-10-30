"""Validation utilities for EEG data and user inputs."""

from __future__ import annotations
import mne
import numpy as np
import streamlit as st
from typing import List, Optional, Tuple, Any
from pathlib import Path


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class DataValidator:
    """Validates EEG data, file inputs, and processing parameters."""
    
    @staticmethod
    def validate_edf_file(file_path: Path) -> Tuple[bool, Optional[str]]:
        """Validate an EDF file can be loaded.
        
        Args:
            file_path: Path to EDF file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to load the file
            raw = mne.io.read_raw_edf(str(file_path), preload=False, verbose=False)
            
            # Basic validation checks
            if len(raw.ch_names) == 0:
                return False, "No channels found in EDF file"
            
            if raw.n_times == 0:
                return False, "No data samples found in EDF file"
            
            if raw.info["sfreq"] <= 0:
                return False, "Invalid sampling frequency"
            
            return True, None
            
        except Exception as e:
            return False, f"Failed to load EDF file: {str(e)}"
    
    @staticmethod
    def validate_raw_data(raw: mne.io.BaseRaw) -> Tuple[bool, List[str]]:
        """Validate loaded raw EEG data.
        
        Args:
            raw: MNE Raw object
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        is_valid = True
        
        # Check basic properties
        if len(raw.ch_names) == 0:
            warnings.append("No channels found")
            is_valid = False
        
        if raw.n_times == 0:
            warnings.append("No data samples found") 
            is_valid = False
        
        # Check sampling rate
        sfreq = raw.info["sfreq"]
        if sfreq < 64:
            warnings.append(f"Low sampling rate ({sfreq} Hz) may limit analysis")
        elif sfreq > 2000:
            warnings.append(f"Very high sampling rate ({sfreq} Hz) may slow processing")
        
        # Check duration
        duration_min = len(raw.times) / sfreq / 60
        if duration_min < 0.5:
            warnings.append(f"Very short recording ({duration_min:.1f} minutes)")
        elif duration_min > 60:
            warnings.append(f"Long recording ({duration_min:.0f} minutes) may slow processing")
        
        # Check for bad channels
        if len(raw.info["bads"]) > len(raw.ch_names) * 0.5:
            warnings.append(f"Many bad channels ({len(raw.info['bads'])}/{len(raw.ch_names)})")
        
        # Check data quality
        try:
            data = raw.get_data(picks="eeg")
            if data.size > 0:
                # Check for flat channels
                flat_channels = np.sum(np.std(data, axis=1) < 1e-12)
                if flat_channels > 0:
                    warnings.append(f"{flat_channels} channels appear flat")
                
                # Check for extreme values
                extreme_vals = np.sum(np.abs(data) > 1e-3)  # > 1mV
                if extreme_vals > data.size * 0.01:  # > 1% of samples
                    warnings.append("Some samples have extreme values (>1mV)")
        
        except Exception as e:
            warnings.append(f"Could not validate data quality: {str(e)}")
        
        return is_valid, warnings
    
    @staticmethod
    def validate_filter_params(raw: mne.io.BaseRaw, l_freq: Optional[float], 
                             h_freq: Optional[float], resample_freq: Optional[float]) -> List[str]:
        """Validate filter parameters.
        
        Args:
            raw: MNE Raw object
            l_freq: High-pass frequency
            h_freq: Low-pass frequency  
            resample_freq: Resampling frequency
            
        Returns:
            List of validation error messages
        """
        errors = []
        nyquist = raw.info["sfreq"] / 2
        
        # High-pass filter validation
        if l_freq is not None:
            if l_freq < 0:
                errors.append("High-pass frequency must be positive")
            elif l_freq >= nyquist:
                errors.append(f"High-pass frequency ({l_freq} Hz) must be < Nyquist ({nyquist} Hz)")
        
        # Low-pass filter validation
        if h_freq is not None:
            if h_freq <= 0:
                errors.append("Low-pass frequency must be positive")
            elif h_freq >= nyquist:
                errors.append(f"Low-pass frequency ({h_freq} Hz) must be < Nyquist ({nyquist} Hz)")
        
        # Filter order validation
        if l_freq is not None and h_freq is not None:
            if l_freq >= h_freq:
                errors.append("High-pass frequency must be < low-pass frequency")
        
        # Resampling validation
        if resample_freq is not None:
            if resample_freq <= 0:
                errors.append("Resample frequency must be positive")
            elif resample_freq > raw.info["sfreq"]:
                errors.append("Cannot upsample - resample frequency must be ≤ original sampling rate")
            elif h_freq is not None and resample_freq < 2 * h_freq:
                errors.append(f"Resample frequency ({resample_freq} Hz) must be > 2 × low-pass frequency ({h_freq} Hz)")
        
        return errors
    
    @staticmethod
    def validate_time_window(raw: mne.io.BaseRaw, start_sec: float, end_sec: float) -> Tuple[float, float, List[str]]:
        """Validate and correct time window parameters.
        
        Args:
            raw: MNE Raw object
            start_sec: Start time in seconds
            end_sec: End time in seconds
            
        Returns:
            Tuple of (corrected_start, corrected_end, warnings)
        """
        warnings = []
        max_time = len(raw.times) / raw.info["sfreq"]
        
        # Correct start time
        corrected_start = max(0.0, min(start_sec, max_time))
        if corrected_start != start_sec:
            warnings.append(f"Start time corrected: {start_sec:.2f} → {corrected_start:.2f}s")
        
        # Correct end time
        corrected_end = max(corrected_start, min(end_sec, max_time))
        if corrected_end != end_sec:
            warnings.append(f"End time corrected: {end_sec:.2f} → {corrected_end:.2f}s")
        
        # Check minimum duration
        duration = corrected_end - corrected_start
        if duration < 0.1:
            corrected_end = min(corrected_start + 0.1, max_time)
            warnings.append(f"Minimum duration enforced: {duration:.2f} → {corrected_end - corrected_start:.2f}s")
        
        return corrected_start, corrected_end, warnings
    
    @staticmethod
    def validate_channel_selection(raw: mne.io.BaseRaw, channels: List[str]) -> Tuple[List[str], List[str]]:
        """Validate channel selection.
        
        Args:
            raw: MNE Raw object
            channels: List of channel names to validate
            
        Returns:
            Tuple of (valid_channels, invalid_channels)
        """
        available_channels = set(raw.ch_names)
        valid_channels = [ch for ch in channels if ch in available_channels]
        invalid_channels = [ch for ch in channels if ch not in available_channels]
        
        return valid_channels, invalid_channels
    
    @staticmethod
    def show_validation_results(is_valid: bool, warnings: List[str], errors: List[str] = None) -> None:
        """Display validation results in Streamlit UI.
        
        Args:
            is_valid: Whether validation passed
            warnings: List of warning messages
            errors: List of error messages
        """
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        
        if warnings:
            for warning in warnings:
                st.warning(f"⚠️ {warning}")
        
        if is_valid and not warnings and not errors:
            st.success("✅ Validation passed!")
    
    @staticmethod
    def validate_annotations_csv(file_path: Path) -> Tuple[bool, List[str]]:
        """Validate CSV annotations file format.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        import pandas as pd
        
        try:
            df = pd.read_csv(file_path)
            errors = []
            
            # Check required columns
            required_cols = {"latency", "duration", "type"}
            if not required_cols.issubset(df.columns):
                missing = required_cols - set(df.columns)
                errors.append(f"Missing required columns: {missing}")
            
            # Check data types if columns exist
            if "latency" in df.columns:
                if not pd.api.types.is_numeric_dtype(df["latency"]):
                    errors.append("'latency' column must be numeric")
            
            if "duration" in df.columns:
                if not pd.api.types.is_numeric_dtype(df["duration"]):
                    errors.append("'duration' column must be numeric")
                elif (df["duration"] <= 0).any():
                    errors.append("'duration' must be positive")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            return False, [f"Failed to read CSV file: {str(e)}"]