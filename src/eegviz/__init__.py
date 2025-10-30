"""
EEG Visualizer - A comprehensive EEG analysis and visualization tool.

Built with MNE-Python and Streamlit for interactive EEG data analysis.
"""

__version__ = "0.1.0"
__author__ = "EEG Visualizer Team"
__email__ = "contact@eeg-visualizer.com"

# Configure matplotlib for non-interactive use
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Streamlit

# Import key modules for easy access
from . import config
from .core.session import SessionManager
from .core.validation import DataValidator

__all__ = [
    "config", 
    "SessionManager", 
    "DataValidator",
    "__version__",
]
