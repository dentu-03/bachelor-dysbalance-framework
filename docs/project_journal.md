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
