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
