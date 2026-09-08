# MHEALTH MultiRocket LOSO Summary

Dieses Dokument fasst die MultiRocket-basierte Leave-One-Subject-Out-Auswertung auf MHEALTH zusammen.

## Rolle im Framework

MultiRocket wird als stärkere Rocket-basierte Zeitreihenmodellschicht ergänzt.

Die bestehende MiniRocket-Auswertung bleibt als schnelle und robuste Baseline erhalten. MultiRocket dient als leistungsfähigere Referenz, um zu prüfen, ob die segment-sicheren MHEALTH-Tensoren auch unter einer stärkeren Zeitreihenmodellierung stabil generalisieren.

| Ebene | Rolle |
|---|---|
| MiniRocket | schnelle robuste Baseline |
| MultiRocket | stärkere Rocket-basierte Referenzmodellschicht |
| Dysbalance Scores | erklärbare funktionale Abweichungsebene |
| Isolation Forest | modellbasierte Anomaly-Ebene |
| Dysbalance Memory | Event-, Episoden- und Hypothesenebene |

## Datengrundlage

| Größe | Wert |
|---|---:|
| Dataset | MHEALTH |
| Subjects | 10 |
| Windows | 2555 |
| Tensor shape | `(2555, 23, 250)` |
| Channels | 23 |
| Window length | 250 |
| Validation | Leave-One-Subject-Out |

## Modellkonfiguration

| Parameter | Wert |
|---|---:|
| Model | MultiRocketClassifier |
| n_kernels | 10000 |
| random_state | 42 |
| validation | leave-one-subject-out |

## Aggregierte MultiRocket-Ergebnisse

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| Accuracy | 0.9725 | 0.0351 | 0.9202 | 1.0000 |
| Macro F1 | 0.9694 | 0.0400 | 0.9039 | 1.0000 |
| Weighted F1 | 0.9673 | 0.0427 | 0.8991 | 1.0000 |

## Fold-Ergebnisse

| Test Subject | Accuracy | Macro F1 | Weighted F1 |
|---:|---:|---:|---:|
| 1 | 0.9202 | 0.9039 | 0.8991 |
| 10 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 0.9549 | 0.9533 | 0.9516 |
| 3 | 0.9962 | 0.9964 | 0.9962 |
| 4 | 0.9242 | 0.9106 | 0.9066 |
| 5 | 1.0000 | 1.0000 | 1.0000 |
| 6 | 0.9331 | 0.9341 | 0.9238 |
| 7 | 1.0000 | 1.0000 | 1.0000 |
| 8 | 0.9960 | 0.9960 | 0.9960 |
| 9 | 1.0000 | 1.0000 | 1.0000 |

## Vergleich mit MiniRocket LOSO

| Model | Accuracy Mean | Accuracy Std | Accuracy Min | Accuracy Max | Macro F1 Mean |
|---|---:|---:|---:|---:|---:|
| MiniRocket | 0.9521 | 0.0423 | 0.9038 | 1.0000 | 0.9433 |
| MultiRocket | 0.9725 | 0.0351 | 0.9202 | 1.0000 | 0.9694 |

MultiRocket verbessert die mittlere LOSO-Accuracy gegenüber MiniRocket von 0.9521 auf 0.9725. Der mittlere Macro-F1 steigt von 0.9433 auf 0.9694.

## Interpretation

Die MultiRocket-Ergebnisse zeigen, dass die MHEALTH-Tensoren eine sehr starke subject-übergreifend lernbare Zeitreihenstruktur enthalten.

Wissenschaftlich ist besonders wichtig:

- Die Auswertung nutzt Leave-One-Subject-Out statt nur eines festen Subject-Splits.
- MultiRocket erreicht eine höhere mittlere Leistung als MiniRocket.
- Die schwächsten Folds bleiben oberhalb von 0.92 Accuracy.
- Mehrere Subjects erreichen perfekte Klassifikation.
- Die Ergebnisse bestätigen die technische Qualität der segment-sicheren Tensorisierung.

## Bedeutung für das Dysbalance-Framework

MultiRocket ersetzt nicht die erklärbaren Dysbalance Scores. Stattdessen ergänzt es die Modellschicht.

| Baustein | Aussage |
|---|---|
| MultiRocket | starke zeitliche Klassifizierbarkeit der Rohfenster |
| Functional Dysbalance Score | erklärbare funktionale Abweichung vom subject- und activity-spezifischen Referenzzustand |
| Isolation Forest | modellbasierte Bestätigung auffälliger Score-Strukturen |
| Dysbalance Memory | zeitliche Organisation auffälliger Fenster zu Hypothesen |

## Bedeutung für spätere Garmin-/Polar-Daten

Die MultiRocket-Schicht ist direkt anschlussfähig an spätere eigene Zeitreihenfenster.

- Polar-H10-Fenster können als hochauflösende Herz-/RR-Zeitreihen modelliert werden.
- Garmin-Fenster können Kontext-, Aktivitäts- und Tagesstrukturinformationen ergänzen.
- MultiRocket kann als starke Referenzmodellschicht für zeitliche Muster dienen.
- Dysbalance Scores bleiben die erklärbare Ebene.
- Das Memory kann wiederkehrende Pilotmuster als Events, Episoden und Hypothesen speichern.

## Grenzen

- MHEALTH ist ein kontrollierter Activity-Recognition-Datensatz.
- Die hohe Klassifikationsleistung ist keine klinische Dysbalance-Validierung.
- ECG wird im MHEALTH-Kontext nur konservativ als Zusatzsignal betrachtet.
- Die Auswertung zeigt Subjekttransfer, aber noch keine echte Longitudinalität.
- Echte Alltagsvalidierung benötigt TILES oder spätere Pilotdaten.

## Zwischenfazit

MultiRocket wurde erfolgreich als stärkere Rocket-basierte Modellschicht in das MHEALTH-Experiment integriert.

Die Ergebnisse stärken drei zentrale Thesis-Aussagen:

1. Die segment-sichere Tensorisierung erzeugt hochwertige Zeitreihenrepräsentationen.
2. MHEALTH bestätigt die Übertragbarkeit der Modellpipeline auf ein externes multimodales Sensorset.
3. MultiRocket ergänzt das Framework als leistungsfähige Modellreferenz, während Dysbalance Scores und Memory die erklärbare und longitudinale Ebene bilden.
