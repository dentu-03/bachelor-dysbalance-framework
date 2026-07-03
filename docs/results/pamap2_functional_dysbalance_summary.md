# PAMAP2 Functional Dysbalance Summary

## Einordnung in die Bachelorarbeit

PAMAP2 ist der erste neue öffentliche multimodale Datensatz, der im Rahmen der Bachelorarbeit vollständig durch die entwickelte Pipeline verarbeitet wurde.

Der Datensatz dient nicht nur als Aktivitätsklassifikationsproblem, sondern als erster praktischer Nachweis dafür, dass die im Studienprojekt entwickelte Methodik auf einen neuen Datensatz übertragen werden kann.

Im Studienprojekt wurde bereits gezeigt, dass physiologische und funktionale Signale nicht nur klassifiziert, sondern auch in erklärbare Abweichungsmaße überführt werden können. Dort wurden insbesondere folgende methodische Bausteine entwickelt:

- physiologisch motivierte Verhältnisbildung
- Log-Ratio-Transformation
- personenbezogene Z-Normalisierung
- Threshold-Sweeps
- Aggregation auffälliger Fenster auf Personen- oder Zustandsniveau

In der Bachelorarbeit wird diese Logik nun verallgemeinert und auf neue multimodale Datensätze übertragen.

PAMAP2 bildet dabei den ersten motorisch-funktionalen Anwendungsfall.

## Ausgangspunkt: Von Klassifikation zu Abweichungsmodellierung

Zunächst wurde auf PAMAP2 eine MiniRocket-basierte Activity-Classification-Baseline trainiert.

Diese Baseline hatte zwei Aufgaben:

1. technische Validierung der Pipeline
2. Nachweis, dass die erzeugten Tensoren sinnvolle zeitliche Signaturen enthalten

Das Ergebnis war eine subject-wise Test Accuracy von:

`0.9541`

Damit wurde bestätigt, dass Parser, Cleaning, Segmentierung, Imputation, Tensorisierung und Labeling eine modellierbare Repräsentation erzeugen.

Der nächste Schritt war jedoch bewusst keine reine Optimierung der Klassifikation, sondern der Übergang zur erklärbaren Dysbalance-Analyse.

## Feature-Berechnung

Auf Basis der segment-sicheren PAMAP2-Tensoren wurden funktionale Bewegungsfeatures berechnet.

Die Feature-Berechnung verwendet die vorhandenen IMU-Sensorpositionen:

- Hand
- Chest
- Ankle

Berechnete Feature-Gruppen:

- RMS der Beschleunigung pro Sensorposition
- RMS der Gyroskopdaten pro Sensorposition
- mittlere Extremitätenbewegung
- Gesamtbewegungsintensität
- Log-Ratio Extremitäten/Chest
- Log-Ratio Hand/Ankle

Die resultierende Feature-Tabelle besitzt die Form:

`(7587, 22)`

Die Tabelle enthält keine fehlenden Werte.

## Log-Ratio-Motivation

Die Log-Ratio-Transformation wurde bereits im Studienprojekt als zentrale Methode verwendet, um Verhältnisse symmetrisch zu modellieren.

Beispiel:

- Verhältnis `2 / 1` ergibt einen positiven Log-Wert
- Verhältnis `1 / 2` ergibt einen gleich starken negativen Log-Wert

Dadurch wird nicht nur die Stärke, sondern auch die Richtung einer funktionalen Relation abbildbar.

Für PAMAP2 wurden insbesondere folgende Relationen verwendet:

- Extremitätenbewegung im Verhältnis zur Chest-Bewegung
- Handbewegung im Verhältnis zur Ankle-Bewegung

Diese Relationen sind nicht als medizinische Diagnose zu verstehen, sondern als funktionale Bewegungsmarker.

## Score-Definition

Für den ersten Functional-Dysbalance-Score wurden drei erklärbare Features ausgewählt:

- `total_acc_rms`
- `log_extremity_chest_acc_ratio`
- `log_hand_ankle_acc_ratio`

Diese Features wurden pro Subject und Aktivität z-normalisiert.

Damit wird nicht gefragt:

> Bewegt sich eine Person generell stark?

Sondern:

> Weicht ein Fenster von der individuellen Referenz derselben Person innerhalb derselben Aktivität ab?

Diese Normalisierung ist zentral für die Bachelorarbeit, weil sie den Übergang von globaler Klassifikation zu personalisierter Abweichungsmodellierung ermöglicht.

## Functional Deviation Strength

Der aggregierte Score lautet:

`functional_deviation_strength`

Er wird als Mittelwert der absoluten z-Werte der drei Score-Komponenten berechnet.

Verwendete Komponenten:

- `z_total_acc_rms`
- `z_log_extremity_chest_acc_ratio`
- `z_log_hand_ankle_acc_ratio`

Interpretation:

- niedriger Wert: Fenster liegt nahe an der individuellen Aktivitätsreferenz
- hoher Wert: Fenster weicht stark von der individuellen Aktivitätsreferenz ab

## Ergebnisse

Erzeugte Tabellen:

- Score-Tabelle: `(7587, 26)`
- Threshold-Report: `(272, 8)`
- Subject-Summary: `(8, 12)`

Validierung:

- NaNs: `0`
- maximale Functional Deviation Strength: ca. `7.15`

Der Anteil auffälliger Fenster mit

`functional_deviation_strength > 2.0`

liegt je Subject ungefähr zwischen:

`3.39 %` und `4.40 %`

Das ist plausibel, weil die Z-Normalisierung innerhalb von Subject und Aktivität erfolgt. Der Score identifiziert dadurch nicht einfach intensive Aktivitäten, sondern ungewöhnliche Ausführungen innerhalb einer vergleichbaren Aktivitätsklasse.

## Beispielhafte Interpretation

Die stärksten Abweichungen treten in konkreten Fenstern mit Zeitstempeln, Subject-ID und Aktivitätslabel auf.

Dadurch kann das Framework auffällige Abschnitte nicht nur quantitativ zählen, sondern auch lokalisieren.

Diese Eigenschaft ist für die Bachelorarbeit wichtig, weil sie eine Brücke zwischen maschineller Zeitreihenanalyse und erklärbarer Ergebnisdarstellung bildet.

Das System gibt nicht nur eine Klassifikation aus, sondern erzeugt interpretierbare Hinweise wie:

- welches Subject betroffen ist
- welche Aktivität betroffen ist
- welches Zeitfenster auffällig ist
- welche Score-Komponenten zur Auffälligkeit beitragen

## Grafische Ergebnisdarstellung

Für die Functional Deviation Strength wurden zwei Plots erzeugt:

- `reports/figures/pamap2_functional_deviation_by_subject.png`
- `reports/figures/pamap2_functional_deviation_by_activity.png`

Die Plots zeigen die Verteilung des Scores nach Subject und Aktivität.

Zusätzlich wurden Schwellenlinien bei `1.5` und `2.0` eingezeichnet, um auffällige Bereiche visuell einzuordnen.

## Bezug zum Studienprojekt

Im Studienprojekt wurden bereits zwei zentrale Beispiele für erklärbare Dysbalance-Modellierung umgesetzt:

1. muskuläre Dysbalance anhand von EMG-Verhältnissen
2. autonome Dysbalance anhand von Stress-/Erholungsrelationen in WESAD

Die aktuelle PAMAP2-Auswertung überträgt diese Logik auf funktionale Bewegungsdaten.

Der Unterschied zur Studienprojektphase liegt darin, dass die Methodik nun stärker als wiederverwendbares Framework organisiert ist:

- allgemeine Log-Ratio-Funktionen
- allgemeine Z-Normalisierung
- allgemeiner Threshold-Sweep
- datasetbezogene Feature-Extraktion
- reproduzierbare Artefakte
- dokumentierte Ergebnisberichte

Damit ist PAMAP2 nicht nur ein weiteres Klassifikationsexperiment, sondern der erste neue Nachweis, dass die im Studienprojekt entwickelte Idee auf ein neues multimodales Setting übertragbar ist.

## Wissenschaftliche Bedeutung

Dieser Schritt markiert den Übergang von einer reinen Aktivitätserkennung zu einer erklärbaren, personalisierten Abweichungsanalyse.

Die Bachelorarbeit baut damit systematisch auf dem Studienprojekt auf:

- Studienprojekt: Proof-of-Concept für Dysbalance-Metriken
- Bachelorarbeit: Generalisierung zu einem multimodalen, wiederverwendbaren Framework

PAMAP2 liefert dabei den funktional-motorischen Baustein.

WESAD kann im nächsten Schritt als autonom-physiologischer Referenzdatensatz eingebunden werden, da es bereits im Studienprojekt für stressbezogene Dysbalance-Analysen genutzt wurde.
