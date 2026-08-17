# MHEALTH Pipeline Summary

## Rolle im Framework

MHEALTH wird als kompakter externer Validierungsdatensatz in das Dysbalance-Framework integriert.

Der Datensatz ergänzt die bisherigen Framework-Bausteine:

- PAMAP2: funktional-motorische Dysbalance
- WESAD: autonom-physiologische Dysbalance
- MHEALTH: externe multimodale Transferprüfung mit Bewegungssignalen und chest ECG

MHEALTH ist damit kein Ersatz für PAMAP2 oder WESAD, sondern ein Brückendatensatz.

Die zentrale wissenschaftliche Rolle besteht darin zu prüfen, ob sich die bestehende Pipeline auf einen weiteren multimodalen Biosignal-Datensatz übertragen lässt.

## Datenimport

Der Datensatz wurde lokal unter folgendem Pfad abgelegt:

- `data/raw/mhealth/`

Verwendetes Archiv:

- `data/raw/mhealth/mhealth_dataset.zip`

Extrahierte Struktur:

- `data/raw/mhealth/MHEALTHDATASET/README.txt`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject1.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject2.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject3.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject4.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject5.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject6.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject7.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject8.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject9.log`
- `data/raw/mhealth/MHEALTHDATASET/mHealth_subject10.log`

Die ZIP-Datei bleibt lokal und wird nicht versioniert.

## Rohdatenstruktur

Die technische Inspektion ergab:

| Eigenschaft | Wert |
|---|---:|
| Subject-Dateien | 10 |
| Rohspalten pro Datei | 24 |
| Labels pro Subject | 0-12 |
| Fehlende Werte | 0 |
| Samplingrate | 50 Hz |

Die README beschreibt 12 Aktivitäten sowie eine zusätzliche Nullklasse.

Label `0` repräsentiert Null-, Übergangs- oder Nicht-Aktivitätsphasen und wird für die erste Activity- und Dysbalance-Pipeline ausgeschlossen.

## Parser

Parser:

- `src/parsers/parse_mhealth.py`

Der Parser liest alle zehn Subject-Logs, vergibt explizite Spaltennamen, ergänzt Subject-ID, Sample-Index und Aktivitätsnamen und speichert komprimierte CSV-Dateien im Interim-Bereich.

Erzeugte lokale Outputs:

- `data/interim/mhealth/subjects/subject_01.csv.gz`
- `data/interim/mhealth/subjects/subject_02.csv.gz`
- `data/interim/mhealth/subjects/subject_03.csv.gz`
- `data/interim/mhealth/subjects/subject_04.csv.gz`
- `data/interim/mhealth/subjects/subject_05.csv.gz`
- `data/interim/mhealth/subjects/subject_06.csv.gz`
- `data/interim/mhealth/subjects/subject_07.csv.gz`
- `data/interim/mhealth/subjects/subject_08.csv.gz`
- `data/interim/mhealth/subjects/subject_09.csv.gz`
- `data/interim/mhealth/subjects/subject_10.csv.gz`
- `data/interim/mhealth/mhealth_subject_summary.csv`
- `data/interim/mhealth/mhealth_label_distribution.csv`

## Parser-Ergebnisse

| Kennzahl | Wert |
|---|---:|
| Gesamtzeilen | 1,215,745 |
| Aktivitätszeilen ohne Label 0 | 343,195 |
| Nullklassen-Zeilen | 872,550 |
| NaNs | 0 |

Die Nullklasse dominiert die Rohdaten deutlich. Diese Beobachtung ist methodisch wichtig, da ein Einschluss von Label `0` die Klassifikation und Dysbalance-Auswertung stark verzerren würde.

## Tensorisierung

Tensorisierung:

- `src/tensorization/tensorize_mhealth.py`

Einstellung:

| Parameter | Wert |
|---|---:|
| Window size | 250 Samples |
| Window duration | 5 Sekunden |
| Step size | 125 Samples |
| Step duration | 2.5 Sekunden |
| Samplingrate | 50 Hz |
| Signal channels | 23 |
| Label 0 | ausgeschlossen |

Die Tensorisierung ist segment-sicher. Fenster werden nur innerhalb zusammenhängender Aktivitätsabschnitte erzeugt und überschreiten keine Label-Grenzen.

## Tensor-Outputs

Erzeugte lokale Outputs:

- `data/interim/mhealth/by_subject/subject_01_X.npy`
- `data/interim/mhealth/by_subject/subject_01_y.npy`
- `data/interim/mhealth/by_subject/subject_01_metadata.csv`
- entsprechende Dateien für Subjects 02-10
- `data/interim/mhealth/by_subject/mhealth_tensor_summary.csv`

Tensorform:

- `X = (n_windows, 23, 250)`
- `y = (n_windows,)`

## Tensorisierungsergebnisse

| Subject | Windows | Channels | Window size | NaNs |
|---:|---:|---:|---:|---|
| 1 | 263 | 23 | 250 | False |
| 2 | 266 | 23 | 250 | False |
| 3 | 265 | 23 | 250 | False |
| 4 | 264 | 23 | 250 | False |
| 5 | 253 | 23 | 250 | False |
| 6 | 239 | 23 | 250 | False |
| 7 | 251 | 23 | 250 | False |
| 8 | 248 | 23 | 250 | False |
| 9 | 255 | 23 | 250 | False |
| 10 | 251 | 23 | 250 | False |

Gesamtzahl erzeugter Fenster:

- 2,555

## Fensterverteilung nach Aktivitätslabel

| Label | Aktivität | Fenster |
|---:|---|---:|
| 1 | standing_still | 230 |
| 2 | sitting_relaxing | 230 |
| 3 | lying_down | 230 |
| 4 | walking | 230 |
| 5 | climbing_stairs | 224 |
| 6 | waist_bends_forward | 211 |
| 7 | frontal_elevation_arms | 221 |
| 8 | knees_bending | 219 |
| 9 | cycling | 230 |
| 10 | jogging | 230 |
| 11 | running | 230 |
| 12 | jump_front_back | 70 |

Label `12` ist deutlich kleiner als die übrigen Aktivitätsklassen. Klassifikationsmetriken für diese Klasse müssen daher vorsichtig interpretiert werden.

## Wissenschaftliche Einordnung

Die bisherige MHEALTH-Integration zeigt, dass die bestehende Pipeline auf einen weiteren multimodalen Datensatz übertragbar ist.

Besonders relevant ist die strukturelle Nähe zu PAMAP2:

- mehrere Körpersensoren
- Aktivitätslabels
- segment-sichere Fenster
- vergleichbare 5-Sekunden-Fenster

Zusätzlich enthält MHEALTH chest ECG und schafft dadurch eine konzeptionelle Brücke zur physiologischen Analyse in WESAD und zu späteren Brustgurt-basierten Pilotdaten.

## Supervised Activity Baseline

Nach Import und Tensorisierung wurde eine erste MiniRocket-basierte Activity-Baseline berechnet.

Modell:

- `MiniRocketClassifier`
- Eingabeform: `(n_windows, 23, 250)`
- 23 Signal-Kanäle
- 5-Sekunden-Fenster
- Label `0` ausgeschlossen

### Subject-Split 1-8 vs. 9-10

Erster Split:

| Split | Subjects | Windows |
|---|---|---:|
| Train | 1-8 | 2,049 |
| Test | 9-10 | 506 |

Ergebnis:

| Metrik | Wert |
|---|---:|
| Accuracy | 1.0000 |
| Macro F1 | 1.0000 |
| Weighted F1 | 1.0000 |

Dieses Ergebnis zeigt, dass MHEALTH sehr klare lernbare Aktivitätsstrukturen enthält. Es darf jedoch nicht isoliert überinterpretiert werden, da nur ein einzelner Subject-Split geprüft wurde.

### Leave-One-Subject-Out Robustness Check

Zur robusteren Einschätzung wurde zusätzlich ein Leave-One-Subject-Out-Experiment über alle zehn Subjects durchgeführt.

| Test Subject | Accuracy | Macro F1 | Weighted F1 |
|---:|---:|---:|---:|
| 1 | 0.9506 | 0.9488 | 0.9463 |
| 2 | 0.9248 | 0.9106 | 0.9073 |
| 3 | 0.9132 | 0.8889 | 0.8843 |
| 4 | 0.9242 | 0.9106 | 0.9066 |
| 5 | 1.0000 | 1.0000 | 1.0000 |
| 6 | 0.9038 | 0.8889 | 0.8717 |
| 7 | 0.9084 | 0.8889 | 0.8778 |
| 8 | 0.9960 | 0.9960 | 0.9960 |
| 9 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 |

Aggregierte LOSO-Ergebnisse:

| Metrik | Mittelwert | Standardabweichung | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Accuracy | 0.9521 | 0.0423 | 0.9038 | 1.0000 |
| Macro F1 | 0.9433 | 0.0511 | 0.8889 | 1.0000 |
| Weighted F1 | 0.9390 | 0.0556 | 0.8717 | 1.0000 |

### Klassenbezogene Beobachtungen

Die schwächsten mittleren F1-Werte über LOSO traten bei folgenden Aktivitäten auf:

| Aktivität | Mean Precision | Mean Recall | Mean F1 |
|---|---:|---:|---:|
| running | 0.9139 | 0.8261 | 0.7908 |
| jogging | 0.8070 | 0.8435 | 0.8000 |
| sitting_relaxing | 0.8500 | 0.9000 | 0.8667 |
| lying_down | 0.9000 | 0.9000 | 0.9000 |

Die meisten übrigen Aktivitäten erreichen nahezu perfekte oder perfekte mittlere Werte.

Die niedrigeren Werte für `jogging` und `running` sind plausibel, da beide Aktivitäten dynamisch ähnlich sind und subject-spezifisch unterschiedlich ausgeführt werden können.

### Wissenschaftliche Interpretation

Die MHEALTH-Baseline bestätigt die Übertragbarkeit der bestehenden segment-sicheren Multisensor-Pipeline auf einen externen Datensatz.

Der einzelne Subject-Split erreicht eine perfekte Testleistung. Die LOSO-Ergebnisse zeigen jedoch ein differenzierteres und wissenschaftlich belastbareres Bild: Die Generalisierung ist insgesamt hoch, variiert aber zwischen Subjects und Aktivitätsklassen.

Damit erfüllt MHEALTH seine Rolle als kompakter externer Validierungsdatensatz.

## Grenzen

Die aktuelle Pipeline ist noch eine technische Integrations- und Tensorisierungsstufe.

Noch nicht enthalten sind:

- supervised activity baseline
- Dysbalance-Features
- Dysbalance-Scores
- Anomaly-Analyse
- Memory-Anbindung
- ECG-spezifische Auswertung

Die ECG-Kanäle werden zunächst konservativ behandelt und nicht klinisch interpretiert.

## Zwischenfazit

MHEALTH ist erfolgreich importiert, geparst und segment-sicher tensorisiert.

Der Datensatz ist technisch sauber:

- keine fehlenden Werte
- konsistente 24-Spalten-Struktur
- alle Subjects enthalten Labels 0-12
- alle Aktivitätsklassen 1-12 sind nach Ausschluss von Label 0 verfügbar
- 2,555 segment-sichere 5-Sekunden-Fenster wurden erzeugt

Damit ist MHEALTH bereit für eine erste subject-wise Activity-Baseline.
