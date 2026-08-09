# Longitudinal Dysbalance Memory Design

## Purpose

This document defines the Longitudinal Dysbalance Memory component of the dysbalance framework.

The purpose of the memory component is to transform isolated window-level dysbalance and anomaly outputs into longitudinally interpretable structures.

The memory component is not a diagnostic system.

It creates structured hypotheses about repeated or persistent physiological deviations.

## Relation to the Research Question

The central research question asks whether personalized physiological deviation patterns can be detected, explained and longitudinally tracked across biosignal datasets.

The previous framework stages already address detection and explanation:

- supervised baselines detect learnable signal structure
- dysbalance scores represent interpretable physiological deviations
- anomaly detection identifies unusual windows in model-based feature space

The Longitudinal Dysbalance Memory addresses the remaining part:

- longitudinal tracking of repeated or persistent personalized deviation patterns

## Conceptual Hierarchy

The memory component uses five levels.

### Level 1: Window

A window is the smallest unit of analysis.

Examples:

- one PAMAP2 5-second movement window
- one WESAD 10-second chest-signal window
- one future TILES subject-day or subject-session unit
- one future Polar pilot window

A window can contain:

- dysbalance score
- anomaly score
- threshold flag
- model anomaly flag
- dataset context
- subject context
- activity or condition label
- timestamp or sample range

### Level 2: Dysbalance Event

A dysbalance event is created when a window is considered relevant for longitudinal tracking.

A window can become an event if at least one of the following is true:

- a dysbalance score exceeds a configured threshold
- a model-based anomaly flag is true
- an anomaly rank percentile is very high
- a domain-specific score indicates strong directed activation or deviation

An event is still local and short-term.

It does not imply persistence.

### Level 3: Dysbalance Episode

An episode is a group of temporally adjacent or contextually related events.

For window-based datasets, events can be grouped into an episode if they occur close together within the same subject, dataset, session and domain.

For day-level datasets such as TILES, repeated abnormal subject-days can form an episode.

An episode summarizes:

- start and end position
- duration or number of windows
- dominant domain
- dominant context
- maximum score
- mean score
- number of model anomalies
- number of threshold anomalies
- main contributing components

### Level 4: Dysbalance Hypothesis

A hypothesis is created when one or more episodes suggest a repeated or meaningful pattern.

A hypothesis is subject-specific.

Examples:

- subject S6 repeatedly shows unusual autonomic deviation during baseline windows
- a subject repeatedly shows high functional deviation during stairs or posture transitions
- a future TILES participant shows repeated recovery-related deviations across multiple workdays
- a future Polar pilot session shows repeated activation after specific movement patterns

A hypothesis is not a diagnosis.

It is a structured, explainable observation that can be tracked over time.

### Level 5: Hypothesis Status

Each hypothesis receives a status.

Allowed statuses:

- new
- observed
- confirmed
- stable
- weakened
- discarded

Status meaning:

new:
A first event or episode has been detected.

observed:
The pattern appears more than once but evidence is still limited.

confirmed:
The pattern appears repeatedly or with strong score support.

stable:
The pattern remains present across later windows, sessions or days.

weakened:
The pattern becomes less frequent or less intense.

discarded:
The pattern does not repeat or appears to be a one-off artefact.

## Scientific Rationale

The memory component is needed because window-level anomaly detection alone is not sufficient.

A single anomalous window can be caused by:

- sensor noise
- transient movement
- segmentation artefact
- normal physiological variability
- true but isolated deviation

Longitudinal memory reduces overinterpretation by tracking whether deviations repeat, persist or disappear.

This supports a cautious interpretation:

- one event is a signal candidate
- one episode is a short-term pattern
- repeated episodes form a hypothesis
- hypotheses can strengthen or weaken over time

## Relation to Previous Study Project

The previous study project introduced the idea of physiologically motivated dysbalance scores.

It focused mainly on window-level or aggregate-level abnormality rates.

The bachelor thesis extends this by introducing a memory layer.

The extension is:

- previous: identify abnormal windows or rates
- current: track abnormal events as evolving hypotheses

This creates a transition from static dysbalance detection to longitudinal deviation tracking.

## Relation to Existing Results

### PAMAP2

PAMAP2 currently provides:

- functional_deviation_strength
- activity context
- subject context
- timestamp range
- Isolation Forest anomaly score
- model anomaly flag
- high overlap between functional deviation and model anomaly

Expected memory use:

- create functional-motor events from high deviation windows
- group nearby windows into movement episodes
- summarize repeated subject-activity patterns

PAMAP2 is not truly longitudinal over weeks.

Its role for memory is schema testing and episode logic.

### WESAD

WESAD currently provides:

- z_autonomic_activation
- autonomic_deviation_strength
- stress or affect condition labels
- subject context
- sample range
- Isolation Forest anomaly score
- model anomaly flag
- strong relation between autonomic deviation strength and anomaly score

Expected memory use:

- create autonomic events from high activation or high deviation windows
- distinguish directed activation from undirected deviation
- identify subject-condition episodes
- test hypothesis status transitions on controlled condition sequences

WESAD is not a long-term real-world dataset.

Its role for memory is controlled physiological hypothesis testing.

### MHEALTH

MHEALTH is planned as compact external validation.

Expected memory use:

- test whether movement and ECG-derived events can use the same event schema
- compare with PAMAP2-style functional episodes
- prepare transition to Polar pilot data

### TILES-2018

TILES is planned as the main longitudinal real-world case.

Expected memory use:

- create day-level or session-level dysbalance events
- aggregate repeated events into episodes
- track subject-level hypotheses across weeks
- connect physiological deviations with contextual or survey information where appropriate

### Polar Pilot

The optional Polar pilot should use the same memory schema.

Expected memory use:

- create pilot-session events
- test intended movement or recovery patterns
- demonstrate practical framework usage on new sensor data

The pilot is exploratory and not a validation dataset.

## Event Schema

A dysbalance event should contain at least:

- event_id
- dataset
- domain
- subject_id
- session_id
- source_level
- window_index
- start_position
- end_position
- context_label
- context_name
- primary_score_name
- primary_score_value
- anomaly_score
- anomaly_score_z
- anomaly_rank_percent
- is_threshold_event
- is_model_anomaly
- event_strength
- event_type
- component_summary
- created_from

Suggested event types:

- functional_motor_deviation
- autonomic_activation
- autonomic_deviation
- model_anomaly
- combined_score_model_event
- longitudinal_day_deviation
- pilot_sensor_event

## Episode Schema

A dysbalance episode should contain at least:

- episode_id
- dataset
- domain
- subject_id
- session_id
- event_type
- context_name
- n_events
- start_position
- end_position
- mean_event_strength
- max_event_strength
- mean_anomaly_score
- n_threshold_events
- n_model_anomalies
- dominant_primary_score
- dominant_context
- episode_strength
- episode_status_seed

## Hypothesis Schema

A dysbalance hypothesis should contain at least:

- hypothesis_id
- subject_id
- domain
- event_type
- context_name
- n_episodes
- first_seen
- last_seen
- mean_episode_strength
- max_episode_strength
- recurrence_count
- current_status
- evidence_summary
- interpretation_note
- limitations_note

## Initial Event Creation Rules

The first implementation should use simple and transparent rules.

### PAMAP2 event rules

Create a functional event if:

- functional_deviation_strength is greater than or equal to 2.0
- or is_model_anomaly is true
- or anomaly_rank_percent is greater than or equal to 95

Primary score:

- functional_deviation_strength

Event type:

- functional_motor_deviation

Domain:

- functional_motor

### WESAD event rules

Create an autonomic activation event if:

- z_autonomic_activation is greater than or equal to 2.0

Create an autonomic deviation event if:

- autonomic_deviation_strength is greater than or equal to 1.5
- or is_model_anomaly is true
- or anomaly_rank_percent is greater than or equal to 95

Primary scores:

- z_autonomic_activation
- autonomic_deviation_strength

Event types:

- autonomic_activation
- autonomic_deviation

Domain:

- autonomic

## Initial Episode Grouping Rules

Events should be grouped into episodes by:

- dataset
- subject_id
- session_id
- domain
- event_type
- context_name

Within each group, events are sorted by position.

For window-based data, consecutive or near-consecutive event windows should be grouped into the same episode.

Initial maximum gap:

- PAMAP2: 2 windows
- WESAD: 2 windows

This is intentionally simple and transparent.

More advanced temporal logic can be added later for TILES.

## Initial Hypothesis Rules

Hypotheses are generated from episodes.

Initial status rules:

new:
- exactly one episode
- low or moderate episode strength

observed:
- two episodes
- or one strong episode

confirmed:
- at least three episodes
- or at least two strong episodes

stable:
- confirmed pattern that persists across multiple sessions or days

weakened:
- previously confirmed pattern with reduced recent evidence

discarded:
- one weak episode with no recurrence in later data

For PAMAP2 and WESAD, stable and weakened are limited because the datasets are not true long-term longitudinal datasets.

For TILES and Polar pilot sessions, stable and weakened become more meaningful.

## Evaluation Questions

The memory component should answer:

1. Which dysbalance events are created from the existing scores and anomalies?
2. Which events group into episodes?
3. Which subjects show repeated patterns?
4. Which domains produce stronger or more frequent hypotheses?
5. Do hypotheses differ between functional-motor and autonomic data?
6. Can the same schema support public datasets and future pilot sensor sessions?
7. Which limitations arise when applying longitudinal logic to non-longitudinal datasets?

## Expected Outputs

The first implementation should create:

- reports/longitudinal/dysbalance_events.csv
- reports/longitudinal/dysbalance_episodes.csv
- reports/longitudinal/dysbalance_hypotheses.csv
- reports/longitudinal/dysbalance_memory_summary.json

Optional figures later:

- event counts by dataset and domain
- episode strength by subject
- hypothesis status distribution
- subject-level event timeline examples

## Interpretation Rules

The memory output must be interpreted cautiously.

Allowed interpretation:

- candidate repeated deviation pattern
- model-supported dysbalance hypothesis
- subject-specific physiological or movement-related pattern
- framework event requiring further inspection

Not allowed interpretation:

- diagnosis
- disease claim
- medical risk classification
- clinical abnormality
- treatment recommendation

## Why This Is Innovative

The memory component is innovative in the context of this thesis because it connects multiple previously separate layers:

- explainable dysbalance scoring
- model-based anomaly detection
- subject-level pattern tracking
- future longitudinal data integration
- pilot sensor extensibility

The central contribution is the transformation from window-level signal analysis to longitudinally trackable dysbalance hypotheses.

## First Implementation Scope

The first implementation should use the already generated PAMAP2 and WESAD Isolation Forest outputs.

It should:

1. load anomaly score reports
2. create event rows using transparent rules
3. group events into episodes
4. aggregate episodes into hypotheses
5. export reproducible CSV files
6. create a summary JSON
7. remain compatible with MHEALTH, TILES and Polar pilot data later

The first implementation should not yet depend on TILES access.

TILES should be added after the memory schema is stable.
