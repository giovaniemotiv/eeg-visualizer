# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended for large datasets
- **Storage**: 1 GB free space for installation, additional space for data
- **Internet**: Required for initial package installation

### Recommended Requirements
- **Python**: 3.10 or 3.11 (latest stable)
- **RAM**: 16 GB for large EEG files (>100 MB)
- **CPU**: Multi-core processor for faster filtering and analysis
- **Graphics**: Dedicated GPU helpful for complex visualizations

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/eeg-visualizer.git
cd eeg-visualizer

# Install in editable mode with all dependencies
pip install -e src/

# Verify installation
python -c "import eegviz; print('Installation successful!')"
```

### Method 2: Using conda

```bash
# Create a new conda environment
conda create -n eeg-visualizer python=3.10
conda activate eeg-visualizer

# Clone and install
git clone https://github.com/your-username/eeg-visualizer.git
cd eeg-visualizer
pip install -e src/

# Or create from environment file (if provided)
conda env create -f environment.yml
conda activate eeg-visualizer
```

### Method 3: Development Installation

```bash
# For contributors and developers
git clone https://github.com/your-username/eeg-visualizer.git
cd eeg-visualizer

# Install with development dependencies
pip install -e src/[dev]

# Install pre-commit hooks
pre-commit install

# Run tests to verify installation
python -m pytest tests/
```

## Package Dependencies

### Core Dependencies
```
mne >= 1.10.0           # EEG analysis library
streamlit >= 1.33.0     # Web application framework
matplotlib >= 3.7.0     # Plotting library
numpy >= 1.21.0         # Numerical computing
pandas >= 1.3.0         # Data manipulation
scipy >= 1.7.0          # Scientific computing
```

### Visualization Dependencies
```
plotly >= 5.0.0         # Interactive plots
seaborn >= 0.11.0       # Statistical visualization
imageio >= 2.9.0        # Image/GIF handling
pillow >= 8.0.0         # Image processing
```

### Optional Dependencies
```
jupyter >= 1.0.0        # Notebook support
ipywidgets >= 7.6.0     # Interactive widgets
nibabel >= 3.2.0        # Neuroimaging data
pyvista >= 0.37.0       # 3D brain visualization
```

## Platform-Specific Instructions

### Windows

1. **Install Python**: Download from [python.org](https://python.org) or use Microsoft Store
2. **Install Git**: Download from [git-scm.com](https://git-scm.com)
3. **Open PowerShell or Command Prompt**
4. **Follow pip installation method above**

#### Windows-Specific Notes:
- Use PowerShell for better command support
- May need to install Visual C++ Build Tools for some packages
- Consider using Windows Subsystem for Linux (WSL) for better compatibility

### macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python and Git**:
   ```bash
   brew install python git
   ```

3. **Follow pip installation method**

#### macOS-Specific Notes:
- Xcode Command Line Tools may be required: `xcode-select --install`
- Consider using pyenv for Python version management

### Linux (Ubuntu/Debian)

1. **Update package manager**:
   ```bash
   sudo apt update
   ```

2. **Install dependencies**:
   ```bash
   sudo apt install python3 python3-pip python3-venv git
   ```

3. **Follow pip installation method**

#### Linux-Specific Notes:
- Install tkinter if needed: `sudo apt install python3-tk`
- For CentOS/RHEL: use `yum` or `dnf` instead of `apt`

## Docker Installation (Alternative)

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  eeg-visualizer:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
```

```bash
# Build and run
docker-compose up --build
```

### Manual Docker Build

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY src/ /app/src/
COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN pip install -e src/

EXPOSE 8501
CMD ["streamlit", "run", "src/eegviz/app/main.py"]
```

```bash
# Build and run
docker build -t eeg-visualizer .
docker run -p 8501:8501 eeg-visualizer
```

## Verification and Testing

### Basic Verification

```python
# Test core imports
import eegviz
import mne
import streamlit

# Check versions
print(f"EEGViz: {eegviz.__version__}")
print(f"MNE: {mne.__version__}")
print(f"Streamlit: {streamlit.__version__}")

# Test basic functionality
from eegviz.core.session import SessionManager
session = SessionManager()
print("Installation verified successfully!")
```

### Run Test Suite

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=eegviz --cov-report=html

# Test specific functionality
python -m pytest tests/test_bands.py -v
```

### Test with Sample Data

```bash
# Start the application
py -m streamlit run src/eegviz/app/main.py

# Download sample data
curl -O https://github.com/your-username/eeg-visualizer/raw/main/examples/sample_eeg.edf

# Upload the sample file through the web interface
```

## Troubleshooting Installation

### Common Issues

#### 1. Python Version Conflicts
**Error**: "Python version not supported"
**Solution**:
```bash
# Check Python version
python --version

# Use specific Python version
python3.10 -m pip install -e src/

# Or create virtual environment
python -m venv eeg-env
source eeg-env/bin/activate  # Linux/Mac
eeg-env\Scripts\activate     # Windows
```

#### 2. Permission Errors
**Error**: "Permission denied" during installation
**Solution**:
```bash
# Use user installation
pip install --user -e src/

# Or fix permissions
sudo chown -R $USER:$USER ~/.local/
```

#### 3. Package Conflicts
**Error**: "Conflicting dependencies"
**Solution**:
```bash
# Create clean environment
conda create -n eeg-clean python=3.10
conda activate eeg-clean
pip install -e src/

# Or use pip-tools
pip install pip-tools
pip-compile src/requirements.in
pip-sync requirements.txt
```

#### 4. MNE Installation Issues
**Error**: MNE-related import errors
**Solution**:
```bash
# Install MNE separately first
pip install mne[hdf5]

# Then install eeg-visualizer
pip install -e src/
```

#### 5. Streamlit Issues
**Error**: Streamlit command not found
**Solution**:
```bash
# Reinstall streamlit
pip uninstall streamlit
pip install streamlit

# Check PATH
echo $PATH  # Linux/Mac
echo $env:PATH  # Windows PowerShell
```

### Platform-Specific Troubleshooting

#### Windows
- **Error**: "Microsoft Visual C++ 14.0 is required"
  **Solution**: Install Visual Studio Build Tools
- **Error**: "Long path names not supported"
  **Solution**: Enable long path support in Windows settings

#### macOS
- **Error**: "Command Line Tools not found"
  **Solution**: `xcode-select --install`
- **Error**: "Architecture not supported"
  **Solution**: Use Rosetta 2 on Apple Silicon Macs

#### Linux
- **Error**: "Qt platform plugin not found"
  **Solution**: `sudo apt install python3-pyqt5`
- **Error**: "Display not available"
  **Solution**: Install X11 forwarding or use virtual display

## Performance Optimization

### Memory Management

```python
# Configure MNE for lower memory usage
import mne
mne.set_config('MNE_MEMMAP_MIN_SIZE', '1M')
mne.set_config('MNE_CACHE_DIR', '/path/to/large/drive')
```

### Streamlit Configuration

```toml
# .streamlit/config.toml
[server]
maxUploadSize = 1000
maxMessageSize = 1000

[theme]
base = "light"
primaryColor = "#FF6B6B"
```

## Next Steps

After successful installation:

1. **Read the User Guide**: `docs/user_guide.md`
2. **Try the Tutorial**: `docs/tutorial.md`
3. **Explore Examples**: `examples/` directory
4. **Join the Community**: GitHub Discussions

## Getting Help

- **Documentation**: Check this guide and others in `docs/`
- **GitHub Issues**: Report installation problems
- **Community Support**: Ask questions in GitHub Discussions
- **Email Support**: contact@eeg-visualizer.com (if available)