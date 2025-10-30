"""
EEG Visualizer - Main Streamlit Application

A comprehensive EEG analysis and visualization tool built with MNE-Python and Streamlit.
Supports EDF/EDF+ files, marker import, real-time filtering, and advanced visualizations.
"""

from __future__ import annotations
import streamlit as st
import mne
import mne.io

# Import our organized components
from eegviz.core.session import SessionManager
from eegviz.core.validation import DataValidator
from eegviz.ui.upload import FileUploadComponent
from eegviz.ui.channels import ChannelSelectionComponent
from eegviz.ui.filters import FilterControlsComponent
from eegviz.ui.visualizations import VisualizationPanelComponent
from eegviz.ui.exports import ExportComponent
from eegviz.io.markers_csv import add_csv_markers
from eegviz.io.markers_json import add_json_markers
from eegviz.preprocess.channels import normalize_names, set_montage
from eegviz.preprocess.windows import restrict_interval


def main():
    """Main application function."""
    # Configure Streamlit page
    st.set_page_config(
        page_title="EEG Visualizer",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session manager and components
    session = SessionManager()
    uploader = FileUploadComponent()
    channel_selector = ChannelSelectionComponent()
    filter_controls = FilterControlsComponent()
    visualizer = VisualizationPanelComponent()
    exporter = ExportComponent()
    
    # App header
    st.title("🧠 EEG Visualizer")
    st.caption("Load EDF/EDF+ files, apply filters, analyze, and visualize EEG data")
    
    # Show session info in debug mode
    if st.sidebar.checkbox("Debug Mode", value=False):
        session.display_session_info()
    
    # Step 1: File Upload
    edf_file, csv_file, json_file = uploader.render_upload_sidebar()
    
    if not edf_file:
        st.info("👆 Upload an EDF/EDF+ file in the sidebar to begin analysis")
        _show_welcome_info()
        return
    
    # Validate and load EDF file
    if not uploader.validate_edf_file(edf_file):
        return
    
    # Load EDF data if not already loaded or if file changed
    if session.raw_data is None or _file_changed(edf_file, session):
        with st.spinner("Loading EDF file..."):
            try:
                edf_path = session.save_uploaded_file(edf_file)
                raw = mne.io.read_raw_edf(str(edf_path), preload=True, verbose=False)
                
                # Basic preprocessing
                normalize_names(raw)
                set_montage(raw, "standard_1020")
                
                # Validate loaded data
                is_valid, warnings = DataValidator.validate_raw_data(raw)
                if warnings:
                    DataValidator.show_validation_results(is_valid, warnings)
                
                session.raw_data = raw
                st.success(f"✅ EDF file loaded successfully!")
                
            except Exception as e:
                st.error(f"❌ Failed to load EDF file: {str(e)}")
                return
    
    raw = session.raw_data
    
    # Step 2: Load Markers
    _handle_marker_loading(raw, csv_file, json_file, session)
    
    # Step 3: Channel Selection
    kept_channels, bad_channels = channel_selector.render_channel_selection(raw)
    channel_selector.apply_channel_selection(raw, kept_channels, bad_channels)
    
    # Step 4: Filter Controls
    filter_params, apply_filters = filter_controls.render_filter_controls(raw)
    
    # Apply filters if requested
    if apply_filters or (session.filter_applied and session.processed_data is not None):
        if apply_filters:
            # Validate filter parameters
            errors = DataValidator.validate_filter_params(
                raw, filter_params.get("l_freq"), 
                filter_params.get("h_freq"), filter_params.get("resample")
            )
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                processed = filter_controls.apply_filters(raw, filter_params)
                session.processed_data = processed
                session.filter_applied = True
        
        current_data = session.processed_data
    else:
        current_data = raw.copy()
        if not session.filter_applied:
            st.info("💡 Using unfiltered data. Apply filters for preprocessing.")
    
    # Step 5: Time Window Selection
    _render_time_window_selection(current_data)
    
    # Get time window from session state
    start_sec = st.session_state.get("time_window_start", 0.0)
    end_sec = st.session_state.get("time_window_end", min(30.0, len(current_data.times) / current_data.info["sfreq"]))
    
    # Validate and correct time window
    max_time = len(current_data.times) / current_data.info["sfreq"]
    start_sec, end_sec, time_warnings = DataValidator.validate_time_window(current_data, start_sec, end_sec)
    
    if time_warnings:
        for warning in time_warnings:
            st.warning(f"⚠️ {warning}")
    
    # Update session state with corrected values
    st.session_state["time_window_start"] = start_sec
    st.session_state["time_window_end"] = end_sec
    
    # Get EEG picks for analysis
    picks = mne.pick_types(current_data.info, eeg=True, exclude="bads")
    
    if len(picks) == 0:
        st.error("❌ No valid EEG channels selected. Please check your channel selection.")
        return
    
    # Step 6: Visualizations
    st.divider()
    visualizer.render_visualization_panel(current_data, start_sec, end_sec, picks)
    
    # Step 7: Export Options
    st.divider()
    exporter.render_export_section(current_data, start_sec, end_sec, picks)
    
    # Show data summary in footer
    _show_data_summary(session, start_sec, end_sec)


def _file_changed(uploaded_file, session: SessionManager) -> bool:
    """Check if the uploaded file has changed."""
    current_filename = getattr(st.session_state, "last_edf_filename", None)
    current_size = getattr(st.session_state, "last_edf_size", None)
    
    new_filename = uploaded_file.name
    new_size = len(uploaded_file.getvalue())
    
    if current_filename != new_filename or current_size != new_size:
        st.session_state["last_edf_filename"] = new_filename
        st.session_state["last_edf_size"] = new_size
        return True
    
    return False


def _handle_marker_loading(raw: mne.io.BaseRaw, csv_file, json_file, session: SessionManager):
    """Handle loading of marker files."""
    if not csv_file and not json_file:
        return
    
    st.header("🏷️ Markers")
    
    total_added = 0
    
    if csv_file:
        try:
            csv_path = session.save_uploaded_file(csv_file)
            
            # Validate CSV format
            is_valid, errors = DataValidator.validate_annotations_csv(csv_path)
            if not is_valid:
                for error in errors:
                    st.error(f"❌ CSV validation failed: {error}")
            else:
                added = add_csv_markers(raw, csv_path)
                total_added += added
                if added > 0:
                    st.success(f"✅ Added {added} markers from CSV")
                
        except Exception as e:
            st.error(f"❌ Failed to load CSV markers: {str(e)}")
    
    if json_file:
        try:
            json_path = session.save_uploaded_file(json_file)
            added = add_json_markers(raw, json_path)
            total_added += added
            if added > 0:
                st.success(f"✅ Added {added} markers from JSON")
                
        except Exception as e:
            st.error(f"❌ Failed to load JSON markers: {str(e)}")
    
    if total_added > 0:
        labels = sorted(set(raw.annotations.description))
        st.info(f"📊 Total markers: {total_added} | Unique labels: {len(labels)}")
        
        # Show marker summary
        with st.expander("📋 Marker Summary", expanded=False):
            import pandas as pd
            df = pd.DataFrame({
                "Label": raw.annotations.description,
                "Onset (s)": raw.annotations.onset,
                "Duration (s)": raw.annotations.duration,
            })
            st.dataframe(df.head(20), use_container_width=True)
            if len(df) > 20:
                st.caption(f"Showing first 20 of {len(df)} markers")


def _render_time_window_selection(current_data: mne.io.BaseRaw):
    """Render time window selection interface."""
    st.header("⏱️ Time Window Selection")
    
    max_time = len(current_data.times) / current_data.info["sfreq"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Manual time selection
        start_sec, end_sec = st.slider(
            "Time interval (seconds)",
            min_value=0.0,
            max_value=max_time,
            value=(0.0, min(30.0, max_time)),
            step=0.1,
            help="Select the time window for analysis"
        )
    
    with col2:
        # Annotation-based selection
        if len(current_data.annotations) > 0:
            labels = sorted(set(current_data.annotations.description))
            label_options = ["(Manual selection)"] + labels
            
            selected_label = st.selectbox(
                "Or select by annotation",
                options=label_options,
                help="Jump to a specific annotated interval"
            )
            
            if selected_label != "(Manual selection)":
                # Find first occurrence of this label
                for onset, duration, label in zip(
                    current_data.annotations.onset, 
                    current_data.annotations.duration, 
                    current_data.annotations.description
                ):
                    if label == selected_label:
                        start_sec = float(onset)
                        end_sec = float(onset + duration)
                        break
        else:
            st.info("No annotations available for selection")
    
    # Store in session state
    st.session_state["time_window_start"] = start_sec
    st.session_state["time_window_end"] = end_sec
    
    # Show window info
    duration = end_sec - start_sec
    st.caption(f"📊 Selected window: {start_sec:.2f} - {end_sec:.2f}s (duration: {duration:.2f}s)")


def _show_data_summary(session: SessionManager, start_sec: float, end_sec: float):
    """Show data summary in an expander."""
    with st.expander("📊 Data Summary", expanded=False):
        summary = session.get_data_summary()
        
        if summary["status"] == "data_loaded":
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Channels", f"{summary['n_channels'] - summary['n_bad_channels']}/{summary['n_channels']}")
                
            with col2:
                st.metric("Sampling Rate", f"{summary['sampling_rate']:.0f} Hz")
                
            with col3:
                st.metric("Total Duration", f"{summary['duration_sec']:.1f}s")
                
            with col4:
                st.metric("Current Window", f"{end_sec - start_sec:.1f}s")
            
            # Additional info
            st.write(f"**Data Type:** {summary['data_type'].title()}")
            st.write(f"**Filters Applied:** {'Yes' if summary['filter_applied'] else 'No'}")
            st.write(f"**Annotations:** {summary['n_annotations']}")
            if summary['n_bad_channels'] > 0:
                st.write(f"**Bad Channels:** {summary['n_bad_channels']}")


def _show_welcome_info():
    """Show welcome information and instructions."""
    st.markdown("""
    ## 👋 Welcome to EEG Visualizer
    
    This application helps you analyze and visualize EEG data with powerful tools built on MNE-Python.
    
    ### 🚀 Getting Started
    1. **Upload** your EDF/EDF+ file using the sidebar
    2. **Optionally** add marker files (CSV or JSON format)
    3. **Select** channels and mark bad channels
    4. **Apply** filters and preprocessing
    5. **Choose** time windows for analysis
    6. **Visualize** your data with various plot types
    7. **Export** results and processed data
    
    ### 📁 Supported File Formats
    - **EDF/EDF+**: European Data Format for EEG recordings
    - **BDF**: BioSemi Data Format
    - **CSV Markers**: Columns: `latency`, `duration`, `type`
    - **JSON Markers**: Format: `{"Markers": [{"startDatetime": "...", "endDatetime": "...", "label": "..."}]}`
    
    ### 🎯 Analysis Features
    - **Real-time filtering** (high-pass, low-pass, notch)
    - **Topographic maps** for spatial brain activity patterns
    - **Power spectral density** analysis
    - **Event-related potentials** (ERPs)
    - **Time-frequency analysis** 
    - **Regional analysis** by brain areas
    - **Condition contrasts** for experimental comparisons
    - **Temporal animations** (GIF export)
    """)


if __name__ == "__main__":
    main()