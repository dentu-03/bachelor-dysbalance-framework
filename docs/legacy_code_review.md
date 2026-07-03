# Legacy Code Review – KI-Studienprojekt

Dieses Dokument bewertet, welche Teile des alten Studienprojekts in die Bachelorarbeit übernommen werden sollen.

## Grundsatz

Es wird nicht blind kopiert. Alte Skripte dienen als Referenz und werden in saubere Framework-Module überführt.

## Erste Sichtung

### `src/analysis/phase2/windowing.py`

Status: Platzhalter

Bewertung:
Nicht direkt übernehmbar. Für die Bachelorarbeit muss eine allgemeine Windowing-Logik neu erstellt werden.

Geplante neue Position:
`src/preprocessing/windowing.py`

---

### `src/analysis/phase2/rms.py`

Status: einfache RMS-Hilfsfunktion

Bewertung:
Inhaltlich brauchbar. Kann als Grundlage für allgemeine Feature-Funktionen genutzt werden.

Geplante neue Position:
`src/preprocessing/features.py`

---

### `src/analysis/phase3/phase3_multimodal_score.py`

Status: Proof-of-Concept für Score-Fusion

Bewertung:
Wissenschaftlich wichtige Idee, aber technisch zu hardcoded. Die Logik soll verallgemeinert werden.

Geplante neue Position:
`src/dysbalance/fusion.py`

---

## Noch zu prüfen

Folgende Dateien müssen noch gesichtet werden, bevor Funktionen übernommen werden:

- `src/analysis/phase2/emg_dysbalance_poc.py`
- `src/analysis/phase2/stress_poc_wesad.py`
- `src/analysis/build_dataset_inventory.py`
- `src/analysis/sync_inventory_to_sqlite.py`
- Modelltrainingsskripte für MiniRocket/ROCKET

Besonders wichtig:

- Z-Normierung
- Log-Ratio-Berechnung
- Threshold-Sweep
- Report-Erstellung
- SQLite-/Inventory-Logik

## Review: Phase-2-Dysbalance-POCs

### `src/analysis/phase2/emg_dysbalance_poc.py`

Status: methodisch sehr relevant, aber POC-artig.

Wichtige übernehmbare Konzepte:

- RMS-Berechnung pro Fenster
- physiologisch motivierte Ratio
- Log-Transformation von Verhältnissen
- subjektbezogene Z-Normierung
- getrennte Normalisierung nach Kontext/Bewegung
- Threshold-Sweep über mehrere Grenzwerte
- Dysbalance-Rate pro Subjekt
- CSV-Export für spätere Reports

Bewertung:
Die Datei enthält die wichtigste Logik für erklärbare muskuläre Dysbalance aus dem Studienprojekt. Für die Bachelorarbeit soll diese Logik jedoch verallgemeinert werden, sodass sie nicht nur für EMG, sondern auch für andere Modalitäten und Scores nutzbar ist.

Geplante neue Module:

- `src/dysbalance/normalization.py`
- `src/dysbalance/ratios.py`
- `src/dysbalance/thresholds.py`
- `src/dysbalance/scores.py`

---

### `src/analysis/phase2/stress_poc_wesad.py`

Status: methodisch sehr relevant, aber stark WESAD-spezifisch.

Wichtige übernehmbare Konzepte:

- einfache Feature-Extraktion aus Biosignalen
- HR / RMSSD als autonome Merkmale
- EDA tonic / phasic rate als Stressmerkmale
- physiologisch motivierter Stress-Index
- Log-Transformation
- subjektbezogene Z-Normierung
- Threshold-Sweep
- Vergleich der Auffälligkeitsraten pro Label
- Visualisierung von Z-Verteilungen

Bewertung:
Die Datei zeigt, wie aus Rohsignalen erklärbare physiologische Scores entstehen können. Für die Bachelorarbeit soll diese Logik in allgemeine Feature- und Score-Module überführt werden.

Geplante neue Module:

- `src/preprocessing/features.py`
- `src/dysbalance/scores.py`
- `src/dysbalance/thresholds.py`
- `src/anomaly/zscore_detector.py`

## Entscheidung

Die Bachelorarbeit übernimmt die zentralen wissenschaftlichen Konzepte aus den Phase-2-POCs:

- Feature-Berechnung
- Log-Ratios
- personalisierte Z-Normierung
- Threshold-Sweeps
- erklärbare Dysbalance-Raten

Die alten Skripte werden nicht direkt kopiert, sondern in allgemeine, wiederverwendbare Framework-Module überführt.
