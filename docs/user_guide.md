# User Guide

## Getting Started with EEG Visualizer

This comprehensive guide will walk you through every aspect of using EEG Visualizer, from loading your first EEG file to creating publication-ready visualizations and exporting results.

## Table of Contents

1. [First Steps](#first-steps)
2. [Data Loading](#data-loading)
3. [Channel Management](#channel-management)
4. [Filtering and Preprocessing](#filtering-and-preprocessing)
5. [Time Window Selection](#time-window-selection)
6. [Visualizations](#visualizations)
7. [Analysis Tools](#analysis-tools)
8. [Export and Sharing](#export-and-sharing)
9. [Advanced Features](#advanced-features)
10. [Best Practices](#best-practices)

## First Steps

### Launching the Application

1. **Open your terminal/command prompt**
2. **Navigate to the project directory**:
   ```bash
   cd path/to/eeg-visualizer
   ```
3. **Start the application**:
   ```bash
   py -m streamlit run src/eegviz/app/main.py
   ```
4. **Open your web browser** and go to `http://localhost:8501`

### Interface Overview

The EEG Visualizer interface consists of:

- **Sidebar**: File upload, channel selection, filter controls
- **Main Panel**: Visualizations, analysis results, export options
- **Header**: Application title and navigation
- **Footer**: Session information and data summary

## Data Loading

### Supported File Formats

#### EDF/EDF+ Files
- **Standard EEG format**: European Data Format
- **File extensions**: `.edf`, `.EDF`
- **Features**: Supports annotations, multiple sampling rates
- **Size limits**: Up to 500 MB (configurable)

#### BDF Files
- **BioSemi format**: 24-bit data
- **File extensions**: `.bdf`, `.BDF`
- **Features**: High-resolution recordings

### Loading Your First File

1. **Click "Browse files"** in the sidebar under "📁 Upload EDF File"
2. **Select your EEG file** from your computer
3. **Wait for processing** - you'll see a spinner and progress indicators
4. **Check the success message** - green checkmark indicates successful loading
5. **Review data summary** - basic information about your recording

#### What Happens During Loading:
- File validation and format checking
- Channel name normalization
- Electrode montage setup (10-20 system)
- Data integrity verification
- Memory allocation optimization

### Adding Markers and Annotations

EEG Visualizer supports two marker formats:

#### CSV Markers
Perfect for simple event lists:

```csv
latency,duration,type
1.5,0.5,stimulus_onset
3.2,0.2,button_press
5.8,1.0,artifact_period
10.1,0.1,stimulus_offset
```

**Required columns:**
- `latency`: Time in seconds from recording start
- `duration`: Event duration in seconds
- `type`: Event label/description

#### JSON Markers
Ideal for complex experimental data:

```json
{
  "Markers": [
    {
      "startDatetime": "2024-01-01T10:00:01.500Z",
      "endDatetime": "2024-01-01T10:00:02.000Z",
      "label": "visual_stimulus",
      "metadata": {
        "condition": "target",
        "response_time": 0.45
      }
    }
  ]
}
```

**Required fields:**
- `startDatetime`: ISO format timestamp
- `endDatetime`: ISO format timestamp  
- `label`: Event description

**Loading Markers:**
1. Upload your EDF file first
2. Use "📎 Marker Files" section in sidebar
3. Upload CSV and/or JSON marker files
4. Review marker summary in the main panel

## Channel Management

### Understanding Channel Selection

EEG analysis often requires selecting specific channels based on:
- **Brain regions** of interest
- **Data quality** 
- **Analysis type**
- **Computational resources**

### Channel Selection Interface

#### Individual Channel Selection
- **View all channels**: Expandable list of all EEG channels
- **Quick selection**: Common electrode groups (frontal, central, parietal, etc.)
- **Search functionality**: Find specific electrodes quickly

#### Channel Groups
Predefined selections for common analyses:

- **Frontal**: F3, F4, F7, F8, Fp1, Fp2, Fz
- **Central**: C3, C4, Cz
- **Parietal**: P3, P4, Pz, P7, P8
- **Occipital**: O1, O2, Oz
- **Temporal**: T3, T4, T5, T6

#### Bad Channel Management
Mark channels as "bad" when they contain:
- **Excessive noise** or artifacts
- **Flat signals** (electrode disconnection)
- **High impedance** readings
- **Continuous artifacts** (muscle, movement)

**How to mark bad channels:**
1. Review channel quality in the data browser
2. Use the "Mark as Bad" checkboxes
3. Bad channels are automatically excluded from analysis
4. Can be reversed if marked incorrectly

### Channel Quality Assessment

#### Visual Inspection
- Look for flat lines, excessive noise, or outlier values
- Compare similar channels (e.g., left vs. right hemisphere)
- Check for consistent patterns across channels

#### Automatic Detection
EEG Visualizer provides warnings for:
- Channels with unusual variance
- Flat or near-flat signals
- Channels outside normal amplitude ranges

## Filtering and Preprocessing

### Understanding EEG Filtering

Filtering removes unwanted frequency components while preserving signals of interest.

#### Filter Types

**High-Pass Filter**
- **Purpose**: Remove slow drifts and DC offsets
- **Recommended**: 0.1-1 Hz for most analyses
- **Clinical**: 0.5 Hz for routine EEG review
- **Research**: 0.1 Hz for ERP studies

**Low-Pass Filter**
- **Purpose**: Remove high-frequency noise
- **Recommended**: 40-100 Hz depending on analysis
- **Anti-aliasing**: Below Nyquist frequency (sampling_rate/2)
- **Muscle artifacts**: 30 Hz cutoff removes most EMG

**Band-Pass Filter**
- **Combination**: High-pass + Low-pass
- **Common ranges**: 
  - Clinical EEG: 0.5-70 Hz
  - ERP analysis: 0.1-30 Hz
  - Spectral analysis: 1-100 Hz

**Notch Filter**
- **Purpose**: Remove line frequency interference
- **Settings**: 50 Hz (Europe) or 60 Hz (North America)
- **Harmonics**: Also filter 100/120 Hz if present

#### Filter Interface

1. **Choose filter type** from the dropdown
2. **Set cutoff frequencies** using the sliders
3. **Preview filter response** in the frequency domain plot
4. **Apply filters** with the "Apply Filters" button
5. **Review filtered data** in the visualization panel

#### Filter Parameters

**Transition Bandwidth**
- Controls filter sharpness
- Narrower = sharper cutoff, more computational cost
- Default: 25% of cutoff frequency

**Filter Length**
- Affects filter stability and edge artifacts
- Auto-calculated for optimal performance
- Can be manually adjusted for specific needs

### Resampling

**When to resample:**
- Original sampling rate > 500 Hz for most analyses
- Computational efficiency for large datasets
- Standardizing across different recordings

**Guidelines:**
- Maintain > 2× highest frequency of interest
- 250 Hz sufficient for most clinical EEG
- 500 Hz for high-gamma analysis
- 1000 Hz for high-frequency oscillations

## Time Window Selection

### Choosing Analysis Windows

#### Considerations
- **Analysis type**: ERPs need event-locked windows
- **Frequency resolution**: Longer windows = better frequency resolution
- **Computational load**: Shorter windows = faster processing
- **Statistical power**: More data = better statistics

#### Selection Methods

**Manual Selection**
- Use the time slider to select start/end points
- Precise control over analysis window
- Visual feedback with waveform display

**Annotation-Based Selection**
- Jump to specific experimental events
- Automatically set windows around markers
- Useful for event-related analysis

**Multiple Windows**
- Analyze different time periods
- Compare pre/post conditions
- Time-course analysis

### Time Window Validation

EEG Visualizer automatically:
- Checks window is within data range
- Warns about very short/long windows
- Validates marker-based selections
- Corrects invalid time ranges

## Visualizations

### Topographic Maps

**Purpose**: Show spatial distribution of brain activity

#### When to Use
- Understanding spatial patterns
- Identifying artifact sources
- Publication figures
- Clinical interpretation

#### Parameters
- **Time point**: Specific moment to visualize
- **Averaging window**: Time around selected point
- **Interpolation**: Smooth vs. discrete visualization
- **Color scale**: Data range and colormap

#### Interpretation Tips
- **Hot colors** (red): High positive values
- **Cool colors** (blue): High negative values or low power
- **Symmetric scale**: Centers around zero for ERP data
- **Asymmetric scale**: For power/magnitude data

### Power Spectral Density (PSD)

**Purpose**: Analyze frequency content of EEG signals

#### Applications
- Sleep stage analysis
- Attention/arousal states
- Pathological oscillations
- Medication effects

#### Parameters
- **Frequency range**: Focus on specific bands
- **Window method**: Welch (recommended) vs. multitaper
- **Overlap**: Window overlap percentage
- **Averaging**: Across channels or time

#### Interpretation
- **Alpha peak** (8-13 Hz): Relaxed wakefulness
- **Beta activity** (13-30 Hz): Active thinking
- **Theta increase** (4-8 Hz): Drowsiness
- **Delta dominance** (0.5-4 Hz): Deep sleep

### Raw Data Browser

**Purpose**: Examine continuous EEG data

#### Features
- **Multi-channel display**: All selected channels
- **Zooming**: Time and amplitude scaling
- **Scrolling**: Navigate through recording
- **Annotation overlay**: View markers and events

#### Navigation
- Use mouse wheel to zoom in/out
- Click and drag to pan
- Keyboard shortcuts for quick navigation
- Jump to specific time points

### Regional Analysis

**Purpose**: Compare activity across brain regions

#### Brain Regions
- **Frontal**: Executive functions, attention
- **Parietal**: Spatial processing, attention
- **Temporal**: Language, memory
- **Occipital**: Visual processing
- **Central**: Motor functions

#### Visualization Options
- **Bar charts**: Compare average power/amplitude
- **Box plots**: Show distribution and outliers
- **Time series**: Regional activity over time
- **Correlation matrices**: Inter-regional connectivity

### Temporal Animations (GIFs)

**Purpose**: Show brain activity evolution over time

#### Applications
- **Presentations**: Dynamic visualization for talks
- **Social media**: Engaging content for outreach
- **Education**: Teaching brain dynamics
- **Research**: Understanding temporal patterns

#### Parameters
- **Time range**: Period to animate
- **Frame rate**: Smooth vs. fast animation
- **Duration**: Total animation length
- **Resolution**: Quality vs. file size

## Analysis Tools

### Frequency Band Analysis

#### Standard EEG Bands

**Delta (0.5-4 Hz)**
- Associated with deep sleep
- Increased in pathological conditions
- Normal in very young children

**Theta (4-8 Hz)**
- Present during drowsiness
- Increased during meditation
- Memory encoding processes

**Alpha (8-13 Hz)**
- Relaxed wakefulness, eyes closed
- Reduced during mental activity
- Individual peak frequency varies

**Beta (13-30 Hz)**
- Active thinking and concentration
- Motor planning and execution
- Can indicate anxiety if excessive

**Gamma (30-100 Hz)**
- Cognitive binding processes
- Attention and consciousness
- Requires careful artifact control

#### Custom Band Definition
- Define your own frequency ranges
- Multiple bands for specific research
- Compare different frequency windows

### Statistical Analysis

#### Band Power Comparisons
- **Absolute power**: Raw power in each band
- **Relative power**: Proportion of total power
- **Power ratios**: Between different bands
- **Normalized power**: Z-scored or baseline corrected

#### Condition Contrasts
- **Paired comparisons**: Before vs. after
- **Between groups**: Patients vs. controls  
- **Multiple conditions**: ANOVA-style analysis
- **Effect sizes**: Cohen's d, eta-squared

#### Statistical Tests
- **T-tests**: Paired and independent samples
- **Wilcoxon tests**: Non-parametric alternatives
- **Permutation tests**: Distribution-free methods
- **Multiple comparisons**: FDR correction

### Event-Related Analysis

#### Epoch Extraction
- **Time-locked segments**: Around specific events
- **Baseline correction**: Pre-stimulus normalization
- **Artifact rejection**: Automatic and manual
- **Averaging**: Across trials and subjects

#### ERP Components
- **P300**: Attention and memory (300ms, positive)
- **N400**: Language processing (400ms, negative)
- **MMN**: Auditory change detection (150-250ms)
- **CNV**: Expectancy and preparation (slow wave)

#### Analysis Options
- **Peak detection**: Amplitude and latency
- **Area under curve**: Component strength
- **Topographic analysis**: Spatial distribution
- **Time-frequency**: Induced oscillations

## Export and Sharing

### Export Formats

#### Processed Data
**EDF Format**
- Standard for EEG data sharing
- Preserves all metadata and annotations
- Compatible with most EEG software

**FIF Format**
- MNE-Python native format
- Includes all preprocessing information
- Fastest loading for future analysis

**CSV Format**
- Simple data matrix
- Easy import to Excel, R, MATLAB
- Good for statistical analysis

#### Visualizations
**PNG Images**
- High resolution for publications
- Adjustable DPI (dots per inch)
- Transparent backgrounds available

**SVG Vector Graphics**
- Scalable for any size
- Editable in vector graphics software
- Perfect for illustrations

**PDF Documents**
- Multi-page reports
- Combined figures and text
- Ready for publication

#### Analysis Results
**Excel Workbooks**
- Multiple sheets for different analyses
- Formatted tables and charts
- Easy sharing with collaborators

**JSON Data**
- Structured analysis results
- Machine-readable format
- API integration friendly

### Export Workflow

1. **Select export type** from the export panel
2. **Choose format and quality** settings
3. **Customize filename** and metadata
4. **Preview before export** (when available)
5. **Download files** to your computer

### Sharing and Collaboration

#### Data Sharing Best Practices
- **Remove identifying information** before sharing
- **Document preprocessing steps** for reproducibility
- **Include methodology** descriptions
- **Version control** for analysis scripts

#### Publication Workflow
1. **Standardize visualizations** across figures
2. **High-resolution exports** for print quality
3. **Color accessibility** for colorblind readers
4. **Consistent formatting** and fonts

## Advanced Features

### Batch Processing

#### Multiple File Analysis
- Load and process multiple EEG files
- Consistent preprocessing pipeline
- Aggregate results across subjects
- Export combined datasets

#### Automated Pipelines
- Define preprocessing steps once
- Apply to new data automatically
- Quality control checkpoints
- Error handling and logging

### Custom Analysis Scripts

#### Integration with Jupyter
- Export data for notebook analysis
- Custom visualization code
- Advanced statistical methods
- Machine learning applications

#### Python API Access
```python
from eegviz.core import SessionManager
from eegviz.analysis import compute_band_powers

# Load session data
session = SessionManager()
raw = session.raw_data

# Custom analysis
results = compute_band_powers(raw, custom_bands)
```

### Advanced Visualizations

#### 3D Brain Plots
- Source localization visualization
- Cortical surface mapping
- Interactive rotation and zooming
- Multiple view angles

#### Connectivity Analysis
- Coherence between channels
- Phase-locking values
- Network graphs
- Functional connectivity matrices

#### Time-Frequency Analysis
- Spectrograms for single trials
- Event-related spectral perturbation
- Inter-trial coherence
- Wavelets and Hilbert transforms

## Best Practices

### Data Quality Control

#### Before Analysis
1. **Visual inspection** of raw data
2. **Check channel labels** and locations
3. **Identify obvious artifacts** early
4. **Verify sampling rate** and timing

#### During Preprocessing
1. **Conservative filtering** initially
2. **Document all steps** for reproducibility
3. **Save intermediate results**
4. **Quality checks** after each step

#### After Analysis
1. **Sanity checks** on results
2. **Compare with literature** values
3. **Statistical validation**
4. **Peer review** when possible

### Computational Efficiency

#### For Large Datasets
- **Downsample** when appropriate
- **Select relevant channels** only
- **Use shorter time windows** for exploration
- **Process in chunks** if necessary

#### Memory Management
- **Close unnecessary applications**
- **Monitor memory usage** in debug mode
- **Use swap space** if available
- **Consider cloud computing** for very large analyses

### Analysis Strategy

#### Exploratory Phase
1. **Broad overview** of data quality
2. **Quick visualizations** to understand patterns
3. **Identify interesting** features or artifacts
4. **Plan detailed analysis** based on findings

#### Confirmatory Phase
1. **Hypothesis-driven** analysis
2. **Rigorous statistical** testing
3. **Control for multiple** comparisons
4. **Validate findings** with independent data

### Reproducibility Guidelines

#### Documentation
- **Record all parameters** used
- **Note software versions**
- **Describe data sources**
- **Include rationale** for choices

#### Version Control
- **Save analysis scripts**
- **Track parameter changes**
- **Backup original data**
- **Archive final results**

### Troubleshooting Common Issues

#### Performance Problems
- **Reduce time window** size
- **Select fewer channels**
- **Lower visualization** resolution
- **Close other applications**

#### Visualization Issues
- **Check data scaling**
- **Verify channel selection**
- **Adjust color ranges**
- **Try different plot types**

#### Analysis Errors
- **Validate input parameters**
- **Check for NaN values**
- **Verify time ranges**
- **Review preprocessing steps**

## Getting Help

### Built-in Help
- **Tooltips**: Hover over interface elements
- **Error messages**: Detailed problem descriptions
- **Validation warnings**: Automatic data checking
- **Debug mode**: Detailed system information

### Community Resources
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and tutorials
- **Example datasets**: Practice with sample data
- **Video tutorials**: Step-by-step walkthroughs

### Professional Support
- **Consulting services**: Custom analysis workflows
- **Training workshops**: In-person or virtual
- **Technical support**: Installation and troubleshooting
- **Custom development**: Feature requests and modifications

---

This user guide provides comprehensive information for using EEG Visualizer effectively. For additional help, consult the other documentation files or reach out to the community support channels.