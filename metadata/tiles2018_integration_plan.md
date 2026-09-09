# TILES-2018 Integration Plan

Dieses Dokument beschreibt die geplante Rolle von TILES-2018 als echte longitudinale Erweiterung des Dysbalance-Frameworks.

## Rolle im Framework

TILES-2018 soll nicht als weiterer einfacher Klassifikationsdatensatz behandelt werden.

Die Rolle von TILES liegt in der Prüfung, ob die bisher kontrollierte Memory-Logik auf alltagsnahe, mehrtägige oder mehrwöchige physiologische und behaviorale Daten übertragen werden kann.

## Zentrale Frage

> Können wiederholte physiologische und behaviorale Signale aus einem naturalistischen Setting in Dysbalance Events, Episoden und longitudinale Hypothesen überführt werden?

## Abgrenzung zu bisherigen Datensätzen

| Dataset | Rolle | Evidenztyp |
|---|---|---|
| PAMAP2 | funktional-motorische Modellierung | kontrollierte Sequenz |
| WESAD | autonom-affektive Modellierung | kontrollierte Sequenz |
| MHEALTH | externe funktional-motorische Transferprüfung | kontrollierte Sequenz |
| TILES-2018 | longitudinale Realwelt-Erweiterung | echte Langzeitsequenz |

## Erwartete Modalitäten

Für das Framework sind zunächst nur Modalitäten relevant, die ohne Audioinhalt und ohne sensible Textinhalte ausgewertet werden können.

Priorität:

1. Fitbit-basierte Zeitreihen oder Tagesfeatures.
2. OMSignal-basierte physiologische Features.
3. Aktivitäts-, Schlaf- und Herzfrequenz-Zusammenfassungen.
4. Survey-basierte Stress-, Affect- oder Well-being-Labels als Kontextvariablen.
5. Umwelt- oder Näherungsdaten nur optional.

## Nicht-Ziele

TILES soll in dieser Arbeit nicht verwendet werden für:

- Audioinhalt oder Sprachinhalt.
- personenbezogene Identifikation.
- klinische Diagnostik.
- personenbezogene Leistungsbewertung.
- komplexe Arbeitsplatzüberwachung.
- vollständige Reproduktion aller TILES-Publikationsmodelle.

## Minimaler technischer Scope

Die minimal sinnvolle Integration besteht aus einer subject-day-Tabelle.

Empfohlenes Zielformat:

| Spalte | Bedeutung |
|---|---|
| dataset | `tiles2018` |
| subject_id | pseudonyme Teilnehmerkennung |
| day_index | fortlaufender Studientag |
| timestamp_start | Tagesbeginn oder Beobachtungsfensterbeginn |
| timestamp_end | Tagesende oder Beobachtungsfensterende |
| context_label | verfügbare Survey- oder Kontextinformation |
| hr_mean | mittlere Herzfrequenz |
| hr_std | Streuung der Herzfrequenz |
| activity_total | Aktivitäts- oder Schrittmaß |
| sleep_duration | Schlafdauer, falls vorhanden |
| sleep_quality | Schlafqualität, falls vorhanden |
| missingness_rate | Anteil fehlender Werte |
| primary_score_name | Name des Dysbalance Scores |
| primary_score_value | individueller Abweichungsscore |

## Dysbalance-Logik für TILES

Die erste TILES-Version sollte subject-normalisiert arbeiten.

Mögliche Score-Komponenten:

| Komponente | Interpretation |
|---|---|
| z_hr_mean | Abweichung der mittleren Herzfrequenz vom individuellen Referenzniveau |
| z_hr_variability | Abweichung der Herzfrequenzvariabilität |
| z_activity_total | Abweichung von üblicher Aktivität |
| z_sleep_duration | Abweichung von üblicher Schlafdauer |
| z_sleep_quality | Abweichung von üblicher Schlafqualität |
| z_stress_context | Survey-basierter Stresskontext, falls verfügbar |

Ein erster longitudinaler Dysbalance Score kann als robuste Kombination dieser Komponenten gebildet werden.

## Memory-Anbindung

TILES ist der erste Datensatz, bei dem `is_true_longitudinal_evidence = True` sinnvoll gesetzt werden kann.

Empfohlene Memory-Werte:

| Feld | Wert |
|---|---|
| dataset | `tiles2018` |
| domain | `longitudinal_real_world` |
| source_level | `subject_day` |
| evidence_scope | `longitudinal_real_world_sequence` |
| is_true_longitudinal_evidence | `True` |

## Erwartete Ergebnisse

TILES soll nicht primär hohe Klassifikationsleistung liefern.

Der wissenschaftliche Mehrwert liegt in:

1. echter Wiederholung über Tage oder Wochen,
2. subject-spezifischer Referenzbildung,
3. Verdichtung einzelner Auffälligkeiten zu Episoden,
4. vorsichtiger Hypothesenbildung statt Diagnose,
5. Vorbereitung eigener Garmin-/Polar-Pilotdaten.

## Risiken

| Risiko | Umgang |
|---|---|
| Zugriff benötigt Login oder DUA | zunächst nur Plan und Import-Schnittstelle vorbereiten |
| starke Missingness | Missingness als Feature und Qualitätskriterium erfassen |
| heterogene Modalitäten | minimalen subject-day-Kern definieren |
| Datenschutzsensibilität | keine Audio-, Text- oder Identifikationsdaten verwenden |
| hoher Integrationsaufwand | TILES zunächst als fokussierte Feasibility-Integration behandeln |

## Entscheidungspunkt

TILES wird in dieser Arbeit integriert, wenn mindestens eine longitudinale, subject-bezogene physiologische oder behaviorale Tabelle zugänglich und rechtlich nutzbar ist.

Wenn kein Zugriff innerhalb der Projektzeit möglich ist, bleibt TILES als begründete Framework-Erweiterung und Motivation für eigene Garmin-/Polar-Daten erhalten.

## Nächste technische Schritte

1. Lokale Ordnerstruktur für TILES vorbereiten.
2. Erwartetes Dateninventar dokumentieren.
3. Import-Schema für subject-day-Features definieren.
4. Feasibility-Check-Skript erstellen.
5. Erst danach entscheiden, ob eine echte TILES-Pipeline implementiert wird.

## Zwischenfazit

TILES-2018 ist der logisch nächste Datensatz, weil er die bisherige controlled-window-Logik in eine echte longitudinale Realweltstruktur überführen kann.

Die Integration muss fokussiert, datenschutzsensibel und methodisch vorsichtig erfolgen.
