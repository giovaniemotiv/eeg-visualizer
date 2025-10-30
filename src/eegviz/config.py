"""Configuration settings for EEG Visualizer."""

import matplotlib
import matplotlib.pyplot as plt

# Configure matplotlib for Streamlit
matplotlib.use('Agg')  # Non-interactive backend
plt.ioff()  # Turn off interactive mode

# MNE sphere model for topographic plots
SPHERE = (0.0, 0.0, 0.0, 0.095)

# Standard 14-channel EEG montage
EEG14 = ["AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4"]

# Standard EEG frequency bands
BANDS = {
    "Delta": (1.0, 4.0),
    "Theta": (4.0, 8.0),
    "Alpha": (8.0, 13.0),
    "Beta":  (13.0, 30.0),
    "Gamma": (30.0, 45.0),
}

# Default visualization settings
DEFAULT_COLORMAP = "RdBu_r"
DEFAULT_DPI = 150
ANIMATION_FPS = 10

# File handling settings
MAX_FILE_SIZE_MB = 500
TEMP_DIR = "temp_data"

# Analysis settings
DEFAULT_MONTAGE = "standard_1020"
DEFAULT_FILTER_L_FREQ = 1.0
DEFAULT_FILTER_H_FREQ = 45.0
DEFAULT_NOTCH_FREQ = 60.0  # US standard (50 for Europe)
