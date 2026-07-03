# Artifact Strategy

Dieses Dokument beschreibt, welche Artefakte im Bachelorprojekt systematisch erzeugt werden sollen.

## Ziel

Die Bachelorarbeit soll nicht nur Code und Modelle enthalten, sondern eine nachvollziehbare Sammlung wissenschaftlicher Artefakte:

- Tabellen
- CSV-Dateien
- Metriken
- Grafiken
- Confusion Matrices
- Score-Verteilungen
- Threshold-Sweeps
- Longitudinal-Trendplots
- GUI-Screenshots
- Paper- und Thesis-Figures

Dadurch entsteht eine reproduzierbare Grundlage für Bachelorarbeit, Präsentation und möglichen Paper-Entwurf.

## Grundprinzip

Jeder größere Verarbeitungsschritt soll möglichst ein Artefakt erzeugen.

Pipeline:

Rohdaten
→ Parser-Artefakte
→ Tensor-Artefakte
→ Modell-Artefakte
→ Dysbalance-Artefakte
→ Anomaly-Artefakte
→ Longitudinal-Artefakte
→ GUI-Artefakte
→ Paper-Figures

## Geplante Report-Struktur

reports/
├── datasets/
├── models/
├── dysbalance/
├── anomaly/
├── longitudinal/
├── figures/
└── paper_assets/

## Dataset-Artefakte

Für jeden Datensatz sollen erzeugt werden:

- Rohdatenübersicht
- Anzahl Subjekte
- Anzahl Zeilen/Fenster
- Kanalübersicht
- Missing-Value-Statistik
- Labelverteilung
- Sampling-/Windowing-Information
- Tensor-Shape

Beispiele:

- `reports/datasets/pamap2_summary.csv`
- `reports/datasets/pamap2_label_distribution.png`
- `reports/datasets/pamap2_missing_values.csv`

## Modell-Artefakte

Für KI-Modelle sollen erzeugt werden:

- Train/Test-Splits
- Accuracy / Balanced Accuracy
- Precision / Recall / F1
- Confusion Matrix
- Modellvergleich MiniRocket vs. MultiRocket
- gespeicherte Modellobjekte

Beispiele:

- `reports/models/pamap2_multirocket_metrics.csv`
- `reports/models/pamap2_multirocket_confusion_matrix.png`

## Dysbalance-Artefakte

Für erklärbare Dysbalance-Scores sollen erzeugt werden:

- Z-Score-Verteilungen
- Score-Verteilungen pro Zustand
- Teil-Score-Beiträge
- Gesamt-Dysbalance-Scores
- Vergleich einzelner Modalitäten vs. Fusion

Beispiele:

- `reports/dysbalance/pamap2_z_distribution.png`
- `reports/dysbalance/pamap2_score_components.csv`

## Anomaly-Artefakte

Für Anomalieerkennung sollen erzeugt werden:

- Anteil auffälliger Fenster pro Zustand
- Threshold-Sweep-Tabellen
- Threshold-Sweep-Plots
- Vergleich unterschiedlicher Anomaly-Methoden

Beispiele:

- `reports/anomaly/pamap2_threshold_sweep.csv`
- `reports/anomaly/pamap2_threshold_sweep.png`

## Longitudinal-Artefakte

Für das Longitudinal Dysbalance Memory sollen erzeugt werden:

- Verlauf einzelner Personen
- wiederkehrende Muster
- Trendplots
- gespeicherte Muster-Hypothesen
- Statusänderungen: neu, bestätigt, abgeschwächt, verworfen

Beispiele:

- `reports/longitudinal/person_001_dysbalance_timeline.png`
- `reports/longitudinal/dysbalance_memory.csv`

## GUI-Artefakte

Für den GUI-Demonstrator sollen erzeugt werden:

- Screenshots
- Beispielreports
- Beispielansichten einzelner Personen
- Visualisierung aktueller und longitudinaler Dysbalance

Beispiele:

- `reports/paper_assets/gui_dashboard_example.png`
- `reports/paper_assets/gui_longitudinal_memory.png`

## Paper- und Thesis-Figures

Besonders wichtige Grafiken sollen zusätzlich in `reports/paper_assets/` gesammelt werden.

Ziel:
Diese Abbildungen sollen direkt für Bachelorarbeit, Präsentation oder Paper-Entwurf nutzbar sein.

## Wissenschaftlicher Nutzen

Die Artefaktstrategie erhöht:

- Reproduzierbarkeit
- Nachvollziehbarkeit
- wissenschaftliche Transparenz
- Qualität der Auswertung
- visuelle Stärke der Bachelorarbeit
- Präsentationsqualität
