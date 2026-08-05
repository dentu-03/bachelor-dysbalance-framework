# Anomaly Detection Plan

## Purpose

This document defines the anomaly detection work package of the bachelor thesis.

The goal is not to add an arbitrary machine learning module, but to extend the existing dysbalance framework with a scientifically meaningful anomaly detection layer.

The anomaly detection layer should answer the following question:

Can personalized physiological deviations that are already visible through dysbalance scores also be detected by unsupervised or weakly supervised anomaly detection methods?

This connects directly to the central thesis question:

Inwiefern lassen sich personalisierte physiologische Abweichungsmuster mithilfe eines KI-basierten multimodalen Dysbalance-Frameworks über verschiedene Biosignal-Datensätze hinweg erkennen, erklären und longitudinal verfolgen?

At the current project stage, the anomaly detection block mainly addresses:

- erkennen: anomalous windows should be detectable
- erklären: anomaly decisions should be compared with interpretable dysbalance components
- vorbereiten longitudinaler Verfolgung: anomaly events can later become input for Dysbalance Memory

## Scientific Motivation

The previous study project already introduced the idea of physiologically motivated dysbalance scores.

That previous approach followed this pattern:

- define physiologically meaningful ratios or score components
- apply log transformations where ratios are used
- normalize values relative to a person-specific reference
- detect deviations using thresholds
- aggregate deviation frequencies by subject, condition, or modality

The bachelor thesis extends this idea.

The current framework already contains two working dysbalance domains:

1. PAMAP2:
   - functional-motor dysbalance
   - movement intensity and body-region relationships
   - subject- and activity-normalized deviation strength

2. WESAD:
   - autonomic-physiological dysbalance
   - HR, EDA, Respiration, inverse RMSSD
   - subject-normalized autonomic activation and deviation strength

Anomaly detection is introduced as an additional modeling perspective.

The purpose is not to replace the interpretable dysbalance scores. Instead, anomaly detection should test whether algorithmic outlier models identify similar windows as the score-based dysbalance logic.

## Relation to Literature

Anomaly detection is commonly used to identify observations that deviate strongly from expected behavior or from the majority of observations.

Relevant methodological references:

1. Chandola, Banerjee, and Kumar (2009)
   - Anomaly Detection: A Survey
   - ACM Computing Surveys
   - Provides a general conceptual foundation for anomaly detection.

2. Scholkopf et al. (2001)
   - Estimating the Support of a High-Dimensional Distribution
   - Neural Computation
   - Provides the foundation for One-Class SVM style novelty detection.

3. Liu, Ting, and Zhou (2008)
   - Isolation Forest
   - IEEE ICDM
   - Introduces isolation-based anomaly detection.

4. Breunig et al. (2000)
   - LOF: Identifying Density-Based Local Outliers
   - ACM SIGMOD
   - Introduces local density-based outlier detection.

These methods are appropriate here because the thesis does not have clinically annotated anomaly labels. Instead, the available labels represent experimental states such as activity or stress. Therefore, anomaly detection should be evaluated indirectly by comparing anomaly scores with known conditions and with the already computed dysbalance scores.

## Conceptual Distinction

The thesis must clearly distinguish three concepts:

1. Classification:
   Predict a known class label from sensor windows.

2. Dysbalance scoring:
   Compute interpretable, physiologically motivated deviation scores from personalized references.

3. Anomaly detection:
   Learn a model of normal or common patterns and assign anomaly scores to windows that deviate from that model.

Classification is supervised.

Dysbalance scoring is interpretable and rule-based or feature-compositional.

Anomaly detection is unsupervised or weakly supervised.

In this thesis, anomaly detection is not interpreted as diagnosis. It only marks windows as unusual relative to the chosen reference distribution.

## Planned Data Inputs

The anomaly module should not work on raw 3D tensors first.

Reason:

Raw tensors are high-dimensional and harder to interpret. The thesis contribution is not raw black-box anomaly detection. The goal is explainable dysbalance modeling.

Therefore, the first anomaly detection implementation should use existing feature and score tables.

### PAMAP2 Input

Primary input file:

- data/processed/pamap2/dysbalance/pamap2_functional_scores.csv

Candidate columns:

- total_acc_rms
- log_extremity_chest_acc_ratio
- log_hand_ankle_acc_ratio
- z_total_acc_rms
- z_log_extremity_chest_acc_ratio
- z_log_hand_ankle_acc_ratio
- functional_deviation_strength

Context columns:

- subject_id
- activity_id
- activity_name
- window_index
- start_timestamp
- end_timestamp

### WESAD Input

Primary input file:

- data/processed/wesad/dysbalance/wesad_autonomic_scores.csv

Candidate columns:

- hr_bpm
- rmssd_ms
- eda_mean
- resp_std
- z_hr_bpm
- z_eda_mean
- z_resp_std
- z_inverse_rmssd
- z_autonomic_activation
- autonomic_deviation_strength

Context columns:

- subject_id
- label
- label_name
- window_index
- start_sample
- end_sample

## Planned Modeling Levels

The anomaly detection block should be implemented in three levels.

### Level 1: Score-Level Anomaly Detection

Use only the final dysbalance score or a very small score vector.

PAMAP2:

- functional_deviation_strength

WESAD:

- z_autonomic_activation
- autonomic_deviation_strength

Purpose:

This level tests whether the final dysbalance scores themselves produce meaningful anomaly rankings.

Advantages:

- very interpretable
- directly comparable to threshold sweeps
- low dimensional
- robust and easy to explain

Limitation:

- may not detect component-specific anomalies if the aggregated score hides them

### Level 2: Component-Level Anomaly Detection

Use interpretable z-components instead of only final scores.

PAMAP2:

- z_total_acc_rms
- z_log_extremity_chest_acc_ratio
- z_log_hand_ankle_acc_ratio

WESAD:

- z_hr_bpm
- z_eda_mean
- z_resp_std
- z_inverse_rmssd

Purpose:

This level tests whether anomaly detection benefits from seeing the structure of the dysbalance score.

Advantages:

- still interpretable
- more expressive than a single score
- allows component contribution analysis

Limitation:

- slightly less direct than score-level analysis

### Level 3: Feature-Level Anomaly Detection

Use selected physiological features before final score aggregation.

PAMAP2:

- total_acc_rms
- log_extremity_chest_acc_ratio
- log_hand_ankle_acc_ratio

WESAD:

- hr_bpm
- rmssd_ms
- eda_mean
- resp_std

Purpose:

This level tests whether anomaly detection finds deviations in physiological feature space, even before explicit score aggregation.

Advantages:

- closer to original physiology
- useful for comparison with normalized score space

Limitation:

- feature scales must be standardized
- subject effects may dominate if normalization is not handled carefully

## Planned Algorithms

The first implementation should compare three classical anomaly detection methods.

### Isolation Forest

Reason for use:

- works well as a general unsupervised anomaly detector
- scalable for tabular feature spaces
- does not require a distance metric to be manually defined
- suitable as the first robust baseline

Expected role in thesis:

Isolation Forest serves as the primary model-based anomaly detector.

### One-Class SVM

Reason for use:

- conceptually fits novelty detection
- learns a boundary around normal data
- useful when training on reference or baseline windows

Expected role in thesis:

One-Class SVM serves as a novelty-detection comparison model.

Important limitation:

One-Class SVM can be sensitive to scaling and hyperparameters. Therefore, it should only be used on standardized low-dimensional features.

### Local Outlier Factor

Reason for use:

- detects samples with lower local density than their neighborhood
- useful for local rather than global anomalies

Expected role in thesis:

LOF serves as a local-density comparison model.

Important limitation:

For evaluating unseen windows, LOF must be configured for novelty detection if used in train-test mode.

## Planned Reference Strategies

The choice of training reference is scientifically important.

### Strategy A: Global Unsupervised Outlier Detection

Fit anomaly detectors on all windows of a dataset.

Purpose:

- identify rare windows in the full dataset
- compare anomaly rankings with dysbalance score thresholds

Use case:

- exploratory analysis
- score agreement analysis

Limitation:

- the model also sees stress or abnormal windows during fitting
- therefore it is outlier detection, not pure novelty detection

### Strategy B: Subject-Specific Reference Modeling

Fit anomaly models separately per subject.

Purpose:

- align anomaly detection with the personalized nature of dysbalance
- reduce inter-subject differences

Use case:

- strongest conceptual fit with thesis definition of dysbalance

Limitation:

- fewer windows per model
- some subjects may have too little data in certain contexts

### Strategy C: Normal-State Novelty Detection

Fit only on reference-state windows.

PAMAP2:

- possible reference: common stable activity contexts per subject
- more difficult because activity labels are not normal vs abnormal

WESAD:

- clear reference: baseline windows
- stress, amusement, meditation can be evaluated as non-reference states

Purpose:

- test whether stress or strong deviations are detected as novelty relative to baseline

Use case:

- especially suitable for WESAD

Limitation:

- for PAMAP2, normality is less directly defined

## Planned Evaluation Questions

The anomaly block should not only output anomaly labels. It should answer specific evaluation questions.

### Evaluation Question 1

Do anomaly scores correlate with existing dysbalance scores?

Metrics:

- Spearman correlation between anomaly score and dysbalance score
- mean dysbalance score among top anomaly percentiles
- overlap between threshold-based and model-based anomaly windows

Purpose:

This tests whether model-based anomalies align with physiologically interpretable dysbalance.

### Evaluation Question 2

Are known experimental states enriched among anomalies?

For WESAD:

- Are stress windows overrepresented among top anomaly scores?
- Are baseline windows underrepresented?

For PAMAP2:

- Are specific activities or subjects enriched among high anomaly scores?
- Are top windows physiologically interpretable?

Metrics:

- anomaly rate by condition or activity
- top-k anomaly composition
- condition-wise anomaly score distributions

Purpose:

This tests whether anomalies are not random but structured by physiological or behavioral context.

### Evaluation Question 3

Do anomaly models add information beyond simple thresholds?

Comparison:

- dysbalance threshold only
- anomaly detector only
- overlap between both
- disagreement cases

Purpose:

This tests whether anomaly detection contributes an additional perspective or merely reproduces the threshold logic.

### Evaluation Question 4

Can anomaly events become input for longitudinal memory?

Output needed:

- subject_id
- dataset
- modality/domain
- window index
- timestamp or sample range
- anomaly score
- dysbalance score
- main contributing components
- condition or activity label

Purpose:

This prepares the transition to Longitudinal Dysbalance Memory.

## Planned Output Tables

The module should create reproducible CSV reports.

### PAMAP2 Outputs

Suggested files:

- reports/anomaly/pamap2_anomaly_scores.csv
- reports/anomaly/pamap2_anomaly_summary_by_subject.csv
- reports/anomaly/pamap2_anomaly_summary_by_activity.csv
- reports/anomaly/pamap2_anomaly_overlap_with_thresholds.csv
- reports/anomaly/pamap2_top_anomaly_windows.csv

### WESAD Outputs

Suggested files:

- reports/anomaly/wesad_anomaly_scores.csv
- reports/anomaly/wesad_anomaly_summary_by_subject.csv
- reports/anomaly/wesad_anomaly_summary_by_condition.csv
- reports/anomaly/wesad_anomaly_overlap_with_thresholds.csv
- reports/anomaly/wesad_top_anomaly_windows.csv

## Planned Figures

Suggested figures:

- PAMAP2 anomaly score by activity
- PAMAP2 anomaly score by subject
- PAMAP2 anomaly score versus functional deviation strength
- WESAD anomaly score by condition
- WESAD anomaly score by subject
- WESAD anomaly score versus z_autonomic_activation
- WESAD anomaly score versus autonomic_deviation_strength

Figures should support interpretation rather than only show model output.

## First Implementation Scope

The first implementation should be intentionally limited.

Recommended first script:

- src/anomaly/score_level_anomaly_detection.py

Initial scope:

- load PAMAP2 functional scores
- load WESAD autonomic scores
- define compact feature sets
- run Isolation Forest on score/component-level features
- standardize features before model fitting
- export anomaly scores
- summarize anomaly rates by activity or condition
- compute overlap with existing threshold-based dysbalance flags

Why Isolation Forest first:

- robust baseline
- simple to explain
- suitable for low-dimensional tabular features
- computationally manageable
- good first comparison before adding One-Class SVM and LOF

## Acceptance Criteria

The anomaly detection block is considered useful if it produces:

1. reproducible anomaly scores for PAMAP2 and WESAD
2. summaries by subject and condition or activity
3. overlap analysis with dysbalance thresholds
4. top anomaly windows with interpretable context
5. at least one figure per dataset
6. a short result document explaining what anomaly detection adds
7. no clinical or diagnostic interpretation

## Expected Scientific Contribution

The anomaly module should support the thesis argument that the framework can model personalized deviations from multiple perspectives.

Expected contribution:

- classification validates signal content
- dysbalance scoring provides explainable physiological deviation measures
- anomaly detection tests whether unusual windows emerge from data-driven models
- longitudinal memory can later track whether anomalies are isolated, repeated, or stable over time

The important claim is not that anomaly detection is medically correct.

The important claim is:

Model-based anomaly scores can be compared with interpretable dysbalance scores to identify and characterize unusual physiological windows in a reproducible and personalized framework.

## Risks and Mitigations

### Risk: Anomaly detection becomes too black-box

Mitigation:

Use low-dimensional interpretable feature sets and always report contributing dysbalance components.

### Risk: Subject differences dominate anomaly scores

Mitigation:

Prefer subject-normalized features and subject-specific summaries.

### Risk: Results depend heavily on contamination parameter

Mitigation:

Run contamination sensitivity analysis with values such as 0.02, 0.05, and 0.10.

### Risk: PAMAP2 has no clear normal state

Mitigation:

Treat PAMAP2 first as outlier detection over functional movement deviations, not as strict novelty detection.

### Risk: WESAD stress labels make anomaly detection look like classification

Mitigation:

Use labels only for evaluation after model fitting, not as training targets.

## Planned Next Steps

1. Implement score-level Isolation Forest baseline.
2. Evaluate anomaly score agreement with existing dysbalance scores.
3. Add condition/activity summaries.
4. Add top anomaly window reports.
5. Add figures.
6. Extend to One-Class SVM and LOF only after Isolation Forest baseline is stable.
7. Write anomaly result summary.
8. Use anomaly outputs as input candidates for Longitudinal Dysbalance Memory.
