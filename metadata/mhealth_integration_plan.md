# MHEALTH Integration Plan

## Purpose

MHEALTH is added as a compact external validation dataset for the dysbalance framework.

Its role is not to replace PAMAP2 or WESAD.

Its role is to test whether the existing framework ideas can be transferred to another multimodal biosignal dataset with movement and ECG-related information.

## Scientific Role

MHEALTH connects three parts of the framework:

- PAMAP2: movement and activity recognition
- WESAD: physiological signal interpretation
- future pilot data: wearable sensor transfer

This makes MHEALTH a bridge dataset.

It supports the question whether functional-motor and physiological dysbalance concepts can be reused outside the original development datasets.

## Dataset Role in the Thesis

MHEALTH should be treated as an external validation and transfer dataset.

The intended thesis role is:

- compact multimodal validation
- transfer check for preprocessing and tensorization
- activity baseline comparison
- movement-score transfer
- optional ECG-derived feature exploration
- preparation for later pilot sensor data

MHEALTH should not become the main thesis dataset.

The main framework evidence remains:

- PAMAP2 for functional-motor dysbalance
- WESAD for autonomic dysbalance
- Longitudinal Memory as aggregation layer
- TILES-2018 as later longitudinal target

## Planned Pipeline

### Phase 1: Data Import

Tasks:

- obtain the dataset
- store raw files under `data/raw/mhealth/`
- document source and attribution
- inspect file format and signal columns
- identify subjects, labels and sensors

Expected output:

- `metadata/mhealth_data_import.md`
- raw file inventory

### Phase 2: Parser

Tasks:

- parse subject log files
- preserve subject IDs
- preserve activity labels
- preserve signal columns
- handle missing or invalid values explicitly
- create an interim representation

Expected output:

- `src/parsers/parse_mhealth.py`
- `data/interim/mhealth/`
- parser summary table

### Phase 3: Tensorization

Tasks:

- create segment-safe windows
- avoid windows crossing activity boundaries
- choose an initial window length comparable to existing pipelines
- preserve metadata per window
- create subject-wise arrays

Expected output:

- `src/tensorization/tensorize_mhealth.py`
- `data/interim/mhealth/by_subject/`
- tensorization summary

### Phase 4: Supervised Baseline

Tasks:

- train a MiniRocket baseline
- use subject-wise train/test split
- report accuracy and class-wise performance
- compare with PAMAP2 baseline cautiously

Expected output:

- `src/models/train_mhealth_activity_baseline.py`
- `docs/results/mhealth_pipeline_summary.md`

### Phase 5: Dysbalance Features

Tasks:

- derive movement-related RMS features
- define body-location ratios if sensor placement allows it
- evaluate whether ECG-derived simple features are feasible
- keep ECG interpretation conservative

Expected output:

- `src/dysbalance/mhealth_movement_features.py`
- optional ECG feature module
- processed feature CSV

### Phase 6: Dysbalance Scores

Tasks:

- apply subject-specific or subject-context-specific normalization
- compute interpretable deviation strength
- run threshold sweep
- compare with PAMAP2-style functional dysbalance

Expected output:

- `src/dysbalance/mhealth_functional_scores.py`
- `docs/results/mhealth_dysbalance_summary.md`

### Phase 7: Anomaly and Memory Compatibility

Tasks:

- connect MHEALTH scores to existing anomaly pipeline if feasible
- test whether MHEALTH events can use the same Memory schema
- mark evidence scope as controlled window sequence

Expected output:

- MHEALTH anomaly score table
- optional MHEALTH memory events
- framework compatibility statement

## Initial Scientific Questions

MHEALTH should answer:

1. Can the existing preprocessing and tensorization strategy be transferred to another multimodal biosignal dataset?
2. Does a MiniRocket activity baseline produce usable subject-wise performance?
3. Can functional-motor dysbalance scores be constructed with comparable logic to PAMAP2?
4. Do movement-derived deviations align with model-based anomaly scores?
5. Can the existing Memory schema represent MHEALTH events without structural changes?
6. Does ECG information provide a useful bridge toward autonomic or wearable pilot data?

## Non-Goals

MHEALTH is not used for:

- clinical ECG diagnosis
- full cardiological interpretation
- replacing WESAD autonomic analysis
- true longitudinal evidence
- final validation of the Polar pilot
- exhaustive activity-recognition benchmarking

## Risk Management

Potential risks:

- signal column layout differs from expectations
- activity labels may require careful mapping
- ECG quality may not support robust feature extraction
- subject-wise generalization may be weaker than PAMAP2
- sensor placement may limit direct ratio transfer

Mitigation:

- inspect files before implementing assumptions
- document all column mappings
- start with movement and activity baseline
- treat ECG features as optional
- keep interpretation conservative

## Success Criteria

The MHEALTH integration is successful if it produces:

- reproducible raw-data import notes
- parser summary
- segment-safe window tensors
- subject-wise baseline result
- at least one interpretable movement-derived dysbalance score
- clear comparison to PAMAP2
- compatibility with the existing Memory schema

## Current Decision

MHEALTH will be integrated after the first Longitudinal Dysbalance Memory implementation.

The first step is not model training.

The first step is data access, attribution and raw structure inspection.
