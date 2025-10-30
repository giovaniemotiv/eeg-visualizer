# Examples

This directory contains example files and workflows for using EEG Visualizer.

## Sample Data

### Marker Files

**CSV format example:**
```csv
latency,duration,type
1.5,0.5,stimulus_onset
3.2,0.2,button_press
5.8,1.0,artifact_period
```

**JSON format example:**
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

## Basic Workflow

1. **Load your EDF file** using the sidebar file uploader
2. **Add markers** (optional) by uploading CSV or JSON files
3. **Select channels** and mark any bad channels
4. **Apply filters** appropriate for your analysis
5. **Create visualizations** and export results

## Tips

- Start with a short time window (10-30 seconds) for faster processing
- Always check data quality before analysis
- Use appropriate filter settings for your research question
- Export your processed data for reproducible analysis

## Getting Help

- Check the [User Guide](../docs/user_guide.md) for detailed instructions
- Review the [Installation Guide](../docs/installation.md) if you have setup issues
- Open an issue on GitHub for bugs or feature requests