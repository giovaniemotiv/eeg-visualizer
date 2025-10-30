# 🧠 EEG Visualizer# EEG Visualizer (Streamlit + MNE-Python)



A comprehensive, user-friendly EEG analysis and visualization application built with MNE-Python and Streamlit. Load EDF/EDF+ files, apply advanced filtering, create stunning visualizations, and export results with just a few clicks.A modular, testable project scaffold for visualizing Emotiv EDF/EDF+ EEG data with MNE-Python.

Includes a Streamlit UI and a clean package layout (`src/eegviz`).

![Python](https://img.shields.io/badge/python-3.8%2B-blue)

![MNE](https://img.shields.io/badge/MNE--Python-1.10%2B-green)## Quickstart

![Streamlit](https://img.shields.io/badge/Streamlit-1.33%2B-red)```bash

![License](https://img.shields.io/badge/license-MIT-yellow)pip install -e .[dev]

streamlit run src/eegviz/app/main.py

## 🎯 Key Features```


### 📊 **Data Loading & Preprocessing**
- **Multiple file format support**: EDF, EDF+, BDF files
- **Marker integration**: Import annotations from CSV or JSON files
- **Channel management**: Interactive channel selection and bad channel marking
- **Real-time filtering**: High-pass, low-pass, band-pass, and notch filters
- **Data validation**: Comprehensive error checking and warnings

### 🎨 **Advanced Visualizations**
- **Topographic maps**: Spatial distribution of brain activity
- **Power Spectral Density (PSD)**: Frequency domain analysis
- **Regional analysis**: Brain activity by anatomical regions
- **Temporal animations**: Export time-lapse GIFs of brain activity
- **Raw data browser**: Interactive time-series visualization
- **Event-related analysis**: Compare conditions and contrasts

### 🔧 **Analysis Tools**
- **Band power analysis**: Alpha, beta, gamma, theta frequency bands
- **Time-frequency analysis**: Spectrograms and time-frequency maps
- **Epoch extraction**: Event-locked data analysis
- **Statistical contrasts**: Compare different experimental conditions
- **Custom time windows**: Analyze specific time intervals

### 💾 **Export Capabilities**
- **Processed data**: Save filtered EEG data in multiple formats
- **Visualizations**: High-quality PNG/SVG plots
- **Analysis results**: CSV exports of band power and statistics
- **Annotations**: Export marker data and analysis windows
- **Animated GIFs**: Time-lapse brain activity movies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/eeg-visualizer.git
   cd eeg-visualizer
   ```

2. **Install dependencies**
   ```bash
   # Using pip
   pip install -e src/

   # Or using conda
   conda env create -f environment.yml
   conda activate eeg-visualizer
   ```

3. **Run the application**
   ```bash
   py -m streamlit run src/eegviz/app/main.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start analyzing your EEG data!

## 📁 Project Structure

```
eeg-visualizer/
├── src/
│   ├── pyproject.toml          # Package configuration and dependencies
│   └── eegviz/                 # Main package
│       ├── __init__.py
│       ├── config.py           # Global configuration settings
│       ├── types.py            # Type definitions and data structures
│       │
│       ├── app/
│       │   └── main.py         # 🎯 Main Streamlit application
│       │
│       ├── core/               # 🏗️ Core business logic
│       │   ├── __init__.py
│       │   ├── session.py      # Session state management
│       │   ├── validation.py   # Data validation and error checking
│       │   └── epochs.py       # Epoch handling and extraction
│       │
│       ├── ui/                 # 🎨 User interface components
│       │   ├── __init__.py
│       │   ├── upload.py       # File upload interface
│       │   ├── channels.py     # Channel selection controls
│       │   ├── filters.py      # Filter parameter controls
│       │   ├── visualizations.py  # Visualization panel
│       │   └── exports.py      # Export options interface
│       │
│       ├── io/                 # 📤 Input/output operations
│       │   ├── __init__.py
│       │   ├── edf_loader.py   # EDF/EDF+ file loading
│       │   ├── markers_csv.py  # CSV marker import
│       │   └── markers_json.py # JSON marker import
│       │
│       ├── preprocess/         # 🔧 Data preprocessing
│       │   ├── __init__.py
│       │   ├── filtering.py    # Signal filtering functions
│       │   ├── channels.py     # Channel operations (montage, naming)
│       │   └── windows.py      # Time window operations
│       │
│       ├── analysis/           # 📊 Signal analysis
│       │   ├── __init__.py
│       │   ├── bands.py        # Frequency band analysis
│       │   ├── psd.py          # Power spectral density
│       │   └── contrast.py     # Condition comparisons
│       │
│       ├── viz/                # 📈 Visualization modules
│       │   ├── __init__.py
│       │   ├── topomap.py      # Topographic mapping
│       │   ├── psd_plot.py     # PSD plotting
│       │   ├── regional.py     # Regional brain plots
│       │   └── temporal_gif.py # Animated visualizations
│       │
│       └── export/             # 💾 Export utilities
│           ├── __init__.py
│           ├── save_raw.py     # Raw data export
│           ├── bandpower_csv.py # Band power CSV export
│           └── annotations.py  # Annotation export
│
├── tests/                      # 🧪 Unit tests
│   ├── conftest.py
│   └── test_*.py
│
├── docs/                       # 📚 Documentation (optional)
├── examples/                   # 💡 Example datasets and workflows
├── LICENSE                     # 📄 MIT License
└── README.md                   # 📖 This file
```

## 🔧 Detailed Usage Guide

### 1. Loading EEG Data

#### Supported File Formats
- **EDF (European Data Format)**: Standard format for EEG recordings
- **EDF+**: Enhanced EDF with discontinuous recordings support
- **BDF**: BioSemi Data Format (24-bit)

#### Steps:
1. Click "Browse files" in the sidebar
2. Select your EDF/EDF+ file
3. Wait for automatic loading and validation
4. Check the data summary for basic information

### 2. Adding Markers/Annotations

#### CSV Format
Create a CSV file with columns:
```csv
latency,duration,type
1.5,0.5,"stimulus_start"
3.2,1.0,"response"
10.1,0.1,"artifact"
```

#### JSON Format
Structure your JSON file as:
```json
{
  "Markers": [
    {
      "startDatetime": "2024-01-01T10:00:01.500Z",
      "endDatetime": "2024-01-01T10:00:02.000Z",
      "label": "stimulus_start"
    }
  ]
}
```

### 3. Channel Selection and Management

#### Channel Operations:
- **Select channels**: Choose specific EEG channels for analysis
- **Mark bad channels**: Exclude noisy or artifact-contaminated channels
- **Channel groups**: Select by region (frontal, parietal, etc.)
- **Montage setting**: Automatic 10-20 electrode positioning

#### Best Practices:
- Review channel quality before analysis
- Mark obviously bad channels early
- Use channel groups for region-specific analysis

### 4. Filtering and Preprocessing

#### Available Filters:
- **High-pass filter**: Remove slow drifts (recommended: 0.1-1 Hz)
- **Low-pass filter**: Remove high-frequency noise (recommended: 40-100 Hz)
- **Notch filter**: Remove line noise (50/60 Hz)
- **Band-pass filter**: Combine high and low-pass

#### Recommended Settings:
```
ERP Analysis:     0.1-30 Hz
Spectral Analysis: 1-100 Hz
Gamma Studies:    1-200 Hz (if sampling rate allows)
Clinical Review:  0.5-70 Hz
```

#### Resampling:
- Downsample high-frequency data to reduce computational load
- Maintain at least 2x the highest frequency of interest (Nyquist criterion)

### 5. Time Window Selection

#### Methods:
1. **Manual selection**: Use slider to select start/end times
2. **Annotation-based**: Jump to specific annotated events
3. **Epoch analysis**: Extract multiple time-locked segments

#### Considerations:
- Longer windows: Better frequency resolution, more computational time
- Shorter windows: Better temporal resolution, faster processing
- Event-locked windows: Essential for ERP analysis

### 6. Visualization Options

#### Topographic Maps
- **Usage**: Spatial distribution of brain activity
- **Parameters**: Time point, frequency band, interpolation method
- **Best for**: Understanding spatial patterns, identifying artifacts

#### Power Spectral Density (PSD)
- **Usage**: Frequency domain analysis
- **Parameters**: Window method, frequency range, averaging
- **Best for**: Spectral power analysis, frequency band comparisons

#### Regional Analysis
- **Usage**: Activity by brain regions (frontal, parietal, etc.)
- **Parameters**: Region selection, aggregation method
- **Best for**: Comparing activity across brain areas

#### Temporal GIFs
- **Usage**: Time-lapse animations of brain activity
- **Parameters**: Time range, frame rate, visualization type
- **Best for**: Presentations, understanding temporal dynamics

### 7. Advanced Analysis Features

#### Band Power Analysis
```python
# Frequency bands analyzed:
Delta:   0.5-4 Hz   (deep sleep, pathology)
Theta:   4-8 Hz     (drowsiness, meditation)
Alpha:   8-13 Hz    (relaxed wakefulness)
Beta:    13-30 Hz   (active thinking)
Gamma:   30-100 Hz  (cognitive processes)
```

#### Condition Contrasts
- Compare different experimental conditions
- Statistical testing between groups
- Effect size calculations
- Multiple comparison corrections

#### Event-Related Analysis
- Extract epochs around specific events
- Average across trials
- Peak detection and latency analysis
- Component identification (P300, N400, etc.)

### 8. Export and Save Results

#### Available Export Formats:

1. **Processed EEG Data**
   - EDF format (standard)
   - FIF format (MNE native)
   - MAT format (MATLAB)

2. **Visualizations**
   - PNG (high resolution)
   - SVG (vector graphics)
   - PDF (publication ready)

3. **Analysis Results**
   - CSV (band power, statistics)
   - Excel (formatted tables)
   - JSON (structured data)

4. **Animations**
   - GIF (presentations)
   - MP4 (video format)

## ⚙️ Configuration

### Global Settings (`config.py`)
```python
# Visualization defaults
DEFAULT_COLORMAP = "RdBu_r"
DEFAULT_DPI = 150
ANIMATION_FPS = 10

# Analysis parameters
DEFAULT_BANDS = {
    "delta": (0.5, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
    "gamma": (30, 100)
}

# File handling
MAX_FILE_SIZE_MB = 500
TEMP_DIR = "temp_data"
```

### Environment Variables
```bash
# Optional: Set custom temporary directory
export EEGVIZ_TEMP_DIR="/path/to/temp"

# Optional: Set custom cache directory
export EEGVIZ_CACHE_DIR="/path/to/cache"

# Optional: Enable debug mode
export EEGVIZ_DEBUG=true
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=eegviz

# Run specific test file
python -m pytest tests/test_bands.py -v
```

### Test Structure
```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_bands.py           # Band analysis tests
├── test_validation.py      # Data validation tests
├── test_session.py         # Session management tests
├── test_filters.py         # Filtering tests
└── test_exports.py         # Export functionality tests
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. File Loading Problems
**Problem**: "Failed to load EDF file"
**Solutions**:
- Ensure file is not corrupted
- Check file permissions
- Verify EDF format compliance
- Try converting with MNE-Python directly:
  ```python
  import mne
  raw = mne.io.read_raw_edf("your_file.edf", preload=True)
  ```

#### 2. Memory Issues
**Problem**: "Out of memory" errors
**Solutions**:
- Reduce time window size
- Downsample data before analysis
- Close other applications
- Use `preload=False` for large files

#### 3. Visualization Errors
**Problem**: Plots not displaying correctly
**Solutions**:
- Check channel selection (need EEG channels)
- Verify time window is within data range
- Ensure proper montage is set
- Check for NaN values in data

#### 4. Filter Application Issues
**Problem**: Filtering fails or produces artifacts
**Solutions**:
- Check filter parameters (cutoff frequencies)
- Ensure adequate sampling rate
- Use appropriate filter transitions
- Check for data discontinuities

#### 5. Export Problems
**Problem**: Export fails or corrupted files
**Solutions**:
- Check available disk space
- Verify write permissions
- Try different export formats
- Close files before re-exporting

### Debug Mode

Enable debug mode for detailed information:
1. Check "Debug Mode" in the sidebar
2. View session state information
3. Monitor memory usage
4. See detailed error messages

### Performance Optimization

#### For Large Files:
1. **Downsample**: Reduce sampling rate if appropriate
2. **Chunk analysis**: Process data in smaller time windows
3. **Channel selection**: Analyze fewer channels
4. **Preload control**: Use `preload=False` for exploration

#### For Better Visualization:
1. **Adjust DPI**: Lower for faster rendering, higher for publication
2. **Color maps**: Choose perceptually uniform colormaps
3. **Interpolation**: Balance quality vs. speed
4. **Animation settings**: Reduce frame rate for faster export

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/your-username/eeg-visualizer.git
cd eeg-visualizer

# Install in development mode
pip install -e src/[dev]

# Install pre-commit hooks
pre-commit install
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Document functions with docstrings
- Write unit tests for new features

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📚 API Reference

### Core Classes

#### `SessionManager`
Manages application state and user session data.
```python
from eegviz.core.session import SessionManager

session = SessionManager()
session.raw_data = your_mne_raw_object
summary = session.get_data_summary()
```

#### `DataValidator`
Validates input data and parameters.
```python
from eegviz.core.validation import DataValidator

is_valid, warnings = DataValidator.validate_raw_data(raw)
errors = DataValidator.validate_filter_params(raw, l_freq=1, h_freq=40)
```

#### UI Components
All UI components follow the same pattern:
```python
from eegviz.ui.filters import FilterControlsComponent

filter_controls = FilterControlsComponent()
params, apply = filter_controls.render_filter_controls(raw)
processed = filter_controls.apply_filters(raw, params)
```

### Analysis Functions

#### Band Power Analysis
```python
from eegviz.analysis.bands import compute_band_powers

powers = compute_band_powers(
    raw, 
    bands={"alpha": (8, 13), "beta": (13, 30)},
    method="welch"
)
```

#### Visualization
```python
from eegviz.viz.topomap import plot_topomap

fig = plot_topomap(
    raw, 
    time_point=1.0,
    colormap="RdBu_r",
    contours=6
)
```

## 🌟 Examples and Use Cases

### 1. Clinical EEG Review
```python
# Load clinical EEG
raw = load_edf("clinical_recording.edf")

# Apply clinical filters
raw.filter(l_freq=0.5, h_freq=70)
raw.notch_filter(freqs=60)  # US line frequency

# Review by pages
plot_time_series(raw, duration=10, scalings="auto")
```

### 2. Research ERP Analysis
```python
# Load research data with events
raw = load_edf("erp_experiment.edf")
events = load_csv_markers("stimulus_events.csv")

# Preprocess for ERP
raw.filter(l_freq=0.1, h_freq=30)
epochs = create_epochs(raw, events, tmin=-0.2, tmax=0.8)

# Analyze ERP components
evoked = epochs.average()
plot_evoked_topomap(evoked, times=[0.1, 0.2, 0.3])
```

### 3. Sleep Study Analysis
```python
# Load overnight recording
raw = load_edf("sleep_study.edf")

# Focus on sleep frequencies
raw.filter(l_freq=0.5, h_freq=35)

# Analyze sleep stages
band_powers = compute_band_powers(raw, window_length=30)
plot_hypnogram(band_powers)
```

### 4. Neurofeedback Application
```python
# Real-time analysis setup
raw = load_edf("neurofeedback_session.edf")

# Focus on specific frequency bands
alpha_power = compute_alpha_power(raw, realtime=True)
plot_realtime_feedback(alpha_power)
```

## 📊 Data Examples

### Sample Datasets
The `examples/` directory contains sample datasets:

1. **`sample_eeg.edf`**: 10-minute resting state EEG (32 channels)
2. **`erp_experiment.edf`**: ERP paradigm with stimulus markers
3. **`clinical_sample.edf`**: Clinical EEG with annotations
4. **`sleep_demo.edf`**: Short sleep recording segment

### Marker File Examples
- **`stimuli.csv`**: Event markers for experimental paradigms
- **`clinical_events.json`**: Clinical annotations and artifacts
- **`sleep_stages.csv`**: Sleep stage annotations

## 🆘 Support and Resources

### Documentation
- [MNE-Python Documentation](https://mne.tools/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [EEG Analysis Tutorials](https://mne.tools/stable/auto_tutorials/)

### Community
- [GitHub Issues](https://github.com/your-username/eeg-visualizer/issues): Bug reports and feature requests
- [Discussions](https://github.com/your-username/eeg-visualizer/discussions): Questions and community support
- [MNE Forum](https://mne.discourse.group/): General EEG analysis questions

### Citation
If you use EEG Visualizer in your research, please cite:
```bibtex
@software{eeg_visualizer,
  title={EEG Visualizer: A Comprehensive EEG Analysis Tool},
  author={Your Name},
  year={2024},
  url={https://github.com/your-username/eeg-visualizer}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MNE-Python Team**: For the excellent EEG analysis library
- **Streamlit Team**: For the amazing web app framework
- **EEG Community**: For feedback and contributions
- **Contributors**: Everyone who has helped improve this project

---

<div align="center">

**Made with ❤️ for the EEG research community**

[⭐ Star this repo](https://github.com/your-username/eeg-visualizer) | [🐛 Report bug](https://github.com/your-username/eeg-visualizer/issues) | [💡 Request feature](https://github.com/your-username/eeg-visualizer/issues)

</div>