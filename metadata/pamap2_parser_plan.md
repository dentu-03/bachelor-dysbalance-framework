# PAMAP2 Parser Plan

## Dataset role

PAMAP2 is the first newly integrated dataset in the Bachelor Dysbalance Framework.

Scientific role:

- functional physiological deviation modeling
- activity-related time-series analysis
- validation of parser -> windowing -> tensorization -> AI pipeline
- first new dataset beyond the previous KI-Studienprojekt

## Raw data location

Protocol data:

data/raw/pamap2/PAMAP2_Dataset/Protocol/

Optional data:

data/raw/pamap2/PAMAP2_Dataset/Optional/

For the first parser version, only the official Protocol data will be used.

## Initial inspection

The Protocol folder contains 9 subject files:

- subject101.dat
- subject102.dat
- subject103.dat
- subject104.dat
- subject105.dat
- subject106.dat
- subject107.dat
- subject108.dat
- subject109.dat

Each file contains 54 columns.

Observed row counts:

- subject101: approx. 376,417 rows
- subject102: approx. 447,000 rows
- subject103: approx. 252,833 rows
- subject104: approx. 329,576 rows
- subject105: approx. 374,783 rows
- subject106: approx. 361,817 rows
- subject107: approx. 313,599 rows
- subject108: approx. 408,031 rows
- subject109: approx. 8,477 rows

Note:

subject109 is much shorter than the other subjects and may need special handling during evaluation.

## Expected column structure

PAMAP2 contains:

- timestamp
- activity label
- heart rate
- IMU hand
- IMU chest
- IMU ankle

Each IMU contains multiple channels such as:

- temperature
- accelerometer
- gyroscope
- magnetometer
- orientation

The exact column names will be implemented explicitly in the parser.

## First parser goal

The first parser version should not yet perform full tensorization.

Goal of version 1:

raw .dat files
-> pandas DataFrame
-> named columns
-> subject_id column
-> remove optional data
-> save cleaned interim CSV or Parquet

## Scientific processing decisions

Initial decisions:

- Use Protocol data only.
- Keep subject IDs.
- Preserve activity labels.
- Preserve timestamp.
- Keep heart rate, accelerometer and gyroscope channels initially.
- Handle missing values explicitly, especially heart-rate NaNs.
- Do not drop subjects automatically before documenting missingness and row counts.

## Next step

Implement src/parsers/parse_pamap2.py with explicit column names and a first cleaned interim export.
