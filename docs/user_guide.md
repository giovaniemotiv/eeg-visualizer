# User Guide

## Getting Started

1. **Start the application**
   ```bash
   streamlit run src/eegviz/app/main.py
   ```

2. **Upload your EEG file**
   - Use the file uploader in the sidebar
   - Supported formats: EDF, EDF+, BDF

3. **Add markers (optional)**
   - Upload CSV or JSON marker files
   - See file format examples below

## Basic Workflow

### 1. Load Data
- Upload an EEG file using the sidebar
- The application will validate and load the data
- Check the data summary for basic information

### 2. Select Channels
- Choose which EEG channels to analyze
- Mark bad or noisy channels to exclude them
- Use channel groups for region-specific analysis

### 3. Apply Filters
- High-pass filter: Remove slow drifts (recommended: 1 Hz)
- Low-pass filter: Remove noise (recommended: 45 Hz) 
- Notch filter: Remove line noise (50/60 Hz)

### 4. Analyze and Visualize
- Create topographic maps of brain activity
- View power spectral density plots
- Analyze activity by brain regions
- Export results and visualizations

## File Formats

### Marker Files

**CSV format:**
```csv
latency,duration,type
1.5,0.5,stimulus_onset
3.2,0.2,button_press
5.8,1.0,artifact_period
```

**JSON format:**
```json
{
  "Markers": [
    {
      "startDatetime": "2024-01-01T10:00:01.500Z",
      "endDatetime": "2024-01-01T10:00:02.000Z",
      "label": "stimulus"
    }
  ]
}
```

## Tips

- Always check data quality before analysis
- Mark obviously bad channels early in the process
- Use appropriate filter settings for your analysis type
- Start with shorter time windows for faster processing
- Export your results regularly

## Common Issues

**File won't load**: Check that your EDF file is not corrupted and follows standard format.

**Slow performance**: Try selecting fewer channels or shorter time windows.

**Empty visualizations**: Make sure you have selected valid EEG channels and your time window contains data.