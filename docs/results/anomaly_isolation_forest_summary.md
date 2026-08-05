# Isolation Forest Anomaly Detection Summary

## Rolle im Framework

Dieses Dokument fasst die erste modellbasierte Anomaly-Detection-Auswertung des Dysbalance-Frameworks zusammen.

Die Anomaly Detection dient nicht als Ersatz für die erklärbaren Dysbalance-Scores. Sie ergänzt diese um eine datengetriebene Perspektive:

- Dysbalance-Scoring: physiologisch motiviert und erklärbar
- Anomaly Detection: modellbasierte Erkennung ungewöhnlicher Fenster
- Vergleich beider Perspektiven: Prüfung, ob ungewöhnliche Modellentscheidungen mit erklärbaren Abweichungsscores zusammenhängen

Damit beantwortet dieser Teilabschnitt die Frage, ob personalisierte physiologische Abweichungen nicht nur über Schwellenwerte, sondern auch über ein datengetriebenes Anomaly-Modell sichtbar werden.

## Methodische Einordnung

Als erste Anomaly-Baseline wurde Isolation Forest verwendet.

Gründe:

- geeignet für tabellarische Feature- und Score-Räume
- robust als erste unsupervised Baseline
- benötigt keine klinischen Anomalie-Labels
- skaliert gut auf die vorhandenen Fensterzahlen
- kann mit niedriger dimensionalen, interpretierbaren Feature-Sets verwendet werden

Die Auswertung verwendet bewusst keine Rohsignal-Tensoren. Stattdessen werden bereits berechnete Feature- und Score-Tabellen verwendet. Dadurch bleibt die Analyse näher an der erklärbaren Dysbalance-Logik.

## Verwendete Feature-Ebenen

Für beide Datensätze wurden drei Ebenen untersucht.

### Score-Level

Diese Ebene nutzt finale Dysbalance-Scores.

PAMAP2:

- `functional_deviation_strength`

WESAD:

- `z_autonomic_activation`
- `autonomic_deviation_strength`

### Component-Level

Diese Ebene nutzt erklärbare normalisierte Score-Komponenten.

PAMAP2:

- `z_total_acc_rms`
- `z_log_extremity_chest_acc_ratio`
- `z_log_hand_ankle_acc_ratio`

WESAD:

- `z_hr_bpm`
- `z_eda_mean`
- `z_resp_std`
- `z_inverse_rmssd`

### Feature-Level

Diese Ebene nutzt ausgewählte physiologische Features vor der finalen Score-Aggregation.

PAMAP2:

- `total_acc_rms`
- `log_extremity_chest_acc_ratio`
- `log_hand_ankle_acc_ratio`

WESAD:

- `hr_bpm`
- `rmssd_ms`
- `eda_mean`
- `resp_std`

## Contamination-Parameter

Es wurden drei Contamination-Werte getestet:

- `0.02`
- `0.05`
- `0.10`

Der Contamination-Wert gibt an, welcher Anteil der Fenster global ungefähr als anomal markiert werden soll.

Beispiel:

Bei `contamination = 0.05` erwartet man global ungefähr 5 % Modell-Anomalien. Wenn eine einzelne Bedingung eine deutlich höhere Rate zeigt, z.B. 8 %, dann ist diese Bedingung unter den Modell-Anomalien überrepräsentiert.

Wichtig:

Eine Anomaly-Rate von 8 % bedeutet nicht, dass 8 % der Fenster klinisch auffällig oder krankhaft sind. Sie bedeutet nur, dass 8 % der Fenster dieser Gruppe vom Modell als ungewöhnlich relativ zur gelernten Datenverteilung markiert wurden.

## Erzeugte Artefakte

Die Auswertung erzeugte lokale Reports unter:

- `reports/anomaly/`

Zentrale Dateien:

- `reports/anomaly/isolation_forest_anomaly_scores_all.csv`
- `reports/anomaly/isolation_forest_overall_summary.json`
- `reports/anomaly/pamap2_isolation_forest_anomaly_scores.csv`
- `reports/anomaly/pamap2_isolation_forest_summary_by_subject.csv`
- `reports/anomaly/pamap2_isolation_forest_summary_by_condition.csv`
- `reports/anomaly/pamap2_isolation_forest_overlap_with_thresholds.csv`
- `reports/anomaly/pamap2_isolation_forest_top_windows.csv`
- `reports/anomaly/wesad_isolation_forest_anomaly_scores.csv`
- `reports/anomaly/wesad_isolation_forest_summary_by_subject.csv`
- `reports/anomaly/wesad_isolation_forest_summary_by_condition.csv`
- `reports/anomaly/wesad_isolation_forest_overlap_with_thresholds.csv`
- `reports/anomaly/wesad_isolation_forest_top_windows.csv`

Die Reports sind lokal erzeugte Analyseartefakte und werden nicht im Git-Repository versioniert.

## WESAD: Erste Beobachtungen

Für WESAD wurde im Component-Level bei `contamination = 0.05` folgende modellbasierte Anomaly-Rate nach Zustand beobachtet:

| Zustand | Anomaly-Rate |
|---|---:|
| baseline | 3.82 % |
| stress | 8.15 % |
| amusement | 2.93 % |
| meditation | 5.09 % |

### Interpretation

Stress zeigt mit 8.15 % die höchste Anomaly-Rate. Da der globale Contamination-Wert bei 5 % liegt, sind Stress-Fenster unter den Modell-Anomalien überrepräsentiert.

Das ist wissenschaftlich relevant, weil WESAD-Stress bereits im Autonomic Dysbalance Score klar erhöhte Werte zeigte. Die Anomaly Detection bestätigt diese Richtung aus einer datengetriebenen Perspektive.

Die Beobachtung kann so interpretiert werden:

Stress-Fenster liegen im komponentenbasierten autonomen Merkmalsraum häufiger außerhalb der vom Isolation Forest gelernten Hauptverteilung.

### Zusammenhang zur vorherigen Dysbalance-Auswertung

Vorherige WESAD-Auswertung:

- Stress hatte die höchste mittlere `z_autonomic_activation`
- Stress überschritt Aktivierungsschwellen deutlich häufiger als baseline, amusement und meditation

Neue Anomaly-Auswertung:

- Stress zeigt auch im modellbasierten Component-Level die höchste Anomaly-Rate

Damit ergibt sich eine konsistente Evidenzlinie:

1. physiologisch motivierter Score zeigt Stress-Aktivierung
2. threshold-basierte Auswertung zeigt häufigere starke Aktivierung
3. Isolation Forest markiert Stress-Fenster häufiger als ungewöhnlich

## PAMAP2: Erste Beobachtungen

Für PAMAP2 wurde im Component-Level bei `contamination = 0.05` folgende modellbasierte Anomaly-Rate nach Aktivität beobachtet:

| Aktivität | Anomaly-Rate |
|---|---:|
| descending stairs | 8.12 % |
| ascending stairs | 7.19 % |
| lying | 6.99 % |
| running | 6.25 % |
| rope jumping | 6.06 % |
| sitting | 5.21 % |
| standing | 4.68 % |
| ironing | 4.57 % |
| vacuum cleaning | 4.35 % |
| Nordic walking | 3.64 % |
| cycling | 3.55 % |
| walking | 3.50 % |

### Interpretation

Treppensteigen zeigt die höchsten Anomaly-Raten. Das ist plausibel, weil Treppenbewegungen komplexer, asymmetrischer und stärker phasenabhängig sein können als einfache zyklische Aktivitäten wie Walking oder Cycling.

Running und Rope Jumping zeigen ebenfalls erhöhte Werte, was mit stärkerer Bewegungsintensität und höherer Dynamik vereinbar ist.

Die erhöhte Rate bei `lying` muss vorsichtig interpretiert werden. Sie könnte weniger eine funktionale Dysbalance anzeigen, sondern eher eine modellbasierte Auffälligkeit statischer Sensorlage- oder Ratio-Muster. Gerade bei sehr niedriger Bewegung können log-ratio-basierte Komponenten empfindlich auf kleine Unterschiede reagieren.

### Bedeutung für das Framework

PAMAP2 zeigt, dass Anomaly Detection nicht nur Intensität findet, sondern auch Aktivitäten identifizieren kann, deren Bewegungsstruktur relativ zur Gesamtdatenverteilung ungewöhnlicher ist.

Dabei bleibt wichtig:

Die Anomaly-Rate ist kein direktes Gesundheitsmaß. Sie beschreibt nur eine modellbasierte Abweichung innerhalb der gewählten Feature-Repräsentation.

## Wissenschaftliche Bedeutung

Die ersten Isolation-Forest-Ergebnisse unterstützen den methodischen Aufbau der Arbeit.

Für WESAD zeigt sich:

- Stress ist nicht nur klassifizierbar.
- Stress ist nicht nur über einen erklärbaren autonomen Score erhöht.
- Stress ist auch modellbasiert häufiger anomal.

Für PAMAP2 zeigt sich:

- Aktivitäten unterscheiden sich in ihrer modellbasierten Auffälligkeit.
- Besonders komplexe oder dynamische Bewegungen können erhöhte Anomaly-Raten erzeugen.
- Einzelne Auffälligkeiten müssen physiologisch und methodisch interpretiert werden.

Damit ergänzt Anomaly Detection die bisherigen Framework-Bausteine:

- Supervised Baselines prüfen Signalgehalt.
- Dysbalance Scores liefern erklärbare physiologische Abweichungen.
- Anomaly Detection liefert eine zusätzliche datengetriebene Sicht auf ungewöhnliche Fenster.

## Anschlussfähigkeit für spätere Pilotdaten

Das aktuelle Anomaly-Schema enthält bereits Felder wie:

- `dataset`
- `domain`
- `session_id`
- `subject_id`
- `window_index`
- `feature_set`
- `anomaly_score`
- `anomaly_score_z`
- `anomaly_rank_percent`
- `is_model_anomaly`

Damit kann das Schema später auf eigene Pilotdaten übertragen werden.

Ein späterer Polar-Brustgurt- oder Multisensor-Test kann als explorativer Pilot angeschlossen werden, z.B. mit:

- `dataset = polar_pilot`
- `domain = autonomic` oder `mixed_sensor`
- `subject_id = pilot_001`
- `session_id = konkrete Messsession`

Der Pilot-Test wäre keine klinische Validierung, sondern eine Demonstration, wie das Framework auf neue Sensordaten angewendet werden kann.

## Grenzen

Die Ergebnisse müssen vorsichtig interpretiert werden.

Wichtige Einschränkungen:

- Es gibt keine klinischen Anomalie-Labels.
- Der Contamination-Parameter beeinflusst die Anzahl markierter Fenster.
- PAMAP2 besitzt keinen klaren Normalzustand.
- WESAD-Stress ist ein experimenteller Zustand und keine medizinische Diagnose.
- Anomaly Detection hängt von der gewählten Feature-Repräsentation ab.
- Hohe Anomaly-Raten müssen immer mit Feature-Komponenten und Kontext interpretiert werden.

## Nächste Schritte

1. Overlap zwischen modellbasierten Anomalien und Score-Thresholds genauer auswerten.
2. Top-Anomaly-Windows pro Datensatz interpretieren.
3. Visualisierungen für Anomaly Scores erzeugen.
4. Prüfen, ob One-Class SVM und LOF als Vergleichsmodelle notwendig sind.
5. Anomaly-Ausgaben als Input für Longitudinal Dysbalance Memory vorbereiten.

## Overlap zwischen Isolation Forest und Dysbalance-Thresholds

Nach der ersten Anomaly-Auswertung wurde geprüft, wie stark die modellbasierten Isolation-Forest-Anomalien mit den bereits vorhandenen Dysbalance-Thresholds überlappen.

Diese Analyse ist methodisch wichtig, weil sie zeigt, ob das datengetriebene Modell ähnliche Fenster als auffällig bewertet wie die erklärbaren Score-basierten Dysbalance-Regeln.

## PAMAP2 Overlap

Für PAMAP2 wurde der Component-Level Isolation Forest bei `contamination = 0.05` mit dem Threshold auf `functional_deviation_strength` verglichen.

| Threshold | Model-Anomalien | Threshold-Anomalien | Overlap | Overlap der Modell-Anomalien | Overlap der Threshold-Anomalien | Jaccard |
|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 380 | 517 | 375 | 98.68 % | 72.53 % | 0.7184 |
| 2.0 | 380 | 306 | 304 | 80.00 % | 99.35 % | 0.7958 |
| 2.5 | 380 | 206 | 206 | 54.21 % | 100.00 % | 0.5421 |

Interpretation:

PAMAP2 zeigt eine sehr starke Übereinstimmung zwischen modellbasierter Anomaly Detection und erklärbarem funktionalem Dysbalance-Score.

Besonders bei `functional_deviation_strength > 2.0` werden fast alle Threshold-Anomalien auch durch den Isolation Forest gefunden. Gleichzeitig überschreiten 80 % der Modell-Anomalien diesen Dysbalance-Threshold.

Das spricht dafür, dass der funktionale Dysbalance-Score eine Struktur im Bewegungsfeature-Raum abbildet, die auch ein datengetriebenes Modell als ungewöhnlich erkennt.

Die Top-Anomaly-Windows bestätigen diese Interpretation, da die höchsten Modell-Anomalien sehr hohe Werte der `functional_deviation_strength` aufweisen.

## WESAD Overlap

Für WESAD wurde der Component-Level Isolation Forest bei `contamination = 0.05` mit zwei Threshold-Referenzen verglichen:

- `z_autonomic_activation`
- `autonomic_deviation_strength`

### Gerichtete autonome Aktivierung

| Threshold | Model-Anomalien | Threshold-Anomalien | Overlap | Overlap der Modell-Anomalien | Overlap der Threshold-Anomalien | Jaccard |
|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 445 | 968 | 198 | 44.49 % | 20.45 % | 0.1630 |
| 2.0 | 445 | 391 | 150 | 33.71 % | 38.36 % | 0.2187 |
| 2.5 | 445 | 121 | 92 | 20.67 % | 76.03 % | 0.1941 |

### Ungerichtete autonome Abweichungsstärke

| Threshold | Model-Anomalien | Threshold-Anomalien | Overlap | Overlap der Modell-Anomalien | Overlap der Threshold-Anomalien | Jaccard |
|---:|---:|---:|---:|---:|---:|---:|
| 1.5 | 445 | 396 | 298 | 66.97 % | 75.25 % | 0.5488 |
| 2.0 | 445 | 76 | 76 | 17.08 % | 100.00 % | 0.1708 |
| 2.5 | 445 | 12 | 12 | 2.70 % | 100.00 % | 0.0270 |

Interpretation:

WESAD zeigt ein differenzierteres Bild als PAMAP2.

Der Overlap mit `z_autonomic_activation` ist moderat. Das bedeutet, dass gerichtete autonome Aktivierung und modellbasierte Auffälligkeit nicht identisch sind.

Der Overlap mit `autonomic_deviation_strength` ist deutlich stärker. Besonders auffällig ist, dass alle Fenster mit `autonomic_deviation_strength > 2.0` auch durch den Isolation Forest als Anomalien erkannt werden.

Damit zeigt WESAD, dass Isolation Forest vor allem starke ungerichtete autonome Komponentenabweichungen erkennt, nicht nur gerichtete Stress-Aktivierung.

## Bedeutung der Top-WESAD-Anomalien

Die Top-WESAD-Anomalien liegen teilweise im Zustand `baseline`.

Das ist kein Widerspruch zur vorherigen Stress-Auswertung. Es zeigt vielmehr, dass modellbasierte Anomaly Detection eine andere Frage beantwortet.

`z_autonomic_activation` beschreibt gerichtete autonome Aktivierung.

`autonomic_deviation_strength` beschreibt ungerichtete physiologische Auffälligkeit.

Ein Fenster kann deshalb eine hohe ungerichtete Abweichungsstärke besitzen, ohne gleichzeitig stark stress-aktiviert zu sein.

Diese Unterscheidung ist für das Framework wichtig, weil sie zeigt, dass unterschiedliche Dysbalance-Perspektiven verschiedene physiologische Phänomene sichtbar machen.

## Zwischenfazit der Overlap-Analyse

Die Overlap-Analyse liefert eine wichtige methodische Erkenntnis:

PAMAP2 zeigt eine sehr starke Übereinstimmung zwischen funktionalem Dysbalance-Score und modellbasierter Anomaly Detection.

WESAD zeigt eine stärkere Übereinstimmung zwischen Isolation Forest und ungerichteter autonomer Abweichungsstärke als zwischen Isolation Forest und gerichteter autonomer Aktivierung.

Damit wird deutlich:

- Score-basierte Dysbalance und Modell-Anomalien können stark übereinstimmen.
- Die Stärke der Übereinstimmung hängt von Domäne und Score-Definition ab.
- Gerichtete Aktivierung und allgemeine Auffälligkeit müssen getrennt interpretiert werden.
- Anomaly Detection ergänzt die erklärbaren Scores, ersetzt sie aber nicht.

## Korrelation zwischen Anomaly Scores und Dysbalance Scores

Zusätzlich zur Overlap-Analyse wurden Pearson- und Spearman-Korrelationen zwischen den Isolation-Forest-Anomaly-Scores und den zentralen Dysbalance-Scores berechnet.

Ausgewertet wurde jeweils der Component-Level Isolation Forest bei `contamination = 0.05`.

| Datensatz / Score | Pearson | Spearman |
|---|---:|---:|
| PAMAP2: `functional_deviation_strength` vs. `anomaly_score` | 0.9499 | 0.9480 |
| WESAD: `z_autonomic_activation` vs. `anomaly_score` | 0.3955 | 0.3171 |
| WESAD: `autonomic_deviation_strength` vs. `anomaly_score` | 0.9034 | 0.8458 |

### Interpretation

PAMAP2 zeigt eine sehr starke lineare und rangbasierte Beziehung zwischen `functional_deviation_strength` und `anomaly_score`.

Das bedeutet, dass die modellbasierte Anomaly Detection nahezu dieselbe Auffälligkeitsstruktur erfasst wie der erklärbare funktionale Dysbalance-Score. Dies stärkt die methodische Belastbarkeit des PAMAP2-Dysbalance-Scores.

Bei WESAD ist die Korrelation zwischen `z_autonomic_activation` und `anomaly_score` nur moderat. Das zeigt, dass gerichtete autonome Aktivierung und modellbasierte Auffälligkeit nicht identisch sind.

Deutlich stärker ist der Zusammenhang zwischen `autonomic_deviation_strength` und `anomaly_score`. Die hohe Korrelation zeigt, dass Isolation Forest bei WESAD vor allem ungerichtete autonome Komponentenabweichungen erkennt.

Damit bestätigt die Korrelationsanalyse die vorherige Overlap-Interpretation:

- PAMAP2: funktionaler Dysbalance-Score und Modell-Anomalie stimmen sehr stark überein.
- WESAD: Modell-Anomalie stimmt stärker mit ungerichteter autonomer Abweichungsstärke überein als mit gerichteter autonomer Aktivierung.
- Gerichtete Aktivierung und allgemeine physiologische Auffälligkeit müssen getrennt interpretiert werden.

