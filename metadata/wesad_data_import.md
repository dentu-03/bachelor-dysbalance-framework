# WESAD Data Import

This document records how the WESAD dataset was integrated into the Bachelor thesis project.

## Role in the thesis

WESAD is used as the autonomic-physiological reference dataset of the Bachelor thesis.

In the previous study project, WESAD was already used for:

- biosignal parsing
- aeon-compatible tensorization
- ROCKET-based stress classification
- explainable autonomic dysbalance proof-of-concept analysis

In the Bachelor thesis, WESAD is not treated as an unrelated new dataset. Instead, it serves as a continuation and generalization anchor for the methods developed during the study project.

## Source location

The dataset was copied from the previous study project directory:

`/home/dennis_preusch/Dokumente/UNI/5.Semester/KI-Studienprojekt/project-data/raw/wesad`

## Target location

The dataset was copied into the current Bachelor thesis project:

`data/raw/wesad`

## Import validation

Validation after copying:

- total size: approximately `17G`
- number of subject PKL files: `15`

Detected subject files:

- `S2/S2.pkl`
- `S3/S3.pkl`
- `S4/S4.pkl`
- `S5/S5.pkl`
- `S6/S6.pkl`
- `S7/S7.pkl`
- `S8/S8.pkl`
- `S9/S9.pkl`
- `S10/S10.pkl`
- `S11/S11.pkl`
- `S13/S13.pkl`
- `S14/S14.pkl`
- `S15/S15.pkl`
- `S16/S16.pkl`
- `S17/S17.pkl`

Additional files per subject:

- questionnaire CSV files
- subject readme files
- Respiban text files

The global WESAD readme PDF is also present:

- `data/raw/wesad/wesad_readme.pdf`

## Versioning note

The raw WESAD data is not tracked by Git.

The repository tracks only code, configuration, documentation and lightweight result summaries. Raw data, interim data, processed tensors, model artefacts and generated report files remain local.
