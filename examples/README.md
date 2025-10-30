# Example Workflows

This directory contains example datasets and step-by-step workflows for common EEG analysis tasks using EEG Visualizer.

## Available Examples

### 1. Basic EEG Analysis (`basic_eeg_workflow.md`)
- Load EDF file
- Basic preprocessing
- Channel selection
- Simple visualizations
- Export results

### 2. Event-Related Potential Analysis (`erp_analysis.md`)
- Load experimental data with markers
- Epoch extraction around events
- ERP averaging and visualization
- Statistical analysis
- Publication-ready figures

### 3. Sleep Stage Analysis (`sleep_analysis.md`)
- Load overnight sleep recording
- Spectral analysis
- Sleep stage visualization
- Hypnogram creation
- Sleep metrics calculation

### 4. Clinical EEG Review (`clinical_workflow.md`)
- Load clinical EEG recording
- Artifact identification
- Abnormality detection
- Report generation
- Annotation export

### 5. Frequency Band Analysis (`frequency_bands.md`)
- Band power calculation
- Topographic mapping
- Regional comparisons
- Statistical testing
- Results export

## Sample Data Files

### `sample_eeg.edf`
- **Description**: 10-minute resting-state EEG recording
- **Channels**: 32 EEG channels (10-20 system)
- **Sampling Rate**: 500 Hz
- **Conditions**: Eyes closed, relaxed state
- **Use Cases**: Basic analysis, visualization testing

### `erp_experiment.edf`
- **Description**: Visual oddball paradigm
- **Channels**: 64 EEG channels
- **Sampling Rate**: 1000 Hz
- **Events**: Target and non-target stimuli
- **Use Cases**: ERP analysis, event-related studies

### `sleep_recording.edf`
- **Description**: 2-hour sleep segment
- **Channels**: 6 EEG channels + EOG + EMG
- **Sampling Rate**: 200 Hz
- **Stages**: Wake, N1, N2, N3, REM
- **Use Cases**: Sleep analysis, spectral studies

### `clinical_sample.edf`
- **Description**: Clinical EEG with abnormalities
- **Channels**: 21 EEG channels
- **Sampling Rate**: 256 Hz
- **Features**: Spike-wave complexes, artifacts
- **Use Cases**: Clinical training, artifact detection

## Marker Files

### `visual_stimuli.csv`
```csv
latency,duration,type
1.5,0.1,target_stimulus
3.2,0.1,non_target_stimulus
5.8,0.1,target_stimulus
8.1,0.1,non_target_stimulus
```

### `sleep_stages.csv`
```csv
latency,duration,type
0,30,wake
30,30,stage_1
60,30,stage_2
90,30,stage_2
120,30,stage_3
```

### `clinical_events.json`
```json
{
  "Markers": [
    {
      "startDatetime": "2024-01-01T10:00:05.500Z",
      "endDatetime": "2024-01-01T10:00:06.000Z",
      "label": "spike_wave_complex"
    },
    {
      "startDatetime": "2024-01-01T10:01:15.200Z",
      "endDatetime": "2024-01-01T10:01:17.800Z",
      "label": "muscle_artifact"
    }
  ]
}
```

## Quick Start Guide

1. **Download sample data**: Get `sample_eeg.edf` from this directory
2. **Start EEG Visualizer**: Run `py -m streamlit run src/eegviz/app/main.py`
3. **Upload the sample file**: Use the file upload in the sidebar
4. **Follow a workflow**: Choose one of the example workflows below
5. **Experiment**: Try different settings and visualizations

## Workflow Examples

### Basic Visualization Workflow

1. **Load Data**
   - Upload `sample_eeg.edf`
   - Review data summary (32 channels, 500 Hz, 10 minutes)

2. **Select Channels**
   - Keep all EEG channels
   - Mark any obviously bad channels

3. **Apply Filters**
   - High-pass: 0.5 Hz
   - Low-pass: 40 Hz
   - Notch: 60 Hz (or 50 Hz depending on location)

4. **Choose Time Window**
   - Start: 60 seconds (avoid start artifacts)
   - Duration: 10 seconds for initial exploration

5. **Create Visualizations**
   - Topographic map at a representative time point
   - Power spectral density across all channels
   - Regional analysis by brain area

6. **Export Results**
   - Save topographic map as PNG
   - Export PSD data as CSV
   - Save filtered data as EDF

### ERP Analysis Workflow

1. **Prepare Data**
   - Upload `erp_experiment.edf`
   - Upload `visual_stimuli.csv` markers

2. **Preprocessing**
   - High-pass filter: 0.1 Hz
   - Low-pass filter: 30 Hz
   - Select relevant channels (Pz, Cz, Fz for P300)

3. **Epoch Analysis**
   - Extract epochs around target stimuli
   - Time window: -200 to +800 ms
   - Baseline correction: -200 to 0 ms

4. **Visualize ERPs**
   - Average across trials
   - Plot ERP waveforms
   - Create topographic maps at key time points

5. **Statistical Analysis**
   - Compare target vs. non-target conditions
   - Peak detection around 300 ms
   - Export statistics and figures

### Sleep Analysis Workflow

1. **Load Sleep Data**
   - Upload `sleep_recording.edf`
   - Upload `sleep_stages.csv` if available

2. **Configure for Sleep**
   - High-pass: 0.3 Hz
   - Low-pass: 35 Hz
   - Focus on central channels (C3, C4)

3. **Spectral Analysis**
   - Calculate PSD in 30-second epochs
   - Focus on sleep-relevant bands:
     - Delta: 0.5-4 Hz
     - Theta: 4-8 Hz
     - Alpha: 8-13 Hz
     - Sigma: 11-15 Hz (sleep spindles)

4. **Sleep Stage Visualization**
   - Plot spectral power over time
   - Create hypnogram
   - Identify sleep stages and transitions

5. **Sleep Metrics**
   - Calculate sleep efficiency
   - REM latency
   - Deep sleep percentage

## Tips for Each Workflow

### General Tips
- Always start with data quality assessment
- Use conservative filtering initially
- Document all preprocessing steps
- Save intermediate results

### ERP-Specific Tips
- Use liberal artifact rejection initially
- Check for adequate trial numbers
- Baseline correction is crucial
- Consider individual differences

### Sleep-Specific Tips
- Use appropriate scoring epoch length (30s)
- Focus on central electrodes
- Consider age-related normative values
- Account for first-night effects

### Clinical-Specific Tips
- Follow standard clinical montages
- Use clinical filter settings
- Document abnormalities systematically
- Consider referential vs. bipolar montages

## Troubleshooting Common Issues

### File Loading Problems
- Check file format (EDF/EDF+ supported)
- Verify file isn't corrupted
- Ensure file size is reasonable (<500MB)

### Memory Issues
- Reduce time window size
- Select fewer channels
- Downsample if appropriate

### Visualization Problems
- Check channel selection
- Verify time window is valid
- Adjust scaling if plots look strange

### Analysis Errors
- Validate filter parameters
- Check for sufficient data length
- Ensure proper epoch definitions

## Creating Your Own Examples

To add new example workflows:

1. **Prepare sample data** (anonymized, small file size)
2. **Write step-by-step instructions**
3. **Include expected results**
4. **Test with fresh installation**
5. **Document any special requirements**

## Contributing Examples

We welcome community contributions of example workflows! Please:

1. Fork the repository
2. Add your example to this directory
3. Include sample data (if possible) or clear instructions
4. Write clear, step-by-step instructions
5. Test thoroughly
6. Submit a pull request

## Support

For help with examples:
- Check the main documentation
- Review error messages carefully
- Ask questions in GitHub Discussions
- Report bugs in GitHub Issues

---

These examples provide hands-on experience with EEG Visualizer's capabilities. Start with the basic workflow and progress to more advanced analyses as you become comfortable with the interface.