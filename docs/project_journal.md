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
