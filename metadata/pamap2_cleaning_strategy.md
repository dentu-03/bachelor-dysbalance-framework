# PAMAP2 Cleaning Strategy

This document defines the initial cleaning strategy for the PAMAP2 Protocol dataset.

## Scope

Only the Protocol subset is used for the first Bachelor thesis pipeline iteration.

The Optional subset is not used initially, because the Protocol subset already provides a controlled and sufficiently rich basis for activity, movement and physiological analysis.

## Label handling

Activity label `0` represents transient or undefined activity periods.

Initial strategy:

- exclude label `0` for supervised activity classification
- keep label `0` only for exploratory inspection if needed
- document all exclusions explicitly in generated reports

Subject `109` is very short and contains only labels `0` and `24`.

Initial strategy:

- include subject `109` in raw summaries
- exclude subject `109` from first robust classification/tensorization experiments
- revisit later if rope-jumping-specific analysis is needed

## Channel handling

The official PAMAP2 files contain 54 columns:

- timestamp
- activity ID
- heart rate
- 3 IMU positions: hand, chest, ankle
- each IMU contains temperature, acceleration, gyroscope, magnetometer and orientation values

Initial signal selection:

- use timestamp
- use activity ID
- use subject ID
- use heart rate
- use accelerometer ±16g channels
- use gyroscope channels
- initially exclude orientation channels because they are marked as invalid in the dataset documentation
- initially exclude accelerometer ±6g channels to avoid redundant acceleration representations

## Missing values

Heart rate has many missing values because it was sampled at a lower frequency than the IMU channels.

Initial strategy:

- do not drop full rows only because heart rate is missing
- interpolate or forward-fill heart rate only in a later dedicated preprocessing step
- keep missingness visible in summaries

## First cleaned representation

The first cleaned PAMAP2 representation should therefore contain:

- subject_id
- timestamp
- activity_id
- heart_rate
- hand_acc16_x/y/z
- hand_gyro_x/y/z
- chest_acc16_x/y/z
- chest_gyro_x/y/z
- ankle_acc16_x/y/z
- ankle_gyro_x/y/z

This results in:

- 3 metadata columns: subject_id, timestamp, activity_id
- 1 physiological channel: heart_rate
- 18 IMU channels: 3 positions × 6 movement channels

Total: 22 columns.

## Methodological note

This cleaning strategy preserves multimodal information while avoiding invalid or redundant channels in the first pipeline iteration. It also keeps the framework focused on explainable signal processing before more complex feature extraction or tensorization is introduced.
