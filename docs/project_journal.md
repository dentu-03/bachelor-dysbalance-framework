# Project Journal

Dieses Dokument begleitet die Bachelorarbeit fortlaufend und dokumentiert Arbeitsschritte, Entscheidungen, Erkenntnisse und offene Fragen.

## 2026-07-03 – Projektstart

Das Bachelor-Projekt wurde als eigenständiges Git-Repository angelegt.

Ziel ist die Weiterentwicklung des KI-Studienprojekts zu einem KI-basierten, multimodalen Dysbalance-Framework mit:

- Parser- und Tensorisierungspipeline
- MultiRocket-basierter Zeitreihenanalyse
- personalisierter Referenzmodellierung
- erklärbaren Dysbalance-Scores
- Anomalieerkennung
- longitudinaler Musterverfolgung
- GUI-Demonstrator

## 2026-07-03 – Entscheidung: Fortführung statt kompletter Neustart

Die Bachelorarbeit wird nicht als komplett neues Projekt begonnen, sondern als methodische Weiterentwicklung des Studienprojekts.

Begründung:

- bestehende Parser-/Tensorisierungslogik kann als Grundlage dienen
- Vorarbeit bleibt wissenschaftlich anschlussfähig
- Bachelorarbeit kann stärker auf KI-Methodik, Generalisierung und Anomalieerkennung fokussieren
- neue Datensätze erweitern den wissenschaftlichen Wert

## 2026-07-03 – Sichtung der alten Studienprojekt-Codebasis

Relevante alte Dateien wurden identifiziert.

Ergebnis der ersten Sichtung:

- `windowing.py` ist nur ein Platzhalter und wird nicht direkt übernommen
- `rms.py` enthält eine einfache RMS-Funktion und kann als Grundlage dienen
- `phase3_multimodal_score.py` enthält eine wichtige Score-Fusion-Idee, ist aber noch stark POC- und pfadabhängig

Entscheidung:

Die Konzepte aus dem Studienprojekt werden übernommen, aber als allgemeine, wiederverwendbare Module neu aufgebaut.

Zu übernehmende Konzepte:

- Windowing
- Tensorisierung
- RMS / Feature-Berechnung
- Log-Ratio-Logik
- personalisierte Z-Normierung
- Threshold-Sweeps
- Dysbalance-Scores
- multimodale Score-Fusion
- Reports und Metadaten

## 2026-07-03 – Sichtung der Phase-2-Dysbalance-POCs

Die alten POCs für EMG- und Stress-Dysbalance wurden geprüft.

Erkenntnis:

Die POCs enthalten die methodisch wichtigsten Bausteine für die Bachelorarbeit:

- Log-Ratio-basierte Dysbalance-Metriken
- personalisierte Z-Normierung
- Threshold-Sweeps
- Subjekt-bezogene Auswertung
- erklärbare Score-Logik
- CSV-/Report-Ausgabe

Entscheidung:

Die Logik wird nicht 1:1 übernommen, sondern in allgemeine Framework-Module überführt. Dadurch wird das neue Bachelor-Projekt sauberer, wiederverwendbarer und wissenschaftlich besser dokumentierbar.

## 2026-07-03 – Artifact-Strategie festgelegt

Es wurde entschieden, dass das Bachelorprojekt systematisch wissenschaftliche Artefakte erzeugen soll.

Ziel ist nicht nur lauffähiger Code, sondern eine reproduzierbare Sammlung aus:

- Tabellen
- Reports
- Metriken
- Grafiken
- Confusion Matrices
- Score-Verteilungen
- Threshold-Sweeps
- longitudinalen Trendplots
- GUI-Screenshots
- Paper-/Thesis-Figures

Diese Artefakte sollen die spätere Bachelorarbeit, Präsentation und mögliche Paper-Struktur visuell und wissenschaftlich stärken.

## 2026-07-03 – Erste generalisierte Dysbalance-Module implementiert

Aus den Phase-2-Proof-of-Concepts des Studienprojekts wurden die zentralen methodischen Bausteine nicht direkt kopiert, sondern als allgemeine Framework-Module neu aufgebaut.

Implementierte Module:

- `src/dysbalance/normalization.py`
- `src/dysbalance/ratios.py`
- `src/dysbalance/thresholds.py`

Wissenschaftliche Bedeutung:

Diese Module bilden die erste stabile Grundlage für die erklärbare Dysbalance-Analyse der Bachelorarbeit.

Abgebildete Methodik:

1. Log-Ratio-Transformation  
   Verhältnisse werden symmetrisch modelliert. Verdopplung und Halbierung erhalten denselben Abstand mit unterschiedlichem Vorzeichen.

2. Personalisierte Z-Normierung  
   Werte werden relativ zum individuellen Referenzzustand einer Person oder Gruppe bewertet.

3. Threshold-Sweep  
   Auffälligkeiten werden nicht nur bei einem einzelnen Grenzwert betrachtet, sondern über mehrere Schwellenwerte robust ausgewertet.

Erkenntnis:

Damit ist der Übergang vom alten POC-Code zu einer wiederverwendbaren Framework-Logik begonnen. Die Bachelorarbeit erhält dadurch eine klarere methodische Struktur als das Studienprojekt.

## 2026-07-03 – PAMAP2 Protocol Parser und Erstinspektion

Der erste neue Datensatz der Bachelorarbeit, PAMAP2, wurde als Protocol-Datensatz initial eingelesen.

Implementiertes Modul:

- `src/parsers/parse_pamap2.py`

Der Parser benennt die offiziellen 54 PAMAP2-Spalten und ergänzt zusätzlich eine `subject_id`-Spalte. Dadurch entstehen beim geladenen DataFrame 55 Spalten.

Ergebnis der Erstinspektion:

- 9 Protocol-Dateien wurden erkannt.
- Die meisten Subjects besitzen mehrere hunderttausend Samples.
- `subject109.dat` ist deutlich kürzer und enthält nur die Aktivitätslabels 0 und 24.
- Die Herzfrequenzspalte weist ca. 90.8 Prozent fehlende Werte auf.
- Dieses Verhalten ist plausibel, da die IMU-Signale mit höherer Frequenz vorliegen als die Herzfrequenz.

Wissenschaftliche Bedeutung:

PAMAP2 ist damit als erster neuer multimodaler Datensatz technisch angebunden. Die Analyse bestätigt außerdem eine wichtige methodische Herausforderung der Bachelorarbeit: unterschiedliche Abtastraten und fehlende Werte zwischen Modalitäten müssen systematisch behandelt werden.

Nächste Schritte:

- Aktivitätslabels dokumentieren
- relevante IMU- und HR-Kanäle auswählen
- Cleaning-Strategie definieren
- Fensterung und Tensorisierung vorbereiten

## 2026-07-03 – PAMAP2 Initial Cleaning Summary

Für PAMAP2 wurde ein erstes Cleaning-Summary-Skript implementiert:

- `src/preprocessing/clean_pamap2.py`

Das Skript setzt die zuvor dokumentierte Cleaning-Strategie praktisch um:

- Auswahl von 22 erklärbaren Startspalten
- Ausschluss von Aktivitätslabel `0`
- Ausschluss von Subject `109` für die erste robuste Pipeline-Iteration
- Erzeugung eines lokalen Summary-Artefakts unter `reports/datasets/pamap2_initial_cleaning_summary.csv`

Ergebnis:

- Für Subjects 101–108 bleiben jeweils ca. 174k bis 272k Samples erhalten.
- Subject 109 wird erwartungsgemäß vollständig aus der ersten Pipeline ausgeschlossen.
- Die Herzfrequenz-Missingness bleibt bei ca. 90.8 Prozent.
- Das bestätigt, dass HR nicht zeilenweise naiv behandelt werden darf, sondern später über eine eigene Resampling-/Imputationsstrategie integriert werden muss.

Methodische Bedeutung:

Dieser Schritt trennt Rohdateninspektion von echter Modellvorbereitung. Dadurch bleibt nachvollziehbar, welche Daten aus methodischen Gründen ausgeschlossen wurden und welche Modalitäten in der ersten Framework-Iteration verwendet werden.

## 2026-07-03 – PAMAP2 Cleaned Interim Files erzeugt

Die PAMAP2-Cleaning-Pipeline wurde erweitert, sodass nicht nur ein Summary-Report erzeugt wird, sondern auch echte bereinigte Zwischenartefakte.

Erzeugte lokale Dateien:

- `data/interim/pamap2/protocol_cleaned/subject101_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject102_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject103_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject104_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject105_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject106_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject107_cleaned.pkl.gz`
- `data/interim/pamap2/protocol_cleaned/subject108_cleaned.pkl.gz`

Subject 109 erzeugt kein Clean-Artefakt, da es für die erste robuste Pipeline-Iteration ausgeschlossen wird und nach Filterung keine Zeilen übrig bleiben.

Validierung:

- 8 Clean-Dateien wurden erzeugt.
- Gesamtgröße der Clean-Artefakte: ca. 197 MB.
- `subject101_cleaned.pkl.gz` besitzt die Form `(249957, 22)`.
- Die Spalten entsprechen exakt der dokumentierten ersten Cleaning-Strategie.

Methodische Bedeutung:

Damit ist PAMAP2 als erster neuer Datensatz nicht nur theoretisch ausgewählt, sondern praktisch in eine reproduzierbare Zwischenrepräsentation überführt. Dieser Zustand bildet die direkte Grundlage für Fensterung, Tensorisierung und spätere MultiRocket-Experimente.

## 2026-07-03 – Reusable Sliding Window Utilities

Ein allgemeines Windowing-Modul wurde implementiert:

- `src/tensorization/windowing.py`

Das Modul stellt wiederverwendbare Funktionen bereit für:

- Berechnung gültiger Sliding-Window-Startindizes
- Umwandlung von 2D-Zeitreihen in aeon-kompatible Tensoren
- Majority-Labeling pro Fenster
- Start- und Endzeitpunkte pro Fenster

Die erzeugte Tensorform entspricht dem in Studienprojekt und Bachelorarbeit verwendeten Standard:

`(n_windows, n_channels, n_timepoints)`

Methodische Bedeutung:

Damit wurde ein bisher nur implizit oder POC-artig vorhandener Bestandteil des Studienprojekts als saubere, wiederverwendbare Framework-Komponente neu implementiert. Dieses Modul bildet die Grundlage für die PAMAP2-Tensorisierung und spätere datasetübergreifende Verarbeitung.

## 2026-07-03 – Segment-sichere PAMAP2-Tensorisierung

Für PAMAP2 wurde eine erste konkrete Tensorisierung implementiert:

- `src/tensorization/tensorize_pamap2.py`

Zunächst wurde Subject 101 als kontrollierter Einzeltest tensorisiert.

Einstellungen:

- Fenstergröße: 500 Samples
- Schrittweite: 250 Samples
- angenommene Samplingrate: 100 Hz
- Fensterdauer: ca. 5 Sekunden
- Overlap: 50 Prozent
- Tensorform: `(n_windows, n_channels, n_timepoints)`

Erster naiver Versuch:

- 998 Fenster
- 20 Fenster liefen über große Zeitlücken
- maximale Fensterdauer: ca. 245 Sekunden

Problem:

Nach Entfernung von Label `0` entstehen Zeitlücken. Wenn danach naiv über den bereinigten DataFrame gefenstert wird, können Fenster über entfernte transiente Phasen oder Aktivitätswechsel laufen. Das ist methodisch unsauber.

Korrektur:

Die Tensorisierung wurde segment-sicher gemacht. Neue Segmente entstehen bei:

- Zeitlücke größer als 0.05 Sekunden
- Aktivitätswechsel

Heart Rate wird nur innerhalb solcher Segmente interpoliert.

Finales Ergebnis für Subject 101:

- `X shape`: `(979, 19, 500)`
- `y shape`: `(979,)`
- `metadata shape`: `(979, 9)`
- Fenster länger als 5.2 Sekunden: `0`

Methodische Bedeutung:

Dieser Schritt ist zentral für die wissenschaftliche Qualität der Pipeline. Er verhindert, dass künstliche Fenster über entfernte oder physiologisch nicht zusammenhängende Zeitbereiche entstehen. Damit ist die erste PAMAP2-Tensorisierung reproduzierbar und methodisch vertretbar.

## 2026-07-03 – PAMAP2 Tensor Imputation und finaler Subject-101-Tensor

Für die PAMAP2-Tensorisierung wurde ein allgemeines Imputation-Modul implementiert:

- `src/preprocessing/imputation.py`

Die Imputation ersetzt NaN-Werte in 3D-Zeitreihentensoren kanalweise durch den jeweiligen Kanal-Median. Falls ein Kanal vollständig aus NaN-Werten bestehen sollte, wird ein definierter Fallback-Wert verwendet.

Das PAMAP2-Tensorisierungsskript speichert nun zusätzlich:

- `X_subject101.npy`
- `y_subject101.npy`
- `metadata_subject101.csv`
- `channel_medians_subject101.npy`

Finale Validierung für Subject 101:

- `X shape`: `(979, 19, 500)`
- `y shape`: `(979,)`
- `metadata shape`: `(979, 9)`
- `overall_nan_pct`: `0.0`
- Fenster länger als 5.2 Sekunden: `0`
- Anzahl Aktivitätsklassen: `12`

Methodische Bedeutung:

Damit ist der erste neue Datensatz der Bachelorarbeit bis zu einem modellbereiten, aeon-kompatiblen Tensor verarbeitet. Die Pipeline umfasst nun Rohdatenimport, Cleaning, Segmentierung, HR-Interpolation, Sliding Windowing, Majority-Labeling, Metadatenexport und NaN-Imputation.

## 2026-07-03 – PAMAP2 By-Subject Tensorisierung abgeschlossen

Die PAMAP2-Tensorisierung wurde von einem kontrollierten Einzeltest mit Subject 101 auf alle validen Subjects erweitert.

Verarbeitete Subjects:

- 101
- 102
- 103
- 104
- 105
- 106
- 107
- 108

Subject 109 bleibt für die erste robuste Pipeline-Iteration ausgeschlossen.

Erzeugte lokale Artefakte:

- `data/processed/pamap2/by_subject/X_subject*.npy`
- `data/processed/pamap2/by_subject/y_subject*.npy`
- `data/processed/pamap2/by_subject/metadata_subject*.csv`
- `data/processed/pamap2/by_subject/channel_medians_subject*.npy`

Validierung:

- 8 X-Dateien
- 8 y-Dateien
- 8 Metadaten-Dateien
- 8 Kanal-Median-Dateien
- Gesamtzahl Fenster: `7587`
- Tensorform pro Subject: `(n_windows, 19, 500)`
- NaNs nach Imputation: `0`
- Fenster länger als 5.2 Sekunden: `0`
- Gesamtgröße der by-subject Artefakte: ca. `551 MB`

Methodische Bedeutung:

PAMAP2 ist damit als erster neuer multimodaler Datensatz vollständig bis zu modellbereiten, aeon-kompatiblen Zeitreihentensoren verarbeitet. Die Pipeline ist reproduzierbar, segment-sicher, dokumentiert und für erste MultiRocket- oder MiniRocket-Baseline-Experimente vorbereitet.

## 2026-07-03 – Erste PAMAP2 MiniRocket Activity-Classification-Baseline

Für PAMAP2 wurde eine erste KI-Baseline mit MiniRocket implementiert:

- `src/models/train_pamap2_activity_baseline.py`

Aufgabe:

- Activity Classification auf PAMAP2
- Input: by-subject Tensoren
- Tensorform: `(n_windows, 19, 500)`
- Modell: `MiniRocketClassifier`
- Split: subject-wise

Split:

- Training: Subjects 101, 102, 103, 104, 105, 106
- Test: Subjects 107, 108

Datenumfang:

- Train shape: `(5647, 19, 500)`
- Test shape: `(1940, 19, 500)`
- Train NaNs: `0`
- Test NaNs: `0`
- Testklassen: 12 Aktivitätsklassen

Ergebnis:

- Accuracy: `0.9541`
- Macro F1: ca. `0.94`
- Weighted F1: ca. `0.95`

Erzeugte lokale Artefakte:

- `reports/models/pamap2_minirocket_baseline_summary.json`
- `reports/models/pamap2_minirocket_classification_report.json`
- `reports/models/pamap2_minirocket_classification_report.txt`
- `reports/models/pamap2_minirocket_confusion_matrix.csv`
- `reports/models/pamap2_minirocket_confusion_matrix_raw.png`
- `reports/models/pamap2_minirocket_confusion_matrix_normalized.png`
- `models/pamap2/pamap2_minirocket_subject_split.joblib`

Methodische Bedeutung:

Die hohe Accuracy zeigt, dass die PAMAP2-Pipeline technisch und methodisch funktionsfähig ist. Parser, Cleaning, Segmentierung, HR-Interpolation, Imputation, Tensorisierung und Labeling erzeugen modellierbare Zeitreihenrepräsentationen. Damit steht die erste KI-Baseline der Bachelorarbeit auf einem neuen öffentlichen multimodalen Datensatz.

## 2026-07-03 – PAMAP2 Functional Dysbalance Scores

Auf Basis der PAMAP2-Tensoren wurden erste funktionale Bewegungsfeatures und daraus erklärbare Abweichungsscores berechnet.

Implementierte Module:

- `src/dysbalance/pamap2_movement_features.py`
- `src/dysbalance/pamap2_functional_scores.py`
- `src/dysbalance/plot_pamap2_functional_scores.py`

Berechnete Bewegungsfeatures:

- RMS der Beschleunigung pro Sensorposition
- RMS der Gyroskopdaten pro Sensorposition
- mittlere Extremitätenbewegung
- Gesamtbewegungsintensität
- Log-Ratio Extremitäten/Chest
- Log-Ratio Hand/Ankle

Erster Functional-Dysbalance-Score:

Die drei Features

- `total_acc_rms`
- `log_extremity_chest_acc_ratio`
- `log_hand_ankle_acc_ratio`

wurden pro Subject und Aktivität z-normalisiert. Dadurch beschreibt der Score nicht einfach hohe Bewegung, sondern Abweichung von der individuellen Referenz innerhalb derselben Aktivität.

Der aggregierte Score `functional_deviation_strength` ist der Mittelwert der absoluten z-Werte dieser drei Komponenten.

Ergebnisse:

- Score-Tabelle: `(7587, 26)`
- Threshold-Report: `(272, 8)`
- Subject-Summary: `(8, 12)`
- NaNs: `0`
- maximale Functional Deviation Strength: ca. `7.15`
- Anteil `functional_deviation_strength > 2.0`: ca. `3.39 %` bis `4.40 %` je Subject

Erzeugte lokale Artefakte:

- `data/processed/pamap2/features/pamap2_movement_features.csv`
- `data/processed/pamap2/dysbalance/pamap2_functional_scores.csv`
- `reports/dysbalance/pamap2_movement_feature_summary.csv`
- `reports/dysbalance/pamap2_functional_threshold_sweep.csv`
- `reports/dysbalance/pamap2_functional_subject_summary.csv`
- `reports/figures/pamap2_functional_deviation_by_subject.png`
- `reports/figures/pamap2_functional_deviation_by_activity.png`

Methodische Bedeutung:

Damit wurde die Pipeline erstmals von reiner Aktivitätsklassifikation zu erklärbarer, personalisierter Abweichungsmodellierung erweitert. Das ist der zentrale Übergang vom Studienprojekt zur Bachelorarbeit: KI und Zeitreihenverarbeitung dienen nicht nur der Klassifikation, sondern der interpretierbaren Erkennung individueller physiologischer und funktionaler Abweichungsmuster.

## 2026-07-03 – WESAD als autonom-physiologischer Referenzdatensatz integriert

WESAD wurde aus dem Studienprojekt in das Bachelor-Arbeitsverzeichnis übernommen und als autonom-physiologischer Referenzdatensatz eingebunden.

Rohdatenquelle im Studienprojekt:

- `/home/dennis_preusch/Dokumente/UNI/5.Semester/KI-Studienprojekt/project-data/raw/wesad`

Ziel im Bachelorprojekt:

- `data/raw/wesad`

Validierung des Imports:

- Gesamtgröße: ca. `17 GB`
- Subject-PKL-Dateien: `15`
- Subjects: S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S13, S14, S15, S16, S17

Implementiertes Modul:

- `src/parsers/parse_wesad_chest.py`

Bezug zum Studienprojekt:

Im Studienprojekt wurde WESAD bereits für ROCKET-basierte Stressklassifikation und für eine autonome Dysbalance-Proof-of-Concept-Analyse verwendet. Die Bachelorarbeit führt diese Methodik fort, organisiert sie aber in einer saubereren, wiederverwendbaren Pipeline.

Tensorisierungsstrategie:

- Chest-Signale only
- Kanäle: ACC x/y/z, ECG, EMG, EDA, Temp, Resp
- 8 Kanäle insgesamt
- Samplingrate: 700 Hz
- Fenstergröße: 7000 Samples
- Fensterdauer: 10 Sekunden
- Schrittweite: 3500 Samples
- Overlap: 50 Prozent
- Labels: 1 baseline, 2 stress, 3 amusement, 4 meditation
- Labels 0, 6 und 7 werden ausgeschlossen

Verbesserung gegenüber dem Studienprojekt:

Die neue Bachelor-Version nutzt segment-sicheres Windowing. Fenster werden nur innerhalb gültiger, zusammenhängender Labelsegmente erzeugt. Dadurch entstehen keine Fenster über irrelevante oder transiente Labelbereiche hinweg.

Erzeugte lokale Artefakte:

- `data/interim/wesad/chest_by_subject/X_S*.npy`
- `data/interim/wesad/chest_by_subject/y_S*.npy`
- `data/interim/wesad/chest_by_subject/metadata_S*.csv`
- `reports/datasets/wesad_chest_tensorization_summary.csv`

Validierung:

- 15 X-Dateien
- 15 y-Dateien
- 15 Metadaten-Dateien
- Gesamtzahl Fenster: `8892`
- Tensorform pro Subject: `(n_windows, 8, 7000)`
- NaNs: `0`
- Größe der WESAD-Interim-Artefakte: ca. `3.8 GB`

Methodische Bedeutung:

Mit WESAD steht nun neben PAMAP2 ein zweiter vollständig tensorisierter Datensatz im Bachelor-Framework zur Verfügung. Während PAMAP2 den funktional-motorischen Analysepfad abbildet, repräsentiert WESAD den autonom-physiologischen Analysepfad. Damit wird die im Studienprojekt entwickelte multimodale Dysbalance-Idee systematisch in der Bachelorarbeit fortgeführt.

## 2026-07-03 – WESAD MiniRocket Baselines und Standardisierungseffekt

Für WESAD wurden erste MiniRocket-Baselines auf den segment-sicher erzeugten Chest-Tensoren trainiert.

Aufgabe:

- Klassifikation der Zustände baseline, stress, amusement und meditation
- Input: WESAD Chest Tensoren
- Tensorform: `(n_windows, 8, 7000)`
- Modell: `MiniRocketClassifier`
- Split: subject-wise

Subject-wise Split:

- Training: S2, S3, S4, S5, S6, S7, S8, S9, S10, S11
- Test: S13, S14, S15, S16, S17

Datenumfang:

- Train shape: `(5909, 8, 7000)`
- Test shape: `(2983, 8, 7000)`
- Train NaNs: `0`
- Test NaNs: `0`

Baseline ohne Standardisierung:

- Accuracy: `0.6433`
- Macro F1: ca. `0.54`
- Weighted F1: ca. `0.62`

Baseline mit trainingsbasierter kanalweiser Standardisierung:

- Accuracy: `0.7167`
- Macro F1: ca. `0.66`
- Weighted F1: ca. `0.71`

Verbesserung:

- Accuracy: +`0.0734`
- Macro F1: +ca. `0.12`
- Weighted F1: +ca. `0.09`

Erzeugte lokale Artefakte:

- `reports/models/wesad_minirocket_baseline_summary.json`
- `reports/models/wesad_minirocket_classification_report.txt`
- `reports/models/wesad_minirocket_confusion_matrix_raw.png`
- `reports/models/wesad_minirocket_confusion_matrix_normalized.png`
- `models/wesad/wesad_minirocket_subject_split.joblib`
- `reports/models/wesad_minirocket_standardized_baseline_summary.json`
- `reports/models/wesad_minirocket_standardized_classification_report.txt`
- `reports/models/wesad_minirocket_standardized_confusion_matrix_raw.png`
- `reports/models/wesad_minirocket_standardized_confusion_matrix_normalized.png`
- `models/wesad/wesad_minirocket_standardized_subject_split.joblib`

Bezug zum Studienprojekt:

Im Studienprojekt wurde WESAD bereits mit ROCKET-basierten Methoden sehr erfolgreich klassifiziert. Die aktuelle Bachelor-Auswertung verwendet jedoch einen strengeren subject-wise Split und eine segment-sichere Tensorisierung. Dadurch ist das Ergebnis nicht direkt als schlechtere Leistung zu interpretieren, sondern als realistischere Generalisierungsprüfung über Personen hinweg.

Methodische Bedeutung:

Die Verbesserung durch kanalweise Standardisierung zeigt, dass WESAD stark durch Signal-Skalen und Personenunterschiede geprägt ist. Das unterstützt die zentrale Annahme der Bachelorarbeit: Für physiologische Biosignale reicht reine globale Klassifikation nicht aus. Personalisierte Normalisierung und erklärbare Abweichungsmodellierung sind notwendig, um robuste und interpretierbare Aussagen zu ermöglichen.
