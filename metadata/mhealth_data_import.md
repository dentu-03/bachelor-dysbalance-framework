# MHEALTH Data Import

## Purpose

This document records the local import, file structure and first technical inspection of the MHEALTH dataset.

MHEALTH is used as a compact external validation dataset for the dysbalance framework.

Its role is to test transferability of the existing movement, physiological and memory-related pipeline concepts.

## Source

Dataset:

- MHEALTH Dataset
- UCI Machine Learning Repository
- Dataset ID: 319
- DOI: 10.24432/C5TW22

Local download date:

- 2026-08-15

Local raw path:

- `data/raw/mhealth/`

Downloaded archive:

- `data/raw/mhealth/mhealth_dataset.zip`

Archive size:

- 75,567,983 bytes
- approximately 73 MB on disk

SHA256:

- `16ad0ce709f3f00df18f348610d15bce0884b79e2143f57f446493673f02b8e0`

## Dataset Authors and Citation Note

The README identifies the dataset authors as:

- Oresti Banos
- Rafael Garcia
- Alejandro Saez

The README asks users to cite:

Banos, O., Garcia, R., Holgado-Terriza, J.A., Damas, M., Pomares, H., Rojas, I., Saez, A., Villalonga, C.:
mHealthDroid: a novel framework for agile development of mobile health applications.
Proceedings of the 6th International Work-conference on Ambient Assisted Living and Active Ageing, Belfast, United Kingdom, December 2-5, 2014.

This citation should be added to the final thesis bibliography if MHEALTH results are used.

## Extracted File Structure

The archive contains one dataset directory:

- `MHEALTHDATASET/`

Extracted files:

- `MHEALTHDATASET/README.txt`
- `MHEALTHDATASET/mHealth_subject1.log`
- `MHEALTHDATASET/mHealth_subject2.log`
- `MHEALTHDATASET/mHealth_subject3.log`
- `MHEALTHDATASET/mHealth_subject4.log`
- `MHEALTHDATASET/mHealth_subject5.log`
- `MHEALTHDATASET/mHealth_subject6.log`
- `MHEALTHDATASET/mHealth_subject7.log`
- `MHEALTHDATASET/mHealth_subject8.log`
- `MHEALTHDATASET/mHealth_subject9.log`
- `MHEALTHDATASET/mHealth_subject10.log`

## Experimental Setup from README

According to the README, the dataset contains recordings from ten volunteers performing twelve physical activities.

Sensor locations:

- chest
- right wrist / right lower arm
- left ankle

Sensor type:

- Shimmer2 wearable sensors

Sampling rate:

- 50 Hz

Measured modalities:

- acceleration
- gyroscope
- magnetometer
- chest ECG lead 1
- chest ECG lead 2

The chest sensor provides the ECG channels.

The README states that ECG was not used for the original recognition model but was collected for future work purposes.

## Activity Labels

The README lists twelve physical activities:

| Label | Activity |
|---:|---|
| 1 | Standing still |
| 2 | Sitting and relaxing |
| 3 | Lying down |
| 4 | Walking |
| 5 | Climbing stairs |
| 6 | Waist bends forward |
| 7 | Frontal elevation of arms |
| 8 | Knees bending |
| 9 | Cycling |
| 10 | Jogging |
| 11 | Running |
| 12 | Jump front and back |

Additional label:

| Label | Meaning |
|---:|---|
| 0 | Null class |

For the first supervised and dysbalance pipelines, label 0 should be excluded because it represents non-activity or transition periods.

## Column Structure

Each subject log contains 24 columns.

README column interpretation:

| Column | Meaning |
|---:|---|
| 1 | chest acceleration X |
| 2 | chest acceleration Y |
| 3 | chest acceleration Z |
| 4 | ECG lead 1 |
| 5 | ECG lead 2 |
| 6 | left ankle acceleration X |
| 7 | left ankle acceleration Y |
| 8 | left ankle acceleration Z |
| 9 | left ankle gyroscope X |
| 10 | left ankle gyroscope Y |
| 11 | left ankle gyroscope Z |
| 12 | left ankle magnetometer X |
| 13 | left ankle magnetometer Y |
| 14 | left ankle magnetometer Z |
| 15 | right lower arm acceleration X |
| 16 | right lower arm acceleration Y |
| 17 | right lower arm acceleration Z |
| 18 | right lower arm gyroscope X |
| 19 | right lower arm gyroscope Y |
| 20 | right lower arm gyroscope Z |
| 21 | right lower arm magnetometer X |
| 22 | right lower arm magnetometer Y |
| 23 | right lower arm magnetometer Z |
| 24 | label |

Note:

The README appears to list column 13 twice in the ankle magnetometer section. For implementation, the expected 24-column structure is interpreted as columns 12, 13 and 14 for ankle magnetometer X, Y and Z.

Units:

- acceleration: m/s^2
- gyroscope: deg/s
- magnetic field: local units
- ECG: mV

## First Technical Inspection

Inspection command:

- read all subject log files with whitespace separation
- no header
- checked number of rows
- checked number of columns
- checked labels
- checked missing values

Summary:

| File | Rows | Columns | Labels | Missing values |
|---|---:|---:|---|---:|
| mHealth_subject1.log | 161280 | 24 | 0-12 | 0 |
| mHealth_subject2.log | 130561 | 24 | 0-12 | 0 |
| mHealth_subject3.log | 122112 | 24 | 0-12 | 0 |
| mHealth_subject4.log | 116736 | 24 | 0-12 | 0 |
| mHealth_subject5.log | 119808 | 24 | 0-12 | 0 |
| mHealth_subject6.log | 98304 | 24 | 0-12 | 0 |
| mHealth_subject7.log | 104448 | 24 | 0-12 | 0 |
| mHealth_subject8.log | 129024 | 24 | 0-12 | 0 |
| mHealth_subject9.log | 135168 | 24 | 0-12 | 0 |
| mHealth_subject10.log | 98304 | 24 | 0-12 | 0 |

Total raw rows across all subject files:

- 1,215,745 rows

## Initial Quality Assessment

The dataset is technically well suited for integration.

Positive findings:

- all ten expected subject files are present
- all files contain 24 columns
- all subjects contain labels 0 to 12
- no missing values were found
- README provides sensor placement and activity mapping
- sampling rate is explicitly stated as 50 Hz

Open points:

- label 0 handling must be defined
- README column typo should be documented in parser comments
- ECG-derived features should be treated conservatively
- subject-wise generalization must be evaluated
- segment-safe windowing is required to avoid crossing activity boundaries

## Initial Processing Decision

The first parser should:

- read all ten subject logs
- assign subject IDs 1 to 10
- use explicit column names
- preserve label 0 during raw parsing
- create summaries with and without label 0
- write interim per-subject files
- avoid any filtering that is not documented

The first tensorization should:

- exclude label 0
- use segment-safe activity windows
- preserve subject and activity metadata
- initially use movement and ECG channels together only if technically stable
- keep ECG interpretation conservative

## Scientific Interpretation

MHEALTH is a strong transfer dataset because it combines multi-location body movement signals with chest ECG.

It can therefore connect the movement-centered PAMAP2 branch with the physiological WESAD branch.

However, MHEALTH should not be overinterpreted as a clinical ECG dataset.

Its main role is external framework validation, not medical diagnosis.

## Next Step

Implement a parser:

- `src/parsers/parse_mhealth.py`

Expected parser outputs:

- `data/interim/mhealth/subject_01.csv`
- per-subject summary
- label distribution summary
- column validation summary
