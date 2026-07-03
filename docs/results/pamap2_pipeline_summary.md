# PAMAP2 Pipeline Summary

## Dataset Role

PAMAP2 is used as the first new public multimodal biosignal dataset in this Bachelor thesis framework.

Its role is to validate whether the developed pipeline can process multimodal physiological and movement data into reproducible, model-ready time-series tensors.

The dataset contributes the following signal modalities:

- heart rate
- wrist IMU
- chest IMU
- ankle IMU

The first pipeline iteration uses the PAMAP2 Protocol subset.

## Preprocessing Strategy

The original PAMAP2 Protocol files contain 54 columns. During parsing, an additional `subject_id` column is added.

The first cleaned representation contains 22 columns:

- `subject_id`
- `timestamp`
- `activity_id`
- `heart_rate`
- 18 IMU movement channels

The selected IMU channels are:

- accelerometer ±16g channels
- gyroscope channels

The following channels are excluded in the first iteration:

- orientation channels, because they are marked as invalid in the dataset documentation
- accelerometer ±6g channels, to avoid redundant acceleration representations
- temperature and magnetometer channels, to keep the first model focused on movement and physiological load

## Label Handling

Activity label `0` represents transient or undefined activity periods.

For the first robust activity-classification pipeline, label `0` is excluded.

Subject `109` is also excluded from the first robust iteration because it is very short and contains only labels `0` and `24`.

The valid subjects for the first modeling step are:

- 101
- 102
- 103
- 104
- 105
- 106
- 107
- 108

## Segment-Safe Windowing

After removing label `0`, the time series contains temporal gaps. A naive sliding-window approach would create artificial windows across removed transient regions.

To prevent this, the tensorization uses segment-safe windowing.

A new segment starts when:

- the timestamp gap is greater than `0.05` seconds
- the activity label changes

Sliding windows are created only inside such contiguous same-activity segments.

This prevents windows from crossing physiologically unrelated time periods.

## Heart Rate Handling

Heart rate is sparse in PAMAP2 because it is sampled at a lower frequency than the IMU channels.

For the first tensorization step, heart rate is interpolated only within contiguous segments.

This avoids interpolation across removed transient activity gaps.

## Tensorization

The PAMAP2 tensors follow the aeon-compatible shape convention:

`(n_windows, n_channels, n_timepoints)`

Windowing configuration:

- sampling assumption: 100 Hz
- window size: 500 samples
- approximate window duration: 5 seconds
- step size: 250 samples
- overlap: 50 percent

Final tensor shape per subject:

`(n_windows, 19, 500)`

The 19 channels consist of:

- 1 heart-rate channel
- 18 IMU channels

## Imputation

Before saving the final model-ready tensors, NaN values are imputed channel-wise.

Imputation strategy:

- compute one median value per channel
- replace NaNs in each channel with the corresponding channel median
- use a fallback value only if an entire channel consists of NaNs

After imputation, all saved PAMAP2 tensors are NaN-free.

## By-Subject Tensorization Result

The by-subject tensorization produced the following number of windows:

| Subject | Windows |
|---:|---:|
| 101 | 979 |
| 102 | 1032 |
| 103 | 682 |
| 104 | 907 |
| 105 | 1068 |
| 106 | 979 |
| 107 | 912 |
| 108 | 1028 |

Total number of windows:

`7587`

Validation result:

- 8 X files
- 8 y files
- 8 metadata files
- 8 channel-median files
- NaNs after imputation: `0`
- windows longer than 5.2 seconds: `0`

## MiniRocket Baseline

A first activity-classification baseline was trained using MiniRocket.

Task:

- PAMAP2 activity classification

Split:

- training subjects: 101, 102, 103, 104, 105, 106
- test subjects: 107, 108

Input shapes:

- train: `(5647, 19, 500)`
- test: `(1940, 19, 500)`

Model:

- `MiniRocketClassifier`

Result:

- accuracy: `0.9541`
- macro F1: approximately `0.94`
- weighted F1: approximately `0.95`

## Generated Local Artefacts

Tensor artefacts:

- `data/processed/pamap2/by_subject/X_subject*.npy`
- `data/processed/pamap2/by_subject/y_subject*.npy`
- `data/processed/pamap2/by_subject/metadata_subject*.csv`
- `data/processed/pamap2/by_subject/channel_medians_subject*.npy`

Model artefacts:

- `models/pamap2/pamap2_minirocket_subject_split.joblib`

Report artefacts:

- `reports/models/pamap2_minirocket_baseline_summary.json`
- `reports/models/pamap2_minirocket_classification_report.json`
- `reports/models/pamap2_minirocket_classification_report.txt`
- `reports/models/pamap2_minirocket_confusion_matrix.csv`
- `reports/models/pamap2_minirocket_confusion_matrix_raw.png`
- `reports/models/pamap2_minirocket_confusion_matrix_normalized.png`

## Interpretation

The MiniRocket baseline confirms that the PAMAP2 processing pipeline produces meaningful and model-ready time-series representations.

The high subject-wise test accuracy indicates that the selected channels, segment-safe windowing, heart-rate handling, imputation and labeling strategy preserve activity-specific temporal signal patterns.

This result is important because it validates the technical foundation before moving toward more complex dysbalance-score modeling.

## Scientific Relevance

This pipeline step demonstrates that the developed framework can transform a public multimodal biosignal dataset into reproducible, explainable and machine-learning-ready tensors.

It also establishes the first successful activity-recognition baseline of the Bachelor thesis and provides a reference point for later comparisons with additional datasets and dysbalance-oriented analyses.
