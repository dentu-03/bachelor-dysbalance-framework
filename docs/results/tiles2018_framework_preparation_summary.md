# TILES-2018 Framework Preparation Summary

Dieses Dokument beschreibt den aktuellen Stand der TILES-2018-Vorbereitung im Dysbalance-Framework.

## Aktueller Status

TILES-2018 ist aktuell als echte longitudinale Erweiterung vorbereitet, aber noch nicht datengetrieben integriert.

Lokal liegt noch keine nutzbare TILES-subject-day-Tabelle vor. Deshalb werden keine TILES-Scores, keine TILES-Memory-Events und keine echten longitudinalen TILES-Hypothesen erzeugt.

## Implementierte Vorbereitung

| Komponente | Datei | Status |
|---|---|---|
| Integrationsplan | `metadata/tiles2018_integration_plan.md` | vorbereitet |
| Subject-Day-Schema | `metadata/tiles2018_subject_day_schema.md` | vorbereitet |
| lokales Inventar | `src/parsers/inspect_tiles2018_inventory.py` | implementiert |
| Schema-Validator | `src/parsers/validate_tiles2018_subject_day_schema.py` | implementiert |
| longitudinaler Score-Adapter | `src/dysbalance/tiles2018_longitudinal_scores.py` | implementiert |
| Memory-Event-Adapter | `src/longitudinal/tiles2018_memory_adapter.py` | implementiert |
| optionale Memory-Einbindung | `src/longitudinal/dysbalance_memory.py` | implementiert |

## Geplante Datenkette

data/raw/tiles2018
→ data/interim/tiles2018/subject_day_features.csv
→ data/processed/tiles2018/dysbalance/tiles2018_longitudinal_scores.csv
→ reports/tiles2018/tiles2018_memory_events.csv
→ reports/longitudinal/dysbalance_events.csv
→ reports/longitudinal/dysbalance_episodes.csv
→ reports/longitudinal/dysbalance_hypotheses.csv

## Methodische Bedeutung

TILES ist nicht als weiterer klassischer Klassifikationsdatensatz geplant.

Die Rolle von TILES liegt in der Prüfung, ob die bisher auf kontrollierten Window-Sequenzen entwickelte Dysbalance-Memory-Logik auf echte mehrtägige oder mehrwöchige Realweltsequenzen übertragen werden kann.

## Aktuelle Memory-Auswirkung

Da noch keine TILES-Memory-Events vorhanden sind, bleibt die bestehende Memory-Auswertung unverändert.

| Kennzahl | Wert |
|---|---:|
| Events | 1444 |
| Episoden | 799 |
| Hypothesen | 340 |
| echte longitudinale Hypothesen | 0 |

Damit wird aktuell keine echte TILES-Evidenz behauptet.

## Erwartete TILES-Rolle bei vorhandenen Daten

Wenn eine nutzbare subject-day-Tabelle vorliegt, kann TILES erstmals echte longitudinale Framework-Evidenz liefern.

Dann kann die bestehende Hypothesenlogik für `dataset = tiles2018` automatisch setzen:

| Feld | Wert |
|---|---|
| evidence_scope | `longitudinal_real_world_sequence` |
| is_true_longitudinal_evidence | `True` |

## Datenschutz- und Scope-Grenzen

Die vorbereitete TILES-Integration fokussiert nur aggregierte physiologische oder behaviorale Features.

Nicht vorgesehen sind:

- Audioinhalte.
- Transkripte.
- Freitext.
- Standortverläufe.
- personenbezogene Identifikation.
- Arbeitsplatz- oder Leistungsbewertung.

## Thesis-Interpretation

Der aktuelle Stand ist methodisch wichtig, weil er eine ehrliche Grenze zieht:

> Das Framework ist longitudinal-ready, aber ohne TILES- oder Pilotdaten noch nicht longitudinal validiert.

Diese Trennung verhindert eine Überinterpretation der bisherigen kontrollierten Datensätze.

## Zwischenfazit

TILES-2018 ist nun als echte longitudinale Zielschicht technisch vorbereitet. Die Integration bleibt bewusst datenabhängig: Erst wenn erlaubte subject-day-Daten verfügbar sind, werden echte longitudinale Events, Episoden und Hypothesen erzeugt.
