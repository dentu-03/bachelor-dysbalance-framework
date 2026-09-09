# TILES-2018 Subject-Day Schema

Dieses Dokument definiert das minimale kanonische Format für eine spätere TILES-2018-Integration.

## Zweck

TILES-2018 soll als echte longitudinale Ebene in das Dysbalance-Framework eingebunden werden.

Da die Rohdaten lokal noch nicht vorhanden sind, wird zunächst ein neutrales subject-day-Zielformat definiert. Dieses Format kann später aus erlaubten TILES-Dateien oder aus eigenen Garmin-/Polar-Pilotdaten erzeugt werden.

## Granularität

Die erste Integrationsstufe arbeitet nicht auf Rohsignalebene, sondern auf Tages- oder Beobachtungsfenster-Ebene.

Empfohlene Einheit:

> eine Zeile = ein Teilnehmer an einem Studientag oder einem längeren Beobachtungsfenster

## Pflichtspalten

| Spalte | Typ | Beschreibung |
|---|---|---|
| dataset | string | immer `tiles2018` |
| subject_id | string | pseudonyme Teilnehmerkennung |
| day_index | integer | fortlaufender Tag je Teilnehmer |
| timestamp_start | datetime/string | Beginn des Beobachtungsfensters |
| timestamp_end | datetime/string | Ende des Beobachtungsfensters |
| source_level | string | empfohlen: `subject_day` |
| missingness_rate | float | Anteil fehlender Werte zwischen 0 und 1 |

## Empfohlene physiologische und behaviorale Spalten

| Spalte | Typ | Bedeutung |
|---|---|---|
| hr_mean | float | mittlere Herzfrequenz |
| hr_std | float | Streuung der Herzfrequenz |
| resting_hr | float | Ruheherzfrequenz, falls verfügbar |
| activity_total | float | Aktivitätsmaß, z.B. Schritte oder Aktivitätsminuten |
| sedentary_minutes | float | inaktive Minuten |
| sleep_duration | float | Schlafdauer |
| sleep_quality | float | Schlafqualität oder Schlafscore |
| stress_context | float/string | Survey- oder Kontextvariable zu Stress |
| affect_context | float/string | Survey- oder Kontextvariable zu Affect/Well-being |

## Abgeleitete Dysbalance-Spalten

Diese Spalten entstehen nach subject-spezifischer Normalisierung.

| Spalte | Typ | Bedeutung |
|---|---|---|
| z_hr_mean | float | robuste Abweichung der Tagesherzfrequenz vom individuellen Referenzniveau |
| z_hr_std | float | robuste Abweichung der Herzfrequenzstreuung |
| z_activity_total | float | robuste Abweichung der Aktivität |
| z_sleep_duration | float | robuste Abweichung der Schlafdauer |
| z_sleep_quality | float | robuste Abweichung der Schlafqualität |
| longitudinal_deviation_strength | float | kombinierter longitudinaler Dysbalance Score |

## Memory-kompatible Spalten

| Spalte | Zielwert |
|---|---|
| domain | `longitudinal_real_world` |
| primary_score_name | `longitudinal_deviation_strength` |
| primary_score_value | Wert aus `longitudinal_deviation_strength` |
| context_name | z.B. `workday`, `off_day`, `unknown`, Survey-Kontext |
| evidence_scope | `longitudinal_real_world_sequence` |
| is_true_longitudinal_evidence | `True` |

## Datenschutz- und Scope-Regeln

Nicht in das kanonische subject-day-Format übernehmen:

- Audioinhalte.
- Transkripte.
- Freitextantworten.
- Standortverläufe.
- Bluetooth-/Proximity-Rohdaten mit Identifikationsrisiko.
- personenbezogene Rollen- oder Arbeitsplatzinformationen.

## Minimale Nutzbarkeit

Eine TILES-Tabelle gilt für diese Arbeit als minimal nutzbar, wenn sie enthält:

1. mindestens `subject_id`,
2. mindestens zwei Tage oder Beobachtungsfenster je ausgewähltem Subject,
3. mindestens eine physiologische oder behaviorale Messgröße,
4. eine interpretierbare Zeitachse,
5. keine nicht benötigten sensiblen Inhalte.

## Zwischenfazit

Dieses Schema hält TILES bewusst klein und methodisch kontrollierbar.

Der Fokus liegt nicht auf vollständiger TILES-Reproduktion, sondern auf der Frage, ob echte longitudinale Daten in dieselbe Dysbalance-Memory-Architektur überführt werden können.
