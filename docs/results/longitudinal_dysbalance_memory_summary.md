# Longitudinal Dysbalance Memory Summary

Dieses Dokument beschreibt den aktuellen Stand des Longitudinal Dysbalance Memory. Die Memory-Schicht überführt Fenster-basierte Dysbalance- und Anomaly-Ergebnisse in eine höhere Struktur aus Events, Episoden und Hypothesen.

Der aktuelle Stand integriert:

- PAMAP2
- WESAD
- MHEALTH

Alle drei Datensätze werden weiterhin als kontrollierte Sequenzdaten interpretiert. Es wird keine echte longitudinale Evidenz behauptet.

## Rolle im Framework

Das Longitudinal Dysbalance Memory bildet die Brücke zwischen einzelnen auffälligen Fenstern und einer späteren longitudinalen Beobachtung.

Die Pipeline lautet:

1. Window-level Dysbalance Scores
2. Window-level Anomaly Detection
3. Dysbalance Events
4. Dysbalance Episodes
5. Subject-specific Dysbalance Hypotheses
6. Evidence Scope und Status-Interpretation

Damit ist die Memory-Schicht ein vorbereitender Framework-Baustein für spätere Langzeitdaten und Pilotmessungen.

## Motivation

Ein einzelnes auffälliges Fenster ist nur begrenzt aussagekräftig. Erst wenn Auffälligkeiten wiederholt auftreten, zeitlich gruppiert sind oder in ähnlichen Kontexten erscheinen, entsteht eine Hypothese über ein mögliches wiederkehrendes Muster.

Das Memory-System dient deshalb nicht der Diagnose, sondern der strukturierten Verwaltung von Auffälligkeitshypothesen.

## Eingabedaten

Aktuell werden drei Anomaly-Ausgaben verwendet:

| Dataset | Input | Feature Set | Contamination |
|---|---|---|---:|
| PAMAP2 | `reports/anomaly/pamap2_isolation_forest_anomaly_scores.csv` | `component_level` | 0.05 |
| WESAD | `reports/anomaly/wesad_isolation_forest_anomaly_scores.csv` | `component_level` | 0.05 |
| MHEALTH | `reports/anomaly/mhealth/mhealth_isolation_forest_predictions.csv` | `movement_component_level` | 0.05 |

Die Feature-Set-Unterscheidung ist wichtig, weil MHEALTH eine eigene Anomaly-Datei mit anderen Spaltennamen besitzt. MHEALTH verwendet `is_anomaly` statt `is_model_anomaly` und besitzt keine `anomaly_score_z` oder `anomaly_rank_percent`-Spalten.

## Event-Regeln

### PAMAP2

PAMAP2-Events entstehen aus:

- `functional_deviation_strength >= 2.0`
- modellbasierter Anomaly Detection
- hoher Anomaly-Rank-Position

Mögliche Event-Typen:

- `combined_score_model_event`
- `functional_motor_deviation`
- `model_anomaly`
- `high_rank_anomaly`

### WESAD

WESAD-Events entstehen aus:

- `z_autonomic_activation >= 2.0`
- `autonomic_deviation_strength >= 1.5`
- modellbasierter Anomaly Detection
- hoher Anomaly-Rank-Position

Mögliche Event-Typen:

- `autonomic_activation`
- `autonomic_deviation`
- `combined_score_model_event`
- `model_anomaly`
- `high_rank_anomaly`

### MHEALTH

MHEALTH-Events entstehen aus:

- `functional_deviation_strength >= 2.0`
- modellbasierter Anomaly Detection auf `movement_component_level`

Mögliche Event-Typen:

- `combined_score_model_event`
- `functional_motor_deviation`
- `model_anomaly`

MHEALTH wird funktional-motorisch interpretiert. Die ECG-Komponente bleibt ein konservatives Zusatzsignal und wird nicht klinisch interpretiert.

## Episodenbildung

Events werden zu Episoden gruppiert, wenn sie innerhalb desselben Kontexts nah beieinander liegen.

Gruppierungskriterien:

- Dataset
- Domain
- Subject
- Session
- Event-Typ
- Context Name

Zusätzlich gilt:

| Parameter | Wert |
|---|---:|
| `MAX_GAP_WINDOWS` | 2 |

Das bedeutet: Events desselben Typs und Kontexts werden zu einer Episode verbunden, wenn zwischen ihren Fensterindizes höchstens zwei Fenster Abstand liegen.

## Hypothesenbildung

Episoden werden zu subject-spezifischen Hypothesen aggregiert.

Gruppierungskriterien:

- Dataset
- Domain
- Subject
- Event-Typ
- Context Name

Für jede Hypothese werden unter anderem gespeichert:

- Anzahl Episoden
- erste Beobachtung
- letzte Beobachtung
- mittlere Episodenstärke
- maximale Episodenstärke
- Wiederholungszahl
- aktueller Status
- Evidence Scope
- Interpretationshinweis
- Limitationshinweis

## Statuslogik

Die aktuelle Statuslogik ist framework-intern:

| Status | Regel |
|---|---|
| `new` | einzelne schwächere Episode |
| `observed` | zwei Episoden oder starke Einzelepisode |
| `confirmed` | mindestens drei Episoden |

Diese Statuswerte sind keine klinischen Bestätigungen. Sie dienen nur der internen Priorisierung von Hypothesen.

## Overclaiming-Schutz

Alle aktuellen PAMAP2-, WESAD- und MHEALTH-Hypothesen erhalten:

| Feld | Wert |
|---|---|
| `evidence_scope` | `controlled_window_sequence` |
| `is_true_longitudinal_evidence` | `False` |

Damit bleibt klar: Die aktuellen Ergebnisse sind longitudinal-ready, aber noch keine echten longitudinalen Befunde.

Echte longitudinale Evidenz wäre erst mit alltagsnahen Langzeitdaten oder Pilotdaten möglich.

## Aktuelle Gesamtergebnisse

| Größe | Wert |
|---|---:|
| Events | 1,444 |
| Episodes | 799 |
| Hypotheses | 340 |
| True longitudinal hypotheses | 0 |

## Events nach Datensatz

| Dataset | Events |
|---|---:|
| WESAD | 934 |
| PAMAP2 | 382 |
| MHEALTH | 128 |

## Episoden nach Datensatz

| Dataset | Episodes |
|---|---:|
| WESAD | 448 |
| PAMAP2 | 238 |
| MHEALTH | 113 |

## Hypothesen nach Datensatz

| Dataset | Hypotheses |
|---|---:|
| PAMAP2 | 132 |
| WESAD | 117 |
| MHEALTH | 91 |

## Hypothesenstatus

| Status | Count |
|---|---:|
| observed | 191 |
| confirmed | 88 |
| new | 61 |

## Events nach Typ

| Event Type | Count |
|---|---:|
| combined_score_model_event | 615 |
| autonomic_activation | 391 |
| model_anomaly | 338 |
| autonomic_deviation | 98 |
| functional_motor_deviation | 2 |

## Episoden nach Typ

| Event Type | Count |
|---|---:|
| combined_score_model_event | 319 |
| model_anomaly | 270 |
| autonomic_activation | 144 |
| autonomic_deviation | 64 |
| functional_motor_deviation | 2 |

## Hypothesen nach Typ

| Event Type | Count |
|---|---:|
| model_anomaly | 168 |
| combined_score_model_event | 134 |
| autonomic_activation | 23 |
| autonomic_deviation | 13 |
| functional_motor_deviation | 2 |

## MHEALTH-Erweiterung

Die Integration von MHEALTH erweitert das Memory um eine externe funktional-motorische Validierungsebene.

MHEALTH trägt bei:

| Größe | Wert |
|---|---:|
| Events | 128 |
| Episodes | 113 |
| Hypotheses | 91 |

MHEALTH-Events bestehen aus:

| Event Type | Count |
|---|---:|
| model_anomaly | 115 |
| combined_score_model_event | 13 |

MHEALTH-Hypothesenstatus:

| Status | Count |
|---|---:|
| new | 57 |
| observed | 33 |
| confirmed | 1 |

Die eine bestätigte MHEALTH-Hypothese ist framework-intern zu verstehen. Sie zeigt wiederkehrende kontrollierte Sequenzauffälligkeit, aber keine echte longitudinale oder klinische Bestätigung.

## Interpretation

Die Memory-Erweiterung zeigt, dass sich mehrere Datensätze in eine gemeinsame Ereignis- und Hypothesenstruktur überführen lassen.

PAMAP2 liefert funktional-motorische Bewegungsauffälligkeiten.

WESAD liefert autonom-physiologische Auffälligkeiten.

MHEALTH liefert eine externe funktional-motorische Transferprüfung mit Chest-, Arm-, Ankle- und ECG-Signalen.

Gemeinsam zeigen die drei Datensätze:

- Window Scores lassen sich in Events überführen.
- Events lassen sich zu Episoden gruppieren.
- Episoden lassen sich zu Subject-Hypothesen aggregieren.
- Die Hypothesen bleiben durch `evidence_scope` begrenzt.
- Das Framework ist bereit für echte longitudinale Daten.

## Bedeutung für TILES-2018

TILES bleibt die wichtigste öffentliche Option für echte longitudinale Evidenz.

Mögliche spätere TILES-Struktur:

- `dataset = tiles2018`
- `evidence_scope = longitudinal_real_world_sequence`
- subject-day events
- mehrtägige Episoden
- wiederkehrende Muster über Wochen
- Statusänderungen wie `stable`, `weakened` oder `discarded`

TILES würde damit nicht nur einen weiteren Datensatz darstellen, sondern die erste echte Langzeitprüfung der Memory-Schicht.

## Bedeutung für Garmin Forerunner 965 und Polar H10

Für spätere Validierung und Tests stehen Garmin Forerunner 965 und Polar H10 als mögliche eigene Pilot-Sensorik zur Verfügung.

Diese Pilotdaten können später als Real-World-Validation-Layer dienen.

Mögliche spätere Felder:

| Feld | Beispiel |
|---|---|
| `dataset` | `garmin_polar_pilot` |
| `domain` | `mixed_sensor` oder `autonomic` |
| `subject_id` | `pilot_001` |
| `session_id` | konkrete Messsession |
| `evidence_scope` | `session_or_pilot_sequence` oder später `longitudinal_real_world_sequence` |

Wichtig: Diese Geräte werden im aktuellen Stand noch nicht ausgewertet. Sie dienen als spätere Validierungs- und Testperspektive.

Für die Thesis ist diese Einordnung wertvoll, weil sie zeigt, dass das Framework nicht nur auf öffentliche Datensätze beschränkt ist, sondern für spätere reale Sensoraufnahmen vorbereitet wurde.

## Grafische Darstellung

Zusätzlich wurden zwei Übersichtsplots für das Longitudinal Dysbalance Memory erzeugt:

- `reports/figures/longitudinal_memory_hypothesis_status_by_dataset.png`
- `reports/figures/longitudinal_memory_hypothesis_types_by_dataset.png`

Die Plots visualisieren die Verteilung der Hypothesenstatus sowie die Verteilung der Hypothesentypen getrennt nach Datensatz.

## Lokale Artefakte

Erzeugte Dateien:

- `reports/longitudinal/dysbalance_events.csv`
- `reports/longitudinal/dysbalance_episodes.csv`
- `reports/longitudinal/dysbalance_hypotheses.csv`
- `reports/longitudinal/dysbalance_memory_summary.json`

Quellcode:

- `src/longitudinal/dysbalance_memory.py`
- `src/longitudinal/plot_dysbalance_memory.py`

Design-Dokument:

- `metadata/longitudinal_memory_design.md`

## Grenzen

Die aktuelle Memory-Auswertung besitzt wichtige Grenzen:

- PAMAP2, WESAD und MHEALTH sind keine echten Langzeitdatensätze.
- Die Episodenlogik basiert zunächst auf Fensterabständen.
- Statuswerte wie `confirmed` sind framework-intern zu verstehen.
- Es gibt keine klinische Validierung.
- Sensorartefakte können Events erzeugen.
- Kontextuelle Interpretation bleibt notwendig.
- Garmin- und Polar-Daten sind noch nicht erhoben oder integriert.
- Echte longitudinale Aussagen sind erst mit TILES-2018 oder Pilotdaten möglich.

## Zwischenfazit

Das Longitudinal Dysbalance Memory schließt die methodische Lücke zwischen Fensteranalyse und longitudinaler Verfolgung.

Aktuell zeigt es:

- PAMAP2, WESAD und MHEALTH lassen sich gemeinsam in die Memory-Struktur überführen.
- Score- und Anomaly-Ausgaben lassen sich in Events überführen.
- Events lassen sich zu Episoden gruppieren.
- Episoden lassen sich zu subject-spezifischen Hypothesen aggregieren.
- Alle aktuellen Hypothesen bleiben durch `evidence_scope` sauber begrenzt.
- Das Schema ist vorbereitet für TILES-2018 sowie spätere Garmin-/Polar-Pilotdaten.

Damit ist der longitudinale Framework-Baustein konzeptionell und technisch longitudinal-ready.
