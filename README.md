# EEG Visualizer

A web-based EEG analysis tool built with MNE-Python and Streamlit.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![MNE](https://img.shields.io/badge/MNE--Python-1.10%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33%2B-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Features

- Load EDF/EDF+ files with automatic validation
- Import event markers from CSV or JSON files
- Interactive channel selection and bad channel marking
- Real-time filtering (high-pass, low-pass, notch)
- Topographic brain maps
- Power spectral density analysis
- Regional brain activity analysis
- Export processed data and visualizations

## Quick Start

### Installation

```bash
git clone https://github.com/your-username/eeg-visualizer.git
cd eeg-visualizer
pip install -e src/
```

### Running the Application

**Method 1: Using Python module (Recommended)**
```bash
py -m streamlit run src/eegviz/app/main.py
```

**Method 2: Direct streamlit command**
```bash
streamlit run src/eegviz/app/main.py
```

**Method 3: With specific port**
```bash
py -m streamlit run src/eegviz/app/main.py --server.port 8502
```

### Access the Application

Open your browser and go to `http://localhost:8501` (or the port shown in the terminal output).

### Troubleshooting

**If streamlit command is not found:**
- Use Method 1 with `py -m streamlit`
- Make sure Streamlit is installed: `pip install streamlit`

**If port is already in use:**
- Use Method 3 to specify a different port
- Or the application will automatically find an available port

## Project Structure

```
src/eegviz/
├── app/main.py        # Streamlit application
├── core/              # Session management and validation
├── ui/                # UI components
├── io/                # File loading
├── analysis/          # Signal analysis
├── viz/               # Visualization
└── export/            # Data export
```

## File Formats

### EDF Files
Standard EEG recording format with annotation support.

### Marker Files

**CSV format:**
```csv
latency,duration,type
1.5,0.5,stimulus
3.2,0.2,response
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

## Development

### Dependencies

Core requirements:
- mne>=1.10.1
- streamlit>=1.33
- matplotlib>=3.7
- numpy>=1.24
- pandas>=2.0

### Testing

```bash
pip install -e src/[dev]
pytest tests/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Documentation

- [Installation Guide](docs/installation.md)
- [User Guide](docs/user_guide.md)
- [Examples](examples/)