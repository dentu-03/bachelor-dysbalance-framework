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
