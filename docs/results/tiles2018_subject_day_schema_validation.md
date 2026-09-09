# TILES-2018 Subject-Day Schema Validation

Dieses Dokument prüft, ob lokal bereits eine kanonische TILES-subject-day-Tabelle vorliegt.

## Ergebnis

- Input: `/home/dennis_preusch/Dokumente/UNI/6.Semester/Thesis/bachelor-dysbalance-framework/data/interim/tiles2018/subject_day_features.csv`
- Exists: False
- Schema valid: False
- Reason: input file missing
- Rows: 0
- Columns: 0
- Subjects: 0
- Min days per subject: None
- Max days per subject: None
- Median days per subject: None

## Missing required columns

- `dataset`
- `subject_id`
- `day_index`
- `timestamp_start`
- `timestamp_end`
- `source_level`
- `missingness_rate`

## Available recommended signal columns

- none

## Sensitive column hints

- none

## Interpretation

Aktuell liegt noch keine nutzbare kanonische subject-day-Tabelle vor. Die TILES-Schicht bleibt daher vorbereitet, aber noch nicht datengetrieben integriert.
