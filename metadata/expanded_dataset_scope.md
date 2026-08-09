# Expanded Dataset Scope: PAMAP2, WESAD, MHEALTH and TILES-2018

## Purpose

This document defines the expanded dataset strategy of the bachelor thesis.

The goal is to strengthen the dysbalance framework without turning the thesis into an uncontrolled collection of unrelated dataset analyses.

The expanded scope uses four datasets with different roles:

1. PAMAP2 as the primary functional-motor dataset.
2. WESAD as the primary autonomic-physiological stress dataset.
3. MHEALTH as a compact external movement and ECG validation dataset.
4. TILES-2018 as the longitudinal real-world framework dataset.

The central idea is not that every dataset must implement every module equally. Instead, each dataset contributes a specific methodological role to the framework.

## Relation to the Research Question

The central research question is:

Inwiefern lassen sich personalisierte physiologische Abweichungsmuster mithilfe eines modellbasierten multimodalen Dysbalance-Frameworks über verschiedene Biosignal-Datensätze hinweg erkennen, erklären und longitudinal verfolgen?

The four-dataset scope maps to the research question as follows:

- erkennen: PAMAP2, WESAD, MHEALTH, anomaly detection
- erklären: PAMAP2 functional scores, WESAD autonomic scores, MHEALTH validation features
- über verschiedene Biosignal-Datensätze hinweg: PAMAP2, WESAD, MHEALTH
- longitudinal verfolgen: TILES-2018 and later optional Polar pilot sessions

## Dataset Roles

| Dataset | Role | Domain | Main Contribution |
|---|---|---|---|
| PAMAP2 | Primary controlled movement dataset | Functional-motor | Movement dysbalance and activity baseline |
| WESAD | Primary controlled autonomic dataset | Autonomic stress/regulation | Stress-related autonomic dysbalance |
| MHEALTH | Compact external validation dataset | Movement plus ECG | Transfer of movement dysbalance logic and ECG bridge |
| TILES-2018 | Longitudinal real-world dataset | Workplace physiology and behavior | Longitudinal Dysbalance Memory |

## PAMAP2 Role

PAMAP2 remains the primary functional-motor dataset.

It is already integrated and evaluated.

Completed contributions:

- dataset inspection
- cleaning
- segment-safe tensorization
- MiniRocket activity classification baseline
- functional movement feature extraction
- functional dysbalance scoring
- threshold analysis
- Isolation Forest anomaly detection
- score-anomaly overlap analysis

Scientific role:

PAMAP2 shows that functional-motor deviations can be represented using interpretable movement features, personalized normalization and model-based anomaly comparison.

## WESAD Role

WESAD remains the primary autonomic-physiological dataset.

It is already integrated and evaluated.

Completed contributions:

- local import from previous study project
- segment-safe chest tensorization
- MiniRocket condition baselines
- standardized MiniRocket baseline
- autonomic feature extraction
- directed autonomic activation score
- undirected autonomic deviation strength
- threshold analysis
- Isolation Forest anomaly detection
- score-anomaly overlap and correlation analysis

Scientific role:

WESAD shows that stress-related autonomic activation and general autonomic abnormality are related but not identical. This is a central interpretive result of the framework.

## MHEALTH Role

MHEALTH should be integrated as a compact external validation dataset.

It should not become a full third main dataset with the same depth as PAMAP2 and WESAD.

Its role is to test whether the functional-motor framework logic transfers to a second activity dataset that also contains ECG.

Expected contribution:

- external validation of movement-related preprocessing
- second activity-recognition baseline
- movement dysbalance feature transfer
- optional ECG-derived activity response features
- bridge between PAMAP2 movement data and WESAD autonomic data
- preparation for later Polar chest strap pilot data

Scientific question for MHEALTH:

Can the functional-motor dysbalance logic developed on PAMAP2 be transferred to a second movement dataset that includes ECG information?

Recommended MHEALTH scope:

- parse and inspect dataset
- create segment-safe windows
- train a compact MiniRocket or MultiRocket activity baseline
- extract movement features analogous to PAMAP2 where possible
- optionally extract ECG-derived HR or rhythm proxy features
- compute a compact MHEALTH functional deviation score
- compare activity-level patterns with PAMAP2
- document transferability and limitations

Explicit non-goals for MHEALTH:

- no complete new framework branch
- no extensive clinical ECG interpretation
- no attempt to overclaim generality from one additional dataset
- no complex longitudinal modeling, because MHEALTH is not the main longitudinal dataset

Expected thesis placement:

MHEALTH should appear after PAMAP2 and WESAD as an external validation subsection.

Possible title:

External Movement and ECG Validation on MHEALTH

## TILES-2018 Role

TILES-2018 should become the longitudinal real-world case of the thesis.

Its role is more ambitious than MHEALTH, but it must be focused.

TILES should not be treated as another simple classification dataset. Its value lies in longitudinal, naturalistic data.

Expected contribution:

- real-world longitudinal physiology and behavior
- repeated measurements over time
- connection between physiological patterns, daily states and context
- input for Longitudinal Dysbalance Memory
- demonstration that the framework can move beyond short controlled lab windows

Scientific question for TILES:

Can repeated physiological and behavioral signals be transformed into longitudinal dysbalance events, episodes and subject-level hypotheses?

Recommended TILES scope:

- inspect available files and access conditions
- identify usable physiological streams
- identify usable daily or session-level labels or surveys
- define a subject-day or subject-session feature table
- compute personalized deviations over time
- generate dysbalance events
- aggregate events into episodes
- feed events into Longitudinal Dysbalance Memory
- analyze a limited number of representative subjects or cohorts
- visualize trajectories over days or weeks

Possible TILES features:

- resting or daily heart-rate statistics
- wearable-derived activity or movement summaries
- sleep or recovery indicators if available
- stress or affect survey indicators if available
- day-level deviation from individual baseline
- repeated anomaly or dysbalance episodes

Explicit non-goals for TILES:

- no full parsing of every sensor stream if it is not necessary
- no attempt to model all surveys
- no full workplace-behavior prediction task
- no clinical diagnosis
- no privacy-invasive interpretation
- no uncontrolled expansion into audio or interpersonal behavior unless strictly necessary

Expected thesis placement:

TILES should appear as the longitudinal framework case after the controlled dataset results and after the definition of Longitudinal Dysbalance Memory.

Possible title:

Longitudinal Dysbalance Memory on TILES-2018

## Polar Pilot Role

The planned Polar chest strap pilot should remain optional and exploratory.

It should not replace public dataset evaluation.

Expected role:

- demonstrate how new personal sensor sessions could enter the framework
- test the practical schema on self-recorded or pilot sensor data
- compare intended movement or recovery patterns with framework outputs
- show feasibility, not validation

Scientific framing:

The Polar pilot is an exploratory proof-of-use, not a clinical validation and not a central evidence source.

Expected thesis placement:

Appendix, discussion, or small outlook subsection.

Possible title:

Exploratory Pilot Demonstration with New Sensor Data

## Revised Thesis Phase Structure

The thesis should be structured into phases.

### Phase 1: Data Foundation and Reproducible Pipelines

Datasets:

- PAMAP2
- WESAD
- later MHEALTH
- later TILES inspection

Goal:

Create reproducible parsers, cleaning logic, windowing and metadata documentation.

### Phase 2: Supervised Baselines

Datasets:

- PAMAP2
- WESAD
- later MHEALTH

Goal:

Verify that the sensor windows contain learnable structure.

Models:

- MiniRocket
- optional MultiRocket robustness check

### Phase 3: Explainable Dysbalance Scoring

Datasets:

- PAMAP2
- WESAD
- later MHEALTH compact validation

Goal:

Create interpretable, personalized dysbalance scores.

Domains:

- functional-motor dysbalance
- autonomic dysbalance
- optional movement-plus-ECG dysbalance

### Phase 4: Model-Based Anomaly Detection

Datasets:

- PAMAP2
- WESAD
- later MHEALTH if useful

Goal:

Compare score-based dysbalance with data-driven anomaly scores.

Primary model:

- Isolation Forest

Optional models:

- One-Class SVM
- Local Outlier Factor

### Phase 5: Longitudinal Dysbalance Memory

Datasets:

- initially PAMAP2 and WESAD outputs for schema testing
- then TILES-2018 as the main longitudinal case

Goal:

Transform window-level scores and anomalies into events, episodes and longitudinal hypotheses.

Core concepts:

- dysbalance event
- episode
- repeated pattern
- hypothesis
- hypothesis status
- subject-level memory

### Phase 6: Exploratory New-Sensor Pilot

Datasets:

- optional Polar chest strap pilot
- optional second simple sensor

Goal:

Demonstrate that the framework schema can accept new sensor sessions.

## Why This Scope Is Scientifically Strong

The expanded scope is strong because each dataset has a distinct role.

PAMAP2 answers:

Can movement dysbalance be modeled in controlled activity data?

WESAD answers:

Can autonomic stress-related dysbalance be modeled in controlled physiological data?

MHEALTH answers:

Does the movement-dysbalance logic transfer to another activity dataset with ECG?

TILES answers:

Can dysbalance be followed over time in a naturalistic longitudinal setting?

Polar pilot answers:

Can the framework be used as a practical platform for new sensor sessions?

Together, this forms a coherent progression from controlled datasets to longitudinal real-world analysis and exploratory sensor deployment.

## Why This Scope Is Risky

The scope is ambitious.

Risks:

- too many datasets may dilute the main argument
- TILES may require significant access, parsing and missing-data handling
- MHEALTH may duplicate PAMAP2 rather than add conceptual depth
- MultiRocket and additional baselines could distract from the framework contribution
- thesis writing time may be reduced if integration work becomes too large

## Risk Mitigation

The expanded scope should be managed with clear priority levels.

Priority 1:

- Longitudinal Dysbalance Memory
- TILES feasibility and focused integration

Priority 2:

- MHEALTH compact validation
- MultiRocket robustness check

Priority 3:

- optional Polar pilot
- additional anomaly models beyond Isolation Forest

If time becomes limited, the fallback scope remains scientifically valid:

- PAMAP2
- WESAD
- Isolation Forest anomaly detection
- Longitudinal Memory schema
- TILES as conceptual target or partial case

## Current Decision

MHEALTH and TILES-2018 will be included in the thesis roadmap.

MHEALTH will be used as a compact external validation dataset.

TILES-2018 will be used as the main longitudinal framework case, provided that access and data structure are feasible within the remaining project time.

The next immediate implementation step should still be Longitudinal Dysbalance Memory, because both TILES and the future Polar pilot depend on that schema.
