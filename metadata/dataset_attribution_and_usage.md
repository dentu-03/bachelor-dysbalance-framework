# Dataset Attribution and Usage Notes

## Purpose

This document records which external datasets are used in this project, how they should be attributed, and how they are used within the dysbalance framework.

The raw datasets are not versioned in Git. Only source code, configuration files, metadata notes, and documentation are tracked.

## General Usage Rules

For all external datasets:

- Original authors and institutions must be cited in the thesis.
- The original dataset source must be referenced.
- Recommended scientific citations should be used where available.
- Raw data remains local under data/raw/.
- Derived tensors, processed data, models, and generated reports remain local if they are large or automatically reproducible.
- The repository only tracks code, configuration, metadata, and documentation.

## PAMAP2 Physical Activity Monitoring Dataset

### Official Name

PAMAP2 Physical Activity Monitoring Dataset

### Source

UCI Machine Learning Repository

Dataset URL:

https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring

### Authors

The dataset is associated with:

- Attila Reiss
- Didier Stricker

### Recommended Citation

Reiss, A., and Stricker, D. (2012).
Introducing a New Benchmarked Dataset for Activity Monitoring.
16th IEEE International Symposium on Wearable Computers, ISWC 2012, 108-109.
DOI: 10.1109/ISWC.2012.13

Additional related publication:

Reiss, A., and Stricker, D. (2012).
Creating and Benchmarking a New Dataset for Physical Activity Monitoring.
PETRA 2012.

### Project Role

PAMAP2 is used as the main functional-motor dataset.

Within the dysbalance framework it supports:

- activity recognition baseline
- functional movement feature extraction
- subject- and activity-normalized deviation scores
- threshold-based analysis of functional dysbalance

### Local Usage

Local raw/interim/processed paths:

- data/raw/pamap2/
- data/interim/pamap2/
- data/processed/pamap2/

Local result documents:

- docs/results/pamap2_pipeline_summary.md
- docs/results/pamap2_functional_dysbalance_summary.md

Implemented processing:

- protocol file cleaning
- exclusion of transient activity label 0
- exclusion of subject 109 due to insufficient protocol data
- segment-safe tensorization
- 500 sample windows
- 50 percent overlap
- tensor shape: n_windows x 19 x 500
- MiniRocket activity baseline
- functional dysbalance score

### Usage Note

The dataset is used only for scientific work within this bachelor thesis. Raw data is not redistributed through the repository.

## WESAD: Wearable Stress and Affect Detection Dataset

### Official Name

WESAD: A Multimodal Dataset for Wearable Stress and Affect Detection

### Source

Official WESAD dataset page by the University of Siegen / Ubiquitous Computing Group:

https://kristofvl.github.io/usi/data_wesad.html

Publication DOI:

https://doi.org/10.1145/3242969.3242985

### Authors

The dataset is associated with:

- Philip Schmidt
- Attila Reiss
- Robert Duerichen
- Claus Marberger
- Kristof Van Laerhoven

### Recommended Citation

Schmidt, P., Reiss, A., Duerichen, R., Marberger, C., and Van Laerhoven, K. (2018).
Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection.
Proceedings of the 20th ACM International Conference on Multimodal Interaction, ICMI 2018, 400-408.
DOI: 10.1145/3242969.3242985

### Project Role

WESAD is used as the autonomic-physiological reference dataset.

Within the dysbalance framework it supports:

- stress and affect state analysis
- subject-wise condition classification baseline
- autonomic feature extraction
- subject-normalized autonomic activation score
- autonomic deviation strength
- threshold-based analysis of physiological dysbalance

### Local Usage

Local raw/interim/processed paths:

- data/raw/wesad/
- data/interim/wesad/
- data/processed/wesad/

Local result documents:

- metadata/wesad_data_import.md
- docs/results/wesad_autonomic_dysbalance_summary.md

Implemented processing:

- local import from the previous study project
- segment-safe chest tensorization
- 7000 sample windows
- 10 second windows
- 50 percent overlap
- tensor shape: n_windows x 8 x 7000
- MiniRocket baseline
- standardized MiniRocket baseline
- autonomic feature extraction
- autonomic dysbalance score
- condition-wise visualizations

### Usage Note

The dataset is used only for scientific work within this bachelor thesis. Raw data is not redistributed through the repository.

## Planned or Configured Datasets

The configuration file configs/datasets.yaml also contains additional possible dataset candidates, including:

- MHEALTH
- TILES-2018

At the current project stage, these datasets are not central result datasets. If they are used later, source, authorship, citation, and usage notes must be added here.

## Current Citation Status

At minimum, the thesis must cite:

1. PAMAP2 Physical Activity Monitoring Dataset
2. WESAD: Wearable Stress and Affect Detection Dataset

Both datasets must be described in the methodology chapter, and their original authors must be acknowledged.

## Open To-Dos Before Final Submission

- Verify final dataset URLs.
- Verify final recommended citations.
- Add BibTeX entries for PAMAP2 and WESAD.
- Check exact license and usage notes from the original sources.
- Transfer dataset descriptions into the thesis methodology chapter.
- Mention that raw data is excluded from Git for reproducibility and licensing reasons.
