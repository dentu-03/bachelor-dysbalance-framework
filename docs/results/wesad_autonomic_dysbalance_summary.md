# WESAD Autonomic Dysbalance Summary

## Rolle im Projekt

WESAD dient in dieser Arbeit als autonom-physiologischer Referenzdatensatz. Während PAMAP2 primär funktional-motorische Aktivitäts- und Bewegungsdaten abbildet, liefert WESAD multimodale Biosignale zur Analyse von Stress, Erholung und autonomer Regulation.

Damit bildet WESAD den physiologischen Gegenpart zur PAMAP2-Auswertung:

- PAMAP2: funktional-motorische Dysbalance
- WESAD: autonom-physiologische Dysbalance

Die Auswertung verfolgt nicht nur eine Klassifikation von Zuständen, sondern eine erklärbare Modellierung personalisierter physiologischer Abweichungen.

## Datengrundlage

Verwendet wurden die segment-sicher erzeugten WESAD-Chest-Tensoren.

Tensorisierung:

- Samplingrate: 700 Hz
- Fensterlänge: 7000 Samples
- Fensterdauer: 10 Sekunden
- Überlappung: 50 %
- Kanäle: 8
  - ACC x/y/z
  - ECG
  - EMG
  - EDA
  - Temp
  - Resp

Zustände:

- baseline
- stress
- amusement
- meditation

Gesamter Datenumfang:

- Feature-Tabelle: `(8892, 20)`
- Score-Tabelle: `(8892, 28)`
- Keine fehlenden Werte nach Feature-Berechnung

Fensteranzahl pro Zustand:

| Zustand | Fenster |
|---|---:|
| baseline | 3504 |
| stress | 1976 |
| amusement | 1093 |
| meditation | 2319 |

## Klassifikationsbaselines

Vor der Dysbalance-Modellierung wurden MiniRocket-Baselines auf den WESAD-Chest-Tensoren trainiert.

Subject-wise Split:

- Training: S2, S3, S4, S5, S6, S7, S8, S9, S10, S11
- Test: S13, S14, S15, S16, S17

Baseline ohne Standardisierung:

- Accuracy: `0.6433`
- Macro F1: ca. `0.54`
- Weighted F1: ca. `0.62`

Baseline mit trainingsbasierter kanalweiser Standardisierung:

- Accuracy: `0.7167`
- Macro F1: ca. `0.66`
- Weighted F1: ca. `0.71`

Die Verbesserung durch Standardisierung zeigt, dass WESAD stark von kanalspezifischen Skalen und interindividuellen Signalunterschieden geprägt ist. Dies unterstützt die Annahme, dass physiologische Biosignale nicht nur global klassifiziert, sondern personalisiert normalisiert und interpretiert werden sollten.

## Autonomic Feature Extraction

Für jedes 10-Sekunden-Fenster wurden erklärbare physiologische Features extrahiert.

Extrahierte Merkmale:

| Signal | Merkmale |
|---|---|
| ECG | geschätzte Herzfrequenz, RMSSD, Peak-Anzahl |
| EDA | Mittelwert, Standardabweichung, Spannweite |
| Resp | Mittelwert, Standardabweichung, Spannweite |
| Temp | Mittelwert, Standardabweichung |
| EMG | RMS |
| ACC | RMS |

Die ECG-basierte HR- und RMSSD-Schätzung ist eine reproduzierbare, leichte Window-Level-Approximation und nicht als klinische ECG-Auswertung zu verstehen. Für die Zielsetzung der Arbeit ist sie als erklärbares autonomes Merkmal geeignet.

## Score-Definition

Der autonome Aktivierungsscore kombiniert vier subject-normalisierte Komponenten:

- `z_hr_bpm`
- `z_eda_mean`
- `z_resp_std`
- `z_inverse_rmssd`

Dabei gilt:

`z_inverse_rmssd = -z_rmssd_ms`

Damit steht ein niedriger RMSSD-Wert für höhere autonome Aktivierung.

Der rohe Aktivierungsscore wird berechnet als:

`autonomic_activation_raw = mean(z_hr_bpm, z_eda_mean, z_resp_std, z_inverse_rmssd)`

Anschließend wird dieser Score erneut subject-normalisiert:

`z_autonomic_activation = subject_z(autonomic_activation_raw)`

Zusätzlich wurde eine ungerichtete Abweichungsstärke berechnet:

`autonomic_deviation_strength = mean(abs(z_hr_bpm), abs(z_eda_mean), abs(z_resp_std), abs(z_inverse_rmssd))`

Damit entstehen zwei komplementäre Perspektiven:

- `z_autonomic_activation`: gerichtete autonome Aktivierung
- `autonomic_deviation_strength`: ungerichtete physiologische Abweichungsstärke

## Ergebnisse nach Zustand

### Gerichtete autonome Aktivierung

| Zustand | Mittelwert z_autonomic_activation | Standardabweichung |
|---|---:|---:|
| baseline | -0.4932 | 0.6355 |
| stress | 1.3926 | 0.6862 |
| amusement | -0.2430 | 0.7530 |
| meditation | -0.3269 | 0.6288 |

Stress zeigt klar die höchste autonome Aktivierung. Baseline, amusement und meditation liegen im Mittel deutlich niedriger.

### Positive Aktivierungsschwellen

Anteil der Fenster mit positiver autonomer Aktivierung über festen Schwellen:

| Zustand | z > 1.5 | z > 2.0 |
|---|---:|---:|
| baseline | 1.06 % | 0.63 % |
| stress | 43.67 % | 18.07 % |
| amusement | 3.48 % | 0.82 % |
| meditation | 1.29 % | 0.13 % |

Diese Werte zeigen, dass Stress nicht nur im Mittel erhöht ist, sondern auch deutlich häufiger starke autonome Aktivierung erzeugt.

### Ungerichtete Abweichungsstärke

| Zustand | mean_autonomic_deviation_strength | > 1.5 | > 2.0 |
|---|---:|---:|---:|
| baseline | 0.7231 | 2.54 % | 0.80 % |
| stress | 1.0429 | 12.04 % | 1.67 % |
| amusement | 0.6446 | 1.10 % | 0.37 % |
| meditation | 0.7033 | 2.46 % | 0.47 % |

Auch die ungerichtete Abweichungsstärke ist bei Stress am höchsten. Der Unterschied ist jedoch weniger stark als bei der gerichteten Aktivierung. Das spricht dafür, dass Stress in WESAD vor allem als gerichtete autonome Aktivierung sichtbar wird.

## Visualisierungen

Erzeugte lokale Abbildungen:

- `reports/figures/wesad_autonomic_activation_by_condition.png`
- `reports/figures/wesad_autonomic_deviation_strength_by_condition.png`
- `reports/figures/wesad_autonomic_component_means_by_condition.png`

Die Abbildungen zeigen:

- die Verteilung der autonomen Aktivierung pro Zustand
- die Verteilung der ungerichteten Abweichungsstärke pro Zustand
- die mittleren Score-Komponenten pro Zustand

## Bezug zum Studienprojekt

Im Studienprojekt wurde bereits ein WESAD-Stress-Proof-of-Concept mit einem physiologisch motivierten Stress-Score umgesetzt. Die aktuelle Bachelor-Auswertung greift diese Idee auf, erweitert sie jedoch methodisch:

- segment-sichere Tensorisierung
- systematische Feature-Tabelle
- subject-normalisierte Score-Komponenten
- getrennte gerichtete und ungerichtete Dysbalance-Perspektive
- Threshold-Sweep und reproduzierbare Artefakte
- Vergleich mit subject-wise Klassifikationsbaselines

Damit wird aus einem Proof-of-Concept ein reproduzierbarer Baustein des Dysbalance-Frameworks.

## Wissenschaftliche Bedeutung

Die WESAD-Ergebnisse stützen die zentrale Annahme der Arbeit:

Physiologische Abweichungen lassen sich nicht nur klassifizieren, sondern durch personalisierte, erklärbare Score-Komponenten sichtbar machen.

Besonders relevant ist, dass der Stresszustand durch den autonomen Score klar hervorgehoben wird:

- Stress besitzt die höchste mittlere autonome Aktivierung.
- Stress überschreitet Aktivierungsschwellen deutlich häufiger als baseline, amusement und meditation.
- Die subject-normalisierte Betrachtung reduziert interindividuelle Unterschiede und macht Zustandsveränderungen vergleichbarer.

Damit liefert WESAD eine zweite, vom PAMAP2-Datensatz unabhängige Evidenz dafür, dass das Dysbalance-Framework über unterschiedliche physiologische Domänen hinweg anwendbar ist.

## Lokale Artefakte

Feature- und Score-Dateien:

- `data/processed/wesad/features/wesad_autonomic_features.csv`
- `data/processed/wesad/dysbalance/wesad_autonomic_scores.csv`

Reports:

- `reports/dysbalance/wesad_autonomic_feature_summary.csv`
- `reports/dysbalance/wesad_autonomic_label_summary.csv`
- `reports/dysbalance/wesad_autonomic_subject_label_summary.csv`
- `reports/dysbalance/wesad_autonomic_threshold_sweep.csv`

Modelle und Klassifikationsreports:

- `reports/models/wesad_minirocket_baseline_summary.json`
- `reports/models/wesad_minirocket_standardized_baseline_summary.json`
- `reports/models/wesad_minirocket_confusion_matrix_raw.png`
- `reports/models/wesad_minirocket_standardized_confusion_matrix_raw.png`
- `models/wesad/wesad_minirocket_subject_split.joblib`
- `models/wesad/wesad_minirocket_standardized_subject_split.joblib`
