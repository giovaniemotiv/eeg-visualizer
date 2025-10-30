"""Epoch creation and management utilities."""

from __future__ import annotations
import mne
import numpy as np
from mne import events_from_annotations
from typing import List, Optional, Tuple, Dict, Any


class EpochManager:
    """Handles creation and management of MNE Epochs from annotations."""
    
    def __init__(self):
        self.last_epochs = None
        self.last_event_id = None
    
    def create_epochs_from_labels(
        self,
        raw: mne.io.BaseRaw,
        labels_to_use: List[str],
        tmin: float,
        tmax: float,
        picks,
        baseline: Optional[Tuple[float, float]] = None,
        decim: int = 1,
        reject_by_annotation: bool = True,
        detrend: Optional[int] = 1,
    ) -> Tuple[Optional[mne.Epochs], Optional[Dict[str, int]], Optional[str]]:
        """Create MNE Epochs from annotation labels.
        
        Args:
            raw: MNE Raw object with annotations
            labels_to_use: List of annotation labels to include
            tmin: Start time relative to event (seconds)
            tmax: End time relative to event (seconds)  
            picks: Channel picks
            baseline: Baseline correction period (start, end) in seconds
            decim: Decimation factor
            reject_by_annotation: Whether to reject epochs overlapping with bad annotations
            detrend: Detrending polynomial order (None for no detrending)
            
        Returns:
            Tuple of (epochs, event_id_dict, error_message)
        """
        try:
            # Check if annotations exist
            if not len(raw.annotations):
                return None, None, "No annotations present in the data"
            
            # Build events from annotations
            events, mapping = events_from_annotations(raw, verbose=False)
            
            if len(events) == 0:
                return None, None, "No events found in annotations"
            
            # Filter mapping to only include requested labels
            event_id = {label: code for label, code in mapping.items() if label in labels_to_use}
            
            if not event_id:
                available_labels = list(mapping.keys())
                return None, None, f"No matching labels found. Available: {available_labels}"
            
            # Create epochs
            epochs = mne.Epochs(
                raw,
                events,
                event_id=event_id,
                tmin=tmin,
                tmax=tmax,
                baseline=baseline,
                picks=picks,
                preload=True,
                reject_by_annotation=reject_by_annotation,
                detrend=detrend,
                decim=decim,
                verbose=False
            )
            
            # Check if any epochs were created
            if len(epochs) == 0:
                return None, None, f"No valid epochs found for labels: {labels_to_use}"
            
            # Store for later use
            self.last_epochs = epochs
            self.last_event_id = event_id
            
            return epochs, event_id, None
            
        except Exception as e:
            return None, None, f"Failed to create epochs: {str(e)}"
    
    def get_epoch_counts(self, epochs: mne.Epochs, event_id: Dict[str, int]) -> Dict[str, int]:
        """Get count of epochs for each condition.
        
        Args:
            epochs: MNE Epochs object
            event_id: Event ID mapping
            
        Returns:
            Dictionary mapping condition names to epoch counts
        """
        counts = {}
        for label, event_code in event_id.items():
            # Count epochs for this event type
            condition_epochs = epochs[label] if label in epochs.event_id else None
            counts[label] = len(condition_epochs) if condition_epochs is not None else 0
        
        return counts
    
    def validate_epoch_parameters(
        self,
        raw: mne.io.BaseRaw,
        tmin: float,
        tmax: float,
        baseline: Optional[Tuple[float, float]] = None
    ) -> List[str]:
        """Validate epoch creation parameters.
        
        Args:
            raw: MNE Raw object
            tmin: Start time relative to event
            tmax: End time relative to event
            baseline: Baseline period
            
        Returns:
            List of validation warnings
        """
        warnings = []
        
        # Check epoch duration
        epoch_duration = tmax - tmin
        if epoch_duration <= 0:
            warnings.append("Epoch duration must be positive (tmax > tmin)")
        elif epoch_duration < 0.1:
            warnings.append("Very short epochs may not be useful for analysis")
        elif epoch_duration > 30.0:
            warnings.append("Very long epochs may include multiple events")
        
        # Check tmin/tmax relative to sampling rate
        sfreq = raw.info["sfreq"]
        min_samples = max(1, int(epoch_duration * sfreq))
        if min_samples < 10:
            warnings.append("Epochs will have very few samples")
        
        # Validate baseline
        if baseline is not None:
            baseline_start, baseline_end = baseline
            if baseline_start >= baseline_end:
                warnings.append("Baseline start must be < baseline end")
            elif baseline_start < tmin or baseline_end > tmax:
                warnings.append("Baseline period must be within epoch time range")
            elif baseline_end > 0:
                warnings.append("Baseline typically ends at or before event (t=0)")
        
        return warnings
    
    def create_evoked_from_epochs(
        self,
        epochs: mne.Epochs,
        condition: str
    ) -> Optional[mne.Evoked]:
        """Create evoked response from epochs for a specific condition.
        
        Args:
            epochs: MNE Epochs object
            condition: Condition name
            
        Returns:
            MNE Evoked object or None if failed
        """
        try:
            if condition not in epochs.event_id:
                return None
            
            condition_epochs = epochs[condition]
            if len(condition_epochs) == 0:
                return None
            
            evoked = condition_epochs.average()
            return evoked
            
        except Exception:
            return None
    
    def get_epochs_info(self, epochs: mne.Epochs) -> Dict[str, Any]:
        """Get information about created epochs.
        
        Args:
            epochs: MNE Epochs object
            
        Returns:
            Dictionary with epoch information
        """
        if epochs is None:
            return {"status": "no_epochs"}
        
        # Get basic info
        info = {
            "status": "epochs_created",
            "n_epochs": len(epochs),
            "n_channels": len(epochs.ch_names),
            "tmin": epochs.tmin,
            "tmax": epochs.tmax,
            "sfreq": epochs.info["sfreq"],
            "baseline": epochs.baseline,
            "conditions": list(epochs.event_id.keys()),
        }
        
        # Get epoch counts per condition
        condition_counts = {}
        for condition in epochs.event_id.keys():
            try:
                condition_epochs = epochs[condition]
                condition_counts[condition] = len(condition_epochs)
            except:
                condition_counts[condition] = 0
        
        info["condition_counts"] = condition_counts
        
        # Check for dropped epochs
        if hasattr(epochs, "drop_log"):
            n_dropped = sum(1 for log in epochs.drop_log if len(log) > 0)
            info["n_dropped"] = n_dropped
            info["drop_rate"] = n_dropped / (len(epochs) + n_dropped) if (len(epochs) + n_dropped) > 0 else 0
        
        return info
    
    def suggest_epoch_parameters(self, raw: mne.io.BaseRaw) -> Dict[str, Any]:
        """Suggest reasonable epoch parameters based on data properties.
        
        Args:
            raw: MNE Raw object
            
        Returns:
            Dictionary with suggested parameters
        """
        sfreq = raw.info["sfreq"]
        
        # Suggest based on sampling rate and typical ERP analysis
        suggestions = {
            "tmin": -0.2,  # 200ms pre-stimulus
            "tmax": 0.8,   # 800ms post-stimulus  
            "baseline": (-0.2, 0.0),  # Pre-stimulus baseline
            "decim": max(1, int(sfreq / 250)),  # Target ~250Hz for ERPs
        }
        
        # Adjust for very high or low sampling rates
        if sfreq < 125:
            suggestions["decim"] = 1
            suggestions["tmin"] = -0.1
            suggestions["tmax"] = 0.5
        elif sfreq > 1000:
            suggestions["decim"] = int(sfreq / 250)
        
        return suggestions