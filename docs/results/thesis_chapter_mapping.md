# Thesis Chapter Mapping

Dieses Dokument ordnet den aktuellen Projektstand auf eine mögliche Kapitelstruktur der Bachelorarbeit ab.

## Ziel

Das Mapping soll zeigen, welche bestehenden Ergebnisse, Skripte und Dokumente später in welche Thesis-Kapitel überführt werden können.

Es dient nicht als finale Gliederung, sondern als Arbeitsbrücke zwischen Repository und schriftlicher Ausarbeitung.

## Vorgeschlagene Kapitelstruktur

| Kapitel | Arbeitstitel | Hauptfunktion |
|---|---|---|
| 1 | Einleitung | Problem, Motivation, Forschungsfrage |
| 2 | Grundlagen und verwandte Arbeiten | Biosignale, Wearables, Zeitreihenklassifikation, Anomalieerkennung, Erklärbarkeit |
| 3 | Methodik | Framework-Architektur, Datensätze, Scores, Modelle, Memory |
| 4 | Implementierung | Repository-Struktur, Pipelines, technische Umsetzung |
| 5 | Ergebnisse | Datensatz-spezifische und Cross-Dataset-Befunde |
| 6 | Diskussion | Interpretation, Domänenspezifik, Grenzen der Aussagekraft |
| 7 | Fazit und Ausblick | Beitrag, Limitationen, TILES/Pilotdaten |

## Kapitel 1: Einleitung

### Inhaltliche Bausteine

| Baustein | Quelle im Repository | Status |
|---|---|---|
| Motivation personalisierter physiologischer Abweichungen | `docs/results/thesis_consolidation_summary.md` | vorhanden |
| zentrale Forschungsfrage | `docs/results/thesis_consolidation_summary.md` | vorhanden |
| Arbeitsdefinition Dysbalance | `docs/results/thesis_consolidation_summary.md` | vorhanden |
| Abgrenzung zu Diagnostik | `docs/results/framework_cross_dataset_summary.md` | vorhanden |
| Longitudinalitätsproblem | `metadata/longitudinal_memory_design.md` | vorhanden |

### Schreibkern

Die Einleitung sollte erklären, warum reine Klassifikation nicht ausreicht, wenn physiologische Abweichungen personalisiert, erklärbar und über Zeit interpretierbar werden sollen.

## Kapitel 2: Grundlagen und verwandte Arbeiten

### Inhaltliche Bausteine

| Thema | Benötigte Inhalte | Status |
|---|---|---|
| Biosignale und Wearables | ECG, ACC, EDA, RESP, HR, Aktivität, Schlaf | teilweise vorhanden |
| PAMAP2 | Datensatzbeschreibung und Sensorik | vorhanden |
| WESAD | Datensatzbeschreibung und autonom-affektive Zustände | vorhanden |
| MHEALTH | Datensatzbeschreibung und externe Transferrolle | vorhanden |
| TILES-2018 | longitudinale Realweltrolle | vorbereitet |
| Zeitreihenklassifikation | MiniRocket, MultiRocket | methodisch vorhanden |
| Anomaly Detection | Isolation Forest | vorhanden |
| Erklärbarkeit | Score-basierte und komponentenbasierte Interpretation | vorhanden |
| Longitudinal Memory | Events, Episoden, Hypothesen | vorhanden |

### Noch zu ergänzen

Für dieses Kapitel müssen später Literaturquellen und formale Grundlagen ausgearbeitet werden.

## Kapitel 3: Methodik

### Framework-Architektur

| Methodischer Bestandteil | Repository-Quelle |
|---|---|
| Gesamtarchitektur | `docs/results/thesis_consolidation_summary.md` |
| Cross-Dataset Framework | `docs/results/framework_cross_dataset_summary.md` |
| Datensatzrollen | `metadata/expanded_dataset_scope.md` |
| Dysbalance-Definition | `docs/results/thesis_consolidation_summary.md` |
| Anomaly-Konzept | `metadata/anomaly_detection_plan.md` |
| Memory-Konzept | `metadata/longitudinal_memory_design.md` |
| TILES-Konzept | `metadata/tiles2018_integration_plan.md` |

### Score-Methodik

| Score-Typ | Datensatz | Quelle |
|---|---|---|
| funktional-motorisch | PAMAP2 | `src/dysbalance/pamap2_functional_scores.py` |
| funktional-motorisch + ECG-Kontext | MHEALTH | `src/dysbalance/mhealth_functional_scores.py` |
| autonom-physiologisch | WESAD | `src/dysbalance/wesad_autonomic_scores.py` |
| longitudinal subject-day | TILES-2018 | `src/dysbalance/tiles2018_longitudinal_scores.py` |

### Modellmethodik

| Modellschicht | Rolle |
|---|---|
| MiniRocket | Baseline und Vergleich |
| MultiRocket | starke diskriminative Zeitreihen-Referenz |
| Isolation Forest | unsupervised Anomaly-Schicht |
| Memory | temporale Verdichtung zu Hypothesen |

## Kapitel 4: Implementierung

### Technische Bausteine

| Bereich | Dateien |
|---|---|
| Parser | `src/parsers/` |
| Tensorisierung | `src/tensorization/` |
| Preprocessing | `src/preprocessing/` |
| Dysbalance Scores | `src/dysbalance/` |
| Anomaly Detection | `src/anomaly/` |
| Modelle | `src/models/` |
| Longitudinal Memory | `src/longitudinal/` |
| Konfiguration | `configs/datasets.yaml` |
| Metadokumentation | `metadata/` |

### Wichtige Implementierungsargumente

- reproduzierbare Dateipfade,
- klare Trennung von Rohdaten, Zwischendaten, verarbeiteten Daten und Reports,
- kein Commit von Rohdaten,
- generierbare Reports,
- modulare Erweiterbarkeit für TILES und spätere Pilotdaten.

## Kapitel 5: Ergebnisse

### Datensatz-spezifische Ergebnisse

| Dataset | Ergebnisquelle |
|---|---|
| PAMAP2 | `docs/results/pamap2_multirocket_loso_summary.md` |
| WESAD | `docs/results/wesad_multirocket_standardized_split_summary.md` |
| MHEALTH | `docs/results/mhealth_multirocket_loso_summary.md` |

### Cross-Dataset Ergebnisse

| Ergebnisblock | Quelle |
|---|---|
| Cross-Dataset Summary | `docs/results/framework_cross_dataset_summary.md` |
| MultiRocket Vergleich | `docs/results/cross_dataset_multirocket_summary.md` |
| Error-Dysbalance-Link | `docs/results/multirocket_error_dysbalance_link_summary.md` |
| Error-Memory-Link | `docs/results/multirocket_error_memory_link_summary.md` |
| Evidence Matrix | `docs/results/multirocket_evidence_matrix.md` |
| Case Studies | `docs/results/multirocket_error_case_studies.md` |

### Ergebnis-Kernaussage

PAMAP2 liefert den stärksten positiven Zusammenhang zwischen Modellunsicherheit, funktionaler Dysbalance, Anomaly Detection und Memory.

MHEALTH und WESAD zeigen dagegen, dass Klassifikationsfehler nicht pauschal als Dysbalance interpretiert werden dürfen.

## Kapitel 6: Diskussion

### Diskussionsachsen

| Achse | Kernaussage |
|---|---|
| Generalisierbarkeit | Framework funktioniert über mehrere Biosignaldomänen |
| Domänenspezifik | motorische und autonom-affektive Domänen unterscheiden sich deutlich |
| Erklärbarkeit | Scores, Komponenten und Memory schaffen interpretierbare Ebenen |
| Fehlerinterpretation | Fehler können, müssen aber nicht, Dysbalance anzeigen |
| Longitudinalität | Memory ist vorbereitet, echte Langzeitvalidierung steht aus |
| Datenschutz | TILES und Pilotdaten werden bewusst aggregiert geplant |

### Zentrale Diskussionsformulierung

Die Arbeit vermeidet die Gleichsetzung von Modellfehler und Dysbalance. Stattdessen zeigt sie, dass Modellfehler, Dysbalance Scores, Anomaly Detection und Memory in bestimmten Domänen zusammenfallen können, aber stets kontextabhängig interpretiert werden müssen.

## Kapitel 7: Fazit und Ausblick

### Beitrag

Die Arbeit liefert:

1. eine generalisierbare multimodale Biosignal-Pipeline,
2. erklärbare Dysbalance Scores,
3. eine unsupervised Anomaly-Schicht,
4. eine starke MultiRocket-Referenzschicht,
5. eine temporale Memory-Schicht,
6. eine vorbereitete echte longitudinale TILES-Schicht.

### Ausblick

| Ausblick | Rolle |
|---|---|
| TILES-2018 | erste echte longitudinale Realweltprüfung |
| Garmin Forerunner 965 | spätere Aktivitäts-, Schlaf- und Tagesstrukturinformationen |
| Polar H10 | spätere hochauflösende Herz-/RR-Pilotdaten |
| eigene Pilotdaten | explorative Übertragung des Frameworks |

## Schreibreife Einschätzung

| Bereich | Schreibreife |
|---|---|
| Forschungsfrage und Definition | hoch |
| Methodik Framework | hoch |
| PAMAP2 Ergebnisse | hoch |
| WESAD Ergebnisse | hoch |
| MHEALTH Ergebnisse | hoch |
| Cross-Dataset Interpretation | hoch |
| MultiRocket Fehleranalyse | hoch |
| Memory-Konzept | hoch |
| TILES | vorbereitet, aber ohne echte Daten |
| Literaturkapitel | noch auszuarbeiten |
| finale Diskussion | strukturell vorbereitet |

## Nächste Schreibaufgaben

| Priorität | Aufgabe |
|---|---|
| 1 | Methodik-Kapitel aus Framework-Architektur ausformulieren |
| 2 | Ergebnisse nach Datensatz und Cross-Dataset strukturieren |
| 3 | Diskussion der Fehler-Dysbalance-Memory-Differenzierung schreiben |
| 4 | Grundlagen/Literatur mit Quellen ergänzen |
| 5 | TILES und Pilotdaten als ehrlichen Ausblick einordnen |

## Zwischenfazit

Das Repository enthält inzwischen genügend strukturierte Evidenz für einen vollständigen Methodik- und Ergebnisteil.

Die größte verbleibende Schreibarbeit liegt nicht mehr in der technischen Pipeline, sondern in der wissenschaftlichen Ausformulierung, Literaturverankerung und präzisen Diskussion der Grenzen.
