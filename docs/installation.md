# Installation Guide

## Requirements

- Python 3.8 or higher
- Git

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/giovaniemotiv/eeg-visualizer.git
   cd eeg-visualizer
   ```

2. **Install the package**
   ```bash
   pip install -e src/
   ```

3. **Run the application**
   ```bash
   streamlit run src/eegviz/app/main.py
   ```

4. **Access the application**
   Open your web browser and go to `http://localhost:8501`

## Dependencies

The package will automatically install:
- MNE-Python for EEG processing
- Streamlit for the web interface
- Matplotlib for plotting
- NumPy and Pandas for data handling

## Troubleshooting

### Common Issues

**Import errors**: Make sure you installed with the `-e` flag for editable installation.

**Port already in use**: Streamlit will automatically find an available port, or specify one with `--server.port 8502`.

**Missing dependencies**: Reinstall with `pip install -e src/ --force-reinstall`.

## Development Installation

For development work:

```bash
pip install -e src/[dev]
```

This includes additional tools for testing and code quality.