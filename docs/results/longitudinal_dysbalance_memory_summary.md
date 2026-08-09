# Longitudinal Dysbalance Memory Summary

## Rolle im Framework

Das Longitudinal Dysbalance Memory ist ein Framework-Baustein zur strukturierten Weiterverarbeitung von Dysbalance- und Anomaly-Ergebnissen.

Es transformiert einzelne auffällige Fenster in interpretierbare Verlaufseinheiten:

Window → Event → Episode → Hypothesis

Damit wird der Schritt von einer punktuellen Fensteranalyse zu einer verlaufsfähigen Hypothesenstruktur vorbereitet.

Wichtig:

Das Memory-Modul ist kein diagnostisches System. Es erzeugt Framework-Hypothesen über wiederkehrende oder starke Abweichungsmuster. Diese Hypothesen müssen kontextuell interpretiert werden und sind keine medizinischen Aussagen.

## Motivation

Die bisherigen Framework-Schritte erzeugen Scores und Anomaly-Flags auf Fensterebene:

- PAMAP2: funktional-motorische Dysbalance
- WESAD: autonom-physiologische Dysbalance
- Isolation Forest: modellbasierte Anomaly Scores

Ein einzelnes auffälliges Fenster reicht jedoch nicht aus, um von einem stabilen Muster zu sprechen. Einzelne Auffälligkeiten können durch Sensorrauschen, Übergänge, kurze Bewegungsartefakte oder normale physiologische Variabilität entstehen.

Das Memory-Modul reduziert diese Gefahr, indem es Auffälligkeiten über mehrere Ebenen aggregiert:

1. auffälliges Fenster
2. Dysbalance Event
3. zusammenhängende Episode
4. subject-spezifische Hypothese

## Eingabedaten

Die erste Implementierung nutzt die bereits erzeugten Isolation-Forest-Ausgaben für PAMAP2 und WESAD.

Verwendete Einstellung:

- Feature-Ebene: `component_level`
- Contamination: `0.05`
- maximale Fensterlücke für Episodenbildung: `2`

Eingaben:

- `reports/anomaly/pamap2_isolation_forest_anomaly_scores.csv`
- `reports/anomaly/wesad_isolation_forest_anomaly_scores.csv`

## Event-Regeln

### PAMAP2

Ein PAMAP2-Fenster wird zu einem Event, wenn mindestens eine der folgenden Bedingungen gilt:

- `functional_deviation_strength >= 2.0`
- `is_model_anomaly == True`
- `anomaly_rank_percent >= 95`

Event-Typen:

- `functional_motor_deviation`
- `model_anomaly`
- `combined_score_model_event`
- `high_rank_anomaly`

### WESAD

Für WESAD werden zwei autonome Perspektiven unterschieden:

1. gerichtete autonome Aktivierung
2. ungerichtete autonome Abweichungsstärke

Ein autonomes Aktivierungs-Event entsteht bei:

- `z_autonomic_activation >= 2.0`

Ein autonomes Abweichungs-Event entsteht bei mindestens einer der folgenden Bedingungen:

- `autonomic_deviation_strength >= 1.5`
- `is_model_anomaly == True`
- `anomaly_rank_percent >= 95`

Event-Typen:

- `autonomic_activation`
- `autonomic_deviation`
- `model_anomaly`
- `combined_score_model_event`
- `high_rank_anomaly`

## Episodenbildung

Events werden zu Episoden gruppiert nach:

- Dataset
- Domain
- Subject
- Session
- Event-Typ
- Kontext

Innerhalb dieser Gruppen werden nahe beieinanderliegende Events zusammengefasst.

Initiale Regel:

- maximale Lücke: `2` Fenster

Für PAMAP2 und WESAD ist diese Episodenbildung ein kontrollierter Schema-Test auf Fenstersequenzen. Für TILES-2018 soll dieselbe Logik später auf echte Tages- oder Session-Verläufe übertragen werden.

## Hypothesenbildung

Aus Episoden werden subject-spezifische Hypothesen gebildet.

Eine Hypothese fasst zusammen:

- Dataset
- Subject
- Domain
- Event-Typ
- Kontext
- Anzahl Episoden
- erste und letzte Beobachtung
- mittlere und maximale Episodenstärke
- aktuellen Status
- Evidenzzusammenfassung

Statuswerte:

- `new`
- `observed`
- `confirmed`
- `stable`
- `weakened`
- `discarded`

In der aktuellen Implementierung treten auf PAMAP2 und WESAD nur `new`, `observed` und `confirmed` auf.

Wichtig:

`confirmed` bedeutet hier nur, dass eine Hypothese innerhalb des Framework-Schemas wiederholt oder stark beobachtet wurde. Es bedeutet keine medizinische oder klinische Bestätigung.

## Overclaiming-Schutz

Da PAMAP2 und WESAD keine echten mehrwöchigen Longitudinaldatensätze sind, enthält jede Hypothese zusätzliche Felder:

- `evidence_scope`
- `is_true_longitudinal_evidence`
- `status_interpretation`

Für PAMAP2 und WESAD gilt:

- `evidence_scope = controlled_window_sequence`
- `is_true_longitudinal_evidence = False`

Damit wird explizit dokumentiert, dass die aktuelle Memory-Anwendung ein kontrollierter Schema-Test ist.

Echte longitudinale Evidenz soll später über TILES-2018 entstehen.

## Ergebnisse

Die erste Memory-Auswertung erzeugte:

| Ebene | Anzahl |
|---|---:|
| Events | 1316 |
| Episodes | 686 |
| Hypotheses | 249 |

### Events nach Datensatz

| Dataset | Events |
|---|---:|
| WESAD | 934 |
| PAMAP2 | 382 |

### Episoden nach Datensatz

| Dataset | Episodes |
|---|---:|
| WESAD | 448 |
| PAMAP2 | 238 |

### Hypothesen nach Datensatz

| Dataset | Hypotheses |
|---|---:|
| PAMAP2 | 132 |
| WESAD | 117 |

### Hypothesenstatus nach Datensatz

| Dataset | confirmed | observed | new |
|---|---:|---:|---:|
| PAMAP2 | 25 | 107 | 0 |
| WESAD | 62 | 51 | 4 |

### Hypothesentypen nach Datensatz

| Dataset | autonomic_activation | autonomic_deviation | combined_score_model_event | functional_motor_deviation | model_anomaly |
|---|---:|---:|---:|---:|---:|
| PAMAP2 | 0 | 0 | 83 | 2 | 47 |
| WESAD | 23 | 13 | 38 | 0 | 43 |

### Events nach Typ

| Event-Typ | Anzahl |
|---|---:|
| combined_score_model_event | 602 |
| autonomic_activation | 391 |
| model_anomaly | 223 |
| autonomic_deviation | 98 |
| functional_motor_deviation | 2 |

## Interpretation

Die Ergebnisse zeigen, dass aus den vorhandenen Score- und Anomaly-Ausgaben eine strukturierte Memory-Schicht erzeugt werden kann.

Bei PAMAP2 entstehen viele `combined_score_model_event`-Hypothesen. Das passt zur vorherigen Overlap- und Korrelationsanalyse: Der funktionale Dysbalance-Score und der Isolation-Forest-Anomaly-Score stimmen bei PAMAP2 sehr stark überein.

Bei WESAD ist das Bild differenzierter. Es entstehen Hypothesen für:

- gerichtete autonome Aktivierung
- ungerichtete autonome Abweichung
- kombinierte Score-Modell-Evidenz
- reine Modell-Anomalien

Das bestätigt erneut, dass WESAD nicht nur als Stress-vs-Nicht-Stress-Problem interpretiert werden sollte. Das Framework unterscheidet zwischen gerichteter Aktivierung und allgemeiner autonomer Auffälligkeit.

## Bedeutung für TILES-2018

Das Memory-Modul wurde bewusst so entworfen, dass TILES-2018 später anschließen kann.

PAMAP2 und WESAD dienen aktuell als Schema-Test:

- Fenster werden zu Events.
- Events werden zu Episoden.
- Episoden werden zu Hypothesen.

TILES soll anschließend echte longitudinale Evidenz liefern:

- subject-day events
- mehrtägige Episoden
- wiederkehrende Muster über Wochen
- Statusänderungen wie stable oder weakened

Damit wird TILES nicht als weiterer isolierter Datensatz behandelt, sondern als natürlicher nächster Schritt des Frameworks.

## Bedeutung für den Polar-Pilot

Auch der geplante Polar-Brustgurt-Test kann später dasselbe Schema nutzen.

Mögliche spätere Felder:

- `dataset = polar_pilot`
- `domain = autonomic` oder `mixed_sensor`
- `subject_id = pilot_001`
- `session_id = konkrete Messsession`

Der Pilot-Test wäre eine explorative Demonstration, keine Validierung.

## Grafische Darstellung

Zusätzlich wurden zwei Übersichtsplots für das Longitudinal Dysbalance Memory erzeugt:

- `reports/figures/longitudinal_memory_hypothesis_status_by_dataset.png`
- `reports/figures/longitudinal_memory_hypothesis_types_by_dataset.png`

Die Plots visualisieren die Verteilung der Hypothesenstatus sowie die Verteilung der Hypothesentypen getrennt nach Datensatz.

Sie dienen als kompakte Ergebnisübersicht und unterstützen die Interpretation der Memory-Schicht auf aggregierter Ebene.

## Lokale Artefakte

Erzeugte Dateien:

- `reports/longitudinal/dysbalance_events.csv`
- `reports/longitudinal/dysbalance_episodes.csv`
- `reports/longitudinal/dysbalance_hypotheses.csv`
- `reports/longitudinal/dysbalance_memory_summary.json`

Quellcode:

- `src/longitudinal/dysbalance_memory.py`

Design-Dokument:

- `metadata/longitudinal_memory_design.md`

## Grenzen

Die aktuelle Memory-Auswertung besitzt wichtige Grenzen:

- PAMAP2 und WESAD sind keine echten Langzeitdatensätze.
- Die Episodenlogik basiert zunächst auf Fensterabständen.
- Statuswerte wie `confirmed` sind framework-intern zu verstehen.
- Es gibt keine klinische Validierung.
- Sensorartefakte können Events erzeugen.
- Kontextuelle Interpretation bleibt notwendig.
- Echte longitudinale Aussagen sind erst mit TILES-2018 oder Pilotdaten möglich.

## Zwischenfazit

Das Longitudinal Dysbalance Memory schließt die bisher offene methodische Lücke zwischen Fensteranalyse und longitudinaler Verfolgung.

Aktuell zeigt es:

- Score- und Anomaly-Ausgaben lassen sich in Events überführen.
- Events lassen sich zu Episoden gruppieren.
- Episoden lassen sich zu subject-spezifischen Hypothesen aggregieren.
- Die Hypothesen bleiben durch `evidence_scope` und `status_interpretation` sauber begrenzt.
- Das Schema ist vorbereitet für TILES-2018 und spätere Pilotdaten.

Damit ist der longitudinale Framework-Baustein konzeptionell und technisch vorbereitet.
