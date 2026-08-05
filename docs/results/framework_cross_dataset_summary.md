# Cross-Dataset Framework Summary: PAMAP2 and WESAD

## Purpose

This document summarizes the current cross-dataset state of the dysbalance framework.

The goal is to show that the framework is not limited to a single dataset or physiological domain. Instead, it is applied to two different multimodal biosignal datasets:

- PAMAP2 for functional-motor dysbalance
- WESAD for autonomic-physiological dysbalance

Together, both datasets provide early evidence that personalized physiological deviations can be modeled across different signal domains.

## Central Research Connection

The central research question of this thesis is:

Inwiefern lassen sich personalisierte physiologische Abweichungsmuster mithilfe eines KI-basierten multimodalen Dysbalance-Frameworks über verschiedene Biosignal-Datensätze hinweg erkennen, erklären und longitudinal verfolgen?

The current PAMAP2 and WESAD results address the first two parts of this question:

- erkennen: deviations are detectable through classification baselines and thresholded scores
- erklären: deviations are represented through interpretable physiological score components

The longitudinal part remains a later framework extension.

## Dataset Roles

| Dataset | Domain | Primary Role | Framework Perspective |
|---|---|---|---|
| PAMAP2 | Movement and activity | Functional-motor modeling | Motor dysbalance |
| WESAD | Stress and autonomic regulation | Autonomic physiological modeling | Autonomic dysbalance |

The datasets are complementary:

- PAMAP2 focuses on body movement, activity, and sensorimotor patterns.
- WESAD focuses on stress, autonomic activation, and physiological regulation.

## PAMAP2 Summary

PAMAP2 was used as the main functional-motor dataset.

Implemented pipeline:

- raw protocol inspection
- cleaning and column selection
- exclusion of transient activity label 0
- exclusion of subject 109 because of insufficient valid protocol data
- segment-safe tensorization
- channel median imputation
- MiniRocket activity classification baseline
- movement feature extraction
- functional dysbalance scoring
- subject- and activity-specific normalization
- threshold-based deviation analysis
- result visualizations

Main tensor properties:

| Property | Value |
|---|---:|
| Subjects | 8 |
| Windows | 7587 |
| Channels | 19 |
| Timepoints per window | 500 |
| Window duration | 5 seconds |
| Overlap | 50 percent |

Classification baseline:

| Model | Split | Accuracy |
|---|---|---:|
| MiniRocket | Subject-wise | 0.9541 |

Functional dysbalance score:

The PAMAP2 score is based on movement-related features such as total acceleration intensity and log-ratio relationships between body-worn sensors.

Central idea:

- movement intensity and body-region relationships are extracted per window
- values are normalized per subject and activity
- deviation strength is computed from absolute normalized components
- threshold sweeps identify unusually strong functional deviations

Observed pattern:

- functional deviation strength is present across all subjects
- the percentage of windows above a deviation threshold remains in a plausible low single-digit range
- top deviation windows are traceable back to interpretable movement features

Framework interpretation:

PAMAP2 demonstrates that the framework can model functional-motor deviations using interpretable movement features and personalized normalization.

## WESAD Summary

WESAD was used as the autonomic-physiological reference dataset.

Implemented pipeline:

- local data import from the previous study project
- segment-safe chest tensorization
- MiniRocket condition classification baseline
- standardized MiniRocket condition classification baseline
- autonomic feature extraction
- subject-normalized autonomic scoring
- threshold-based autonomic activation analysis
- result visualizations

Main tensor properties:

| Property | Value |
|---|---:|
| Subjects | 15 |
| Windows | 8892 |
| Channels | 8 |
| Timepoints per window | 7000 |
| Window duration | 10 seconds |
| Overlap | 50 percent |

Classification baselines:

| Model | Preprocessing | Split | Accuracy |
|---|---|---|---:|
| MiniRocket | none | Subject-wise | 0.6433 |
| MiniRocket | Train-set channel standardization | Subject-wise | 0.7167 |

The improvement through channel-wise standardization shows that WESAD is strongly affected by channel scales and inter-subject signal differences.

Autonomic dysbalance score:

The WESAD score combines subject-normalized components:

- heart rate
- electrodermal activity
- respiratory variability
- inverse RMSSD

Central idea:

- high heart rate indicates physiological activation
- high EDA indicates sympathetic activation
- respiratory variability contributes a stress-related regulation component
- low RMSSD is represented as inverse RMSSD and indicates reduced parasympathetic regulation
- components are normalized per subject
- a directed autonomic activation score and an undirected deviation strength are computed

Main condition-level result:

| Condition | Mean z_autonomic_activation | z > 2.0 |
|---|---:|---:|
| baseline | -0.4932 | 0.63 percent |
| stress | 1.3926 | 18.07 percent |
| amusement | -0.2430 | 0.82 percent |
| meditation | -0.3269 | 0.13 percent |

Framework interpretation:

WESAD demonstrates that stress-related autonomic activation can be represented through explainable, subject-normalized score components without relying only on direct classification.

## Cross-Dataset Comparison

| Aspect | PAMAP2 | WESAD |
|---|---|---|
| Domain | Functional-motor | Autonomic-physiological |
| Main signals | IMU and heart rate | ACC, ECG, EMG, EDA, Temp, Resp |
| Main task | Activity recognition and movement deviation | Stress and affect-related autonomic deviation |
| Baseline model | MiniRocket | MiniRocket |
| Best current baseline | 0.9541 accuracy | 0.7167 accuracy |
| Dysbalance type | Functional deviation strength | Autonomic activation and deviation strength |
| Normalization | Subject and activity | Subject |
| Interpretability | Movement intensity and body-region ratios | HR, EDA, Resp, inverse RMSSD |
| Main contribution | Motor-domain dysbalance modeling | Autonomic-domain dysbalance modeling |

## Methodological Pattern Across Datasets

Both dataset pipelines follow the same general framework logic:

1. Convert multimodal biosignals into segment-safe windows.
2. Build a classification baseline to verify signal validity.
3. Extract interpretable physiological features.
4. Normalize features in a personalized way.
5. Combine features into a dysbalance-related score.
6. Apply threshold sweeps to quantify abnormal or elevated states.
7. Visualize and document the result.

This shared pattern is central for the thesis, because it shows that the framework is not a one-off dataset solution.

## Difference Between Classification and Dysbalance Modeling

The classification baselines answer the question:

Can the dataset contain enough information to predict known labels?

The dysbalance scores answer a different question:

Can physiological deviations from a personalized reference state be represented in an interpretable way?

This distinction is important because the thesis is not primarily about maximizing classification accuracy. Classification is used as a validation step. The core contribution is the explainable modeling of personalized deviations.

## Current Evidence for Generalizability

The current state supports limited but meaningful cross-dataset generalizability.

Evidence:

- The same framework structure was applied to two different datasets.
- Both datasets use multimodal physiological signals.
- Both pipelines use segment-safe tensorization.
- Both datasets include classification baselines.
- Both datasets include interpretable score components.
- Both score systems use personalized normalization.
- Both datasets produce threshold-based deviation summaries.
- Both results are reproducible through versioned source code.

Limitations:

- Only two datasets have been fully evaluated so far.
- PAMAP2 and WESAD measure different physiological phenomena.
- The score definitions are domain-specific.
- No longitudinal dataset has been fully integrated yet.
- Clinical interpretation is explicitly out of scope.

## Current Scientific Interpretation

The results suggest that the dysbalance framework can be applied across physiological domains if the score components are adapted to the domain.

This leads to an important thesis argument:

The framework is generalizable at the methodological level, not because the same exact score is used everywhere, but because the same modeling principles are reused:

- multimodal signal windows
- interpretable features
- personalized normalization
- deviation scoring
- threshold analysis
- visual explanation

## Relation to the Next Work Package

The next missing framework block is anomaly detection.

PAMAP2 and WESAD currently provide:

- supervised baselines
- interpretable deviation scores
- threshold-based analyses

The next step should add:

- unsupervised or weakly supervised anomaly detection
- comparison between score-based deviations and model-based anomalies
- reusable anomaly interfaces under src/anomaly/
- reports under reports/anomaly/

After that, the longitudinal memory component can be built on top of the anomaly and dysbalance outputs.

## Current Project State

Completed core result blocks:

- PAMAP2 activity baseline
- PAMAP2 functional dysbalance score
- WESAD condition baselines
- WESAD autonomic dysbalance score
- dataset attribution notes
- cross-dataset framework summary

Open core result blocks:

- anomaly detection
- longitudinal dysbalance memory
- final evaluation tables
- thesis chapter drafts
- final literature and BibTeX cleanup
