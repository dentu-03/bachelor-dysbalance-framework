# TILES-2018 Longitudinal Score Summary

Dieses Dokument beschreibt den Status der vorbereiteten TILES-2018-Score-Schicht.

## Ergebnis

- Status: missing_input
- Scores created: False
- Input: `/home/dennis_preusch/Dokumente/UNI/6.Semester/Thesis/bachelor-dysbalance-framework/data/interim/tiles2018/subject_day_features.csv`
- Output: `/home/dennis_preusch/Dokumente/UNI/6.Semester/Thesis/bachelor-dysbalance-framework/data/processed/tiles2018/dysbalance/tiles2018_longitudinal_scores.csv`

## Interpretation

Aktuell liegt lokal noch keine kanonische TILES-subject-day-Tabelle vor.

Die Score-Schicht ist daher vorbereitet, aber noch nicht datengetrieben ausgeführt.

Sobald `data/interim/tiles2018/subject_day_features.csv` existiert, erzeugt das Skript subject-normalisierte longitudinale Dysbalance Scores.

## Methodische Einordnung

Die TILES-Score-Schicht ist bewusst subject-normalisiert. Dadurch wird nicht ein globaler Normwert modelliert, sondern die Abweichung vom individuellen Referenzzustand.

Für die Thesis ist diese Schicht der Übergang von kontrollierten Window-Sequenzen zu echter longitudinaler Realwelt-Evidenz.
