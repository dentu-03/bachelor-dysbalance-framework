# WESAD MultiRocket Standardized Split Summary

Dieses Dokument fasst die MultiRocket-basierte Auswertung auf WESAD zusammen.

## Rolle im Framework

WESAD bildet in meiner Arbeit die zentrale autonom-physiologische Domäne. Im Unterschied zu PAMAP2 und MHEALTH steht hier nicht primär Bewegungsaktivität im Vordergrund, sondern die Modellierung von Baseline, Stress, Amusement und Meditation anhand multimodaler Chest-Signale.

Die MultiRocket-Auswertung ergänzt die bestehende MiniRocket-Baseline und prüft, ob eine stärkere Rocket-basierte Zeitreihenmodellschicht die subject-wise Generalisierung der WESAD-Zustände verbessert.

## Datengrundlage

| Größe | Wert |
|---|---:|
| Dataset | WESAD |
| Sensorbereich | Chest |
| Train subjects | S2, S3, S4, S5, S6, S7, S8, S9, S10, S11 |
| Test subjects | S13, S14, S15, S16, S17 |
| Train shape | `(5909, 8, 700)` |
| Test shape | `(2983, 8, 700)` |
| Effective timepoints | 700 |
| Temporal stride | 10 |
| Labels | baseline, stress, amusement, meditation |

## Modellkonfiguration

| Parameter | Wert |
|---|---:|
| Model | MultiRocketClassifier |
| n_kernels | 5000 |
| n_jobs | 4 |
| random_state | 42 |
| Preprocessing | train-set channel-wise standardization |
| Temporal reduction | stride 10 |

Die zeitliche Reduktion von 7,000 auf 700 Timepoints pro Fenster wurde verwendet, um MultiRocket auf WESAD ressourcensicher auszuführen. Die Modellvariante ist deshalb als standardisierte, zeitlich reduzierte WESAD-Chest-Auswertung zu interpretieren.

## Modellvergleich

| Model | Variant | Accuracy | Macro F1 | Weighted F1 | Temporal Stride |
|---|---|---:|---:|---:|---:|
| MiniRocket | raw subject split | 0.6433 |  |  | 1 |
| MiniRocket | standardized subject split | 0.7167 |  |  | 1 |
| MultiRocket | standardized subject split stride10 | 0.7730 | 0.6981 | 0.7614 | 10 |

## Aggregierte Ergebnisse

| Metric | Wert |
|---|---:|
| Accuracy | 0.7730 |
| Macro F1 | 0.6981 |
| Weighted F1 | 0.7614 |
| Error rate | 0.2270 |
| Fehler gesamt | 677 |
| Accuracy-Gewinn vs. raw MiniRocket | 0.1297 |
| Accuracy-Gewinn vs. standardized MiniRocket | 0.0563 |

## Subject-spezifische Ergebnisse

| Test Subject | Windows | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| S13 | 597 | 0.6801 | 0.5957 | 0.6755 |
| S14 | 598 | 0.8579 | 0.8315 | 0.8600 |
| S15 | 599 | 0.7462 | 0.6981 | 0.7141 |
| S16 | 595 | 0.7294 | 0.5730 | 0.6947 |
| S17 | 594 | 0.8519 | 0.7495 | 0.8288 |

## Stärkste Testsubjects

| Test Subject | Accuracy | Macro F1 |
|---|---:|---:|
| S14 | 0.8579 | 0.8315 |
| S17 | 0.8519 | 0.7495 |
| S15 | 0.7462 | 0.6981 |

## Schwächste Testsubjects

| Test Subject | Accuracy | Macro F1 |
|---|---:|---:|
| S13 | 0.6801 | 0.5957 |
| S16 | 0.7294 | 0.5730 |
| S15 | 0.7462 | 0.6981 |

## Häufigste Verwechslungen

| True Label | Predicted Label | Errors |
|---|---|---:|
| amusement | stress | 183 |
| meditation | baseline | 152 |
| baseline | amusement | 71 |
| amusement | baseline | 65 |
| meditation | amusement | 57 |
| meditation | stress | 53 |
| baseline | stress | 46 |
| baseline | meditation | 29 |
| amusement | meditation | 10 |
| stress | amusement | 9 |
| stress | baseline | 2 |

Die häufigste Verwechslung ist amusement → stress. Zusätzlich werden meditation-Fenster häufig als baseline, amusement oder stress klassifiziert. Diese Fehlerstruktur ist für die Arbeit besonders relevant, weil sie zeigt, dass WESAD nicht nur ein Klassifikationsproblem, sondern auch ein Problem physiologischer Zustandsüberlappung ist.

## Schwächste subject-class-Kombinationen

| Test Subject | Label | Label Name | Precision | Recall | F1 | Support |
|---|---:|---|---:|---:|---:|---:|
| S16 | 3 | amusement | 0.0625 | 0.0278 | 0.0385 | 72 |
| S13 | 3 | amusement | 0.0794 | 0.0667 | 0.0725 | 75 |
| S17 | 3 | amusement | 0.8333 | 0.2055 | 0.3297 | 73 |
| S15 | 4 | meditation | 0.8909 | 0.3141 | 0.4645 | 156 |
| S16 | 4 | meditation | 1.0000 | 0.4194 | 0.5909 | 155 |
| S15 | 3 | amusement | 0.7955 | 0.4795 | 0.5983 | 73 |
| S14 | 3 | amusement | 0.5795 | 0.6986 | 0.6335 | 73 |
| S16 | 2 | stress | 0.5429 | 1.0000 | 0.7037 | 133 |
| S13 | 1 | baseline | 0.7610 | 0.6638 | 0.7091 | 235 |
| S13 | 2 | stress | 0.6098 | 0.9542 | 0.7440 | 131 |
| S15 | 1 | baseline | 0.6461 | 0.9829 | 0.7797 | 234 |
| S17 | 2 | stress | 0.7194 | 0.9860 | 0.8319 | 143 |

## Interpretation aus Sicht der Arbeit

Die MultiRocket-Ergebnisse verbessern die bisherige WESAD-Baseline deutlich. Besonders wichtig ist dabei nicht nur der absolute Accuracy-Gewinn, sondern die interpretierbare Fehlerstruktur.

Zentrale Beobachtungen:

- Stress wird sehr stark erkannt und weist im Gesamtreport einen sehr hohen Recall auf.
- Amusement ist die schwächste Klasse und wird häufig als stress oder baseline interpretiert.
- Meditation ist grundsätzlich gut erkennbar, zeigt aber subject-spezifische Überlappungen mit baseline und amusement.
- Die subject-spezifischen Ergebnisse schwanken deutlich stärker als bei MHEALTH und PAMAP2.
- Diese Schwankung passt zur biologischen und affektiven Heterogenität autonomer Signale.

Für meine Thesis ist das besonders wertvoll: MultiRocket zeigt, dass eine stärkere Zeitreihenmodellschicht WESAD besser ausnutzen kann als MiniRocket. Gleichzeitig bleiben die Grenzen rein diskriminativer Klassifikation sichtbar.

## Bedeutung für das Dysbalance-Framework

| Ebene | Aussage |
|---|---|
| MultiRocket | verbesserte subject-wise Zustandsklassifikation auf WESAD |
| Autonomic Dysbalance Score | erklärbare Abweichung physiologischer Aktivierungs- und Regulationsmerkmale |
| Isolation Forest | modellbasierte Bestätigung allgemeiner autonomer Abweichungsstruktur |
| Dysbalance Memory | Überführung auffälliger Fenster in Events, Episoden und Hypothesen |

Die Ergebnisse stützen die zentrale Architekturentscheidung der Arbeit: Starke Zeitreihenmodelle liefern Leistungsfähigkeit, während Dysbalance Scores und Memory die erklärbare Interpretationsebene bereitstellen.

## Vergleich zu PAMAP2 und MHEALTH

Im Vergleich zu den funktional-motorischen Datensätzen ist WESAD schwieriger. Das ist kein Nachteil, sondern wissenschaftlich produktiv: Während PAMAP2 und MHEALTH robuste Bewegungsstruktur zeigen, macht WESAD sichtbar, dass autonom-affektive Zustände stärker subject-abhängig und physiologisch überlappend sind.

Damit entsteht eine klare cross-dataset-Rollenverteilung:

| Dataset | Domäne | MultiRocket-Rolle |
|---|---|---|
| PAMAP2 | funktional-motorisch | starke subject-wise Bewegungsmodellierung |
| MHEALTH | funktional-motorisch + ECG | sehr starke externe Bewegungsvalidierung |
| WESAD | autonom-affektiv | schwierige, aber verbesserte Zustandsmodellierung |

## Grenzen

- Die WESAD-MultiRocket-Auswertung verwendet eine zeitliche Reduktion auf 700 Timepoints.
- Der Vergleich mit MiniRocket ist fair hinsichtlich Subject-Split und Standardisierung, aber nicht identisch hinsichtlich zeitlicher Auflösung.
- WESAD ist kein echter Longitudinaldatensatz.
- Die Klassifikation affektiver Zustände ersetzt keine klinische Bewertung.
- Amusement zeigt eine deutliche Modellunsicherheit und sollte in der Interpretation vorsichtig behandelt werden.

## Zwischenfazit

MultiRocket verbessert die WESAD-Subject-Split-Baseline deutlich. Gleichzeitig zeigt die Fehlerstruktur, dass autonom-affektive Zustände schwieriger und stärker subject-abhängig sind als funktional-motorische Bewegungsaktivitäten.

Für meine Arbeit ist WESAD damit kein reiner Performance-Datensatz, sondern ein wichtiger Prüfstein für die Trennung zwischen leistungsstarker Zeitreihenklassifikation und erklärbarer Dysbalance-Modellierung.
